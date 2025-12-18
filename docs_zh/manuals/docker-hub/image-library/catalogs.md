---
description: 探索 Docker Hub 专业集合，如生成式 AI 目录。
keywords: Docker Hub, Hub, 目录
title: Docker Hub 目录
linkTitle: 目录
weight: 60
---

Docker Hub 目录是您获取值得信赖、开箱即用的容器镜像和资源的首选集合，专为满足特定开发需求而设计。它们让发现高质量、预验证内容变得更加简单，使您能够自信地快速构建、部署和管理应用程序。Docker Hub 中的目录具有以下优势：

- **简化内容发现**：经过组织和策划的内容使您能够轻松发现适合特定领域或技术的工具和资源。
- **降低复杂性**：由 Docker 及其合作伙伴验证的可信资源，确保安全性、可靠性和符合最佳实践。
- **加速开发**：快速将高级功能集成到您的应用程序中，无需进行大量研究或配置工作。

以下部分概述了 Docker Hub 中可用的关键目录。

## MCP 目录

[MCP 目录](https://hub.docker.com/mcp/) 是一个集中式、可信赖的注册中心，用于发现、共享和运行兼容 Model Context Protocol (MCP) 的工具。它无缝集成到 Docker Hub 中，包括：

- 超过 100 个经过验证的 MCP 服务器，打包为 Docker 镜像
- 来自 New Relic、Stripe 和 Grafana 等合作伙伴的工具
- 经发布者验证的版本化发布
- 通过 Docker Desktop 和 Docker CLI 简化的拉取和运行支持

每个服务器都在隔离的容器中运行，以确保一致的行为并最大限度地减少配置问题。对于使用 Claude Desktop 或其他 MCP 客户端的开发者，该目录提供了一种通过即插即用工具扩展功能的简便方法。

要了解有关 MCP 服务器的更多信息，请参阅 [MCP 目录和工具包](../../ai/mcp-catalog-and-toolkit/_index.md)。

## AI 模型目录

[AI 模型目录](https://hub.docker.com/catalogs/models/) 提供了经过策划和信任的模型，与 [Docker Model Runner](../../ai/model-runner/_index.md) 配合使用。该目录旨在通过提供预打包、开箱即用的模型来简化 AI 开发，您可以使用熟悉的 Docker 工具拉取、运行并与之交互。

借助 AI 模型目录和 Docker Model Runner，您可以：

- 从 Docker Hub 或任何符合 OCI 标准的注册中心拉取和提供模型
- 通过兼容 OpenAI 的 API 与模型交互
- 使用 Docker Desktop 或 CLI 在本地运行和测试模型
- 使用 `docker model` CLI 打包和发布模型

无论您是构建生成式 AI 应用程序、将大语言模型 (LLM) 集成到工作流中，还是试验机器学习工具，AI 模型目录都能简化模型管理体验。