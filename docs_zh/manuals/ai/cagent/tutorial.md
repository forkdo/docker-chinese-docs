---
title: 构建一个编程助手
description: 创建一个能够读取、编写和验证代码变更的编程助手，帮助你的项目开发
keywords: [cagent, tutorial, coding agent, ai assistant]
weight: 30
---

本教程将教你如何构建一个能够协助软件开发任务的编程助手。你将从一个基础助手开始，逐步添加能力，最终得到一个可用于生产的助手，它能够读取代码、修改代码、运行测试，甚至查找文档。

完成本教程后，你将掌握如何组织助手指令、配置工具，以及如何组合多个助手来处理复杂工作流。

## 你将构建的内容

一个能够：

- 读取和修改项目中的文件
- 运行测试和代码检查等命令
- 遵循结构化的开发工作流
- 在需要时查找文档
- 跟踪多步骤任务的进度

## 你将学到的内容

- 如何在 YAML 中配置 cagent 助手
- 如何为助手提供工具访问权限（文件系统、Shell 等）
- 如何编写高效的助手指令
- 如何组合多个助手处理专门任务
- 如何为自己的项目定制助手

## 前置条件

开始之前，你需要：

- **安装 cagent** - 参见 [安装指南](_index.md#installation)
- **配置 API 密钥** - 在环境中设置 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`。密钥可从 [Anthropic](https://console.anthropic.com/) 或 [OpenAI](https://platform.openai.com/api-keys) 获取
- **一个项目** - 任何你希望助手协助的代码库

## 创建你的第一个助手

cagent 助手通过 YAML 配置文件定义。最简单的助手只需要模型和定义其用途的指令。

创建一个名为 `agents.yml` 的文件：

```yaml
agents:
  root:
    model: openai/gpt-5
    description: 一个基础的编程助手
    instruction: |
      你是一个有用的编程助手。
      帮助我编写和理解代码。
```

运行你的助手：

```console
$ cagent run agents.yml
```

尝试询问："如何在 Python 中读取文件？"

助手可以回答编程问题，但还无法查看你的文件或运行命令。要让它在实际开发中发挥作用，需要为它提供工具访问权限。

## 添加工具

编程助手需要与项目文件交互并运行命令。通过添加工具集来启用这些能力。

更新 `agents.yml` 以添加文件系统和 Shell 访问权限：

```yaml
agents:
  root:
    model: openai/gpt-5
    description: 具备文件系统访问权限的编程助手
    instruction: |
      你是一个有用的编程助手。
      你可以读写文件来帮助我开发软件。
      在完成任务前，始终检查代码是否正常工作。
    toolsets:
      - type: filesystem
      - type: shell
```

运行更新后的助手并尝试："读取 README.md 文件并总结内容。"

你的助手现在可以：

- 读写当前目录中的文件
- 执行 Shell 命令
- 探索项目结构

> [!NOTE] 默认情况下，文件系统访问权限仅限于当前工作目录。如果助手需要访问其他目录，会请求权限。

助手现在可以与代码交互，但行为仍然比较通用。接下来，你将教会它如何高效工作。

## 组织助手指令

通用指令产生通用结果。对于生产环境使用，你希望助手遵循特定的工作流并理解项目的约定。

使用结构化指令更新你的助手。此示例展示了一个 Go 开发助手，但你可以将其模式适配到任何语言：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: 专家级 Go 开发者
    instruction: |
      你的目标是通过检查、修改和验证代码变更来协助代码相关任务。

      <TASK>
          # 工作流：
          # 1. 分析：理解需求并识别相关代码。
          # 2. 检查：搜索文件，分析结构和依赖关系。
          # 3. 修改：遵循最佳实践进行变更。
          # 4. 验证：运行代码检查/测试。如果发现问题，返回修改步骤。
      </TASK>

      约束条件：
      - 在修改前彻底检查
      - 始终在任务完成前验证变更
      - 将代码写入文件，不要在聊天中显示

      ## 开发工作流
      - `go build ./...` - 构建应用
      - `go test ./...` - 运行测试
      - `golangci-lint run` - 检查代码质量

    add_date: true
    add_environment_info: true
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
```

尝试询问："为 main.go 中的 `parseConfig` 函数添加错误处理"

结构化指令为你的助手提供了：

- 清晰的工作流（分析、检查、修改、验证）
- 项目特定的命令
- 防止常见错误的约束
- 环境上下文（`add_date` 和 `add_environment_info`）

`todo` 工具集帮助助手跟踪多步骤任务的进度。当你要求复杂变更时，助手会分解工作并在进行时更新进度。

## 组合多个助手

复杂任务通常需要专业助手。你可以添加处理特定职责的子助手，比如在主助手专注于编码时研究文档。

添加一个能够搜索文档的图书管理员助手：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: 专家级 Go 开发者
    instruction: |
      你的目标是通过检查、修改和验证代码变更来协助代码相关任务。

      当你需要查找文档或研究某些内容时，请咨询图书管理员助手。

      （其余指令与之前部分相同...）
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
    sub_agents:
      - librarian

  librarian:
    model: anthropic/claude-haiku-4-5
    description: 文档研究员
    instruction: |
      你是图书管理员。你的工作是查找相关文档、文章或资源来帮助开发助手。

      根据需要搜索互联网并获取网页。
    toolsets:
      - type: mcp
        ref: docker:duckduckgo
      - type: fetch
```

尝试询问："如何在 Go 中使用 `context.Context`？然后将其添加到我的服务器代码中。"

你的主助手会将研究任务委托给图书管理员，然后利用这些信息修改代码。这使主助手的上下文专注于编码任务，同时仍能访问最新的文档。

为图书管理员使用更小、更快的模型（Haiku）可以节省成本，因为文档查找不需要与代码变更相同的推理深度。

## 适配你的项目

现在你理解了核心概念，可以为你的特定项目定制助手：

### 更新开发命令

用你的项目工作流替换 Go 命令：

```yaml
## 开发工作流
- `npm test` - 运行测试
- `npm run lint` - 检查代码质量
- `npm run build` - 构建应用
```

### 添加项目特定约束

如果助手总是犯同样的错误，添加明确的约束：

```yaml
约束条件：
  - 在任务完成前始终运行测试
  - 遵循 src/ 目录中的现有代码风格
  - 永远不要修改 generated/ 目录中的文件
  - 新文件使用 TypeScript 严格模式
```

### 选择合适的模型

对于编程任务，使用注重推理的模型：

- `anthropic/claude-sonnet-4-5` - 强推理能力，适合复杂代码
- `openai/gpt-5` - 快速，良好的通用编程能力

对于文档查找等辅助任务，较小的模型效果良好：

- `anthropic/claude-haiku-4-5` - 快速且经济
- `openai/gpt-5-mini` - 适合简单任务

### 基于使用情况迭代

改进助手的最佳方法是使用它。当你发现问题时：

1. 添加特定指令以防止问题
2. 更新约束以指导行为
3. 在开发工作流中添加相关命令
4. 考虑为复杂领域添加专业子助手

## 你学到的内容

你现在知道如何：

- 创建基本的 cagent 配置
- 添加工具以启用助手能力
- 编写结构化指令以获得一致的行为
- 组合多个助手处理专门任务
- 为不同的编程语言和工作流定制助手

## 后续步骤

- 学习 [最佳实践](best-practices.md) 以处理大输出、组织助手团队和优化性能
- 将 cagent 与你的 [编辑器](integrations/acp.md) 集成，或在 MCP 客户端中将助手用作 [工具](integrations/mcp.md)
- 查看 [配置参考](reference/config.md) 了解所有可用选项
- 探索 [工具参考](reference/toolsets.md) 了解可启用的功能
- 查看 [示例配置](https://github.com/docker/cagent/tree/main/examples) 了解不同用例
- 查看完整的 [golang_developer.yaml](https://github.com/docker/cagent/blob/main/golang_developer.yaml)，这是 Docker 团队用来开发 cagent 的配置