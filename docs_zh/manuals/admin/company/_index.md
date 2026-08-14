---
title: 公司概览
linkTitle: 公司
weight: 20
description: 了解如何使用公司管理多个组织，包括管理用户、所有者与安全性。
keywords: company, multiple organizations, manage companies, Docker Home, Docker Business settings
grid:
  - title: 创建公司
    description: 了解如何创建公司。
    icon: building-office-2
    link: /admin/company/new-company/
  - title: 管理公司
    description: 添加组织、管理公司所有者并邀请成员。
    icon: building-storefront
    link: /admin/company/manage/
  - title: 配置 SSO 和 SCIM
    description: 为您的公司设置单点登录和 SCIM 配置。
    icon: key
    link: /enterprise/security/single-sign-on/
  - title: 域名管理
    description: 添加并验证您公司的域名。
    icon: check-badge
    link: /enterprise/security/domain-management/
  - title: 常见问题
    description: 探索有关公司的常见问题。
    link: /faq/admin/company-faqs/
    icon: question-mark-circle
aliases:
  - /docker-hub/creating-companies/
---

{{< summary-bar feature_name="Company" >}}

公司提供了跨多个组织的单一可见性视图，用于集中化的组织和设置管理。拥有 Docker Business 订阅的组织所有者可以创建公司并通过 Docker Home 进行管理。

## 公司结构

下图展示了公司与其关联组织之间的关系。

![展示公司与 Docker 组织关系的图表](/admin/images/docker-admin-structure.webp)

有关完整的管理层级结构，请参阅
[管理概览](/manuals/admin/_index.md#company-and-organization-hierarchy)。

## 公司角色

公司包含一个或多个公司所有者。公司的创建者同时成为公司所有者和组织所有者，并作为组织所有者占用一个席位。创建后，公司可以有多个所有者，每个所有者都能查看整个公司的情况。他们可以管理其下每个组织的设置，并拥有与组织所有者相同的访问权限。

- 一个公司最多可以有十个独立的公司所有者。
- 除非满足以下任一情况，否则公司所有者不占用席位：
  - 他们被添加为公司下某个组织的成员。
  - 启用了 SSO，且公司所有者通过 SSO 登录，这会将其自动添加为组织成员。

要添加或移除公司所有者，请参阅
[管理公司](/manuals/admin/company/manage.md#company-owners)。

## 后续步骤

在以下章节中了解如何创建和管理公司。

{{< grid >}}
