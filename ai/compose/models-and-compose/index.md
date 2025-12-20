# 在 Docker Compose 应用程序中定义 AI 模型





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="https://docs.docker.com/compose/releases/release-notes/#2380">2.38.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Compose 允许您将 AI 模型定义为应用程序的核心组件，这样您就可以在声明服务依赖关系的同时声明模型依赖关系，并在任何支持 Compose 规范的平台上运行应用程序。

## 先决条件

- Docker Compose v2.38 或更高版本
- 支持 Compose 模型的平台，例如 Docker Model Runner (DMR) 或兼容的云提供商。
  如果您使用的是 DMR，请参阅[要求](/manuals/ai/model-runner/_index.md#requirements)。

## 什么是 Compose 模型？

Compose `models` 是在应用程序中定义 AI 模型依赖关系的标准化方式。通过在 Compose 文件中使用 [`models` 顶层元素](/reference/compose-file/models.md)，您可以：

- 声明您的应用程序需要哪些 AI 模型
- 指定模型配置和要求
- 使您的应用程序可在不同平台之间移植
- 让平台处理模型配置和生命周期管理

## 基本模型定义

要在 Compose 应用程序中定义模型，请使用 `models` 顶层元素：

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
- 一个名为 `llm` 的模型定义，引用 `ai/smollm2` 模型镜像

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
- `model`（必需）：模型的 OCI 工件标识符。这是 Compose 通过模型运行器拉取和运行的内容。
- `context_size`：定义模型的最大令牌上下文大小。

   > [!NOTE]
   > 每个模型都有自己的最大上下文大小。增加上下文长度时，
   > 请考虑您的硬件限制。通常，尽量根据您的特定需求
   > 保持上下文大小尽可能小。

- `runtime_flags`：在模型启动时传递给推理引擎的原始命令行标志列表。
   例如，如果您使用 llama.cpp，可以传递任何[可用参数](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)。
- 平台特定选项也可以通过扩展属性 `x-*` 获得。

> [!TIP]
> 在[常见运行时配置](#common-runtime-configurations)部分查看更多示例。

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

使用短语法，平台会根据模型名称自动生成环境变量：
- `LLM_URL` - 访问 LLM 模型的 URL
- `LLM_MODEL` - LLM 模型的模型标识符
- `EMBEDDING_MODEL_URL` - 访问嵌入模型的 URL
- `EMBEDDING_MODEL_MODEL` - 嵌入模型的模型标识符

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

使用此配置，您的服务将接收：
- `AI_MODEL_URL` 和 `AI_MODEL_NAME` 用于 LLM 模型
- `EMBEDDING_URL` 和 `EMBEDDING_NAME` 用于嵌入模型

## 平台可移植性

使用 Compose 模型的一个主要好处是可以在支持 Compose 规范的不同平台之间移植。

### Docker Model Runner

当[启用了 Docker Model Runner](/manuals/ai/model-runner/_index.md) 时：

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
- 提供访问模型的端点 URL
- 将环境变量注入到服务中

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

云提供商可能会：
- 使用托管的 AI 服务而不是在本地运行模型
- 应用云特定的优化和扩展
- 提供额外的监控和日志记录功能
- 自动处理模型版本控制和更新

## 常见运行时配置

以下是一些针对不同用例的配置示例。

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
      - "--verbose-prompt"                # 在生成前打印详细的提示
      - "--log-prefix"                    # 在日志消息中启用前缀
      - "--log-timestamps"                # 在日志消息中启用时间戳
      - "--log-colors"                    # 启用彩色日志记录
```

### 保守模式（禁用推理）

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

### 创造性模式（高随机性）

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

### 高确定性

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

## 使用提供程序服务的替代配置

> [!IMPORTANT]
>
> 此方法已弃用。请改用 [`models` 顶层元素](#basic-model-definition)。

您也可以使用 `provider` 服务类型，它允许您声明应用程序所需的平台功能。
对于 AI 模型，您可以使用 `model` 类型来声明模型依赖关系。

要定义模型提供程序：

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

- [`models` 顶层元素](/reference/compose-file/models.md)
- [`models` 属性](/reference/compose-file/services.md#models)
- [Docker Model Runner 文档](/manuals/ai/model-runner.md)
- [Compose Model Runner 文档](/manuals/ai/compose/models-and-compose.md)
