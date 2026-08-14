---
title: OpenCode
weight: 60
description: |
  在 Docker 沙箱中使用 OpenCode，支持多提供商身份验证和 TUI
  界面，用于 AI 开发。
keywords: docker sandboxes, opencode, ai agent, authentication, sbx
---

本指南涵盖在沙箱环境中使用 OpenCode 的身份验证、配置与操作方法。

官方文档：[OpenCode](https://opencode.ai/docs)

## 快速开始

创建沙箱并为项目目录运行 OpenCode：

```console
$ sbx run opencode ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run opencode
```

OpenCode 会启动一个 TUI（文本用户界面），您可以在其中选择偏好的 LLM 提供商并与代理交互。

## 身份验证

OpenCode 支持多个提供商。使用[存储的密钥](../security/credentials.md#stored-secrets)为您想要使用的提供商保存密钥：

```console
$ sbx secret set openai
$ sbx secret set anthropic
$ sbx secret set google
$ sbx secret set xai
$ sbx secret set groq
$ sbx secret set aws
$ sbx secret set openrouter
```

您只需配置想要使用的提供商。OpenCode 会检测可用的凭据，并在 TUI 中提供这些提供商。

### OpenCode Zen API 密钥

OpenCode Zen API 密钥不属于 `sbx secret set` 所支持的内置 OpenCode 凭据。若要使用 OpenCode Zen API 密钥，请将其作为[自定义密钥](../security/credentials.md#custom-secrets)保存：

在主机上设置 `OPENCODE_API_KEY` 环境变量，然后保存它：

```console
$ sbx secret set-custom \
    --host opencode.ai \
    --env OPENCODE_API_KEY \
    --value "$OPENCODE_API_KEY"
```

自定义密钥会将真实密钥保留在主机密钥库中。沙箱接收的是 `OPENCODE_API_KEY` 的占位符，主机端代理会在发往 `opencode.ai` 的请求中将该占位符替换为真实密钥。

OpenCode Zen 还需要对 `opencode.ai` 的网络访问权限：

```console
$ sbx policy allow network opencode.ai:443
```

如果您添加了全局自定义密钥，请重新创建已有的 OpenCode 沙箱，以便新的环境变量在沙箱内部可用。

## 配置

沙箱不会获取您主机上的用户级配置。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

OpenCode 使用 TUI 界面，不需要大量的配置文件。代理在启动时会提示您选择提供商，您也可以在一次会话中切换提供商。

### Default startup command

沙箱运行 `opencode`，不带任何隐式标志。`--` 之后的参数会直接透传。例如，要恢复一个已有的会话：

```console
$ sbx run opencode -- -s <session-id>
```

### TUI 模式

OpenCode 默认以 TUI 模式启动。界面会显示：

- 可用的 LLM 提供商（基于已配置的凭据）
- 当前会话历史
- 文件操作与工具使用情况
- 实时的代理响应

使用键盘快捷键在界面中导航并与代理交互。

## Base image

模板：`docker/sandbox-templates:opencode`

OpenCode 支持多个 LLM 提供商，并通过沙箱代理自动注入凭据。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。