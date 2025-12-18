---
title: Dynamic MCP
linkTitle: Dynamic MCP
description: 使用自然语言发现并按需添加 MCP 服务器，Dynamic MCP 服务器
keywords: dynamic mcps, mcp discovery, mcp-find, mcp-add, code-mode, ai agents, model context protocol
weight: 35
params:
  sidebar:
    badge:
      color: green
      text: 新功能
---

Dynamic MCP 使 AI 代理能够在对话过程中按需发现并添加 MCP 服务器，无需手动配置。您不再需要在启动代理会话前预先配置每个 MCP 服务器，客户端可以搜索 [MCP 目录](/manuals/ai/mcp-catalog-and-toolkit/catalog.md) 并根据需要添加服务器。

当您将 MCP 客户端连接到 [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md) 时，此功能会自动启用。网关提供一组原始工具，代理在运行时使用这些工具来发现和管理服务器。

{{% experimental %}}

Dynamic MCP 是一个处于早期开发阶段的实验性功能。虽然欢迎您尝试并探索其功能，但您可能会遇到意外行为或限制。我们欢迎通过 [GitHub issues](https://github.com/docker/mcp-gateway/issues) 提交错误报告，通过 [GitHub discussions](https://github.com/docker/mcp-gateway/discussions) 提出一般性问题和功能请求。

{{% /experimental %}}

## 工作原理

当您将客户端连接到 MCP 网关时，网关会与您已启用的任何 MCP 服务器一起公开一组小型管理工具。这些管理工具允许代理与网关的配置进行交互：

| 工具             | 描述                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `mcp-find`       | 在目录中按名称或描述搜索 MCP 服务器             |
| `mcp-add`        | 向当前会话添加新的 MCP 服务器                              |
| `mcp-config-set` | 配置 MCP 服务器的设置                                     |
| `mcp-remove`     | 从会话中移除 MCP 服务器                                    |
| `mcp-exec`       | 执行当前会话中已存在的工具 |
| `code-mode`      | 创建一个支持 JavaScript 的工具，组合多个 MCP 服务器工具 |

有了这些工具，代理可以搜索目录、添加服务器、处理身份验证，并直接使用新添加的工具，而无需重启或手动配置。

动态添加的服务器和工具仅与您的 _当前会话_ 相关联。当您开始新会话时，之前添加的服务器不会自动包含在内。

## 先决条件

要使用 Dynamic MCP，您需要：

- Docker Desktop 版本 4.50 或更高版本，并启用 [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- 支持 MCP 的 LLM 应用程序（例如 Claude Desktop、Visual Studio Code 或 Claude Code）
- 您的客户端配置为连接到 MCP 网关

请参阅 [Docker MCP Toolkit 入门指南](/manuals/ai/mcp-catalog-and-toolkit/get-started.md) 了解设置说明。

## 使用方法

使用 MCP Toolkit 时，Dynamic MCP 会自动启用。您的连接客户端现在可以在对话期间使用 `mcp-find`、`mcp-add` 和其他管理工具。

要体验 Dynamic MCP 的功能，请将您的 AI 客户端连接到 Docker MCP Toolkit 并尝试以下提示：

```plaintext
我可以使用哪些 MCP 服务器来处理 SQL 数据库？
```

给定此提示后，您的代理将使用 MCP Toolkit 提供的 `mcp-find` 工具在 [MCP 目录](./catalog.md) 中搜索与 SQL 相关的服务器。

要向会话添加服务器，只需编写一个提示，MCP Toolkit 会负责安装和运行服务器：

```plaintext
添加 postgres mcp 服务器
```

## 使用代码模式进行工具组合

`code-mode` 工具作为实验性功能提供，用于创建组合多个 MCP 服务器工具的自定义 JavaScript 函数。其预期用例是启用协调多个服务的单一操作工作流。

> **注意**
>
> 代码模式处于早期开发阶段，目前尚不可靠，不适合一般使用。
> 出于这个原因，文档有意省略了使用示例。
>
> 核心 Dynamic MCP 功能（`mcp-find`、`mcp-add`、`mcp-config-set`、`mcp-remove`）按文档工作，是当前使用的推荐重点。

该架构的工作原理如下：

1. 代理使用服务器名称列表和工具名称调用 `code-mode`
2. 网关创建一个可以访问这些服务器工具的沙箱
3. 在当前会话中注册一个新工具，使用指定的名称
4. 代理调用新创建的工具
5. 代码在沙箱中执行，通过指定的工具与外界交互
6. 结果返回给代理

沙箱只能通过 MCP 工具与外界交互，这些工具已经在隔离容器中运行，并具有受限权限。

## 安全注意事项

Dynamic MCP 在 MCP Toolkit 中保持与静态 MCP 服务器配置相同的安全模型：

- MCP 目录中的所有服务器均由 Docker 构建、签名和维护
- 服务器在具有受限资源的隔离容器中运行
- 代码模式在隔离沙箱中运行代理编写的 JavaScript，只能通过 MCP 工具进行交互
- 凭据由网关管理并安全注入到容器中

动态功能的关键区别在于代理可以在运行时添加新工具。

## 禁用 Dynamic MCP

Dynamic MCP 在 MCP Toolkit 中默认启用。如果您只想使用静态配置的 MCP 服务器，可以禁用动态工具功能：

```console
$ docker mcp feature disable dynamic-tools
```

稍后要重新启用该功能：

```console
$ docker mcp feature enable dynamic-tools
```

更改此设置后，您可能需要重启任何连接的 MCP 客户端。

## 进一步阅读

请查看 [Docker Dynamic MCP 服务器](https://docker.com/blog) 博客文章，了解有关如何使用动态工具的更多示例和灵感。