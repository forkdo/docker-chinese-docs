---
title: Kit spec 参考
linkTitle: Spec 参考
description: kit 的 spec.yaml 逐字段参考，包括凭据、网络规则、环境、setup、文件、agent 指令，以及 sandbox 块。
keywords: sandboxes, sbx, kits, spec.yaml, reference, schema, fields
weight: 22
---

{{< summary-bar feature_name="Docker Sandboxes sbx" >}}

> [!NOTE]
> Kits 处于实验阶段。随着功能演进，kit 文件格式、CLI 命令，以及创建、加载和管理
> kit 的体验都可能发生变化。请在 [docker/sbx-releases](https://github.com/docker/sbx-releases)
> 仓库中反馈意见和提交 bug 报告。

本页记录了 kit 的 `spec.yaml` 中的每个字段。有关 kit 是什么以及如何使用它们的概述，
请参阅 [Kits](kits.md)。

有关解析器和测试使用的规范性 v2 语法，请参阅 `docker/sbx-kits-contrib` 仓库中的
[`schemaVersion: "2"` specification](https://github.com/docker/sbx-kits-contrib/blob/main/spec/SPEC-v2.md)。

一个 kit 目录需要一个必需的 `spec.yaml` 和一个可选的 `files/` 树：

```text
my-kit/
├── spec.yaml       # required
└── files/          # optional — static files to inject
    ├── home/
    └── workspace/
```

## Schema 版本

从 Docker Sandboxes 0.36 版本开始，支持两个 schema 版本。新的 kit 请使用
`schemaVersion: "2"`。版本 `"1"` 通过旧路径仍然被接受。

加载器在 `schemaVersion` 上分叉。一个 v2 spec 仅使用 v2 语法。在 `schemaVersion: "2"`
spec 中的旧 v1 字段会在解码时被拒绝，而不是被折叠进 v2 模型。每个 `spec.yaml` 保持使用
一种语法。

v2 中变更了什么：

| v1                                          | v2                                       |
| ------------------------------------------- | ---------------------------------------- |
| `credentials.sources.<id>`                  | `credentials:` 列表项，带 `service`       |
| `network.allowedDomains` / `deniedDomains`  | `permissions.network.allow` / `deny`     |
| `network.serviceDomains` / `serviceAuth`    | `credentials[].apiKey.inject`            |
| `network.publishedPorts` / `publishedPorts` | 顶层 `ports`                             |
| 独立的 `oauth:` 块                           | `credentials[].oauth`                    |
| `oauth.skipIfEnv`                           | 接受但忽略                               |
| `environment.proxyManaged`                  | `credentials[].apiKey.proxyManaged`      |
| `memory` / `agentContext`                   | `agentInstructions.content`              |
| `kind: agent` / `agent:` 块                 | `kind: sandbox` / `sandbox:` 块           |
| `sandbox.aiFilename`                        | `agentInstructions.filename`             |
| `sandbox.entrypoint.run`                    | `sandbox.entrypoint`                     |
| `sandbox.entrypoint.args`                   | `sandbox.command.default`                |
| `sandbox.entrypoint.ttyArgs`               | `sandbox.command.interactive`            |
| `tmpfs:`                                    | `volumes:` 带 `type: tmpfs` 的项          |
| `volumes:`（映射形式）                       | `volumes:` 序列（`- path: <path>`）       |
| `commands:` / `commands.initFiles`          | `setup:` / `setup.files`                 |
| `settings:` / `kitDir` / `persistence`      | 已移除                                   |

凭据发现也在 v2 中移出了 kit：kit 声明它需要哪些凭据以及如何注入它们，但每个值的来源由用户
通过 [凭据绑定](../security/credentials.md#credential-bindings) 控制。

> [!NOTE]
> 解析器接受 `mixins` 和 `sandbox.build`，但运行时支持尚待实现。设置了 `sandbox.build` 的
> kit 也必须设置 `sandbox.image`。

## 顶层字段

```yaml
schemaVersion: "2"
kind: <mixin | sandbox>
name: <name>
version: <version>
displayName: <name>
description: <text>
sourceURL: <url>
licenses:
  - MIT
locked:
  - sandbox.image
security:
  privileged: false
```

| Field           | Required | Description                                                                                     |
| --------------- | -------- | ----------------------------------------------------------------------------------------------- |
| `schemaVersion` | Yes      | Spec schema 版本。本语法使用 `"2"`。                                                            |
| `kind`          | Yes      | `mixin` 用于扩展 agent 的 kit；`sandbox` 用于定义一个 agent 的 kit。                            |
| `name`          | Yes      | 唯一标识符。小写字母数字加连字符，1 到 64 个字符。                                              |
| `version`       | No       | Kit 版本。                                                                                       |
| `displayName`   | No       | 可读名称。                                                                                       |
| `description`   | No       | 简短描述。                                                                                       |
| `sourceURL`     | No       | 源仓库或文档 URL。                                                                              |
| `licenses`      | No       | SPDX 许可证标识符。                                                                             |
| `locked`        | No       | 子 kit 不可覆盖的点分路径。                                                                      |
| `security`      | No       | 容器安全设置。`security.privileged: true` 以特权模式运行容器。                                   |

一个 kit 还声明行为块，例如 `agentInstructions`、`permissions`、`ports`、`credentials`、
`environment`、`setup` 和 `volumes`。

## Kit 种类

### `kind: mixin`

mixin 将能力叠加到已有的 sandbox 上。它不得声明 `sandbox:` 块、`extends:` 或 `mixins:`。
mixin 可以声明 `requires:` 来固定它所设计的基 agent：

```yaml
schemaVersion: "2"
kind: mixin
name: github-tools
requires:
  agent: claude
```

`requires.agent` 取一个基 agent 名称。它被作为 kit 名称校验，并在组合时强制执行。

### `kind: sandbox`

sandbox kit 定义一个完整的 agent。根 sandbox 必须声明一个 `sandbox:` 块。使用 `extends:` 的
sandbox 可以继承父级镜像并省略自己的 `sandbox:` 块：

```yaml
schemaVersion: "2"
kind: sandbox
name: claude-safe
extends: claude
```

`extends:` 仅限 sandbox。父级必须解析为 sandbox kit。`mixins:` 也仅限 sandbox 并被解析器
接受，但运行时组合支持尚待实现。

## Sandbox 块

```yaml
sandbox:
  image: <image-ref>
  build:
    context: .
    dockerfile: Dockerfile
    args:
      AGENT_VERSION: "1.0.0"
    target: runtime
    platforms:
      - linux/amd64
  entrypoint: [my-agent, "--flag"]
  command:
    default: ["--task-mode"]
    interactive: []
  resources:
    cpu: 2
    memory: 4g
    gpu: "1"
```

| Field                | Required | Description                                                                                                     |
| -------------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `sandbox.image`      | 省略 `extends:` 时 | Docker 镜像引用。                                                                                                |
| `sandbox.build`      | No       | 构建配置。运行时支持尚待实现，因此带 `build:` 的 kit 也必须设置 `image:`。                                       |
| `sandbox.entrypoint` | No       | 固定的进程前缀，为字符串数组。第一个元素是 agent 二进制。                                                        |
| `sandbox.command`    | No       | 特定模式的参数尾。对 `default` 使用列表简写，或对 `default` 和 `interactive` 使用映射。                          |
| `sandbox.resources`  | No       | 可选的 CPU、内存和 GPU 约束。内存使用字节大小字符串，如 `4096m` 或 `4g`。                                        |

有效命令在非交互式启动时是 `entrypoint` 加 `command.default`，在 TTY 会话中是 `entrypoint`
加 `command.interactive`。如果省略 `interactive`，则回退到 `default`。

对于使用 `extends:` 的 kit，`sandbox.command` 替换完整的继承参数尾，包括父级
`sandbox.entrypoint` 中二进制之后的标志。它不会追加到该尾部。定义子级需要的每个参数。例如，
`claude` 的一个添加了 `--settings` 的子级也必须包含 `--dangerously-skip-permissions` 以保留
该行为。

agent 的容器镜像必须提供：

- UID 为 1000 的非 root `agent` 用户，具有无需密码的 sudo。
- 由 `agent` 拥有的 `/home/agent/` 家目录。
- 跨 sudo 保留的 HTTP 代理环境变量（`HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY`）。
- agent 二进制，要么烘焙进去，要么用 [`setup.install`](#setup) 安装。

基于 `docker/sandbox-templates:shell-docker` 构建即可获得这些基础要求。

## Agent 指令

```yaml
agentInstructions:
  filename: CLAUDE.md
  content: |
    Ruff is installed. Run `ruff check` before committing.
```

| Field      | Description                                                                                         |
| ---------- | --------------------------------------------------------------------------------------------------- |
| `filename` | AI 配置文件名。对 `kind: sandbox` 有意义；对 `kind: mixin` 则忽略并发出警告。                        |
| `content`  | Markdown 指令。对 sandbox，内联进 profile。对 mixin，写入 kit 记忆。                                 |

对 mixin，引擎将 `content` 写入 `<dir-of-AI-file>/kits-memory/<kit-name>.md`，并向基 AI 文件
添加一个 `## Kits` 指针小节。这将每个 mixin 的指令保留在单独的文件中。

## 凭据

kit 声明它需要的凭据，以及代理如何将它们注入出站请求。它不声明主机发现来源。用户通过密钥
存储或首次运行提示提供值，而 [凭据绑定](../security/credentials.md) 授权其使用。kit 不能
读取任意宿主环境变量或文件。

```yaml
credentials:
  - service: <service-id>
    description: <text> # optional
    required: <true | false> # optional, default false
    provider: <provider> # optional, reserved
    apiKey:
      name: <ENV_VAR>
      proxyManaged: true
      inject:
        - domain: <domain>
          header: <header>
          format: <format>
        - domain: <domain>
          scheme: bearer
        - domain: <domain>
          scheme: basic
          username: <user> # required with scheme: basic
    oauth:
      tokenEndpoint:
        host: <host>
        path: <path>
      sentinels:
        accessToken: <sentinel>
        refreshToken: <sentinel>
      credentialFile:
        path: <path>
        template: |
          {
            "<key>": {
              "accessToken": "{{.AccessToken}}",
              "refreshToken": "{{.RefreshToken}}",
              "expiresAt": {{.ExpiresAt}},
              "scopes": {{.ScopesJSON}}
            }
          }
```

`credentials` 是一个列表；每个条目命名一个 `service` 并配置一个或多个认证机制。

| Field         | Description                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `service`     | 凭据标识符，与用 `sbx secret set` 存储的值匹配。小写 kebab-case。                                                                          |
| `description` | 可选。在批准 [绑定](../security/credentials.md#credential-bindings) 时显示给用户。                                                          |
| `required`    | 将凭据标记为对 agent 至关重要。如果没有绑定，`sbx` 会警告并以扣留凭据的方式启动。默认 `false`。                                              |
| `provider`    | 为提供方注册表保留。接受并发出警告，无运行时效果。                                                                                         |
| `apiKey`      | API 密钥注入（见 [apiKey](#apikey)）。                                                                                                      |
| `oauth`       | OAuth 拦截（见 [oauth](#oauth)）。                                                                                                          |

每个服务必须声明 `apiKey`、`oauth`，或两者。当两者在运行时都解析时，API 密钥优先，OAuth
作为回退。

### `apiKey`

| Field               | Description                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | 凭据的环境变量名（例如 `ANTHROPIC_API_KEY`）。                                                                                                    |
| `proxyManaged`      | 若为 `true`，`sbx` 将容器内 `name` 设为 `proxy-managed` 哨兵值。默认 `false`。                                                                    |
| `inject[].domain`   | 注入凭据的域名。也必须在 [`permissions.network`](#network) 中被允许。                                                                             |
| `inject[].header`   | 代理设置的 HTTP 请求头（例如 `x-api-key`、`Authorization`）。                                                                                     |
| `inject[].format`   | 请求头值格式，带一个 `%s` 占位符（例如 `"%s"` 或 `"Bearer %s"`）。与 `scheme` 互斥。                                                             |
| `inject[].scheme`   | 常见认证方案的简写。`bearer` 展开为 `Authorization: Bearer %s`；`basic` 需要 `username`。与 `format` 互斥。                                        |
| `inject[].username` | HTTP Basic 认证的用户名，例如 Git over HTTPS 的 `x-access-token`。                                                                                |

### `oauth`

对于使用 OAuth 认证的 agent（例如 Claude Code），代理拦截 token 响应，用哨兵值替换真实
token，然后在出站请求时换回真实 token。默认情况下，token 永远不会进入沙箱。设置
`passthrough: true` 可退出哨兵屏蔽，将真实 token 响应送入沙箱。

| Field                                    | Description                                                                                                                                                                                       |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tokenEndpoint.host` / `path`            | 代理拦截的 OAuth token 端点。                                                                                                                                                                     |
| `sentinels.accessToken` / `refreshToken` | 写入容器以替代真实 token 的哨兵值。                                                                                                                                                               |
| `credentialFile.path`                    | 在容器内写入凭据文件的位置（`~` 展开）。                                                                                                                                                         |
| `credentialFile.template`                | 用于渲染凭据文件的 Go 模板。支持 `{{.AccessToken}}`、`{{.RefreshToken}}`、`{{.ExpiresAt}}`、`{{.Scopes}}` 和 `{{.ScopesJSON}}`。对 JSON 数组使用 `{{.ScopesJSON}}`。 |
| `credentialFile.structure`               | 由 schema v2 定义但 `sbx` 引擎不支持的声明式 JSON 形状。仅结构的 kit 验证失败。请使用 `credentialFile.template`。                                                |
| `resourceHosts`                          | 代理在出站请求上附加 token 的 API 主机，与 token 端点主机不同。                                                                                                  |
| `skipIfEnv`                              | 为兼容性接受，但在 schema v2 中被忽略。v2 绑定是权威来源，而非宿主环境变量。                                                                                       |
| `responseFields`                         | 覆盖代理从 token 响应读取的默认字段名。                                                                                                                                                          |
| `passthrough`                            | 若为 `true`，代理原样传递 token 响应，而不是用哨兵值替换 token。                                                                                                  |

## 网络

网络出口在 `permissions.network` 下声明。凭据不再携带自己的域名映射——代理只将凭据注入其
[`apiKey.inject`](#apikey) 列出的域名，而沙箱到达的每个域名都必须在此处被允许。

```yaml
permissions:
  network:
    allow: [<domain>, ...]
    deny: [<domain>, ...]
```

| Field                       | Description                                                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `permissions.network.allow` | 沙箱可以到达的域名。                                                                                            |
| `permissions.network.deny`  | 沙箱被阻止到达的域名。拒绝优先于允许，包括跨组合的 kit。                                                        |

允许和拒绝模式：

| Pattern               | Example                  | Status                      |
| --------------------- | ------------------------ | --------------------------- |
| Exact host            | `api.example.com`        | Enforced                    |
| Exact host and port   | `api.example.com:8080`   | Enforced                    |
| Single-label wildcard | `*.example.com`          | Enforced                    |
| Multi-label wildcard  | `**.example.com`         | Parsed; enforcement pending |
| Port range            | `api.example.com:80-443` | Parsed; enforcement pending |
| Port wildcard         | `api.example.com:*`      | Parsed; enforcement pending |
| CIDR                  | `10.0.0.0/8`             | Parsed; enforcement pending |

在 v1 中这是 `network:` 块（`allowedDomains` / `deniedDomains`，加上 `serviceDomains` /
`serviceAuth`）。在 v2 中，这些字段是解码错误。

## 端口

使用 `ports` 将沙箱服务暴露给宿主机：

```yaml
ports:
  - container: 8080
    protocol: tcp
    name: web
```

| Field       | Description                                                         |
| ----------- | ------------------------------------------------------------------- |
| `container` | 容器端口，1 到 65535。                                              |
| `protocol`  | `tcp` 或 `udp`。空表示 `tcp`。                                      |
| `name`      | 列出已发布端口绑定的工具所展示的可选标签。                          |

宿主机端口在 `127.0.0.1` 上临时分配。用户可以用 `sbx ports --publish <host>:<container>`
固定宿主机端口。

## 环境

```yaml
environment:
  variables:
    <NAME>: <value>
```

| Field       | Description                                    |
| ----------- | ---------------------------------------------- |
| `variables` | 直接在容器内设置的键值对。                     |

变量名必须是有效的 shell 标识符（`[A-Za-z_][A-Za-z0-9_]*`）。

不要设置 `DASH_`、`SBX_` 或 `DOCKER_` 变量，并避免覆盖 `HOME`、`USER`、`SHELL`、`PATH`、
`LD_PRELOAD` 和 `LD_LIBRARY_PATH`。运行时保留这些名称并可能覆盖它们。

## Setup

```yaml
setup:
  install:
    - command: <shell-string>
      user: <uid>
      description: <text>
  startup:
    - command: [<argv>, ...]
      user: <uid>
      background: <true | false>
      description: <text>
  files:
    - path: <path>
      content: <text>
      mode: <octal>
      onlyIfMissing: <true | false>
      description: <text>
```

### 执行顺序

当创建一个沙箱时，kit 内容按此顺序应用：

1. 网络权限和环境变量。
2. `files/home/` 下的静态文件。
3. `setup.install` 命令，按声明顺序。
4. `setup.files` 项。
5. `setup.startup` 命令注册用于每次沙箱启动。
6. `files/workspace/` 下的静态文件，在 workspace 就绪后。用 `--clone` 时，这意味着仓库克隆
   之后。

对于堆叠的 kit，每个阶段的项按 `--kit` 顺序应用。一个 install 命令可以消费来自 `files/home/`
的打包文件，但不能消费来自 `files/workspace/` 或 `setup.files` 的文件，因为那些文件落得更晚。

`sbx kit add` 重建沙箱，而不是就地修改它。它支持仅限于 `environment.variables`、
`setup.install` 和 `permissions.network.allow` 的 mixin kit，它们遵循与沙箱创建相同的顺序。
它拒绝声明静态文件、`setup.startup` 或 `setup.files` 的 kit。要使用这些字段，请用 kit 重建
沙箱。

### install

在应用 kit 时同步运行，无论是在沙箱创建期间还是通过 `sbx kit add`。Shell 字符串传给
`sh -c`。

| Field         | Default | Description                   |
| ------------- | ------- | ----------------------------- |
| `command`     | —       | Shell 命令字符串。            |
| `user`        | `"0"`   | 运行的用户。`"0"` = root。    |
| `description` | —       | 可读描述。                    |

### startup

在每次沙箱启动时运行。字符串数组，不由 shell 解释。

| Field         | Default  | Description                         |
| ------------- | -------- | ----------------------------------- |
| `command`     | —        | 命令和参数，为字符串数组。          |
| `user`        | `"1000"` | 运行的用户。`"1000"` = agent。     |
| `background`  | `false`  | 阻塞后续启动命令，直到此命令完成。设为 `true` 让后续命令无需等待即可运行。 |
| `description` | —        | 可读描述。                          |

启动命令是非交互式的。它们在 agent 连接之前运行，没有终端连接，因此它们不能提示用户（例如，
交互式 `aws login` 会挂起或失败）。它们也不门控 agent 的入口点：一旦启动命令被分发，agent
就会启动，无论 `background` 如何。值 `false` 在启动分发器内等待它运行下一个命令；它不会延迟
agent 入口点。将启动命令用于非交互式准备——启动守护进程、预热缓存、刷新配置——并将任何需要在
agent 运行前落盘的值用于 `setup.files`。

启动命令必须是幂等的。它们在每次沙箱启动时运行，并在容器重启时重放，因此一个在第二次调用时
失败或行为异常的命令会破坏重启路径。用存在性检查保护工作，使用 upsert 而非 insert，并优先
选择无论运行多少次都收敛到相同终态的命令。

### files

在沙箱启动时写入的文件，带运行时替换。

| Field           | Default  | Description                                               |
| --------------- | -------- | --------------------------------------------------------- |
| `path`          | —        | 绝对容器路径。                                            |
| `content`       | —        | 文件内容。`${WORKDIR}` 展开为 workspace 路径。             |
| `mode`          | `"0644"` | 文件权限，八进制。                                        |
| `onlyIfMissing` | `false`  | 如果文件已存在则跳过。                                    |

## 静态文件

```text
my-kit/files/
├── home/       → /home/agent/
└── workspace/  → primary workspace path
```

| Kit path           | Container destination                   |
| ------------------ | --------------------------------------- |
| `files/home/`      | `/home/agent/`（配置文件、点文件）      |
| `files/workspace/` | 主 workspace 路径                        |

父目录自动创建。现有文件被覆盖。绝对路径和路径遍历序列（`../../`）被拒绝。

## 卷

```yaml
volumes:
  - path: /workspace
    size: 10g
    mode: "0755"
  - path: /tmp/scratch
    type: tmpfs
    size: 512m
    mode: "1777"
```

| Field  | Description                                                         |
| ------ | ------------------------------------------------------------------- |
| `path` | 必需的绝对容器路径。                                                |
| `type` | 空表示块支持卷，或 `tmpfs` 表示 RAM 支持存储。                       |
| `size` | 可选的字节大小字符串。                                              |
| `mode` | 可选的八进制权限。                                                  |

卷仅在创建沙箱时应用。`sbx kit add` 不能将卷附加到运行中的容器。
