---
title: 动态 MCP
linkTitle: 动态 MCP
description: 使用自然语言通过动态 MCP 服务器按需发现并添加 MCP 服务器
keywords: dynamic mcps, mcp discovery, mcp-find, mcp-add, code-mode, ai agents, model context protocol
weight: 35
params:
  sidebar:
    badge:
      color: green
      text: New
---

Dynamic MCP 使 AI 代理能够在对话过程中按需发现并添加 MCP 服务器，无需手动配置。在启动代理会话之前，无需预先配置每个 MCP 服务器，客户端可以搜索 [MCP 目录](/manuals/ai/mcp-catalog-and-toolkit/catalog.md) 并根据需要添加服务器。

当您将 MCP 客户端连接到 [MCP 工具包](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md) 时，此功能会自动启用。网关提供了一组基础工具，供代理在运行时用于发现和管理服务器。

{{% experimental %}}

Dynamic MCP 是早期开发阶段的实验性功能。欢迎您尝试并探索其功能，但您可能会遇到意外行为或限制。欢迎通过 [GitHub 问题](https://github.com/docker/mcp-gateway/issues) 提交错误报告，以及通过 [GitHub 讨论](https://github.com/docker/mcp-gateway/discussions) 提出一般性问题和功能请求。

{{% /experimental %}}

## 工作原理

当您将客户端连接到 MCP 网关时，网关会暴露一小套管理工具，以及您已启用的任何 MCP 服务器。这些管理工具让代理可以与网关的配置进行交互：

| 工具             | 描述                                                              |
| ---------------- | ------------------------------------------------------------------------ |
| `mcp-find`       | 按名称或描述在目录中搜索 MCP 服务器             |
| `mcp-add`        | 将新的 MCP 服务器添加到当前会话                              |
| `mcp-config-set` | 配置 MCP 服务器的设置                                     |
| `mcp-remove`     | 从会话中移除 MCP 服务器                                    |
| `mcp-exec`       | 按名称执行当前会话中存在的工具                |
| `code-mode`      | 创建一个启用 JavaScript 的工具，该工具组合了多个 MCP 服务器工具 |

有了这些可用的工具，代理可以搜索目录、添加服务器、处理身份验证，并直接使用新添加的工具，无需重启或手动配置。

动态添加的服务器和工具仅与您*当前的会话相关联*。当您启动新会话时，之前添加的服务器不会自动包含在内。

## 先决条件

要使用 Dynamic MCP，您需要：

- Docker Desktop 4.50 或更高版本，并已启用 [MCP 工具包](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- 一个支持 MCP 的 LLM 应用程序（例如 Claude Desktop、Visual Studio Code 或 Claude Code）
- 您的客户端已配置为连接到 MCP 网关

有关设置说明，请参阅 [Docker MCP 工具包入门](/manuals/ai/mcp-catalog-and-toolkit/get-started.md)。

## 用法

当您使用 MCP 工具包时，Dynamic MCP 会自动启用。您连接的客户端现在可以在对话中使用 `mcp-find`、`mcp-add` 和其他管理工具。

要查看 Dynamic MCP 的实际操作，请将您的 AI 客户端连接到 Docker MCP 工具包，并尝试以下提示：

```plaintext
我可以使用哪些 MCP 服务器来处理 SQL 数据库？
```

对于此提示，您的代理将使用 MCP 工具包提供的 `mcp-find` 工具在 [MCP 目录](./catalog.md) 中搜索与 SQL 相关的服务器。

要将会话添加服务器，只需编写一个提示，MCP 工具包就会负责安装和运行服务器：

```plaintext
添加 postgres mcp 服务器
```

## 使用代码模式进行工具组合

`code-mode` 工具作为一项实验性功能提供，用于创建组合多个 MCP 服务器工具的自定义 JavaScript 函数。其预期用例是支持在单个操作中协调多个服务的工作流。

> **注意**
>
> 代码模式处于早期开发阶段，尚未可靠到可供常规使用。
> 本文档目前有意省略用法示例。
>
> 核心 Dynamic MCP 功能（`mcp-find`、`mcp-add`、`mcp-config-set`、`mcp-remove`）按文档所述工作，是当前使用的推荐重点。

其架构如下：

1.  代理使用服务器名称列表和工具名称调用 `code-mode`
2.  网关创建一个可访问这些服务器工具的沙箱
3.  一个新工具以指定名称注册到当前会话中
4.  代理调用新创建的工具
5.  代码在沙箱中执行，并可访问指定的工具
6.  结果返回给代理

沙箱只能通过 MCP 工具与外部世界交互，这些工具已经在具有受限权限的隔离容器中运行。

## 安全注意事项

Dynamic MCP 维护与 MCP 工具包中静态 MCP 服务器配置相同的安全模型：

-   MCP 目录中的所有服务器均由 Docker 构建、签名和维护
-   服务器在具有受限资源的隔离容器中运行
-   代码模式在隔离的沙箱中运行代理编写的 JavaScript，该沙箱只能通过 MCP 工具进行交互
-   凭据由网关管理并安全注入容器

与动态功能的关键区别在于，代理可以在运行时添加新工具。

## 禁用 Dynamic MCP

Dynamic MCP 在 MCP 工具包中默认启用。如果您更喜欢仅使用静态配置的 MCP 服务器，可以禁用动态工具功能：

```console
$ docker mcp feature disable dynamic-tools
```

要在稍后重新启用该功能：

```console
$ docker mcp feature enable dynamic-tools
```

更改此设置后，您可能需要重启任何已连接的 MCP 客户端。

## 延伸阅读

请查看 [使用 Docker 的动态 MCP 服务器](https://docker.com/blog) 博客文章，获取更多关于如何使用动态工具的示例和灵感。