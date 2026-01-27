# 配置 Claude Code




本指南涵盖了在沙箱环境中运行 Claude Code 的身份验证、配置文件和常用选项。

## 快速开始

要为项目目录创建沙箱并运行 Claude Code：

```console
$ docker sandbox run claude ~/my-project
```

### 直接传递提示词

使用特定提示词启动 Claude：

```console
$ docker sandbox run <sandbox-name> -- "为登录功能添加错误处理"
```

或者：

```console
$ docker sandbox run <sandbox-name> -- "$(cat prompt.txt)"
```

这将启动 Claude 并立即处理提示词。

## 身份验证

Claude Code 需要一个 Anthropic API 密钥才能工作。推荐的方法是在 shell 配置文件中设置 `ANTHROPIC_API_KEY` 环境变量。

Docker Sandboxes 通过守护进程运行，不会继承当前 shell 会话的环境变量。为了使 API 密钥在沙箱中可用，您需要在 shell 配置文件中全局设置它。

将 API 密钥添加到您的 shell 配置文件：

```plaintext {title="~/.bashrc 或 ~/.zshrc"}
export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

然后应用更改：

1. 加载您的 shell 配置：`source ~/.bashrc`（或 `~/.zshrc`）
2. 重启 Docker Desktop，以便守护进程获取新的环境变量
3. 创建并运行您的沙箱：

```console
$ docker sandbox create claude ~/project
$ docker sandbox run <sandbox-name>
```

沙箱将检测环境变量并自动使用它。

### 交互式身份验证

如果未找到凭据，Claude Code 将在启动时提示您进行身份验证。使用此方法时，您需要为每个工作区分别进行身份验证。

为避免重复身份验证，请使用上述的 `ANTHROPIC_API_KEY` 环境变量方法。

## 配置

可以通过 CLI 选项配置 Claude Code。在沙箱名称和 `--` 分隔符之后传递的任何参数都会直接传递给 Claude Code。

在沙箱名称后传递选项：

```console
$ docker sandbox run <sandbox-name> -- [claude-options]
```

例如：

```console
$ docker sandbox run <sandbox-name> -- --continue
```

有关可用选项，请参阅 [Claude Code CLI 参考](https://docs.claude.com/en/docs/claude-code/cli-reference)。

## 基础镜像

Claude Code 沙箱模板是一个在沙箱虚拟机内运行的容器镜像。它包括：

- 基于 Ubuntu 的环境，包含 Claude Code
- 开发工具：Docker CLI、GitHub CLI、Node.js、Go、Python 3、Git、ripgrep、jq
- 具有 sudo 权限的非 root 用户 `agent`
- 用于运行其他容器的私有 Docker 守护进程

默认情况下，Claude 在沙箱中以 `--dangerously-skip-permissions` 启动。

您可以基于 `docker/sandbox-templates:claude-code` 构建自定义模板。有关详细信息，请参阅 [自定义模板](templates.md)。

## 后续步骤

- [有效使用沙箱](workflows.md)
- [自定义模板](templates.md)
- [网络策略](network-policies.md)
- [故障排除](troubleshooting.md)
- [CLI 参考](/reference/cli/docker/sandbox/)
