---
title: 角色和权限
linkTitle: 角色和权限
description: 使用 Docker 的角色系统控制对内容、注册表和组织管理的访问
keywords: roles, permissions, custom roles, core roles, access control, organization management, docker hub, admin console, security
tags: [admin]
aliases:
  - /admin/organization/roles/
  - /security/for-admins/roles-and-permissions/
grid:
  - title: "核心角色"
    description: 了解 Docker 内置的 Member、Editor 和 Owner 角色及其预定义权限。
    icon: "admin_panel_settings"
    link: /enterprise/security/roles-and-permissions/core-角色/
  - title: "自定义角色"
    description: 创建符合您组织特定需求的定制化权限集。
    icon: "tune"
    link: /enterprise/security/roles-and-permissions/自定义-角色/
weight: 40
---

{{< summary-bar feature_name="General admin" >}}

角色控制用户在您的 Docker 组织中可以执行的操作。当您邀请用户或创建团队时，您会为他们分配角色，这些角色决定了他们对仓库、团队和组织设置的权限。

Docker 提供两种类型的角色以满足不同的组织需求：

- [核心角色](/manuals/enterprise/security/roles-and-permissions/核心-角色.md)，具有预定义的权限集
- [自定义角色](/manuals/enterprise/security/roles-and-permissions/自定义-角色.md)，您可以根据特定需求进行定制

## Docker 角色

### 核心角色

核心角色是 Docker 内置的角色，具有预定义的权限集：

- **Member（成员）**：非管理角色，具有基本访问权限。成员可以查看组织中的其他成员，并从他们有权限的仓库中拉取镜像。
- **Editor（编辑者）**：具有部分管理访问权限。编辑者可以创建、编辑和删除仓库，并管理团队对仓库的权限。
- **Owner（所有者）**：具有完全管理访问权限。所有者可以管理所有组织设置，包括仓库、团队、成员、账单和安全功能。

### 自定义角色

自定义角色允许您通过从用户管理、团队管理、账单和 Hub 权限等类别中选择特定权限来创建定制的权限集。当 Docker 的核心角色无法满足您的需求时，请使用自定义角色。

## 何时使用每种角色

在以下情况下使用核心角色：

- Docker 的预定义权限集符合您的组织结构
- 您希望进行简单、直接的角色分配
- 您刚开始使用 Docker 组织管理
- 您的访问控制需求是标准的，不需要细粒度的权限

在以下情况下使用自定义角色：

- 您需要核心角色中没有的特定权限组合
- 您想要创建专门的角色，如账单管理员、安全审计员或仓库管理员
- 您需要部门特定的访问控制
- 您希望通过精确的权限授予来实施最小权限原则

## 角色如何协同工作

您可以为用户和团队分配核心角色或自定义角色，但不能同时分配两者。然而，角色会与团队权限结合使用：

1. **角色权限**：在组织范围内应用（核心角色或自定义角色）。自定义角色可以授予对组织范围设置和仓库访问的权限。
2. **团队权限**：当用户被添加到团队时，提供额外的仓库特定权限。这是与基于角色的权限系统分开的权限系统。

这种分层方法为您提供了灵活性，可以通过角色提供广泛的组织访问权限，并通过团队成员身份提供特定的仓库访问权限。

## 后续步骤

选择最适合您组织需求的角色类型：

{{< grid >}}