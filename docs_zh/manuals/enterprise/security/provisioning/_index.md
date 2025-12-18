---
description: 了解如何为 SSO 配置配置用户。
keywords: provision users, provisioning, JIT, SCIM, group mapping, sso, docker admin, admin, security
title: 配置用户
linkTitle: 配置
weight: 20
aliases:
 - /security/for-admins/provisioning/
grid:
  - title: "即时 (JIT) 配置"
    description: "在首次登录时设置自动用户创建。适用于设置要求最少的小型团队。"
    icon: "schedule"
    link: "just-in-time/"
  - title: "SCIM 配置"
    description: "在 IdP 和 Docker 之间启用连续的用户数据同步。适合大型组织。"
    icon: "sync"
    link: "scim/"
  - title: "组映射"
    description: "使用 IdP 组配置基于角色的访问控制。适用于需要严格访问控制的组织。"
    icon: "group"
    link: "group-mapping/"
---

{{< summary-bar feature_name="SSO" >}}

配置 SSO 连接后，下一步是配置用户。此过程通过基于身份提供商 (IdP) 数据的自动化用户管理，确保用户能够访问您的组织。

本页面概述了用户配置及支持的配置方法。

## 什么是配置？

配置通过基于身份提供商 (IdP) 自动执行账户创建、更新和停用等任务来帮助管理用户。用户配置有三种方法，每种方法都针对不同的组织需求提供优势：

| 配置方法 | 说明 | Docker 中的默认设置 | 推荐对象 |
| :--- | :--- | :------------- | :--- |
| 即时 (JIT) | 用户首次通过 SSO 登录时自动创建和配置用户账户 | 默认启用 | 需要最少设置、小型团队或低安全环境的组织 |
| 跨域身份管理系统 (SCIM) | 在您的 IdP 和 Docker 之间连续同步用户数据，确保用户属性在无需手动干预的情况下保持更新 | 默认禁用 | 大型组织或用户信息或角色频繁变化的环境 |
| 组映射 | 将用户组从您的 IdP 映射到 Docker 中的特定角色和权限，基于组成员身份实现细粒度访问控制 | 默认禁用 | 需要严格访问控制和基于角色的用户管理的组织 |

## 默认配置设置

配置 SSO 连接时，Docker 默认启用 JIT 配置。启用 JIT 后，用户首次通过 SSO 流程登录时会自动创建用户账户。

对于某些组织，JIT 配置可能无法提供足够的控制或安全性。在这种情况下，可以配置 SCIM 或组映射，以便管理员更好地控制用户访问和属性。

## SSO 属性

用户通过 SSO 登录时，Docker 会从您的 IdP 获取多个属性来管理用户身份和权限。这些属性包括：

- 电子邮件地址：用户的唯一标识符
- 全名：用户的完整姓名
- 组：可选。用于基于组的访问控制
- Docker 组织：可选。指定用户所属的组织
- Docker 团队：可选。定义用户在组织内所属的团队
- Docker 角色：可选。确定用户在 Docker 中的权限
- Docker 会话分钟数：可选。设置用户必须重新向 IdP 认证之前的会话持续时间。必须是大于 0 的正整数。如未提供，将应用默认会话超时

> [!NOTE]
>
> 未指定 Docker 会话分钟数时应用默认会话超时。Docker Desktop 会话在 90 天或 30 天不活动后过期。Docker Hub 和 Docker Home 会话在 24 小时后过期。

## SAML 属性映射

如果您的组织使用 SAML 进行 SSO，Docker 会从 SAML 断言消息中检索这些属性。不同的 IdP 可能对这些属性使用不同的名称。

| SSO 属性	| SAML 断言消息属性 |
| :--- | :--- |
| 电子邮件地址 |	`"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"`, `email` |
| 全名	| `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"`, `name`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname"`, `"http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname"` |
| 组（可选） |	`"http://schemas.xmlsoap.org/claims/Group"`, `"http://schemas.microsoft.com/ws/2008/06/identity/claims/groups"`, `Groups`, `groups` |
| Docker 组织（可选）	| `dockerOrg` |
| Docker 团队（可选） |	`dockerTeam` |
| Docker 角色（可选） |	`dockerRole` |
| Docker 会话分钟数（可选） | `dockerSessionMinutes`, 必须是大于 0 的正整数 |

## 后续步骤

选择最适合您组织需求的配置方法：

{{< grid >}}