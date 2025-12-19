---
title: 配置 Claude Code
description: 了解如何配置 Claude Code 身份验证、传递 CLI 选项，以及使用 Docker 自定义沙盒代理环境。
weight: 30
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

本指南介绍在沙盒环境中运行 Claude Code 的身份验证、配置文件和常用选项。

## 快速入门

在沙盒中启动 Claude 的最简单方法：

```console
$ docker sandbox run claude
```

这将启动一个沙盒化的 Claude Code 代理，并将当前工作目录作为其工作空间。

或者指定其他工作空间：

```console
$ docker sandbox run -w ~/my-project claude
```

## 向 Claude 传递 CLI 选项

Claude Code 支持各种命令行选项，您可以通过 `docker sandbox run` 传递这些选项。代理名称（`claude`）之后的任何参数都会直接传递给沙盒内的 Claude Code。

### 继续之前的对话

恢复您最近的对话：

```console
$ docker sandbox run claude -c
```

或者使用长格式：

```console
$ docker sandbox run claude --continue
```

### 直接传递提示

使用特定提示启动 Claude：

```console
$ docker sandbox run claude "为登录函数添加错误处理"
```

这将启动 Claude 并立即处理该提示。

### 组合选项

您可以将沙盒选项与 Claude 选项结合使用：

```console
$ docker sandbox run -e DEBUG=1 claude -c
```

这将创建一个 `DEBUG` 设置为 `1` 的沙盒，启用调试输出以便进行故障排除，并继续之前的对话。

### 可用的 Claude 选项

所有 Claude Code CLI 选项都可以通过 `docker sandbox run` 工作：

- `-c, --continue` - 继续最近的对话
- `-p, --prompt` - 从 stdin 读取提示（对管道操作很有用）
- `--dangerously-skip-permissions` - 跳过权限提示（在沙盒中默认启用）
- 以及更多选项 - 请参阅 [Claude Code 文档](https://docs.claude.com/en/docs/claude-code) 获取完整列表

## 身份验证

Claude 沙盒支持以下凭据管理策略。

### 策略 1：`sandbox`（默认）

```console
$ docker sandbox run claude
```

首次运行时，Claude 会提示您输入 Anthropic API 密钥。凭据存储在名为 `docker-claude-sandbox-data` 的持久 Docker 卷中。所有未来的 Claude 沙盒都会自动使用这些存储的凭据，并且它们在沙盒重启和删除后仍然保留。

沙盒将此卷挂载到 `/mnt/claude-data`，并在沙盒用户的主目录中创建符号链接。

> [!NOTE]
> 如果您的工作区包含带有 `primaryApiKey` 字段的 `.claude.json` 文件，您将收到关于潜在冲突的警告。您可以选择从 `.claude.json` 中移除 `primaryApiKey` 字段，或者继续并忽略该警告。

### 策略 2：`none`

不进行自动凭据管理。

```console
$ docker sandbox run --credentials=none claude
```

Docker 不会发现、注入或存储任何凭据。您必须在容器内手动进行身份验证。凭据不会与其他沙盒共享，但在容器的生命周期内会持续存在。

## 配置

Claude Code 可以通过 CLI 选项进行配置。您在代理名称后传递的任何参数都会直接传递给容器内的 Claude Code。

在代理名称后传递选项：

```console
$ docker sandbox run claude [claude-options]
```

例如：

```console
$ docker sandbox run claude --continue
```

请参阅 [Claude Code CLI 参考](https://docs.claude.com/en/docs/claude-code/cli-reference) 获取可用选项的完整列表。

## 高级用法

有关更高级的配置，包括环境变量、卷挂载、Docker 套接字访问和自定义模板，请参阅[高级配置](advanced-config.md)。

## 基础镜像

`docker/sandbox-templates:claude-code` 镜像包含具有自动凭据管理的 Claude Code，以及开发工具（Docker CLI、GitHub CLI、Node.js、Go、Python 3、Git、ripgrep、jq）。它以非 root 的 `agent` 用户身份运行，具有 `sudo` 访问权限，并默认使用 `--dangerously-skip-permissions` 启动 Claude。

## 下一步

- [高级配置](advanced-config.md)
- [故障排除](troubleshooting.md)
- [CLI 参考](/reference/cli/docker/sandbox/)