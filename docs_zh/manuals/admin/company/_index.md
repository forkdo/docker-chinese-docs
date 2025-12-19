---
title: 公司管理概览
weight: 20
description: 了解如何使用公司管理多个组织，包括管理用户、所有者以及安全性。
keywords: company, multiple organizations, manage companies, admin console, Docker Business settings
grid:
- title: 创建公司
  description: 了解如何创建公司。
  icon: apartment
  link: /admin/company/new-company/
- title: 管理组织
  description: 了解如何在公司中添加和管理组织以及席位。
  icon: store
  link: /admin/company/organizations/
- title: 管理公司所有者
  description: 详细了解公司所有者以及如何管理他们。
  icon: supervised_user_circle
  link: /admin/company/owners/
- title: 管理用户
  description: 探索如何管理所有组织中的用户。
  icon: group_add
  link: /admin/company/users/
- title: 配置单点登录
  description: 了解如何为整个公司配置 SSO。
  icon: key
  link: /security/for-admins/single-sign-on/
- title: 设置 SCIM
  description: 设置 SCIM 以自动配置和取消配置公司中的用户。
  icon: checklist
  link: /security/for-admins/provisioning/scim/
- title: 域名管理
  description: 添加并验证公司的域名。
  icon: domain_verification
  link: /security/for-admins/domain-management/
- title: 常见问题
  description: 探索有关公司的常见问题。
  link: /faq/admin/company-faqs/
  icon: help
aliases:
- /docker-hub/creating-companies/
---

{{< summary-bar feature_name="Company" >}}

公司提供了跨多个组织的单一可见性视图，简化了组织和设置管理。

拥有 Docker Business 订阅的组织所有者可以创建公司并通过 [Docker 管理控制台](https://app.docker.com/admin) 进行管理。

下图展示了公司与其关联组织之间的关系。

![展示公司与 Docker 组织关系的图表](/admin/images/docker-admin-structure.webp)

## 主要功能

通过公司，管理员可以：

- 查看和管理所有嵌套组织
- 集中配置公司和组织设置
- 控制对公司访问权限
- 最多可将十名唯一用户分配为公司所有者角色
- 为所有嵌套组织配置 SSO 和 SCIM
- 强制公司中所有用户使用 SSO

## 创建和管理公司

在以下章节中了解如何创建和管理公司。

{{< grid >}}