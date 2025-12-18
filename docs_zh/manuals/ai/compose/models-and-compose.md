---
title: 在 Docker Compose 应用中定义 AI 模型
linkTitle: 在 Compose 中使用模型
description: 了解如何使用 models 顶级元素在 Docker Compose 应用中定义和使用 AI 模型
keywords: compose, docker compose, models, ai, 机器学习, 云提供商, 规范
aliases:
  - /compose/how-tos/model-runner/
  - /ai/compose/model-runner/
weight: 10
params:
  sidebar:
    badge:
      color: green
      text: 新功能
---

{{< summary-bar feature_name="Compose 模型" >}}

Compose 允许您将 AI 模型定义为应用的核心组件，这样您就可以在服务旁边声明模型依赖，并在任何支持 Compose 规范的平台上运行应用。

## 前置条件

- Docker Compose v2.38 或更高版本
- 支持 Compose 模型的平台，例如 Docker Model Runner (DMR) 或兼容的云提供商。
  如果使用 DMR，请参阅 [需求](/manuals/ai/model-runner/_index.md#requirements)。

## 什么是 Compose 模型？

Compose `models` 是在应用中定义 AI 模型依赖的标准方式。通过在 Compose 文件中使用 [`models` 顶级元素](/reference/compose-file/models.md)，您可以：

- 声明应用所需的 AI 模型
- 指定模型配置和需求
- 使应用在不同平台间具有可移植性
- 让平台处理模型供应和生命周期管理

## 基本模型定义

要在 Compose 应用中定义模型，请使用 `models` 顶级元素：

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
- 一个名为 `chat-app` 的服务，使用名为 `llm` 的模型
- 一个 `llm` 模型定义，引用 `ai/smollm2` 模型镜像

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
- `model`（必需）：模型的 OCI 构件标识符。Compose 通过模型运行器拉取并运行此标识符。
- `context_size`：定义模型的最大 token 上下文大小。

   > [!NOTE]
   > 每个模型都有自己的最大上下文大小。增加上下文长度时，
   > 请考虑您的硬件限制。通常，尽量保持上下文大小
   > 符合您的特定需求。

- `runtime_flags`：模型启动时传递给推理引擎的原始命令行标志列表。
   例如，如果您使用 llama.cpp，可以传递 [可用参数](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) 中的任意一个。
- 平台特定选项可能也通过扩展属性 `x-*` 提供

> [!TIP]
> 更多示例请参阅 [常见运行时配置](#常见运行时配置) 部分。

## 服务模型绑定

服务可以通过两种方式引用模型：简写语法和完整语法。

### 简写语法

简写语法是将模型绑定到服务的最简单方式：

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

使用简写语法时，平台会根据模型名称自动生成环境变量：
- `LLM_URL` - 访问 LLM 模型的 URL
- `LLM_MODEL` - LLM 模型的标识符
- `EMBEDDING_MODEL_URL` - 访问 embedding-model 的 URL
- `EMBEDDING_MODEL_MODEL` - embedding-model 的标识符

### 完整语法

完整语法允许您自定义环境变量名称：

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

使用此配置，您的服务将接收：
- `AI_MODEL_URL` 和 `AI_MODEL_NAME` 用于 LLM 模型
- `EMBEDDING_URL` 和 `EMBEDDING_NAME` 用于 embedding 模型

## 平台可移植性

使用 Compose 模型的一个关键优势是可以在支持 Compose 规范的不同平台间移植。

### Docker Model Runner

当 [Docker Model Runner 启用时](/manuals/ai/model-runner/_index.md)：

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
- 拉取并在本地运行指定的模型
- 提供访问模型的端点 URL
- 将环境变量注入服务

### 云提供商

相同的 Compose 文件可以在支持 Compose 模型的云提供商上运行：

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
    # 云特定配置
    x-cloud-options:
      - "cloud.instance-type=gpu-small"
      - "cloud.region=us-west-2"
```

云提供商可能：
- 使用托管 AI 服务而非本地运行模型
- 应用云特定的优化和扩展
- 提供额外的监控和日志功能
- 自动处理模型版本控制和更新

## 常见运行时配置

以下是一些针对不同用例的示例配置。

### 开发环境

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
      - "--verbose"                       # 设置详细级别为无限
      - "--verbose-prompt"                # 在生成前打印详细提示
      - "--log-prefix"                    # 在日志消息中启用前缀
      - "--log-timestamps"                # 在日志消息中启用时间戳
      - "--log-colors"                    # 启用彩色日志
```

### 保守模式，禁用推理

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

### 创造性模式，高随机性

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

## 使用提供商服务的替代配置

> [!IMPORTANT]
>
> 此方法已弃用。请改用 [`models` 顶级元素](#基本模型定义)。

您也可以使用 `provider` 服务类型，它允许您声明应用所需的平台能力。
对于 AI 模型，您可以使用 `model` 类型来声明模型依赖。

定义模型提供商：

```yaml
services:
  chat:
    image: my-chat-app
    depends_on:
      - ai_runner

  ai_runner:
    provider:
      type: model
      options:
        model: ai/smollm2
        context-size: 1024
        runtime-flags: "--no-prefill-assistant"
```

## 参考

- [`models` 顶级元素](/reference/compose-file/models.md)
- [`models` 属性](/reference/compose-file/services.md#models)
- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose Model Runner 文档](/manuals/ai/compose/models-and-compose.md)