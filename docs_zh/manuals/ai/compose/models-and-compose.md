---
title: 在 Docker Compose 应用程序中定义 AI 模型
linkTitle: 在 Compose 中使用 AI 模型
description: 了解如何使用 models 顶级元素在 Docker Compose 应用程序中定义和使用 AI 模型
keywords: compose, docker compose, models, ai, machine learning, cloud providers, specification
weight: 10
---

{{< summary-bar feature_name="Compose models" >}}

Compose 允许您将 AI 模型定义为应用程序的核心组件，因此您可以将模型依赖项与服务一起声明，并在任何支持 Compose 规范的平台上运行应用程序。

## 先决条件

- Docker Compose v2.38 或更高版本
- 支持 Compose 模型的平台，例如 [Docker Model Runner (DMR)](/manuals/ai/model-runner/_index.md#requirements)。

## 什么是 Compose 模型？

Compose `models` 是在应用程序中定义 AI 模型依赖项的标准化方式。通过在 Compose 文件中使用 [`models` 顶级元素](/reference/compose-file/models.md)，您可以：

- 声明应用程序需要哪些 AI 模型
- 指定模型配置和要求
- 使应用程序可在不同平台之间移植
- 让平台处理模型配置和生命周期管理

## 基本模型定义

要在 Compose 应用程序中定义模型，请使用 `models` 顶级元素：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
```

此示例定义了：
- 一个名为 `chat-app` 的服务，它使用名为 `llm` 的模型
- 一个 `llm` 的模型定义，它引用 `ai/smollm2` 模型镜像

## 模型配置选项

模型支持各种配置选项：

```yaml
models:
  llm:
    model: ai/smollm2
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

常见配置选项包括：
- `model`（必需）：模型的 OCI 构件标识符。这是 Compose 通过模型运行器拉取和运行的镜像。
- `context_size`：定义模型的最大令牌上下文大小。

   > [!注意]
   > 每个模型都有自己的最大上下文大小。增加上下文长度时，
   > 请考虑您的硬件限制。通常，请尝试将上下文大小
   > 保持在满足您特定需求的最小可行值。

- `runtime_flags`：模型启动时传递给推理引擎的原始命令行标志列表。
   有关常用参数和示例，请参阅[配置选项](/manuals/ai/model-runner/configuration.md)。
- 通过扩展属性 `x-*` 可能还提供特定于平台的选项

> [!提示]
> 请参阅[常见运行时配置](#常见运行时配置)部分中的更多示例。

## 服务模型绑定

服务可以通过两种方式引用模型：短语法和长语法。

### 短语法

短语法是将模型绑定到服务的最简单方法：

```yaml
services:
  app:
    image: my-app
    models:
      - llm
      - embedding-model

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

使用短语法时，平台会根据模型名称自动生成环境变量：
- `LLM_URL` - 访问 LLM 模型的 URL
- `LLM_MODEL` - LLM 模型的模型标识符
- `EMBEDDING_MODEL_URL` - 访问 embedding-model 的 URL
- `EMBEDDING_MODEL_MODEL` - embedding-model 的模型标识符

### 长语法

长语法允许您自定义环境变量名称：

```yaml
services:
  app:
    image: my-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME
      embedding-model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_NAME

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

使用此配置，您的服务将收到：
- LLM 模型的 `AI_MODEL_URL` 和 `AI_MODEL_NAME`
- embedding 模型的 `EMBEDDING_URL` 和 `EMBEDDING_NAME`

## 平台可移植性

使用 Compose 模型的一个关键优势是可在支持 Compose 规范的不同平台之间移植。

### Docker Model Runner

当[启用 Docker Model Runner](/manuals/ai/model-runner/_index.md)时：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME

models:
  llm:
    model: ai/smollm2
    context_size: 4096
    runtime_flags:
      - "--no-prefill-assistant"
```

Docker Model Runner 将：
- 在本地拉取并运行指定的模型
- 提供用于访问模型的端点 URL
- 将环境变量注入服务

### 云提供商

Compose 模型规范是可移植的。实现了 Compose 规范的平台可以支持 `models` 顶级元素，从而允许同一份 Compose 文件在不同的基础设施上运行。可以使用扩展属性（`x-*`）配置特定于云的行为：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
    # 特定于云的配置
    x-cloud-options:
      - "cloud.instance-type=gpu-small"
      - "cloud.region=us-west-2"
```

平台如何处理模型定义取决于其实现。平台可能会：

- 使用托管 AI 服务而不是在本地运行模型
- 应用特定于平台的优化和扩展
- 提供额外的监控和日志记录功能
- 自动处理模型版本控制和更新

## 常见运行时配置

以下是各种用例的一些示例配置。

### 开发

```yaml
services:
  app:
    image: app
    models:
      dev_model:
        endpoint_var: DEV_URL
        model_var: DEV_MODEL

models:
  dev_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--verbose"                       # 将详细级别设置为无穷大
      - "--verbose-prompt"                # 在生成前打印详细提示
      - "--log-prefix"                    # 在日志消息中启用前缀
      - "--log-timestamps"                # 在日志消息中启用时间戳
      - "--log-colors"                    # 启用彩色日志记录
```

### 保守且禁用推理

```yaml
services:
  app:
    image: app
    models:
      conservative_model:
        endpoint_var: CONSERVATIVE_URL
        model_var: CONSERVATIVE_MODEL

models:
  conservative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # 温度
      - "0.1"
      - "--top-k"               # Top-k 采样
      - "1"
      - "--reasoning-budget"    # 禁用推理
      - "0"
```

### 高随机性的创造性

```yaml
services:
  app:
    image: app
    models:
      creative_model:
        endpoint_var: CREATIVE_URL
        model_var: CREATIVE_MODEL

models:
  creative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # 温度
      - "1"
      - "--top-p"               # Top-p 采样
      - "0.9"
```

### 高度确定性

```yaml
services:
  app:
    image: app
    models:
      deterministic_model:
        endpoint_var: DET_URL
        model_var: DET_MODEL

models:
  deterministic_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # 温度
      - "0"
      - "--top-k"               # Top-k 采样
      - "1"
```

### 并发处理

```yaml
services:
  app:
    image: app
    models:
      concurrent_model:
        endpoint_var: CONCURRENT_URL
        model_var: CONCURRENT_MODEL

models:
  concurrent_model:
    model: ai/model
    context_size: 2048
    runtime_flags:
      - "--threads"             # 生成期间使用的线程数
      - "8"
      - "--mlock"               # 锁定内存以防止交换
```

### 丰富词汇模型

```yaml
services:
  app:
    image: app
    models:
      rich_vocab_model:
        endpoint_var: RICH_VOCAB_URL
        model_var: RICH_VOCAB_MODEL

```yaml
models:
  rich_vocab_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # 温度
      - "0.1"
      - "--top-p"               # Top-p 采样
      - "0.9"
```

### 嵌入模型

在使用嵌入模型与 `/v1/embeddings` 端点时，必须包含 `--embeddings` 运行时标志，以便模型能够正确配置。

```yaml
services:
  app:
    image: app
    models:
      embedding_model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_MODEL

models:
  embedding_model:
    model: ai/all-minilm
    context_size: 2048
    runtime_flags:
      - "--embeddings"          # 嵌入模型必需
```

## 参考文档

- [`models` 顶级元素](/reference/compose-file/models.md)
- [`models` 属性](/reference/compose-file/services.md#models)
- [Docker Model Runner 文档](/manuals/ai/model-runner/_index.md)
- [配置选项](/manuals/ai/model-runner/configuration.md) - 上下文大小和运行时参数
- [推理引擎](/manuals/ai/model-runner/inference-engines.md) - llama.cpp 和 vLLM 详情
- [API 参考](/manuals/ai/model-runner/api-reference.md) - OpenAI 和 Ollama 兼容 API
