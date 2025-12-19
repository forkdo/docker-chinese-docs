---
title: 掌握用户和访问管理
summary: 在确保安全性和效率的同时，简化 Docker 中的用户访问。
description: 一份关于使用 SSO 和活动日志等工具管理角色、配置用户以及优化 Docker 访问的指南。
tags: [admin]
params:
  featured: false
  time: 20 分钟
  image:
  resource_links:
    - title: Docker 管理概述
      url: /admin/
    - title: 单点登录
      url: /security/for-admins/single-sign-on/
    - title: 纳入您的组织
      url: /admin/organization/onboard/
    - title: 角色和权限
      url: /security/for-admins/roles-and-permissions/
    - title: 洞察
      url: /admin/organization/insights/
    - title: 活动日志
      url: /admin/organization/activity-logs/
---

管理角色和权限是确保 Docker 环境安全，同时实现轻松协作和运营效率的关键。本指南引导 IT 管理员了解用户和访问管理的基础知识，提供分配角色、配置用户以及使用活动日志和 Insights 等工具来监控和优化 Docker 使用情况的策略。

## 本指南适合谁？

- 负责配置和维护安全用户访问的 IT 团队
- 专注于执行安全访问实践的安全专业人员
- 监督团队协作和资源管理的项目经理

## 您将学到什么

- 如何评估和管理 Docker 用户访问权限，并使账户与组织需求保持一致
- 何时使用团队配置来实现可扩展的访问控制
- 如何使用 SSO、SCIM 和 JIT 自动化和简化用户配置
- 如何充分利用 Docker 的监控工具

## 工具集成

本指南涵盖与以下工具的集成：

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)