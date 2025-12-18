---
title: DMR REST API
description: Docker Model Runner REST API 端点和使用示例的参考文档。
weight: 30
keywords: Docker, ai, model runner, rest api, openai, endpoints, documentation
---

启用 Model Runner 后，将有新的 API 端点可用。你可以使用这些端点以编程方式与模型交互。

### 确定基础 URL

与端点交互的基础 URL 取决于你运行 Docker 的方式：

{{< tabs >}}
{{< tab name="Docker Desktop">}}

- 从容器内：`http://model-runner.docker.internal/`
- 从主机进程：`http://localhost:12434/`（假设在默认端口 12434 上启用了 TCP 主机访问）

{{< /tab >}}
{{< tab name="Docker Engine">}}

- 从容器内：`http://172.17.0.1:12434/`（其中 `172.17.0.1` 表示主机网关地址）
- 从主机进程：`http://localhost:12434/`

> [!NOTE]
> `172.17.0.1` 接口默认可能对 Compose 项目中的容器不可用。
> 在这种情况下，在你的 Compose 服务 YAML 中添加 `extra_hosts` 指令：
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
> 然后你可以通过 http://model-runner.docker.internal:12434/ 访问 Docker Model Runner API

{{< /tab >}}
{{</tabs >}}

### 可用的 DMR 端点

- 创建模型：

  ```text
  POST /models/create
  ```

- 列出模型：

  ```text
  GET /models
  ```

- 获取模型：

  ```text
  GET /models/{namespace}/{name}
  ```

- 删除本地模型：

  ```text
  DELETE /models/{namespace}/{name}
  ```

### 可用的 OpenAI 端点

DMR 支持以下 OpenAI 端点：

- [列出模型](https://platform.openai.com/docs/api-reference/models/list)：

  ```text
  GET /engines/llama.cpp/v1/models
  ```

- [检索模型](https://platform.openai.com/docs/api-reference/models/retrieve)：

  ```text
  GET /engines/llama.cpp/v1/models/{namespace}/{name}
  ```

- [列出聊天补全](https://platform.openai.com/docs/api-reference/chat/list)：

  ```text
  POST /engines/llama.cpp/v1/chat/completions
  ```

- [创建补全](https://platform.openai.com/docs/api-reference/completions/create)：

  ```text
  POST /engines/llama.cpp/v1/completions
  ```


- [创建嵌入](https://platform.openai.com/docs/api-reference/embeddings/create)：

  ```text
  POST /engines/llama.cpp/v1/embeddings
  ```

要通过 Unix 套接字 (`/var/run/docker.sock`) 调用这些端点，需在其路径前加上 `/exp/vDD4.40`。

> [!NOTE]
> 你可以省略路径中的 `llama.cpp`。例如：`POST /engines/v1/chat/completions`。

## REST API 示例

### 从容器内请求

要从另一个容器内使用 `curl` 调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions \
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

### 使用 TCP 从主机请求

要通过 TCP 从主机调用 `chat/completions` OpenAI 端点：

1. 从 Docker Desktop GUI 或通过 [Docker Desktop CLI](/manuals/desktop/features/desktop-cli.md) 启用主机侧的 TCP 支持。
   例如：`docker desktop enable model-runner --tcp <port>`。

   如果你在 Windows 上运行，还需启用 GPU 支持的推理。
   参见 [启用 Docker Model Runner](get-started.md#enable-docker-model-runner-in-docker-desktop)。

1. 按照上一节的文档使用 `localhost` 和正确的端口与之交互。

```bash
#!/bin/sh

  curl http://localhost:12434/engines/llama.cpp/v1/chat/completions \
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

### 使用 Unix 套接字从主机请求

要通过 Docker 套接字使用 `curl` 从主机调用 `chat/completions` OpenAI 端点：

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/llama.cpp/v1/chat/completions \
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