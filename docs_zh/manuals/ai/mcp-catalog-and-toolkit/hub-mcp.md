---
title: Docker Hub MCP 服务器
linkTitle: Hub MCP 服务器
description: Docker Hub MCP 服务器通过 MCP 协议使 Docker Hub 镜像元数据可被 LLM 访问，用于内容发现。
keywords: Docker Hub MCP Server, Hub MCP server, Hub MCP
weight: 60
---

Docker Hub MCP 服务器是一个模型上下文协议（Model Context Protocol，MCP）服务器，它通过 Docker Hub API 提供丰富的镜像元数据，使 LLM 能够进行更智能的内容发现和仓库管理。

有关 MCP 概念及 MCP 服务器工作原理的更多信息，请参阅 [Docker MCP 目录和工具包](index.md) 概述页面。

## 主要功能

- **高级 LLM 上下文**：Docker 的 MCP 服务器为 LLM 提供详细的、结构化的 Docker Hub 镜像上下文，使推荐更智能、更相关，无论是选择基础镜像还是自动化 CI/CD 工作流。
- **自然语言镜像发现**：开发者可以使用自然语言查找合适的容器镜像，无需记住标签或仓库名称。只需描述需求，Docker Hub 即可返回匹配意图的镜像。
- **简化的仓库管理**：Hub MCP 服务器使智能体能够通过自然语言管理仓库，快速获取镜像详情、查看统计信息、搜索内容并执行关键操作。

## 安装 Docker Hub MCP 服务器

1. 在 **MCP Toolkit** 菜单中，选择 **Catalog** 标签页，搜索 **Docker Hub**，点击加号图标添加 Docker Hub MCP 服务器。
1. 在服务器的 **Configuration** 标签页中，输入 Docker Hub 用户名和个人访问令牌（PAT）。
1. 在 MCP Toolkit 的 **Clients** 标签页中，确保 Gordon 已连接。
1. 从 **Ask Gordon** 菜单中，现在可以发送与 Docker Hub 账户相关的请求，具体内容取决于 Docker Hub MCP 服务器提供的工具。测试时可询问 Gordon：

   ```text
   我的命名空间中有哪些仓库？
   ```

> [!TIP]
> 默认情况下，Gordon [客户端](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#install-an-mcp-client) 已启用，
> 这意味着 Gordon 可以自动与您的 MCP 服务器交互。

## 使用 Claude Desktop 作为客户端

1. 将 Docker Hub MCP 服务器配置添加到您的 `claude_desktop_config.json`：

   {{< tabs >}}
   {{< tab name="仅用于公开仓库">}}

   ```json
   {
     "mcpServers": {
       "docker-hub": {
         "command": "node",
         "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"]
       }
     }
   }
   ```

   其中：
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径

   {{< /tab >}}
   {{< tab name="用于认证访问">}}

   ```json
   {
     "mcpServers": {
       "docker-hub": {
         "command": "node",
         "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio", "--username=YOUR_DOCKER_HUB_USERNAME"],
         "env": {
           "HUB_PAT_TOKEN": "YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN"
         }
       }
     }
   }
   ```

   其中：
   - `YOUR_DOCKER_HUB_USERNAME` 是您的 Docker Hub 用户名。
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径

   {{< /tab >}}
   {{</tabs >}}

1. 保存配置文件，并完全重启 Claude Desktop 以使更改生效。

## 在 Visual Studio Code 中使用

1. 将 Docker Hub MCP 服务器配置添加到 Visual Studio Code 的用户设置（JSON）文件中。您可以通过打开 `Command Palette` 并输入 `Preferences: Open User Settings (JSON)` 来完成此操作。

   {{< tabs >}}
   {{< tab name="仅用于公开仓库">}}

   ```json
   {
     "mcpServers": {
       "docker-hub": {
         "command": "node",
         "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"]
       }
     }
   }
   ```

   其中：
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径

   {{< /tab >}}
   {{< tab name="用于认证访问">}}

   ```json
   {
     "mcpServers": {
       "docker-hub": {
         "command": "node",
         "args": ["/FULL/PATH/TO/YOUR/docker-hub-mcp-server/dist/index.js", "--transport=stdio"],
         "env": {
           "HUB_USERNAME": "YOUR_DOCKER_HUB_USERNAME",
           "HUB_PAT_TOKEN": "YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN"
         }
       }
     }
   }
   ```

   其中：
   - `YOUR_DOCKER_HUB_USERNAME` 是您的 Docker Hub 用户名。
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径

   {{< /tab >}}
   {{</tabs >}}

1. 打开 `Command Palette` 并输入 `MCP: List Servers`。
1. 选择 `docker-hub` 并选择 `Start Server`。

## 使用其他客户端

要将 Docker Hub MCP 服务器集成到您自己的开发环境中，请参阅 GitHub 仓库 [`hub-mcp`](https://github.com/docker/hub-mcp) 上的源代码和安装说明。

## 使用示例

本节提供 Docker Hub 工具常见操作的任务导向示例。

### 查找镜像

```console
# 搜索官方镜像
$ docker ai "在 Docker Hub 上搜索官方 nginx 镜像"

# 搜索轻量级镜像以减少部署大小并提高性能
$ docker ai "搜索占用空间小的最小 Node.js 镜像"

# 获取基础镜像的最新标签
$ docker ai "向我展示 go 的最新标签详情"

# 查找具有企业功能和可靠性的生产就绪数据库
$ docker ai "搜索生产就绪的数据库镜像"

# 比较 Ubuntu 版本以选择适合项目的版本
$ docker ai "帮我找到适合我项目的 Ubuntu 版本"
```

### 仓库管理

```console
# 创建仓库
$ docker ai "在我的命名空间中创建一个仓库"

# 列出我命名空间中的所有仓库
$ docker ai "列出我命名空间中的所有仓库"

# 找到我命名空间中最大的仓库
$ docker ai "我的哪个仓库占用空间最多？"

# 找到最近未更新的仓库
$ docker ai "我的哪些仓库在过去 60 天内没有推送过？"

# 找到当前活跃并正在使用的仓库
$ docker ai "向我展示我最近更新的仓库"

# 获取仓库详情
$ docker ai "向我展示我的 '<repository-name>' 仓库的信息"
```

### 拉取/推送镜像

```console
# 拉取最新 PostgreSQL 版本
$ docker ai "拉取最新的 postgres 镜像"

# 将镜像推送到您的 Docker Hub 仓库
$ docker ai "将我的 <image-name> 推送到我的 <repository-name> 仓库"
```

### 标签管理

```console
# 列出仓库的所有标签
$ $ docker ai "向我展示我的 '<repository-name>' 仓库的所有标签"

# 找到最近推送的标签
$ docker ai "我的 '<repository-name>' 仓库最近推送的标签是什么？"

# 列出支持特定架构的标签
$ docker ai "列出 '<repository-name>' 仓库中支持 amd64 架构的标签"

# 获取特定标签的详细信息
$ docker ai "向我展示 '<repository-name>' 仓库中 '<tag-name>' 标签的详情"

# 检查特定标签是否存在
$ docker ai "检查 'v1.2.0' 版本是否存在于我的 'my-web-app' 仓库中"
```

### Docker Hardened Images

```console
# 列出可用的 Hardened Images
$ docker ai "运行 Node.js 应用程序，最安全的镜像是什么？"

# 将 Dockerfile 更新为使用 Hardened Image
$ docker ai "你能帮我更新 Dockerfile，使用 Docker Hardened Image 替换当前镜像吗"
```
> [!NOTE]
> 访问 Docker Hardened Images 需要订阅。如果您有兴趣使用 Docker Hardened Images，请访问 [Docker Hardened Images](https://www.docker.com/products/hardened-images/)。

## 参考

本节提供 Docker Hub MCP 服务器中可用工具的完整列表。

### Docker Hub MCP 服务器工具

用于与您的 Docker 仓库交互并在 Docker Hub 上发现内容的工具。

| 名称 | 描述 |
|------|-------------|
| `check-repository` | 检查仓库 |
| `check-repository-tag` | 检查仓库标签 |
| `check-repository-tags` | 检查仓库标签 |
| `create-repository` | 创建新仓库 |
| `docker-hardened-images` | 列出指定命名空间中可用的 [Docker Hardened Images](https://www.docker.com/products/hardened-images/) |
| `get-namespaces` | 获取用户的组织/命名空间 |
| `get-repository-dockerfile` | 获取仓库的 Dockerfile |
| `get-repository-info` | 获取仓库信息 |
| `list-repositories-by-namespace` | 列出命名空间下的仓库 |
| `list-repository-tags` | 列出仓库标签 |
| `read-repository-tag` | 读取仓库标签 |
| `search` | 在 Docker Hub 上搜索内容 |
| `set-repository-dockerfile` | 设置仓库的 Dockerfile |
| `update-repository-info` | 更新仓库信息 |