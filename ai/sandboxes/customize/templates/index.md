# Templates




每个沙箱都可定制——agent 在工作时安装包、拉取镜像、配置工具，这些更改在沙箱的生命周期内
持久保留。模板将一个配置好的环境捕获为可复用的镜像，这样你就不必每次都重新设置。

## 自定义模板

自定义模板是可复用的沙箱镜像，它通过烘焙进去的额外工具和配置来扩展某个内置的 agent 环境。
与其让 agent 每次都安装包，不如构建一次模板并在沙箱和团队成员之间复用它。

当多个人需要相同的环境、当设置包含繁琐到需要重复的步骤、或当你需要特定工具的固定版本时，
模板就很有意义。对于一次性工作，默认镜像就够了——让 agent 安装需要的东西。

> [!NOTE]
> 自定义模板定制的是已有 agent 的环境——它们不会创建新的 agent 运行时。在沙箱内启动的 agent
> 由你扩展的基础镜像变体和你在 `sbx run` 命令中指定的 agent 决定，而不是由模板中安装的二进制
> 决定。要从零定义一个新 agent，请参阅 [Kits](kits.md#define-an-agent)。

### 基础镜像

所有沙箱模板都发布为 `docker/sandbox-templates:<variant>`。它们基于 Ubuntu，并以具有 sudo
访问权限的非 root `agent` 用户运行。多数变体包含 Git、Docker CLI，以及常见的开发工具如
Node.js、Python、Go 和 Java。

| Variant               | Agent                                                                |
| --------------------- | -------------------------------------------------------------------- |
| `claude-code`         | [Claude Code](https://claude.ai/download)                            |
| `claude-code-minimal` | Claude Code with a minimal toolset (no Node.js, Python, Go, or Java) |
| `codex`               | [OpenAI Codex](https://github.com/openai/codex)                      |
| `copilot`             | [GitHub Copilot](https://github.com/github/copilot-cli)              |
| `cursor-agent`        | [Cursor](https://cursor.com/cli)                                     |
| `docker-agent`        | [Docker Agent](https://github.com/docker/docker-agent)               |
| `droid`               | [Droid](https://www.factory.ai)                                      |
| `gemini`              | [Gemini CLI](https://github.com/google-gemini/gemini-cli)            |
| `kiro`                | [Kiro](https://kiro.dev)                                             |
| `opencode`            | [OpenCode](https://opencode.ai)                                      |
| `shell`               | No agent pre-installed. Use for manual agent setup.                  |

每个变体也有一个 `-docker` 版本（例如 `claude-code-docker`），它包含运行在沙箱内的完整 Docker
Engine——无需本地 Docker 守护进程。当你选择内置 agent 而未指定自定义模板时，`sbx run` 和
`sbx create` 默认使用 `-docker` 模板变体。

从 `-docker` 模板创建的 agent 容器在 microVM 内（而非你的宿主机上）以特权模式运行，在
`/var/lib/docker` 有专用块卷，并且 `dockerd` 在沙箱内自动启动。块卷默认 50 GB 并使用稀疏文件，
因此只有当 Docker 写入它时才占用磁盘空间。

要覆盖卷大小，在启动沙箱前将 `DOCKER_SANDBOXES_DOCKER_SIZE` 环境变量设置为大小字符串：

```console
$ DOCKER_SANDBOXES_DOCKER_SIZE=10g sbx run claude
```

如果你不需要在沙箱内构建或运行容器，并想要更轻量、非特权的环境，请使用非 Docker 变体。用
`--template` 显式指定它：

```console
$ sbx run claude --template docker.io/docker/sandbox-templates:claude-code
```

### 构建自定义模板

构建自定义模板需要 [Docker Desktop](/manuals/desktop/_index.md)。

编写一个扩展某个基础镜像的 Dockerfile。选择与你计划运行的 agent 匹配的变体。例如，扩展
`claude-code` 来定制 Claude Code 环境，或扩展 `codex` 来定制 OpenAI Codex 环境。

以下示例创建了一个预装 Rust 和 protocol buffer 工具的 Claude Code 模板：

```dockerfile
FROM docker/sandbox-templates:claude-code
USER root
RUN apt-get update && apt-get install -y protobuf-compiler
USER agent
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

系统级包安装（`apt-get`）使用 `root`，在安装用户级工具前切换回 `agent`。安装到主目录的
工具，如 `rustup`、`nvm` 或 `pyenv`，必须以 `agent` 运行——否则它们安装在 `/root/` 下，在
沙箱内不可用。

构建镜像并推送到 OCI 仓库，例如 Docker Hub：

```console
$ docker build -t my-org/my-template:v1 --push .
```

> [!NOTE]
> Docker Sandboxes 使用的 Docker 守护进程直接从仓库拉取模板；它不共享宿主机上本地 Docker 守护
> 进程的镜像存储。

> [!IMPORTANT]
> 对于 Docker Hub，`sbx` 复用你的 `sbx login` 会话来拉取私有镜像。对于其他仓库（GitHub Container
> Registry、ECR、ACR、自托管的 Nexus 等），请在运行沙箱前用
> [`sbx secret set --registry`](../security/credentials.md#registry-credentials) 存储拉取
> 凭据：
> >
> > ```console
> > $ gh auth token | sbx secret set --registry ghcr.io --password-stdin
> > ```
> >
> > 没有存储的凭据时，从非 Docker Hub 仓库的拉取是匿名的，私有镜像会拉取失败。

对于本地构建的镜像，将镜像保存为 tar 并直接加载到沙箱运行时，而不是从仓库拉取：

```console
$ docker image save my-org/my-template:v1 -o my-template.tar
$ sbx template load my-template.tar
$ sbx run --template my-org/my-template:v1 claude
```

`sbx template load` 将 tar 导入沙箱运行时的镜像存储，因此镜像在沙箱创建时不需要从仓库可达。

除非你使用宽松的 `allow-all` 网络策略，否则你可能还需要将自定义工具依赖的任何域名加入
允许列表：

```console
$ sbx policy allow network "*.example.com:443,example.com:443"
```

然后用你的模板运行沙箱。你指定的 agent 必须匹配你模板扩展的基础镜像变体：

```console
$ sbx run --template docker.io/my-org/my-template:v1 claude
```

因为这个模板扩展 `claude-code` 基础镜像，你用 `claude` 运行它。如果你扩展 `codex`，用
`codex`；如果你扩展 `shell`，用 `shell`（它会把你放入没有 agent 的 Bash shell）。

> [!NOTE]
> 与 Docker 命令不同，`sbx` 不会在镜像引用中自动解析 Docker Hub 域名（`docker.io`）。

### 模板缓存

模板镜像在本地缓存。首次使用从仓库拉取；后续沙箱复用缓存。缓存的镜像在沙箱创建和删除之间
持久保留，并在你运行 `sbx reset` 时清除。

## 将沙箱保存为模板

除了编写 Dockerfile，你可以将运行中的沙箱状态保存为模板。这会将已安装的包、配置更改和文件
捕获到可复用的镜像中——当你交互式设置好一个环境并想保留它时很有用。

> [!WARNING]
> 保存沙箱会捕获其整个文件系统，包括存储在其上的任何秘密。如果你手动向沙箱添加了 API 密钥、
> token 或其他凭据，它们会被嵌入到保存的模板中，并与你分发的任何对象共享。要将凭据排除在模板
> 之外，请用 `sbx secret set` 管理它们——代理在运行时注入它们，因此它们永远不会写入文件系统。
> 更多信息请参阅 [管理凭据](../security/credentials.md)。

### 保存与复用

停止沙箱（或让 CLI 提示你），然后用名称和标签保存它：

```console
$ sbx template save my-sandbox my-template:v1
```

镜像存储在沙箱运行时的本地镜像存储中。用 `-t` 标志从中创建新沙箱：

```console
$ sbx run -t my-template:v1 claude
```

### 列出与移除模板

列出所有已保存的模板：

```console
$ sbx template ls
```

移除你不再需要的模板：

```console
$ sbx template rm my-template:v1
```

### 导出与导入

要分享已保存的模板或将其移动到另一台机器，将其导出为 tar 文件：

```console
$ sbx template save my-sandbox my-template:v1 --output my-template.tar
```

在另一台机器上，加载 tar 文件并使用它：

```console
$ sbx template load my-template.tar
$ sbx run -t my-template:v1 claude
```

### 限制

agent 配置文件在创建沙箱时总是被重新创建。对用户级 agent 配置文件（如
`/home/agent/.claude/settings.json` 和 `/home/agent/.claude.json`）的更改不会在保存的模板中
持久保留。

如果保存的模板是为与你在 `sbx run` 中指定的 agent 不同的 agent 构建的，你会收到警告。例如，
保存一个 Claude 沙箱并用 `codex` 运行它会产生：

```text
⚠ WARNING: template "my-template:v1" was built for the "claude" agent but you are using "codex".
  The sandbox may not work correctly. Consider using: sbx run -t my-template:v1 claude
```

