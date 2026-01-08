---
title: 角色与权限
linkTitle: 角色与权限
description: 使用 Docker 的角色系统控制对内容、注册表和组织管理的访问权限
keywords: roles, permissions, custom roles, core roles, access control, organization management, docker hub, admin console, security
tags:
- admin
aliases:
- /admin/organization/roles/
- /security/for-admins/roles-and-permissions/
grid:
- title: 核心角色
  description: 了解 Docker 内置的 Member、Editor 和 Owner 角色及其预定义权限。
  icon: admin_panel_settings
  link: /enterprise/security/roles-and-permissions/core-roles/
- title: 自定义角色
  description: 创建符合组织特定需求的定制化权限组合。
  icon: tune
  link: /enterprise/security/roles-and-permissions/custom-roles/
weight: 40
---

{{< summary-bar feature_name="General admin" >}}

角色控制用户在 Docker 组织中可执行的操作。当您邀请用户或创建团队时，需为其分配角色，这些角色决定了他们对仓库、团队和组织设置的权限。

Docker 提供两种角色类型以满足不同的组织需求：

- [核心角色](/manuals/enterprise/security/roles-and-permissions/core-roles.md) 具有预定义权限
- [自定义角色](/manuals/enterprise/security/roles-and-permissions/custom-roles.md) 可根据您的特定需求进行定制

## Docker 角色

### 核心角色

核心角色是 Docker 内置的、具有预定义权限组合的角色：

- **Member**：非管理角色，具有基本访问权限。成员可以查看组织内的其他成员，并从其有权访问的仓库中拉取镜像。
- **Editor**：部分管理权限。编辑者可以创建、编辑和删除仓库，并管理仓库的团队权限。
- **Owner**：完全管理权限。所有者可以管理所有组织设置，包括仓库、团队、成员、账单和安全功能。

### 自定义角色

自定义角色允许您从用户管理、团队管理、账单和 Hub 权限等类别中选择特定权限，创建定制化的权限组合。当 Docker 的核心角色无法满足您的需求时，请使用自定义角色。

## 何时使用每种角色

在以下情况下使用核心角色：

- Docker 的预定义权限组合与您的组织结构相匹配
- 您希望进行简单直接的角色分配
- 您刚开始使用 Docker 组织管理
- 您的访问控制需求是标准的，不需要细粒度权限

在以下情况下使用自定义角色：

- 您需要核心角色中未提供特定权限组合
- 您希望创建专门的权限角色，如账单管理员、安全审计员或仓库管理员
- 您需要按部门进行访问控制
- 您希望通过精确的权限授予来实施最小权限原则

## 角色如何协同工作

您可以为用户和团队分配核心角色或自定义角色，但不能同时分配两者。然而，角色与团队权限协同工作：

1. **角色权限**：应用于整个组织（核心或自定义角色）。自定义角色可以同时授予组织范围的设置权限和仓库访问权限。
2. **团队权限**：当用户被添加到团队时，会获得额外的仓库特定权限。这是与基于角色的权限系统分离的权限系统。

这种分层方法为您提供了灵活性，通过角色提供广泛的组织访问权限，通过团队成员身份提供特定的仓库访问权限。

## 后续步骤

选择最适合您组织需求的角色类型：

{{< grid >}}