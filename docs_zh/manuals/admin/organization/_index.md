---
title: 组织管理概述
linkTitle: 组织管理
weight: 10
description: 了解如何管理您的 Docker 组织，包括团队、成员、权限和设置。
keywords: 组织, 管理员, 概述, 管理团队, 角色
grid:
- title: 组织入职
  description: 了解如何完成组织入职并保障其安全。
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
  description: 控制您的开发者可以拉取哪些类型的镜像。
  icon: photo_library
  link: /admin/organization/image-access/
- title: 注册表访问管理
  description: 定义您的开发者可以访问哪些注册表。
  icon: home_storage
  link: /admin/organization/registry-access/
- title: 组织设置
  description: 为您的组织配置信息并管理设置。
  icon: settings
  link: /admin/organization/general-settings/
- title: SSO 和 SCIM
  description: '为您的组织设置 [单点登录 (Single Sign-On)](/security/for-admins/single-sign-on/)
    和 [SCIM](/security/for-admins/provisioning/scim/)。

    '
  icon: key
- title: 域名管理
  description: 添加、验证和审计您的域名。
  link: /security/for-admins/domain-management/
  icon: domain_verification
- title: 常见问题
  description: 探索常见的组织 FAQ。
  link: /faq/admin/organization-faqs/
  icon: help
---

Docker 组织是一组包含集中管理功能的团队和仓库集合。它帮助管理员对成员和权限进行分组管理，实现高效、可扩展的管理方式。

## 组织结构

下图展示了组织如何与团队和成员相关联。

![展示团队和成员在 Docker 组织内关系的图表](/admin/images/org-structure.webp)

## 组织成员

组织所有者拥有完全的管理员权限，可以管理整个组织的成员、角色和团队。

一个组织包括成员和可选的团队。团队有助于对成员进行分组，并简化权限管理。

## 创建和管理您的组织

请参阅以下章节，了解如何创建和管理您的组织。

{{< grid >}}