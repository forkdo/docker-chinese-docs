---
description: 探索专门的 Docker Hub 集合，例如生成式 AI 目录。
keywords: Docker Hub, Hub, catalog
title: Docker Hub 目录
linkTitle: 目录
weight: 60
---

Docker Hub 目录是您值得信赖的、开箱即用的容器镜像和资源集合，旨在满足特定的开发需求。它们让您可以更轻松地找到高质量、经过预先验证的内容，从而能够自信地快速构建、部署和管理应用程序。Docker Hub 中的目录：

- **简化内容发现**：经过组织和策划的内容，让您轻松发现针对特定领域或技术的工具和资源。
- **降低复杂性**：由 Docker 及其合作伙伴审核的可信资源，确保安全性、可靠性并遵循最佳实践。
- **加速开发**：无需进行大量研究或设置，即可将高级功能快速集成到您的应用程序中。

以下部分概述了 Docker Hub 中可用的关键目录。

## MCP 目录

[MCP 目录](https://hub.docker.com/mcp/) 是一个集中式、可信的注册中心，用于发现、共享和运行与模型上下文协议 (MCP) 兼容的工具。该目录与 Docker Hub 无缝集成，包含：

- 超过 100 个打包为 Docker 镜像的经过验证的 MCP 服务器
- 来自 New Relic、Stripe 和 Grafana 等合作伙伴的工具
- 带有发布者验证的版本化发布
- 通过 Docker Desktop 和 Docker CLI 提供简化的拉取和运行支持

每个服务器都在隔离的容器中运行，以确保行为一致并最大限度地减少配置麻烦。对于使用 Claude Desktop 或其他 MCP 客户端的开发人员来说，该目录提供了一种使用即插即用工具扩展功能的简便方法。

要了解有关 MCP 服务器的更多信息，请参阅 [MCP 目录和工具包](../../ai/mcp-catalog-and-toolkit/_index.md)。

## AI 模型目录

[AI 模型目录](https://hub.docker.com/catalogs/models/) 提供经过策划、可信赖的模型，这些模型可与 [Docker 模型运行器](../../ai/model-runner/_index.md) 配合使用。该目录旨在通过提供预先打包、开箱即用的模型，让您使用熟悉的 Docker 工具即可拉取、运行和交互，从而使 AI 开发更易于访问。

借助 AI 模型目录和 Docker 模型运行器，您可以：

- 从 Docker Hub 或任何符合 OCI 标准的注册中心拉取和服务模型
- 通过与 OpenAI 兼容的 API 与模型交互
- 使用 Docker Desktop 或 CLI 在本地运行和测试模型
- 使用 `docker model` CLI 打包和发布模型

无论您是构建生成式 AI 应用程序、将 LLM 集成到工作流程中，还是试验机器学习工具，AI 模型目录都简化了模型管理体验。