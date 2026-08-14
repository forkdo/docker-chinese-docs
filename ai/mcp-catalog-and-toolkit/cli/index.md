# 从 CLI 使用 MCP Toolkit




> [!NOTE]
> 此处记录的 `docker mcp` 命令在 Docker Desktop 4.62 及更高版本中可用。较早的版本可能不支持所展示的全部命令。

`docker mcp` 命令让你可以在终端中管理 MCP 配置文件、服务器、OAuth 凭据和目录。可将 CLI 用于脚本编写、自动化以及无界面环境。

## 配置文件（Profiles）

### 创建配置文件

```console
$ docker mcp profile create --name <profile-id>
```

配置文件 ID 用于在后续命令中引用该配置文件：

```console
$ docker mcp profile create --name web-dev
```

### 列出配置文件

```console
$ docker mcp profile list
```

### 查看配置文件

```console
$ docker mcp profile show <profile-id>
```

### 移除配置文件

```console
$ docker mcp profile remove <profile-id>
```

> [!CAUTION]
> 移除配置文件会删除其所有服务器配置和设置。此操作无法撤销。

## 服务器（Servers）

### 浏览目录

列出可用服务器及其 ID：

```console
$ docker mcp catalog server ls mcp/docker-mcp-catalog
```

输出会按名称列出每个服务器。该名称（例如 `playwright` 或 `github-official`）即为在 `catalog://` URI 中使用的服务器 ID。

要在 Docker Desktop 中查找服务器 ID，请打开 **MCP Toolkit** > **Catalog**，选择一个服务器，然后查看 **Server ID** 字段。

### Add servers to a profile（将服务器添加到配置文件）

服务器通过 URI 引用。URI 格式取决于服务器的来源：

| 格式                                  | 来源                 |
| ------------------------------------- | -------------------- |
| `catalog://<catalog-ref>/<server-id>` | OCI 目录             |
| `docker://<image>:<tag>`              | Docker 镜像          |
| `https://<url>/v0/servers/<uuid>`     | MCP 社区注册中心     |
| `file://<path>`                       | 本地 YAML 或 JSON 文件 |

最常用的格式是 `catalog://`，其中 `<catalog-ref>` 对应 **Catalog** 字段，`<server-id>` 对应 Docker Desktop 中显示或 `catalog server ls` 输出中的 **Server ID** 字段：

```console
$ docker mcp profile server add <profile-id> \
  --server catalog://<catalog-ref>/<server-id>
```

在一条命令中添加多个服务器：

```console
$ docker mcp profile server add web-dev \
  --server catalog://mcp/docker-mcp-catalog/github-official \
  --server catalog://mcp/docker-mcp-catalog/playwright
```

添加在本地 YAML 文件中定义的服务器：

```console
$ docker mcp profile server add my-profile \
  --server file://./my-server.yaml
```

该 YAML 文件定义服务器镜像和配置：

```yaml
name: my-server
title: My Server
type: server
image: myimage:latest
description: Description of the server
```

如果服务器需要 OAuth 身份验证，请在添加后于 Docker Desktop 中进行授权。参见 [OAuth authentication](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md#oauth-authentication)。

### 列出服务器

列出所有配置文件中的全部服务器：

```console
$ docker mcp profile server ls
```

按配置文件过滤：

```console
$ docker mcp profile server ls --filter profile=web-dev
```

### 移除服务器

```console
$ docker mcp profile server remove <profile-id> --name <server-name>
```

一次移除多个服务器：

```console
$ docker mcp profile server remove web-dev \
  --name github-official \
  --name playwright
```

### 配置服务器设置

为配置文件中的服务器设置和获取配置值：

```console
$ docker mcp profile config <profile-id> --set <server-id>.<key>=<value>
$ docker mcp profile config <profile-id> --get-all
$ docker mcp profile config <profile-id> --del <server-id>.<key>
```

服务器的配置键及其期望值由各个服务器自行定义。请查看服务器的文档，或在 Docker Desktop 中的 **MCP Toolkit** > **Catalog** > **Configuration** 下查看其条目。

## 网关（Gateway）

使用指定配置文件运行 MCP Gateway：

```console
$ docker mcp gateway run --profile <profile-id>
```

省略 `--profile` 则使用默认配置文件。

### 手动连接客户端

要连接 Docker Desktop 中未列出的任意客户端，请将其配置为通过 `stdio` 运行网关。例如，在基于 JSON 的客户端配置中：

```json
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "web-dev"],
      "type": "stdio"
    }
  }
}
```

对于 Claude Desktop，格式为：

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "web-dev"]
    }
  }
}
```

### 连接已命名的客户端

将受支持的客户端连接到配置文件：

```console
$ docker mcp client connect <client> --profile <profile-id>
```

例如，将 VS Code 连接到某个项目专用配置文件：

```console
$ docker mcp client connect vscode --profile my-project
```

这会在当前目录中创建 `.vscode/mcp.json` 文件。由于这是用户专用文件，请将其加入 `.gitignore`：

```console
$ echo ".vscode/mcp.json" >> .gitignore
```

## 共享配置文件

使用 OCI 注册表或版本控制与团队共享配置文件。

### 通过 OCI 注册表共享

配置文件以 OCI 制品形式通过任何兼容 OCI 的注册表共享。出于安全原因，其中不包含凭据。团队成员在拉取后需单独配置身份验证凭据。

将名为 `web-dev` 的现有配置文件推送到 OCI 注册表：

```console
$ docker mcp profile push web-dev registry.example.com/profiles/web-dev:v1
```

拉取同一配置文件：

```console
$ docker mcp profile pull registry.example.com/profiles/team-standard:latest
```

### 通过版本控制共享

对于项目专用配置文件，你可以使用 `export` 和 `import` 命令，并将配置文件与代码一起存储在版本控制中。团队成员可以导入该文件以获得相同的配置。

将配置文件导出到你的项目目录：

```console
$ mkdir -p .docker
$ docker mcp profile export web-dev .docker/mcp-profile.json
```

克隆仓库的团队成员可以导入该配置文件：

```console
$ docker mcp profile import .docker/mcp-profile.json
```

这会创建一个包含文件中所定义服务器和配置的配置文件。如有需要，任何身份验证凭据都必须单独配置。

## Custom catalogs（自定义目录）

自定义目录让你能为团队或组织精心整理出聚焦的服务器集合。有关自定义目录是什么以及何时使用的概述，参见[自定义目录](/manuals/ai/mcp-catalog-and-toolkit/catalog.md#custom-catalogs)。

目录通过 OCI 引用来标识，例如 `registry.example.com/mcp/my-catalog:latest`。目录中的服务器使用与[将服务器添加到配置文件](#add-servers-to-a-profile)时相同的 URI 方案。

### 定制 Docker 目录

以 Docker 目录为基础，然后添加或移除服务器以符合组织的需要。首先复制它：

```console
$ docker mcp catalog tag mcp/docker-mcp-catalog \
  registry.example.com/mcp/company-tools:latest
```

列出其中包含的服务器：

```console
$ docker mcp catalog server ls registry.example.com/mcp/company-tools:latest
```

移除组织未批准的服务器：

```console
$ docker mcp catalog server remove \
  registry.example.com/mcp/company-tools:latest \
  --name <server-name>
```

添加你自己打包为 Docker 镜像的私有服务器：

```console
$ docker mcp catalog server add registry.example.com/mcp/company-tools:latest \
  --server docker://registry.example.com/mcp/internal-api:latest \
  --server docker://registry.example.com/mcp/data-pipeline:latest
```

准备就绪后推送：

```console
$ docker mcp catalog push registry.example.com/mcp/company-tools:latest
```

### 从零构建目录

若只想精确包含你所选择的内容而不含其他，可从零创建目录。你可以包含 Docker 目录中的服务器、你自己的私有镜像，或两者兼有。

创建目录并指定要包含哪些服务器：

```console
$ docker mcp catalog create registry.example.com/mcp/data-tools:latest \
  --title "Data Analysis Tools" \
  --server catalog://mcp/docker-mcp-catalog/sequentialthinking \
  --server catalog://mcp/docker-mcp-catalog/brave \
  --server docker://registry.example.com/mcp/analytics:latest
```

查看结果：

```console
$ docker mcp catalog show registry.example.com/mcp/data-tools:latest
```

推送以进行分发：

```console
$ docker mcp catalog push registry.example.com/mcp/data-tools:latest
```

### 分发目录

推送你的目录，以便团队成员导入：

```console
$ docker mcp catalog push <oci-reference>
```

团队成员可以使用 CLI 拉取：

```console
$ docker mcp catalog pull <oci-reference>
```

或使用 Docker Desktop 导入：选择 **MCP Toolkit** > **Catalog** > **Import catalog**，然后输入 OCI 引用。

### 在网关中使用自定义目录

使用你的目录（而非默认的 Docker 目录）运行网关：

```console
$ docker mcp gateway run --catalog <oci-reference>
```

对于 [Dynamic MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)（智能体在对话过程中发现并添加服务器），这会把智能体能找到的范围限制在你精选的集合内。

若不使用配置文件而直接启用目录中的特定服务器：

```console
$ docker mcp gateway run --catalog <oci-reference> \
  --servers <name1> --servers <name2>
```

## 延伸阅读

- [开始使用 MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/get-started.md)
- [MCP Profiles](/manuals/ai/mcp-catalog-and-toolkit/profiles.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)

