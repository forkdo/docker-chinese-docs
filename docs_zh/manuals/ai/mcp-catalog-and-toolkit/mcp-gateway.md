---
title: MCP Gateway
linkTitle: Gateway
description: Docker 的 MCP Gateway 通过容器化的 MCP 服务器，为 AI 工具提供安全、集中且可扩展的编排，赋能开发者、运维人员和安全团队。
keywords: MCP Gateway
weight: 40
aliases:
- /ai/mcp-gateway/
---

> [!NOTE]
> 作为 Docker AI Governance 一部分的 MCP Gateway 是仅限邀请的功能。[联系 Docker 销售团队](https://www.docker.com/pricing/contact-sales/)以了解更多信息。

MCP Gateway 是 Docker 用于编排 Model Context Protocol (MCP) 服务器的开源解决方案。它充当客户端与服务器之间的集中式代理，管理配置、凭证和访问控制。

在不使用 MCP Gateway 的情况下使用 MCP 服务器时，您需要为每个 AI 应用程序单独进行配置。而使用 MCP Gateway，您只需配置应用程序连接到该 Gateway。随后，Gateway 会为你的[配置文件](/manuals/ai/mcp-catalog-and-toolkit/profiles.md)中的所有服务器处理生命周期管理、路由和身份验证。

如果您启用了 MCP Toolkit 并使用 Docker Desktop，Gateway 会在后台自动运行。您无需手动启动或配置它。本文档面向希望了解 Gateway 工作原理或为高级用例直接运行它的用户。

> [!TIP]
> E2B 沙盒现已包含对 Docker MCP Catalog 的直接访问，让开发者能够使用超过 200 种工具和服务，无缝构建和运行 AI 代理。更多信息，请参阅 [E2B 沙盒](sandboxes.md)。

## 工作原理

MCP Gateway 在受限的 Docker 容器中运行 MCP 服务器，这些容器具有受限的权限、网络访问和资源使用。它包含内置的日志记录和调用追踪功能，以确保对 AI 工具活动的完全可见性和治理。

MCP Gateway 管理服务器的整个生命周期。当 AI 应用程序需要使用某个工具时，它会向 Gateway 发送请求。Gateway 识别出处理该工具的服务器，如果该服务器尚未运行，则将其作为 Docker 容器启动。然后，Gateway 注入任何所需的凭证，应用安全限制，并将请求转发给服务器。服务器处理请求，并通过 Gateway 将结果返回给 AI 应用程序。

MCP Gateway 解决了一个根本性问题：MCP 服务器只是需要在某处运行的程序。直接在您的机器上运行意味着要处理安装、依赖项、更新和安全风险。通过将它们作为由 Gateway 管理的容器运行，您可以获得隔离性、一致的环境和集中控制。

Gateway 会结合配置文件来确定哪些服务器可用。运行 Gateway 时，你可以使用 `--profile` 标志指定要使用的配置文件，从而决定向客户端提供哪些服务器。

## 使用方法

要使用 MCP Gateway，您需要启用 MCP Toolkit 的 Docker Desktop。请按照 [MCP Toolkit 指南](toolkit.md) 通过 Docker Desktop 界面启用和配置服务器；若需基于终端的工作流，请参阅[从 CLI 使用 MCP Toolkit](cli.md)。

### 手动安装 MCP Gateway

对于没有 Docker Desktop 的 Docker Engine，您需要先单独下载并安装 MCP Gateway，然后才能运行它。

1. 从 [GitHub 发布页面](https://github.com/docker/mcp-gateway/releases/latest) 下载最新的二进制文件。

2. 将二进制文件移动或符号链接到与您的操作系统匹配的目标位置：

   | 操作系统 | 二进制文件目标位置                  |
   | ------- | ----------------------------------- |
   | Linux   | `~/.docker/cli-plugins/docker-mcp`  |
   | macOS   | `~/.docker/cli-plugins/docker-mcp`  |
   | Windows | `%USERPROFILE%\.docker\cli-plugins` |

3. 使二进制文件可执行：

   ```bash
   $ chmod +x ~/.docker/cli-plugins/docker-mcp
   ```

您现在可以使用 `docker mcp` 命令：

```bash
docker mcp --help
```

## 其他信息

有关 MCP Gateway 工作原理和可用自定义选项的更多详细信息，请参阅 [GitHub 上](https://github.com/docker/mcp-gateway)的完整文档。
