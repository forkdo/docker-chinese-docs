---
title: PKG 安装程序
description: 了解如何使用 PKG 安装程序。同时探索其他配置选项。
keywords: pkg, mac, docker desktop, install, deploy, configure, admin, mdm
tags:
- admin
weight: 20
aliases:
- /desktop/setup/install/enterprise-deployment/pkg-install-and-configure/
---

{{< summary-bar feature_name="PKG installer" >}}

PKG 安装包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，无需每个用户手动设置。借助此安装包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，从而提高整个组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 下载后，双击 `Docker.pkg` 运行安装程序。
5. 按照安装向导的说明授权安装程序并继续安装。
   - **简介**：选择 **Continue**。
   - **许可**：查看许可协议并选择 **Agree**。
   - **选择目标**：此步骤可选。建议保留默认安装目标（通常为 `Macintosh HD`）。选择 **Continue**。
   - **安装类型**：选择 **Install**。
   - **安装**：使用您的管理员密码或 Touch ID 进行身份验证。
   - **摘要**：安装完成后，选择 **Close**。

> [!NOTE]
>
> 使用 PKG 安装 Docker Desktop 时，应用内更新会自动禁用。这可以确保组织保持版本一致性，并防止未经批准的更新。对于使用 `.dmg` 安装程序安装的 Docker Desktop，仍支持应用内更新。
>
> 当有可用更新时，Docker Desktop 会通知您。要更新 Docker Desktop，请从 Docker Admin Console 下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本，请查看[发行说明](/manuals/desktop/release-notes.md)页面。

## 从命令行安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 在终端中，运行以下命令：

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## 其他资源

- 了解如何使用 [Intune](use-intune.md) 或 [Jamf Pro](use-jamf-pro.md) 部署适用于 Mac 的 Docker Desktop
- 探索如何为您的用户[强制登录](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)。