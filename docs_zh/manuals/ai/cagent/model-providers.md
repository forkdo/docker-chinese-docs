---
title: 模型提供商
description: 获取 API 密钥并配置云模型提供商以使用 cagent
keywords: [cagent, 模型提供商, api 密钥, anthropic, openai, google, gemini]
weight: 10
---

要运行 cagent，你需要一个模型提供商。你可以使用带有 API 密钥的云提供商，也可以使用 [Docker Model Runner](local-models.md) 在本地运行模型。

本指南涵盖云提供商。如需本地替代方案，请参阅 [使用 Docker Model Runner 运行本地模型](local-models.md)。

## 支持的提供商

cagent 支持以下云模型提供商：

- Anthropic - Claude 模型
- OpenAI - GPT 模型
- Google - Gemini 模型

## Anthropic

Anthropic 提供 Claude 系列模型，包括 Claude Sonnet 和 Claude Opus。

获取 API 密钥的方法：

1. 访问 [console.anthropic.com](https://console.anthropic.com/)。
2. 注册或登录你的账户。
3. 导航到 API Keys 部分。
4. 创建一个新的 API 密钥。
5. 复制该密钥。

将你的 API 密钥设置为环境变量：

```console
$ export ANTHROPIC_API_KEY=your_key_here
```

在你的代理配置中使用 Anthropic 模型：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    instruction: You are a helpful coding assistant
```

可用模型包括：

- `anthropic/claude-sonnet-4-5`
- `anthropic/claude-opus-4-5`
- `anthropic/claude-haiku-4-5`

## OpenAI

OpenAI 提供 GPT 系列模型，包括 GPT-5 和 GPT-5 mini。

获取 API 密钥的方法：

1. 访问 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)。
2. 注册或登录你的账户。
3. 导航到 API Keys 部分。
4. 创建一个新的 API 密钥。
5. 复制该密钥。

将你的 API 密钥设置为环境变量：

```console
$ export OPENAI_API_KEY=your_key_here
```

在你的代理配置中使用 OpenAI 模型：

```yaml
agents:
  root:
    model: openai/gpt-5
    instruction: You are a helpful coding assistant
```

可用模型包括：

- `openai/gpt-5`
- `openai/gpt-5-mini`

## Google Gemini

Google 提供 Gemini 系列模型。

获取 API 密钥的方法：

1. 访问 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)。
2. 使用你的 Google 账户登录。
3. 创建一个 API 密钥。
4. 复制该密钥。

将你的 API 密钥设置为环境变量：

```console
$ export GOOGLE_API_KEY=your_key_here
```

在你的代理配置中使用 Gemini 模型：

```yaml
agents:
  root:
    model: google/gemini-2.5-flash
    instruction: You are a helpful coding assistant
```

可用模型包括：

- `google/gemini-2.5-flash`
- `google/gemini-2.5-pro`

## OpenAI 兼容提供商

你可以使用 `openai` 提供商类型连接到任何实现 OpenAI API 规范的模型或提供商。这包括 Azure OpenAI、本地推理服务器和其他兼容端点。

通过指定基础 URL 来配置 OpenAI 兼容提供商：

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
```

默认情况下，cagent 使用 `OPENAI_API_KEY` 环境变量进行身份验证。如果你的提供商使用不同的变量，请使用 `token_key` 指定：

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
      token_key: YOUR_PROVIDER_API_KEY
```

## 下一步

- 按照 [教程](tutorial.md) 构建你的第一个代理
- 了解 [使用 Docker Model Runner 运行本地模型](local-models.md)，作为云提供商的替代方案
- 查看 [配置参考](reference/config.md) 了解高级模型设置