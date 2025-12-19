---
title: Model Context Protocol (MCP)
description: 了解如何在 Gordon 中使用 Model Context Protocol (MCP) 服务器，以扩展 Docker Desktop 中的 AI 功能。
keywords: ai, mcp, gordon, docker desktop, docker, llm, model context protocol
grid:
- title: 内置工具
  description: 使用内置工具。
  icon: construction
  link: /ai/gordon/mcp/built-in-tools
- title: MCP 配置
  description: 基于每个项目配置 MCP 工具。
  icon: manufacturing
  link: /ai/gordon/mcp/yaml
aliases:
 - /desktop/features/gordon/mcp/
---

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，用于标准化应用程序向大型语言模型提供上下文和附加功能的方式。MCP 采用客户端-服务器协议，其中客户端（例如 Gordon 这样的应用程序）发送请求，服务器处理这些请求，从而向 AI 提供必要的上下文。MCP 服务器可以通过执行代码以执行操作并检索结果、调用外部 API 或其他类似操作来收集此上下文。

Gordon 以及 Claude Desktop 或 Cursor 等其他 MCP 客户端，可以与作为容器运行的 MCP 服务器进行交互。

{{< grid >}}