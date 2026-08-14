---
title: 查看并导出审计事件
linkTitle: 查看与导出
weight: 30
description: 在托管的审计日志界面中搜索、筛选并导出 Docker AI Governance 审计事件。
keywords: docker sandboxes, audit events, audit logs, AI Governance, CSV export
---

云端投递方式会将 AI Governance 审计记录存储在 Docker Cloud 中，并在托管的审计日志界面中提供访问。使用托管视图可以调查策略决策，或将事件导出为 CSV。

## View audit events（查看审计事件）

查看审计事件：

1. 登录 [Docker Home](https://app.docker.com/)。
1. 打开你的组织。
1. 进入 **AI Platform** > **Audit logs**。
1. 打开 **Audit Events**。

**Audit Events** 视图包含总事件数、允许事件、拒绝事件和需要确认（consent-required）事件的汇总卡片。事件表包含以下列：

| 列        | 说明                                             |
| --------- | ------------------------------------------------ |
| Time      | Docker 记录该事件的时间。                        |
| Event     | 事件类型或策略动作。                             |
| Principal | 与该事件关联的 Docker 用户。                     |
| Resource  | 目标资源，例如域名、文件路径或工具。             |
| Decision  | 治理决策，例如 allow、deny 或 consent。          |
| Agent     | 与该事件关联的 AI 代理（在 Docker 已知的情况下）。 |

## Filter and search events（筛选与搜索事件）

使用审计日志筛选器按决策和时间范围缩小事件表范围。使用搜索功能可按主体（principal）、资源、事件类型或代理查找事件。

对于较大的结果集，事件表使用游标分页。

## Export events to CSV（将事件导出为 CSV）

当你需要筛选后审计事件的离线副本时，使用 CSV 导出：

1. 打开 **Audit Events**。
1. 为想要导出的事件应用筛选条件和搜索词。
1. 选择 **Export**。
1. 从 Docker 提供的链接下载生成的 CSV 文件。

CSV 导出最多包含 1 000 000 行。下载链接在 24 小时后过期。
