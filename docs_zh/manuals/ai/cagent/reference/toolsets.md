---
title: 工具集参考
linkTitle: 工具集
description: cagent 工具集及其功能的完整参考
keywords: [ai, agent, cagent, tools, toolsets]
weight: 20
---

本文档介绍了 cagent 中可用的工具集及其各自的功能。工具赋予代理执行操作的能力——与文件交互、执行命令、访问外部资源以及管理状态。

有关配置文件语法以及如何在代理 YAML 中设置工具集的信息，请参阅[配置文件参考](./config.md)。

## 代理如何使用工具

为代理配置工具集后，这些工具将在代理的上下文中可用。代理可以根据当前任务，通过名称调用工具并传递适当的参数。

工具调用流程：

1. 代理分析任务并确定要使用的工具
2. 代理根据需求构建工具参数
3. cagent 执行工具并返回结果
4. 代理处理结果并决定下一步操作

代理可以按顺序调用多个工具，或根据工具结果做出决策。工具选择是自动的，基于代理对任务的理解和可用能力。

## 工具类型

cagent 支持三种类型的工具集：

内置工具集
: 直接内置于 cagent 的核心功能（`filesystem`、`shell`、`memory` 等）。这些功能提供了文件操作、命令执行和状态管理的基本能力。
MCP 工具集
: 由 Model Context Protocol 服务器提供的工具，可以是本地进程（stdio）或远程服务器（HTTP/SSE）。MCP 能够访问广泛的标准化工具生态系统。
自定义工具集
: 封装为具有类型化参数的 shell 脚本（`script_shell`）。这使您可以为特定用例定义领域专用工具。

## 配置

工具集在代理的 YAML 文件中的 `toolsets` 数组下进行配置：

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

      # 本地 MCP 服务器 (stdio)
      - type: mcp
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]

      # 远程 MCP 服务器 (SSE)
      - type: mcp
        remote:
          url: https://mcp.example.com/sse
          transport_type: sse
          headers:
            Authorization: Bearer ${API_TOKEN}

      # 自定义 shell 工具
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
| `toon`        | string           | 逗号分隔的正则表达式模式，匹配应压缩 JSON 输出的工具名称。通过使用自动编码简化/压缩匹配工具的 JSON 响应来减少令牌使用。示例：`"search.*,list.*"` |
| `defer`       | boolean or array | 控制哪些工具加载到初始上下文中。设置为 `true` 以延迟所有工具，或设置为工具名称数组以延迟特定工具。延迟工具在通过 `search_tool`/`add_tool` 显式加载之前不会消耗上下文。         |

### 工具选择

默认情况下，代理可以访问其配置工具集中的所有工具。您可以使用 `tools` 选项来限制这一点：

```yaml
toolsets:
  - type: filesystem
    tools: [read_file, write_file, list_directory]
```

这对于以下情况很有用：

- 出于安全考虑限制代理能力
- 为较小的模型减少上下文大小
- 创建具有专注工具访问权限的专业代理

### 延迟加载

延迟加载将工具保留在初始上下文窗口之外，仅在显式请求时才加载它们。这对于大多数工具不会被使用的大型工具集非常有用，可以显著减少上下文消耗。

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
    defer: [search_files, list_directory] # 仅这些工具被延迟
```

代理可以通过 `search_tool` 发现延迟工具，并在需要时通过 `add_tool` 将它们加载到上下文中。最适合包含数十个工具的工具集，其中通常只使用少数几个。

### 输出压缩

`toon` 属性压缩匹配工具的 JSON 输出以减少令牌使用。当工具的输出是 JSON 时，它会在返回给代理之前使用高效编码自动压缩：

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    toon: "search.*,list.*" # 压缩搜索/列表工具的输出
```

对于返回大型 JSON 响应（API 结果、文件列表、搜索结果）的工具很有用。压缩对代理是透明的，但可以显著减少冗长工具输出的上下文消耗。

### 每个代理的工具配置

不同的代理可以有不同的工具集：

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

这允许具有专注能力、安全边界和优化性能的专业代理。

## 内置工具参考

### Filesystem

`filesystem` 工具集赋予代理处理文件和目录的能力。代理可以读取文件以了解上下文、写入新文件、对现有文件进行有针对性的编辑、搜索内容以及探索目录结构。对于代码分析、文档更新、配置管理以及需要理解或修改项目文件的任何代理来说，这是必不可少的。

默认情况下，访问权限仅限于当前工作目录。代理可以在运行时请求访问其他目录，这需要您的批准。

#### 配置

```yaml
toolsets:
  - type: filesystem

  # 可选：限制为特定工具
  - type: filesystem
    tools: [read_file, write_file, edit_file]
```

### Shell

`shell` 工具集允许代理在系统的 shell 环境中执行命令。这对于需要运行构建、执行测试、管理进程、与 CLI 工具交互或执行系统操作的代理很有用。代理可以在前台或后台运行命令。

命令在当前工作目录中执行，并从 cagent 进程继承环境变量。此工具集功能强大，但应适当考虑安全性。

#### 配置

```yaml
toolsets:
  - type: shell
```

### Think

`think` 工具集为代理提供推理草稿板。代理可以记录想法和推理步骤，而无需采取行动或修改数据。对于需要规划多个步骤、验证要求或在长时间对话中保持上下文的复杂任务特别有用。

代理使用它来分解问题、列出适用规则、验证是否拥有所有需要的信息，并在采取行动之前记录其推理过程。

#### 配置

```yaml
toolsets:
  - type: think
```

### Todo

`todo` 工具集为代理提供任务跟踪能力，用于管理多步操作。代理可以将复杂工作分解为离散任务，跟踪每个步骤的进度，并确保在完成任务之前不会遗漏任何内容。对于处理具有多个依赖关系的复杂工作流的代理特别有价值。

`shared` 选项允许待办事项在多代理系统中跨不同代理持久存在，从而实现协调。

#### 配置

```yaml
toolsets:
  - type: todo

  # 可选：跨代理共享待办事项
  - type: todo
    shared: true
```

### Memory

`memory` 工具集允许代理跨对话和会话存储和检索信息。代理可以记住用户偏好、项目上下文、先前决策以及其他应持久存在的信息。对于随时间推移与用户交互或需要维护项目或环境状态的代理很有用。

记忆存储在本地数据库文件中，并在 cagent 会话之间持久存在。

#### 配置

```yaml
toolsets:
  - type: memory

  # 可选：指定数据库位置
  - type: memory
    path: ./agent-memories.db
```

### Fetch

`fetch` 工具集使代理能够从 HTTP/HTTPS URL 检索内容。代理可以获取文档、API 响应、网页或任何可通过 HTTP GET 请求访问的内容。对于需要访问外部资源、检查 API 文档或检索网页内容的代理很有用。

代理可以在需要身份验证或其他目的时指定自定义 HTTP 标头。

#### 配置

```yaml
toolsets:
  - type: fetch
```

### API

`api` 工具集允许您定义调用 HTTP API 的自定义工具。类似于 `script_shell`，但用于 Web 服务，这使您可以将 REST API、webhook 或任何 HTTP 端点作为代理可以使用的工具公开。代理将这些视为具有自动参数验证的类型化工具。

使用此功能与外部服务集成、调用内部 API、触发 webhook 或与任何基于 HTTP 的系统交互。

#### 配置

每个 API 工具都使用包含端点、HTTP 方法和可选类型化参数的 `api_config` 定义：

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
      instruction: 创建支持票证
      args:
        title:
          type: string
          description: 票证标题
        description:
          type: string
          description: 票证描述
      required: [title, description]
```

对于 GET 请求，参数会插入到端点 URL 中。对于 POST 请求，参数会作为 JSON 发送到请求正文中。

支持的参数类型：`string`、`number`、`boolean`、`array`、`object`。

### Script Shell

`script_shell` 工具集允许您通过将 shell 命令封装为具有类型化参数的自定义工具来定义自定义工具。这使您可以将特定领域的操作作为一等工具公开给代理。代理将这些自定义工具视为与内置工具相同，自动处理参数验证和类型检查。

使用此功能为部署脚本、构建命令、测试运行器或任何特定于项目或工作流的操作创建工具。

#### 配置

每个自定义工具都使用命令、描述和可选类型化参数定义：

```yaml
toolsets:
  - type: script_shell
    tools:
      deploy:
        cmd: ./deploy.sh
        description: 将应用程序部署到环境
        args:
          environment:
            type: string
            description: 目标环境 (dev, staging, prod)
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

您定义的工具将对代理可用。在上面的示例中，代理将可以访问 `deploy` 和 `run_tests` 工具。

## 自动工具

某些工具会根据代理的配置自动添加到代理中。您不需要显式配置这些工具——它们在需要时出现。

### transfer_task

当代理配置了 `sub_agents` 时自动可用。允许代理将任务委派给子代理并接收返回的结果。

### handoff

当代理配置了 `handoffs` 时自动可用。允许代理将整个对话转移到不同的代理。

## 下一步

- 阅读[配置文件参考](./config.md)了解 YAML 文件结构
- 查看[CLI 参考](./cli.md)了解如何运行代理
- 探索[MCP 服务器](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)以获取扩展功能
- 浏览[示例配置](https://github.com/docker/cagent/tree/main/examples)