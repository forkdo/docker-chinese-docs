---
title: 活动日志
weight: 50
description: 了解如何访问和解读 Docker 组织和仓库的活动日志。
keywords: 审计日志, 组织活动, Docker 业务日志, 仓库活动, Docker 变更追踪, Docker 安全日志, 日志过滤, Docker 事件日志
aliases:
- /docker-hub/audit-log/
---

{{< summary-bar feature_name="Activity logs" >}}

活动日志显示在组织和仓库级别发生的活动的时序列表。活动日志为组织所有者提供所有成员活动的记录。

通过活动日志，所有者可以查看和追踪：

 - 所做的更改内容
 - 更改发生的日期
 - 发起更改的人员

例如，活动日志显示诸如仓库创建或删除的日期、创建仓库的成员、仓库名称以及隐私设置更改时间等活动。

如果仓库属于已订阅 Docker Business 或 Team 订阅的组织，所有者也可以查看其仓库的活动日志。

## 访问活动日志

{{< tabs >}}
{{< tab name="Docker Home">}}

在 Docker Home 中查看活动日志：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Activity logs**。

{{< /tab >}}
{{< tab name="API">}}

使用 Docker Hub API 查看活动日志，请使用 [Audit logs 端点](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

{{< /tab >}}
{{< /tabs >}}

## 过滤和自定义活动日志

> [!IMPORTANT]
>
> Docker Home 保留活动日志 30 天。要检索超过 30 天的活动，必须使用 [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

默认情况下，**Activity** 选项卡显示过去 30 天内记录的所有事件。要缩小视图范围，使用日历选择特定的日期范围。日志将更新为仅显示该期间内发生的活动。

您也可以按活动类型进行过滤。使用 **All Activities** 下拉菜单专注于组织级别、仓库级别或计费相关的事件。在 Docker Hub 中查看仓库时，**Activities** 选项卡仅显示该仓库的事件。

选择类别（**Organization**、**Repository** 或 **Billing**）后，使用 **All Actions** 下拉菜单进一步按特定事件类型精炼结果。

> [!NOTE]
>
> Docker Support 触发的事件显示为用户名 **dockersupport**。

## 活动日志事件类型

请参考以下部分了解事件列表及其描述：

### 组织事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Team Created | 与创建团队相关的活动 |
| Team Updated | 与修改团队相关的活动 |
| Team Deleted | 与删除团队相关的活动 |
| Team Member Added | 添加到团队的成员详细信息 |
| Team Member Removed | 从团队中移除的成员详细信息 |
| Team Member Invited | 邀请到团队的成员详细信息 |
| Organization Member Added | 添加到组织的成员详细信息 |
| Organization Member Removed | 从组织中移除的成员详细信息 |
| Member Role Changed | 组织中成员角色更改的详细信息 |
| Organization Created | 与创建新组织相关的活动 |
| Organization Settings Updated | 与更新的组织设置相关的详细信息 |
| Registry Access Management enabled | 启用注册表访问管理相关的活动 |
| Registry Access Management disabled | 禁用注册表访问管理相关的活动 |
| Registry Access Management registry added | 添加注册表相关的活动 |
| Registry Access Management registry removed | 移除注册表相关的活动 |
| Registry Access Management registry updated | 与更新的注册表相关的详细信息 |
| Single Sign-On domain added | 添加到组织的单点登录域详细信息 |
| Single Sign-On domain removed | 从组织中移除的单点登录域详细信息 |
| Single Sign-On domain verified | 为组织验证的单点登录域详细信息 |
| Access token created | 在组织中创建的访问令牌 |
| Access token updated | 在组织中更新的访问令牌 |
| Access token deleted | 在组织中删除的访问令牌 |
| Policy created | 添加设置策略的详细信息 |
| Policy updated | 更新设置策略的详细信息 |
| Policy deleted | 删除设置策略的详细信息 |
| Policy transferred | 将设置策略转移给另一个所有者的详细信息 |
| Create SSO Connection | 创建新的组织/公司 SSO 连接的详细信息 |
| Update SSO Connection | 更新现有组织/公司 SSO 连接的详细信息 |
| Delete SSO Connection | 删除现有组织/公司 SSO 连接的详细信息 |
| Enforce SSO | 切换现有组织/公司 SSO 连接强制执行的详细信息 |
| Enforce SCIM | 切换现有组织/公司 SSO 连接 SCIM 的详细信息 |
| Refresh SCIM Token | 现有组织/公司 SSO 连接 SCIM 令牌刷新的详细信息 |
| Change SSO Connection Type | 现有组织/公司 SSO 连接连接类型更改的详细信息 |
| Toggle JIT provisioning | 现有组织/公司 SSO 连接 JIT 切换的详细信息 |

### 仓库事件

> [!NOTE]
>
> 包含用户操作的事件描述可能指 Docker 用户名、个人访问令牌 (PAT) 或组织访问令牌 (OAT)。例如，如果用户向仓库推送标签，事件将包含描述：`<user-access-token>` 推送标签到仓库。

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Repository Created | 与创建新仓库相关的活动 |
| Repository Deleted | 与删除仓库相关的活动 |
| Repository Updated | 与更新仓库描述、完整描述或状态相关的活动 |
| Privacy Changed | 与更新的隐私策略相关的详细信息 |
| Tag Pushed | 与推送的标签相关的活动 |
| Tag Deleted | 与删除的标签相关的活动 |
| Categories Updated | 与设置或更新仓库类别相关的活动 |

### 计费事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Plan Upgraded | 当组织的计费计划升级到更高级别时发生。|
| Plan Downgraded | 当组织的计费计划降级到较低级别时发生。 |
| Seat Added | 当为组织的计费计划添加席位时发生。 |
| Seat Removed | 当从组织的计费计划中移除席位时发生。 |
| Billing Cycle Changed | 当组织的计费周期发生更改时发生。|
| Plan Downgrade Canceled | 当取消组织的计划降级调度时发生。|
| Seat Removal Canceled | 当取消组织计费计划的席位移除调度时发生。 |
| Plan Upgrade Requested | 当组织中的用户请求计划升级时发生。 |
| Plan Downgrade Requested | 当组织中的用户请求计划降级时发生。 |
| Seat Addition Requested | 当组织中的用户请求增加席位数量时发生。 |
| Seat Removal Requested | 当组织中的用户请求减少席位数量时发生。 |
| Billing Cycle Change Requested | 当组织中的用户请求更改计费周期时发生。 |
| Plan Downgrade Cancellation Requested | 当组织中的用户请求取消计划降级调度时发生。 |
| Seat Removal Cancellation Requested | 当组织中的用户请求取消席位移除调度时发生。 |

### 卸载事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Offload Lease Start | 当在组织中启动卸载租约时发生。 |
| Offload Lease End | 当在组织中结束卸载租约时发生。 |