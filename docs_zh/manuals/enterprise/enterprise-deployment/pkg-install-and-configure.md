---
title: PKG 安装程序
description: 了解如何使用 PKG 安装程序。同时探索其他配置选项。
keywords: pkg, mac, docker desktop, install, deploy, configure, admin, mdm
tags: [admin]
weight: 20
aliases:
 - /desktop/setup/install/enterprise-deployment/pkg-install-and-configure/
---

{{< summary-bar feature_name="PKG installer" >}}

PKG 安装包支持多种 MDM（移动设备管理）解决方案，非常适合批量安装，可避免用户手动设置。通过此安装包，IT 管理员可以确保 Docker Desktop 的安装标准化并符合策略驱动，从而提高组织内的效率和软件管理能力。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 从 **macOS** 选项卡中，点击 **Download PKG installer** 按钮。
4. 下载完成后，双击 `Docker.pkg` 运行安装程序。
5. 按照安装向导的说明授权安装程序并继续安装。
   - **Introduction**：点击 **Continue**。
   - **License**：查看许可协议并点击 **Agree**。
   - **Destination Select**：此步骤为可选。建议保留默认安装目标（通常为 `Macintosh HD`）。点击 **Continue**。
   - **Installation Type**：点击 **Install**。
   - **Installation**：使用管理员密码或 Touch ID 进行身份验证。
   - **Summary**：安装完成后，点击 **Close**。

> [!NOTE]
>
> 使用 PKG 安装 Docker Desktop 时，应用内更新会自动禁用。这确保了组织可以保持版本一致性，并防止未经批准的更新。对于使用 `.dmg` 安装程序安装的 Docker Desktop，仍然支持应用内更新。
>
> Docker Desktop 会在有可用更新时通知您。要更新 Docker Desktop，请从 Docker 管理控制台下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要及时了解新版本发布信息，请查看 [发布说明](/manuals/desktop/release-notes.md) 页面。

## 从命令行安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 从 **macOS** 选项卡中，点击 **Download PKG installer** 按钮。
4. 在终端中运行以下命令：

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## 额外资源

- 查看如何使用 [Intune](use-intune.md) 或 [Jamf Pro](use-jamf-pro.md) 为 Mac 部署 Docker Desktop
- 探索如何为您的用户 [Enforce sign-in](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)