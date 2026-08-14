---
title: SCIM 概述
linkTitle: SCIM
weight: 10
description: 了解跨域身份管理系统的工作原理以及如何进行设置。
keywords: SCIM, SSO, user provisioning, de-provisioning, role mapping, assign users
aliases:
  - /security/for-admins/scim/
  - /security/for-admins/provisioning/scim/
---

{{< summary-bar feature_name="SSO" >}}

使用跨域身份管理系统（SCIM，System for Cross-domain Identity Management）为您的 Docker 组织自动化用户管理。SCIM 会自动配置和取消配置用户、同步团队成员身份，并使您的 Docker 组织与您的身份提供商保持同步。

本页向您展示如何使用 SCIM 为 Docker 自动化用户配置和取消配置。

## 先决条件

在开始之前，您必须满足以下条件：

- 为您的组织配置了 SSO
- 拥有 Docker Home 和身份提供商的管理员访问权限

## SCIM 的工作原理

SCIM 通过您的身份提供商为 Docker 自动化用户配置和取消配置。启用 SCIM 后，任何在您的身份提供商中分配给 Docker 应用程序的用户都会自动被配置并添加到您的 Docker 组织。当某个用户在您的身份提供商中从 Docker 应用程序移除时，SCIM 会停用并将其从您的 Docker 组织中移除。

除了配置和移除之外，SCIM 还会同步在身份提供商中进行的个人资料更新（例如姓名更改）。您可以将 SCIM 与 Docker 默认的即时 (JIT) 配置一起使用，也可以在禁用 JIT 的情况下单独使用。

SCIM 自动化以下内容：

- 创建用户
- 更新用户个人资料
- 移除和停用用户
- 重新激活用户
- 组映射

> [!NOTE]
>
> SCIM 仅管理在 SCIM 启用后通过您的身份提供商配置的用户。它无法移除在 SCIM 设置之前手动添加到您 Docker 组织的用户。
>
> 要移除这些用户，请从您的 Docker 组织中手动删除他们。有关更多信息，请参阅 [管理组织成员](/manuals/admin/organization/manage/members.md)。

## 后续步骤

- 如果您在启用 SCIM 之前是通过即时 (JIT) 配置的用户，请参阅[将 JIT 迁移到 SCIM](/manuals/enterprise/security/provisioning/scim/migrate-scim.md)。
- [组映射](/manuals/enterprise/security/provisioning/scim/group-mapping.md) 以将身份提供商组与成员同步。
- [排查配置问题](/manuals/enterprise/security/provisioning/troubleshoot-provisioning.md) 了解 SCIM、JIT 和属性相关问题。
