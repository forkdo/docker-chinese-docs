---
title: Docker MCP 目录和工具包
linkTitle: MCP 目录和工具包
params:
  sidebar:
    group: AI
    badge:
      color: blue
      text: Beta
weight: 10
description: 了解 Docker 在 Docker Hub 上的 MCP 目录
keywords: Docker, ai, mcp servers, ai agents, extension, docker desktop, llm, docker hub
grid:
 - title: 开始使用 MCP 工具包
   description: 了解如何快速安装和使用 MCP 工具包来设置服务器和客户端。
   icon: explore
   link: /ai/mcp-catalog-and-toolkit/get-started/
 - title: MCP 目录
   description: 了解 MCP 目录的优势、使用方法以及如何贡献内容
   icon: hub
   link: /ai/mcp-catalog-and-toolkit/catalog/
 - title: MCP 工具包
   description: 了解关于 MCP 工具包以管理 MCP 服务器和客户端
   icon: /icons/toolkit.svg
   link: /ai/mcp-catalog-and-toolkit/toolkit/
 - title: 动态 MCP
   description: 使用自然语言按需发现和添加 MCP 服务器
   icon: search
   link: /ai/mcp-catalog-and-toolkit/dynamic-mcp/
 - title: MCP 网关
   description: 了解支持 MCP 工具包的底层技术
   icon: developer_board
   link: /ai/mcp-catalog-and-toolkit/mcp-gateway/
 - title: Docker Hub MCP 服务器
   description: 探索关于 Docker Hub 服务器，用于搜索镜像、管理仓库等
   icon: device_hub
   link: /ai/mcp-catalog-and-toolkit/hub-mcp/
---

{{< summary-bar feature_name="Docker MCP 目录和工具包" >}}

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP)
是一种开放协议，标准化了 AI 应用访问外部工具和数据源的方式。通过将 LLM
连接到本地开发工具、数据库、API 和其他资源，MCP 扩展了它们超越基础训练
的能力范围。

通过客户端-服务器架构，诸如 Claude、ChatGPT 和
[Gordon](/manuals/ai/gordon/_index.md) 等应用作为客户端，向 MCP 服务器
发送请求，服务器处理这些请求后将必要的上下文传递给 AI 模型。

MCP 服务器扩展了 AI 应用的实用性，但在本地运行服务器也带来了一些操作
挑战。通常，服务器必须直接安装在您的机器上，并为每个应用单独配置。在
本地运行未经信任的代码需要仔细审查，而保持服务器更新和解决环境冲突的
责任也落在用户身上。

## Docker MCP 功能

Docker 提供三个集成组件，解决在本地运行 MCP 服务器的挑战：

MCP 目录
: Docker Hub 上经过验证的 MCP 服务器精选集合，以容器镜像形式打包和分发。
所有服务器都经过版本控制，附带完整的来源和 SBOM 元数据，并持续维护和
更新安全补丁。

MCP 工具包
: Docker Desktop 中的图形界面，用于发现、配置和管理 MCP 服务器。工具包
提供统一方式来搜索服务器、处理身份验证，并将它们连接到您使用的 AI
应用。

MCP 网关
: 支撑 MCP 工具包的核心开源组件。MCP 网关管理 MCP 容器，提供统一端点，
将您启用的服务器暴露给您使用的所有 AI 应用。

这种集成方法确保：

- 从精选工具目录中简化发现和设置可信 MCP 服务器
- 在 Docker Desktop 内集中配置和身份验证
- 默认提供安全、一致的执行环境
- 提升性能，因为应用可以共享单个服务器运行时，而无需为每个应用启动
重复的服务器。

![MCP 概览](./images/mcp-overview.svg)

## 了解更多

{{< grid >}}