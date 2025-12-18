---
title: 模型
description: 了解模型顶级元素
keywords: compose, compose 规范, 模型, compose 文件参考
weight: 120
---

{{< summary-bar feature_name="Compose 模型" >}}

顶级 `models` 部分声明了你的 Compose 应用程序所使用的 AI 模型。这些模型通常作为 OCI 工件被拉取，由模型运行器执行，并以 API 形式暴露，供你的服务容器消费。

服务只有在 `services` 顶级元素中的 `models` 属性明确授权时，才能访问模型。

## 示例

### 示例 1

```yaml
services:
  app:
    image: app
    models:
      - ai_model


models:
  ai_model:
    model: ai/model
```

在此基本示例中：

 - app 服务使用 `ai_model`。
 - `ai_model` 被定义为 OCI 工件（`ai/model`），由模型运行器拉取并提供服务。
 - Docker Compose 将连接信息（例如 `AI_MODEL_URL`）注入到容器中。

### 示例 2

```yaml
services:
  app:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL

models:
  my_model:
    model: ai/model
    context_size: 1024
    runtime_flags: 
      - "--a-flag"
      - "--another-flag=42"
```

在此高级设置中：

 - 服务 app 使用长语法引用 `my_model`。
 - Compose 将模型运行器的 URL 作为环境变量 `MODEL_URL` 注入。

## 属性

- `model`（必需）：模型的 OCI 工件标识符。Compose 通过模型运行器拉取并运行此标识符。
- `context_size`：定义模型的最大 token 上下文大小。
- `runtime_flags`：当模型启动时，传递给推理引擎的原始命令行标志列表。

## 额外资源

有关使用 `model` 的更多示例和信息，请参阅 [在 Compose 中使用 AI 模型](/manuals/ai/compose/models-and-compose.md)