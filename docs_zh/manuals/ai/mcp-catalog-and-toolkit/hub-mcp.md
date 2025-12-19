---
title: Docker Hub MCP 服务器
linkTitle: Hub MCP 服务器
description: Docker Hub MCP 服务器使 LLM 能够访问 Docker Hub 镜像元数据，以实现内容发现。
keywords: Docker Hub MCP Server, Hub MCP server, Hub MCP
weight: 60
---

Docker Hub MCP 服务器是一个模型上下文协议（MCP）服务器，它通过 Docker Hub API 接口，使 LLM 能够访问丰富的镜像元数据，从而实现智能内容发现和仓库管理。

有关 MCP 概念以及 MCP 服务器工作原理的更多信息，请参阅 [Docker MCP 目录和工具包](index.md) 概述页面。

## 关键特性

- **高级 LLM 上下文**：Docker 的 MCP 服务器为 LLM 提供关于 Docker Hub 镜像的详细、结构化上下文，从而为开发人员提供更智能、更相关的建议，无论他们是选择基础镜像还是自动化 CI/CD 工作流。
- **自然语言镜像发现**：开发人员可以使用自然语言找到合适的容器镜像，无需记住标签或仓库名称。只需描述您的需求，Docker Hub 就会返回符合您意图的镜像。
- **简化的仓库管理**：Hub MCP 服务器使代理（Agent）能够通过自然语言管理仓库，快速轻松地获取镜像详情、查看统计信息、搜索内容并执行关键操作。

## 安装 Docker Hub MCP 服务器

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog** 选项卡，搜索 **Docker Hub**，然后选择加号图标以添加 Docker Hub MCP 服务器。
2. 在服务器的 **Configuration** 选项卡中，插入您的 Docker Hub 用户名和个人访问令牌（PAT）。
3. 在 MCP Toolkit 的 **Clients** 选项卡中，确保 Gordon 已连接。
4. 从 **Ask Gordon** 菜单中，您现在可以根据 Docker Hub MCP 服务器提供的工具，发送与您的 Docker Hub 账户相关的请求。要进行测试，请询问 Gordon：

   ```text
   What repositories are in my namespace?
   ```

> [!TIP]
> 默认情况下，Gordon [客户端](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#install-an-mcp-client) 是启用的，
> 这意味着 Gordon 可以自动与您的 MCP 服务器交互。

## 使用 Claude Desktop 作为客户端

1. 将 Docker Hub MCP 服务器配置添加到您的 `claude_desktop_config.json`：

   {{< tabs >}}
   {{< tab name="仅用于公共仓库">}}

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
   {{< tab name="用于需要身份验证的访问">}}

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
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌。
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径。

   {{< /tab >}}
   {{< /tabs >}}

2. 保存配置文件并完全重启 Claude Desktop 以使更改生效。

## 在 Visual Studio Code 中使用

1. 将 Docker Hub MCP 服务器配置添加到 Visual Studio Code 的用户设置（JSON）文件中。您可以通过打开 `命令面板` 并输入 `Preferences: Open User Settings (JSON)` 来完成此操作。

   {{< tabs >}}
   {{< tab name="仅用于公共仓库">}}

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
   {{< tab name="用于需要身份验证的访问">}}

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
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌。
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是您克隆仓库的完整路径。

   {{< /tab >}}
   {{< /tabs >}}

2. 打开 `命令面板` 并输入 `MCP: List Servers`。
3. 选择 `docker-hub`，然后选择 `Start Server`。

## 使用其他客户端

要将 Docker Hub MCP 服务器集成到您自己的开发环境中，请参阅 [`hub-mcp` GitHub 仓库](https://github.com/docker/hub-mcp) 上的源代码和安装说明。

## 使用示例

本节提供针对常见 Docker Hub 工具操作的任务导向示例。

### 查找镜像

```console
# 搜索官方镜像
$ docker ai "Search for official nginx images on Docker Hub"

# 搜索轻量级镜像以减小部署大小并提高性能
$ docker ai "Search for minimal Node.js images with small footprint"

# 获取基础镜像的最新标签
$ docker ai "Show me the latest tag details for go"

# 查找具有企业功能和可靠性的生产就绪数据库
$ docker ai "Search for production ready database images"

# 比较 Ubuntu 版本以为我的项目选择合适的版本
$ docker ai "Help me find the right Ubuntu version for my project"
```

### 仓库管理

```console
# 创建仓库
$ docker ai "Create a repository in my namespace"

# 列出我命名空间中的所有仓库
$ docker ai "List all repositories in my namespace"

# 查找我命名空间中最大的仓库
$ docker ai "Which of my repositories takes up the most space?"

# 查找最近未更新的仓库
$ docker ai "Which of my repositories haven't had any pushes in the last 60 days?"

# 查找当前活跃且正在使用的仓库
$ docker ai "Show me my most recently updated repositories"

# 获取仓库的详细信息
$ docker ai "Show me information about my '<repository-name>' repository"
```

### 拉取/推送镜像

```console
# 拉取最新版本的 PostgreSQL
$ docker ai "Pull the latest postgres image"

# 将镜像推送到您的 Docker Hub 仓库
$ docker ai "Push my <image-name> to my <repository-name> repository"
```

### 标签管理

```console
# 列出仓库的所有标签
$ docker ai "Show me all tags for my '<repository-name>' repository"

# 查找最近推送的标签
$ docker ai "What's the most recent tag pushed to my '<repository-name>' repository?"

# 列出支持架构筛选的标签
$ docker ai "List tags for in the '<repository-name>' repository that support amd64 architecture"

# 获取特定标签的详细信息
$ docker ai "Show me details about the '<tag-name>' tag in the '<repository-name>' repository"

# 检查特定标签是否存在
$ docker ai "Check if version 'v1.2.0' exists for my 'my-web-app' repository"
```

### Docker 强化镜像

```console
# 列出可用的强化镜像
$ docker ai "What is the most secure image I can use to run a node.js application?"

# 将 Dockerfile 转换为使用强化镜像
$ docker ai "Can you help me update my Dockerfile to use a docker hardened image instead of the current one"
```
> [!NOTE]
> 要访问 Docker 强化镜像，需要订阅。如果您有兴趣使用 Docker 强化镜像，请访问 [Docker 强化镜像](https://www.docker.com/products/hardened-images/)。

## 参考

本节提供您可以在 Docker Hub MCP 服务器中找到的工具的综合列表。

### Docker Hub MCP 服务器工具

用于与您的 Docker 仓库交互并发现 Docker Hub 上内容的工具。

| 名称 | 描述 |
|------|-------------|
| `check-repository` | 检查仓库 |
| `check-repository-tag` | 检查仓库标签 |
| `check-repository-tags` | 检查仓库标签 |
| `create-repository` | 创建新仓库 |
| `docker-hardened-images` | 列出指定命名空间中可用的 [Docker 强化镜像](https://www.docker.com/products/hardened-images/) |
| `get-namespaces` | 获取用户的组织/命名空间 |
| `get-repository-dockerfile` | 获取仓库的 Dockerfile |
| `get-repository-info` | 获取仓库信息 |
| `list-repositories-by-namespace` | 列出命名空间下的仓库 |
| `list-repository-tags` | 列出仓库标签 |
| `read-repository-tag` | 读取仓库标签 |
| `search` | 在 Docker Hub 上搜索内容 |
| `set-repository-dockerfile` | 为仓库设置 Dockerfile |
| `update-repository-info` | 更新仓库信息 |