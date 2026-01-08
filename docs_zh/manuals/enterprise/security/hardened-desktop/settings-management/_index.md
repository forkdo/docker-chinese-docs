---
description: 了解 Settings Management 的工作原理、适用对象及其带来的优势
keywords: Settings Management, rootless, docker desktop, hardened desktop, admin control, enterprise
tags:
- admin
title: Settings Management
linkTitle: Settings Management
aliases:
- /desktop/hardened-desktop/settings-management/
- /security/for-admins/hardened-desktop/settings-management/
weight: 10
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

Settings Management 让管理员能够配置并强制执行 Docker Desktop 设置，在终端用户机器上统一实施。它有助于保持配置一致，并增强组织内的安全性。

## 谁应该使用 Settings Management？

Settings Management 专为以下组织设计：

- 需要集中控制 Docker Desktop 配置
- 希望在团队间标准化 Docker Desktop 环境
- 在受监管环境中运营，必须强制执行合规策略

## Settings Management 的工作原理

管理员可以使用以下方法之一定义设置：

- [Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)：通过 Docker Admin Console 创建并分配设置策略。这提供了一个基于 Web 的界面，用于管理整个组织的设置。
- [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)：在用户机器上放置配置文件以强制执行设置。此方法适用于自动部署和脚本化安装。

强制执行的设置会覆盖用户定义的配置，且开发者无法修改。

## 可配置的设置

Settings Management 支持广泛的 Docker Desktop 功能，包括：

- 代理配置
- 网络设置
- 容器隔离选项
- 注册表访问控制
- 资源限制
- 安全策略
- 云策略

有关可强制执行的完整设置列表，请参阅[设置参考](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md)。

## 策略优先级

当存在多个策略时，Docker Desktop 按以下顺序应用它们：

1. 用户特定策略：最高优先级
2. 组织默认策略：当不存在用户特定策略时应用
3. 本地 `admin-settings.json` 文件：最低优先级，会被 Admin Console 策略覆盖
4. [配置描述文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only)：Docker Admin Console 策略的超集。适用于 Docker Desktop 4.48 及更高版本。

## 设置 Settings Management

1. 确认您已[添加并验证](/manuals/enterprise/security/domain-management.md#add-and-verify-a-domain)组织的域名。
2. [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)以确保所有开发者都使用您的组织进行身份验证。
3. 选择一种配置方法：
    - 在 [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 或 [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 上使用 `--admin-settings` 安装程序标志自动创建 `admin-settings.json`。
    - 手动创建并配置 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)。
    - 在 [Docker Admin Console](configure-admin-console.md) 中创建设置策略。

配置完成后，开发者在以下情况下会收到强制执行的设置：

- 退出并重新启动 Docker Desktop，然后登录
- 首次启动并登录 Docker Desktop

> [!NOTE]
>
> Docker Desktop 不会在设置更改后自动提示用户重新启动或重新进行身份验证。您可能需要将这些要求告知您的开发者。

## 开发者体验

当设置被强制执行时：

- 设置选项在 Docker Desktop 中显示为灰色，无法通过 Dashboard、CLI 或配置文件修改
- 如果启用了增强容器隔离 (Enhanced Container Isolation)，开发者无法使用特权容器或类似方法在 Docker Desktop Linux VM 内更改强制执行的设置

这确保了环境的一致性，同时清晰地显示哪些设置由管理员管理。

## 查看已应用的设置

当管理员应用 Settings Management 策略时，Docker Desktop 会在 GUI 中将大多数强制执行的设置显示为灰色。

Docker Desktop GUI 目前不会显示所有集中设置，特别是管理员通过 Admin Console 应用的增强容器隔离 (ECI) 设置。

作为解决方法，您可以检查 `settings-store.json` 文件以查看所有已应用的设置：

  - Mac：`~/Library/Application Support/Docker/settings-store.json`
  - Windows：`%APPDATA%\Docker\settings-store.json`
  - Linux：`~/.docker/desktop/settings-store.json`

`settings-store.json` 文件包含所有设置，包括那些可能未出现在 Docker Desktop GUI 中的设置。

## 限制

Settings Management 具有以下限制：

- 在隔离网络或离线环境中无效
- 与限制使用 Docker Hub 进行身份验证的环境不兼容

## 下一步

开始使用 Settings Management：

- [使用 `admin-settings.json` 文件配置 Settings Management](configure-json-file.md)
- [使用 Docker Admin Console 配置 Settings Management](configure-admin-console.md)