---
title: 管理
description: Docker Admin Console 中的管理功能和角色概述
keywords: 管理员, 管理, 公司, 组织, Admin Console, 用户账户, 账户管理
weight: 10
params:
  sidebar:
    group: Enterprise
grid:
- title: 公司管理
  description: 探索如何管理公司。
  icon: apartment
  link: /admin/company/
- title: 组织管理
  description: 了解组织管理。
  icon: store
  link: /admin/organization/
- title: 为您的组织开通
  description: 了解如何为您的组织开通并保障安全。
  icon: explore
  link: /admin/organization/onboard
- title: 公司 FAQ
  description: 发现关于公司的常见问题和解答。
  icon: help
  link: /faq/admin/company-faqs/
- title: 组织 FAQ
  description: 探索关于组织的热门 FAQ 话题。
  icon: help
  link: /faq/admin/organization-faqs/
- title: 安全
  description: 探索管理员的安全功能。
  icon: shield_locked
  link: /security/
aliases:
- /docker-hub/admin-overview
---

管理员可以使用 [Docker Admin Console](https://app.docker.com/admin) 管理公司和组织。Admin Console 提供了跨 Docker 环境的集中可观测性、访问管理和安全控制。

## 公司和组织层次结构

[Docker Admin Console](https://app.docker.com/admin) 为管理员提供其公司和组织的集中可观测性、访问管理和控制。为了提供这些功能，Docker 使用以下层次结构和角色。

![显示 Docker 管理层次结构的图表，公司位于顶部，然后是组织、团队和成员](./images/docker-admin-structure.webp)

### 公司

公司对多个 Docker 组织进行分组以进行集中配置。公司仅对 Docker Business 订阅者可用。

公司具有以下管理员角色：

- 公司所有者：可以查看和管理公司内的所有组织。具有对公司范围设置的完全访问权限，并继承与组织所有者相同的权限。

### 组织

组织包含团队和仓库。所有 Docker Team 和 Business 订阅者必须至少有一个组织。

组织具有以下管理员角色：

- 组织所有者：可以管理组织设置、用户和访问控制。

### 团队

团队是可选的，允许您对成员进行分组以集体分配仓库权限。团队简化了跨项目或职能的权限管理。

### 成员

成员是添加到组织中的任何 Docker 用户。组织和公司所有者可以为成员分配角色以定义其访问级别。

> [!NOTE]
>
> 创建公司是可选的，但 Team 和 Business 订阅需要组织。

## Admin Console 功能

Docker 的 [Admin Console](https://app.docker.com/admin) 允许您：

- 创建和管理公司和组织
- 为成员分配角色和权限
- 将成员分组到团队中，按项目或角色管理访问
- 设置公司范围的策略，包括 SCIM 配置和安全强制执行

## 管理公司和组织

在以下部分中了解如何管理公司和组织。

{{< grid >}}