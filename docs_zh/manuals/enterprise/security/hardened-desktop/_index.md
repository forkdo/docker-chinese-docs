---
title: 强化版 Docker Desktop
linkTitle: 强化版 Docker Desktop
description: 在不影响生产力的前提下，帮助组织机构保护开发者环境的安全特性
keywords: security, hardened desktop, enhanced container isolation, registry access management, settings management, admins, docker desktop, image access management, air-gapped containers
tags:
- admin
aliases:
- /desktop/hardened-desktop/
- /security/for-admins/hardened-desktop/
grid:
- title: 设置管理
  description: 了解设置管理如何保护开发者的工作流程。
  icon: shield_locked
  link: /enterprise/security/hardened-desktop/settings-management/
- title: 增强型容器隔离
  description: 了解增强型容器隔离如何防范容器攻击。
  icon: security
  link: /enterprise/security/hardened-desktop/enhanced-container-isolation/
- title: 注册表访问管理
  description: 控制开发者在使用 Docker Desktop 时可以访问的注册表。
  icon: home_storage
  link: /enterprise/security/hardened-desktop/registry-access-management/
- title: 镜像访问管理
  description: 控制开发者可以从 Docker Hub 拉取的镜像。
  icon: photo_library
  link: /enterprise/security/hardened-desktop/image-access-management/
- title: 气隙容器
  description: 限制容器访问不需要的网络资源。
  icon: vpn_lock
  link: /enterprise/security/hardened-desktop/air-gapped-containers/
weight: 60
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

强化版 Docker Desktop 提供了一系列安全特性，旨在加强开发者环境的安全性，同时不影响生产力或开发者体验。

借助强化版 Docker Desktop，您可以强制执行严格的安全策略，防止开发者和容器绕过组织控制。您还可以增强容器隔离，以防范可能破坏 Docker Desktop Linux 虚拟机或底层主机系统的恶意载荷等安全威胁。

## 哪些人应该使用强化版 Docker Desktop？

强化版 Docker Desktop 非常适合注重安全性的组织机构，特别是那些：

- 不为开发者机器提供 root 或管理员权限
- 希望对 Docker Desktop 配置进行集中控制
- 必须满足特定合规性要求

## 强化版 Docker Desktop 的工作原理

强化版 Docker Desktop 的各项特性既可以独立工作，也可以协同工作，从而创建一种纵深防御的安全策略。它们保护开发者工作站免受多层面的攻击，包括 Docker Desktop 配置、容器镜像管理和容器运行时安全：

- 注册表访问管理和镜像访问管理可防止访问未经授权的容器注册表和镜像类型，从而减少暴露于恶意载荷的风险
- 增强型容器隔离在 Linux 用户命名空间中以非 root 权限运行容器，限制恶意容器的影响
- 气隙容器允许您为容器配置网络限制，防止恶意容器访问组织的内部网络资源
- 设置管理可以锁定 Docker Desktop 配置，以强制执行公司策略并防止开发者有意或无意地引入不安全的设置

## 后续步骤

探索强化版 Docker Desktop 的各项特性，了解它们如何加强组织的安全态势：

{{< grid >}}