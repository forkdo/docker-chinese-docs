# Docker MCP Catalog and Toolkit




[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) 是一种开放协议，用于标准化 AI 应用程序访问外部工具和数据源的方式。通过将 LLM 连接到本地开发工具、数据库、API 和其他资源，MCP 扩展了其超越基础训练的能力。

问题在于，在本地运行 MCP 服务器会带来运维上的摩擦。你使用的每个应用程序都需要单独安装和配置每个服务器。你要在自己的机器上直接运行不受信任的代码，手动管理更新，并自行排查依赖冲突。为 Claude 配置一个 GitHub 服务器后，还要为 Cursor 再配置一遍，以此类推。每一次你都要管理凭据、权限和环境设置。

## Docker MCP 功能

[MCP Toolkit](/ai/mcp-catalog-and-toolkit/toolkit/) 和 [MCP Gateway](/ai/mcp-catalog-and-toolkit/mcp-gateway/) 通过集中式管理解决了这些挑战。你不必为每个 AI 应用程序分别配置每个服务器，而是只需设置一次，然后将所有客户端连接到它。整个工作流围绕三个概念展开：目录（catalogs）、配置文件（profiles）和客户端（clients）。

![MCP overview](./images/mcp_toolkit.avif)

[目录](/ai/mcp-catalog-and-toolkit/catalog/)是 MCP 服务器的精选集合。Docker MCP Catalog 提供 300 多个已验证的服务器，它们被打包为容器镜像，具备版本管理、来源溯源和安全更新。组织可以创建包含已批准服务器的[自定义目录](/ai/mcp-catalog-and-toolkit/catalog/#custom-catalogs)供其团队使用。

[配置文件](/ai/mcp-catalog-and-toolkit/profiles/)将服务器组织成命名集合，以适配不同项目。你的 "web-dev" 配置文件可能使用 GitHub 和 Playwright；而 "backend" 配置文件则使用数据库工具。配置文件同时支持来自目录的容器化服务器和远程 MCP 服务器。配置一次后，即可在各客户端之间或与团队共享。

客户端是连接到你的配置文件的 AI 应用程序。Claude Code、Cursor、Zed 等通过 MCP Gateway 进行连接，Gateway 会将请求路由到正确的服务器，并处理身份验证和生命周期管理。

> [!NOTE]
> 作为 Docker AI Governance 一部分的 MCP Gateway 是仅限邀请的功能。[联系 Docker 销售团队](https://www.docker.com/pricing/contact-sales/)以了解更多信息。

## 了解更多



