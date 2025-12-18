---
title: 手册
description: 通过本系列用户指南学习如何安装、设置、配置和使用 Docker 产品
keywords: docker, 文档, 手册, 产品, 用户指南, 操作指南
# 硬编码此页面的 URL
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
    description: 构建并部署任何应用到任意环境。
    icon: build
    link: /build/
  - title: Docker Engine
    description: 行业领先的容器运行时。
    icon: developer_board
    link: /engine/
  - title: Docker Compose
    description: 定义和运行多容器应用。
    icon: /icons/Compose.svg
    link: /compose/
  - title: Testcontainers
    description: 使用您首选的编程语言以编程方式运行容器。
    icon: /icons/Testcontainers.svg
    link: /testcontainers/
  - title: Cagent
    description: 协助您完成任务的开源多智能体解决方案。
    icon: /icons/cagent.svg
    link: /ai/cagent
  ai:
  - title: Ask Gordon
    description: 使用您的个人 AI 助手简化工作流程，充分利用 Docker 生态系统。
    icon: note_add
    link: /ai/gordon/
  - title: Docker Model Runner
    description: 查看和管理您的本地模型。
    icon: /icons/models.svg
    link: /ai/model-runner/
  - title: MCP Catalog and Toolkit
    description: 使用 MCP 服务器增强您的 AI 工作流程。
    icon: /icons/toolkit.svg
    link: /ai/mcp-catalog-and-toolkit/
  products:
  - title: Docker Desktop
    description: 您的容器开发指挥中心。
    icon: /icons/Whale.svg
    link: /desktop/
  - title: Docker Hardened Images
    description: 安全、精简的镜像，用于可信的软件交付。
    icon: /icons/dhi.svg
    link: /dhi/
  - title: Docker Offload
    description: 在云端构建和运行容器。
    icon: cloud
    link: /offload/
  - title: Build Cloud
    description: 在云端更快地构建您的镜像。
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
    description: 在云端使用真实依赖项运行集成测试。
    icon: package_2
    link: https://testcontainers.com/cloud/docs/
  platform:
  - title: Administration
    description: 为公司和组织提供集中式可观测性。
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
    description: 为管理员和开发人员提供安全保护。
    icon: lock
    link: /security/
  - title: Subscription
    description: Docker 产品的商业使用许可证。
    icon: card_membership
    link: /subscription/
  enterprise:
  - title: Deploy Docker Desktop
    description: 在公司范围内大规模部署 Docker Desktop
    icon: download
    link: /enterprise/enterprise-deployment/
---

本节包含有关如何安装、设置、配置和使用 Docker 产品的用户指南。

## 开源

开源开发和容器化技术。

{{< grid items=open-source >}}

## AI

所有 Docker AI 工具的集中访问位置。

{{< grid items=ai >}}

## 产品

面向创新团队的端到端开发者解决方案。

{{< grid items=products >}}

## 平台

与 Docker 平台相关的文档，例如管理和订阅管理。

{{< grid items=platform >}}

## 企业

面向 IT 管理员，提供大规模部署 Docker Desktop 的帮助，以及与安全功能相关的配置指导。

{{< grid items=enterprise >}}