---
description: 了解设置管理的工作原理、适用对象及其提供的优势
keywords: 设置管理, rootless, docker desktop, 硬化桌面, 管理员控制, 企业
tags: [admin]
title: 设置管理
linkTitle: 设置管理
aliases:
 - /desktop/hardened-desktop/settings-management/
 - /security/for-admins/hardened-desktop/settings-management/
weight: 10
---

{{< summary-bar feature_name="Hardened Docker Desktop" >}}

设置管理允许管理员在最终用户机器上配置和强制执行 Docker Desktop 设置。它有助于在组织内保持一致的配置并增强安全性。

## 谁应该使用设置管理？

设置管理专为以下组织设计：

- 需要对 Docker Desktop 配置进行集中控制
- 希望在团队中标准化 Docker Desktop 环境
- 在受监管环境中运营，必须强制执行合规策略

## 设置管理的工作原理

管理员可以使用以下方法之一定义设置：

- [管理控制台](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md)：通过 Docker 管理控制台创建和分配设置策略。这提供了基于 Web 的界面来管理整个组织的设置。
- [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)：在用户机器上放置配置文件以强制执行设置。此方法适用于自动化部署和脚本安装。

强制执行的设置会覆盖用户定义的配置，并且开发者无法修改。

## 可配置设置

设置管理支持 Docker Desktop 的广泛功能，包括：

- 代理配置
- 网络设置
- 容器隔离选项
- 注册表访问控制
- 资源限制
- 安全策略
- 云策略

有关可强制执行设置的完整列表，请参阅 [设置参考](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md)。

## 策略优先级

当存在多个策略时，Docker Desktop 按以下顺序应用它们：

1. 用户特定策略：最高优先级
1. 组织默认策略：在没有用户特定策略时应用
1. 本地 `admin-settings.json` 文件：最低优先级，会被管理控制台策略覆盖
1. [配置文件](/manuals/enterprise/security/enforce-sign-in/methods.md#configuration-profiles-method-mac-only)：Docker 管理控制台策略的超集。需要 Docker Desktop 版本 4.48 或更高版本。

## 设置设置管理

1. 确认您已 [添加并验证](/manuals/enterprise/security/domain-management.md#add-and-verify-a-domain) 组织的域名。
2. [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md) 以确保所有开发者使用组织凭据进行身份验证。
3. 选择配置方法：
    - 在 [macOS](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 或 [Windows](/manuals/desktop/setup/install/windows-install.md#install-from-the-command-line) 上使用 `--admin-settings` 安装程序标志自动创建 `admin-settings.json`。
    - 手动创建和配置 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md)。
    - 在 [Docker 管理控制台](configure-admin-console.md) 中创建设置策略。

配置后，开发者在以下情况下接收强制执行的设置：

- 退出并重新启动 Docker Desktop，然后登录
- 首次启动并登录 Docker Desktop

> [!NOTE]
>
> Docker Desktop 在设置更改后不会自动提示用户重启或重新身份验证。您可能需要向开发者传达这些要求。

## 开发者体验

当设置被强制执行时：

- Docker Desktop 中的设置选项在界面中显示为灰色，无法通过仪表板、CLI 或配置文件修改
- 如果启用了增强容器隔离，开发者无法在 Docker Desktop Linux VM 内使用特权容器或类似方法更改强制执行的设置

这确保了环境的一致性，同时为管理员管理的设置提供了清晰的视觉指示。

## 查看已应用的设置

当管理员应用设置管理策略时，Docker Desktop 在 GUI 中将大多数强制执行的设置显示为灰色。

Docker Desktop GUI 当前不显示所有集中式设置，特别是管理员通过管理控制台应用的增强容器隔离 (ECI) 设置。

作为变通方案，您可以检查 `settings-store.json` 文件以查看所有已应用的设置：

  - Mac: `~/Library/Application Support/Docker/settings-store.json`
  - Windows: `%APPDATA%\Docker\settings-store.json`
  - Linux: `~/.docker/desktop/settings-store.json`

`settings-store.json` 文件包含所有设置，包括可能不出现在 Docker Desktop GUI 中的设置。

## 限制

设置管理有以下限制：

- 不适用于气隙或离线环境
- 与限制与 Docker Hub 进行身份验证的环境不兼容

## 下一步

开始使用设置管理：

- [使用 `admin-settings.json` 文件配置设置管理](configure-json-file.md)
- [使用 Docker 管理控制台配置设置管理](configure-admin-console.md)