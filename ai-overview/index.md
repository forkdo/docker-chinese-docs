# Docker AI 概览


Docker 在你的开发工作流中提供了用于处理 AI 的工具。每个工具服务于不同的目的。

## 我需要哪个工具？

| 我想要…… | 使用 | CLI 命令 |
| --------------------------------------------------------------- | -------------------------------------------------------- | ---------------- |
| 获取 Docker 任务（容器、镜像、Dockerfile）的 AI 帮助 | [Gordon](./ai/gordon/) | `docker ai` |
| 使用兼容 OpenAI 的 API 在本地运行 AI 模型 | [Model Runner](./ai/model-runner/) | `docker model` |
| 通过 MCP 将 AI 工具连接到外部服务 | [MCP Catalog and Toolkit](./ai/mcp-catalog-and-toolkit/) | `docker mcp` |
| 构建和编排自定义多智能体团队 | [Docker Agent](./ai/docker-agent/) | `docker agent` |
| 在隔离环境中运行编码智能体 | [Docker Sandboxes](./ai/sandboxes/) | `sbx` |

## 这些工具如何关联

**Gordon** 是 Docker 内置的 AI 助手。它帮助处理 Docker 相关的任务，例如调试容器、编写 Dockerfile 和管理镜像。你可以通过 Docker Desktop 或 `docker ai` 命令与它交互。

**Docker Agent** 是一个用于在 YAML 中定义 AI 智能体团队的开源框架。你可以用特定角色、模型和工具配置智能体，然后从终端运行它们。Docker Agent 是一个通用的智能体运行时，并不特定于 Docker 任务。

**Docker Sandboxes** 提供用于运行编码智能体的隔离 microVM 环境。它支持多种智能体，包括 Claude Code、Codex、Copilot、Gemini 和 Docker Agent。Sandboxes 是隔离层——智能体本身是独立的工具。

**Model Runner** 让你在本地运行 LLM。Docker Agent 等其他工具可以使用 Model Runner 作为模型提供方。

**MCP Catalog and Toolkit** 使用模型上下文协议管理 AI 工具与外部服务之间的连接。Gordon、Docker Agent 和第三方工具都可以使用通过 Toolkit 配置的 MCP 服务器。

