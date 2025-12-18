---
description: 了解 Just-in-Time 配置如何与你的 SSO 连接配合工作。
keywords: 用户配置, Just-in-Time 配置, JIT, 自动配置, Docker Admin, 管理员, 安全
title: Just-in-Time 配置
linkTitle: Just-in-Time
weight: 10
aliases:
 - /security/for-admins/provisioning/just-in-time/
---

{{< summary-bar feature_name="SSO" >}}

Just-in-Time (JIT) 配置通过在 SSO 身份验证期间自动创建和更新用户账户来简化用户入职流程。这消除了手动账户创建，并确保用户能够立即访问你组织的资源。JIT 会验证用户是否属于该组织，并根据你的身份提供商 (IdP) 配置将他们分配到相应的团队。当你创建 SSO 连接时，JIT 配置默认为启用状态。

本页面解释了 JIT 配置的工作原理、SSO 身份验证流程，以及如何禁用 JIT 配置。

## 前置条件

开始之前，你必须具备：

- 为你的组织配置了 SSO
- 对 Docker Home 和你的身份提供商具有管理员访问权限

## 启用 JIT 配置的 SSO 身份验证

当用户使用 SSO 登录且你启用了 JIT 配置时，系统会自动执行以下步骤：

1. 系统检查是否已为用户的电子邮件地址创建了 Docker 账户。

    - 如果账户存在：系统使用现有账户，并在必要时更新用户的全名。
    - 如果账户不存在：系统使用基本用户属性（电子邮件、名字和姓氏）创建一个新的 Docker 账户。系统会基于用户的电子邮件、名字和随机数字生成一个唯一的用户名，以确保所有用户名在平台中唯一。

2. 系统检查是否有针对 SSO 组织的待处理邀请。

    - 找到邀请：邀请会自动被接受。
    - 邀请包含特定组：用户会被添加到 SSO 组织中的该组。

3. 系统验证 IdP 在身份验证期间是否共享了组映射。

    - 提供了组映射：用户被分配到相关的组织和团队。
    - 未提供组映射：系统检查用户是否已经是组织成员。如果不是，用户会被添加到 SSO 连接中配置的默认组织和团队。

下图概述了启用 JIT 的 SSO 身份验证流程：

   ![启用 JIT 配置的工作流](../images/jit-enabled-flow.svg)

## 禁用 JIT 配置的 SSO 身份验证

当 JIT 配置被禁用时，SSO 身份验证期间会发生以下操作：

1. 系统检查是否已为用户的电子邮件地址创建了 Docker 账户。

    - 如果账户存在：系统使用现有账户，并在必要时更新用户的全名。
    - 如果账户不存在：系统使用基本用户属性（电子邮件、名字和姓氏）创建一个新的 Docker 账户。系统会基于用户的电子邮件、名字和随机数字生成一个唯一的用户名，以确保所有用户名在平台中唯一。

2. 系统检查是否有针对 SSO 组织的待处理邀请。

   - 找到邀请：如果用户是组织成员或有待处理邀请，登录成功，邀请会自动被接受。
   - 未找到邀请：如果用户不是组织成员且无待处理邀请，登录失败，显示 `Access denied` 错误。用户必须联系管理员以获得组织邀请。

禁用 JIT 后，只有在启用 [SCIM](scim/#enable-scim-in-docker) 时才能使用组映射。如果未启用 SCIM，用户不会被自动配置到组中。

下图概述了禁用 JIT 的 SSO 身份验证流程：

![禁用 JIT 配置的工作流](../images/jit-disabled-flow.svg)

## 禁用 JIT 配置

> [!WARNING]
>
> 禁用 JIT 配置可能会影响用户的访问和工作流程。禁用 JIT 后，用户不会被自动添加到你的组织中。用户必须已经是组织成员或有待处理邀请才能通过 SSO 成功登录。要在禁用 JIT 的情况下自动配置用户，请[使用 SCIM](./scim.md)。

你可能因以下原因想要禁用 JIT 配置：

- 你有多个组织，已启用 SCIM，并希望 SCIM 成为配置的唯一来源
- 你希望通过组织的安全配置来控制和限制使用，并希望使用 SCIM 来配置访问权限

JIT 默认为用户启用。如果你启用了 SCIM，可以禁用 JIT：

1. 前往 [Docker Home](https://app.docker.com/)，从左上角账户下拉菜单中选择你的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择 **Action** 图标，然后选择 **Disable JIT provisioning**。
1. 选择 **Disable** 以确认。

## 后续步骤

- 配置 [SCIM 配置](/manuals/enterprise/security/provisioning/scim.md) 以进行高级用户管理。
- 设置 [组映射](/manuals/enterprise/security/provisioning/group-mapping.md) 以自动将用户分配到团队。
- 查看 [配置故障排除](/manuals/enterprise/troubleshoot/troubleshoot-provisioning.md)。