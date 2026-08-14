---
title: 将 Claude Code 与 Docker Model Runner 配合使用
description: 配置 Claude Code 以使用 Docker Model Runner，从而可以使用本地模型进行编码。
summary: '通过兼容 Anthropic 的 API 将 Claude Code 连接到 Docker Model Runner，

  打包具有更大上下文窗口的 `gpt-oss`，并检查请求。

  '
keywords: ai, claude code, docker model runner, anthropic, local models, coding assistant
params:
  tags: [ai]
  time: 10 minutes
---

本指南展示如何将 Claude Code 以 Docker Model Runner 作为后端模型提供者来运行。您将把 Claude Code 指向本地兼容 Anthropic 的 API、运行一个编码模型，并打包具有更大上下文窗口的 `gpt-oss`，以支持更长的仓库提示。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

在本指南中，您将学习如何：

- 拉取一个编码模型并启动带有 Docker Model Runner 的 Claude Code
- 使端点配置持久化
- 验证本地 API 端点并检查请求
- 打包具有更大上下文窗口的 `gpt-oss`，以支持更长的提示

## 先决条件

在开始之前，请确保您已具备：

- 已安装 [Docker Desktop](../get-started/get-docker.md) 或 Docker Engine
- 已[启用 Docker Model Runner](../manuals/ai/model-runner/get-started.md#enable-docker-model-runner)
- 已[安装 Claude Code](https://code.claude.com/docs/en/quickstart)

如果您使用 Docker Desktop，请在 **设置** > **AI** 中打开 TCP 访问，或运行：

```console
$ docker desktop enable model-runner --tcp 12434
```

## 步骤 1：拉取编码模型

在启动 Claude Code 之前先拉取一个模型：

```console
$ docker model pull ai/devstral-small-2
```

如果您想要另一个具有大上下文窗口、专注于编码的模型，也可以使用 `ai/qwen3-coder`。

## 步骤 2：使用 Docker Model Runner 启动 Claude Code

在运行 Claude Code 时，将 `ANTHROPIC_BASE_URL` 设置为您本地的 Docker Model Runner 端点。

在 macOS 或 Linux 上：

```console
$ ANTHROPIC_BASE_URL=http://localhost:12434 claude --model ai/devstral-small-2
```

在 Windows PowerShell 上：

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:12434"
claude --model ai/devstral-small-2
```

Claude Code 现在会将请求发送到 Docker Model Runner，而不是 Anthropic 的托管 API。

## 步骤 3：排查首次启动问题

如果 Claude Code 无法连接，请检查 Docker Model Runner 的状态：

```console
$ docker model status
```

如果 Claude Code 找不到模型，请列出本地模型：

```console
$ docker model ls
```

如果模型缺失，请先拉取它。如有需要，请使用完整的模型名称，例如 `ai/devstral-small-2`。

## 步骤 4：使端点持久化

为了避免每次都设置环境变量，请将其添加到您的 shell 配置文件中：

```bash {title="~/.bashrc 或 ~/.zshrc"}
export ANTHROPIC_BASE_URL=http://localhost:12434
```

在 Windows PowerShell 上，将其添加到您的 PowerShell 配置文件中：

```powershell {title="$PROFILE"}
$env:ANTHROPIC_BASE_URL = "http://localhost:12434"
```

重新加载 shell 后，您只需使用模型标志即可运行 Claude Code：

```console
$ claude --model ai/devstral-small-2
```

## 步骤 5：验证 API 端点

发送一个测试请求以确认兼容 Anthropic 的 API 可达：

```console
$ curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/devstral-small-2",
    "max_tokens": 32,
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

有关请求格式的更多详细信息，请参阅 [兼容 Anthropic 的 API 参考](../manuals/ai/model-runner/api-reference.md#anthropic-compatible-api)。

## 步骤 6：检查 Claude Code 请求

要检查 Claude Code 发送到 Docker Model Runner 的请求，请运行：

```console
$ docker model requests --model ai/devstral-small-2 | jq .
```

这有助于您调试提示、上下文使用情况以及兼容性问题。

## 步骤 7：打包具有更大上下文窗口的 `gpt-oss`

`ai/gpt-oss` 默认使用比专注于编码的模型更小的上下文窗口。如果您想将其用于仓库级别的提示，请打包一个更大的变体：

```console
$ docker model pull ai/gpt-oss
$ docker model package --from ai/gpt-oss --context-size 32000 gpt-oss:32k
```

然后使用打包后的模型运行 Claude Code：

```console
$ ANTHROPIC_BASE_URL=http://localhost:12434 claude --model gpt-oss:32k
```

## 了解更多

- [Docker Model Runner 概述](../manuals/ai/model-runner/_index.md)
- [Docker Model Runner API 参考](../manuals/ai/model-runner/api-reference.md)
- [IDE 和工具集成](../manuals/ai/model-runner/ide-integrations.md)
