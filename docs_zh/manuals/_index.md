---
title: 手册
description: 通过本系列用户指南，了解如何安装、设置、配置和使用 Docker 产品
keywords: docker, docs, manuals, products, user guides, how-to
url: /manuals/
layout: wide
params:
  icon: description
  sidebar:
    groups:
    - Open source
    - AI
    - Products
    - Platform
    - Enterprise
  notoc: true
  open-source:
  - title: Docker Build
    description: 在任何地方构建和交付任何应用程序。
    icon: build
    link: /build/
  - title: Docker Engine
    description: 行业领先的容器运行时。
    icon: developer_board
    link: /engine/
  - title: Docker Compose
    description: 定义和运行多容器应用程序。
    icon: /icons/Compose.svg
    link: /compose/
  - title: Testcontainers
    description: 使用您喜欢的编程语言以编程方式运行容器。
    icon: /icons/Testcontainers.svg
    link: /testcontainers/
  - title: Cagent
    description: 开源的多智能体解决方案，助您完成任务。
    icon: /icons/cagent.svg
    link: /ai/cagent
  ai:
  - title: Ask Gordon
    description: 借助您的个人 AI 助手，简化工作流程并充分利用 Docker 生态系统。
    icon: note_add
    link: /ai/gordon/
  - title: Docker Model Runner
    description: 查看和管理本地模型。
    icon: /icons/models.svg
    link: /ai/model-runner/
  - title: MCP Catalog and Toolkit
    description: 使用 MCP 服务器增强您的 AI 工作流程。
    icon: /icons/toolkit.svg
    link: /ai/mcp-catalog-and-toolkit/
  products:
  - title: Docker Desktop
    description: 容器开发的指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker Hardened Images
    description: 用于可信软件交付的安全、最小化镜像。
    icon: /icons/dhi.svg
    link: /dhi/
  - title: Docker Offload
    description: 在云中构建和运行容器。
    icon: cloud
    link: /offload/
  - title: Build Cloud
    description: 在云中更快地构建镜像。
    icon: /icons/logo-build-cloud.svg
    link: /build-cloud/
  - title: Docker Hub
    description: 发现、共享和集成容器镜像。
    icon: hub
    link: /docker-hub/
  - title: Docker Scout
    description: 镜像分析和策略评估。
    icon: /icons/Scout.svg
    link: /scout/
  - title: Docker Extensions
    description: 自定义您的 Docker Desktop 工作流程。
    icon: extension
    link: /extensions/
  - title: Testcontainers Cloud
    description: 在云中运行具有真实依赖项的集成测试。
    icon: package_2
    link: https://testcontainers.com/cloud/docs/
  platform:
  - title: Administration
    description: 面向公司和组织的集中式可观察性。
    icon: admin_panel_settings
    link: /admin/
  - title: Billing
    description: 管理账单和支付方式。
    icon: payments
    link: /billing/
  - title: Accounts
    description: 管理您的 Docker 账户。
    icon: account_circle
    link: /accounts/
  - title: Security
    description: 面向管理员和开发人员的安全保障。
    icon: lock
    link: /security/
  - title: Subscription
    description: Docker 产品的商业使用许可。
    icon: card_membership
    link: /subscription/
  enterprise:
  - title: Deploy Docker Desktop
    description: 在公司内部大规模部署 Docker Desktop
    icon: download
    link: /enterprise/enterprise-deployment/
---

本节包含关于如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源

开源开发和容器化技术。

{{< grid items=open-source >}}

## AI

所有 Docker AI 工具，尽在一个易于访问的位置。

{{< grid items=ai >}}

## 产品

面向创新团队的端到端开发者解决方案。

{{< grid items=products >}}

## 平台

与 Docker 平台相关的文档，例如管理和订阅管理。

{{< grid items=platform >}}

## 企业

面向 IT 管理员，提供关于如何大规模部署 Docker Desktop 的帮助，以及与安全相关功能的配置指导。

{{< grid items=enterprise >}}