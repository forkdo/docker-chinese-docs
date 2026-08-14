# Claude Code


官方文档：[Claude Code](https://code.claude.com/docs)

## 快速开始

通过指定项目目录，在沙箱中启动 Claude Code：

```console
$ sbx run claude ~/my-project
```

工作空间参数默认为当前目录，因此在项目目录内直接运行 `sbx run claude` 也可以。若要以特定提示词启动 Claude：

```console
$ sbx run claude --name my-sandbox -- "Add error handling to the login function"
```

`--` 之后的所有内容都会直接传递给 Claude Code。您也可以用 `-- "$(cat prompt.txt)"` 从文件中管道传入提示词。

## 身份验证

Claude Code 需要使用 Anthropic API 密钥或 Claude 订阅。

**API 密钥**：使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的密钥：

```console
$ sbx secret set anthropic
```

**Claude 订阅**：如果未设置 API 密钥，可在 Claude Code 内使用 `/login` 命令通过 OAuth 进行身份验证。

## 配置

沙箱不会获取您主机上的用户级配置（例如 `~/.claude`）。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

### Default startup command

不带额外参数时，沙箱运行：

```text
claude --dangerously-skip-permissions
```

当 `--` 之后的第一个参数本身就是一个标志（以 `-` 开头）时，该参数会被追加到默认标志之后，因此 `--dangerously-skip-permissions` 得以保留：

```console
$ sbx run claude -- -c   # 运行 claude --dangerously-skip-permissions -c
```

当第一个参数是裸词（例如 `agents` 子命令）时，它会替换默认值。

可用选项请参阅 [Claude Code CLI 参考](https://code.claude.com/docs/en/cli-reference)。

## Agents view

Claude Code 的 [agents view](https://code.claude.com/docs/en/agent-view)
会启动在后台并行运行任务的会话。将其与
[克隆模式](../workflows.md#clone-mode)搭配使用，可以让这些会话的改动保留在沙箱内：

```console
$ sbx run --clone claude -- agents
```

此调用会替换[默认启动命令](#default-startup-command)，因此其中不包含 `--dangerously-skip-permissions`，您也无法在沙箱内部切换到跳过权限模式。要解决此问题，可使用 Claude Code 的自动模式，或显式传入该标志：

```console
$ sbx run --clone claude -- --dangerously-skip-permissions agents
```

Claude Code 可能会使用分支或工作树（worktree）来隔离其后台会话的改动。这取决于具体的任务、Claude Code 配置以及项目指令。`--clone` 标志并不控制此行为。Claude Code 会在沙箱内（而非您主机的检出目录中）创建这些分支和工作树。

要查看某次会话创建的分支，请从主机获取 `sandbox-<sandbox-name>` 远程：

```console
$ git fetch sandbox-<sandbox-name>
$ git diff main..sandbox-<sandbox-name>/<branch>
```

有关克隆模式的详情，请参阅 [Git 工作流](../workflows.md#git-workflows)。

## Base image

沙箱使用 `docker/sandbox-templates:claude-code`。如需在此基础之上构建您自己的镜像，请参阅
[模板](../customize/templates.md)。

## 使用本地模型

`--model` 标志会将 Claude Code 的 Anthropic API 请求路由到运行在您主机上的模型。该功能为实验性功能，不支持 Windows。

启用该功能：

```console
$ sbx settings set platform.allowExperimentalFeatures true
$ sbx settings set feature.model true
```

要使用内置的 `llmman` 模型服务器，可传入一个 GGUF 模型引用或简称：

```console
$ sbx run --model gemma4 claude
```

首次使用时，`sbx` 会启动 `llmman`、拉取模型，并在您主机上保持该服务器运行。后续沙箱会复用该服务器及其模型存储。

若要改用已有的 Ollama 安装，请在模型名称前加上 `ollama/` 前缀：

```console
$ sbx run --model ollama/gemma4 claude
```

Ollama 必须已安装并正在运行。`sbx` 会连接到它，但不会启动或管理 Ollama 进程。

您也可以为已有的沙箱更改模型：

```console
$ sbx run --name <sandbox-name> --model <model-name>
```

更改模型会重新创建沙箱容器。工作空间和由套件（kit）拥有的卷会保留。

若要改用 Docker Model Runner，请参阅
[在 Docker 沙箱中使用 Docker Model Runner 运行 Claude Code](/guides/claude-code-sandbox-model-runner/)。
