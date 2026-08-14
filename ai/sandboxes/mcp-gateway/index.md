# MCP gateway


Docker Sandboxes 包含一个 MCP 网关，用于将 agent 连接到 Model Context Protocol 服务器。该网关
为沙箱内的 agent 提供一个 MCP 端点，而 `sbx` 在宿主机上管理已注册的服务器、OAuth 凭据和沙箱
生命周期。

这与直接在 Claude Code 等 agent 中配置 MCP 服务器不同。直接 MCP 设置配置的是该 agent 自己的
MCP 客户端。而使用 Docker Sandboxes，你在宿主机上注册一次 MCP 服务器，沙箱网关将它们暴露给
隔离沙箱内受支持的 agent。那个宿主管理的网关为凭据、显式服务器加载、实时更新和组织治理提供了
单一路径。

> [!NOTE]
> Docker Sandboxes 的 MCP 网关与 Docker Desktop MCP Toolkit 是分开的。使用 `sbx mcp` 不需要
> Docker Desktop MCP Toolkit，MCP Toolkit 的服务器设置也不与 Docker Sandboxes 共享。

## 先决条件

- 用 `sbx login` 登录。
- 使用在启动时配置 MCP 的 agent 集成：Claude Code、Codex、Gemini、Kiro 或 OpenCode。
- 对于需要 OAuth 但不支持动态客户端注册的远程服务器，请向服务器提供方注册一个 OAuth 客户端。
- 对于解析到 OCI 包的 `--local --url` 注册，请使用已安装并运行 Docker 的宿主机。显式的
  `--command docker ...` 注册也需要 Docker。

## 快速开始

先从在宿主机上注册一个 MCP 服务器开始：

```console
$ sbx mcp add notion --url https://mcp.notion.com/mcp
```

如果服务器需要 OAuth，`sbx` 在存储注册前会打开一个授权流程。注册后，验证服务器已注册：

```console
$ sbx mcp ls
NAME                 TYPE     URL/COMMAND
notion               remote   https://mcp.notion.com/mcp
```

然后启动一个沙箱并暴露已注册的服务器：

```console
$ sbx run claude --name mcp-demo --static-mcp notion
```

沙箱以 MCP 网关启动，并预加载 `notion` 服务器。注册保留在宿主机上，可被其他沙箱复用。

## 注册一个 MCP 服务器

`sbx mcp add` 按名称注册一个 MCP 服务器。注册将服务器定义记录在宿主机上。它本身不会将服务器
附加到沙箱。要暴露已注册的服务器给沙箱，请在创建沙箱时用
[`--static-mcp`](#use-static-mode) 传入它，或对已在运行的沙箱使用
[`sbx mcp load`](#add-a-server-to-a-running-sandbox)。

服务器名称可以包含字母、数字、点、连字符和下划线。

`--url` 标志可以指向不同类型的输入。执行位置取决于你注册的内容：

- 远程端点 URL 标识一个运行中的 MCP 服务器。服务器在远程运行，沙箱网关连接到它。
- 带 `--local` 的元数据 URL 返回一个注册项、`server.json` 或 `server.yaml`，描述一个使用 OCI
  打包的 stdio 服务器。`sbx` 解析镜像并用 Docker 在宿主机上运行它。
- 显式命令作为 stdio MCP 服务器在宿主机上运行。

本地 stdio 服务器在宿主机上运行，而非沙箱内。沙箱内的 agent 只连接到 MCP 网关。

### 远程端点 URL

对于远程 MCP 端点，传入服务器 URL：

```console
$ sbx mcp add notion --url https://mcp.notion.com/mcp
$ sbx mcp add linear --url https://mcp.linear.app/mcp
```

### 本地 stdio 服务器

某些 MCP 服务器通过 stdio 通信，而不是暴露远程 HTTP 端点。当 `sbx` 应在宿主机上启动 MCP 服务器
时，使用本地 stdio 服务器。你可以提供元数据 URL 或显式命令。

#### 从注册表或清单元数据

当你有一个 MCP 社区注册表 URL，或一个返回 `server.json` 或 `server.yaml` 文档的 URL 时，使用
`--local --url`。注册项或清单必须描述一个使用 stdio 传输的 OCI 包。`sbx` 不会从元数据启动非
OCI 包类型，例如 `npm`。要使用这些服务器，请注册一个显式命令。

此路径从元数据解析镜像，并用 Docker 在宿主机上启动它，因此宿主机必须已安装并运行 Docker。

```console
$ sbx mcp add fetch --local \
  --url https://registry.modelcontextprotocol.io/v0/servers/fetch-mcp/versions/latest
```

如果注册项没有发布 OCI stdio 包，`sbx` 会拒绝注册，而不是在本地启动它。

服务器清单描述 MCP 服务器包以及如何启动它。它可以托管在 GitHub raw URL、内部 HTTP 服务器或
CDN 上。

```console
$ sbx mcp add opine --local --url https://example.com/mcp/opine/server.yaml
```

#### 从显式命令

当你已经知道可执行文件和参数，或需要自定义 Docker 标志时，使用 `--command`。该命令可以是包运行
器如 `npx`，或 Docker 容器命令：

```console
$ sbx mcp add playwright --command npx --args @playwright/mcp@latest
$ sbx mcp add local-image-server --command docker \
  --args "run,-i,--rm,your/image"
```

要为宿主进程设置工作目录，传入 `--dir`。该标志仅对 `--command` 有效：

```console
$ sbx mcp add local-fs --command node --args server.js --dir /srv/data
```

当你有已发布的服务器定义且不需要自定义 `docker run` 时，使用注册表或清单元数据。对本地开发、
私有服务器或自定义容器标志使用 `--command`。

> [!WARNING]
> 本地 stdio 服务器在宿主机上运行，在沙箱隔离之外。如果命令启动一个 Docker 容器，该容器使用
> 宿主 Docker 隔离，而非沙箱隔离。该进程或容器可以访问宿主文件、宿主网络资源，以及提供给它的
> 凭据。使用受信任的命令和镜像，除非服务器需要，否则避免挂载宿主路径或传递凭据。

## 为基于 OAuth 的服务器授权

如果已注册的远程服务器需要 OAuth，`sbx mcp add` 默认启动授权流程：

```console
$ sbx mcp add notion --url https://mcp.notion.com/mcp
Resolving MCP server "notion"...
Open this URL to authorize MCP server "notion":
https://api.notion.com/v1/oauth/authorize?...
MCP server "notion" authorized
MCP server "notion" registered (type: remote)
```

OAuth 凭据保留在宿主机上。在本地网关模式下，`sbx` 将 token 存储在宿主操作系统的凭据存储中。

要注册一个基于 OAuth 的服务器而不授权它，传入 `--skip_auth`：

```console
$ sbx mcp add notion --url https://mcp.notion.com/mcp --skip_auth
```

### 使用预注册的 OAuth 客户端

在本地网关模式下，你可以注册一个不支持动态客户端注册的远程 OAuth 服务器。如果服务器发布了
OAuth 元数据，传入你向服务器提供方注册的客户端 ID：

```console
$ sbx mcp add slack --url https://slack.example.com/mcp \
  --client-id <CLIENT_ID>
```

如果服务器没有发布 OAuth 元数据，传入 `--oauth-authorization-server` 以及客户端 ID。该标志接受
本地文件路径，或指向 RFC 8414 授权服务器元数据文档的 HTTP 或 HTTPS URL。该文档必须定义
`authorization_endpoint` 和 `token_endpoint`：

```console
$ sbx mcp add serverx --url https://mcp.serverx.example/mcp \
  --oauth-authorization-server ./serverx-authorization-server.json \
  --client-id <CLIENT_ID>
```

这些标志仅对 `--url` 有效。

对于机密 OAuth 客户端，请在注册服务器之前存储客户端密钥。没有 `--client-secret` 标志：

```console
$ sbx secret set mcp:slack.client_secret
$ sbx mcp add slack --url https://slack.example.com/mcp \
  --client-id <CLIENT_ID>
```

客户端密钥保留在加密的宿主凭据存储中，不会写入 MCP 注册。如果服务器需要机密客户端但没存储
密钥，注册会成功但跳过授权。存储密钥后，运行 `sbx mcp auth <server>`。

### 设置 OAuth 作用域

使用可重复的 `--scope` 标志记录授权期间请求的默认作用域：

```console
$ sbx mcp add serverx --url https://mcp.serverx.example/mcp \
  --scope read --scope write
```

`sbx mcp auth` 命令也接受 `--scope` 以覆盖一次授权的已记录默认值。如果授权服务器通告了受支持的
作用域，每个请求的作用域都必须在该集合中。

对于暴露给沙箱的每个基于 OAuth 的远程服务器，网关暴露一个名为 `<server>-authorize` 的辅助工具，
例如 `notion-authorize`。agent 可以调用该工具来授权或重新授权服务器。如果服务器未授权，该辅助
工具是该服务器暴露的唯一工具。

你可以从宿主机管理 OAuth 凭据：

```console
$ sbx mcp auth status notion
$ sbx mcp auth notion
$ sbx mcp auth rm notion
```

使用 `--all` 将 `auth`、`auth status` 或 `auth rm` 应用到所有已注册的基于 OAuth 的服务器。使用
`--format=json` 获得机器可读输出。

## 选择 MCP 模式

每个沙箱都会启动一个 MCP 网关。当沙箱启动时，受支持的 agent 集成读取网关 URL 并向 agent 注册
它。

你是否在创建沙箱时传入 `--static-mcp` 决定了它的 MCP 模式：

- 静态模式预加载指定的服务器，并且不向 agent 暴露动态发现工具。
- 动态模式不预加载任何服务器，并让 agent 查找并附加已注册的服务器。

此选择在沙箱重启期间保留。

### 使用静态模式

传入 `--static-mcp` 以预加载已注册的 MCP 服务器：

```console
$ sbx mcp add notion --url https://mcp.notion.com/mcp
$ sbx mcp add linear --url https://mcp.linear.app/mcp
$ sbx run claude --name my-session --static-mcp notion,linear
```

你可以将 `--static-mcp` 作为逗号分隔的列表传入，或重复该标志：

```console
$ sbx run claude --name my-session \
  --static-mcp notion --static-mcp linear
```

静态集合中的每个名称必须已经用 `sbx mcp add` 注册。网关不向 agent 暴露 `mcp-find`、
`mcp-add` 或 `mcp-config-set`。

当重新连接到已有沙箱时，你无法通过传入 `--static-mcp` 替换初始集合。要从宿主机附加另一个
服务器，请使用 [`sbx mcp load`](#add-a-server-to-a-running-sandbox)。

### 使用动态模式

省略 `--static-mcp` 以使用动态模式。网关不预加载任何服务器，并向 agent 暴露 `mcp-find`、
`mcp-add` 和 `mcp-config-set`。agent 可以在会话期间搜索已注册的服务器目录并附加服务器。

如果你在动态沙箱启动后运行 `sbx mcp add`，其网关会刷新可搜索的目录。agent 然后可以在不重启的
情况下找到并附加新注册。`sbx mcp add` 命令本身不会附加服务器。

## 向运行中的沙箱添加服务器

要将已注册的服务器附加到运行中的沙箱，请使用 `sbx mcp load`。这在静态和动态模式下都有效：

```console
$ sbx mcp add linear --url https://mcp.linear.app/mcp
$ sbx mcp load linear --sandbox my-session
MCP server "linear" loaded into sandbox "my-session" (live)
```

已连接的 agent 会话会收到工具列表更新，因此添加的工具无需重新连接即可可见。加载的服务器在
沙箱重启期间保持附加。

## 内置网关工具

本地 MCP 网关暴露一小部分内置工具。这些工具属于网关本身，而非某个已注册的 MCP 服务器。agent
可以在与服务器工具相同的 MCP 连接上看到并调用它们，因此它们可能出现在 agent 工具列表、日志、
策略决策、审计日志或审批提示中。

你不需要为正常设置直接调用这些工具。使用 `sbx mcp` 命令从宿主机注册服务器并管理凭据。这些工具
很重要，因为 agent 可以在会话期间调用它们，而管理员可以独立于已注册 MCP 服务器提供的工具来治理
它们。

| Tool                 | Description                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `mcp-exec`           | Executes a tool by name through the gateway.                                               |
| `code-mode`          | Creates an ephemeral JavaScript tool that can call selected tools through the MCP gateway. |
| `mcp-find`           | Searches the registered server catalog without changing sandbox state. Dynamic mode only.  |
| `mcp-add`            | Attaches a registered server to the sandbox. Dynamic mode only.                            |
| `mcp-config-set`     | Sets per-session configuration overrides for an attached server. Dynamic mode only.        |
| `<server>-authorize` | Starts or restarts OAuth authorization for an exposed OAuth-backed remote server.          |

用 `mcp-add` 附加的服务器在沙箱重启期间保持附加。网关为基于 OAuth 的远程服务器暴露
`<server>-authorize`，即使它们已有有效 token。本地 stdio 服务器不暴露此辅助工具。如果 `code-mode`
创建了生成的工具，该工具由连接到沙箱网关的客户端共享，并在网关被替换或停止时消失。

在 MCP 访问策略中，内置网关工具是 `MCP::Primordial` 资源，并使用 `invokePrimordial` 动作。来自已
注册 MCP 服务器的工具是 `MCP::Tool` 资源，并使用 `invokeTool` 动作。详情请参阅
[MCP 策略参考](governance/reference/mcp-policy.md)。

## 管理注册

列出已注册的服务器：

```console
$ sbx mcp ls
```

检查已注册的服务器：

```console
$ sbx mcp inspect notion
```

移除已注册的服务器：

```console
$ sbx mcp rm notion
```

对于基于 OAuth 的服务器，`sbx mcp rm` 在移除服务器注册前先移除 OAuth 访问 token。预注册的 OAuth
客户端的客户端密钥及其身份绑定保留在宿主凭据存储中，因此当你重新添加相同客户端时可以复用它们。
该命令会打印用于移除它们的 `sbx secret rm` 命令。要仅移除 OAuth 访问 token，请使用
`sbx mcp auth rm`。

## 治理

拥有 AI Governance 的组织可以使用
[MCP 访问策略](governance/access-controls/mcp.md) 来控制 MCP 服务器注册、工具调用、网关元工具、
资源、提示和审批要求。MCP 访问策略是用 Cedar 编写的组织策略。

