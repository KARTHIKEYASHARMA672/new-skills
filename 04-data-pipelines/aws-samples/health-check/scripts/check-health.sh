#!/usr/bin/env bash
# check-health.sh — 多服务健康巡检（CloudWatch 指标直查）
#
# 用法: check-health.sh <account-id> <region> [--service <name>] [--hours N]
#
# 输出:
#   stdout: JSON 格式的健康摘要（供 Claude 解析）
#   stderr: 进度日志
#
# 对每个服务查 CloudWatch 关键指标，同时检查告警状态。
# 不依赖告警配置——直接查指标值判断健康。

set -euo pipefail

# ── 参数解析 ──────────────────────────────────────────────
ACCOUNT_ID=""
REGION=""
SERVICE_FILTER=""
HOURS_BACK=1

show_help() {
    cat >&2 <<'HELP'
用法: check-health.sh <account-id> <region> [options]

多服务健康巡检：查 CloudWatch 指标 + 告警状态。

参数:
  account-id    AWS 账号 ID
  region        AWS Region

选项:
  --service <name>  只检查指定服务（默认检查所有）
  --hours N         查询最近 N 小时（默认 1）
  --help, -h        显示帮助

示例:
  check-health.sh <account-id> ap-northeast-1
  check-health.sh <account-id> ap-northeast-1 --service payments-api
  check-health.sh <account-id> ap-northeast-1 --hours 6
HELP
    exit 0
}

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h) show_help ;;
        --service) SERVICE_FILTER="$2"; shift 2 ;;
        --hours) HOURS_BACK="$2"; shift 2 ;;
        *) POSITIONAL+=("$1"); shift ;;
    esac
done

ACCOUNT_ID="${POSITIONAL[0]:-}"
REGION="${POSITIONAL[1]:-}"

if [[ -z "$ACCOUNT_ID" || -z "$REGION" ]]; then
    echo '{"error": "缺少必需参数。用法: check-health.sh <account-id> <region>"}' >&2
    exit 1
fi

# ── 辅助函数 ──────────────────────────────────────────────
log() { echo "[health-check] $*" >&2; }

# 时间范围
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_TIME=$(date -u -v-${HOURS_BACK}H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "${HOURS_BACK} hours ago" +"%Y-%m-%dT%H:%M:%SZ")

log "巡检范围: Account=$ACCOUNT_ID Region=$REGION Hours=$HOURS_BACK"
log "时间窗口: $START_TIME → $END_TIME"

# ── Phase 1: 告警状态 ────────────────────────────────────
check_alarms() {
    log "Phase 1: 查询告警状态..."

    local alarms_json
    alarms_json=$(aws cloudwatch describe-alarms \
        --region "$REGION" \
        --output json 2>/dev/null) || {
        log "告警查询失败"
        echo '{"alarms": {"status": "error"}}'
        return 1
    }

    local alarm_summary
    alarm_summary=$(echo "$alarms_json" | jq '{
        total: (.MetricAlarms | length),
        in_alarm: [.MetricAlarms[] | select(.StateValue == "ALARM")] | length,
        insufficient: [.MetricAlarms[] | select(.StateValue == "INSUFFICIENT_DATA")] | length,
        ok: [.MetricAlarms[] | select(.StateValue == "OK")] | length,
        details: [.MetricAlarms[] | select(.StateValue != "OK") | {
            name: .AlarmName,
            state: .StateValue,
            metric: .MetricName,
            namespace: .Namespace
        }]
    }')

    echo "$alarm_summary"
    log "Phase 1 完成: $(echo "$alarm_summary" | jq '.in_alarm') ALARM, $(echo "$alarm_summary" | jq '.insufficient') INSUFFICIENT_DATA"
}

# ── Phase 2: EKS 健康检查 ────────────────────────────────
check_eks_health() {
    local cluster_name="$1"
    log "  EKS: $cluster_name"

    # 检查集群状态
    local cluster_status
    cluster_status=$(aws eks describe-cluster \
        --name "$cluster_name" \
        --region "$REGION" \
        --query 'cluster.status' \
        --output text 2>/dev/null) || cluster_status="UNKNOWN"

    # Container Insights 指标：node CPU
    local node_cpu
    node_cpu=$(aws cloudwatch get-metric-statistics \
        --namespace ContainerInsights \
        --metric-name node_cpu_utilization \
        --dimensions Name=ClusterName,Value="$cluster_name" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Average Maximum \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            avg: ([.Datapoints[].Average] | if length > 0 then add / length else null end),
            max: ([.Datapoints[].Maximum] | max // null),
            datapoints: (.Datapoints | length)
        }') || node_cpu='{"avg":null,"max":null,"datapoints":0}'

    # Pod restarts
    local pod_restarts
    pod_restarts=$(aws cloudwatch get-metric-statistics \
        --namespace ContainerInsights \
        --metric-name pod_number_of_container_restarts \
        --dimensions Name=ClusterName,Value="$cluster_name" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Sum Maximum \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            total: ([.Datapoints[].Sum] | add // 0),
            max_per_period: ([.Datapoints[].Maximum] | max // 0),
            datapoints: (.Datapoints | length)
        }') || pod_restarts='{"total":0,"max_per_period":0,"datapoints":0}'

    # 判断健康状态
    local status="HEALTHY"
    local issues="[]"

    local max_cpu
    max_cpu=$(echo "$node_cpu" | jq '.max // 0')
    if (( $(echo "$max_cpu > 95" | bc -l 2>/dev/null || echo 0) )); then
        status="CRITICAL"
        issues=$(echo "$issues" | jq '. + ["node CPU > 95%: '"$max_cpu"'%"]')
    elif (( $(echo "$max_cpu > 80" | bc -l 2>/dev/null || echo 0) )); then
        if [[ "$status" != "CRITICAL" ]]; then status="DEGRADED"; fi
        issues=$(echo "$issues" | jq '. + ["node CPU > 80%: '"$max_cpu"'%"]')
    fi

    local restart_total
    restart_total=$(echo "$pod_restarts" | jq '.total')
    if (( $(echo "$restart_total > 10" | bc -l 2>/dev/null || echo 0) )); then
        status="CRITICAL"
        issues=$(echo "$issues" | jq '. + ["pod restarts > 10/h: '"$restart_total"'"]')
    elif (( $(echo "$restart_total > 3" | bc -l 2>/dev/null || echo 0) )); then
        if [[ "$status" != "CRITICAL" ]]; then status="DEGRADED"; fi
        issues=$(echo "$issues" | jq '. + ["pod restarts > 3/h: '"$restart_total"'"]')
    fi

    if [[ $(echo "$node_cpu" | jq '.datapoints') == "0" ]]; then
        status="UNKNOWN"
        issues=$(echo "$issues" | jq '. + ["无 Container Insights 数据（可能未开启）"]')
    fi

    jq -n \
        --arg name "$cluster_name" \
        --arg type "eks" \
        --arg cluster_status "$cluster_status" \
        --arg status "$status" \
        --argjson node_cpu "$node_cpu" \
        --argjson pod_restarts "$pod_restarts" \
        --argjson issues "$issues" \
        '{
            name: $name,
            type: $type,
            cluster_status: $cluster_status,
            health: $status,
            metrics: {node_cpu: $node_cpu, pod_restarts: $pod_restarts},
            issues: $issues
        }'
}

# ── Phase 3: RDS 健康检查 ────────────────────────────────
check_rds_health() {
    local db_identifier="$1"
    local is_cluster="$2"  # "true" or "false"
    log "  RDS: $db_identifier (cluster=$is_cluster)"

    local ns_dimension
    if [[ "$is_cluster" == "true" ]]; then
        ns_dimension="Name=DBClusterIdentifier,Value=$db_identifier"
    else
        ns_dimension="Name=DBInstanceIdentifier,Value=$db_identifier"
    fi

    # CPU
    local cpu
    cpu=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/RDS \
        --metric-name CPUUtilization \
        --dimensions "$ns_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Average Maximum \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            avg: ([.Datapoints[].Average] | if length > 0 then add / length else null end),
            max: ([.Datapoints[].Maximum] | max // null)
        }') || cpu='{"avg":null,"max":null}'

    # FreeableMemory
    local memory
    memory=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/RDS \
        --metric-name FreeableMemory \
        --dimensions "$ns_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Minimum Average \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            min_bytes: ([.Datapoints[].Minimum] | min // null),
            avg_bytes: ([.Datapoints[].Average] | if length > 0 then add / length else null end),
            min_mb: (([.Datapoints[].Minimum] | min // 0) / 1048576 | floor)
        }') || memory='{"min_bytes":null,"avg_bytes":null,"min_mb":null}'

    # DatabaseConnections
    local connections
    connections=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/RDS \
        --metric-name DatabaseConnections \
        --dimensions "$ns_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Maximum Average \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            max: ([.Datapoints[].Maximum] | max // null),
            avg: ([.Datapoints[].Average] | if length > 0 then add / length else null end)
        }') || connections='{"max":null,"avg":null}'

    # 判断健康状态
    local status="HEALTHY"
    local issues="[]"

    local max_cpu
    max_cpu=$(echo "$cpu" | jq '.max // 0')
    if (( $(echo "$max_cpu > 95" | bc -l 2>/dev/null || echo 0) )); then
        status="CRITICAL"
        issues=$(echo "$issues" | jq '. + ["CPU > 95%: '"$max_cpu"'%"]')
    elif (( $(echo "$max_cpu > 80" | bc -l 2>/dev/null || echo 0) )); then
        if [[ "$status" != "CRITICAL" ]]; then status="DEGRADED"; fi
        issues=$(echo "$issues" | jq '. + ["CPU > 80%: '"$max_cpu"'%"]')
    fi

    local min_mem_mb
    min_mem_mb=$(echo "$memory" | jq '.min_mb // 99999')
    if (( min_mem_mb < 100 )); then
        status="CRITICAL"
        issues=$(echo "$issues" | jq '. + ["FreeableMemory < 100MB: '"$min_mem_mb"'MB"]')
    elif (( min_mem_mb < 500 )); then
        if [[ "$status" != "CRITICAL" ]]; then status="DEGRADED"; fi
        issues=$(echo "$issues" | jq '. + ["FreeableMemory < 500MB: '"$min_mem_mb"'MB"]')
    fi

    jq -n \
        --arg name "$db_identifier" \
        --arg type "rds" \
        --argjson is_cluster "$is_cluster" \
        --arg status "$status" \
        --argjson cpu "$cpu" \
        --argjson memory "$memory" \
        --argjson connections "$connections" \
        --argjson issues "$issues" \
        '{
            name: $name,
            type: $type,
            is_cluster: $is_cluster,
            health: $status,
            metrics: {cpu: $cpu, memory: $memory, connections: $connections},
            issues: $issues
        }'
}

# ── Phase 4: ALB 健康检查 ────────────────────────────────
check_alb_health() {
    local alb_arn="$1"
    local alb_name
    alb_name=$(echo "$alb_arn" | sed 's|.*loadbalancer/||' || echo "$alb_arn")
    # CloudWatch dimension format: app/alb-name/hash
    local alb_dimension
    alb_dimension=$(echo "$alb_arn" | sed 's|.*loadbalancer/||' || echo "")
    log "  ALB: $alb_name"

    if [[ -z "$alb_dimension" ]]; then
        echo '{"name":"unknown","type":"alb","health":"UNKNOWN","issues":["无法解析 ALB ARN"]}'
        return
    fi

    # 5xx count
    local target_5xx
    target_5xx=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/ApplicationELB \
        --metric-name HTTPCode_Target_5XX_Count \
        --dimensions Name=LoadBalancer,Value="$alb_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Sum \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            total: ([.Datapoints[].Sum] | add // 0),
            max_per_period: ([.Datapoints[].Sum] | max // 0)
        }') || target_5xx='{"total":0,"max_per_period":0}'

    # RequestCount for ratio
    local request_count
    request_count=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/ApplicationELB \
        --metric-name RequestCount \
        --dimensions Name=LoadBalancer,Value="$alb_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Sum \
        --region "$REGION" \
        --output json 2>/dev/null | jq '([.Datapoints[].Sum] | add // 0)') || request_count=0

    # TargetResponseTime
    local response_time
    response_time=$(aws cloudwatch get-metric-statistics \
        --namespace AWS/ApplicationELB \
        --metric-name TargetResponseTime \
        --dimensions Name=LoadBalancer,Value="$alb_dimension" \
        --start-time "$START_TIME" \
        --end-time "$END_TIME" \
        --period 300 \
        --statistics Average p99 \
        --region "$REGION" \
        --output json 2>/dev/null | jq '{
            avg: ([.Datapoints[].Average] | if length > 0 then add / length else null end),
            p99: ([.Datapoints[] | .ExtendedStatistics.p99 // .Average] | max // null)
        }') || response_time='{"avg":null,"p99":null}'

    # 判断健康
    local status="HEALTHY"
    local issues="[]"
    local total_5xx
    total_5xx=$(echo "$target_5xx" | jq '.total')
    local error_rate=0
    if (( $(echo "$request_count > 0" | bc -l 2>/dev/null || echo 0) )); then
        error_rate=$(echo "scale=4; $total_5xx / $request_count * 100" | bc -l 2>/dev/null || echo 0)
    fi

    if (( $(echo "$error_rate > 5" | bc -l 2>/dev/null || echo 0) )); then
        status="CRITICAL"
        issues=$(echo "$issues" | jq '. + ["5xx 率 > 5%: '"$error_rate"'%"]')
    elif (( $(echo "$error_rate > 1" | bc -l 2>/dev/null || echo 0) )); then
        if [[ "$status" != "CRITICAL" ]]; then status="DEGRADED"; fi
        issues=$(echo "$issues" | jq '. + ["5xx 率 > 1%: '"$error_rate"'%"]')
    fi

    jq -n \
        --arg name "$alb_name" \
        --arg type "alb" \
        --arg status "$status" \
        --argjson target_5xx "$target_5xx" \
        --argjson request_count "$request_count" \
        --argjson response_time "$response_time" \
        --arg error_rate "$error_rate" \
        --argjson issues "$issues" \
        '{
            name: $name,
            type: $type,
            health: $status,
            metrics: {target_5xx: $target_5xx, request_count: $request_count, response_time: $response_time, error_rate_pct: $error_rate},
            issues: $issues
        }'
}

# ── 主流程：发现并检查资源 ────────────────────────────────
main() {
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Phase 1: 告警
    local alarm_result
    alarm_result=$(check_alarms) || alarm_result='{"status":"error"}'

    # Phase 2-4: 发现并检查各类资源
    local service_results="[]"

    # EKS clusters
    log "Phase 2: 发现 EKS 集群..."
    local clusters
    clusters=$(aws eks list-clusters --region "$REGION" --output json 2>/dev/null | jq -r '.clusters[]' 2>/dev/null) || clusters=""

    while IFS= read -r cluster; do
        [[ -z "$cluster" ]] && continue
        if [[ -n "$SERVICE_FILTER" && "$cluster" != *"$SERVICE_FILTER"* ]]; then continue; fi
        local result
        result=$(check_eks_health "$cluster") || result='{"name":"'"$cluster"'","type":"eks","health":"ERROR"}'
        service_results=$(echo "$service_results" | jq --argjson r "$result" '. + [$r]')
    done <<< "$clusters"

    # RDS clusters
    log "Phase 3: 发现 RDS 实例/集群..."
    local rds_clusters
    rds_clusters=$(aws rds describe-db-clusters --region "$REGION" --output json 2>/dev/null | jq -r '.DBClusters[].DBClusterIdentifier' 2>/dev/null) || rds_clusters=""

    while IFS= read -r db; do
        [[ -z "$db" ]] && continue
        if [[ -n "$SERVICE_FILTER" && "$db" != *"$SERVICE_FILTER"* ]]; then continue; fi
        local result
        result=$(check_rds_health "$db" "true") || result='{"name":"'"$db"'","type":"rds","health":"ERROR"}'
        service_results=$(echo "$service_results" | jq --argjson r "$result" '. + [$r]')
    done <<< "$rds_clusters"

    # ALBs
    log "Phase 4: 发现 ALB..."
    local albs
    albs=$(aws elbv2 describe-load-balancers --region "$REGION" --output json 2>/dev/null | jq -r '.LoadBalancers[] | select(.Type == "application") | .LoadBalancerArn' 2>/dev/null) || albs=""

    while IFS= read -r alb; do
        [[ -z "$alb" ]] && continue
        local alb_short
        alb_short=$(echo "$alb" | sed 's|.*loadbalancer/app/||' | cut -d'/' -f1 || echo "$alb")
        if [[ -n "$SERVICE_FILTER" && "$alb_short" != *"$SERVICE_FILTER"* ]]; then continue; fi
        local result
        result=$(check_alb_health "$alb") || result='{"name":"'"$alb_short"'","type":"alb","health":"ERROR"}'
        service_results=$(echo "$service_results" | jq --argjson r "$result" '. + [$r]')
    done <<< "$albs"

    # 汇总
    local overall="HEALTHY"
    local critical_count
    critical_count=$(echo "$service_results" | jq '[.[] | select(.health == "CRITICAL")] | length')
    local degraded_count
    degraded_count=$(echo "$service_results" | jq '[.[] | select(.health == "DEGRADED")] | length')
    local unknown_count
    unknown_count=$(echo "$service_results" | jq '[.[] | select(.health == "UNKNOWN")] | length')

    if [[ "$critical_count" -gt 0 ]]; then
        overall="CRITICAL"
    elif [[ "$degraded_count" -gt 0 ]]; then
        overall="DEGRADED"
    elif [[ "$unknown_count" -gt 0 && $(echo "$service_results" | jq length) -eq "$unknown_count" ]]; then
        overall="UNKNOWN"
    fi

    # 输出
    jq -n \
        --arg account "$ACCOUNT_ID" \
        --arg region "$REGION" \
        --arg ts "$timestamp" \
        --arg start "$START_TIME" \
        --arg end "$END_TIME" \
        --arg overall "$overall" \
        --arg svc_filter "${SERVICE_FILTER:-all}" \
        --argjson alarms "$alarm_result" \
        --argjson services "$service_results" \
        --argjson critical "$critical_count" \
        --argjson degraded "$degraded_count" \
        --argjson unknown "$unknown_count" \
        '{
            account_id: $account,
            region: $region,
            timestamp: $ts,
            time_range: {start: $start, end: $end},
            service_filter: $svc_filter,
            overall_health: $overall,
            summary: {
                total_services: ($services | length),
                critical: $critical,
                degraded: $degraded,
                unknown: $unknown,
                healthy: (($services | length) - $critical - $degraded - $unknown)
            },
            alarms: $alarms,
            services: $services
        }'

    log "完成: overall=$overall (${critical_count} critical, ${degraded_count} degraded, ${unknown_count} unknown)"
}

main
