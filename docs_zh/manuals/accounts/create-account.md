---
title: 创建 Docker 账户
linkTitle: 创建账户
weight: 10
description: 了解如何注册 Docker ID 并登录您的账户
keywords: 账户, docker ID, 账单, 付费计划, 支持, Hub, Store, 论坛, 知识库, beta 访问, 邮箱, 激活, 验证
aliases:
- /docker-hub/accounts/
- /docker-id/
---

您可以通过邮箱地址或使用 Google 或 GitHub 账户注册一个免费的 Docker 账户。创建唯一的 Docker ID 后，您可以访问所有 Docker 产品，包括 Docker Hub、Docker Desktop 和 Docker Scout。

您的 Docker ID 将成为托管 Docker 服务的用户名，以及
[Docker 论坛](https://forums.docker.com/)的用户名。

> [!TIP]
>
> 探索 [Docker 的订阅服务](https://www.docker.com/pricing/)，了解 Docker 还能为您提供哪些功能。

## 创建账户

您可以使用邮箱注册，或使用 Google 或 GitHub 账户注册。

### 使用邮箱注册

1. 访问 [Docker 注册页面](https://app.docker.com/signup/)。
1. 输入一个唯一且有效的邮箱地址。
1. 输入用作 Docker ID 的用户名。一旦创建了 Docker ID，如果您停用此账户，将来将无法再次使用该用户名。

    您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母

1. 输入至少 9 个字符的密码。
1. 选择 **注册**。
1. 打开您的邮箱客户端。Docker 会向您提供的地址发送一封验证邮件。
1. 验证您的邮箱地址以完成注册流程。

> [!NOTE]
>
> 在获得 Docker 完整功能的访问权限之前，您必须验证邮箱地址。

### 使用 Google 或 GitHub 注册

> [!IMPORTANT]
>
> 要使用社交账户注册，您必须先在您的社交账户提供商处验证邮箱地址，然后才能开始。

1. 访问 [Docker 注册页面](https://app.docker.com/signup/)。
1. 选择您的社交账户提供商，Google 或 GitHub。
1. 选择您要链接到 Docker 账户的社交账户。
1. 选择 **授权 Docker** 以允许 Docker 访问您的社交账户信息。您将被重定向到注册页面。
1. 输入用作 Docker ID 的用户名。

    您的用户名：
    - 长度必须在 4 到 30 个字符之间
    - 只能包含数字和小写字母
1. 选择 **注册**。

## 登录您的账户

您可以使用邮箱、Google 或 GitHub 账户，或从 Docker CLI 登录。

### 使用邮箱或 Docker ID 登录

1. 访问 [Docker 登录页面](https://login.docker.com)。
1. 输入您的邮箱地址或 Docker ID，然后选择 **继续**。
1. 输入您的密码，然后选择 **继续**。

要重置密码，请参阅 [重置您的密码](#reset-your-password)。

### 使用 Google 或 GitHub 登录

> [!IMPORTANT]
>
> 您的 Google 或 GitHub 账户必须有已验证的邮箱地址。

您可以使用 Google 或 GitHub 凭据登录。如果您的社交账户使用与现有 Docker ID 相同的邮箱地址，则账户会自动关联。

如果不存在 Docker ID，Docker 会为您创建一个新账户。

Docker 目前不支持将多种登录方式链接到同一个 Docker ID。

### 使用 CLI 登录

使用 `docker login` 命令从命令行进行身份验证。详细信息请参阅 [`docker login`](/reference/cli/docker/login/)。

> [!WARNING]
>
> `docker login` 命令将凭据存储在您主目录下的 `.docker/config.json` 中。密码是 base64 编码的。
>
> 为了提高安全性，请使用
> [Docker 凭据助手](https://github.com/docker/docker-credential-helpers)。
> 为了获得更强的保护，请使用 [个人访问令牌](../security/access-tokens.md) 代替密码。这在 CI/CD 环境中或当凭据助手不可用时特别有用。

## 重置您的密码

要重置您的密码：

1. 访问 [Docker 登录页面](https://login.docker.com/)。
1. 输入您的邮箱地址。
1. 当提示输入密码时，选择 **忘记密码?**。

## 故障排除

如果您有付费的 Docker 订阅，
[联系支持团队](https://hub.docker.com/support/contact/) 以获得帮助。

所有 Docker 用户都可以通过以下资源寻求故障排除信息和支持，Docker 或社区将以尽力而为的方式响应：
   - [Docker 社区论坛](https://forums.docker.com/)
   - [Docker 社区 Slack](http://dockr.ly/comm-slack)