---
title: 管理 Docker 账户
linkTitle: 管理账户
weight: 20
description: 了解如何管理您的 Docker 账户。
keywords: 账户, docker ID, 账户设置, 账户管理, docker home
---

您可以使用 Docker Home 集中管理您的 Docker 账户，包括管理设置和安全设置。

> [!TIP]
>
> 如果您的账户关联了启用了单点登录 (SSO) 的组织，您可能没有权限更新账户设置。
> 您必须联系管理员来更新您的设置。

## 更新账户信息

账户信息在您的 **账户设置** 页面中可见。您可以更新以下账户信息：

- 全名
- 公司
- 地址
- 网站
- Gravatar 邮箱

要使用 Gravatar 添加或更新您的头像：

1. 创建一个 [Gravatar 账户](https://gravatar.com/)。
1. 创建您的头像。
1. 在您的 Docker 账户设置中添加您的 Gravatar 邮箱。

在 Docker 中更新您的头像可能需要一些时间。

## 更新邮箱地址

要更新您的邮箱地址：

1. 登录到您的 [Docker 账户](https://app.docker.com/login)。
1. 选择右上角的头像，然后选择 **账户设置**。
1. 选择 **邮箱**。
1. 输入您的新邮箱地址和密码以确认更改。
1. 选择 **发送验证邮件**。Docker 会向您的新邮箱发送验证链接。

在您完成验证流程之前，您的新邮箱地址将显示为未验证状态。您可以：

- 如需要，重新发送验证邮件。
- 在验证之前随时删除未验证的邮箱地址。

要验证您的邮箱，请打开您的邮箱客户端并按照 Docker 验证邮件中的说明操作。

> [!NOTE]
>
> Docker 账户一次只支持一个已验证的邮箱地址，该邮箱地址用于账户通知和安全相关的通信。您不能向账户添加多个已验证的邮箱地址。

## 更改密码

您可以通过电子邮件发起密码重置来更改密码。要更改密码：

1. 登录到您的 [Docker 账户](https://app.docker.com/login)。
1. 选择右上角的头像，然后选择 **账户设置**。
1. 选择 **密码**，然后选择 **重置密码**。
1. Docker 将向您发送一封包含重置密码说明的密码重置邮件。

## 管理双因素认证

要更新您的双因素认证 (2FA) 设置：

1. 登录到您的 [Docker 账户](https://app.docker.com/login)。
1. 选择右上角的头像，然后选择 **账户设置**。
1. 选择 **2FA**。

更多信息，请参见
[启用双因素认证](../security/2fa/_index.md)。

## 管理个人访问令牌

要管理个人访问令牌：

1. 登录到您的 [Docker 账户](https://app.docker.com/login)。
1. 选择右上角的头像，然后选择 **账户设置**。
1. 选择 **个人访问令牌**。

更多信息，请参见
[创建和管理访问令牌](../security/access-tokens.md)。

## 管理已连接的账户

您可以取消关联已连接的 Google 或 GitHub 账户：

1. 登录到您的 [Docker 账户](https://app.docker.com/login)。
1. 选择右上角的头像，然后选择 **账户设置**。
1. 选择 **已连接的账户**。
1. 选择您已连接账户的 **断开连接**。

要完全取消关联您的 Docker 账户，您还必须从 Google 或 GitHub 中取消 Docker 的关联。更多信息请参见 Google 或 GitHub 的文档：

- [管理您的 Google 账户与第三方之间的连接](https://support.google.com/accounts/answer/13533235?hl=en)
- [查看和撤销 GitHub Apps 的授权](https://docs.github.com/en/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## 转换您的账户

有关将您的账户转换为组织的信息，请参见
[将账户转换为组织](../admin/organization/convert-account.md)。

## 停用您的账户

有关停用您的账户的信息，请参见
[停用用户账户](./deactivate-user-account.md)。