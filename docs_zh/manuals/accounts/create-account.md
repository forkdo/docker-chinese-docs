---
title: 创建 Docker 账户
linkTitle: 创建账户
weight: 10
description: 了解如何注册 Docker ID 并登录到您的账户
keywords: accounts, docker ID, billing, paid plans, support, Hub, Store, Forums, knowledge
  base, beta access, email, activation, verification
aliases:
- /docker-hub/accounts/
- /docker-id/
---

您可以使用电子邮箱地址注册免费的 Docker 账户，也可以通过 Google 或 GitHub 账户注册。创建唯一的 Docker ID 后，您就可以访问所有 Docker 产品，包括 Docker Hub、Docker Desktop 和 Docker Scout。

您的 Docker ID 将成为您在托管 Docker 服务以及 [Docker 论坛](https://forums.docker.com/) 中的用户名。

> [!TIP]
>
> 浏览 [Docker 订阅计划](https://www.docker.com/pricing/) 以了解 Docker 还能为您提供哪些服务。

## 创建账户

使用电子邮箱地址、Google 或 GitHub 账户注册需要额外的验证才能完成账户创建：

- 如果使用 Google 或 GitHub 注册，您必须首先通过该提供商验证您的电子邮箱地址。
- 如果使用电子邮箱地址注册，Docker 会发送一封验证邮件。请按照邮件中的说明验证您的账户并完成注册流程。

在您验证账户之前，Docker 会阻止登录。

### 使用电子邮箱注册

1. 访问 [Docker 注册页面](https://app.docker.com/signup/) 并输入一个唯一的有效电子邮箱地址。
1. 输入一个用作 Docker ID 的用户名。一旦创建了 Docker ID，如果您停用此账户，将来就不能再重复使用该 ID。您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母
1. 选择一个至少 9 个字符长的密码，然后点击 **Sign Up**（注册）。
1. 收到 Docker 验证邮件后，验证您的电子邮箱地址。这样就完成了注册流程。

### 使用 Google 或 GitHub 注册

1. 访问 [Docker 注册页面](https://app.docker.com/signup/)。
1. 选择您的社交账户提供商，Google 或 GitHub。
1. 选择您要链接到 Docker 账户的社交账户。
1. 点击 **Authorize Docker**（授权 Docker）以允许 Docker 访问您的社交账户信息。您将被重定向到注册页面。
1. 输入一个用作 Docker ID 的用户名。您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母
1. 点击 **Sign up**（注册）。

## 登录到您的账户

您可以使用电子邮箱、Google 或 GitHub 账户登录，也可以从 Docker CLI 登录。

### 使用电子邮箱或 Docker ID 登录

1. 访问 [Docker 登录页面](https://login.docker.com)。
1. 输入您的电子邮箱地址或 Docker ID，然后点击 **Continue**（继续）。
1. 输入您的密码，然后点击 **Continue**（继续）。

要重置密码，请参阅 [重置密码](#reset-your-password)。

### 使用 Google 或 GitHub 登录

您可以使用 Google 或 GitHub 凭据登录。如果您的社交账户使用的电子邮箱地址与现有的 Docker ID 相同，这些账户会自动关联。

如果不存在 Docker ID，Docker 会为您创建一个新账户。

Docker 目前不支持将多个登录方式关联到同一个 Docker ID。

### 使用 CLI 登录

使用 `docker login` 命令从命令行进行身份验证。有关详细信息，请参阅 [`docker login`](/reference/cli/docker/login/)。

> [!WARNING]
>
> `docker login` 命令会将凭据存储在您的主目录下的 `.docker/config.json` 文件中。密码会以 base64 编码形式存储。
>
> 为了提高安全性，请使用 [Docker 凭据助手](https://github.com/docker/docker-credential-helpers)。为了获得更强的保护，请使用 [个人访问令牌](../security/access-tokens.md) 而不是密码。这在 CI/CD 环境或无法使用凭据助手时特别有用。

## 重置密码

要重置密码：

1. 访问 [Docker 登录页面](https://login.docker.com/)。
1. 输入您的电子邮箱地址。
1. 当提示输入密码时，点击 **Forgot password?**（忘记密码？）。

## 故障排除

如果您拥有付费的 Docker 订阅，请[联系支持团队](https://hub.docker.com/support/contact/) 获取帮助。

所有 Docker 用户都可以通过以下资源寻求故障排除信息和支持，Docker 或社区会尽力提供响应：
   - [Docker 社区论坛](https://forums.docker.com/)
   - [Docker 社区 Slack](http://dockr.ly/comm-slack)