---
title: Ask Gordon
description: 使用 Docker 桌面版和 CLI 中的 AI 助手简化您的工作流程。
weight: 40
params:
  sidebar:
    badge:
      color: blue
      text: Beta
    group: AI
aliases:
 - /desktop/features/gordon/
---

{{< summary-bar feature_name="Ask Gordon" >}}

Ask Gordon 是嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，帮助您充分利用 Docker 生态系统。

## 主要功能

Ask Gordon 提供基于 AI 的 Docker 工具辅助，能够：

- 优化 Dockerfile
- 运行和排查容器问题
- 与您的镜像和代码交互
- 查找漏洞或配置问题
- 将 Dockerfile 迁移至使用 [Docker Hardened Images](/manuals/dhi/_index.md)

它理解您的本地环境，包括源代码、Dockerfile 和镜像，从而提供个性化且可操作的指导。

Ask Gordon 会记住对话，让您更轻松地切换话题。

Ask Gordon 默认未启用，且不适用于生产环境。您可能还会遇到术语 "Docker AI" 作为这项技术的更广泛引用。

> [!NOTE]
>
> Ask Gordon 由大语言模型 (LLM) 驱动。与其他所有基于 LLM 的工具一样，其响应有时可能不准确。请始终验证所提供的信息。

### Gordon 访问哪些数据？

当您使用 Ask Gordon 时，它访问的数据取决于您的查询：

- 本地文件：如果您使用 `docker ai` 命令，Ask Gordon 可以访问执行命令的当前工作目录中的文件和目录。在 Docker Desktop 中，如果您在 **Ask Gordon** 视图中询问特定文件或目录，系统会提示您选择相关上下文。
- 本地镜像：Gordon 与 Docker Desktop 集成，可以查看本地镜像存储中的所有镜像。这包括您构建或从注册表拉取的镜像。

为了提供准确的响应，Ask Gordon 可能会将相关文件、目录或镜像元数据与您的查询一起发送到 Gordon 后端。此数据传输通过网络进行，但不会被持久存储或与第三方共享。它仅用于处理您的请求并形成响应。有关 Docker AI 隐私条款和条件的详细信息，请查看 [Gordon's Supplemental Terms](https://www.docker.com/legal/docker-ai-supplemental-terms/)。

所有传输的数据均经过加密。

### 数据收集和使用方式

Docker 从您与 Ask Gordon 的交互中收集匿名数据以改进服务。这包括：

- 您的查询：您向 Gordon 提出的问题。
- 响应：Gordon 提供的答案。
- 反馈：点赞和点踩评分。

为确保隐私和安全：

- 数据经过匿名化处理，无法追溯到您或您的账户。
- Docker 不使用此数据训练 AI 模型或与第三方共享。

通过使用 Ask Gordon，您帮助提高了 Docker AI 对所有人的可靠性和准确性。

如果您对数据收集或使用有任何疑虑，可以随时[禁用](#disable-ask-gordon)该功能。

## 启用 Ask Gordon

1. 登录您的 Docker 账户。
1. 转到设置中的 **Beta features** 标签页。
1. 勾选 **Enable Docker AI** 复选框。

   Docker AI 服务条款协议将出现。您必须同意条款才能启用该功能。查看条款后，选择 **Accept and enable** 继续。

1. 选择 **Apply**。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，此设置位于 **Features in development** 页面的 **Experimental features** 标签页下。

## 使用 Ask Gordon

您可以通过以下方式访问 Gordon：

- 在 Docker Desktop 的 **Ask Gordon** 视图中。
- 在 Docker CLI 中使用 `docker ai` 命令。

启用 Docker AI 功能后，您还会在 Docker Desktop 的其他位置看到 **Ask Gordon**。每当您看到带有 **Sparkles** (✨) 图标的按钮时，就可以使用它从 Ask Gordon 获得上下文支持。

## 示例工作流程

Ask Gordon 是 Docker 任务和工作流程的通用 AI 助手。以下是一些您可以尝试的操作：

- [排查崩溃的容器](#troubleshoot-a-crashed-container)
- [获取运行容器的帮助](#get-help-with-running-a-container)
- [优化 Dockerfile](#improve-a-dockerfile)
- [将 Dockerfile 迁移至 DHI](#migrate-a-dockerfile-to-dhi)

更多示例，请直接询问 Gordon。例如：

```console
$ docker ai "What can you do?"
```

### 排查崩溃的容器

如果您使用无效配置或命令启动容器，可以使用 Ask Gordon 排查错误。例如，尝试在没有数据库密码的情况下启动 Postgres 容器：

```console
$ docker run postgres
Error: Database is uninitialized and superuser password is not specified.
       You must specify POSTGRES_PASSWORD to a non-empty value for the
       superuser. For example, "-e POSTGRES_PASSWORD=password" on "docker run".

       You may also use "POSTGRES_HOST_AUTH_METHOD=trust" to allow all
       connections without a password. This is *not* recommended.

       See PostgreSQL documentation about "trust":
       https://www.postgresql.org/docs/current/auth-trust.html
```

在 Docker Desktop 的 **Containers** 视图中，选择容器名称旁的 ✨ 图标，或检查容器并打开 **Ask Gordon** 标签页。

### 获取运行容器的帮助

如果您想运行特定镜像但不确定如何操作，Gordon 可以帮助您设置：

1. 从 Docker Hub 拉取镜像（例如，`postgres`）。
1. 在 Docker Desktop 中打开 **Images** 视图并选择镜像。
1. 选择 **Run** 按钮。

在 **Run a new container** 对话框中，您会看到关于 **Ask Gordon** 的消息。

![Screenshot showing Ask Gordon hint in Docker Desktop.](../../images/gordon-run-ctr.png)

提示中的链接文本是与 Ask Gordon 开始对话的建议提示。

### 优化 Dockerfile

Gordon 可以分析您的 Dockerfile 并提出改进建议。要使用 `docker ai` 命令让 Gordon 评估您的 Dockerfile：

1. 转到您的项目目录：

   ```console
   $ cd <path-to-your-project>
   ```

1. 使用 `docker ai` 命令评估您的 Dockerfile：

   ```console
   $ docker ai rate my Dockerfile
   ```

Gordon 将分析您的 Dockerfile，并在多个维度上识别改进机会：

- 构建缓存优化
- 安全性
- 镜像大小效率
- 最佳实践合规性
- 可维护性
- 可重现性
- 可移植性
- 资源效率

### 将 Dockerfile 迁移至 DHI

将 Dockerfile 迁移至使用 [Docker Hardened Images](/manuals/dhi/_index.md) 有助于您构建更安全、更精简且适合生产的容器。DHIs 减少漏洞，强制执行最佳实践，并简化合规性，使其成为安全软件供应链的坚实基础。

要请求 Gordon 帮助迁移：

{{% include "gordondhi.md" %}}

## 禁用 Ask Gordon

### 对个人用户

如果您已启用 Ask Gordon 并希望再次禁用它：

1. 在 Docker Desktop 中打开 **Settings** 视图。
1. 转到 **Beta features**。
1. 取消勾选 **Enable Docker AI** 复选框。
1. 选择 **Apply**。

### 对组织

要为整个 Docker 组织禁用 Ask Gordon，请使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 并在 `admin-settings.json` 文件中添加以下属性：

```json
{
  "enableDockerAI": {
    "value": false,
    "locked": true
  }
}
```

或者通过将 `allowBetaFeatures` 设置为 false 来禁用所有 Beta 功能：

```json
{
  "allowBetaFeatures": {
    "value": false,
    "locked": true
  }
}
```

## 反馈

<!-- vale Docker.We = NO -->

我们重视您对 Ask Gordon 的意见，并鼓励您分享您的体验。您的反馈帮助我们改进和优化 Ask Gordon，造福所有用户。如果您遇到问题、有建议或只是想分享您的喜欢之处，以下是可以联系我们的方式：

- 点赞和点踩按钮

  使用响应中的点赞或点踩按钮对 Ask Gordon 的回复进行评分。

- 反馈调查

  您可以通过 Docker Desktop 中 **Ask Gordon** 视图中的 _Give feedback_ 链接，或通过 CLI 运行 `docker ai feedback` 命令访问 Ask Gordon 调查。