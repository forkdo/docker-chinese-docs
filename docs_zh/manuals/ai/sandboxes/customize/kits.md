---
title: Kits
description: 使用声明式 YAML 制品，通过工具、凭据、网络规则和配置扩展沙箱。
keywords: sandboxes, sbx, kits, mixins, customization, extensions, agents
weight: 20
---

{{< summary-bar feature_name="Docker Sandboxes sbx" >}}

> [!NOTE]
> Kits 处于实验阶段。随着功能演进，kit 文件格式、CLI 命令，以及创建、加载和管理
> kit 的体验都可能发生变化。请在 [docker/sbx-releases](https://github.com/docker/sbx-releases)
> 仓库中反馈意见和提交 bug 报告。

一个 kit 打包了一组沙箱可用的能力，例如：

- 要安装的工具
- 要设置的环境变量
- 要注入的凭据
- 允许或拒绝域名的网络规则
- 要放入的文件
- 要运行的启动命令
- 要给 agent 的记忆指令

你在一个单独的 `spec.yaml` 文件中声明这些，将 CLI 指向该目录（或 ZIP、OCI 制品、或 Git
URL），沙箱会在运行时应用并强制执行它们。凭据保留在宿主机上，通过代理而非进入 VM，出站流量
被限制为 kit 网络规则所允许的域名。

一个 kit 要么是 mixin，要么是 sandbox：

- Mixin kit（`kind: mixin`）用额外能力扩展已有的 agent。可以在同一个沙箱上堆叠多个。
- Sandbox kit（`kind: sandbox`）从零定义一个完整的 agent：它的镜像、入口点、网络策略，以及
  agent 需要的一切。

## Kits 能做什么

### 运行命令

kit 可以在沙箱内部自动运行命令。**安装命令**在创建时运行一次；**启动命令**在沙箱每次
启动时运行。

安装命令是把 agent 需要的任何东西放进镜像的地方，通过 `apt`、`pip`、`npm`、`curl | bash`，
或任何合适的手段：

```yaml
setup:
  install:
    - command: "apt-get update && apt-get install -y jq"
```

启动命令涵盖类似启动后台服务、预热缓存，或在每次启动时刷新配置的事情。它们必须是幂等的
——请参阅 [`startup`](kit-reference.md#startup) spec 参考：

```yaml
setup:
  startup:
    - command: ["my-daemon"]
      background: true
```

### 注入文件

kit 可以通过两种方式向沙箱注入文件：**与 kit 一起打包的静态文件**，以及在启动时写入、并替换
运行时值的 **`setup.files`**。

静态文件适合在不同沙箱间不变的内容，例如工具配置、共享的 linter 规则、agent 可调用的辅助
脚本，或像风格指南或 API 速查表这样的参考资料。

```text
my-kit/
├── spec.yaml
└── files/
    ├── home/
    │   └── .config/my-tool/settings.json
    └── workspace/
        └── .editorconfig
```

`setup.files` 涵盖依赖于运行时值的内容，例如一个工具在启动时需要将绝对 workspace 路径烘焙
进其配置文件：

```yaml
setup:
  files:
    - path: /home/agent/.my-tool/config.json
      content: '{"workspace": "${WORKDIR}"}'
      onlyIfMissing: true
```

所有字段请参阅 spec 参考中的 [`setup.files`](kit-reference.md#files)。

#### 沙箱管理的 agent 配置

内置 agent kit 为沙箱设置保留以下路径。即使某个文件只针对特定功能需要，也要将这些路径视为
沙箱管理的。不要用静态文件、`setup.files` 或安装命令针对它们。后续设置可能替换你的内容，或
依赖你的文件移除的设置。在此表中，`~` 是 `/home/agent`。

| Built-in agent kit | Managed configuration paths |
| ------------------ | --------------------------- |
| `claude` | `~/.claude.json`, `~/.claude/settings.json`, `~/.claude/.config.json` |
| `codex` | `~/.codex/config.toml` |
| `copilot` | `~/.copilot/config.json` |
| `cursor` | `~/.cursor/cli-config.json` |
| `gemini` | `~/.gemini/settings.json` |
| `kiro` | `~/.kiro/settings/mcp.json` |
| `opencode` | `~/.config/opencode/opencode.json` |

当 agent 支持时，使用单独的设置层。例如，Claude Code 可以用 `--settings` 加载一个额外的设置
文件，OpenCode 可以从 `OPENCODE_CONFIG` 中的路径加载一个。示例请参阅
[定制 agent 设置](kit-examples.md#customize-agent-settings)。不要将 `setup.startup` 用于 agent
在初始化期间必须读取的设置，因为启动命令不门控 agent 入口点。

### 设置环境变量

kit 设置的环境变量在运行时对 agent 可用：

```yaml
environment:
  variables:
    MY_TOOL_WORKSPACE: /home/agent/my-tool
```

有关凭据，请参阅 [向外部服务认证](#authenticate-to-external-services)。不要把秘密值直接放进
`environment.variables`——它们在沙箱 VM 内可见。

> [!IMPORTANT]
> 沙箱为你管理代理设置。它会自动设置 `HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY` 及其小写等价
> 形式，以便流量流经其内置的前向代理，该代理强制执行网络策略并注入凭据。把这些变量留给沙箱
> ——在 kit 中设置它们会把流量从前向代理引开，从而它无法再应用网络策略或注入凭据，这些请求
> 通常连接失败。要通过上游企业代理发送沙箱流量，请在宿主机上配置它。请参阅
> [上游代理](../architecture.md#upstream-proxy)。

### 控制网络访问

网络规则定义沙箱可以到达或阻止哪些域名。kit 网络规则仅适用于使用该 kit 的沙箱：

```yaml
permissions:
  network:
    allow:
      - api.example.com
      - "*.cdn.example.com"
    deny:
      - telemetry.example.com
```

对 agent 需要的主机使用 `allow`，例如包注册表、安装端点，或外部 API。对 agent 不应到达的
主机使用 `deny`，例如遥测端点。如果一个域名同时匹配允许规则和拒绝规则，拒绝规则获胜。

> [!IMPORTANT]
> 当组织治理处于激活状态时，只有组织允许规则授予访问权限，因此 kit 定义的 `allow` 规则被忽略
> ——包括任何 kit 允许 agent 到达的域名。kit 定义的 `deny` 规则仍然适用，因为拒绝只能进一步
> 限制访问。详见 [策略优先级](../governance/concepts.md#precedence)。

有关认证服务，请参阅 [向外部服务认证](#authenticate-to-external-services)。

### 向外部服务认证

kit 可以通过宿主侧代理将凭据附加到出站请求。VM 内的 agent 使用一个哨兵值工作；代理在宿主机
上读取真实凭据，并在请求离开沙箱前覆盖认证请求头。

kit 声明服务、容器内环境变量，以及如何注入凭据。它不声明宿主发现来源。用户通过密钥存储或
首次运行提示提供值，而 [凭据绑定](../security/credentials.md) 授权其使用：

```yaml
credentials:
  - service: my-service
    apiKey:
      name: MY_SERVICE_API_KEY # in-VM env var, set to a sentinel
      proxyManaged: true
      inject:
        - domain: api.example.com # inject on requests to this domain
          header: Authorization # overwrite this header
          format: "Bearer %s"

permissions:
  network:
    allow:
      - api.example.com # the domain must also be reachable
```

agent 以 `MY_SERVICE_API_KEY=proxy-managed` 启动，用该哨兵值发送 `Authorization` 中的请求，
代理在转发前用真实凭据覆盖该请求头。真实秘密永远不会进入 VM。

有关如何在宿主机上提供凭据值、不适合上面示例的其他方法，以及代理在请求时做什么，请参阅
[凭据](../security/credentials.md)。要批准第三方 v2 kit 声明的机制和域名，请参阅
[凭据绑定](../security/credentials.md)。

### 注入 agent 记忆

kit 可以向 agent 的记忆文件追加内容，例如 `CLAUDE.md` 或 `AGENTS.md`。agent 在启动时读取此
文件。用它给 agent 项目约定、kit 安装的工具的使用技巧，或沙箱运行时应处于作用域内的其他
指导。

```yaml
agentInstructions:
  content: |
    Ruff is installed. Run `ruff check` before committing.
    Shared config lives at `/workspace/ruff.toml`.
```

mixin 和 sandbox kit 都可以声明 `agentInstructions.content`。活动的 sandbox kit 设置
`agentInstructions.filename`，它决定记忆文件的名称。sandbox kit 的内容内联写入该文件。每个
mixin 的内容写入它自己的 `<kit-name>.md` 文件，位于同级 `kits-memory/` 目录下，主记忆文件
获得一个指向每个 mixin 文件的 `## Kits` 小节：

```text
/Users/you/
├── myproject/              # workspace
├── AGENTS.md               # main memory file with a "## Kits" index
└── kits-memory/
    ├── ruff-lint.md
    ├── vale.md
    └── git-ssh-sign.md
```

完整的字段 schema 请参阅 spec 参考中的
[`agentInstructions`](kit-reference.md#agent-instructions)。

### 定义一个 agent

sandbox kit 声明一个 `sandbox:` 块，包含 agent 运行的镜像，以及用户启动沙箱时连接到的命令：

```yaml
sandbox:
  image: "my-registry/my-agent:latest"
  entrypoint: [my-agent, "--yolo"]
```

有关用例和示例，请参阅 [Sandbox kits](#sandbox-kits)。

## Mixin kits

mixin kit 用额外能力扩展已有的 agent。常见用例：

- 预安装工具：linter、库，或其他自定义程序
- 授予 agent 访问新的认证服务（数据库、厂商 API）
- 注入共享的团队配置（linter 规则、编辑器设置、点文件）

完整的 mixin 示例请参阅 [放入一份共享配置文件](kit-examples.md#drop-a-shared-config-file) 和
[在沙箱创建时安装工具](kit-examples.md#install-a-tool-at-sandbox-creation)。

## Sandbox kits

sandbox kit 从零定义一个完整的 agent——镜像、入口点，以及 agent 需要的一切。常见用例：

- 打包你构建的自定义 agent，以便他人运行
- 发布一个团队内部的、内置默认值的 agent
- 运行带有你自己配置的现有 agent 的 fork
- 原型化一个新的 agent 集成

sandbox kit 声明 mixin kit 能声明的一切，外加一个
[`sandbox:` 块](kit-reference.md#sandbox-block)，告诉沙箱如何启动 agent。有关逐步讲解，请参阅
[构建你自己的 agent kit](build-an-agent.md)。

### 扩展内置 agent

使用 `extends:` 创建内置 agent 的变体，而无需复制其配置。子 kit 继承父级的镜像、凭据、网络
权限、持久卷、设置、MCP 集成和 agent 指令。对单个父 agent 使用 `extends:`；使用 mixin 来添加
可在一个或多个 agent 上工作的独立能力。有关更改 Claude Code 权限模式的示例，请参阅
[Fork 一个现有 agent](kit-examples.md#fork-an-existing-agent)。

## 使用 kits

kit 可以从本地路径（目录或 ZIP 文件）、Git 仓库或 OCI 仓库加载。多次传递 `--kit` 可在一个
沙箱上堆叠多个 kit。

> [!IMPORTANT]
> `--kit` 仅在创建沙箱时生效。对已有的沙箱名传递它会失败并提示
> `--kit can only be used when creating a new sandbox`。要向运行中的沙箱添加受支持的 mixin kit，
> 请改用 [`sbx kit add`](#local)。`sbx kit add` 重启沙箱以应用更新的 kit 集。VM 状态——已安装
> 的包、Docker 镜像、卷和 agent 历史——在重启期间保留。它支持仅限于 `environment.variables`、
> `setup.install` 和 `permissions.network.allow` 的 mixin kit。要使用其他字段，请用 `--kit` 重建
> 沙箱。

### 本地

将 `--kit` 指向磁盘上的目录或 ZIP 文件：

```console
$ sbx run claude --kit ./my-kit/
$ sbx run claude --kit ./my-kit-1.0.zip
```

在迭代受支持的 mixin kit 时，用 `sbx kit add` 将更改应用到运行中的沙箱：

```console
$ sbx kit add my-sandbox ./my-kit/
```

`sbx kit add` 重启沙箱以应用更新的 kit 集。VM 状态——已安装的包、Docker 镜像、卷和 agent 历史
——在重启期间保留。kit 无法从运行中的沙箱移除——移除并重建它以获得干净的开始。

### Git 仓库

```console
$ sbx run claude --kit "git+https://github.com/docker/sbx-kits-contrib.git#ref=v0.1.0&dir=code-server"
```

- `#ref=<branch|tag|commit>` 固定到特定修订。默认为仓库的默认分支。
- `#dir=<path>` 从子目录加载 kit。
- `git+ssh://` URL 也有效，使用你的本地 SSH agent、Git 凭据助手和 `.netrc`。
- 在 `&` 会启动后台作业的 shell 中，请给 URL 加引号。

### OCI 仓库

```console
$ sbx run claude --kit ghcr.io/myorg/my-kit:1.0
```

对于 Docker Hub，请包含完整的 `docker.io` 前缀。有关发布，请参阅
[打包与分发](#packaging-and-distribution)。

> [!IMPORTANT]
> 对于 Docker Hub，`sbx` 复用你的 `sbx login` 会话来拉取私有 kit。对于其他仓库，请在运行沙箱
> 前用 [`sbx secret set --registry`](../security/credentials.md#registry-credentials) 存储
> 拉取凭据：
> >
> > ```console
> > $ gh auth token | sbx secret set --registry ghcr.io --password-stdin
> > ```
> >
> > 没有存储的凭据时，从非 Docker Hub 仓库的拉取是匿名的，私有 kit 会拉取失败。

### 限制 kit 来源

`sbx` 限制 kit 可以从哪些来源安装。kit 的安装命令在沙箱内以 root 权限运行，因此限制 kit 的
来源可降低供应链风险。默认情况下，只允许托管在 Docker Hub（`docker.io/`）上的 kit。从任何其他
来源加载 kit 会失败：

```console
$ sbx run claude --kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=vale"
ERROR: resolve kits: kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=vale" cannot be installed — its source is not in your allowlist.
```

要允许另一个发布方，将其主机或主机/路径前缀添加到 `kit.allowedSources` 设置。该设置替换整个
列表，因此请包含你想保留的条目：

```console
$ sbx settings set kit.allowedSources '["docker.io/","github.com/docker/"]'
```

条目在路径段边界上作为前缀匹配，因此 `github.com/docker/` 允许 `github.com/docker/sbx-kits-contrib`
但不允许 `github.com/docker-evil/kit`。要移除限制并允许任何远程来源，请将列表设为 `["*"]`。
不推荐这样做。

从本地目录或 ZIP 文件安装由 `kit.allowLocalKits` 设置单独管理，其默认值为 `true`。将其设为
`false` 以要求远程来源：

```console
$ sbx settings set kit.allowLocalKits false
```

对于非交互式使用，两个设置都有环境变量等价物：`DOCKER_SANDBOXES_KIT_ALLOWED_SOURCES` 和
`DOCKER_SANDBOXES_KIT_ALLOW_LOCAL`。

## 打包与分发

`sbx kit` 子命令验证、检查并发布 kit：

- `sbx kit validate <path>` — 检查 kit 目录或 ZIP 是否格式正确。
- `sbx kit inspect <path>` — 显示 kit 详情。添加 `--json` 以获得机器可读输出。
- `sbx kit pack <path> -o <file.zip>` — 将目录打包为 ZIP 文件以分享。
- `sbx kit push <path> <ref>` — 发布到 OCI 仓库（例如 `ghcr.io/myorg/my-kit:1.0`）。
- `sbx kit pull <ref>` — 从仓库下载 kit 作为 ZIP 文件到工作目录。

对于 Docker Hub，请包含完整的 `docker.io` 前缀——`sbx` 不会自动添加它。

`sbx kit pull` 优先使用 [`sbx secret set --registry`](../security/credentials.md#registry-credentials)
存储的凭据，回退到 Docker 凭据存储。`sbx kit push` 仅使用 Docker 凭据存储，因此推送到私有
仓库需要先 `docker login`。

## Spec 参考

有关每个 `spec.yaml` 块的逐字段参考——顶层字段、凭据、网络、环境、setup、静态文件、agent 指令
和 sandbox 块——请参阅 [Kit spec 参考](kit-reference.md)。

## 调试

当 kit 的行为不符合预期时，从网络策略日志和沙箱内的直接检查开始：

- `sbx policy log` 显示沙箱代理看到的每个出站请求、它匹配的规则、可用时的额外上下文，以及它的
  `PROXY` 值，例如 `forward`、`forward-bypass`、`transparent` 或 `browser-open`。用它诊断安装
  时的下载失败、被阻止的域名和意外的 TLS 拦截。如果在你添加凭据的 `apiKey.inject` 后下载失败
  或到达时已损坏，检查注入域名是否过宽。只在需要凭据的主机上注入。
- `sbx exec <sandbox> -- <cmd>` 在已有沙箱内运行任意命令。无需重建即可检查安装后状态很有用：
  `which mytool`、`ls /home/agent/.local/bin/`、`cat /home/agent/.config/...` 等等。

安装和启动命令的输出仅在 `sbx run` 或 `sbx create` 期间发出；`sbx` 不会保留它供以后检查。要
用全新输出重复 setup，移除并重建沙箱：`sbx rm <sandbox> && sbx run ...`。
