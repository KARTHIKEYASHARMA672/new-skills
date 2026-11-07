# CloudWatch Insights 查询模板库

> 以下查询已验证可用。按场景选择，不要自行编写 Insights 查询。
> 所有查询的 `{placeholder}` 需替换为实际值。

---

## 1. 通用错误扫描

适用于任意 log group，快速发现错误和异常。

### 1a. 错误计数（按 5 分钟分桶）

```
filter @message like /(?i)(error|exception|fatal|critical)/
| stats count(*) as error_count by bin(5m)
| sort @timestamp desc
```

用途：看错误趋势，判断是突发还是持续。

### 1b. 错误详情 Top N

```
filter @message like /(?i)(error|exception|fatal|critical)/
| fields @timestamp, @message, @logStream
| sort @timestamp desc
```

用途：拿到具体错误消息和发生时间。

### 1c. 按错误类型分组统计

```
filter @message like /(?i)(error|exception|fatal|critical)/
| parse @message /(?i)(?<error_type>(error|exception|fatal|critical)[:\s]\S+)/
| stats count(*) as cnt by error_type
| sort cnt desc
```

用途：找出出现最多的错误类型。

---

## 2. Lambda 函数

Log group 格式：`/aws/lambda/{function-name}`

### 2a. Lambda 错误和超时

```
filter @type = "REPORT" or @message like /(?i)(error|timeout|task timed out)/
| fields @timestamp, @requestId, @duration, @billedDuration, @memorySize, @maxMemoryUsed, @message
| sort @timestamp desc
```

用途：关联执行报告和错误消息。

### 2b. Lambda 冷启动分析

```
filter @type = "REPORT"
| fields @timestamp, @requestId, @duration, @initDuration, @memorySize, @maxMemoryUsed
| filter ispresent(@initDuration)
| stats count(*) as cold_starts, avg(@initDuration) as avg_init_ms, max(@initDuration) as max_init_ms by bin(5m)
```

用途：分析冷启动频率和耗时。

### 2c. Lambda 内存使用率

```
filter @type = "REPORT"
| stats max(@maxMemoryUsed/@memorySize * 100) as max_mem_pct,
        avg(@maxMemoryUsed/@memorySize * 100) as avg_mem_pct
  by bin(5m)
```

用途：检查是否接近 OOM 边界。

### 2d. Lambda Throttling

```
filter @message like /Rate exceeded|TooManyRequestsException|Throttl/
| stats count(*) as throttle_count by bin(5m)
| sort @timestamp desc
```

---

## 3. EKS / 容器日志

Log group 格式：`/aws/eks/{cluster-name}/containers` 或自定义。

### 3a. Pod 错误日志

```
filter @logStream like /{pod-name-prefix}/
| filter @message like /(?i)(error|exception|fatal|panic|oomkilled)/
| fields @timestamp, @logStream, @message
| sort @timestamp desc
```

### 3b. 容器重启 / CrashLoopBackOff

```
filter @message like /(?i)(back-off restarting|crashloopbackoff|oomkilled|exit code)/
| fields @timestamp, @logStream, @message
| sort @timestamp desc
```

### 3c. Kubernetes 事件（如果 control plane logging 开启）

```
filter @logStream like /kube-apiserver-audit/
| filter responseStatus.code >= 400
| fields @timestamp, verb, requestURI, responseStatus.code, user.username
| sort @timestamp desc
```

---

## 4. ALB Access Log

Log group 格式：通常通过 S3 + Athena 查询；如果配置了 ALB → CloudWatch，用以下模板。

### 4a. 5xx 错误统计

```
filter elb_status_code >= 500
| stats count(*) as error_count by elb_status_code, bin(5m)
| sort @timestamp desc
```

### 4b. 慢请求（按 target response time）

```
filter target_processing_time > 5
| fields @timestamp, request_url, target_processing_time, elb_status_code, target_status_code
| sort target_processing_time desc
```

### 4c. Target 502/504 分析

```
filter elb_status_code = 502 or elb_status_code = 504
| fields @timestamp, request_url, target_status_code, target_processing_time, actions_executed
| sort @timestamp desc
```

---

## 5. API Gateway

Log group 格式：`API-Gateway-Execution-Logs_{api-id}/{stage}` 或自定义访问日志。

### 5a. 按状态码分组

```
fields @timestamp, status, httpMethod, resourcePath, responseLatency
| stats count(*) as cnt by status
| sort cnt desc
```

### 5b. 高延迟请求

```
filter responseLatency > 3000
| fields @timestamp, httpMethod, resourcePath, responseLatency, status
| sort responseLatency desc
```

---

## 6. CloudTrail（审计日志）

Log group 格式：由 trail 的 CloudWatchLogsLogGroupArn 决定。

### 6a. 失败的 API 调用

```
filter errorCode like /./
| fields @timestamp, eventSource, eventName, errorCode, errorMessage, userIdentity.arn
| sort @timestamp desc
```

### 6b. 特定资源的操作历史

```
filter requestParameters.instanceId = "{instance-id}"
  or requestParameters.functionName = "{function-name}"
  or requestParameters.bucketName = "{bucket-name}"
| fields @timestamp, eventName, userIdentity.arn, sourceIPAddress, errorCode
| sort @timestamp desc
```

### 6c. IAM 权限拒绝

```
filter errorCode = "AccessDenied" or errorCode = "UnauthorizedAccess" or errorCode = "Client.UnauthorizedAccess"
| fields @timestamp, eventSource, eventName, errorMessage, userIdentity.arn, requestParameters
| sort @timestamp desc
```

---

## 7. RDS 慢查询

Log group 格式：`/aws/rds/instance/{db-id}/slowquery` 或 `/aws/rds/cluster/{cluster-id}/slowquery`

### 7a. 慢查询 Top N

```
fields @timestamp, @message
| parse @message /Query_time: (?<query_time>[\d.]+)\s+Lock_time: (?<lock_time>[\d.]+)\s+Rows_sent: (?<rows_sent>\d+)\s+Rows_examined: (?<rows_examined>\d+)/
| filter query_time > 1
| sort query_time desc
```

---

## 8. 通用 JSON 格式日志

适用于输出 JSON 格式日志的自定义应用。

### 8a. JSON 日志错误扫描

```
filter level = "ERROR" or level = "FATAL" or level = "error" or level = "fatal"
| fields @timestamp, level, message, error, stack, requestId
| sort @timestamp desc
```

### 8b. JSON 日志按模块统计

```
filter level = "ERROR" or level = "error"
| stats count(*) as cnt by coalesce(module, logger, source, "unknown") as module
| sort cnt desc
```

---

## 陷阱提醒

1. **CloudWatch Insights 查询超时**：单次查询最多扫描指定时间范围内的日志，默认超时 15 分钟。大 log group + 长时间范围可能触发超时 → 缩短时间窗口重试
2. **@message like vs parse**：`like` 用正则，`parse` 用 glob/regex 提取字段。两者性能差异不大
3. **大小写敏感**：`like /error/` 是大小写敏感的，用 `/(?i)error/` 做不区分大小写匹配
4. **@logStream 过滤**：EKS 场景需要用 logStream 过滤 pod，否则会混入其他 pod 的日志
5. **时间范围**：查太长的时间（>24h）在活跃 log group 上可能很慢，建议先用短窗口确认模式再扩大
6. **limit 默认 1000**：Insights 默认最多返回 1000 条。stats 查询不受此限制
