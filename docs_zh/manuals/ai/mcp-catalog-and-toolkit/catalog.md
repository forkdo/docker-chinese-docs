---
title: Docker MCP 目录
linkTitle: MCP 目录
description: 了解 MCP 目录的优势、使用方法以及如何贡献
keywords: docker hub, mcp, mcp servers, ai agents, catalog, docker
weight: 20
---

{{< summary-bar feature_name="Docker MCP Catalog" >}}

[Docker MCP 目录](https://hub.docker.com/mcp) 是一个集中化、可信赖的注册中心，用于发现、共享和运行兼容 MCP 的工具。它与 Docker Hub 集成，提供经过验证、版本化和精心策划的 MCP 服务器，以 Docker 镜像形式打包。该目录也可在 Docker Desktop 中使用。

该目录解决了常见的 MCP 服务器挑战：

- 环境冲突。工具通常需要特定的运行时，可能与现有设置冲突。
- 缺乏隔离性。传统设置可能暴露主机系统。
- 设置复杂。手动安装和配置会拖慢采用速度。
- 跨平台不一致。工具在不同操作系统上可能表现不稳定。

借助 Docker，每个 MCP 服务器作为自包含的容器运行。这使其具有可移植性、隔离性和一致性。您可以使用 Docker CLI 或 Docker Desktop 立即启动工具，无需担心依赖项或兼容性问题。

## 主要功能

- 在一处集中大量经过验证的 MCP 服务器集合。
- 发布者验证和版本化发布。
- 使用 Docker 基础设施进行基于拉取的分发。
- 由 New Relic、Stripe、Grafana 等合作伙伴提供的工具。

> [!NOTE]
> E2B 沙箱现在包含对 Docker MCP 目录的直接访问，为开发人员提供 200 多种工具和服务，以无缝构建和运行 AI 代理。更多信息，请参阅 [E2B 沙箱](sandboxes.md)。

## 工作原理

MCP 目录中的每个工具都打包为带有元数据的 Docker 镜像。

- 在 Docker Hub 的 `mcp/` 命名空间下发现工具。
- 通过 [MCP Toolkit](toolkit.md) 使用简单配置将工具连接到您首选的代理。
- 使用 Docker Desktop 或 CLI 拉取和运行工具。

每个目录条目显示：

- 工具描述和元数据。
- 版本历史记录。
- MCP 服务器提供的工具列表。
- 代理集成的示例配置。

## 服务器部署类型

Docker MCP 目录支持本地和远程服务器部署，每种类型针对不同的用例和需求进行了优化。

### 本地 MCP 服务器

本地 MCP 服务器是作为容器化应用程序在您的机器上直接运行的应用。所有本地服务器均由 Docker 构建并进行数字签名，通过经过验证的来源和完整性提供增强的安全性。这些服务器作为容器在您的本地环境中运行，下载后无需互联网连接即可运行。本地服务器显示 Docker 图标 {{< inline-image src="../../desktop/images/whale-x.svg" alt="docker whale icon" >}} 以表明其由 Docker 构建。

本地服务器提供可预测的性能、完全的数据隐私，并且不依赖外部服务的可用性。它们适用于开发工作流、敏感数据处理以及需要离线功能的场景。

### 远程 MCP 服务器

远程 MCP 服务器是在提供商的基础架构上托管的服务，连接到 GitHub、Notion 和 Linear 等外部服务。许多远程服务器使用 OAuth 身份验证。当远程服务器需要 OAuth 时，MCP Toolkit 会自动处理身份验证——您通过浏览器授权访问，Toolkit 安全地管理凭据。您无需手动创建 API 令牌或配置身份验证。

远程服务器在目录中显示云图标。有关设置说明，请参阅 [MCP Toolkit](toolkit.md#oauth-authentication)。

## 从目录使用 MCP 服务器

要从目录使用 MCP 服务器，请参阅 [MCP Toolkit](toolkit.md)。

## 向目录贡献 MCP 服务器

MCP 服务器注册中心位于 https://github.com/docker/mcp-registry。要提交 MCP 服务器，请遵循 [贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)。

当您的拉取请求经过审查并获得批准后，您的 MCP 服务器将在 24 小时内可在以下位置使用：

- Docker Desktop 的 [MCP Toolkit 功能](toolkit.md)。
- [Docker MCP 目录](https://hub.docker.com/mcp)。
- [Docker Hub](https://hub.docker.com/u/mcp) 的 `mcp` 命名空间（针对由 Docker 构建的 MCP 服务器）。