---
title: 为您的 Docker 账户启用双因素认证
linkTitle: 双因素认证
description: 在您的 Docker 账户上启用或禁用双因素认证，以增强安全性和账户保护
keywords: two-factor authentication, 2FA, docker hub security, account security, TOTP, authenticator app, disable 2FA
weight: 20
aliases:
 - /docker-hub/2fa/
 - /security/2fa/disable-2fa/
 - /security/for-developers/2fa/
 - /security/for-developers/2fa/disable-2fa/
---

双因素认证 (2FA) 为您的 Docker 账户增加了一层重要的安全保护，它要求在登录时除了密码之外，还需要一个独特的安全码。即使您的密码被泄露，这也能防止未经授权的访问。

当您开启双因素认证时，Docker 会提供一个特定于您账户的独特恢复代码。请安全地存储此代码，因为它可以让您在无法访问认证器应用时恢复您的账户。

## 主要优势

双因素认证显著提高了您的账户安全性：

- **防范密码泄露**：即使您的密码被盗或泄露，攻击者没有您的第二因素也无法访问您的账户。
- **安全的 CLI 访问**：开启 2FA 后，Docker CLI 认证需要使用它，确保自动化工具使用个人访问令牌而不是密码。
- **合规要求**：许多组织要求使用 2FA 来访问开发和生产资源。
- **安心保障**：确保您的 Docker 仓库、镜像和账户设置受到行业标准安全实践的保护。

## 前提条件

在开启双因素认证之前，您需要：

- 一部安装了基于时间的一次性密码 (TOTP) 认证器应用的智能手机或设备
- 您的 Docker 账户密码的访问权限

## 启用双因素认证

要为您的 Docker 账户开启 2FA：

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 选择您的头像，然后从下拉菜单中选择 **Account settings**（账户设置）。
3. 选择 **2FA**。
4. 输入您的账户密码，然后选择 **Confirm**（确认）。
5. 保存您的恢复代码并将其存放在安全的地方。如果您无法访问您的认证器应用，可以使用此恢复代码来恢复您的账户。
6. 使用 TOTP 移动应用扫描二维码或输入文本代码。
7. 将您的认证器应用链接后，在文本框中输入六位数代码。
8. 选择 **Enable 2FA**（启用 2FA）。

双因素认证现已在您的账户上激活。每次登录时，您都需要输入来自认证器应用的安全码。

## 禁用双因素认证

> [!WARNING]
>
> 禁用双因素认证会降低您的 Docker 账户的安全性。

1. 登录您的 [Docker 账户](https://app.docker.com/login)。
2. 选择您的头像，然后从下拉菜单中选择 **Account settings**（账户设置）。
3. 选择 **2FA**。
4. 输入您的密码，然后选择 **Confirm**（确认）。
5. 选择 **Disable 2FA**（禁用 2FA）。