---
title: 使用 Docker 为公司成功奠定基础
linkTitle: 管理员设置
summary: 通过优化工作流、标准化开发环境以及确保公司范围内的顺畅部署，充分发挥 Docker 的优势。
description: 了解如何为公司配置并充分利用所有 Docker 产品和功能。
tags: [admin]
params:
  time: 20 分钟
  image:
  resource_links:
    - title: Docker 管理概述
      url: /admin/
    - title: 单点登录
      url: /security/for-admins/single-sign-on/
    - title: 强制登录
      url: /security/for-admins/enforce-sign-in/
    - title: 角色和权限
      url: /security/for-admins/roles-and-permissions/
    - title: 设置管理
      url: /security/for-admins/hardened-desktop/settings-management/
    - title: 仓库访问管理
      url: /security/for-admins/hardened-desktop/registry-access-management/
    - title: 镜像访问管理
      url: /security/for-admins/hardened-desktop/image-access-management/
    - title: Docker 订阅信息
      url: /subscription/details/
---

Docker 的工具提供了一个可扩展、安全的平台，赋能您的开发者更快地创建、交付和运行应用程序。作为管理员，您可以优化工作流、标准化开发环境，并确保组织内的顺畅部署。

通过配置 Docker 产品以满足公司的需求，您可以优化性能、简化用户管理，并对资源保持控制。本指南帮助您设置和配置 Docker 产品，以最大化团队的生产力和成功率，同时满足合规性和安全策略。

## 适用对象

- 负责管理组织内 Docker 环境的管理员
- 希望优化开发和部署工作流的 IT 领导者
- 旨在为多个用户标准化应用程序环境的团队
- 希望优化 Docker 产品使用以获得更大可扩展性和效率的组织
- 拥有 [Docker Business 订阅](https://www.docker.com/pricing/) 的组织

## 您将学到的内容

- 为什么登录公司 Docker 组织可以访问使用数据和增强功能
- 如何标准化 Docker Desktop 版本和设置，为所有用户创建一致的基础，同时允许高级开发者保持灵活性
- 实施 Docker 安全配置的策略，以满足公司 IT 和软件开发安全要求，同时不影响开发者效率

## 涵盖的功能

本指南涵盖以下 Docker 功能：

- [组织](/manuals/admin/organization/_index.md)：管理 Docker 环境的核心结构，将用户、团队和镜像仓库分组。您的组织随订阅创建，由一个或多个所有者管理。登录组织的用户根据购买的订阅分配席位。
- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)：默认情况下，Docker Desktop 不要求登录。您可以配置设置以强制登录，确保开发者登录到您的 Docker 组织。
- [SSO](/manuals/enterprise/security/single-sign-on/_index.md)：没有 SSO 时，Docker 组织中的用户管理是手动的。在身份提供商和 Docker 之间设置 SSO 连接可确保符合安全策略并自动配置用户。添加 SCIM 可进一步自动配置和取消配置用户。
- 通用和安全设置：配置关键设置可确保 Docker 产品在您的环境中顺利上线和使用。您还可以根据公司的特定安全需求启用安全功能。

## 需要参与的人员

- Docker 组织所有者：必须参与流程，且在几个关键步骤中是必需的
- DNS 团队：SSO 设置期间需要验证公司域名
- MDM 团队：负责将 Docker 特定配置文件分发到开发者机器
- 身份提供商团队：需要配置身份提供商并在设置期间建立 SSO 连接
- 开发负责人：熟悉 Docker 配置的开发负责人，帮助为开发者设置建立基础
- IT 团队：熟悉公司桌面策略的 IT 代表，协助将 Docker 配置与这些策略对齐
- 信息安全团队：熟悉公司开发安全策略的安全团队成员，协助配置安全功能
- Docker 测试人员：一小部分开发者，在全面部署前测试新设置和配置

## 工具集成

本指南涵盖与以下工具的集成：

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)
- MDM 解决方案如 Intune