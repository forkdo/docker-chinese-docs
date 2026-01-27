# Docker Home、管理控制台、计费、安全和订阅功能的版本说明


此页面详细介绍了 Docker Home、管理控制台、计费、安全和订阅功能的新增功能、增强功能、已知问题和错误修复。

## 2026-01-27

### 新增功能

- 管理员现在可以使用[镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md)的允许列表来批准绕过镜像访问控制的特定仓库。

## 2025-01-30

### 新增功能

- 通过 PKG 安装程序安装 Docker Desktop 现已全面可用。
- 通过配置文件强制执行登录现已全面可用。

## 2024-12-10

### 新增功能

- 新的 Docker 订阅现已推出。更多信息请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/) 以及[宣布升级 Docker 计划：更简单、更多价值、更好的开发和生产力](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 2024-11-18

### 新增功能

- 管理员现在可以：
  - 使用[配置文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only)强制执行登录（早期访问）。
  - 一次为多个组织强制执行登录（早期访问）。
  - 使用 [PKG 安装程序](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)批量部署 Mac 版 Docker Desktop（早期访问）。
  - [通过 Docker 管理控制台使用桌面设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)（早期访问）。

### 错误修复和增强功能

- 增强容器隔离 (ECI) 已改进为：
  - 允许管理员[关闭 Docker 套接字挂载限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#allowing-all-containers-to-mount-the-docker-socket)。
  - 在使用 [`allowedDerivedImages` 设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#docker-socket-mount-permissions-for-derived-images)时支持通配符标签。

## 2024-11-11

### 新增功能

- [个人访问令牌](/security/access-tokens/) (PAT) 现在支持设置过期日期。

## 2024-10-15

### 新增功能

- 测试版：您现在可以创建[组织访问令牌](/security/for-admins/access-tokens/) (OAT)，以增强组织的安全性并简化 Docker 管理控制台中组织的访问管理。

## 2024-08-29

### 新增功能

- 通过 [MSI 安装程序](/manuals/enterprise/enterprise-deployment/msi-install-and-configure.md)部署 Docker Desktop 现已全面可用。
- 两种新的[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)方法（Windows 注册表项和 `.plist` 文件）现已全面可用。

## 2024-08-24

### 新增功能

- 管理员现在可以查看[组织洞察](/manuals/admin/organization/insights.md)。

## 2024-07-17

### 新增功能

- 您现在可以在 [Docker Home](https://app.docker.com) 中集中访问和管理 Docker 产品。
