---
title: 模型上下文协议 (MCP)
description: 了解如何在 Docker Desktop 中使用 Gordon 配合模型上下文协议 (MCP) 服务器来扩展 AI 功能。
keywords: ai, mcp, gordon, docker desktop, docker, llm, model context protocol
grid:
- title: 内置工具
  description: 使用内置工具。
  icon: construction
  link: /ai/gordon/mcp/built-in-tools
- title: MCP 配置
  description: 按项目配置 MCP 工具。
  icon: manufacturing
  link: /ai/gordon/mcp/yaml
aliases:
 -/desktop/features/gordon/mcp/
---

[模型上下文协议](https://modelcontextprotocol.io/introduction) (MCP) 是一个
开放协议，它标准化了应用程序向大语言模型提供上下文和附加功能的方式。
MCP 作为客户端-服务器协议运行，其中客户端（例如 Gordon 等应用程序）发
送请求，服务器处理这些请求并向 AI 提供必要的上下文。MCP 服务器可能通
过执行代码来执行操作并检索结果、调用外部 API 或执行其他类似操作来获
取此上下文。

Gordon 以及 Claude Desktop 或 Cursor 等其他 MCP 客户端可以与作为容器
运行的 MCP 服务器进行交互。

{{< grid >}}