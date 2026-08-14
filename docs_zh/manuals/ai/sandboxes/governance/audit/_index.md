---
title: AI 治理审计日志
linkTitle: 审计日志
weight: 28
description: 为 Docker AI 治理策略决策捕获、查看、导出与收集结构化审计记录。
keywords: docker sandboxes, audit log, audit logging, AI Governance, policy decision, SIEM, compliance, jsonl
---

{{< summary-bar feature_name="AI Governance Audit Logs" >}}

AI 治理审计日志记录你所在组织的 Docker AI 治理活动。每条记录都会捕获某个治理事件的主体（principal）、动作、目标、决策与时间。记录仅包含元数据，不包含提示内容、智能体输出或参数值。

当你的组织启用了 AI 治理后，审计日志即可使用。Docker 沙箱仅为已登录、拥有 AI 治理许可证且受强制执行的集中式[组织策略](../access-controls/organization.md)管辖的用户发送审计记录。不同时满足这两个条件的 Docker 沙箱用户不会向审计日志发送审计数据。

> [!NOTE]
> AI 治理审计日志是 Docker AI 治理的一部分，需要单独的付费订阅。
> [联系 Docker 销售团队](https://www.docker.com/products/ai-governance/#contact-sales)
> 申请访问权限。

## 要求

要使用 AI 治理审计日志，你的组织需要具备：

- Docker [AI 治理套餐](/manuals/subscription/plans/ai-governance.md)
- 已强制执行的组织治理策略
- 一个 Docker 组织账户
- 一名组织所有者，或者一名拥有包含 AI 治理审计权限的[自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md)的用户，用于配置投递方式并查看托管事件

> [!NOTE]
> 其他 Docker 订阅本身并不足以使用 AI 治理审计日志。没有 AI 治理许可证且未受强制组织策略管辖的用户不会产生审计数据，也不会出现在审计事件或 SIEM 转发输出中。不支持个人账户。

## 覆盖范围

AI 治理审计日志覆盖 Docker 沙箱的策略决策和沙箱会话事件。随着其他 Docker AI 数据源逐步可用，它们也可以通过相同的 schema 发出记录。

## 投递模式

Docker 支持两种审计记录投递模式：

- **本地磁盘**：沙箱守护进程在每台主机上写入 JSON Lines（`.jsonl`）文件。当你需要主机本地留存、气隙环境采集，或通过自有日志采集器收集时，请使用此模式。
- **Docker Cloud**：Docker 将审计记录存储在 Docker Cloud 中。云端投递为托管审计日志视图、CSV 导出以及来自 app.docker.com 的 SIEM 流式转发提供支持。启用 AI 治理后，云端投递默认开启。组织所有者可以在[审计投递设置](configure.md)中将其禁用。

组织所有者以及拥有包含 AI 治理审计权限的[自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md)的用户可以配置本地磁盘、Docker Cloud，或两者同时启用。

托管审计日志视图、CSV 导出与 SIEM 转发都要求启用 Docker Cloud 投递。仅启用本地投递无法支持这些功能。

在托管审计日志可用之前就已使用本地审计日志的组织，初始状态下云端投递为关闭，直到所有者在[审计投递设置](configure.md)中主动启用。

## 数据处理

启用 Docker Cloud 投递后，Docker 会在你的组织配置的留存期内将审计记录存储于 Docker Cloud。有关约束 Docker 服务的法律与隐私条款，请参阅 Docker 的[服务条款](https://www.docker.com/legal/docker-terms-service/)和[隐私政策](https://www.docker.com/legal/privacy/)。

## 了解更多

- [本地审计日志](local.md)
- [配置审计投递](configure.md)
- [查看与导出审计事件](view-export.md)
- [SIEM 转发](siem.md)
- [审计记录参考](record-reference.md)
