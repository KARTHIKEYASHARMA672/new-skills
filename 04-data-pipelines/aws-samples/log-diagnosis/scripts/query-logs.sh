#!/usr/bin/env bash
# query-logs.sh — CloudWatch Insights 查询封装
#
# 用法: query-logs.sh <log-group> <query> <hours-back> <region> [--limit N]
#       query-logs.sh --multi-groups "group1,group2" <query> <hours-back> <region>
#
# 输出:
#   stdout: JSON 格式的查询结果（供 Claude 解析）
#   stderr: 进度日志
#
# 封装 start-query → poll get-query-results → 返回结果 的完整流程

set -euo pipefail

# ── 参数解析 ──────────────────────────────────────────────
LOG_GROUP=""
MULTI_GROUPS=""
QUERY_STRING=""
HOURS_BACK=""
REGION=""
LIMIT=100
MAX_POLL_SECONDS=60

show_help() {
    cat >&2 <<'HELP'
用法: query-logs.sh <log-group> <query> <hours-back> <region> [options]
      query-logs.sh --multi-groups "g1,g2" <query> <hours-back> <region> [options]

CloudWatch Insights 查询封装：start-query → poll → 返回 JSON。

参数:
  log-group     CloudWatch Log Group 名称
  query         CloudWatch Insights 查询语句
  hours-back    查询过去 N 小时（正整数）
  region        AWS Region

选项:
  --multi-groups "g1,g2"  逗号分隔的多个 log group（替代第一个位置参数）
  --limit N               返回最大条数（默认 100）
  --timeout N             poll 超时秒数（默认 60）
  --help, -h              显示帮助

示例:
  query-logs.sh /aws/lambda/my-func \
    'filter @message like /ERROR/ | stats count(*) by bin(5m)' \
    1 ap-northeast-1

  query-logs.sh --multi-groups "/aws/lambda/func-a,/aws/lambda/func-b" \
    'filter @message like /ERROR/' 24 ap-northeast-1 --limit 50
HELP
    exit 0
}

# 解析可选参数
POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h) show_help ;;
        --multi-groups) MULTI_GROUPS="$2"; shift 2 ;;
        --limit) LIMIT="$2"; shift 2 ;;
        --timeout) MAX_POLL_SECONDS="$2"; shift 2 ;;
        *) POSITIONAL+=("$1"); shift ;;
    esac
done

# 分配位置参数
if [[ -n "$MULTI_GROUPS" ]]; then
    # --multi-groups 模式：位置参数是 query, hours-back, region
    QUERY_STRING="${POSITIONAL[0]:-}"
    HOURS_BACK="${POSITIONAL[1]:-}"
    REGION="${POSITIONAL[2]:-}"
else
    # 单 log group 模式：位置参数是 log-group, query, hours-back, region
    LOG_GROUP="${POSITIONAL[0]:-}"
    QUERY_STRING="${POSITIONAL[1]:-}"
    HOURS_BACK="${POSITIONAL[2]:-}"
    REGION="${POSITIONAL[3]:-}"
fi

# 参数校验
if [[ -z "$QUERY_STRING" || -z "$HOURS_BACK" || -z "$REGION" ]]; then
    echo '{"error": "缺少必需参数。用法: query-logs.sh <log-group> <query> <hours-back> <region>"}' >&2
    exit 1
fi

if [[ -z "$LOG_GROUP" && -z "$MULTI_GROUPS" ]]; then
    echo '{"error": "必须指定 log-group 或 --multi-groups"}' >&2
    exit 1
fi

if ! [[ "$HOURS_BACK" =~ ^[0-9]+$ ]]; then
    echo '{"error": "hours-back 必须是正整数"}' >&2
    exit 1
fi

# ── 辅助函数 ──────────────────────────────────────────────
log() { echo "[query-logs] $*" >&2; }

# ── 时间计算 ──────────────────────────────────────────────
END_TIME=$(date +%s)
START_TIME=$((END_TIME - HOURS_BACK * 3600))

log "时间范围: $(date -r "$START_TIME" '+%Y-%m-%d %H:%M:%S') → $(date -r "$END_TIME" '+%Y-%m-%d %H:%M:%S')"

# ── 构建 log group 参数 ──────────────────────────────────
LOG_GROUP_ARGS=()
if [[ -n "$MULTI_GROUPS" ]]; then
    # 纯参数展开切分逗号分隔的 group 列表。
    # 不用 `read -ra <<<`：macOS 自带 bash 3.2 的 here-string 依赖临时文件，
    # 在受限/沙箱环境里会静默失灵（read 退化为读真实 stdin → 垃圾数据），
    # 且 `read` 在 EOF 返回非零会被 `set -e` 当场 abort。参数展开无此问题。
    # 同时避免对含 `*` 的 group 名（如 /aws/lambda/foo-*）触发 glob 展开。
    GROUP_COUNT=0
    remaining="$MULTI_GROUPS"
    while [[ -n "$remaining" ]]; do
        if [[ "$remaining" == *,* ]]; then
            g="${remaining%%,*}"; remaining="${remaining#*,}"
        else
            g="$remaining"; remaining=""
        fi
        g=$(echo "$g" | xargs)  # trim 前后空格
        if [[ -n "$g" ]]; then
            LOG_GROUP_ARGS+=(--log-group-names "$g")
            GROUP_COUNT=$((GROUP_COUNT + 1))
        fi
    done
    log "查询 ${GROUP_COUNT} 个 log groups"
else
    LOG_GROUP_ARGS=(--log-group-name "$LOG_GROUP")
    log "查询 log group: $LOG_GROUP"
fi

# ── 限制查询结果条数 ──────────────────────────────────────
# CloudWatch Insights 通过在查询尾部追加 | limit N 来控制
EFFECTIVE_QUERY="$QUERY_STRING | limit $LIMIT"

# ── Phase 1: 启动查询 ────────────────────────────────────
log "启动 CloudWatch Insights 查询..."

START_RESULT=$(aws logs start-query \
    "${LOG_GROUP_ARGS[@]}" \
    --start-time "$START_TIME" \
    --end-time "$END_TIME" \
    --query-string "$EFFECTIVE_QUERY" \
    --region "$REGION" \
    --output json 2>&1) || {
    echo "{\"error\": \"start-query 失败\", \"detail\": $(echo "$START_RESULT" | jq -Rs .)}"
    exit 1
}

QUERY_ID=$(echo "$START_RESULT" | jq -r '.queryId')
if [[ -z "$QUERY_ID" || "$QUERY_ID" == "null" ]]; then
    echo "{\"error\": \"未获得 queryId\", \"start_result\": $START_RESULT}"
    exit 1
fi

log "Query ID: $QUERY_ID"

# ── Phase 2: Poll 查询结果 ───────────────────────────────
POLL_INTERVAL=1
ELAPSED=0

while true; do
    RESULT=$(aws logs get-query-results \
        --query-id "$QUERY_ID" \
        --region "$REGION" \
        --output json 2>&1) || {
        log "get-query-results 调用失败，重试..."
        sleep "$POLL_INTERVAL"
        ELAPSED=$((ELAPSED + POLL_INTERVAL))
        if [[ $ELAPSED -ge $MAX_POLL_SECONDS ]]; then
            echo "{\"error\": \"poll 超时 (${MAX_POLL_SECONDS}s)\", \"query_id\": \"$QUERY_ID\"}"
            exit 1
        fi
        continue
    }

    STATUS=$(echo "$RESULT" | jq -r '.status')

    case "$STATUS" in
        Complete)
            log "查询完成"
            break
            ;;
        Failed|Cancelled|Timeout)
            log "查询失败: $STATUS"
            echo "{\"error\": \"查询状态: $STATUS\", \"query_id\": \"$QUERY_ID\"}"
            exit 1
            ;;
        Running|Scheduled)
            log "状态: $STATUS (已等待 ${ELAPSED}s)"
            sleep "$POLL_INTERVAL"
            ELAPSED=$((ELAPSED + POLL_INTERVAL))
            # 递增 poll 间隔，上限 5s
            if [[ $POLL_INTERVAL -lt 5 ]]; then
                POLL_INTERVAL=$((POLL_INTERVAL + 1))
            fi
            if [[ $ELAPSED -ge $MAX_POLL_SECONDS ]]; then
                echo "{\"error\": \"poll 超时 (${MAX_POLL_SECONDS}s)\", \"query_id\": \"$QUERY_ID\", \"last_status\": \"$STATUS\"}"
                exit 1
            fi
            ;;
        *)
            log "未知状态: $STATUS"
            sleep "$POLL_INTERVAL"
            ELAPSED=$((ELAPSED + POLL_INTERVAL))
            ;;
    esac
done

# ── Phase 3: 格式化输出 ──────────────────────────────────
# 提取统计信息
STATS=$(echo "$RESULT" | jq '.statistics')
RECORDS_MATCHED=$(echo "$STATS" | jq '.recordsMatched // 0')
RECORDS_SCANNED=$(echo "$STATS" | jq '.recordsScanned // 0')
BYTES_SCANNED=$(echo "$STATS" | jq '.bytesScanned // 0')

# 提取结果（将 [{field, value}] 数组转为对象数组）
RESULTS=$(echo "$RESULT" | jq '
    .results | map(
        map({(.field): .value}) | add
    )
')

RESULT_COUNT=$(echo "$RESULTS" | jq 'length')

# 构建最终输出
OUTPUT=$(jq -n \
    --arg qid "$QUERY_ID" \
    --arg status "Complete" \
    --arg lg "${LOG_GROUP}${MULTI_GROUPS}" \
    --arg query "$QUERY_STRING" \
    --arg region "$REGION" \
    --arg start "$(date -r "$START_TIME" '+%Y-%m-%dT%H:%M:%S')" \
    --arg end "$(date -r "$END_TIME" '+%Y-%m-%dT%H:%M:%S')" \
    --argjson limit "$LIMIT" \
    --argjson count "$RESULT_COUNT" \
    --argjson matched "$RECORDS_MATCHED" \
    --argjson scanned "$RECORDS_SCANNED" \
    --argjson bytes "$BYTES_SCANNED" \
    --argjson results "$RESULTS" \
    '{
        query_id: $qid,
        status: $status,
        log_group: $lg,
        query: $query,
        region: $region,
        time_range: {start: $start, end: $end},
        limit: $limit,
        statistics: {
            records_matched: $matched,
            records_scanned: $scanned,
            bytes_scanned: $bytes,
            results_returned: $count
        },
        results: $results
    }')

echo "$OUTPUT"
log "完成: $RESULT_COUNT 条结果（匹配 $RECORDS_MATCHED / 扫描 $RECORDS_SCANNED 条记录）"
