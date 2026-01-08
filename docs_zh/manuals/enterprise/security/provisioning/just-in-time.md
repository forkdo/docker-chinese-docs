---
description: 了解即时配置 (JIT) 如何与您的 SSO 连接配合使用。
keywords: user provisioning, just-in-time provisioning, JIT, autoprovision, Docker Admin, admin, security
title: 即时配置 (JIT)
linkTitle: 即时配置 (JIT)
weight: 10
aliases:
- /security/for-admins/provisioning/just-in-time/
---

{{< summary-bar feature_name="SSO" >}}

即时配置 (JIT) 通过在 SSO 身份验证期间自动创建和更新用户账户来简化用户入职流程。这消除了手动创建账户的需要，并确保用户可以立即访问您组织的资源。JIT 会验证用户是否属于该组织，并根据您的身份提供商 (IdP) 配置将他们分配到适当的团队。创建 SSO 连接时，默认情况下会启用 JIT 配置。

本页面介绍了 JIT 配置的工作原理、SSO 身份验证流程以及如何禁用 JIT 配置。

## 先决条件

在开始之前，您必须满足以下条件：

- 为您的组织配置了 SSO
- 拥有 Docker Home 和身份提供商的访问权限

## 启用 JIT 配置的 SSO 身份验证

当用户使用 SSO 登录且您启用了 JIT 配置时，系统会自动执行以下步骤：

1. 系统会检查是否存在与用户电子邮件地址关联的 Docker 账户。

    - 如果账户存在：系统会使用现有账户，并在必要时更新用户的全名。
    - 如果账户不存在：系统会使用基本用户属性（电子邮件、名字和姓氏）创建一个新 Docker 账户。系统会根据用户的电子邮件、姓名和随机数生成唯一的用户名，以确保平台上所有用户名都是唯一的。

2. 系统会检查是否有待处理的 SSO 组织邀请。

    - 找到邀请：邀请会被自动接受。
    - 邀请包含特定组：用户会被添加到 SSO 组织中的该组。

3. 系统会验证 IdP 是否在身份验证期间共享了组映射。

    - 提供了组映射：用户会被分配到相关的组织和团队。
    - 未提供组映射：系统会检查用户是否已经是组织成员。如果不是，用户会被添加到 SSO 连接中配置的默认组织和团队。

下图展示了启用 JIT 的 SSO 身份验证流程概览：

   ![JIT 配置启用工作流程](../images/jit-enabled-flow.svg)

## 禁用 JIT 配置的 SSO 身份验证

当 JIT 配置被禁用时，SSO 身份验证期间会执行以下操作：

1. 系统会检查是否存在与用户电子邮件地址关联的 Docker 账户。

    - 如果账户存在：系统会使用现有账户，并在必要时更新用户的全名。
    - 如果账户不存在：系统会使用基本用户属性（电子邮件、名字和姓氏）创建一个新 Docker 账户。系统会根据用户的电子邮件、姓名和随机数生成唯一的用户名，以确保平台上所有用户名都是唯一的。

2. 系统会检查是否有待处理的 SSO 组织邀请。

   - 找到邀请：如果用户是组织成员或有待处理的邀请，登录会成功，且邀请会被自动接受。
   - 未找到邀请：如果用户不是组织成员且没有待处理的邀请，登录会失败，并显示 `访问被拒绝` 错误。用户必须联系管理员以被邀请加入组织。

禁用 JIT 后，只有在您[启用 SCIM](scim/#enable-scim-in-docker) 时才能使用组映射。如果未启用 SCIM，用户将不会被自动配置到组中。

下图展示了禁用 JIT 的 SSO 身份验证流程概览：

![JIT 配置禁用工作流程](../images/jit-disabled-flow.svg)

## 禁用 JIT 配置

> [!WARNING]
>
> 禁用 JIT 配置可能会中断用户的访问和工作流程。禁用 JIT 后，用户将不会被自动添加到您的组织中。用户必须已经是组织成员或有待处理的邀请才能通过 SSO 成功登录。要在禁用 JIT 的情况下自动配置用户，请[使用 SCIM](./scim.md)。

您可能出于以下原因希望禁用 JIT 配置：

- 您有多个组织，已启用 SCIM，并希望 SCIM 成为配置的真实来源
- 您希望根据组织的安全配置控制和限制使用情况，并希望使用 SCIM 配置访问权限

默认情况下，用户会通过 JIT 进行配置。如果您启用了 SCIM，可以禁用 JIT：

1. 转到 [Docker Home](https://app.docker.com/)，然后从左上角的账户下拉菜单中选择您的组织。
1. 选择 **Admin Console**，然后选择 **SSO and SCIM**。
1. 在 **SSO connections** 表中，选择 **Action** 图标，然后选择 **Disable JIT provisioning**。
1. 选择 **Disable** 以确认。

## 后续步骤

- 配置 [SCIM 配置](/manuals/enterprise/security/provisioning/scim.md) 以进行高级用户管理。
- 设置 [组映射](/manuals/enterprise/security/provisioning/group-mapping.md) 以自动将用户分配到团队。
- 查看 [排查配置问题](/manuals/enterprise/troubleshoot/troubleshoot-provisioning.md)。