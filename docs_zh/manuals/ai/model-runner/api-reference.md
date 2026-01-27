---
title: DMR REST API
description: Docker Model Runner REST API 端点的参考文档，包括 OpenAI、Anthropic 和 Ollama 兼容性。
weight: 30
keywords: Docker, ai, model runner, rest api, openai, anthropic, ollama, endpoints, documentation, cline, continue, cursor
---

启用 Model Runner 后，新的 API 端点将可用。您可以使用这些端点以编程方式与模型进行交互。Docker Model Runner 提供与 OpenAI、Anthropic 和 Ollama API 格式的兼容性。

## 确定基础 URL

与端点交互的基础 URL 取决于您运行 Docker 的方式以及您使用的 API 格式。

{{< tabs >}}
{{< tab name="Docker Desktop">}}

| 访问来源 | 基础 URL |
|-------------|----------|
| 容器 | `http://model-runner.docker.internal` |
| 主机进程 (TCP) | `http://localhost:12434` |

> [!NOTE]
> 必须启用 TCP 主机访问。请参阅[在 Docker Desktop 中启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

{{< /tab >}}
{{< tab name="Docker Engine">}}

| 访问来源 | 基础 URL |
|-------------|----------|
| 容器 | `http://172.17.0.1:12434` |
| 主机进程 | `http://localhost:12434` |

> [!NOTE]
> 默认情况下，Compose 项目中的容器可能无法访问 `172.17.0.1` 接口。
> 在这种情况下，请在 Compose 服务 YAML 中添加 `extra_hosts` 指令：
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后您就可以通过 `http://model-runner.docker.internal:12434/` 访问 Docker Model Runner API

{{< /tab >}}
{{</tabs >}}

### 第三方工具的基础 URL

配置期望 OpenAI 兼容 API 的第三方工具时，请使用以下基础 URL：

| 工具类型 | 基础 URL 格式 |
|-----------|-----------------|
| OpenAI SDK / 客户端 | `http://localhost:12434/engines/v1` |
| Anthropic SDK / 客户端 | `http://localhost:12434` |
| Ollama 兼容客户端 | `http://localhost:12434` |

有关具体配置示例，请参阅 [IDE 和工具集成](ide-integrations.md)。

## 支持的 API

Docker Model Runner 支持多种 API 格式：

| API | 描述 | 使用场景 |
|-----|-------------|----------|
| [OpenAI API](#openai-compatible-api) | OpenAI 兼容的聊天补全、嵌入 | 大多数 AI 框架和工具 |
| [Anthropic API](#anthropic-compatible-api) | Anthropic 兼容的消息端点 | 为 Claude 构建的工具 |
| [Ollama API](#ollama-compatible-api) | Ollama 兼容的端点 | 为 Ollama 构建的工具 |
| [图像生成 API](#image-generation-api-diffusers) | 基于 Diffusers 的图像生成 | 根据文本提示生成图像 |
| [DMR API](#dmr-native-endpoints) | 原生 Docker Model Runner 端点 | 模型管理 |

## OpenAI 兼容 API

DMR 实现了 OpenAI API 规范，以最大程度地与现有工具和框架兼容。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/engines/v1/models` | GET | [列出模型](https://platform.openai.com/docs/api-reference/models/list) |
| `/engines/v1/models/{namespace}/{name}` | GET | [检索模型](https://platform.openai.com/docs/api-reference/models/retrieve) |
| `/engines/v1/chat/completions` | POST | [创建聊天补全](https://platform.openai.com/docs/api-reference/chat/create) |
| `/engines/v1/completions` | POST | [创建补全](https://platform.openai.com/docs/api-reference/completions/create) |
| `/engines/v1/embeddings` | POST | [创建嵌入](https://platform.openai.com/docs/api-reference/embeddings/create) |

> [!NOTE]
> 您可以选择性地在路径中包含引擎名称：`/engines/llama.cpp/v1/chat/completions`。
> 这在运行多个推理引擎时非常有用。

### 模型名称格式

在 API 请求中指定模型时，请使用包含命名空间的完整模型标识符：

```json
{
  "model": "ai/smollm2",
  "messages": [...]
}
```

常见模型名称格式：
- Docker Hub 模型：`ai/smollm2`、`ai/llama3.2`、`ai/qwen2.5-coder`
- 带标签版本：`ai/smollm2:360M-Q4_K_M`
- 自定义模型：`myorg/mymodel`

### 支持的参数

以下 OpenAI API 参数受支持：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `model` | string | 必需。模型标识符。 |
| `messages` | array | 聊天补全必需。对话历史记录。 |
| `prompt` | string | 补全必需。提示文本。 |
| `max_tokens` | integer | 生成的最大 token 数。 |
| `temperature` | float | 采样温度 (0.0-2.0)。 |
| `top_p` | float | 核心采样参数 (0.0-1.0)。 |
| `stream` | Boolean | 启用流式响应。 |
| `stop` | string/array | 停止序列。 |
| `presence_penalty` | float | 存在惩罚 (-2.0 到 2.0)。 |
| `frequency_penalty` | float | 频率惩罚 (-2.0 到 2.0)。 |

### 与 OpenAI 的局限性和差异

使用 DMR 的 OpenAI 兼容 API 时，请注意以下差异：

| 功能 | DMR 行为 |
|---------|--------------|
| API 密钥 | 不需要。DMR 忽略 `Authorization` 标头。 |
| 函数调用 | 对于兼容模型，通过 llama.cpp 支持。 |
| 视觉 | 对于多模态模型（例如 LLaVA）支持。 |
| JSON 模式 | 通过 `response_format: {"type": "json_object"}` 支持。 |
| Logprobs | 支持。 |
| Token 计数 | 使用模型的原生 token 编码器，可能与 OpenAI 的不同。 |

## Anthropic 兼容 API

DMR 为为 Claude 构建的工具和框架提供 [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages) 兼容性。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/anthropic/v1/messages` | POST | [创建消息](https://platform.claude.com/docs/en/api/messages/create) |
| `/anthropic/v1/messages/count_tokens` | POST | [计算 token](https://docs.anthropic.com/en/api/messages-count-tokens) |

### 支持的参数

以下 Anthropic API 参数受支持：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `model` | string | 必需。模型标识符。 |
| `messages` | array | 必需。对话消息。 |
| `max_tokens` | integer | 生成的最大 token 数。 |
| `temperature` | float | 采样温度 (0.0-1.0)。 |
| `top_p` | float | 核心采样参数。 |
| `top_k` | integer | Top-k 采样参数。 |
| `stream` | Boolean | 启用流式响应。 |
| `stop_sequences` | array | 自定义停止序列。 |
| `system` | string | 系统提示。 |

### 示例：使用 Anthropic API 聊天

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### 示例：流式响应

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {"role": "user", "content": "Count from 1 to 10"}
    ]
  }'
```

## Ollama 兼容 API

DMR 还为为 Ollama 构建的工具和框架提供 Ollama 兼容端点。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/tags` | GET | 列出可用模型 |
| `/api/show` | POST | 显示模型信息 |
| `/api/chat` | POST | 生成聊天补全 |
| `/api/generate` | POST | 生成补全 |
| `/api/embeddings` | POST | 生成嵌入 |

### 示例：使用 Ollama API 聊天

```bash
curl http://localhost:12434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### 示例：列出模型

```bash
curl http://localhost:12434/api/tags
```

## 图像生成 API (Diffusers)

DMR 通过 Diffusers 后端支持图像生成，使您能够使用 Stable Diffusion 等模型根据文本提示生成图像。

> [!注意]
> Diffusers 后端需要配备 CUDA 支持的 NVIDIA GPU，并且仅适用于 Linux 系统（x86_64 和 ARM64）。有关设置说明，请参阅[推理引擎](inference-engines.md#diffusers)。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/engines/diffusers/v1/images/generations` | POST | 根据文本提示生成图像 |

### 支持的参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `model` | string | 必需。模型标识符（例如：`stable-diffusion:Q4`）。 |
| `prompt` | string | 必需。要生成图像的文字描述。 |
| `size` | string | 图像尺寸，格式为 `宽度x高度`（例如：`512x512`）。 |

### 响应格式

API 返回一个 JSON 响应，其中包含以 base64 编码的生成图像：

```json
{
  "data": [
    {
      "b64_json": "<base64-encoded-image-data>"
    }
  ]
}
```

### 示例：生成图像

```bash
curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stable-diffusion:Q4",
    "prompt": "A picture of a nice cat",
    "size": "512x512"
  }' | jq -r '.data[0].b64_json' | base64 -d > image.png
```

此命令：
1. 向 Diffusers 图像生成端点发送 POST 请求
2. 指定模型、提示词和输出图像尺寸
3. 使用 `jq` 从响应中提取 base64 编码的图像
4. 解码 base64 数据并保存为 `image.png`

## DMR 原生端点

这些端点是 Docker Model Runner 特有的，用于模型管理：

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/models/create` | POST | 拉取/创建模型 |
| `/models` | GET | 列出本地模型 |
| `/models/{namespace}/{name}` | GET | 获取模型详情 |
| `/models/{namespace}/{name}` | DELETE | 删除本地模型 |

## REST API 示例

### 从容器内部发起请求

要在另一个容器中使用 `curl` 调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'

```

### 通过 TCP 从主机发起请求

要通过 TCP 从主机调用 `chat/completions` OpenAI 端点：

1. 通过 Docker Desktop GUI 或 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用主机端 TCP 支持。  
   例如：`docker desktop enable model-runner --tcp <端口>`。

   如果你在 Windows 上运行，还需启用 GPU 加速推理。  
   请参阅[启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

1. 使用 `localhost` 和正确的端口，按照上一节文档进行交互。

```bash
#!/bin/sh

curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "messages": [
          {
              "role": "system",
              "content": "You are a helpful assistant."
          },
          {
              "role": "user",
              "content": "Please write 500 words about the fall of Rome."
          }
      ]
  }'
```

### 通过 Unix 套接字从主机发起请求

要通过 Docker 套接字从主机使用 `curl` 调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### 流式响应

要接收流式响应，请设置 `stream: true`：

```bash
curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "stream": true,
      "messages": [
          {"role": "user", "content": "Count from 1 to 10"}
      ]
  }'
```

## 与 OpenAI SDK 配合使用

### Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed"  # DMR 不需要 API 密钥
)

response = client.chat.completions.create(
    model="ai/smollm2",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:12434/engines/v1',
  apiKey: 'not-needed',
});

const response = await client.chat.completions.create({
  model: 'ai/smollm2',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

## 下一步

- [IDE 和工具集成](ide-integrations.md) - 配置 Cline、Continue、Cursor 等工具
- [配置选项](configuration.md) - 调整上下文大小和运行时参数
- [推理引擎](inference-engines.md) - 了解 llama.cpp、vLLM 和 Diffusers 选项