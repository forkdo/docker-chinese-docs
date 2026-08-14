---
title: Docker MCP 目录
linkTitle: Catalog
description: 浏览 Docker 精选的已验证 MCP 服务器合集，并为你的团队或组织创建自定义目录。
keywords: docker hub, mcp, mcp servers, ai agents, catalog, custom catalog, docker
weight: 20
---

{{< summary-bar feature_name="Docker MCP Catalog" >}}

[Docker MCP 目录](https://hub.docker.com/mcp)是经过验证的 MCP 服务器精选集合，它们被打包为 Docker 镜像并通过 Docker Hub 分发。它解决了在本地运行 MCP 服务器时的常见难题：环境冲突、设置复杂以及安全顾虑。

该目录是可用 MCP 服务器的来源。当你向[配置文件](/manuals/ai/mcp-catalog-and-toolkit/profiles.md)中添加服务器时，就是从目录中进行选择。每个服务器都作为独立容器运行，因此在不同环境中都具有可移植性和一致性。

> [!NOTE]
> E2B 沙箱现在包含对 Docker MCP 目录的直接访问，为开发人员提供超过 200 种工具和服务，以无缝构建和运行 AI 智能体。更多信息，请参阅 [E2B Sandboxes](e2b-sandboxes.md)。

## 目录中包含什么

Docker MCP 目录包括：

- 已验证的服务器：所有服务器均有版本管理，并附带完整的来源溯源和 SBOM 元数据
- 合作伙伴工具：来自 New Relic、Stripe、Grafana 及其他可信合作伙伴的服务器
- Docker 构建的服务器：由 Docker 构建并进行数字签名的本地运行服务器，安全性更高
- 远程服务：连接到 GitHub、Notion 和 Linear 等外部服务的云托管服务器

### 本地服务器与远程服务器

根据运行位置的不同，目录中包含两类服务器：

本地服务器作为容器在你的机器上运行。下载后即可离线工作，并提供可预测的性能和完全的数据隐私。目录中的所有本地服务器均由 Docker 构建并签名。

远程服务器运行在提供商的基础设施上，并连接到外部服务。许多远程服务器使用 OAuth 身份验证，MCP Toolkit 会通过你的浏览器自动处理。

## 浏览目录

你可以在 [hub.docker.com/mcp](https://hub.docker.com/mcp) 浏览可用的 MCP 服务器，也可以直接在 Docker Desktop 中浏览：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**。
2. 选择 **Catalog** 选项卡以浏览可用服务器。
3. 选择一个服务器以查看其描述、工具和配置选项。

## 将服务器添加到配置文件

要将目录中的服务器添加到配置文件：

1. 在 **Catalog** 选项卡中，勾选服务器旁边的复选框。
2. 从下拉菜单中选择要添加到的配置文件。

有关分步说明和客户端连接方式，请参阅[开始使用 MCP Toolkit](get-started.md)或 [MCP Profiles](profiles.md)。

## Custom catalogs（自定义目录）

自定义目录让你能为团队或组织精心整理出聚焦的服务器集合。你无需暴露 Docker 目录中全部 300 多个服务器，而是精确定义哪些服务器可用。

常见用例：

- 限制组织批准使用的服务器范围
- 在公共服务器之外添加组织的私有 MCP 服务器
- 控制团队使用的服务器版本
- 为使用 [Dynamic MCP](dynamic-mcp.md) 的 AI 智能体定义可用的服务器集合

### 自定义目录与 Dynamic MCP

自定义目录与 [Dynamic MCP](/ai/mcp-catalog-and-toolkit/dynamic-mcp/) 配合得尤其好：在 Dynamic MCP 中，智能体会在对话过程中按需发现并添加 MCP 服务器。当你使用自定义目录运行网关时，`mcp-find` 工具只会在该目录内搜索。如果你的目录包含 20 个服务器而不是 300 多个，智能体就会在这个聚焦的集合中工作，按需发现并启用工具，而无需每次手动配置。

### 导入自定义目录

如果你的团队中有人创建并发布了目录，你可以使用其 OCI 注册表引用来导入它。

在 Docker Desktop 中：

1. 选择 **MCP Toolkit** 并选择 **Catalog** 选项卡。
2. 选择 **Import catalog**。
3. 输入目录的 OCI 引用（例如 `registry.example.com/mcp/team-catalog:latest`）。
4. 选择 **Import**。

使用 CLI：

```console
$ docker mcp catalog pull <oci-reference>
```

导入后，该目录会与 Docker 目录并列显示，你可以将其中的服务器添加到配置文件中。

### 创建和管理自定义目录

创建和管理自定义目录需要使用 CLI。有关分步说明，请参阅 CLI 操作指南中的[自定义目录](/manuals/ai/mcp-catalog-and-toolkit/cli.md#custom-catalogs)，其中包括：

- 从 Docker 目录中挑选子集
- 向目录添加私有服务器
- 从零开始构建聚焦的目录
- 将目录推送到注册表以供团队导入

## 向目录贡献 MCP 服务器

MCP 服务器注册中心位于 https://github.com/docker/mcp-registry。要提交 MCP 服务器，请遵循 [贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)。

当您的拉取请求经过审核并被批准后，您的 MCP 服务器将在 24 小时内可在以下位置使用：

- Docker Desktop 的 [MCP Toolkit 功能](toolkit.md)。
- [Docker MCP 目录](https://hub.docker.com/mcp)。
- [Docker Hub](https://hub.docker.com/u/mcp) 的 `mcp` 命名空间（针对由 Docker 构建的 MCP 服务器）。
