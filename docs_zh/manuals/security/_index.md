---
title: 开发者安全
linkTitle: 安全
description: 了解开发者级别的安全功能，如双因素认证（2FA）和访问令牌
keywords: docker, docker hub, docker desktop, 安全, 开发者安全, 2FA, 访问令牌
weight: 40
params:
  sidebar:
    group: Platform
grid_developers:
- title: 设置双因素认证
  description: 为您的 Docker 账户添加额外的身份验证层。
  link: /security/2fa/
  icon: phonelink_lock
- title: 管理访问令牌
  description: 创建个人访问令牌作为密码的替代方案。
  icon: password
  link: /security/access-tokens/
- title: 静态漏洞扫描
  description: 对您的 Docker 镜像自动执行一次性漏洞扫描。
  icon: image_search
  link: /docker-hub/repos/manage/vulnerability-scanning/
- title: Docker Engine 安全
  description: 了解如何保持 Docker Engine 的安全。
  icon: security
  link: /engine/security/
- title: Docker Compose 中的机密管理
  description: 学习如何在 Docker Compose 中使用机密。
  icon: privacy_tip
  link: /compose/how-tos/use-secrets/
grid_resources:
- title: 安全常见问题
  description: 探索常见的安全问题解答。
  icon: help
  link: /faq/security/general/
- title: 安全最佳实践
  description: 了解您可以采取的提升容器安全性的步骤。
  icon: category
  link: /develop/security-best-practices/
- title: 使用 VEX 抑制 CVE
  description: 学习如何抑制在您的镜像中发现的不适用或已修复的漏洞。
  icon: query_stats
  link: /scout/guides/vex/
- title: Docker Hardened 镜像
  description: 学习如何使用 Docker Hardened 镜像增强您的软件供应链安全。
  icon: encrypted_add_circle
  link: /dhi/
---

Docker 通过其开发者级别的安全功能，帮助您保护本地环境、基础设施和网络。

使用双因素认证（2FA）、个人访问令牌和 Docker Scout 等工具来管理访问权限，并在工作流程早期检测漏洞。您还可以通过 Docker Compose 安全地集成机密信息，或使用 Docker Hardened 镜像增强您的软件供应链安全。

请浏览以下部分以了解更多信息。

## 开发者指南

{{< grid items="grid_developers" >}}

## 更多资源

{{< grid items="grid_resources" >}}