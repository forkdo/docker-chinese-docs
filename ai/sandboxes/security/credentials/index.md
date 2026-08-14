# 

<!-- FILE: manuals/ai/sandboxes/security/credentials.md -->

---
title: 凭据
weight: 20
description: Docker Sandboxes 如何处理沙盒化 agent 的 API 密钥和鉴权凭据。
keywords: docker sandboxes, credentials, api keys, authentication, proxy, ssh agent, secrets
---

大多数 agent 都需要一个用于其模型提供商的 API 密钥。你宿主上的一个 HTTP/HTTPS 代理会拦截来自沙盒的出站请求，在宿主上查找匹配的凭据，并在转发之前覆盖鉴权头部。当代理管理生效时，真实的凭据保留在宿主上；沙盒只看到一个哨兵值（sentinel value）。有关凭据隔离如何融入更广阔的沙盒安全模型，请参阅 [信任边界](_index.md#trust-boundaries)。

## 凭据注入如何工作

当沙盒发出出站请求时，宿主侧代理决定三件事：请求是否**匹配** kit（或内置 agent）声明的某个服务、写入哪个**头部**、以及注入哪个**值**。kit 声明匹配和头部；你在宿主上提供值。对于代理管理的凭据，真实值永远不会进入沙盒——agent 只看到一个像 `proxy-managed` 这样的哨兵值。

一个 kit 可以设置 OAuth `passthrough: true` 来选择退出哨兵遮蔽。这会将真实的令牌响应发送到沙盒中，并降低凭据隔离。请参阅 [`oauth` kit 字段](../customize/kit-reference.md#oauth)。

有多种方式来提供该值。当多个来源对同一服务都有值时，已存储的密钥优先。

| 形式                                                                         | 它是什么                                                   | 在以下情况下使用                                                                                                      |
| --------------------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [已存储的凭据](#stored-secrets) (`sbx secret set`)                        | 位于你的 OS 钥匙串中、以服务为键的值                | 任何内置或 kit 声明服务的默认选择                                                             |
| [自定义凭据](#custom-secrets) (`sbx secret set-custom`)                 | 以域和环境变量为键的值                           | 服务模型不适用——agent 验证变量的格式，或凭据随请求体一起传递                 |
| OAuth                                                                       | 宿主侧登录流程；令牌永不进入沙盒 | agent 支持它，例如 Claude Code、Codex、Cursor 或 Droid                                              |
| [凭据绑定](#credential-bindings) (`credentials.yaml`)            | 每个服务的机制与域审批                        | 第三方 `schemaVersion: "2"` kit 所必需                                                               |
| [注册表凭据](#registry-credentials) (`sbx secret set --registry`) | 用于拉取镜像和 kit 的鉴权                     | 从私有注册表拉取模板或 kit                                                                       |

对于多提供商 agent（OpenCode、Docker Agent），代理根据被调用的 API 端点选择凭据。有关按提供商的详细信息，请参阅各个 [agent 页面](../agents/)。

## 已存储的凭据

`sbx secret set` 将凭据存储在你的 OS 钥匙串中，以服务标识符为键。内置 agent 声明一组固定的服务。自定义 kit 可以声明它们自己的。同一个 `sbx secret set` 流程对两者都适用。

### 凭据存储在哪里

支撑 `sbx secret set` 的存储取决于你的操作系统：

- macOS：系统 Keychain。
- Windows：Windows Credential Manager。
- Linux：你的桌面钥匙串暴露的 Secret Service，例如 GNOME Keyring 或 KDE Wallet。

Ubuntu 软件包依赖于 GNOME Keyring，因此标准的桌面安装无需额外设置。

在没有运行中的 Secret Service 的 Linux 宿主上——无头服务器和一些 WSL 环境——`sbx` 会回退到用户配置目录 `$XDG_CONFIG_HOME/com.docker.sandboxes` 下的一个加密文件，当 `$XDG_CONFIG_HOME` 未设置时，默认为 `~/.config/com.docker.sandboxes`。此回退是自动的，无需配置。当你以这种方式存储凭据时，`sbx` 会打印一条提示：

```text
No keychain detected - this secret will be stored in an encrypted file on disk
```

该文件在静止状态下加密，并受 `0700` 目录权限保护，与 `~/.docker/config.json` 相同。这比 OS 钥匙串弱，而 OS 钥匙串还会按应用程序仲裁访问。如果你稍后在宿主上启动了 Secret Service，`sbx` 会再次将新凭据存储到钥匙串中。有关在没有桌面钥匙串的情况下运行沙盒的更多信息，请参阅 [我可以在无头 Linux 上使用 Docker Sandboxes 吗？](../faq.md#can-i-use-docker-sandboxes-on-headless-linux)

### 存储一个凭据

```console
$ sbx secret set anthropic
```

这会交互式地提示你输入凭据值。服务凭据默认是全局的，因此该凭据对所有沙盒都可用。要将凭据限定到特定沙盒：

```console
$ sbx secret set openai --sandbox my-sandbox
```

> [!NOTE]
> 沙盒级凭据会立即生效，即使沙盒正在运行。全局凭据仅在创建沙盒时适用。如果你在沙盒运行时设置或更改了全局凭据，请重建沙盒以使新值生效。

### 从环境变量导入

如果你已经在 shell 中设置了 API 密钥，`sbx secret import` 会读取它们并将其存储到钥匙串中，而无需手动逐个输入：

```console
$ sbx secret import
```

这会扫描当前会话中下面的[内置服务表](#built-in-services)所包含的环境变量，并在写入前提示你逐一确认。要导入单个服务：

```console
$ sbx secret import openai
```

传递 `--all` 可在不提示的情况下导入所有内容（仅新增条目；现有条目保持不变），或传递 `--force` 覆盖现有条目：

```console
$ sbx secret import --all
$ sbx secret import openai --force
```

传递 `--dry-run` 可预览将要导入的内容而不写入任何东西。之后运行 `sbx secret ls` 确认存储了什么。有关在 CI 中设置凭据的信息，请参阅 [CI 与无头使用](../workflows.md#ci-and-headless-use)。

### 内置服务

每个内置服务名称都映射到 `sbx secret import` 读取的环境变量，以及代理将凭据注入的 API 域：

| 服务        | 环境变量                     | API 域                                                                                                                       |
| ----------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `anthropic`  | `ANTHROPIC_API_KEY`          | `api.anthropic.com`, `console.anthropic.com`, `claude.ai`, `mcp-proxy.anthropic.com`                                          |
| `cursor`     | `CURSOR_API_KEY`             | `api2.cursor.sh`, `api3.cursor.sh`, `repo42.cursor.sh`, `cursor.com`                                                          |
| `droid`      | `FACTORY_API_KEY`            | `api.factory.ai`, `app.factory.ai`, `relay.factory.ai`                                                                        |
| `github`     | `GH_TOKEN`, `GITHUB_TOKEN`   | `api.github.com`, `github.com`, `raw.githubusercontent.com`, `gist.github.com`, `copilot.github.com`, `api.githubcopilot.com` |
| `google`     | `GEMINI_API_KEY`, `GOOGLE_API_KEY` | `generativelanguage.googleapis.com`, `oauth2.googleapis.com`, `aiplatform.googleapis.com`, `vertexai.googleapis.com`          |
| `groq`       | `GROQ_API_KEY`               | `api.groq.com`                                                                                                                |
| `mistral`    | `MISTRAL_API_KEY`            | `api.mistral.ai`                                                                                                              |
| `nebius`     | `NEBIUS_API_KEY`             | `api.studio.nebius.com`, `api.tokenfactory.nebius.com`                                                                        |
| `openai`     | `OPENAI_API_KEY`             | `api.openai.com`, `openai.com`, `chatgpt.com`, `www.chatgpt.com`                                                              |
| `openrouter` | `OPENROUTER_API_KEY`         | `openrouter.ai`                                                                                                               |
| `xai`        | `XAI_API_KEY`                | `api.x.ai`                                                                                                                    |

当你使用 `sbx secret set <service>` 存储凭据时，代理会将其注入到发往所列 API 域的请求中。

### kit 声明的服务

自定义 kit 可以在 `spec.yaml` 中声明它们自己的服务标识符。在 `schemaVersion: "2"` 中，凭据在 `credentials:` 列表下声明：

```yaml
credentials:
  - service: my-service
    apiKey:
      name: MY_SERVICE_TOKEN
      proxyManaged: true
      inject:
        - domain: api.my-service.com
          scheme: bearer
```

每个服务声明 `apiKey`、`oauth` 或两者。当两者在运行时都解析时，API 密钥优先，OAuth 作为后备。要提供凭据值，请使用 kit 声明的相同标识符运行 `sbx secret set`：

```console
$ sbx secret set my-service
```

没有单独的注册步骤；钥匙串条目以 kit 已经使用的标识符为键。有关 kit 侧的完整接线，请参阅 [向外部服务鉴权](../customize/kits.md#authenticate-to-external-services)。

### 列出和移除凭据

列出所有已存储的凭据：

```console
$ sbx secret ls
SCOPE      TYPE      NAME      SECRET
(global)   service   github    gho_GCaw4o****...****43qy
```

移除一个凭据：

```console
$ sbx secret rm github
```

> [!NOTE]
> 运行 `sbx reset` 会删除所有已存储的凭据以及所有沙盒状态。你将需要在重置后重新添加你的凭据。

### GitHub 令牌

`github` 服务让 agent 可以访问沙盒内部的 `gh` CLI。传入你现有的 GitHub CLI 令牌：

```console
$ echo "$(gh auth token)" | sbx secret set github
```

这对于创建 pull request、开 issue 或代表你与 GitHub API 交互的 agent 很有用。

### SSH agent

如果你的宿主有一个 SSH agent 并且设置了 `SSH_AUTH_SOCK`，Docker Sandboxes 会将 agent 转发进沙盒并在那里设置 `SSH_AUTH_SOCK`。私钥保留在你的宿主上。沙盒内部的进程可以请求转发 agent 的签名，但无法读取或复制私钥。

使用 SSH agent 转发进行基于 SSH 的 Git 操作以及基于 SSH 的提交签名。签名密钥必须加载到宿主 SSH agent 中，沙盒内的提交签名才能工作。出站 SSH 连接仍受沙盒网络策略约束。有关详细信息，请参阅 [提交签名](../workflows.md#commit-signing)。

## 自定义凭据

> [!IMPORTANT]
> 自定义凭据是实验性的。行为、标志和占位符格式可能会在没有通知的情况下更改。

对于不适合服务标识符模型的凭据——例如，当 agent 在启动时验证环境变量格式，或者凭据落在请求体中而不是头部时——使用 `sbx secret set-custom`。该凭据以一个或多个目标域、一个环境变量名和一个可选的占位符字符串为键，而不是以服务标识符为键。自定义凭据默认是全局的。传递 `--sandbox` 可将其限定到特定沙盒。

```console
$ sbx secret set-custom \
    --host api.example.com \
    --env API_KEY \
    --value <secret>
```

重复 `--host` 可让同一个凭据覆盖多个域——当一个 API 拆分在相关主机名之间或两个不相关的端点共享一个凭据时很有用：

```console
$ sbx secret set-custom \
    --host api.example.com \
    --host uploads.example.com \
    --env API_KEY \
    --value <secret>
```

`--host` 值也可以使用通配符，语法与[网络规则](../governance/concepts.md#network-rules)相同：`*` 匹配单个标签（`*.example.com` 覆盖 `api.example.com`），`**` 匹配任意数量（`**.example.com` 覆盖 `api.example.com` 和 `v2.api.example.com`）。

> [!WARNING]
> 以 `--value <secret>` 形式传递凭据会将其记录到你的 shell 历史中，并暴露给以你的用户身份运行的其他进程。避免将真实凭据内联粘贴——从已在你环境中存在的变量中读取值，如果真实凭据曾在命令行上传递过，请清除 shell 历史。

在沙盒内部，`API_KEY` 被设置为一个生成的占位符（例如 `sbx-cs-<rand>`）。当沙盒进程向任何配置的宿主发送请求，并且该占位符出现在请求中的任何位置时，代理会将其替换为真实值。agent 永远不会看到真实凭据。

只要可以选择，就优先使用[基于服务的流程](#stored-secrets)——kit 负责接线；你只需提供值。

## 凭据绑定

一个凭据绑定文件记录了你为每个服务批准的凭据机制和域。它位于 `~/.config/sbx/credentials.yaml`，在 Windows 上位于 `%APPDATA%\sbx\credentials.yaml`。

声明 `schemaVersion: "2"` 的第三方 kit 需要为其使用的每个凭据获得一个已批准的绑定。`sbx` 在你首次运行此类 kit 时会交互式地创建一个（请参阅 [首次运行审批](#first-run-approval)）；你也可以手动编写条目。仅由内置、嵌入式 kit 声明的凭据由来源（provenance）授权，不需要绑定。

`bindings` 下的每个条目以一个[服务标识符](#built-in-services)为键，并批准一种或两种凭据机制：

- `apiKey`——批准注入该服务的已存储 API 密钥。值来自[密钥存储](#stored-secrets)（`sbx secret set <service>`）；绑定记录的是审批，它不持有或定位该值。
- `oauth`——批准该服务的 OAuth 流程。你在宿主上登录，代理负责令牌刷新和路由。OAuth 域包括令牌端点主机以及 kit 声明的任何资源主机。

每种机制都带有一个 `domains` 列表，记录你批准的域。`sbx` 会在 kit 请求现有绑定未覆盖的域时要求审批。

```yaml
bindings:
  anthropic:
    apiKey:
      domains: [api.anthropic.com]
  github:
    apiKey:
      domains: [api.github.com, github.com]
```

绑定只是一个审批记录：存在 `apiKey` 或 `oauth` 即授权该机制。拒绝凭据则完全不写入任何条目。

### 首次运行审批

当第三方 kit 需要一个没有绑定的凭据时，`sbx` 会引导你完成审批。对于 API 密钥，你可以使用密钥存储中已有的值，或在提示处输入。对于 OAuth，你审批登录流程。在这两种情况下，你都审批 kit 声明的域。`sbx` 将条目写入 `credentials.yaml`。

在非交互式上下文中（CI 或 `--detached`），没有人来回答提示。没有绑定时，沙盒启动时该凭据被扣留。如果 kit 将凭据标记为 `required: true`，`sbx` 还会打印一条警告。通过交互式运行一次 kit，或在无人值守运行前直接编写 `credentials.yaml` 来预先创建绑定。

绑定文件控制第三方 v2 kit 是否可以使用服务凭据。kit 的凭据注入规则和网络权限仍然约束哪些请求可以携带该凭据。

### 需要绑定的 kit

只有声明了 `schemaVersion: "2"` 的第三方 kit 才需要绑定。内置 agent 也使用 `schemaVersion: "2"`，但仅由嵌入式 kit 声明的凭据由来源授权并自动注入。如果第三方 kit 也声明了相同的服务，则该服务需要审批。声明 `schemaVersion: "1"` 的 kit 注入其声明的凭据时不需要绑定。

## 注册表凭据

注册表凭据在向私有 OCI 注册表拉取[模板](../customize/templates.md)或 [kit](../customize/kits.md) 时进行鉴权，还可以让 agent 通过宿主侧代理从沙盒内部拉取和推送镜像。使用 `sbx secret set --registry <host>` 存储它们。对于 Docker Hub，`sbx` 复用你的 `sbx login` 会话——不需要注册表凭据。对于其他注册表（GitHub Container Registry、ECR、ACR、自托管的 Nexus 等），使用 `sbx secret set --registry` 存储凭据。

通过添加 `--all-sandboxes`、添加 `--sandbox SANDBOX`，或两者都不加来选择范围：

```text
sbx secret set [--all-sandboxes | --sandbox SANDBOX] --registry HOST
```

- **仅宿主**（无范围标志）：`sbx` CLI 在创建沙盒时用于拉取模板和 kit。凭据保留在宿主上，永远不会在沙盒内部可用。
- **所有沙盒**（`--all-sandboxes`）：与仅宿主相同，外加代理对来自沙盒的注册表登录请求进行鉴权。凭据保留在宿主上，永远不会写入沙盒文件系统。当 agent 构建并发布容器镜像时使用它。
- **沙盒限定**（`--sandbox SANDBOX`）：与 `--all-sandboxes` 相同的代理行为，但仅针对命名的沙盒。当只有一个沙盒需要注册表访问时使用它。

### 存储注册表凭据

从 stdin 管道传入令牌并指定注册表主机名：

```console
$ gh auth token | sbx secret set --registry ghcr.io --password-stdin
```

对于需要用户名的注册表（例如带有管理员账户的 ACR），添加 `--username`：

```console
$ echo "$ACR_PASSWORD" | sbx secret set \
    --registry myregistry.azurecr.io \
    --username myuser \
    --password-stdin
```

添加 `--all-sandboxes` 使凭据对每一个新沙盒都可用：

```console
$ gh auth token | sbx secret set --all-sandboxes --registry ghcr.io --password-stdin
$ sbx run claude
```

在创建沙盒之前存储所有沙盒的注册表凭据。已存在的沙盒不会拾取稍后添加的所有沙盒注册表凭据。要向现有沙盒添加注册表访问，请改用沙盒级凭据。

要将凭据限定到单个沙盒，将其存储在该沙盒名称下：

```console
$ gh auth token | sbx secret set --sandbox my-app --registry ghcr.io --password-stdin
```

`sbx kit pull` 也使用这些凭据，并以 Docker 凭据存储作为后备。`sbx kit push` 仅使用 Docker 凭据存储——推送目标仍然需要事先 `docker login`。

### 移除注册表凭据

移除某个注册表的仅宿主和所有沙盒条目：

```console
$ sbx secret rm --registry ghcr.io -f
```

要仅移除所有沙盒条目而保留仅宿主凭据，传递 `--all-sandboxes`：

```console
$ sbx secret rm --all-sandboxes --registry ghcr.io -f
```

要移除沙盒级凭据，传递沙盒名称：

```console
$ sbx secret rm --sandbox my-sandbox --registry ghcr.io -f
```

## 最佳实践

- 使用[已存储的凭据](#stored-secrets)来提供凭据。它们在静止状态下加密于 OS 钥匙串中（或在没有钥匙串的 Linux 宿主上一个加密文件中）。请参阅 [凭据存储在哪里](#where-secrets-are-stored)。
- 不要在沙盒内部手动设置 API 密钥。沙盒 agent 预配置为使用代理管理的凭据。
- 注册表凭据保留在宿主上，并在沙盒向注册表鉴权时由代理注入。将它们预留给需要注册表访问的沙盒，并优先使用沙盒范围而非 `--all-sandboxes` 以限制暴露。
- 一些 agent 支持 OAuth 作为另一个安全选项：流程在宿主上运行，因此令牌永远不会在沙盒内部暴露。如果你尚未存储凭据，agent 会提示你鉴权——Codex 从 `sbx run codex` 在宿主上提示，而 Claude Code、Cursor 和 Droid 在沙盒内部交互式提示。要提前鉴权，对 Codex 运行 `sbx secret set openai --oauth`，或在 Claude Code 内使用 `/login`；Cursor 和 Droid 没有提前鉴权的选项，因此它们的登录提示会在 agent 启动时出现。请参阅各个 [agent 页面](../agents/) 了解每个 agent 的流程。
- 如果你将凭据存储在 1Password 中，请参阅 [从 1Password 获取凭据](../workflows.md#sourcing-credentials-from-1password) 了解如何将 `op read` 和 `op run` 与 `sbx` 一起使用。

## 自定义模板与占位值

在 shell 沙盒中构建自定义模板或手动安装 agent 时，某些 agent 需要在启动前设置形如 `OPENAI_API_KEY` 的环境变量。如有需要，请将这些变量设置为占位值（例如 `proxy-managed`）。无论环境变量值如何，代理都会注入实际的凭据。

