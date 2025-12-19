---
title: 构建编码代理
description: 创建一个能够读取、写入并验证项目代码更改的编码代理
keywords: [cagent, 教程, 编码代理, AI 助手]
weight: 30
---

本教程将指导你如何构建一个能够协助软件开发任务的编码代理。你将从一个基础代理开始，逐步为其添加功能，最终得到一个生产就绪的助手，它能够读取代码、进行修改、运行测试，甚至查阅文档。

最终，你将理解如何构建代理指令、配置工具，以及如何组合多个代理以处理复杂的工作流。

## 你将构建什么

一个能够执行以下操作的编码代理：

- 读取和修改项目中的文件
- 运行测试和代码检查等命令
- 遵循结构化的开发工作流
- 在需要时查阅文档
- 跟踪多步骤任务的进度

## 你将学到什么

- 如何在 YAML 中配置 cagent 代理
- 如何让代理访问工具（文件系统、Shell 等）
- 如何编写有效的代理指令
- 如何组合多个代理以处理专门的任务
- 如何为自己的项目调整代理

## 前提条件

开始之前，你需要：

- **已安装 cagent** - 参见[安装指南](_index.md#installation)
- **已配置 API 密钥** - 在环境中设置 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`。从 [Anthropic](https://console.anthropic.com/) 或 [OpenAI](https://platform.openai.com/api-keys) 获取密钥
- **一个可供操作的项目** - 任何你希望获得代理协助的代码库

## 创建你的第一个代理

cagent 代理在 YAML 配置文件中定义。最小化的代理只需要一个模型和定义其用途的指令。

创建一个名为 `agents.yml` 的文件：

```yaml
agents:
  root:
    model: openai/gpt-5
    description: A basic coding assistant
    instruction: |
      You are a helpful coding assistant.
      Help me write and understand code.
```

运行你的代理：

```console
$ cagent run agents.yml
```

尝试提问："How do I read a file in Python?"（如何在 Python 中读取文件？）

代理可以回答编码问题，但它还无法看到你的文件或运行命令。要使其对实际开发工作有用，需要授予其工具访问权限。

## 添加工具

编码代理需要与你的项目文件交互并运行命令。通过添加工具集来启用这些功能。

更新 `agents.yml` 以添加文件系统和 Shell 访问权限：

```yaml
agents:
  root:
    model: openai/gpt-5
    description: A coding assistant with filesystem access
    instruction: |
      You are a helpful coding assistant.
      You can read and write files to help me develop software.
      Always check if code works before finishing a task.
    toolsets:
      - type: filesystem
      - type: shell
```

运行更新后的代理并尝试："Read the README.md file and summarize it."（读取 README.md 文件并总结其内容。）

你的代理现在可以：

- 读取和写入当前目录中的文件
- 执行 Shell 命令
- 探索你的项目结构

> [!NOTE] 默认情况下，文件系统访问仅限于当前工作目录。如果代理需要访问其他目录，它会请求权限。

代理现在可以与你的代码交互，但其行为仍然是通用的。接下来，你将教导它如何有效地工作。

## 构建代理指令

通用的指令产生通用的结果。对于生产用途，你希望代理遵循特定的工作流并理解你项目的约定。

使用结构化的指令更新你的代理。此示例展示了一个 Go 开发代理，但你可以针对任何语言调整此模式：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: Expert Go developer
    instruction: |
      Your goal is to help with code-related tasks by examining, modifying,
      and validating code changes.

      <TASK>
          # Workflow:
          # 1. Analyze: Understand requirements and identify relevant code.
          # 2. Examine: Search for files, analyze structure and dependencies.
          # 3. Modify: Make changes following best practices.
          # 4. Validate: Run linters/tests. If issues found, return to Modify.
      </TASK>

      Constraints:
      - Be thorough in examination before making changes
      - Always validate changes before considering the task complete
      - Write code to files, don't show it in chat

      ## Development Workflow
      - `go build ./...` - Build the application
      - `go test ./...` - Run tests
      - `golangci-lint run` - Check code quality

    add_date: true
    add_environment_info: true
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
```

尝试提问："Add error handling to the `parseConfig` function in main.go"（为 main.go 中的 `parseConfig` 函数添加错误处理）

结构化的指令为你的代理提供了：

- 一个清晰的工作流（分析、检查、修改、验证）
- 要运行的项目特定命令
- 防止常见错误的约束
- 关于环境的上下文（`add_date` 和 `add_environment_info`）

`todo` 工具集帮助代理跟踪多步骤任务的进度。当你要求进行复杂的更改时，代理会分解工作并在执行过程中更新其进度。

## 组合多个代理

复杂的任务通常受益于专门的代理。你可以添加处理特定职责的子代理，例如研究文档，而你的主代理则专注于编码。

添加一个可以搜索文档的图书管理员代理：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: Expert Go developer
    instruction: |
      Your goal is to help with code-related tasks by examining, modifying,
      and validating code changes.

      When you need to look up documentation or research how something works,
      ask the librarian agent.

      (rest of instructions from previous section...)
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
    sub_agents:
      - librarian

  librarian:
    model: anthropic/claude-haiku-4-5
    description: Documentation researcher
    instruction: |
      You are the librarian. Your job is to find relevant documentation,
      articles, or resources to help the developer agent.

      Search the internet and fetch web pages as needed.
    toolsets:
      - type: mcp
        ref: docker:duckduckgo
      - type: fetch
```

尝试提问："How do I use `context.Context` in Go? Then add it to my server code."（如何在 Go 中使用 `context.Context`？然后将其添加到我的服务器代码中。）

你的主代理会将研究任务委托给图书管理员，然后使用该信息来修改你的代码。这使得主代理的上下文专注于编码任务，同时仍然可以访问最新的文档。

为图书管理员使用更小、更快的模型（Haiku）可以节省成本，因为文档查找不需要像代码更改那样的推理深度。

## 为你的项目调整

现在你已经理解了核心概念，可以为你的特定项目调整代理：

### 更新开发命令

将 Go 命令替换为你项目的工作流：

```yaml
## Development Workflow
- `npm test` - Run tests
- `npm run lint` - Check code quality
- `npm run build` - Build the application
```

### 添加项目特定的约束

如果你的代理持续犯同样的错误，请添加明确的约束：

```yaml
Constraints:
  - Always run tests before considering a task complete
  - Follow the existing code style in src/ directories
  - Never modify files in the generated/ directory
  - Use TypeScript strict mode for new files
```

### 选择合适的模型

对于编码任务，使用注重推理的模型：

- `anthropic/claude-sonnet-4-5` - 推理能力强，适用于复杂代码
- `openai/gpt-5` - 速度快，通用编码能力好

对于文档查找等辅助任务，较小的模型效果很好：

- `anthropic/claude-haiku-4-5` - 快速且成本效益高
- `openai/gpt-5-mini` - 适用于简单任务

### 根据使用情况进行迭代

改进代理的最佳方法是使用它。当你发现问题时：

1. 添加特定指令以防止该问题
2. 更新约束以引导行为
3. 向开发工作流添加相关命令
4. 考虑为复杂领域添加专门的子代理

## 你学到了什么

你现在知道如何：

- 创建基本的 cagent 配置
- 添加工具以启用代理功能
- 编写结构化的指令以实现一致的行为
- 组合多个代理以处理专门的任务
- 针对不同的编程语言和工作流调整代理

## 后续步骤

- 学习处理大型输出、构建代理团队和优化性能的[最佳实践](best-practices.md)
- 将 cagent 与你的[编辑器](integrations/acp.md)集成，或在 [MCP 客户端](integrations/mcp.md)中将代理用作工具
- 查阅[配置参考](reference/config.md)了解所有可用选项
- 探索[工具集参考](reference/toolsets.md)以查看可以启用的功能
- 查看[示例配置](https://github.com/docker/cagent/tree/main/examples)以了解不同的用例
- 查看 Docker 团队用于开发 cagent 的完整 [golang_developer.yaml](https://github.com/docker/cagent/blob/main/golang_developer.yaml)