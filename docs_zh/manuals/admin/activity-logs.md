---
title: Activity logs（活动日志）
weight: 30
description: 了解如何访问和解读组织和仓库的 Docker 活动日志。
keywords: audit log, organization activity, Docker business logs, repository activity, track changes Docker, security logs Docker, filter logs, log Docker events
aliases:
- /docker-hub/audit-log/
- /admin/organization/activity-logs/
---

{{< summary-bar feature_name="Activity logs" >}}

活动日志显示按时间顺序排列的组织和仓库级别活动的列表。活动日志为组织所有者提供所有成员活动的记录。

通过活动日志，所有者可以查看和追踪：

 - 进行了哪些更改
 - 更改发生的日期
 - 是谁发起了更改

例如，活动日志会显示诸如仓库创建或删除的日期、创建仓库的成员、仓库名称，以及隐私设置发生更改的时间等活动。

如果仓库是属于订阅了 Docker Business 或 Team 订阅的组织的，所有者还可以查看其仓库的活动日志。

## Access activity logs（访问活动日志）

{{< tabs >}}
{{< tab name="Docker Home">}}

要在 Docker Home 中查看活动日志：

1. 登录 [Docker Home](https://app.docker.com) 并选择你的组织。
1. 选择 **Activity**。

{{< /tab >}}
{{< tab name="API">}}

要使用 Docker Hub API 查看活动日志，请使用 [Audit logs endpoints](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

{{< /tab >}}
{{< /tabs >}}

## Filter and customize activity logs（筛选和自定义活动日志）

> [!IMPORTANT]
>
> Docker Home 保留活动日志 30 天。要检索超过 30 天的活动，你必须使用 [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

默认情况下，**Activity** 选项卡显示最近 30 天内记录的所有事件。要缩小视图范围，请使用日历选择特定的日期范围。日志会更新为仅显示在该时间段内发生的活动。

你还可以按活动类型筛选。使用 **All Activities** 下拉菜单聚焦于组织级别、仓库级别或账单相关的事件。在 Docker Hub 中查看仓库时，**Activities** 选项卡仅显示该仓库的事件。

选择类别——**Organization（组织）**、**Repository（仓库）** 或 **Billing（账单）**——后，使用 **All Actions** 下拉菜单按特定事件类型进一步细化结果。

> [!NOTE]
>
> 由 Docker Support 触发的事件显示在用户名 **dockersupport** 下。

## Types of activity log events（活动日志事件类型）

请参阅以下部分获取事件及其描述的列表：

### Organization events（组织事件）

| Event（事件）                                                          | Description（描述）                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Team Created | 与创建团队相关的活动 |
| Team Updated | 与修改团队相关的活动 |
| Team Deleted | 与删除团队相关的活动 |
| Team Member Added | 添加到你团队的成员详情 |
| Team Member Removed | 从你团队中移除的成员详情 |
| Team Member Invited | 被邀请加入你团队的成员详情 |
| Organization Member Added | 添加到你组织的成员详情 |
| Organization Member Removed | 从你组织移除的成员详情 |
| Member Role Changed | 组织中成员角色变更的详情 |
| Organization Created | 与创建新组织相关的活动 |
| Organization Settings Updated | 与已更新的组织设置相关的详情 |
| Registry Access Management enabled | 与启用 Registry Access Management 相关的活动 |
| Registry Access Management disabled | 与禁用 Registry Access Management 相关的活动 |
| Registry Access Management registry added | 与添加注册表相关的活动 |
| Registry Access Management registry removed | 与移除注册表相关的活动 |
| Registry Access Management registry updated | 与已更新注册表相关的详情 |
| Single Sign-On domain added | 添加到你组织的单点登录域名详情 |
| Single Sign-On domain removed | 从你组织移除的单点登录域名详情 |
| Single Sign-On domain verified | 为你组织验证的单点登录域名详情 |
| Access token created | 在组织中创建的访问令牌 |
| Access token updated | 在组织中更新的访问令牌 |
| Access token deleted | 在组织中删除的访问令牌 |
| Policy created | 添加设置策略的详情 |
| Policy updated | 更新设置策略的详情 |
| Policy deleted | 删除设置策略的详情 |
| Policy transferred | 将设置策略转移到另一个所有者的详情 |
| Create SSO Connection | 创建新的组织/公司 SSO 连接的详情 |
| Update SSO Connection | 更新现有组织/公司 SSO 连接的详情 |
| Delete SSO Connection | 删除现有组织/公司 SSO 连接的详情 |
| Enforce SSO | 切换现有组织/公司 SSO 连接强制执行的详情 |
| Enforce SCIM | 在现有组织/公司 SSO 连接上切换 SCIM 的详情 |
| Refresh SCIM Token | 在现有组织/公司 SSO 连接上刷新 SCIM 令牌的详情 |
| Change SSO Connection Type | 更改现有组织/公司 SSO 连接类型的详情 |
| Toggle JIT provisioning | 在现有组织/公司 SSO 连接上切换 JIT 的详情 |

### Repository events（仓库事件）

> [!NOTE]
>
> 包含用户操作的事件描述可以指代 Docker 用户名、个人访问令牌（PAT）或组织访问令牌（OAT）。例如，如果用户将标签推送到仓库，事件将包含描述：`<user-access-token>` 将标签推送到仓库。

| Event（事件）                                                          | Description（描述）                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Repository Created | 与创建新仓库相关的活动 |
| Repository Deleted | 与删除仓库相关的活动 |
| Repository Updated | 与更新仓库描述、完整描述或状态相关的活动 |
| Privacy Changed | 与已更新的隐私策略相关的详情 |
| Tag Pushed | 与已推送标签相关的活动 |
| Tag Deleted | 与已删除标签相关的活动 |
| Categories Updated | 与设置或更新仓库类别相关的活动 |

### Billing events（账单事件）

| Event（事件）                                                          | Description（描述）                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Plan Upgraded | 当你的组织账单计划升级到更高级别计划时发生。|
| Plan Downgraded | 当你的组织账单计划降级到较低级别计划时发生。 |
| Seat Added | 当向你的组织账单计划添加席位时发生。 |
| Seat Removed | 当从你的组织账单计划移除席位时发生。 |
| Billing Cycle Changed | 当你的组织被收费的循环间隔发生变化时发生。|
| Plan Downgrade Canceled | 当为你的组织安排的计划降级被取消时发生。|
| Seat Removal Canceled | 当为组织账单计划安排的席位移除被取消时发生。 |
| Plan Upgrade Requested | 当你的组织中的用户请求升级计划时发生。 |
| Plan Downgrade Requested | 当你的组织中的用户请求降级计划时发生。 |
| Seat Addition Requested | 当你的组织中的用户请求增加席位数时发生。 |
| Seat Removal Requested | 当你的组织中的用户请求减少席位数时发生。 |
| Billing Cycle Change Requested | 当你的组织中的用户请求更改账单周期时发生。 |
| Plan Downgrade Cancellation Requested | 当你的组织中的用户请求取消已安排的计划降级时发生。 |
| Seat Removal Cancellation Requested | 当你的组织中的用户请求取消已安排的席位移除时发生。 |

### Offload events（Offload 事件）

> [!NOTE]
>
> 事件描述显示参与者的 Docker 用户名以及有关租约（lease）的详情。

| Event（事件）                                                          | Description（描述）                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Offload Lease Start | 当你的组织中启动 Offload 租约时发生。 |
| Offload Lease End | 当你的组织中结束 Offload 租约时发生。 |
