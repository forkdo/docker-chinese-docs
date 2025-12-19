---
title: 组织管理概览
linkTitle: 组织管理
weight: 10
description: 了解如何管理您的 Docker 组织，包括团队、成员、权限和设置。
keywords: organizations, admin, overview, manage teams, roles
grid:
- title: 组织入门
  description: 了解如何入门并保障您的组织安全。
  icon: explore
  link: /admin/organization/onboard
- title: 管理成员
  description: 探索如何管理成员。
  icon: group_add
  link: /admin/organization/members/
- title: 活动日志
  description: 了解如何审计成员的活动。
  icon: text_snippet
  link: /admin/organization/activity-logs/
- title: 镜像访问管理
  description: 控制您的开发者可以拉取的镜像类型。
  icon: photo_library
  link: /admin/organization/image-access/
- title: 仓库访问管理
  description: 定义您的开发者可以访问的仓库。
  icon: home_storage
  link: /admin/organization/registry-access/
- title: 组织设置
  description: 为您的组织配置信息并管理设置。
  icon: settings
  link: /admin/organization/general-settings/
- title: SSO 和 SCIM
  description: '为您的组织设置[单点登录](/security/for-admins/single-sign-on/)
    和 [SCIM](/security/for-admins/provisioning/scim/)。

    '
  icon: key
- title: 域名管理
  description: 添加、验证和审计您的域名。
  link: /security/for-admins/domain-management/
  icon: domain_verification
- title: 常见问题
  description: 探索常见的组织相关问题。
  link: /faq/admin/organization-faqs/
  icon: help
---

Docker 组织是一个由团队和仓库组成的集合，并采用集中式管理。它帮助管理员以一种精简且可扩展的方式对成员进行分组并分配访问权限。

## 组织结构

下图展示了组织与团队及成员之间的关系。

![展示 Docker 组织内团队与成员关系的示意图](/admin/images/org-structure.webp)

## 组织成员

组织所有者拥有完整的管理员访问权限，可以管理整个组织内的成员、角色和团队。

一个组织包含成员和可选的团队。团队帮助对成员进行分组并简化权限管理。

## 创建和管理您的组织

在以下章节中，您将学习如何创建和管理您的组织。

{{< grid >}}