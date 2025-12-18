---
title: 使用 Docker 构建和运行智能 AI 应用
linktitle: 智能 AI 应用
keywords: AI, Docker, Model Runner, MCP Toolkit, Docker Offload, AI agents, application development
summary: |
  学习如何使用 Docker Model Runner、MCP Toolkit 和 Docker Offload 创建 AI 智能体应用。
params:
  tags: [AI]
  time: 30 分钟
---

## 简介

智能体应用正在改变软件的构建方式。这些应用不仅仅是响应，它们能决策、规划和行动。它们由模型驱动，通过智能体编排，并实时集成 API、工具和服务。

所有这些新的智能体应用，无论它们做什么，都共享一个共同的架构。这是一种新型的堆栈，由三个核心组件构建而成：

- 模型：这些是你的 GPT、CodeLlama、Mistral。它们负责推理、写作和规划。它们是智能背后的引擎。

- 智能体：这里是逻辑所在。智能体接收一个目标，将其分解，并找出如何完成。它们编排一切。它们与 UI、工具、模型和网关通信。

- MCP 网关：这是将你的智能体连接到外部世界（包括 API、工具和服务）的桥梁。它通过模型上下文协议（MCP）为智能体调用能力提供标准化方式。

Docker 通过将模型、工具网关和云基础设施统一到一个开发者友好的工作流中，使这个 AI 驱动的堆栈变得更简单、更快、更安全，该工作流使用 Docker Compose。

![智能体堆栈示意图](./images/agentic-ai-diagram.webp)

本指南将带你了解智能体开发的核心组件，并展示 Docker 如何通过以下工具将它们统一起来：

- [Docker Model Runner](../manuals/ai/model-runner/_index.md) 让你能够通过简单的命令和 OpenAI 兼容的 API 在本地运行 LLM。
- [Docker MCP 目录和工具包](../manuals/ai/mcp-catalog-and-toolkit/_index.md) 帮助你发现和安全运行外部工具（如 API 和数据库），使用模型上下文协议（MCP）。
- [Docker MCP 网关](../manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 让你编排和管理 MCP 服务器。
- [Docker Offload](/offload/) 提供一个功能强大、GPU 加速的环境，让你使用熟悉的 Compose 工作流运行 AI 应用。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md) 是将所有内容统一起来的工具，让你使用单个文件定义和运行多容器应用。

在本指南中，你将首先在 Docker Offload 中运行应用，使用你已经熟悉的 Compose 工作流。然后，如果你的机器硬件支持，你将在本地使用相同的工作流运行相同的应用。最后，你将深入研究 Compose 文件、Dockerfile 和应用，了解它们如何协同工作。

## 前置条件

要遵循本指南，你需要：

 - [安装 Docker Desktop 4.43 或更高版本](../get-started/get-docker.md)
 - [启用 Docker Model Runner](/manuals/ai/model-runner.md#enable-dmr-in-docker-desktop)
 - [加入 Docker Offload Beta](/offload/quickstart/)

## 步骤 1：克隆示例应用

你将使用一个现有的示例应用，它展示了如何使用 Docker 的 AI 功能将模型连接到外部工具。

```console
$ git clone https://github.com/docker/compose-for-agents.git
$ cd compose-for-agents/adk/
```

## 步骤 2：使用 Docker Offload 运行应用

你将首先在 Docker Offload 中运行应用，它为运行 AI 工作负载提供了一个托管环境。如果你想要利用云资源，或者你的本地机器不满足在本地运行模型的硬件要求，这非常理想。Docker Offload 包括对 GPU 加速实例的支持，使其成为 AI 模型推理等计算密集型工作负载的理想选择。

要使用 Docker Offload 运行应用，请遵循以下步骤：

1. 登录 Docker Desktop 仪表板。
2. 在终端中，通过运行以下命令启动 Docker Offload：

   ```console
   $ docker offload start
   ```

   当提示时，选择你要用于 Docker Offload 的账户，并在提示 **Do you need GPU support?** 时选择 **Yes**。

3. 在克隆仓库的 `adk/` 目录中，在终端中运行以下命令来构建和运行应用：

   ```console
   $ docker compose up
   ```

   首次运行此命令时，Docker 会从 Docker Hub 拉取模型，这可能需要一些时间。

   应用现在正在 Docker Offload 中运行。注意，使用 Docker Offload 时的 Compose 工作流与本地使用时相同。你在 `compose.yaml` 文件中定义应用，然后使用 `docker compose up` 来构建和运行它。

4. 访问 [http://localhost:8080](http://localhost:8080)。在提示中输入正确或错误的事实，然后按回车。一个智能体会搜索 DuckDuckGo 来验证它，另一个智能体会修改输出。

   ![应用截图](./images/agentic-ai-app.png)

5. 完成后，在终端中按 ctrl-c 停止应用。

6. 运行以下命令停止 Docker Offload：

   ```console
   $ docker offload stop
   ```

## 步骤 3：可选。在本地运行应用

如果你的机器满足必要的硬件要求，你可以使用 Docker Compose 在本地运行整个应用堆栈。这让你能够端到端测试应用，包括模型和 MCP 网关，而无需在云端运行。这个特定示例使用 [Gemma 3 4B 模型](https://hub.docker.com/r/ai/gemma3)，上下文大小为 `10000`。

硬件要求：
 - VRAM：3.5 GB
 - 存储：2.31 GB

如果你的机器超过这些要求，考虑在应用中使用更大的上下文大小或更大的模型来提高智能体性能。你可以轻松地在 `compose.yaml` 文件中更新模型和上下文大小。

要在本地运行应用，请遵循以下步骤：

1. 在克隆仓库的 `adk/` 目录中，在终端中运行以下命令来构建和运行应用：

   ```console
   $ docker compose up
   ```

   首次运行此命令时，Docker 会从 Docker Hub 拉取模型，这可能需要一些时间。

2. 访问 [http://localhost:8080](http://localhost:8080)。在提示中输入正确或错误的事实，然后按回车。一个智能体会搜索 DuckDuckGo 来验证它，另一个智能体会修改输出。

3. 完成后，在终端中按 ctrl-c 停止应用。

## 步骤 4：查看应用环境

你可以在 `adk/` 目录中找到 `compose.yaml` 文件。在文本编辑器中打开它，查看服务是如何定义的。

```yaml {collapse=true,title=compose.yaml}
services:
  adk:
    build:
      context: .
    ports:
      # expose port for web interface
      - "8080:8080"
    environment:
      # point adk at the MCP gateway
      - MCPGATEWAY_ENDPOINT=http://mcp-gateway:8811/sse
    depends_on:
      - mcp-gateway
    models:
      gemma3 :
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  mcp-gateway:
    # mcp-gateway secures your MCP servers
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      # add any MCP servers you want to use
      - --servers=duckduckgo

models:
  gemma3:
    # pre-pull the model when starting Docker Model Runner
    model: ai/gemma3:4B-Q4_0
    context_size: 10000 # 3.5 GB VRAM
    # increase context size to handle search results
    # context_size: 131000 # 7.6 GB VRAM
```

应用由三个主要组件组成：

 - `adk` 服务，这是运行智能 AI 应用的 Web 应用。此服务与 MCP 网关和模型通信。
 - `mcp-gateway` 服务，这是将应用连接到外部工具和服务的 MCP 网关。
 - `models` 块，它定义了与应用一起使用的模型。

当你检查 `compose.yaml` 文件时，你会注意到模型有两个显著元素：

 - `adk` 服务中的服务级 `models` 块
 - 顶级 `models` 块

这两个块一起让 Docker Compose 自动启动并将你的 ADK Web 应用连接到指定的 LLM。

> [!TIP]
>
> 寻找更多模型使用？查看 [Docker AI 模型目录](https://hub.docker.com/catalogs/models/)。

当你检查 `compose.yaml` 文件时，你会注意到网关服务是一个 Docker 维护的镜像，[`docker/mcp-gateway:latest`](https://hub.docker.com/r/docker/agents_gateway)。这个镜像是 Docker 的开源 [MCP 网关](https://github.com/docker/docker-mcp/)，它让你的应用能够连接到 MCP 服务器，这些服务器暴露模型可以调用的工具。在这个示例中，它使用 [`duckduckgo` MCP 服务器](https://hub.docker.com/mcp/server/duckduckgo/overview) 来执行 Web 搜索。

>  [!TIP]
>
> 寻找更多 MCP 服务器使用？查看 [Docker MCP 目录](https://hub.docker.com/catalogs/mcp/)。

通过 Compose 文件中的几行指令，你就能够运行和连接智能 AI 应用的所有必要服务。

除了 Compose 文件，Dockerfile 和它创建的 `entrypoint.sh` 脚本在构建和运行时连接 AI 堆栈中也起着作用。你可以在 `adk/` 目录中找到 `Dockerfile`。在文本编辑器中打开它。

```dockerfile {collapse=true,title=Dockerfile}
# Use Python 3.11 slim image as base
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app
# Install system dependencies
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    uv pip install --system .
# Copy application code
COPY agents/ ./agents/
RUN python -m compileall -q .

COPY <<EOF /entrypoint.sh
#!/bin/sh
set -e

if test -f /run/secrets/openai-api-key; then
    export OPENAI_API_KEY=$(cat /run/secrets/openai-api-key)
fi

if test -n "\${OPENAI_API_KEY}"; then
    echo "Using OpenAI with \${OPENAI_MODEL_NAME}"
else
    echo "Using Docker Model Runner with \${MODEL_RUNNER_MODEL}"
    export OPENAI_BASE_URL=\${MODEL_RUNNER_URL}
    export OPENAI_MODEL_NAME=openai/\${MODEL_RUNNER_MODEL}
    export OPENAI_API_KEY=cannot_be_empty
fi
exec adk web --host 0.0.0.0 --port 8080 --log_level DEBUG
EOF
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENTRYPOINT [ "/entrypoint.sh" ]
```

`entrypoint.sh` 有五个关键的环境变量：

- `MODEL_RUNNER_URL`：由 Compose（通过服务级 `models:` 块）注入，指向你的 Docker Model Runner HTTP 端点。

- `MODEL_RUNNER_MODEL`：由 Compose 注入，选择要在 Model Runner 中启动的模型。

- `OPENAI_API_KEY`：如果你在 Compose 文件中定义 `openai-api-key` 密钥，Compose 会将其挂载在 `/run/secrets/openai-api-key`。入口点脚本读取该文件并将其导出为 `OPENAI_API_KEY`，导致应用使用托管的 OpenAI 而不是 Model Runner。

- `OPENAI_BASE_URL`：当没有真实密钥时，这被设置为 `MODEL_RUNNER_URL`，因此 ADK 的 OpenAI 兼容客户端将请求发送到 Docker Model Runner。

- `OPENAI_MODEL_NAME`：当回退到 Model Runner 时，模型被前缀为 `openai/`，因此客户端选择正确的模型别名。

这些变量一起让相同的 ADK Web 服务器代码无缝地针对以下任一目标：

- 托管的 OpenAI：如果你提供 `OPENAI_API_KEY`（以及可选的 `OPENAI_MODEL_NAME`）
- Model Runner：通过重新映射 `MODEL_RUNNER_URL` 和 `MODEL_RUNNER_MODEL` 到 OpenAI 客户端期望的变量

## 步骤 5：查看应用

`adk` Web 应用是一个智能体实现，它通过环境变量和 API 调用连接到 MCP 网关和模型。它使用 [ADK（Agent Development Kit）](https://github.com/google/adk-python) 定义一个名为 Auditor 的根智能体，该智能体协调两个子智能体，Critic 和 Reviser，来验证和优化模型生成的答案。

这三个智能体是：

- Critic：使用工具集（如 DuckDuckGo）验证事实主张。
- Reviser：根据 Critic 提供的验证裁决编辑答案。
- Auditor：一个高级智能体，它对 Critic 和 Reviser 进行排序。它作为应用的入口点，评估 LLM 生成的内容，验证它们，并优化最终输出。

应用的所有行为都在 Python 中的 `agents/` 目录下定义。以下是显著文件的分解：

- `agents/agent.py`：定义 Auditor，一个 SequentialAgent，它将 Critic 和 Reviser 智能体链接在一起。这个智能体是应用的主要入口点，负责使用真实世界的验证工具审核 LLM 生成的内容。

- `agents/sub_agents/critic/agent.py`：定义 Critic 智能体。它加载语言模型（通过 Docker Model Runner），设置智能体的名称和行为，并连接到 MCP 工具（如 DuckDuckGo）。

- `agents/sub_agents/critic/prompt.py`：包含 Critic 提示，指示智能体使用外部工具提取和验证主张。

- `agents/sub_agents/critic/tools.py`：定义 MCP 工具集配置，包括解析 `mcp/` 字符串、创建工具连接和处理 MCP 网关通信。

- `agents/sub_agents/reviser/agent.py`：定义 Reviser 智能体，它接收 Critic 的发现并最小化重写原始答案。它还包括回调以清理 LLM 输出并确保它处于正确的格式。

- `agents/sub_agents/reviser/prompt.py`：包含 Reviser 提示，指示智能体根据验证的主张裁决修改答案文本。

MCP 网关通过 `MCPGATEWAY_ENDPOINT` 环境变量配置。在这种情况下，`http://mcp-gateway:8811/sse`。这允许应用使用 Server-Sent Events (SSE) 与 MCP 网关容器通信，该容器本身代理对 DuckDuckGo 等外部工具服务的访问。

## 总结

基于智能体的 AI 应用正在成为一种强大的新软件架构。在本指南中，你探索了一个模块化、链式思维系统，其中 Auditor 智能体协调 Critic 和 Reviser 的工作，以事实核查和优化模型生成的答案。这种架构展示了如何以结构化、模块化的方式将本地模型推理与外部工具集成结合起来。

你还可以看到 Docker 如何通过提供一套支持本地和云基础智能 AI 开发的工具来简化这个过程：

- [Docker Model Runner](../manuals/ai/model-runner/_index.md)：通过 OpenAI 兼容的 API 在本地运行和服务开源模型。
- [Docker MCP 目录和工具包](../manuals/ai/mcp-catalog-and-toolkit/_index.md)：启动和管理遵循模型上下文协议（MCP）标准的工具集成。
- [Docker MCP 网关](../manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)：编排和管理 MCP 服务器，将智能体连接到外部工具和服务。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md)：使用单个文件定义和运行多容器智能 AI 应用，使用本地和云端相同的 Docker Compose 工作流。
- [Docker Offload](/offload/)：在安全、托管的云环境中使用与你在本地使用的相同 Docker Compose 工作流运行 GPU 密集型 AI 工作负载。

使用这些工具，你可以高效地开发和测试智能 AI 应用，无论是在本地还是在云端，使用一致的工作流。