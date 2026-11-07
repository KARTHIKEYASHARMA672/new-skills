# 日志诊断报告：{service} / {region}

> 时间范围：{start_time} — {end_time}
> Log Group：{log_groups}
> 扫描方式：CloudWatch Insights
> 诊断时间：{diagnosis_timestamp}

## 错误摘要

| 级别 | 数量 | 占比 |
|------|------|------|
{error_summary_rows}

总计：{total_errors} 条错误 / {records_scanned} 条日志（{bytes_scanned} 扫描）

## Top Errors

{top_errors_detail}

<!-- 每个 top error 格式：
### {rank}. {error_type}（{count} 次）

**严重程度**：{severity}
**首次出现**：{first_seen}
**最近出现**：{last_seen}
**匹配模式**：{pattern_id} — {likely_cause}

示例日志：
```
{sample_log_message}
```

**建议**：{next_steps}
-->

## 时间线

{timeline_analysis}

<!-- 描述错误的时间分布：
- 突发型：{timestamp} 开始集中出现，持续 {duration}
- 持续型：在整个时间范围内均匀分布，平均每 {interval} 出现一次
- 递增型：错误频率随时间增加，可能在恶化
-->

## 受影响资源

{affected_resources}

<!-- 列出涉及的资源：
- Lambda: {function-names}
- EKS Pod: {pod-names}
- ALB: {alb-names}
- RDS: {db-identifiers}
-->

## 建议

{recommendations}

<!-- 
1. 即时操作：需要立刻处理的事项
2. 进一步诊断：建议下钻的方向（路由到 aws-troubleshooting 做深度排查）
3. 长期改进：告警配置、日志优化等建议
-->

---
*报告由 log-diagnosis skill 自动生成。如需深入排查，使用 aws-troubleshooting skill。*
