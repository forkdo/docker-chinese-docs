---
title: 配置审计投递
linkTitle: 配置投递
weight: 20
description: 为 Docker AI 治理审计日志配置本地与云端投递、留存期和变更历史。
keywords: docker sandboxes, audit delivery, AI Governance, audit logs, retention, cloud delivery, AI Platform
---

组织所有者以及拥有包含 AI 治理审计权限的[自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md)的用户可以配置 Docker 写入审计事件的位置。有两种可用的投递目标，可以独立使用或同时使用：

- **本地磁盘**：沙箱守护进程将审计事件写入每台主机的本地磁盘。
- **Docker Cloud**：审计事件被发送到 Docker 的云平台，从而支持托管日志视图、CSV 导出与 SIEM 转发。

## 准备工作

你的组织需要具备：

- Docker [AI 治理套餐](/manuals/subscription/plans/ai-governance.md)
- 已强制执行的组织治理策略
- 组织所有者权限，或拥有 AI 治理审计权限的[自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md)

只有拥有 AI 治理许可证且受强制执行的组织策略管辖的用户才会发送 Docker 沙箱审计数据。

## 配置投递

配置审计投递的步骤：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 打开你的组织。
3. 前往 **AI Platform** > **Audit logs**。
4. 打开 **Audit Delivery**。
5. 选择一种或两种投递模式：
   - **本地磁盘**将审计记录写入每台主机上的 JSON Lines 文件。
   - **Docker Cloud** 将审计记录存储在 Docker Cloud 中，以支持托管搜索、CSV 导出与 SIEM 转发。
6. 保存更改。

启用 AI 治理后，云端投递默认开启。若要让记录仅保留在你的主机本地，请关闭 **Docker Cloud** 并保持 **本地磁盘** 开启。

在托管审计日志可用之前就已使用本地审计日志的组织，初始状态下云端投递为关闭，直到所有者主动启用。

## 配置留存期

选择 **Docker Cloud** 后，你还可以配置云端存储事件的留存时长：

| 字段                     | 说明                                       | 默认值  |
| ------------------------ | ------------------------------------------ | ------- |
| 可搜索留存期（天）       | 事件在托管审计日志视图中保持可搜索的时长。 | 90 天   |
| 归档留存期（天）         | 事件在长期归档存储中保留的时长。           | 90 天   |

归档留存期必须大于或等于可搜索留存期。

缩短留存期仅对之后的记录生效，不会删除此前在更长留存期下已保留的记录。

## 审计投递变更历史

Docker 会记录对你所在组织的审计投递设置所做的每一次更改。每条条目都会捕获时间戳、进行更改的用户以及所设置的投递配置。你可以使用该历史记录审计配置变更，并确认投递模式或留存期窗口的修改时间。

打开 **History** 可查看组织的投递与留存期变更。历史条目会显示是谁做的更改、更改发生的时间，以及变更前后的值。
