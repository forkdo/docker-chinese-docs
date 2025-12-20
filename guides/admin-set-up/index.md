# 使用 Docker 为您的公司奠定成功基础

Docker 的工具提供了一个可扩展、安全的平台，使您的开发人员能够更快地创建、交付和运行应用程序。作为管理员，您可以简化工作流程、标准化开发环境，并确保整个组织的平稳部署。

通过配置 Docker 产品以满足您公司的需求，您可以优化性能、简化用户管理并保持对资源的控制。本指南帮助您设置和配置 Docker 产品，以在满足合规性和安全策略的同时，最大化团队的生产力和成功。

## 本指南面向谁？

- 负责管理组织内 Docker 环境的管理员
- 希望简化开发和部署工作流程的 IT 领导者
- 旨在跨多个用户标准化应用环境的团队
- 寻求优化 Docker 产品使用以获得更高可扩展性和效率的组织
- 拥有 [Docker Business 订阅](https://www.docker.com/pricing/) 的组织

## 您将学到什么

- 为什么登录您公司的 Docker 组织可以访问使用数据和增强功能
- 如何标准化 Docker Desktop 版本和设置，为所有用户创建一致的基准，同时为高级开发人员保留灵活性
- 实施 Docker 安全配置的策略，以满足公司 IT 和软件开发安全要求，同时不妨碍开发人员的生产力

## 涵盖的功能

本指南涵盖以下 Docker 功能：

- [组织](/manuals/admin/organization/_index.md)：管理 Docker 环境的核心结构，用于对用户、团队和镜像仓库进行分组。您的组织随订阅一起创建，并由一个或多个所有者管理。登录组织的用户会根据购买的订阅分配席位。
- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)：默认情况下，Docker Desktop 不要求登录。您可以配置设置来强制执行此操作，并确保您的开发人员登录到您的 Docker 组织。
- [SSO](/manuals/enterprise/security/single-sign-on/_index.md)：如果没有 SSO，Docker 组织中的用户管理是手动的。在您的身份提供商和 Docker 之间建立 SSO 连接可确保符合您的安全策略并自动配置用户。添加 SCIM 可进一步自动配置和取消配置用户。
- 常规和安全设置：配置关键设置可确保 Docker 产品在您的环境中的顺利设置和使用。您还可以根据公司的特定安全需求启用安全功能。

## 需要哪些人员参与

- Docker 组织所有者：必须参与此过程，并且是几个关键步骤所必需的。
- DNS 团队：在 SSO 设置期间需要验证公司域名。
- MDM 团队：负责将特定于 Docker 的配置文件分发给开发人员计算机。
- 身份提供商团队：在设置过程中需要配置身份提供商和建立 SSO 连接。
- 开发负责人：了解 Docker 配置的开发负责人，帮助为开发人员设置建立基准。
- IT 团队：熟悉公司桌面策略的 IT 代表，协助将 Docker 配置与这些策略保持一致。
- 信息安全 (Infosec)：了解公司开发安全策略的安全团队成员，帮助配置安全功能。
- Docker 测试人员：一小群开发人员，用于在全面部署之前测试新设置和配置。

## 工具集成

本指南涵盖与以下工具的集成：

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)
- 像 Intune 这样的 MDM 解决方案

- [沟通与信息收集](/guides/admin-set-up/comms-and-info-gathering/)

- [最终确定计划并开始设置](/guides/admin-set-up/finalize-plans-and-setup/)

- [测试](/guides/admin-set-up/testing/)

- [部署您的 Docker 设置](/guides/admin-set-up/deploy/)

