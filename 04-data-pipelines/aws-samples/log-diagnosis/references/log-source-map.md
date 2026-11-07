# 服务 → Log Group 映射参考

> 定位 log group 时先查此表，再用发现命令确认实际存在。
> 不要凭猜测构造 log group 名——必须 describe-log-groups 确认。

---

## 映射表

| 服务类型 | Log Group 命名惯例 | 发现命令 | 备注 |
|---------|-------------------|---------|------|
| Lambda | `/aws/lambda/{function-name}` | `aws logs describe-log-groups --log-group-name-prefix /aws/lambda/ --region {region}` | 每个函数一个 group |
| EKS Control Plane | `/aws/eks/{cluster-name}/cluster` | `aws logs describe-log-groups --log-group-name-prefix /aws/eks/ --region {region}` | 含 api-server, audit, authenticator 等 stream |
| EKS 容器 (Fluent Bit) | `/aws/containerinsights/{cluster-name}/application` | `aws logs describe-log-groups --log-group-name-prefix /aws/containerinsights/ --region {region}` | 需要开启 Container Insights |
| API Gateway (REST) | `API-Gateway-Execution-Logs_{api-id}/{stage}` | `aws logs describe-log-groups --log-group-name-prefix API-Gateway --region {region}` | 需要在 stage 中开启日志 |
| API Gateway (HTTP) | 由 access log 设置决定 | 检查 API 配置：`aws apigatewayv2 get-stages --api-id {id}` | 可能是自定义 group 名 |
| RDS (MySQL) | `/aws/rds/instance/{db-id}/error`<br>`/aws/rds/instance/{db-id}/slowquery`<br>`/aws/rds/instance/{db-id}/general` | `aws logs describe-log-groups --log-group-name-prefix /aws/rds/ --region {region}` | 需要在 DB 参数组中开启 |
| RDS (PostgreSQL) | `/aws/rds/instance/{db-id}/postgresql` | 同上 | |
| Aurora | `/aws/rds/cluster/{cluster-id}/{log-type}` | 同上 | cluster 级别 |
| ECS (Fargate) | 由 task definition 的 `logConfiguration` 决定 | `aws logs describe-log-groups --log-group-name-prefix /ecs/ --region {region}` | awslogs driver 常用 `/ecs/{service-name}` |
| CloudTrail | 由 trail 配置决定 | `aws cloudtrail describe-trails --region {region}` → 找 `CloudWatchLogsLogGroupArn` | 可能集中在一个 group |
| VPC Flow Logs | 由 flow log 配置决定 | `aws ec2 describe-flow-logs --region {region}` → 找 `LogGroupName` | |
| CodeBuild | `/aws/codebuild/{project-name}` | `aws logs describe-log-groups --log-group-name-prefix /aws/codebuild/ --region {region}` | |
| Step Functions | `/aws/vendedlogs/states/{state-machine-name}` | `aws logs describe-log-groups --log-group-name-prefix /aws/vendedlogs/states/ --region {region}` | 需要开启日志 |
| 自定义应用 | 无固定惯例 | `aws logs describe-log-groups --region {region}` 全量扫 | 可能需要 tag 过滤 |

---

## 自动发现流程

当 skill 需要找到某个服务的 log group 但映射表未覆盖时：

### Step 1: 按前缀搜索

```bash
aws logs describe-log-groups \
    --log-group-name-prefix "/aws/{service}" \
    --region {region} \
    --query 'logGroups[].{name:logGroupName, stored:storedBytes, retention:retentionInDays}' \
    --output table
```

### Step 2: 全量列出 + 名称匹配

```bash
aws logs describe-log-groups \
    --region {region} \
    --query 'logGroups[?contains(logGroupName, `{keyword}`)].{name:logGroupName, stored:storedBytes}' \
    --output table
```

### Step 3: 按 tag 查找

```bash
# 先列出所有 log group 的 tag
aws logs describe-log-groups --region {region} --query 'logGroups[].logGroupName' --output text | while read lg; do
    tags=$(aws logs list-tags-for-resource --resource-arn "arn:aws:logs:{region}:{account-id}:log-group:${lg}:*" 2>/dev/null)
    echo "$lg: $tags"
done
```

> 注意：Step 3 性能较差（N+1 查询），只在 Step 1/2 无结果时使用。

---

## 陷阱

1. **Log group 不存在 ≠ 服务不存在**：很多 AWS 服务默认不开日志，需要手动开启（RDS 慢查询日志、API Gateway 日志、EKS control plane logging 等）
2. **storedBytes = 0**：log group 存在但没数据，可能是刚创建或 retention 已清理
3. **跨 region**：日志是 region 级别的，查 us-west-2 的 Lambda 日志不能用 ap-northeast-1 的 endpoint
4. **CloudTrail log group 共享**：多个 trail 可能写到同一个 log group，查询时需要用 `eventSource` 过滤
5. **EKS 容器日志路径**：取决于日志方案（Fluent Bit / Fluentd / CloudWatch Agent），group 名和结构可能不同
