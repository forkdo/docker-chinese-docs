---
title: Docker MCP Catalog and Toolkit
url: /ai/mcp-catalog-and-toolkit/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker MCP Catalog and Toolkit
    url: /ai/mcp-catalog-and-toolkit/
children:
  - title: Docker MCP Toolkit 入门指南
    url: /ai/mcp-catalog-and-toolkit/get-started/
    description: 了解如何快速安装和使用 MCP Toolkit 来设置服务器和客户端。
  - title: Docker MCP 目录
    url: /ai/mcp-catalog-and-toolkit/catalog/
    description: 了解 MCP 目录的优势、使用方法以及如何贡献内容
  - title: Docker MCP Toolkit
    url: /ai/mcp-catalog-and-toolkit/toolkit/
    description: 使用 MCP Toolkit 设置 MCP 服务器和 MCP 客户端。
  - title: 动态 MCP
    url: /ai/mcp-catalog-and-toolkit/dynamic-mcp/
    description: 使用自然语言通过动态 MCP 服务器按需发现并添加 MCP 服务器
  - title: MCP Gateway
    url: /ai/mcp-catalog-and-toolkit/mcp-gateway/
    description: Docker 的 MCP Gateway 通过容器化的 MCP 服务器，为 AI 工具提供安全、集中且可扩展的编排，赋能开发者、运维人员和安全团队。
  - title: Docker Hub MCP 服务器
    url: /ai/mcp-catalog-and-toolkit/hub-mcp/
    description: Docker Hub MCP 服务器使 LLM 能够访问 Docker Hub 镜像元数据，以实现内容发现。
  - title: 安全常见问题解答
    url: /ai/mcp-catalog-and-toolkit/faqs/
    description: 与 MCP 目录和工具包安全性相关的常见问题
  - title: E2B 沙盒
    url: /ai/mcp-catalog-and-toolkit/e2b-sandboxes/
    description: 专为 AI 智能体设计的基于云的安全沙盒，内置 Docker MCP Gateway 集成
---




[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，用于标准化 AI 应用程序访问外部工具和数据源的方式。通过将 LLM 连接到本地开发工具、数据库、API 和其他资源，MCP 扩展了其超越基础训练的能力。

通过客户端-服务器架构，Claude、ChatGPT 和 [Gordon](/manuals/ai/gordon/_index.md) 等应用程序充当客户端，向 MCP 服务器发送请求，然后服务器处理这些请求并将必要的上下文传递给 AI 模型。

MCP 服务器扩展了 AI 应用程序的实用性，但在本地运行服务器也带来了一些操作挑战。通常，服务器必须直接安装在您的机器上，并为每个应用程序单独配置。在本地运行不受信任的代码需要仔细审查，而保持服务器最新和解决环境冲突的责任则落在用户身上。

## Docker MCP 功能

Docker 提供了三个集成组件，用于解决运行本地 MCP 服务器的挑战：

MCP Catalog
: 一个经过验证的 MCP 服务器精选集合，通过 Docker Hub 作为容器镜像打包和分发。所有服务器都经过版本控制，附带完整的来源和 SBOM 元数据，并持续维护和更新安全补丁。

MCP Toolkit
: Docker Desktop 中用于发现、配置和管理 MCP 服务器的图形界面。Toolkit 提供了一种统一的方式来搜索服务器、处理身份验证以及将它们连接到 AI 应用程序。

MCP Gateway
: 为 MCP Toolkit 提供支持的核心开源组件。MCP Gateway 管理 MCP 容器，并提供一个统一的端点，将您启用的服务器暴露给您使用的所有 AI 应用程序。

这种集成方法确保：

- 从精选的工具目录中简化受信任 MCP 服务器的发现和设置
- 在 Docker Desktop 内进行集中配置和身份验证
- 默认情况下提供安全、一致的执行环境
- 由于应用程序可以共享单个服务器运行时，而不是为每个应用程序启动重复的服务器，从而提高了性能。

![MCP overview](./images/mcp-overview.svg)

## 了解更多


