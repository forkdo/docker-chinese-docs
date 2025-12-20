# 模型提供商

要运行 cagent，您需要一个模型提供商。您可以使用带有 API 密钥的云提供商，也可以通过 [Docker Model
Runner](local-models.md) 本地运行模型。

本指南介绍云提供商。有关本地替代方案，请参阅 [使用 Docker Model Runner 运行本地模型](local-models.md)。

## 支持的提供商

cagent 支持以下云模型提供商：

- Anthropic - Claude 模型
- OpenAI - GPT 模型
- Google - Gemini 模型

## Anthropic

Anthropic 提供 Claude 系列模型，包括 Claude Sonnet 和 Claude Opus。

获取 API 密钥：

1. 访问 [console.anthropic.com](https://console.anthropic.com/)。
2. 注册或登录您的账户。
3. 导航至 API Keys 部分。
4. 创建一个新的 API 密钥。
5. 复制该密钥。

将您的 API 密钥设置为环境变量：

```console
$ export ANTHROPIC_API_KEY=your_key_here
```

在您的 agent 配置中使用 Anthropic 模型：

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

获取 API 密钥：

1. 访问 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)。
2. 注册或登录您的账户。
3. 导航至 API Keys 部分。
4. 创建一个新的 API 密钥。
5. 复制该密钥。

将您的 API 密钥设置为环境变量：

```console
$ export OPENAI_API_KEY=your_key_here
```

在您的 agent 配置中使用 OpenAI 模型：

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

获取 API 密钥：

1. 访问 [aistudio.google.com/apikey](https://aistudio.google.com/apikey)。
2. 使用您的 Google 账户登录。
3. 创建一个 API 密钥。
4. 复制该密钥。

将您的 API 密钥设置为环境变量：

```console
$ export GOOGLE_API_KEY=your_key_here
```

在您的 agent 配置中使用 Gemini 模型：

```yaml
agents:
  root:
    model: google/gemini-2.5-flash
    instruction: You are a helpful coding assistant
```

可用模型包括：

- `google/gemini-2.5-flash`
- `google/gemini-2.5-pro`

## OpenAI 兼容的提供商

您可以使用 `openai` 提供商类型连接到任何实现了 OpenAI API 规范的模型或提供商。这包括 Azure OpenAI、本地推理服务器和其他兼容端点等服务。

通过指定 base URL 来配置 OpenAI 兼容的提供商：

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
```

默认情况下，cagent 使用 `OPENAI_API_KEY` 环境变量进行身份验证。如果您的提供商使用不同的变量，请使用 `token_key` 指定：

```yaml
agents:
  root:
    model: openai/your-model-name
    instruction: You are a helpful coding assistant
    provider:
      base_url: https://your-provider.example.com/v1
      token_key: YOUR_PROVIDER_API_KEY
```

## 后续步骤

- 遵循 [教程](tutorial.md) 构建您的第一个 agent
- 了解 [使用 Docker Model Runner 运行本地模型](local-models.md)，作为云提供商的替代方案
- 查阅 [配置参考](reference/config.md) 以了解高级模型设置
