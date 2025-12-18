---
title: Hardened Docker Desktop
linkTitle: Hardened Docker Desktop
description: Security features that help organizations secure developer environments without impacting productivity
keywords: security, hardened desktop, enhanced container isolation, registry access management, settings management, admins, docker desktop, image access management, air-gapped containers
tags: [admin]
aliases:
 - /desktop/hardened-desktop/
 - /security/for-admins/hardened-desktop/
grid:
  - title: "Settings Management"
    description: Learn how Settings Management can secure your developers' workflows.
    icon: shield_locked
    link: /enterprise/security/hardened-desktop/settings-management/
  - title: "Enhanced Container Isolation"
    description: Understand how Enhanced Container Isolation can prevent container attacks.
    icon: "security"
    link: /enterprise/security/hardened-desktop/enhanced-container-isolation/
  - title: "Registry Access Management"
    description: Control the registries developers can access while using Docker Desktop.
    icon: "home_storage"
    link: /enterprise/security/hardened-desktop/registry-access-management/
  - title: "Image Access Management"
    description: Control the images developers can pull from Docker Hub.
    icon: "photo_library"
    link: /enterprise/security/hardened-desktop/image-access-management/
  - title: "Air-Gapped Containers"
    description: Restrict containers from accessing unwanted network resources.
    icon: "vpn_lock"
    link: /enterprise/security/hardened-desktop/air-gapped-containers/
weight: 60
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

Hardened Docker Desktop 提供了一系列安全功能，旨在加强开发人员环境的安全性，同时不影响生产力或开发人员体验。

使用 Hardened Docker Desktop，您可以强制执行严格的安全策略，防止开发人员和容器绕过组织控制。您还可以增强容器隔离，以抵御安全威胁，例如可能突破 Docker Desktop Linux 虚拟机或底层主机系统的恶意负载。

## 谁应该使用 Hardened Docker Desktop？

Hardened Docker Desktop 适用于注重安全的组织，这些组织：

- 不向开发人员的机器提供 root 或管理员访问权限
- 希望集中控制 Docker Desktop 配置
- 必须满足特定的合规要求

## Hardened Docker Desktop 的工作原理

Hardened Docker Desktop 的功能可以独立工作，也可以协同工作，形成纵深防御的安全策略。它们从多个层面保护开发人员工作站免受攻击，包括 Docker Desktop 配置、容器镜像管理和容器运行时安全：

- Registry Access Management 和 Image Access Management 防止访问未经授权的容器注册表和镜像类型，减少恶意负载的暴露
- Enhanced Container Isolation 在 Linux 用户命名空间内以非 root 权限运行容器，限制恶意容器的影响
- Air-gapped containers 允许您为容器配置网络限制，防止恶意容器访问组织的内部网络资源
- Settings Management 锁定 Docker Desktop 配置以强制执行公司策略，防止开发人员有意或无意地引入不安全设置

## 下一步

探索 Hardened Docker Desktop 功能，了解它们如何加强组织的安全态势：

{{< grid >}}