---
title: 活动日志
weight: 50
description: 了解如何访问和解读组织和仓库的 Docker 活动日志。
keywords: audit log, organization activity, Docker business logs, repository activity, track changes Docker, security logs Docker, filter logs, log Docker events
aliases:
- /docker-hub/audit-log/
---

{{< summary-bar feature_name="Activity logs" >}}

活动日志按时间顺序显示在组织和仓库级别发生的活动。活动日志为组织所有者提供了所有成员活动的记录。

通过活动日志，所有者可以查看和追踪：

 - 做了哪些更改
 - 更改发生的日期
 - 谁发起了更改

例如，活动日志会显示仓库创建或删除的日期、创建仓库的成员、仓库名称，以及隐私设置发生更改的时间。

如果仓库属于订阅了 Docker Business 或 Team 的组织，所有者还可以查看其仓库的活动日志。

## 访问活动日志

{{< tabs >}}
{{< tab name="Docker Home">}}

要在 Docker Home 中查看活动日志：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
1. 选择 **Admin Console**，然后选择 **Activity logs**。

{{< /tab >}}
{{< tab name="API">}}

要使用 Docker Hub API 查看活动日志，请使用 [审计日志端点](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

{{< /tab >}}
{{< /tabs >}}

## 筛选和自定义活动日志

> [!IMPORTANT]
>
> Docker Home 保留活动日志 30 天。要检索 30 天前的活动，您必须使用
> [Docker Hub API](https://docs.docker.com/reference/api/hub/latest/#tag/audit-logs)。

默认情况下，**Activity** 标签页显示过去 30 天内记录的所有事件。要缩小查看范围，请使用日历选择特定的日期范围。日志将更新，仅显示该期间内发生的活动。

您还可以按活动类型筛选。使用 **All Activities** 下拉菜单，重点关注组织级别、仓库级别或账单相关的事件。在 Docker Hub 中，查看仓库时，**Activities** 标签页仅显示该仓库的事件。

选择 **Organization**、**Repository** 或 **Billing** 类别后，使用 **All Actions** 下拉菜单，按特定事件类型进一步细化结果。

> [!NOTE]
>
> Docker Support 触发的事件显示在用户名 **dockersupport** 下。

## 活动日志事件类型

请参考以下部分，了解事件及其描述的列表：

### 组织事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Team Created | 与团队创建相关的活动 |
| Team Updated | 与团队修改相关的活动 |
| Team Deleted | 与团队删除相关的活动 |
| Team Member Added | 添加到团队的成员详情 |
| Team Member Removed | 从团队中移除的成员详情 |
| Team Member Invited | 邀请到团队的成员详情 |
| Organization Member Added | 添加到组织的成员详情 |
| Organization Member Removed | 从组织中移除的成员详情 |
| Member Role Changed | 组织中成员角色更改的详情 |
| Organization Created | 与新组织创建相关的活动 |
| Organization Settings Updated | 与组织设置更新相关的详情 |
| Registry Access Management enabled | 与启用注册表访问管理相关的活动 |
| Registry Access Management disabled | 与禁用注册表访问管理相关的活动 |
| Registry Access Management registry added | 与添加注册表相关的活动 |
| Registry Access Management registry removed | 与移除注册表相关的活动 |
| Registry Access Management registry updated | 与更新注册表相关的详情 |
| Single Sign-On domain added | 添加到组织的单点登录域详情 |
| Single Sign-On domain removed | 从组织中移除的单点登录域详情 |
| Single Sign-On domain verified | 为组织验证的单点登录域详情 |
| Access token created | 在组织中创建的访问令牌 |
| Access token updated | 在组织中更新的访问令牌 |
| Access token deleted | 在组织中删除的访问令牌 |
| Policy created | 添加设置策略的详情 |
| Policy updated | 更新设置策略的详情 |
| Policy deleted | 删除设置策略的详情 |
| Policy transferred | 将设置策略转移到另一个所有者的详情 |
| Create SSO Connection | 创建新组织/公司 SSO 连接的详情 |
| Update SSO Connection | 更新现有组织/公司 SSO 连接的详情 |
| Delete SSO Connection | 删除现有组织/公司 SSO 连接的详情 |
| Enforce SSO | 切换现有组织/公司 SSO 连接的强制执行的详情 |
| Enforce SCIM | 切换现有组织/公司 SSO 连接的 SCIM 的详情 |
| Refresh SCIM Token | 刷新现有组织/公司 SSO 连接的 SCIM 令牌的详情 |
| Change SSO Connection Type | 更改现有组织/公司 SSO 连接的连接类型的详情 |
| Toggle JIT provisioning | 切换现有组织/公司 SSO 连接的 JIT 配置的详情 |

### 仓库事件

> [!NOTE]
>
> 包含用户操作的事件描述可能指 Docker 用户名、个人访问令牌 (PAT) 或组织访问令牌 (OAT)。例如，如果用户推送标签到仓库，事件将包含描述：`<user-access-token>` 推送标签到仓库。

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Repository Created | 与新仓库创建相关的活动 |
| Repository Deleted | 与仓库删除相关的活动 |
| Repository Updated | 与更新仓库的描述、完整描述或状态相关的活动 |
| Privacy Changed | 与更新的隐私策略相关的详情 |
| Tag Pushed | 与推送标签相关的活动 |
| Tag Deleted | 与删除标签相关的活动 |
| Categories Updated | 与设置或更新仓库类别相关的活动 |

### 账单事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Plan Upgraded | 当组织的账单计划升级到更高层级计划时发生。|
| Plan Downgraded | 当组织的账单计划降级到更低层级计划时发生。 |
| Seat Added | 当座位添加到组织的账单计划时发生。 |
| Seat Removed | 当座位从组织的账单计划移除时发生。 |
| Billing Cycle Changed | 当组织的收费周期发生变化时发生。|
| Plan Downgrade Canceled | 当组织的计划降级被取消时发生。|
| Seat Removal Canceled | 当组织的账单计划中的座位移除被取消时发生。 |
| Plan Upgrade Requested | 当组织中的用户请求计划升级时发生。 |
| Plan Downgrade Requested | 当组织中的用户请求计划降级时发生。 |
| Seat Addition Requested | 当组织中的用户请求增加座位数量时发生。 |
| Seat Removal Requested | 当组织中的用户请求减少座位数量时发生。 |
| Billing Cycle Change Requested | 当组织中的用户请求更改账单周期时发生。 |
| Plan Downgrade Cancellation Requested | 当组织中的用户请求取消计划降级时发生。 |
| Seat Removal Cancellation Requested | 当组织中的用户请求取消座位移除时发生。 |

### 卸载事件

| 事件                                                          | 描述                                   |
|:------------------------------------------------------------------|:------------------------------------------------|
| Offload Lease Start | 当组织中的卸载租约开始时发生。 |
| Offload Lease End | 当组织中的卸载租约结束时发生。 |