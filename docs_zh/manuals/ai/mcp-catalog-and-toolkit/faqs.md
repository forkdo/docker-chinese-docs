---
title: 安全常见问题
linkTitle: 安全常见问题
description: 与 MCP 目录和工具包安全相关的常见问题
keywords: MCP, Toolkit, MCP server, MCP client, security, faq
tags: [FAQ]
weight: 70
---

Docker MCP 目录和工具包是一种用于安全构建、共享和运行 MCP 工具的解决方案。本页面解答了关于 MCP 目录和工具包安全的常见问题。

### Docker 添加新 MCP 服务器到目录的流程是什么？

开发者可以向 [Docker MCP Registry](https://github.com/docker/mcp-registry) 提交拉取请求，以提议新的服务器。Docker 提供了详细的 [贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)，帮助开发者达到所需的标准。

目前，目录中的大部分服务器均由 Docker 直接构建。每个服务器都包含以下证明：

- 构建证明：服务器在 Docker Build Cloud 上构建。
- 源代码来源：可验证的源代码来源。
- 已签名的 SBOM：带有加密签名的软件物料清单。

> [!NOTE]
> 在与 [Docker MCP 网关](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 一起使用这些镜像时，
> 您可以使用 `docker mcp gateway run --verify-signatures` CLI 命令在运行时验证证明。


除了 Docker 构建的服务器外，目录还包括来自 GitHub 和 HashiCorp 等受信任注册中心的精选服务器。每个第三方服务器都经过验证流程，包括：

- 在临时构建环境中拉取和构建代码。
- 测试初始化和功能。
- 验证工具能够成功列出。

### Docker 在什么条件下会拒绝 MCP 服务器提交？

Docker 会在拉取请求审核期间的自动化测试和验证过程中拒绝失败的 MCP 服务器提交。此外，Docker 审核人员会根据特定要求评估提交内容，并拒绝不符合这些标准的 MCP 服务器。

### Docker 是否对工具包中恶意 MCP 服务器承担责任？

Docker 的安全措施目前代表一种尽力而为的方法。虽然 Docker 为目录中的每个服务器实施了自动化测试、扫描和元数据提取，但这些安全措施尚未详尽无遗。Docker 正在积极改进其安全流程并扩大测试覆盖范围。企业客户可以联系其 Docker 客户经理，了解特定的安全要求和实施细节。

### MCP 服务器的凭据如何管理？

从 Docker Desktop 版本 4.43.0 开始，凭据安全地存储在 Docker Desktop 虚拟机中。存储实现取决于平台（例如，macOS、WSL2）。您可以使用以下 CLI 命令管理凭据：

- `docker mcp secret ls` - 列出存储的凭据
- `docker mcp secret rm` - 删除特定凭据
- `docker mcp oauth revoke` - 撤销基于 OAuth 的凭据

在即将发布的 Docker Desktop 版本中，Docker 计划支持这些机密的可插拔存储，以及更多开箱即用的存储提供商，为用户提供更多管理凭据的灵活性。

### 卸载 MCP 服务器时凭据会被移除吗？

不会。MCP 服务器在技术上并未卸载，因为它们作为 Docker 容器存在于您的本地 Docker Desktop 中。移除 MCP 服务器会停止容器，但镜像仍保留在您的系统上。即使容器被删除，凭据也会继续存储，直到您手动移除它们。

### 为什么我在目录中看不到远程 MCP 服务器？

如果在 Docker Desktop 目录中看不到远程 MCP 服务器，您的本地目录可能已过期。远程服务器由云图标指示，包括 GitHub、Notion 和 Linear 等服务。

运行以下命令更新目录：

```console
$ docker mcp catalog update
```

更新完成后，刷新 Docker Desktop 中的 **目录** 选项卡。

## 相关页面

- [MCP 工具包入门](/manuals/ai/mcp-catalog-and-toolkit/get-started.md)
- [开源 MCP 网关](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)