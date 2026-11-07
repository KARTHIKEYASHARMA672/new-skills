# 健康巡检报告：{account_id} / {region}

> 巡检时间：{timestamp}
> 巡检范围：{scope}（全局 / 单服务）
> 数据窗口：最近 {hours} 小时

## 总体状态：{overall_status}

| 服务 | 类型 | 状态 | 关键指标 | 问题 |
|------|------|------|---------|------|
{service_status_rows}

## 告警状态

| 状态 | 数量 |
|------|------|
| ALARM | {alarm_count} |
| INSUFFICIENT_DATA | {insufficient_count} |
| OK | {ok_count} |

{alarm_details}

## 异常详情

{anomaly_details}

<!-- 每个异常项：
### {service_name} — {health_status}

**指标**：
- {metric_name}: {value}（阈值: {threshold}）

**建议**：
- {recommendation}
-->

## SLO 达标情况

{slo_compliance}

<!-- 仅对 slo-targets.yaml 中定义了 SLO 的服务：
| 服务 | SLO 目标 | 实际值 | 达标 |
-->

## 建议操作

{recommendations}

<!--
1. 即时关注：CRITICAL 的服务需要立即处理
2. 监控建议：UNKNOWN 的服务需要开启监控
3. 优化建议：DEGRADED 的服务需要关注趋势
-->

---
*报告由 health-check skill 自动生成。异常服务建议使用 log-diagnosis 下钻日志。*
