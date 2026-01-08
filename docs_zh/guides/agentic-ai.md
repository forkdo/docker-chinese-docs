---
title: 使用 Docker 构建和运行智能体 AI 应用程序
linktitle: 智能体 AI 应用程序
keywords: AI, Docker, Model Runner, MCP Toolkit, Docker Offload, AI agents, application development
summary: '了解如何使用 Docker Model Runner、MCP Toolkit 和 Docker Offload 创建 AI 智能体应用程序。

  '
params:
  tags:
  - AI
  time: 30 minutes
---

## 简介

智能体应用程序正在改变软件的构建方式。这些应用不仅仅是响应，它们还能决策、规划和行动。它们由模型驱动，由智能体编排，并与 API、工具和服务实时集成。

所有这些新型智能体应用程序，无论其功能如何，都共享一个共同的架构。这是一个由三个核心组件构建而成的新型技术栈：

- **模型 (Models)**：这些是您的 GPT、CodeLlama、Mistral 等模型。它们负责推理、编写和规划。它们是智能背后的引擎。
- **智能体 (Agent)**：这是逻辑所在之处。智能体接收目标，将其分解，并找出如何完成它。它们编排一切。它们与 UI、工具、模型和网关进行通信。
- **MCP 网关 (MCP gateway)**：这是将您的智能体与外部世界（包括 API、工具和服务）连接起来的桥梁。它提供了一种标准方式，让智能体通过模型上下文协议 (MCP) 调用能力。

Docker 通过将模型、工具网关和云基础设施统一到使用 Docker Compose 的开发者友好型工作流中，使这个 AI 驱动的技术栈更简单、更快速、更安全。

![智能体技术栈图示](./images/agentic-ai-diagram.webp)

本指南将引导您了解智能体开发的核心组件，并展示 Docker 如何通过以下工具将它们全部连接在一起：

- [Docker Model Runner](../manuals/ai/model-runner/_index.md) 让您可以通过简单的命令和兼容 OpenAI 的 API 在本地运行 LLM。
- [Docker MCP Catalog and Toolkit](../manuals/ai/mcp-catalog-and-toolkit/_index.md) 帮助您发现并安全地运行外部工具，如 API 和数据库，使用模型上下文协议 (MCP)。
- [Docker MCP Gateway](../manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 让您编排和管理 MCP 服务器。
- [Docker Offload](/offload/) 提供了一个强大的、GPU 加速的环境来运行您的 AI 应用程序，使用与您本地相同的基于 Compose 的工作流。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md) 是将所有内容连接在一起的工具，让您可以用一个文件定义和运行多容器应用程序。

在本指南中，您将首先在 Docker Offload 中运行应用程序，使用您已经熟悉的相同 Compose 工作流。然后，如果您的机器硬件支持，您将使用相同的工作流在本地运行相同的应用程序。最后，您将深入研究 Compose 文件、Dockerfile 和应用程序，了解它们是如何协同工作的。

## 先决条件

要遵循本指南，您需要：

- [安装 Docker Desktop 4.43 或更高版本](../get-started/get-docker.md)
- [启用 Docker Model Runner](/manuals/ai/model-runner.md#enable-dmr-in-docker-desktop)
- [加入 Docker Offload Beta](/offload/quickstart/)

## 步骤 1：克隆示例应用程序

您将使用一个现有的示例应用程序，该程序演示了如何使用 Docker 的 AI 功能将模型连接到外部工具。

```console
$ git clone https://github.com/docker/compose-for-agents.git
$ cd compose-for-agents/adk/
```

## 步骤 2：使用 Docker Offload 运行应用程序

您将首先在 Docker Offload 中运行应用程序，它提供了一个用于运行 AI 工作负载的托管环境。如果您想利用云资源，或者您的本地机器不满足在本地运行模型的硬件要求，这是理想的选择。Docker Offload 包含对 GPU 加速实例的支持，非常适合像 AI 模型推理这样的计算密集型工作负载。

要使用 Docker Offload 运行应用程序，请按照以下步骤操作：

1. 登录 Docker Desktop 仪表板。
2. 在终端中，运行以下命令启动 Docker Offload：

   ```console
   $ docker offload start
   ```

   出现提示时，选择您想用于 Docker Offload 的账户，并在提示 **您需要 GPU 支持吗？** 时选择 **是**。

3. 在克隆的仓库的 `adk/` 目录中，在终端中运行以下命令来构建并运行应用程序：

   ```console
   $ docker compose up
   ```

   第一次运行此命令时，Docker 会从 Docker Hub 拉取模型，这可能需要一些时间。

   应用程序现在正在使用 Docker Offload 运行。请注意，使用 Docker Offload 时的 Compose 工作流与本地相同。您在 `compose.yaml` 文件中定义您的应用程序，然后使用 `docker compose up` 来构建和运行它。

4. 访问 [http://localhost:8080](http://localhost:8080)。在提示符中输入一个正确或不正确的事实，然后按回车键。一个智能体会搜索 DuckDuckGo 来验证它，另一个智能体会修改输出。

   ![应用程序截图](./images/agentic-ai-app.png)

5. 完成后，在终端中按 `ctrl-c` 停止应用程序。
6. 运行以下命令停止 Docker Offload：

   ```console
   $ docker offload stop
   ```

## 步骤 3：可选。在本地运行应用程序

如果您的机器满足必要的硬件要求，您可以使用 Docker Compose 在本地运行整个应用程序堆栈。这使您可以端到端地测试应用程序，包括模型和 MCP 网关，而无需在云中运行。这个特定的示例使用 [Gemma 3 4B 模型](https://hub.docker.com/r/ai/gemma3)，上下文大小为 `10000`。

硬件要求：
- VRAM：3.5 GB
- 存储空间：2.31 GB

如果您的机器超过这些要求，可以考虑使用更大的上下文大小或更大的模型来运行应用程序，以提高智能体的性能。您可以轻松地在 `compose.yaml` 文件中更新模型和上下文大小。

要在本地运行应用程序，请按照以下步骤操作：

1. 在克隆的仓库的 `adk/` 目录中，在终端中运行以下命令来构建并运行应用程序：

   ```console
   $ docker compose up
   ```

   第一次运行此命令时，Docker 会从 Docker Hub 拉取模型，这可能需要一些时间。

2. 访问 [http://localhost:8080](http://localhost:8080)。在提示符中输入一个正确或不正确的事实，然后按回车键。一个智能体会搜索 DuckDuckGo 来验证它，另一个智能体会修改输出。
3. 完成后，在终端中按 `ctrl-c` 停止应用程序。

## 步骤 4：审查应用程序环境

您可以在 `adk/` 目录中找到 `compose.yaml` 文件。在文本编辑器中打开它以查看服务是如何定义的。

```yaml {collapse=true,title=compose.yaml}
services:
  adk:
    build:
      context: .
    ports:
      # 暴露 web 界面的端口
      - "8080:8080"
    environment:
      # 将 adk 指向 MCP 网关
      - MCPGATEWAY_ENDPOINT=http://mcp-gateway:8811/sse
    depends_on:
      - mcp-gateway
    models:
      gemma3 :
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  mcp-gateway:
    # mcp-gateway 保护您的 MCP 服务器
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      # 添加您想使用的任何 MCP 服务器
      - --servers=duckduckgo

models:
  gemma3:
    # 启动 Docker Model Runner 时预拉取模型
    model: ai/gemma3:4B-Q4_0
    context_size: 10000 # 3.5 GB VRAM
    # 增加上下文大小以处理搜索结果
    # context_size: 131000 # 7.6 GB VRAM
```

该应用程序包含三个主要组件：

- `adk` 服务，这是运行智能体 AI 应用程序的 Web 应用程序。此服务与 MCP 网关和模型通信。
- `mcp-gateway` 服务，这是将应用程序连接到外部工具和服务的 MCP 网关。
- `models` 块，定义了应用程序要使用的模型。

当您检查 `compose.yaml` 文件时，您会注意到模型有两个显著的元素：

- `adk` 服务中的服务级 `models` 块
- 顶级的 `models` 块

这两个块 together 让 Docker Compose 自动启动您的 ADK Web 应用并将其连接到指定的 LLM。

> [!TIP]
>
> 在寻找更多模型吗？查看 [Docker AI 模型目录](https://hub.docker.com/catalogs/models/)。

当检查 `compose.yaml` 文件时，您会注意到网关服务是一个 Docker 维护的镜像，[`docker/mcp-gateway:latest`](https://hub.docker.com/r/docker/agents_gateway)。此镜像是 Docker 的开源 [MCP Gateway](https://github.com/docker/docker-mcp/)，它使您的应用程序能够连接到 MCP 服务器，这些服务器暴露了模型可以调用的工具。在此示例中，它使用 [`duckduckgo` MCP 服务器](https://hub.docker.com/mcp/server/duckduckgo/overview) 来执行网络搜索。

> [!TIP]
>
> 在寻找更多 MCP 服务器吗？查看 [Docker MCP 目录](https://hub.docker.com/catalogs/mcp/)。

只需在 Compose 文件中几行指令，您就能够运行并连接智能体 AI 应用程序的所有必要服务。

除了 Compose 文件之外，Dockerfile 和它创建的 `entrypoint.sh` 脚本在构建和运行时连接 AI 技术栈方面也扮演着重要角色。您可以在 `adk/` 目录中找到 `Dockerfile`。在文本编辑器中打开它。

```dockerfile {collapse=true,title=Dockerfile}
# 使用 Python 3.11 slim 镜像作为基础
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app
# 安装系统依赖
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    uv pip install --system .
# 复制应用程序代码
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

# 创建非 root 用户
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

ENTRYPOINT [ "/entrypoint.sh" ]
```

`entrypoint.sh` 有五个关键的环境变量：

- `MODEL_RUNNER_URL`：由 Compose 注入（通过服务级 `models:` 块），指向您的 Docker Model Runner HTTP 端点。
- `MODEL_RUNNER_MODEL`：由 Compose 注入，用于选择在 Model Runner 中启动哪个模型。
- `OPENAI_API_KEY`：如果您在 Compose 文件中定义了 `openai-api-key` 密钥，Compose 会将其挂载到 `/run/secrets/openai-api-key`。入口点脚本读取该文件并将其导出为 `OPENAI_API_KEY`，导致应用程序使用托管的 OpenAI 而不是 Model Runner。
- `OPENAI_BASE_URL`：当没有真实密钥存在时，此变量被设置为 `MODEL_RUNNER_URL`，以便 ADK 的兼容 OpenAI 的客户端将请求发送到 Docker Model Runner。
- `OPENAI_MODEL_NAME`：当回退到 Model Runner 时，模型会加上 `openai/` 前缀，以便客户端选择正确的模型别名。

这些变量 together 让相同的 ADK Web 服务器代码能够无缝地针对以下两种情况进行目标定位：

- **托管的 OpenAI**：如果您提供了 `OPENAI_API_KEY`（以及可选的 `OPENAI_MODEL_NAME`）
- **Model Runner**：通过将 `MODEL_RUNNER_URL` 和 `MODEL_RUNNER_MODEL` 重新映射到 OpenAI 客户端期望的变量中

## 步骤 5：审查应用程序

`adk` Web 应用程序是一个智能体实现，它通过环境变量和 API 调用连接到 MCP 网关和模型。它使用 [ADK (Agent Development Kit)](https://github.com/google/adk-python) 来定义一个名为 Auditor 的根智能体，该智能体协调两个子智能体 Critic 和 Reviser 来验证和优化模型生成的答案。

这三个智能体是：

- **Critic**：使用工具集（如 DuckDuckGo）验证事实性声明。
- **Reviser**：根据 Critic 提供的验证结果编辑答案。
- **Auditor**：一个更高级别的智能体，它对 Critic 和 Reviser 进行排序。它作为入口点，评估 LLM 生成的答案，验证它们，并优化最终输出。

应用程序的所有行为都在 `agents/` 目录下的 Python 中定义。以下是重要文件的细分：

- `agents/agent.py`：定义了 Auditor，一个 SequentialAgent，它将 Critic 和 Reviser 智能体链接在一起。该智能体是应用程序的主入口点，负责使用真实世界的验证工具审核 LLM 生成的内容。
- `agents/sub_agents/critic/agent.py`：定义了 Critic 智能体。它加载语言模型（通过 Docker Model Runner），设置智能体的名称和行为，并连接到 MCP 工具（如 DuckDuckGo）。
- `agents/sub_agents/critic/prompt.py`：包含 Critic 提示，该提示指示智能体使用外部工具提取和验证声明。
- `agents/sub_agents/critic/tools.py`：定义了 MCP 工具集配置，包括解析 `mcp/` 字符串、创建工具连接以及处理 MCP 网关通信。
- `agents/sub_agents/reviser/agent.py`：定义了 Reviser 智能体，它接收 Critic 的发现并最小程度地重写原始答案。它还包括回调以清理 LLM 输出并确保其格式正确。
- `agents/sub_agents/reviser/prompt.py`：包含 Reviser 提示，该提示指示智能体根据已验证的声明结果修改答案文本。

MCP 网关通过 `MCPGATEWAY_ENDPOINT` 环境变量进行配置。在本例中，是 `http://mcp-gateway:8811/sse`。这允许应用程序使用服务器发送事件 (SSE) 与 MCP 网关容器通信，该容器本身充当中介，访问像 DuckDuckGo 这样的外部工具服务。

## 总结

基于智能体的 AI 应用程序正在成为一种强大的新型软件架构。在本指南中，您探索了一个模块化的、思维链系统，其中 Auditor 智能体协调 Critic 和 Reviser 的工作，以事实核查和优化模型生成的答案。这种架构展示了如何以结构化、模块化的方式将本地模型推理与外部工具集成相结合。

您还了解了 Docker 如何通过提供一套支持本地和基于云的智能体 AI 开发的工具来简化这一过程：

- [Docker Model Runner](../manuals/ai/model-runner/_index.md)：通过兼容 OpenAI 的 API 在本地运行和服务开源模型。
- [Docker MCP Catalog and Toolkit](../manuals/ai/mcp-catalog-and-toolkit/_index.md)：启动和管理遵循模型上下文协议 (MCP) 标准的工具集成。
- [Docker MCP Gateway](../manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)：编排和管理 MCP 服务器，以将智能体连接到外部工具和服务。
- [Docker Compose](/manuals/ai/compose/models-and-compose.md)：使用单个文件定义和运行多容器智能体 AI 应用程序，在本地和云中使用相同的工作流。
- [Docker Offload](/offload/)：在安全、托管的云环境中运行 GPU 密集型 AI 工作负载，使用与您本地相同的 Docker Compose 工作流。

借助这些工具，您可以在本地或云中高效地开发和测试智能体 AI 应用程序，并在整个过程中使用相同的一致工作流。