---
title: Docker 组织概览
linkTitle: 组织
weight: 10
description: >
  了解 Docker 组织账户如何与个人帐户关联，以及如何管理团队、成员、权限和设置。
keywords: organizations, admin, overview, manage teams, roles, members,
  permissions, organization settings, organization account, individual account,
  Docker ID, account types, owners, teams
grid:
  - title: 组织入驻
    description: 了解如何入驻并保护您的组织。
    icon: magnifying-glass-plus
    link: /admin/organization/setup/onboard
  - title: 管理成员
    description: 了解如何管理成员。
    icon: user-plus
    link: /admin/organization/manage/members/
  - title: 活动日志
    description: 了解如何审计成员的活动。
    icon: document-text
    link: /admin/activity-logs/
  - title: 安全
    description:
      从这里开始管理组织的安全性和访问权限，包括单点登录、配置，以及镜像和仓库访问管理。
    icon: shield-check
    link: /enterprise/security/
---

Docker 组织是在集中管理下的团队和仓库的集合。组织管理员可以大规模地对成员进行分组并分配仓库访问权限。

## 组织结构

下图展示了组织与团队及成员之间的关系。

![展示 Docker 组织内团队与成员关系的示意图](/admin/images/org-structure.webp)

有关组织如何融入更广泛的公司层级结构，请参阅
[管理概览](/manuals/admin/_index.md#company-and-organization-hierarchy)。

## 个人与组织账户

Docker 有两种主要账户类型：

- 由 Docker ID 标识的个人账户。
- 供团队和仓库使用的共享工作空间的组织账户。

每个组织由一个或多个个人账户创建和管理。你始终使用个人账户登录，然后在工作于你所拥有或所属的组织中。组织所有者和成员是在该组织中拥有角色的个人账户。有关个人账户，请参阅 [账户](/manuals/accounts/_index.md)。

## 组织角色

组织包含所有者、成员和可选的团队。组织所有者拥有完整的管理员访问权限，可以管理成员、角色和团队。团队是共享相同仓库权限的可选成员分组。

有关每个角色及其权限的详细信息，请参阅
[角色与权限](/manuals/enterprise/security/roles-and-permissions/_index.md)。

## 后续步骤

在以下章节中了解如何创建和管理您的组织。

{{< grid >}}
