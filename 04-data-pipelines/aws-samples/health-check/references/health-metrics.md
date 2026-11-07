# 服务健康指标参考

> 各服务的关键健康指标、CloudWatch 查询参数、判断阈值。
> check-health.sh 按这些指标巡检，Claude 按这些阈值判断健康等级。

---

## EKS

### 节点 CPU 使用率
- **Namespace**: `ContainerInsights`
- **MetricName**: `node_cpu_utilization`
- **Dimensions**: `ClusterName`
- **Statistics**: Average, Maximum
- **DEGRADED**: max > 80%
- **CRITICAL**: max > 95%
- **注意**: 需要开启 Container Insights。未开启时无数据（UNKNOWN）

### Pod 重启次数
- **Namespace**: `ContainerInsights`
- **MetricName**: `pod_number_of_container_restarts`
- **Dimensions**: `ClusterName`
- **Statistics**: Sum, Maximum
- **DEGRADED**: sum > 3/hour
- **CRITICAL**: sum > 10/hour
- **注意**: 生产环境的 pod 不应频繁重启。任何重启都值得关注

### 节点内存使用率
- **Namespace**: `ContainerInsights`
- **MetricName**: `node_memory_utilization`
- **Dimensions**: `ClusterName`
- **Statistics**: Average, Maximum
- **DEGRADED**: max > 85%
- **CRITICAL**: max > 95%

---

## RDS / Aurora

### CPU 使用率
- **Namespace**: `AWS/RDS`
- **MetricName**: `CPUUtilization`
- **Dimensions**: `DBInstanceIdentifier` 或 `DBClusterIdentifier`（Aurora）
- **Statistics**: Average, Maximum
- **DEGRADED**: max > 80%
- **CRITICAL**: max > 95%

### 可用内存
- **Namespace**: `AWS/RDS`
- **MetricName**: `FreeableMemory`（单位: bytes）
- **Dimensions**: 同上
- **Statistics**: Minimum, Average
- **DEGRADED**: min < 500MB
- **CRITICAL**: min < 100MB
- **Aurora 注意**: Aurora 主动使用内存做缓存，FreeableMemory 低不一定是问题。关注 SwapUsage 和 OOM 日志更可靠

### 数据库连接数
- **Namespace**: `AWS/RDS`
- **MetricName**: `DatabaseConnections`
- **Dimensions**: 同上
- **Statistics**: Maximum, Average
- **DEGRADED**: max > max_connections * 80%（max_connections 因实例类型而异，需查 MCP）
- **CRITICAL**: max > max_connections * 95%
- **注意**: 不要硬编码 max_connections 值——因实例类型和参数组配置而异

### 副本延迟
- **Namespace**: `AWS/RDS`
- **MetricName**: `ReplicaLag`（单位: seconds）
- **Dimensions**: 读副本的 DBInstanceIdentifier
- **Statistics**: Maximum, Average
- **DEGRADED**: max > 10s
- **CRITICAL**: max > 60s

---

## Lambda

### 错误率
- **Namespace**: `AWS/Lambda`
- **MetricName**: `Errors` 和 `Invocations`
- **Dimensions**: `FunctionName`
- **计算**: error_rate = Errors / Invocations * 100
- **DEGRADED**: > 1%
- **CRITICAL**: > 10%

### 执行耗时 vs 超时
- **Namespace**: `AWS/Lambda`
- **MetricName**: `Duration`（单位: ms）
- **Dimensions**: `FunctionName`
- **Statistics**: Average, Maximum, p99
- **对比**: Duration / (配置的 Timeout * 1000) * 100
- **DEGRADED**: max > 70% of timeout
- **CRITICAL**: max > 90% of timeout

### 节流
- **Namespace**: `AWS/Lambda`
- **MetricName**: `Throttles`
- **Dimensions**: `FunctionName`
- **Statistics**: Sum
- **DEGRADED**: sum > 0（任何节流都值得关注）
- **CRITICAL**: throttle_rate > 5%

### 并发执行
- **Namespace**: `AWS/Lambda`
- **MetricName**: `ConcurrentExecutions`
- **Dimensions**: `FunctionName`
- **Statistics**: Maximum
- **DEGRADED**: max > reserved concurrency * 80%（如果配了的话）

---

## ALB (Application Load Balancer)

### Target 5xx 错误率
- **Namespace**: `AWS/ApplicationELB`
- **MetricName**: `HTTPCode_Target_5XX_Count` 和 `RequestCount`
- **Dimensions**: `LoadBalancer`
- **计算**: 5xx_rate = HTTPCode_Target_5XX_Count / RequestCount * 100
- **DEGRADED**: > 1%
- **CRITICAL**: > 5%

### 响应时间
- **Namespace**: `AWS/ApplicationELB`
- **MetricName**: `TargetResponseTime`（单位: seconds）
- **Dimensions**: `LoadBalancer`
- **Statistics**: Average, p99（需 Extended Statistics）
- **DEGRADED**: avg > 2s
- **CRITICAL**: avg > 5s

### 不健康 Target 数
- **Namespace**: `AWS/ApplicationELB`
- **MetricName**: `UnHealthyHostCount`
- **Dimensions**: `LoadBalancer`, `TargetGroup`
- **Statistics**: Maximum
- **DEGRADED**: > 0
- **CRITICAL**: = total targets（全部不健康）

---

## ECS (Fargate / EC2)

### CPU 使用率
- **Namespace**: `AWS/ECS`
- **MetricName**: `CPUUtilization`
- **Dimensions**: `ClusterName`, `ServiceName`
- **Statistics**: Average, Maximum
- **DEGRADED**: avg > 80%
- **CRITICAL**: avg > 95%

### 内存使用率
- **Namespace**: `AWS/ECS`
- **MetricName**: `MemoryUtilization`
- **Dimensions**: `ClusterName`, `ServiceName`
- **Statistics**: Average, Maximum
- **DEGRADED**: avg > 80%
- **CRITICAL**: avg > 95%

---

## 通用注意事项

1. **CloudWatch 指标延迟**: 数据有 ~2 分钟延迟，最近的数据点可能不完整
2. **Period 选择**: 5 分钟粒度（300s）是日常巡检的好选择。1 分钟粒度更精确但数据点更多
3. **阈值不是死规则**: 这些阈值是起点，实际环境可能需要调整。如果某个服务长期在 85% CPU 下稳定运行，那可能是正常的
4. **UNKNOWN 不等于健康**: 没有数据可能意味着监控未开启，不代表服务没问题
