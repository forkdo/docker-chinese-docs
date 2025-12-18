---
title: MCP Gateway
description: "Docker 的 MCP Gateway 通过容器化的 MCP 服务器提供安全、集中且可扩展的 AI 工具编排能力——赋能开发者、运维人员和安全团队。"
keywords: MCP Gateway
weight: 40
aliases:
  - /ai/mcp-gateway/
---

MCP Gateway 是 Docker 开源的 Model Context Protocol (MCP) 服务器编排解决方案。它作为客户端与服务器之间的集中式代理，管理配置、凭据和访问控制。

在不使用 MCP Gateway 的情况下使用 MCP 服务器时，你需要为每个 AI 应用单独配置。而使用 MCP Gateway 后，你只需将应用配置为连接到 Gateway，Gateway 会处理所有服务器的生命周期、路由和身份验证。

> [!NOTE]
> 如果你启用了 MCP Toolkit 的 Docker Desktop，Gateway 会在后台自动运行，无需手动启动或配置。本文档面向需要了解 Gateway 工作原理或为高级用例直接运行 Gateway 的用户。

> [!TIP]
> E2B 沙箱现已包含对 Docker MCP 目录的直接访问，为开发者提供超过 200 种工具和服务，无缝构建和运行 AI 代理。详情请见 [E2B 沙箱](sandboxes.md)。

## 工作原理

MCP Gateway 在隔离的 Docker 容器中运行 MCP 服务器，限制其权限、网络访问和资源使用。它内置日志记录和调用追踪功能，确保 AI 工具活动的完全可见性和治理。

MCP Gateway 管理服务器的整个生命周期。当 AI 应用需要使用工具时，它向 Gateway 发送请求。Gateway 识别处理该工具的服务器，如果服务器尚未运行，则将其作为 Docker 容器启动。Gateway 随后注入所需凭据，应用安全限制，并将请求转发给服务器。服务器处理请求后，将结果通过 Gateway 返回给 AI 应用。

MCP Gateway 解决了一个根本问题：MCP 服务器只是需要运行的程序。直接在机器上运行它们意味着需要处理安装、依赖、更新和安全风险。通过 Gateway 管理的容器运行它们，你可以获得隔离、一致的环境和集中控制。

## 使用方法

要使用 MCP Gateway，你需要启用 MCP Toolkit 的 Docker Desktop。请参考 [MCP Toolkit 指南](toolkit.md) 通过图形界面启用和配置服务器。

### 从 CLI 管理 MCP Gateway

启用 MCP Toolkit 后，你也可以通过 CLI 与 MCP Gateway 交互。`docker mcp` 命令套件允许你直接从终端管理服务器和工具。你还可以手动运行带有自定义配置的 Gateway，包括安全限制、服务器目录等。

要使用自定义参数手动运行 MCP Gateway，请使用 `docker mcp` 命令套件。

1. 浏览 [MCP 目录](https://hub.docker.com/mcp)，找到你想要使用的服务器，复制 **手动安装** 部分的安装命令。

   例如，在终端运行以下命令安装 `duckduckgo` MCP 服务器：

   ```console
   docker mcp server enable duckduckgo
   ```

2. 连接客户端，如 Claude Code：

   ```console
   docker mcp client connect claude-code
   ```

3. 运行 Gateway：

   ```console
   docker mcp gateway run
   ```

现在你的 MCP Gateway 已运行，你可以从 Claude Code 通过它利用所有已配置的服务器。

### 手动安装 MCP Gateway

对于没有 Docker Desktop 的 Docker Engine，你需要先单独下载和安装 MCP Gateway，然后才能运行它。

1. 从 [GitHub 发布页面](https://github.com/docker/mcp-gateway/releases/latest) 下载最新版本的二进制文件。

2. 将二进制文件移动或符号链接到与你的操作系统匹配的目标位置：

   | 操作系统 | 二进制目标位置                    |
   | ------- | --------------------------------- |
   | Linux   | `~/.docker/cli-plugins/docker-mcp`|
   | macOS   | `~/.docker/cli-plugins/docker-mcp`|
   | Windows | `%USERPROFILE%\.docker\cli-plugins`|

3. 使二进制文件可执行：

   ```bash
   $ chmod +x ~/.docker/cli-plugins/docker-mcp
   ```

现在你可以使用 `docker mcp` 命令：

```bash
docker mcp --help
```

## 附加信息

有关 MCP Gateway 工作原理和可用自定义选项的更多详细信息，请参阅 [GitHub 上的完整文档](https://github.com/docker/mcp-gateway)。