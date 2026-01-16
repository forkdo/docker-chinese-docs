---
title: DMR REST API
url: /ai/model-runner/api-reference/
parent:
  title: Docker Model Runner
  url: /ai/model-runner/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Model Runner
    url: /ai/model-runner/
  - title: DMR REST API
    url: /ai/model-runner/api-reference/
next:
  title: DMR 入门
  url: /ai/model-runner/get-started/
prev:
  title: 配置选项
  url: /ai/model-runner/configuration/
---


启用 Model Runner 后，新的 API 端点将可用。您可以使用这些端点以编程方式与模型进行交互。Docker Model Runner 提供了与 OpenAI 和 Ollama API 格式的兼容性。

## 确定基础 URL

与端点交互的基础 URL 取决于您运行 Docker 的方式以及您使用的 API 格式。

**Docker Desktop**



| 访问来源 | 基础 URL |
|-------------|----------|
| 容器 | `http://model-runner.docker.internal` |
| 主机进程 (TCP) | `http://localhost:12434` |

> [!NOTE]
> 必须启用 TCP 主机访问。请参阅 [启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

**Docker Engine**



| 访问来源 | 基础 URL |
|-------------|----------|
| 容器 | `http://172.17.0.1:12434` |
| 主机进程 | `http://localhost:12434` |

> [!NOTE]
> `172.17.0.1` 接口默认可能对 Compose 项目中的容器不可用。
> 在这种情况下，请在您的 Compose 服务 YAML 中添加 `extra_hosts` 指令：
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后您就可以通过 `http://model-runner.docker.internal:12434/` 访问 Docker Model Runner API。



### 第三方工具的基础 URL

当配置期望 OpenAI 兼容 API 的第三方工具时，请使用这些基础 URL：

| 工具类型 | 基础 URL 格式 |
|-----------|-----------------|
| OpenAI SDK / 客户端 | `http://localhost:12434/engines/v1` |
| Ollama 兼容客户端 | `http://localhost:12434` |

有关具体配置示例，请参阅 [IDE 和工具集成](ide-integrations.md)。

## 支持的 API

Docker Model Runner 支持多种 API 格式：

| API | 描述 | 用例 |
|-----|-------------|----------|
| [OpenAI API](#openai-compatible-api) | OpenAI 兼容的聊天补全、嵌入 | 大多数 AI 框架和工具 |
| [Ollama API](#ollama-compatible-api) | Ollama 兼容端点 | 为 Ollama 构建的工具 |
| [DMR API](#dmr-native-endpoints) | Docker Model Runner 原生端点 | 模型管理 |

## OpenAI 兼容 API

DMR 实现了 OpenAI API 规范，以实现与现有工具和框架的最大兼容性。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/engines/v1/models` | GET | [列出模型](https://platform.openai.com/docs/api-reference/models/list) |
| `/engines/v1/models/{namespace}/{name}` | GET | [获取模型](https://platform.openai.com/docs/api-reference/models/retrieve) |
| `/engines/v1/chat/completions` | POST | [创建聊天补全](https://platform.openai.com/docs/api-reference/chat/create) |
| `/engines/v1/completions` | POST | [创建补全](https://platform.openai.com/docs/api-reference/completions/create) |
| `/engines/v1/embeddings` | POST | [创建嵌入](https://platform.openai.com/docs/api-reference/embeddings/create) |

> [!NOTE]
> 您可以选择性地在路径中包含引擎名称：`/engines/llama.cpp/v1/chat/completions`。
> 这在运行多个推理引擎时很有用。

### 模型名称格式

在 API 请求中指定模型时，请使用包含命名空间的完整模型标识符：

```json
{
  "model": "ai/smollm2",
  "messages": [...]
}
```

常见的模型名称格式：
- Docker Hub 模型：`ai/smollm2`, `ai/llama3.2`, `ai/qwen2.5-coder`
- 带标签的版本：`ai/smollm2:360M-Q4_K_M`
- 自定义模型：`myorg/mymodel`

### 支持的参数

支持以下 OpenAI API 参数：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `model` | string | 必需。模型标识符。 |
| `messages` | array | 聊天补全必需。对话历史。 |
| `prompt` | string | 补全必需。提示文本。 |
| `max_tokens` | integer | 要生成的最大令牌数。 |
| `temperature` | float | 采样温度 (0.0-2.0)。 |
| `top_p` | float | 核心采样参数 (0.0-1.0)。 |
| `stream` | Boolean | 启用流式响应。 |
| `stop` | string/array | 停止序列。 |
| `presence_penalty` | float | 存在惩罚 (-2.0 到 2.0)。 |
| `frequency_penalty` | float | 频率惩罚 (-2.0 到 2.0)。

### 限制和与 OpenAI 的差异

使用 DMR 的 OpenAI 兼容 API 时，请注意以下差异：

| 功能 | DMR 行为 |
|---------|--------------|
| API 密钥 | 不需要。DMR 会忽略 `Authorization` 头。 |
| 函数调用 | 对于兼容模型，使用 llama.cpp 支持。 |
| 视觉 | 支持多模态模型（例如 LLaVA）。 |
| JSON 模式 | 通过 `response_format: {"type": "json_object"}` 支持。 |
| Logprobs | 支持。 |
| 令牌计数 | 使用模型的本机令牌编码器，可能与 OpenAI 的不同。 |

## Ollama 兼容 API

DMR 还为为 Ollama 构建的工具和框架提供了 Ollama 兼容端点。

### 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/tags` | GET | 列出可用模型 |
| `/api/show` | POST | 显示模型信息 |
| `/api/chat` | POST | 生成聊天补全 |
| `/api/generate` | POST | 生成补全 |
| `/api/embeddings` | POST | 生成嵌入 |

### 示例：使用 Ollama API 进行聊天

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

## DMR 原生端点

这些端点特定于 Docker Model Runner，用于模型管理：

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/models/create` | POST | 拉取/创建模型 |
| `/models` | GET | 列出本地模型 |
| `/models/{namespace}/{name}` | GET | 获取模型详情 |
| `/models/{namespace}/{name}` | DELETE | 删除本地模型 |

## REST API 示例

### 从容器内部发起请求

要使用 `curl` 从另一个容器内部调用 `chat/completions` OpenAI 端点：

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

1. 从 Docker Desktop GUI 或通过 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用主机端 TCP 支持。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果您在 Windows 上运行，还需要启用 GPU 支持的推理。
   请参阅 [启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

1. 如上一节所述，使用 `localhost` 和正确的端口与其交互。

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

### 使用 Unix 套接字从主机发起请求

要使用 `curl` 通过 Docker 套接字从主机调用 `chat/completions` OpenAI 端点：

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

## 与 OpenAI SDK 一起使用

### Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed"  # DMR doesn't require an API key
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

## 后续步骤

- [IDE 和工具集成](ide-integrations.md) - 配置 Cline、Continue、Cursor 和其他工具
- [配置选项](configuration.md) - 调整上下文大小和运行时参数
- [推理引擎](inference-engines.md) - 了解 llama.cpp 和 vLLM 选项
