---
title: 工具集参考
linkTitle: 工具集
description: cagent 工具集及其功能的完整参考
keywords: [ai, agent, cagent, tools, toolsets]
weight: 20
---

本文档参考了 cagent 中可用的工具集及其功能。工具赋予了智能体采取行动的能力——与文件交互、执行命令、访问外部资源以及管理状态。

有关配置文件语法以及如何在智能体 YAML 中设置工具集，请参阅 [配置文件参考](./config.md)。

## 智能体如何使用工具

当您为智能体配置工具集时，这些工具将变为智能体上下文中的可用资源。智能体可以通过名称和适当的参数调用工具来完成手头的任务。

工具调用流程：

1. 智能体分析任务并确定使用哪个工具
2. 智能体根据需求构建工具参数
3. cagent 执行工具并返回结果
4. 智能体处理结果并决定下一步操作

智能体可以按顺序调用多个工具，或根据工具结果做出决策。工具选择是自动的，基于智能体对任务和可用能力的理解。

## 工具类型

cagent 支持三种类型的工具集：

内置工具集
: 直接集成到 cagent 中的核心功能（`filesystem`、`shell`、`memory` 等）。这些提供了文件操作、命令执行和状态管理的基本能力。
MCP 工具集
: 由 Model Context Protocol 服务器提供的工具，可以是本地进程（stdio）或远程服务器（HTTP/SSE）。MCP 能够访问广泛的标准化工具生态系统。
自定义工具集
: 使用类型化参数包装的 Shell 脚本（`script_shell`）。这允许您为特定用例定义领域特定的工具。

## 配置

工具集在智能体的 YAML 文件中的 `toolsets` 数组下配置：

```yaml
agents:
  my_agent:
    model: anthropic/claude-sonnet-4-5
    description: 一个有用的编码助手
    toolsets:
      # 内置工具集
      - type: filesystem

      # 带配置的内置工具集
      - type: memory
        path: ./memories.db

      # 本地 MCP 服务器（stdio）
      - type: mcp
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]

      # 远程 MCP 服务器（SSE）
      - type: mcp
        remote:
          url: https://mcp.example.com/sse
          transport_type: sse
          headers:
            Authorization: Bearer ${API_TOKEN}

      # 自定义 Shell 工具
      - type: script_shell
        tools:
          build:
            cmd: npm run build
            description: 构建项目
```

### 通用配置选项

所有工具集类型都支持以下可选属性：

| 属性          | 类型             | 描述                                                                                                                                                                                                                         |
| ------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instruction` | string           | 使用工具集的附加说明                                                                                                                                                                                       |
| `tools`       | array            | 要启用的特定工具名称（默认为全部）                                                                                                                                                                                     |
| `env`         | object           | 工具集的环境变量                                                                                                                                                                                               |
| `toon`        | string           | 匹配工具名称的逗号分隔正则表达式模式，这些工具的 JSON 输出应被压缩。通过使用自动编码简化/压缩匹配工具的 JSON 响应来减少令牌使用量。示例：`"search.*,list.*"` |
| `defer`       | boolean or array | 控制哪些工具加载到初始上下文中。设置为 `true` 以延迟所有工具，或设置为工具名称数组以延迟特定工具。延迟的工具不会消耗上下文，直到通过 `search_tool`/`add_tool` 显式加载。         |

### 工具选择

默认情况下，智能体可以访问其配置工具集中的所有工具。您可以使用 `tools` 选项限制此范围：

```yaml
toolsets:
  - type: filesystem
    tools: [read_file, write_file, list_directory]
```

这在以下情况下很有用：

- 为了安全而限制智能体能力
- 为较小的模型减少上下文大小
- 创建具有专注工具访问权限的专业智能体

### 延迟加载

延迟加载将工具保留在初始上下文窗口之外，仅在显式请求时加载它们。这对于大多数工具不会使用的大型工具集很有用，可以显著减少上下文消耗。

延迟工具集中的所有工具：

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: true # 所有工具按需加载
```

或延迟特定工具，同时立即加载其他工具：

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: [search_files, list_directory] # 仅延迟这些工具
```

智能体可以通过 `search_tool` 发现延迟的工具，并在需要时通过 `add_tool` 将其加载到上下文中。最适合具有数十个工具而通常只使用其中几个的工具集。

### 输出压缩

`toon` 属性压缩匹配工具的 JSON 输出以减少令牌使用量。当工具的输出是 JSON 时，它会在返回给智能体之前使用高效编码自动压缩：

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    toon: "search.*,list.*" # 压缩搜索/列表工具的输出
```

这对于返回大型 JSON 响应的工具很有用（API 结果、文件列表、搜索结果）。压缩对智能体是透明的，但可以显著减少冗长工具输出的上下文消耗。

### 每个智能体的工具配置

不同的智能体可以有不同的工具集：

```yaml
agents:
  coordinator:
    model: anthropic/claude-sonnet-4-5
    sub_agents: [code_writer, code_reviewer]
    toolsets:
      - type: filesystem
        tools: [read_file]

  code_writer:
    model: openai/gpt-5-mini
    toolsets:
      - type: filesystem
      - type: shell

  code_reviewer:
    model: anthropic/claude-sonnet-4-5
    toolsets:
      - type: filesystem
        tools: [read_file, read_multiple_files]
```

这允许具有专注能力、安全边界和优化性能的专业智能体。

## 内置工具参考

### Filesystem

`filesystem` 工具集赋予您的智能体处理文件和目录的能力。您的智能体可以读取文件以理解上下文、编写新文件、对现有文件进行有针对性的编辑、搜索内容以及探索目录结构。对于代码分析、文档更新、配置管理和任何需要理解或修改项目文件的智能体来说，这是必不可少的。

默认情况下，访问仅限于当前工作目录。智能体可以在运行时请求访问其他目录，这需要您的批准。

#### 配置

```yaml
toolsets:
  - type: filesystem

  # 可选：限制为特定工具
  - type: filesystem
    tools: [read_file, write_file, edit_file]
```

### Shell

`shell` 工具集让您的智能体能够在系统的 Shell 环境中执行命令。对于需要运行构建、执行测试、管理进程、与 CLI 工具交互或执行系统操作的智能体使用此工具。智能体可以在前台或后台运行命令。

命令在当前工作目录中执行，并继承 cagent 进程的环境变量。此工具集功能强大，但应适当考虑安全性。

#### 配置

```yaml
toolsets:
  - type: shell
```

### Think

`think` 工具集为您的智能体提供推理草稿本。智能体可以记录想法和推理步骤，而不采取行动或修改数据。对于智能体需要规划多个步骤、验证要求或在长时间对话中维护上下文的复杂任务特别有用。

智能体使用此工具来分解问题、列出适用规则、验证他们是否拥有所有必要信息，并在行动前记录他们的推理过程。

#### 配置

```yaml
toolsets:
  - type: think
```

### Todo

`todo` 工具集为您的智能体提供任务跟踪能力，用于管理多步骤操作。您的智能体可以将复杂工作分解为离散任务，跟踪每个步骤的进度，并确保在完成请求之前不遗漏任何内容。对于处理具有多个依赖关系的复杂工作流的智能体特别有价值。

`shared` 选项允许待办事项在多智能体系统中的不同智能体之间持续存在，从而实现协调。

#### 配置

```yaml
toolsets:
  - type: todo

  # 可选：在智能体之间共享待办事项
  - type: todo
    shared: true
```

### Memory

`memory` 工具集允许您的智能体在对话和会话之间存储和检索信息。您的智能体可以记住用户偏好、项目上下文、先前决策和其他应持续存在的信息。对于随时间与用户交互或需要维护有关项目或环境状态的智能体很有用。

记忆存储在本地数据库文件中，并在 cagent 会话之间持续存在。

#### 配置

```yaml
toolsets:
  - type: memory

  # 可选：指定数据库位置
  - type: memory
    path: ./agent-memories.db
```

### Fetch

`fetch` 工具集使您的智能体能够从 HTTP/HTTPS URL 检索内容。您的智能体可以获取文档、API 响应、网页或任何可通过 HTTP GET 请求访问的内容。对于需要访问外部资源、检查 API 文档或检索网络内容的智能体很有用。

智能体可以在需要时为身份验证或其他目的指定自定义 HTTP 标头。

#### 配置

```yaml
toolsets:
  - type: fetch
```

### API

`api` 工具集允许您定义调用 HTTP API 的自定义工具。类似于 `script_shell`，但用于 Web 服务，这允许您将 REST API、Webhook 或任何 HTTP 端点作为智能体可以使用的工具公开。智能体将这些视为具有自动参数验证的类型化工具。

使用此工具集成外部服务、调用内部 API、触发 Webhook 或与任何基于 HTTP 的系统交互。

#### 配置

每个 API 工具都使用 `api_config` 定义，其中包含端点、HTTP 方法和可选的类型化参数：

```yaml
toolsets:
  - type: api
    api_config:
      name: search_docs
      endpoint: https://api.example.com/search
      method: GET
      instruction: 搜索文档数据库
      headers:
        Authorization: Bearer ${API_TOKEN}
      args:
        query:
          type: string
          description: 搜索查询
        limit:
          type: number
          description: 最大结果数
      required: [query]

  - type: api
    api_config:
      name: create_ticket
      endpoint: https://api.example.com/tickets
      method: POST
      instruction: 创建支持工单
      args:
        title:
          type: string
          description: 工单标题
        description:
          type: string
          description: 工单描述
      required: [title, description]
```

对于 GET 请求，参数被插入到端点 URL 中。对于 POST 请求，参数作为 JSON 发送到请求体中。

支持的参数类型：`string`、`number`、`boolean`、`array`、`object`。

### Script Shell

`script_shell` 工具集允许您通过用类型化参数包装 Shell 命令来定义自定义工具。这允许您将特定领域的操作作为一等工具公开给您的智能体。智能体将这些自定义工具视为内置工具，参数验证和类型检查自动处理。

使用此工具为部署脚本、构建命令、测试运行器或您项目或工作流中的任何特定操作创建工具。

#### 配置

每个自定义工具都使用命令、描述和可选的类型化参数定义：

```yaml
toolsets:
  - type: script_shell
    tools:
      deploy:
        cmd: ./deploy.sh
        description: 将应用程序部署到环境中
        args:
          environment:
            type: string
            description: 目标环境（dev、staging、prod）
          version:
            type: string
            description: 要部署的版本
        required: [environment]

      run_tests:
        cmd: npm test
        description: 运行测试套件
        args:
          filter:
            type: string
            description: 测试名称过滤模式
```

支持的参数类型：`string`、`number`、`boolean`、`array`、`object`。

#### 工具

您定义的工具将对您的智能体可用。在前面的示例中，智能体将可以访问 `deploy` 和 `run_tests` 工具。

## 自动工具

某些工具会根据智能体的配置自动添加到智能体中。您不需要显式配置这些工具——它们在需要时出现。

### transfer_task

当您的智能体配置了 `sub_agents` 时自动可用。允许智能体将任务委托给子智能体并接收结果。

### handoff

当您的智能体配置了 `handoffs` 时自动可用。允许智能体将整个对话转移到不同的智能体。

## 接下来

- 阅读 [配置文件参考](./config.md) 了解 YAML 文件结构
- 查看 [CLI 参考](./cli.md) 了解运行智能体
- 探索 [MCP 服务器](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 以获得扩展功能
- 浏览 [示例配置](https://github.com/docker/cagent/tree/main/examples)