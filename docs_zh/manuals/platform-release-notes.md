---
title: Docker Home、管理控制台、账单、安全和订阅功能的发布说明
linkTitle: 发布说明
description: 了解 Docker Home、管理控制台以及账单和订阅功能的新功能、错误修复和重大变更
keywords: Docker Home, Docker Admin Console, billing, subscription, security, admin, releases, what's new
weight: 60
params:
  sidebar:
    group: Platform
tags:
- Release notes
- admin
---

此页面详细介绍了 Docker Home、管理控制台、账单、安全和订阅功能的新特性、增强功能、已知问题和错误修复。

## 2025-01-30

### 新增功能

- 现已全面支持通过 PKG 安装程序安装 Docker Desktop。
- 现已全面支持通过配置配置文件强制执行登录。

## 2024-12-10

### 新增功能

- 现已提供新的 Docker 订阅。更多信息，请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/) 和 [宣布升级的 Docker 计划：更简单、更高价值、更佳的开发和生产力](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 2024-11-18

### 新增功能

- 管理员现在可以：
  - 使用 [配置配置文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only) 强制执行登录（早期访问）。
  - 同时为多个组织强制执行登录（早期访问）。
  - 使用 [PKG 安装程序](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md) 批量部署 Docker Desktop for Mac（早期访问）。
  - [通过 Docker 管理控制台使用 Desktop 设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)（早期访问）。

### 错误修复和增强功能

- 增强型容器隔离 (ECI) 已得到改进：
  - 允许管理员 [关闭 Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#allowing-all-containers-to-mount-the-docker-socket)。
  - 在使用 [`allowedDerivedImages` 设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images) 时支持通配符标签。

## 2024-11-11

### 新增功能

- [个人访问令牌](/security/access-tokens/) (PATs) 现在支持过期日期。

## 2024-10-15

### 新增功能

- Beta 版：您现在可以创建 [组织访问令牌](/security/for-admins/access-tokens/) (OATs)，以增强组织的安全性并简化 Docker 管理控制台中组织的访问管理。

## 2024-08-29

### 新增功能

- 通过 [MSI 安装程序](/manuals/enterprise/enterprise-deployment/msi-install-and-configure.md) 部署 Docker Desktop 现已全面支持。
- 两种新的 [强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 方法（Windows 注册表项和 `.plist` 文件）现已全面支持。

## 2024-08-24

### 新增功能

- 管理员现在可以查看 [组织洞察](/manuals/admin/organization/insights.md)。

## 2024-07-17

### 新增功能

- 您现在可以在 [Docker Home](https://app.docker.com) 中集中访问和管理 Docker 产品。