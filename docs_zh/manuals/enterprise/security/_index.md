---
linkTitle: Security
title: 企业级安全
description: 了解 Docker 提供的企业级安全功能，并探索最佳实践
keywords: docker, docker hub, docker desktop, security, enterprises, scale
weight: 10
params:
  sidebar:
    group: Enterprise
grid_admins:
- title: Settings Management
  description: 了解设置管理如何保护开发者的开发工作流。
  icon: shield_locked
  link: /enterprise/security/hardened-desktop/settings-management/
- title: Enhanced Container Isolation
  description: 了解增强型容器隔离如何防止容器攻击。
  icon: security
  link: /enterprise/security/hardened-desktop/enhanced-container-isolation/
- title: Registry Access Management
  description: 控制开发者在使用 Docker Desktop 时可访问的注册表。
  icon: home_storage
  link: /enterprise/security/hardened-desktop/registry-access-management/
- title: Image Access Management
  description: 控制开发者可从 Docker Hub 拉取的镜像。
  icon: photo_library
  link: /enterprise/security/hardened-desktop/image-access-management/
- title: "Air-Gapped Containers"
  description: 限制容器访问不需要的网络资源。
  icon: "vpn_lock"
  link: /enterprise/security/hardened-desktop/air-gapped-containers/
- title: Enforce sign-in
  description: 为团队和组织成员配置登录。
  link: /enterprise/security/enforce-sign-in/
  icon: passkey
- title: Domain management
  description: 识别组织中未捕获的用户。
  link: /enterprise/security/domain-management/
  icon: person_search
- title: Docker Scout
  description: 探索 Docker Scout 如何帮助您构建更安全的软件供应链。
  icon: query_stats
  link: /scout/
- title: SSO
  description: 了解如何为您的公司或组织配置 SSO。
  icon: key
  link: /enterprise/security/single-sign-on/
- title: SCIM
  description: 设置 SCIM 以自动配置和取消配置用户。
  icon: checklist
  link: /enterprise/security/provisioning/scim/
- title: Roles and permissions
  description: 为个人分配角色，赋予他们在组织内的不同权限。
  icon: badge
  link: /enterprise/security/roles-and-permissions/
- title: Private marketplace for Extensions (Beta)
  description: 了解如何配置和设置私有市场，为您的 Docker Desktop 用户提供精选的扩展列表。
  icon: storefront
  link: /desktop/extensions/private-marketplace/
- title: Organization access tokens
  description: 创建组织访问令牌作为密码的替代方案。
  link: /enterprise/security/access-tokens/
  icon: password
---

Docker 为管理员和开发者提供了安全保护机制。

如果您是管理员，您可以对开发者的 Docker 产品强制执行登录，并使用 DevOps 安全控制（如增强型容器隔离和注册表访问管理）来扩展、管理和保护您的 Docker Desktop 实例。

## 管理员指南

探索 Docker 提供的安全功能，以满足您公司的安全策略。

{{< grid items="grid_admins" >}}