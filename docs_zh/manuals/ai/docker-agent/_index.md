---
title: Docker Agent
description: Docker Agent 让你能够构建、编排并共享像团队一样协同工作的 AI 智能体。
weight: 60
aliases:
  - /ai/cagent/
  - /manuals/ai/cagent/
  - /ai/docker-agent/integrations/
  - /ai/docker-agent/reference/
  - /ai/docker-agent/reference/examples/
params:
  sidebar:
    group: AI and agents
keywords: [ai, agent, docker agent, cagent]
---

[Docker Agent](https://github.com/docker/docker-agent) 是一个用于构建由专业 AI 智能体组成的团队的开源框架。与其调用一个通用的模型，不如为智能体定义特定的角色与指令，让它们相互协作来解决问题。你可以从终端使用任何 LLM 提供商来运行这些智能体团队。

> [!NOTE]
> Docker Agent 是用于构建和运行自定义智能体团队的框架。
> 如需 Docker 内置的 AI 助手，请参阅 [Gordon](/ai/gordon/)（`docker ai`）。

## 为何使用智能体团队（Why agent teams）

让单个智能体处理复杂工作意味着不断地进行上下文切换。不妨将工作拆分给各自专注的智能体——每个智能体负责其最擅长的部分。Docker Agent 负责管理它们之间的协调。

下面是一个用于排查问题的双智能体团队：

```yaml
agents:
  root:
    model: openai/gpt-5-mini # Change to the model that you want to use
    description: Bug investigator
    instruction: |
      Analyze error messages, stack traces, and code to find bug root causes.
      Explain what's wrong and why it's happening.
      Delegate fix implementation to the fixer agent.
    sub_agents: [fixer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo

  fixer:
    model: anthropic/claude-sonnet-4-5 # Change to the model that you want to use
    description: Fix implementer
    instruction: |
      Write fixes for bugs diagnosed by the investigator.
      Make minimal, targeted changes and add tests to prevent regression.
    toolsets:
      - type: filesystem
      - type: shell
```

root 智能体负责调查并解释问题。当它理解了问题后，就会转交给 `fixer` 去实施修复。每个智能体都专注于自己的专长领域。

## 安装（Installation）

Docker Agent 已包含在 Docker Desktop 4.63 及更高版本中。在 Docker Desktop 4.49 到 4.62 版本中，该功能被称为 cagent。

对于 Docker Engine 用户或自定义安装：

- **Homebrew**：`brew install docker-agent`
- **Winget**：`winget install Docker.Agent`
- **预编译二进制文件**：[GitHub
  releases](https://github.com/docker/docker-agent/releases)
- **从源码构建**：参阅 [Docker Agent
  repository](https://github.com/docker/docker-agent?tab=readme-ov-file#build-from-source)

`docker-agent` 二进制文件应被复制到 `~/.docker/cli-plugins`，随后即可通过 `docker agent` 命令使用。或者，也可以将其作为独立二进制文件使用。

## 快速开始（Get started）

尝试运行这个缺陷分析团队：

1. 为你想使用的模型提供商设置 API 密钥：

   ```console
   $ export ANTHROPIC_API_KEY=<your_key>  # For Claude models
   $ export OPENAI_API_KEY=<your_key>     # For OpenAI models
   $ export GOOGLE_API_KEY=<your_key>     # For Gemini models
   ```

2. 将[示例配置](#why-agent-teams)保存为 `debugger.yaml`。

3. 运行你的智能体团队：

   ```console
   $ docker agent run debugger.yaml
   ```

你会看到一个提示符，可以在其中描述缺陷或粘贴错误信息。调查智能体分析问题，然后转交给修复智能体去实施。

## 工作原理（How it works）

你与*root 智能体*交互，它可以将工作委派给你定义的子智能体。每个智能体：

- 使用自己的模型与参数
- 拥有自己的上下文（智能体之间不共享知识）
- 可以访问内置工具，如待办列表、记忆和任务委派
- 可以通过 [MCP
  servers](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 使用外部工具

root 智能体将任务委派给列在 `sub_agents` 下的智能体。子智能体也可以拥有自己的子智能体，从而形成更深的层级结构。

## 配置选项（Configuration options）

智能体配置是 YAML 文件。基本结构如下：

```yaml
agents:
  root:
    model: claude-sonnet-4-0
    description: Brief role summary
    instruction: |
      Detailed instructions for this agent...
    sub_agents: [helper]

  helper:
    model: gpt-5-mini
    description: Specialist agent role
    instruction: |
      Instructions for the helper agent...
```

你还可以配置模型设置（如上下文限制）、工具（包括 MCP 服务器）等。完整细节请参阅[配置参考](./configuration/overview/index.md)。

## 共享智能体团队（Share agent teams）

智能体配置被打包为 OCI 制品。可以像容器镜像一样推送和拉取它们：

```console
$ docker agent share push ./debugger.yaml myusername/debugger
$ docker agent share pull myusername/debugger
```

可以使用 Docker Hub 或任何兼容 OCI 的注册表。如果仓库尚不存在，推送时会自动创建。

## 下一步（What's next）

- 跟随[快速入门](./getting-started/quickstart/index.md)构建你的第一个智能体
- 学习构建高效智能体的[最佳实践](./guides/tips/index.md)
- 将 Docker Agent 集成到你的[编辑器](./features/acp/index.md)中，或把智能体用作
  [MCP 客户端中的工具](./tools/mcp/index.md)
- 在 [Docker Agent
  repository](https://github.com/docker/docker-agent/tree/main/examples) 中浏览示例智能体配置
- 通过 [Docker MCP
  Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 将智能体连接到外部工具
- 阅读完整的[配置参考](./configuration/overview/index.md)
