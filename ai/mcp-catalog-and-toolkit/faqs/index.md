# 安全常见问题解答

Docker MCP 目录和工具包是一个用于安全构建、共享和运行 MCP 工具的解决方案。此页面解答了有关 MCP 目录和工具包安全性的常见问题。

### Docker 遵循什么流程将新的 MCP 服务器添加到目录中？

开发者可以向 [Docker MCP Registry](https://github.com/docker/mcp-registry) 提交拉取请求来提议新的服务器。Docker 提供了详细的[贡献指南](https://github.com/docker/mcp-registry/blob/main/CONTRIBUTING.md)，帮助开发者满足所需标准。

目前，目录中的大多数服务器都是由 Docker 直接构建的。每个服务器都包含以下证明：

- 构建证明：服务器在 Docker Build Cloud 上构建。
- 源代码出处：可验证的源代码来源。
- 已签名的 SBOM：带有加密签名的软件物料清单。

> [!NOTE]
> 当使用 [Docker MCP 网关](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 镜像时，
> 您可以使用 `docker mcp gateway run --verify-signatures` CLI 命令在运行时验证证明。

除了 Docker 构建的服务器外，目录还包括来自受信任注册表（如 GitHub 和 HashiCorp）的精选服务器。每个第三方服务器都需经过验证流程，包括：

- 在临时构建环境中拉取和构建代码。
- 测试初始化和功能。
- 验证工具是否可以成功列出。

### 在什么条件下 Docker 会拒绝 MCP 服务器提交？

Docker 会拒绝在拉取请求审查期间未能通过自动化测试和验证流程的 MCP 服务器提交。此外，Docker 审查员会根据特定要求评估提交内容，并拒绝不符合这些标准的 MCP 服务器。

### Docker 是否对工具包中的恶意 MCP 服务器承担责任？

Docker 目前的安全措施代表了一种尽力而为的方法。虽然 Docker 对目录中的每个服务器实施了自动化测试、扫描和元数据提取，但这些安全措施尚不全面。Docker 正在积极努力增强其安全流程并扩大测试覆盖范围。企业客户可以联系其 Docker 客户经理，了解具体的安全要求和实施细节。

### MCP 服务器的凭据是如何管理的？

从 Docker Desktop 4.43.0 版本开始，凭据安全地存储在 Docker Desktop 虚拟机中。存储实现取决于平台（例如 macOS、WSL2）。您可以使用以下 CLI 命令管理凭据：

- `docker mcp secret ls` - 列出存储的凭据
- `docker mcp secret rm` - 删除特定凭据
- `docker mcp oauth revoke` - 撤销基于 OAuth 的凭据

在 Docker Desktop 的后续版本中，Docker 计划支持这些密钥的可插拔存储以及额外的开箱即用存储提供程序，以便用户在管理凭据时拥有更大的灵活性。

### 卸载 MCP 服务器时是否会删除凭据？

不会。MCP 服务器在技术上不会被卸载，因为它们以 Docker 容器形式拉取到本地 Docker Desktop。删除 MCP 服务器会停止容器，但镜像仍保留在系统上。即使容器被删除，凭据也会保留，直到您手动删除它们。

### 为什么我在目录中看不到远程 MCP 服务器？

如果在 Docker Desktop 目录中看不到远程 MCP 服务器，则可能是本地目录已过期。远程服务器由云图标标识，包括 GitHub、Notion 和 Linear 等服务。

通过运行以下命令更新目录：

```console
$ docker mcp catalog update
```

更新完成后，刷新 Docker Desktop 中的**目录**选项卡。

## 相关页面

- [MCP 工具包入门](/manuals/ai/mcp-catalog-and-toolkit/get-started.md)
- [开源 MCP 网关](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
