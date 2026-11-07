# Severity 分类矩阵

> 基于证据判断 severity，不基于猜测。
> 如果信息不足以判断，先收集更多信号再分类。

---

## SEV1 — 服务不可用（立即响应）

### 触发条件（满足任一即为 SEV1）
- 全部 target unhealthy（ALB UnHealthyHostCount = total targets）
- 全部 pod CrashLoopBackOff / 无 Ready pod
- RDS 实例 down / 连接完全不上
- 数据丢失或数据不一致的证据
- 主要 API 完全无响应（100% 5xx 或 timeout）
- 用户报告：完全无法使用服务

### 响应要求
- **时间**: 立即（收到信号后 5 分钟内开始行动）
- **行动**:
  1. 收集证据（describe, metrics, logs 快照）
  2. 输出 incident report
  3. 提供具体缓解命令（标记 human-required）
  4. 如果 5 分钟内无法定位根因 → 建议开 AWS Support Case（Severity=Critical）

### 常见 SEV1 场景
| 症状 | 可能原因 | 首选 Skill |
|------|---------|-----------|
| ALB 全部 502/503 | target 全挂 / SG 问题 | aws-troubleshooting |
| EKS pod 全 CrashLoop | OOM / 镜像问题 / ConfigMap 丢失 | aws-troubleshooting |
| RDS 连接拒绝 | 实例 down / SG / max_connections | aws-troubleshooting |
| Lambda 100% 错误 | 权限 / VPC 配置 / 依赖不可用 | log-diagnosis → aws-troubleshooting |

---

## SEV2 — 服务降级（15 分钟内响应）

### 触发条件（满足任一即为 SEV2）
- 5xx 错误率 > 10% 但服务仍部分可用
- 响应延迟 > SLO 目标的 2x
- 部分 pod/target unhealthy（但整体服务可用）
- Lambda throttling 率 > 5%
- RDS CPU > 95% 持续 > 5 分钟
- RDS 副本延迟 > 60 秒
- 存储空间 < 10% 剩余

### 响应要求
- **时间**: 15 分钟内开始行动
- **行动**:
  1. 用 health-check 确认影响范围
  2. 用 log-diagnosis 定位错误
  3. 输出 incident report + 建议操作
  4. 路由到 aws-troubleshooting 做深度排查（实时查 aws-knowledge MCP / SSM Automation）

### 常见 SEV2 场景
| 症状 | 可能原因 | 首选 Skill |
|------|---------|-----------|
| 5xx 突增但未完全挂 | 部分 target 不健康 / 后端慢 | log-diagnosis → aws-troubleshooting |
| Lambda 频繁超时 | 下游慢 / VPC NAT / 冷启动 | log-diagnosis → aws-troubleshooting |
| 响应变慢 | DB CPU 高 / 连接池满 / 缓存失效 | health-check → log-diagnosis |
| Pod 频繁重启（但有 Ready pod） | 内存泄漏 / 配置错误 | log-diagnosis → aws-troubleshooting |

---

## SEV3 — 异常观察（1 小时内响应）

### 触发条件
- 告警触发但指标已自行恢复
- 非生产环境问题
- 指标趋势异常但未超阈值
- INSUFFICIENT_DATA 告警（新创建或数据中断）
- 单次错误突增但未持续
- 预防性发现（如存储增长趋势、证书即将过期）

### 响应要求
- **时间**: 1 小时内评估
- **行动**:
  1. 用 health-check 做全面巡检
  2. 记录观察，设置关注窗口
  3. 如果有趋势恶化，升级为 SEV2

---

## 升级路径

```
SEV3 → SEV2 条件:
  - 指标持续恶化（15 分钟内未恢复）
  - 影响范围扩大（从单资源扩展到多资源）
  - 用户开始报告影响

SEV2 → SEV1 条件:
  - 服务从降级恶化为不可用
  - 影响范围扩大到全部用户
  - 缓解措施无效
  - 出现数据风险
```

---

## 常见误报场景

这些情况看起来像 incident 但通常不是：

1. **部署中的短暂告警**: Rolling update 期间旧 pod 终止、新 pod 启动时的短暂 5xx/unhealthy → 查看是否在部署窗口内
2. **ASG 缩容**: 健康 target 数减少但整体服务正常 → 检查 ASG activity
3. **INSUFFICIENT_DATA**: 新创建的告警还没收到足够数据点 → 等待或手动查指标
4. **突发流量的短暂节流**: Lambda throttle 但很快恢复 → 检查是否有计划内的流量高峰
5. **维护窗口**: RDS 自动维护导致的短暂指标异常 → 检查维护计划
6. **CloudWatch 数据延迟**: 最近 2 分钟的指标不完整 → 等一会再查

---

## 跨服务影响判断

参考 `../aws-troubleshooting/references/investigation-framework.md` 中的依赖链表。

快速判断规则：
- **单资源问题**（一台 EC2 / 一个 pod）→ 通常 SEV3，除非是关键单点
- **单服务问题**（一个 EKS 集群 / 一个 RDS 实例）→ SEV2 起步
- **跨服务问题**（A 影响 B 影响 C）→ 至少 SEV2，可能 SEV1
- **AWS 侧事件**（Health Dashboard 有事件）→ 根据影响范围判断
