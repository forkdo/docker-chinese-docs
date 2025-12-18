---
title: 配置 Claude Code
description: 了解如何配置 Claude Code 的身份验证、传递 CLI 选项，以及使用 Docker 自定义沙盒代理环境。
weight: 30
---

{{< summary-bar feature_name="Docker 沙盒" >}}

本指南涵盖在沙盒环境中运行 Claude Code 的身份验证、配置文件和常用选项。

## 快速开始

在沙盒中启动 Claude 的最简单方法：

```console
$ docker sandbox run claude
```

这将使用当前工作目录作为工作空间启动一个沙盒化的 Claude Code 代理。

或者指定不同的工作空间：

```console
$ docker sandbox run -w ~/my-project claude
```

## 向 Claude 传递 CLI 选项

Claude Code 支持各种命令行选项，您可以通过 `docker sandbox run` 传递这些选项。代理名称（`claude`）之后的任何参数都会直接传递给沙盒内的 Claude Code。

### 继续之前的对话

恢复最近的对话：

```console
$ docker sandbox run claude -c
```

或使用长格式：

```console
$ docker sandbox run claude --continue
```

### 直接传递提示

使用特定提示启动 Claude：

```console
$ docker sandbox run claude "为登录功能添加错误处理"
```

这将启动 Claude 并立即处理该提示。

### 组合选项

您可以组合沙盒选项和 Claude 选项：

```console
$ docker sandbox run -e DEBUG=1 claude -c
```

这将创建一个 `DEBUG` 设置为 `1` 的沙盒，启用调试输出以进行故障排除，并继续之前的对话。

### 可用的 Claude 选项

所有 Claude Code CLI 选项都可通过 `docker sandbox run` 使用：

- `-c, --continue` - 继续最近的对话
- `-p, --prompt` - 从标准输入读取提示（对管道操作很有用）
- `--dangerously-skip-permissions` - 跳过权限提示（在沙盒中默认启用）
- 更多选项 - 请参阅 [Claude Code 文档](https://docs.claude.com/en/docs/claude-code) 了解完整列表

## 身份验证

Claude 沙盒支持以下凭据管理策略。

### 策略 1：`sandbox`（默认）

```console
$ docker sandbox run claude
```

首次运行时，Claude 会提示您输入 Anthropic API 密钥。凭据存储在名为 `docker-claude-sandbox-data` 的持久化 Docker 卷中。所有未来的 Claude 沙盒都会自动使用这些存储的凭据，且它们在沙盒重启和删除后仍然存在。

沙盒将此卷挂载在 `/mnt/claude-data` 处，并在沙盒用户主目录中创建符号链接。

> [!NOTE]
> 如果您的工作空间包含带有 `primaryApiKey` 字段的 `.claude.json` 文件，您会收到关于潜在冲突的警告。您可以选择从 `.claude.json` 中删除 `primaryApiKey` 字段，或继续并忽略该警告。

### 策略 2：`none`

不进行自动凭据管理。

```console
$ docker sandbox run --credentials=none claude
```

Docker 不会发现、注入或存储任何凭据。您必须在容器内手动进行身份验证。凭据不会与其他沙盒共享，但会在容器生命周期内保持。

## 配置

Claude Code 可通过 CLI 选项进行配置。您在代理名称后传递的任何参数都会直接传递给容器内的 Claude Code。

在代理名称后传递选项：

```console
$ docker sandbox run claude [claude-options]
```

例如：

```console
$ docker sandbox run claude --continue
```

请参阅 [Claude Code CLI 参考](https://docs.claude.com/en/docs/claude-code/cli-reference) 了解可用选项的完整列表。

## 高级用法

有关环境变量、卷挂载、Docker 套接字访问和自定义模板等高级配置，请参阅 [高级配置](advanced-config.md)。

## 基础镜像

`docker/sandbox-templates:claude-code` 镜像包含 Claude Code 和自动凭据管理，以及开发工具（Docker CLI、GitHub CLI、Node.js、Go、Python 3、Git、ripgrep、jq）。它以非 root 的 `agent` 用户身份运行，具有 `sudo` 访问权限，并默认使用 `--dangerously-skip-permissions` 启动 Claude。

## 后续步骤

- [高级配置](advanced-config.md)
- [故障排除](troubleshooting.md)
- [CLI 参考](/reference/cli/docker/sandbox/)