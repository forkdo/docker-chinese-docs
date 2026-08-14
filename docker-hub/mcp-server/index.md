# Docker Hub MCP server


Docker Hub MCP 服务器是一个模型上下文协议（MCP）服务器，它与 Docker Hub API 对接，让大语言模型（LLM）能够访问丰富的镜像元数据，从而实现智能的内容发现与仓库管理。

有关 MCP 概念以及 MCP 服务器如何工作的更多信息，请参阅 [Docker MCP Catalog and Toolkit](/ai/mcp-catalog-and-toolkit/) 概述页面。

## 主要功能（Key features）

- 增强的 LLM 上下文：Docker 的 MCP 服务器为 LLM 提供 Docker Hub 镜像的详细、结构化上下文，无论开发者是在选择基础镜像还是自动化 CI/CD 工作流，都能给出更智能、更贴合需求的推荐。
- 自然语言镜像发现：开发者可以使用自然语言找到合适的容器镜像，无需记住标签或仓库名称。只需描述你的需求，Docker Hub 就会返回符合你意图的镜像。
- 简化的仓库管理：Hub MCP 服务器让代理（agent）能够通过自然语言管理仓库，获取镜像详情、查看统计数据、搜索内容，并快速轻松地执行关键操作。

## 安装 Docker Hub MCP 服务器

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Profiles** 选项卡，接着选择 **Create profile** 创建一个新的配置文件，或者选择一个已有的配置文件来使用。
2. 选择 **Catalog** 选项卡，搜索 **Docker Hub**，然后选择 **Add to** 将其添加到你的配置文件中。
3. 选择 **Profiles** 选项卡，选择你添加了 Docker Hub 的配置文件，然后选择 Docker Hub MCP 服务器上的配置图标。输入你的 Docker Hub 用户名和个人访问令牌（PAT）。
4. 在同一配置文件的 **Clients** 部分，如果你已经连接了某个客户端，它会自动连接。否则，选择加号图标来添加一个客户端。

有关设置配置文件和连接客户端的更多细节，请参阅 [Get started with Docker MCP Toolkit](/ai/mcp-catalog-and-toolkit/get-started/)。

## 使用 Claude Desktop 作为客户端

1. 将 Docker Hub MCP 服务器配置添加到你的 `claude_desktop_config.json` 中：

   **For public repositories only**



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

   Where :
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是你克隆该仓库的完整路径

   **For authenticated access**



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

   Where :
   - `YOUR_DOCKER_HUB_USERNAME` 是你的 Docker Hub 用户名。
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是你克隆该仓库的完整路径


   

1. 保存配置文件，并完全重启 Claude Desktop 以使更改生效。

## 与 Visual Studio Code 配合使用

1. 将 Docker Hub MCP 服务器配置添加到 Visual Studio Code 的 User Settings (JSON)（用户设置（JSON））文件中。你可以打开 `Command Palette` 并输入 `Preferences: Open User Settings (JSON)` 来完成此操作。


   **For public repositories only**



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

   Where :
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是你克隆该仓库的完整路径

   **For authenticated access**



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

   Where :
   - `YOUR_DOCKER_HUB_USERNAME` 是你的 Docker Hub 用户名。
   - `YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN` 是 Docker Hub 个人访问令牌
   - `/FULL/PATH/TO/YOUR/docker-hub-mcp-server` 是你克隆该仓库的完整路径


   

1. 打开 `Command Palette` 并输入 `MCP: List Servers`。
1. 选择 `docker-hub` 并选择 `Start Server`。

## 使用其他客户端

要将 Docker Hub MCP 服务器集成到你自己的开发环境中，请参阅 [`hub-mcp` GitHub 仓库](https://github.com/docker/hub-mcp) 上的源代码和安装说明。


## 使用示例

本节提供面向常见 Docker Hub 工具操作的任务型示例。

### 查找镜像（Finding images）


```console
# 搜索官方镜像
$ docker ai "Search for official nginx images on Docker Hub"

# 搜索轻量级镜像，以减小部署体积并提升性能
$ docker ai "Search for minimal Node.js images with small footprint"

# 获取基础镜像的最新标签
$ docker ai "Show me the latest tag details for go"

# 查找具备企业级特性与可靠性的生产就绪数据库
$ docker ai "Search for production ready database images"

# 对比 Ubuntu 版本，为我的项目选择合适的版本
$ docker ai "Help me find the right Ubuntu version for my project"
```

### 仓库管理（Repository management）

```console
# 创建仓库
$ docker ai "Create a repository in my namespace"

# 列出我命名空间下的所有仓库
$ docker ai "List all repositories in my namespace"

# 找出我命名空间中体积最大的仓库
$ docker ai "Which of my repositories takes up the most space?"

# 查找最近未更新的仓库
$ docker ai "Which of my repositories haven't had any pushes in the last 60 days?"

# 查找当前活跃且正在使用的仓库
$ docker ai "Show me my most recently updated repositories"

# 获取某个仓库的详情
$ docker ai "Show me information about my '<repository-name>' repository"
```

### 拉取/推送镜像（Pull/push images）


```console
# 拉取最新版 PostgreSQL
$ docker ai "Pull the latest postgres image"

# 将镜像推送到你的 Docker Hub 仓库
$ docker ai "Push my <image-name> to my <repository-name> repository"
```

### 标签管理（Tag management）

```console
# 列出仓库的所有标签
$ docker ai "Show me all tags for my '<repository-name>' repository"

# 查找最近推送的标签
$ docker ai "What's the most recent tag pushed to my '<repository-name>' repository?"

# 按架构过滤列出标签
$ docker ai "List tags for in the '<repository-name>' repository that support amd64 architecture"

# 获取特定标签的详细信息
$ docker ai "Show me details about the '<tag-name>' tag in the '<repository-name>' repository"

# 检查某个标签是否存在
$ docker ai "Check if version 'v1.2.0' exists for my 'my-web-app' repository"
```

### Docker Hardened Images

```console
# 列出可用的加固镜像
$ docker ai "What is the most secure image I can use to run a node.js application?"

# 将 Dockerfile 转换为使用加固镜像
$ docker ai "Can you help me update my Dockerfile to use a docker hardened image instead of the current one"
```
> [!NOTE]
> 要使用 Docker Hardened Images，需要订阅。如果你有兴趣使用 Docker Hardened Images，请访问 [Docker Hardened Images](https://www.docker.com/products/hardened-images/)。

## 参考（Reference）

本节完整列出了你可以在 Docker Hub MCP 服务器中找到的工具。

### Docker Hub MCP 服务器工具

用于与你的 Docker 仓库交互并发现 Docker Hub 内容的相关工具。

| Name | Description |
|------|-------------|
| `check-repository` | 检查仓库 |
| `check-repository-tag` | 检查仓库标签 |
| `check-repository-tags` | 检查仓库标签列表 |
| `create-repository` | 创建新仓库 |
| `docker-hardened-images` | 列出指定命名空间下可用的 [Docker Hardened Images](https://www.docker.com/products/hardened-images/) |
| `get-namespaces` | 获取用户的组织/命名空间 |
| `get-repository-dockerfile` | 获取仓库的 Dockerfile |
| `get-repository-info` | 获取仓库信息 |
| `list-repositories-by-namespace` | 列出命名空间下的仓库 |
| `list-repository-tags` | 列出仓库标签 |
| `read-repository-tag` | 读取仓库标签 |
| `search` | 在 Docker Hub 上搜索内容 |
| `set-repository-dockerfile` | 设置仓库的 Dockerfile |
| `update-repository-info` | 更新仓库信息 |

