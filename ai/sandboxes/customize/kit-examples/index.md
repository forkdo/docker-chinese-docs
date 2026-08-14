# Kit 示例




> [!NOTE]
> Kits 处于实验阶段。随着功能演进，kit 文件格式、CLI 命令，以及创建、加载和管理
> kit 的体验都可能发生变化。请在 [docker/sbx-releases](https://github.com/docker/sbx-releases)
> 仓库中反馈意见和提交 bug 报告。

下面每个小节展示一个 `spec.yaml` 片段，演示一种 kit 模式。这些不是完整的、可分发
的 kit——而是小而聚焦的示例，你可以提取到自己的 kit 中。有关完整的 spec 参考，请
参阅 [Kit spec 参考](kit-reference.md)。

## 放入一份共享配置文件

当内容在每个沙箱中都相同、且不需要在运行时替换任何值时，使用 `files/workspace/`
下的静态文件。典型用例：linter 规则、编辑器设置、共享的 `.editorconfig`、团队点文件。

```text
ruff-lint/
├── spec.yaml
└── files/
    └── workspace/
        └── ruff.toml
```

```yaml {title="ruff-lint/spec.yaml"}
schemaVersion: "2"
kind: mixin
name: ruff-lint
displayName: Ruff
description: Python linting with shared team config

setup:
  install:
    - command: "uv tool install ruff@latest"
      user: "1000"
```

```toml {title="ruff-lint/files/workspace/ruff.toml"}
line-length = 80

[lint]
select = ["E", "F", "I"]
```

## 在沙箱创建时安装工具

`setup.install` 在每个沙箱创建时运行一次。任何需要落入镜像的内容都放在这里——包
管理器（`apt-get`、`pip`、`npm`）、二进制下载，或厂商安装脚本。

> [!TIP]
> 每个新沙箱都会运行所有 `setup.install` 命令。结果不会在沙箱之间缓存。创建 kit 避免了
> 构建和分发镜像，因此 kit 很适合较小、可组合的变化。对于大量的构建或安装步骤，请考虑
> 使用 [自定义模板](templates.md#build-a-custom-template)。沙箱会从本地缓存复用模板镜像。

```yaml
setup:
  install:
    - command: "apt-get update && apt-get install -y jq"
    - command: "curl -fsSL https://example.com/install.sh | sh"
```

安装命令默认以 root 运行。当该步骤应以 agent 用户运行时，设置 `user: "1000"`——例如，
针对用户级前缀的 `npm install -g`，或任何写入 `/home/agent/` 的操作。

安装步骤在 `sh` 下运行，而非 bash，因此仅 bash 内置的命令（如 `source`）会失败并
报 `sh: source: not found`。当你需要它们时，显式管道到 `bash`（`curl … | bash`）或将
步骤包裹在 `bash -c '…'` 中。

下载受沙箱的 [网络访问规则](../governance/access-controls/network.md) 约束。一个能从你的
宿主机解析的域名在沙箱内仍可能被阻止——例如，`get.sdkman.io` 在你用
`sbx policy allow network get.sdkman.io` 允许它之前会返回 403。一个工具也可能需要镜像中
没有的基础包：例如 [SDKMAN!](https://sdkman.io/) 需要 `zip` 和 `unzip`，因此在安装它之前
添加一个 `apt-get install -y zip unzip` 步骤（以 root 身份）。

> [!WARNING]
> `curl … | bash` 会掩盖下载失败。管道的退出状态是 bash 的，而 bash 在空输入时退出 `0`，
> 因此被阻止或失败的下载仍会报告成功——即使什么都没安装，沙箱也会在没有任何错误的情况下
> 被创建。先下载，再运行，这样失败的获取会让该步骤失败：
> >
> > ```yaml
> > setup:
> >   install:
> >     - command: "curl -fsSL https://example.com/install.sh -o /tmp/install.sh && bash /tmp/install.sh"
> >       user: "1000"
> > ```

## 定制 shell 环境

某些工具安装到版本化目录中，并期望你从 shell 配置文件中 source 一个初始化脚本，使其
命令进入 `PATH`。版本管理器如 [nvm](https://github.com/nvm-sh/nvm) 和
[SDKMAN!](https://sdkman.io/) 遵循此模式。要让该工具在每个 shell 中都可用，请将 source
行追加到安装命令中的 `/etc/sandbox-persistent.sh`。

`/etc/sandbox-persistent.sh` 是沙箱的持久环境文件。它在每次 bash 调用之前被 source——包括
交互式 shell 和非交互式 shell，包括用 `sbx run` 启动的 agent 和用 `sbx exec` 运行的命令。
追加到这里使该工具对 agent 可用，无论其 shell 如何启动。同一个文件也是你设置自定义
环境变量的地方；请参阅
[FAQ](../faq.md#how-do-i-set-custom-environment-variables-inside-a-sandbox)。

```yaml {title="nvm/spec.yaml"}
schemaVersion: "2"
kind: mixin
name: nvm
displayName: nvm
description: Node version manager available in every shell

setup:
  install:
    - command: "curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash"
      user: "1000"
      description: Install nvm
    - command: |
        cat >> /etc/sandbox-persistent.sh <<'EOF'
        export NVM_DIR="$HOME/.nvm"
        unset NPM_CONFIG_PREFIX
        [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
        EOF
      user: "1000"
      description: Source nvm for every shell
```

两个安装步骤都以 `user: "1000"` 运行。这会把工具安装在 `/home/agent/` 下，并可以更新
`/etc/sandbox-persistent.sh`，该文件由 agent 用户拥有。追加行中的 `$HOME` 在 source 时按
用户解析，因此 agent 用户找到它自己的安装。追加到该文件而不是覆盖它——沙箱依赖其现有内容。

基础镜像自带自己的 Node 并设置了 `NPM_CONFIG_PREFIX`，nvm 不会与之一起激活。在 source
`nvm.sh` 之前 `unset NPM_CONFIG_PREFIX` 可清除该冲突。source 使 `nvm` 命令可用；它不会把
某个 Node 版本放到 `PATH` 上。运行 `nvm install --lts` 来添加一个——如果你把它作为安装步骤
脚本化，请包裹在 `bash -c '…'` 中，因为安装步骤在 `sh` 下运行。

只追加初始化脚本，不要追加工具的 tab 补全脚本。因为 `/etc/sandbox-persistent.sh` 在每次
命令之前被 source，补全脚本——依赖仅在补全期间存在的变量——可能破坏 agent 依赖的非交互式
shell。

## 安装内部 CA 证书

如果你的组织使用一个检查 HTTPS 流量的代理，请在沙箱信任存储中安装该代理的内部根 CA。
这有助于 agent 和 SDK 信任由代理签名的证书。

```text
internal-ca/
├── spec.yaml
└── files/
    └── home/
        └── internal-ca.crt
```

使用扩展名为 `.crt` 的 PEM 编码证书。`files/home/` 下的文件落入沙箱中的 `/home/agent/`，
因此 `files/home/internal-ca.crt` 变为 `/home/agent/internal-ca.crt`——这正是安装命令读取的
路径。如果流量可能由多个内部代理签名，请在 kit 中包括每个代理的根 CA，并在运行
`update-ca-certificates` 之前安装每个证书。

```yaml {title="internal-ca/spec.yaml"}
schemaVersion: "2"
kind: mixin
name: internal-ca

setup:
  install:
    - command: "install -m 0644 /home/agent/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt && update-ca-certificates"
      user: "0"
      description: Install internal CA certificate
```

`update-ca-certificates` 将证书添加到系统信任存储，因此读取系统 bundle 的工具和 SDK 无需
进一步配置即可信任代理的证书。

## 运行后台服务

`setup.startup` 在每次沙箱启动时运行。要让像开发服务器或守护进程这样的长运行服务保持存活，
设置 `background: true`。沙箱在后台运行该命令，并在每次启动时重放启动命令，因此服务在
停止/启动循环后会恢复：

```yaml
setup:
  startup:
    - command: ["my-service", "--port", "8080"]
      user: "1000"
      background: true
```

后台服务不会写入你的终端。要捕获其输出用于调试，请将命令包裹在 shell 中并重定向到日志文件。
让 `background: true` 在后台运行命令，而不是自己添加尾随的 `&`：

```yaml
setup:
  startup:
    - command:
        - sh
        - -c
        - my-service --port 8080 > /tmp/my-service.log 2>&1
      user: "1000"
      background: true
```

一个空日志文件告诉你包装器运行了；一个被填充的日志文件告诉你服务为何失败。

## 将运行时值写入文件

当配置文件需要一个直到沙箱启动才知道的值——最常见的是绝对 workspace 路径——使用
`setup.files`。`${WORKDIR}` 占位符在写入文件时展开为主要的 workspace 路径。

```yaml
setup:
  files:
    - path: /home/agent/.local/bin/start-code-server.sh
      content: |
        exec code-server --bind-addr 0.0.0.0:8080 --auth none "${WORKDIR}"
      mode: "0755"
  startup:
    - command:
        - sh
        - -c
        - nohup /home/agent/.local/bin/start-code-server.sh > /tmp/code-server.log 2>&1 &
      user: "1000"
```

`mode: "0755"` 使生成的文件可执行，以便启动命令可以直接调用它。

只要内容依赖于运行时值，就使用 `setup.files` 而非静态文件。否则使用静态文件。

> [!TIP]
> 此片段取自 contrib 仓库中的
> [code-server kit](https://github.com/docker/sbx-kits-contrib/tree/main/code-server)，
> 它也是一个可运行的示例，演示了完整模式。

## 分发一个 Claude Code skill

Claude Code 从 workspace 中的 `.claude/skills/<name>/SKILL.md` 读取项目级 skill。将
一个放入 `files/workspace/`，它在沙箱中就可用了。

```text
docker-review/
├── spec.yaml
└── files/
    └── workspace/
        └── .claude/
            └── skills/
                └── docker-review/
                    └── SKILL.md
```

```yaml {title="docker-review/spec.yaml"}
schemaVersion: "2"
kind: mixin
name: docker-review
displayName: Dockerfile review skill
description: Ships a Claude Code skill that reviews Dockerfiles
```

```markdown {title="docker-review/files/workspace/.claude/skills/docker-review/SKILL.md"}
---
name: docker-review
description: Review a Dockerfile for best practices. Use when the user asks to review, audit, or improve a Dockerfile.
---

When reviewing a Dockerfile, check:

1. Base image — pinned tag or digest, appropriate for the workload
2. Layer order — dependencies copied before application source
3. Image size — multi-stage builds, `.dockerignore`, package-manager cache flags
4. Security — non-root `USER`, no secrets in `ARG`/`ENV`
5. Reproducibility — pinned package versions, frontend directive where relevant
```

kit 必须以 workspace 为目标而不是 `~/.claude/`，因为沙箱不会从宿主机获取用户级的 agent
配置。详见 [FAQ](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

## 定制 agent 设置

某些 agent 从多个文件合并设置。当 agent 支持时，将 kit 设置放在单独的文件中，而不是
替换 [沙箱管理的 agent 配置](kits.md#sandbox-managed-agent-configuration)。

Claude Code 的 `--settings` 选项加载一个额外的设置文件。扩展内置的 `claude` kit 以添加
该选项而无需复制其配置，并将额外的文件放在沙箱管理的路径之外：

```text
claude-sonnet/
├── spec.yaml
└── files/
    └── home/
        └── .config/
            └── claude/
                └── sonnet.json
```

```yaml {title="claude-sonnet/spec.yaml"}
schemaVersion: "2"
kind: sandbox
name: claude-sonnet
extends: claude

sandbox:
  command:
    - --dangerously-skip-permissions
    - --settings
    - /home/agent/.config/claude/sonnet.json
```

```json {title="claude-sonnet/files/home/.config/claude/sonnet.json"}
{
  "model": "sonnet"
}
```

Claude Code 将额外的文件与沙箱管理的用户设置合并。因为该文件在 `files/home/` 下，它会留在
沙箱内，而不是被写入直接挂载的宿主机 workspace。用子 kit 的名字启动沙箱：

```console
$ sbx run claude-sonnet --kit ./claude-sonnet
```

OpenCode 通过 `OPENCODE_CONFIG` 支持一个额外的配置文件。将 kit 的配置与沙箱管理的
`/home/agent/.config/opencode/opencode.json` 分开，例如放在
`/home/agent/.config/opencode/team.json`：

```text
opencode-team/
├── spec.yaml
└── files/
    └── home/
        └── .config/
            └── opencode/
                └── team.json
```

```yaml {title="opencode-team/spec.yaml"}
schemaVersion: "2"
kind: mixin
name: opencode-team
requires:
  agent: opencode

environment:
  variables:
    OPENCODE_CONFIG: /home/agent/.config/opencode/team.json
```

```json {title="opencode-team/files/home/.config/opencode/team.json"}
{
  "$schema": "https://opencode.ai/config.json",
  "autoupdate": false
}
```

OpenCode 将自定义文件与其全局和项目配置文件合并。完整的顺序请参阅 OpenCode 的
[配置优先级](https://opencode.ai/docs/config/#precedence-order)。

agent 设置机制各不相同。如果某个 agent 不支持用于该设置的额外配置文件、启动选项或环境
变量，kit 无法在 agent 启动前替换沙箱管理的用户设置。`setup.startup` 不会门控 agent 入口点，
因此不要用它来设置 agent 在初始化期间必须读取的配置。

## Fork 一个现有 agent

Sandbox kit（`kind: sandbox`）从零定义一个完整的 agent。最常见的变体是内置 agent 的 fork。
使用 `extends:` 继承父级的完整配置，并仅声明你想更改的字段。此示例替换内置的 `claude`
入口点，使 Claude Code 使用手动权限模式而非绕过审批提示：

```yaml {title="claude-safe/spec.yaml"}
schemaVersion: "2"
kind: sandbox
name: claude-safe
displayName: Claude Code (with approval prompts)
description: Claude Code in manual permission mode

extends: claude

sandbox:
  entrypoint: [claude, "--permission-mode", "manual"]
```

子级继承了内置镜像、凭据、网络权限、持久卷、设置、MCP 集成和 agent 指令。它的
`sandbox.entrypoint` 替换继承的入口点。

用 kit 的 `name:` 作为 `sbx run` 的 agent 参数启动：

```console
$ sbx run claude-safe --kit ./claude-safe
```

有关从零构建新 sandbox kit 的逐步讲解，请参阅 [构建 agent](build-an-agent.md)。

## 更多示例

这些模式都取自 [sbx-kits-contrib](https://github.com/docker/sbx-kits-contrib) 仓库中可用的
kit，其中每个示例都是一个完整、可加载的 kit。用它来研究 kit 的完整形态，或直接加载一个：

```console
$ sbx run claude --kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=<kit>"
```

