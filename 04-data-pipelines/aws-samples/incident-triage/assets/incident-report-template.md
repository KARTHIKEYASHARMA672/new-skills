# Incident Report

> 时间：{timestamp}
> 触发方式：{trigger}（告警 / 用户报告 / 巡检发现）
> Severity：{severity}

## 概要

{one_line_summary}

## 影响范围

- **服务**：{affected_services}
- **Region**：{region}
- **Blast Radius**：{blast_radius}（单资源 / 单服务 / AZ / Region）
- **用户影响**：{user_impact}
- **持续时间**：{duration}（自 {start_time} 起）

## 信号

{signals}

<!-- 信号来源：
### 告警
- {alarm_name}: {metric} {comparison} {threshold}，当前值 {current_value}

### 指标快照
- {metric}: {value}（正常范围: {normal_range}）

### 错误日志摘要
- {error_pattern}: {count} 次（最近: {latest_timestamp}）

### 最近变更（CloudTrail）
- {timestamp}: {event_name} by {actor}
-->

## 根因（初步判断）

{root_cause_hypothesis}

**置信度**：{confidence}（高 / 中 / 低）
**判断依据**：{evidence}

## 即时操作

{immediate_actions}

<!-- 每个操作：
### {action_number}. {action_description}
- **命令**: `{command}`
- **预期效果**: {expected_outcome}
- **权限**: human-required
- **风险**: {risk_assessment}
-->

## 下一步

{next_steps}

<!-- 路由建议：
- [ ] 使用 {skill_name} 进一步诊断
- [ ] 开 AWS Support Case（如果 5 分钟内无法定位根因）
- [ ] 通知 {stakeholder}
-->

## 时间线

| 时间 | 事件 |
|------|------|
{timeline_rows}

---
*报告由 incident-triage skill 自动生成。深度诊断请使用 aws-troubleshooting skill。*
