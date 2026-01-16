---
title: 配置文件参考
url: /ai/cagent/reference/config/
parent:
  title: cagent
  url: /ai/cagent/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: cagent
    url: /ai/cagent/
  - title: 配置文件参考
    url: /ai/cagent/reference/config/
prev:
  title: 工具集参考
  url: /ai/cagent/reference/toolsets/
---


本文档记录了 cagent 代理的 YAML 配置文件格式。
它涵盖了文件结构、代理参数、模型配置、工具集设置以及 RAG 来源。

有关每个工具集的功能和特定选项的详细文档，请参阅 [工具集参考](./toolsets.md)。

## 文件结构

配置文件有四个顶级部分：

```yaml
agents: # 必需 - 代理定义
  root:
    model: anthropic/claude-sonnet-4-5
    description: 此代理的功能
    instruction: 它应如何行为

models: # 可选 - 模型配置
  custom_model:
    provider: openai
    model: gpt-5

rag: # 可选 - RAG 来源
  docs:
    docs: [./documents]
    strategies: [...]

metadata: # 可选 - 作者、许可证、自述文件
  author: 您的姓名
```

## 代理

| 属性                   | 类型    | 描述                                         | 是否必需 |
| ---------------------- | ------- | -------------------------------------------- | -------- |
| `model`                | string  | 模型引用或名称                               | 是       |
| `description`          | string  | 代理用途的简要描述                           | 否       |
| `instruction`          | string  | 详细的行为指令                               | 是       |
| `sub_agents`           | array   | 用于任务委派的代理名称                       | 否       |
| `handoffs`             | array   | 用于对话转接的代理名称                       | 否       |
| `toolsets`             | array   | 可用工具                                     | 否       |
| `welcome_message`      | string  | 启动时显示的消息                             | 否       |
| `add_date`             | boolean | 在上下文中包含当前日期                       | 否       |
| `add_environment_info` | boolean | 包含工作目录、操作系统、Git 信息             | 否       |
| `add_prompt_files`     | array   | 要包含的提示文件路径                         | 否       |
| `max_iterations`       | integer | 最大工具调用循环次数（未设置则为无限）       | 否       |
| `num_history_items`    | integer | 对话历史记录限制                             | 否       |
| `code_mode_tools`      | boolean | 为工具启用代码模式                           | 否       |
| `commands`             | object  | 可通过 `/command_name` 访问的命名提示         | 否       |
| `structured_output`    | object  | 结构化响应的 JSON 模式                       | 否       |
| `rag`                  | array   | RAG 来源名称                                 | 否       |

### 任务委派与对话转接

代理支持两种不同的委派机制。根据您需要任务结果还是对话控制来选择。

#### Sub_agents：分层任务委派

使用 `sub_agents` 进行分层任务委派。父代理使用 `transfer_task` 工具将特定任务分配给子代理。子代理在其自己的上下文中执行并返回结果。父代理保持控制权，并可以按顺序委派给多个代理。

这适用于结构化工作流，您需要组合来自专家的结果，或者任务有明确的边界。每个委派的任务独立运行并向父代理报告。

**示例：**

```yaml
agents:
  root:
    sub_agents: [researcher, analyst]
    instruction: |
      将研究委派给 researcher。
      将分析委派给 analyst。
      组合结果并呈现发现。
```

根代理调用：`transfer_task(agent="researcher", task="Find pricing data")`。研究员完成任务并将结果返回给根代理。

#### Handoffs：对话转接

使用 `handoffs` 将对话控制权转接给不同的代理。当一个代理使用 `handoff` 工具时，新代理将完全接管。原始代理退后，直到有人将其转回。

这适用于不同的代理应拥有正在进行的对话的不同部分，或者当专家需要作为同行协作而无需协调员管理每一步时。

**示例：**

```yaml
agents:
  generalist:
    handoffs: [database_expert, security_expert]
    instruction: |
      帮助解决一般开发问题。
      如果对话转向数据库优化，
      则转接给 database_expert。
      如果出现安全问题，则转接给 security_expert。

  database_expert:
    handoffs: [generalist, security_expert]
    instruction: 处理数据库设计和优化。

  security_expert:
    handoffs: [generalist, database_expert]
    instruction: 审查代码中的安全漏洞。
```

当用户询问查询性能时，generalist 执行：`handoff(agent="database_expert")`。数据库专家现在拥有对话权，可以直接与用户继续工作，或者如果讨论转向 SQL 注入问题，则转接给 security_expert。

### 命令

用户通过 `/command_name` 调用的命名提示。支持 JavaScript 模板字面量，使用 `${env.VARIABLE}` 表示环境变量：

```yaml
commands:
  greet: "向 ${env.USER} 问好"
  analyze: "分析 ${env.PROJECT_NAME || 'demo'}"
```

运行命令：`cagent run config.yaml /greet`

### 结构化输出

将响应约束为 JSON 模式（仅限 OpenAI 和 Gemini）：

```yaml
structured_output:
  name: code_analysis
  strict: true
  schema:
    type: object
    properties:
      issues:
        type: array
        items: { ... }
    required: [issues]
```

## 模型

| 属性                  | 类型    | 描述                                         | 是否必需 |
| --------------------- | ------- | -------------------------------------------- | -------- |
| `provider`            | string  | `openai`, `anthropic`, `google`, `dmr`       | 是       |
| `model`               | string  | 模型名称                                     | 是       |
| `temperature`         | float   | 随机性 (0.0-2.0)                             | 否       |
| `max_tokens`          | integer | 最大响应长度                                 | 否       |
| `top_p`               | float   | 核心采样 (0.0-1.0)                           | 否       |
| `frequency_penalty`   | float   | 重复惩罚 (-2.0 到 2.0，仅限 OpenAI)          | 否       |
| `presence_penalty`    | float   | 主题惩罚 (-2.0 到 2.0，仅限 OpenAI)          | 否       |
| `base_url`            | string  | 自定义 API 端点                              | 否       |
| `parallel_tool_calls` | boolean | 启用并行工具执行（默认：true）               | 否       |
| `token_key`           | string  | 认证令牌密钥                                 | 否       |
| `track_usage`         | boolean | 跟踪令牌使用情况                             | 否       |
| `thinking_budget`     | mixed   | 推理努力（特定于提供者）                     | 否       |
| `provider_opts`       | object  | 特定于提供者的选项                           | 否       |

### 合金模型

通过用逗号分隔名称来轮换使用多个模型：

```yaml
model: anthropic/claude-sonnet-4-5,openai/gpt-5
```

### 思考预算

控制推理深度。配置因提供者而异：

- **OpenAI**：字符串值 - `minimal`, `low`, `medium`, `high`
- **Anthropic**：整数令牌预算 (1024-32768，必须小于 `max_tokens`)
  - 设置 `provider_opts.interleaved_thinking: true` 以在推理期间使用工具
- **Gemini**：整数令牌预算 (0 禁用，-1 为动态，最大 24576)
  - Gemini 2.5 Pro：128-32768，无法禁用（最小 128）

```yaml
# OpenAI
thinking_budget: low

# Anthropic
thinking_budget: 8192
provider_opts:
  interleaved_thinking: true

# Gemini
thinking_budget: 8192    # 固定
thinking_budget: -1      # 动态
thinking_budget: 0       # 禁用
```

### Docker 模型运行器 (DMR)

运行本地模型。如果省略 `base_url`，cagent 会通过 Docker 模型插件自动发现。

```yaml
provider: dmr
model: ai/qwen3
max_tokens: 8192
base_url: http://localhost:12434/engines/llama.cpp/v1 # 可选
```

通过 `provider_opts.runtime_flags` 传递 llama.cpp 选项（数组、字符串或多行）：

```yaml
provider_opts:
  runtime_flags: ["--ngl=33", "--threads=8"]
  # 或: runtime_flags: "--ngl=33 --threads=8"
```

模型配置字段会自动映射到运行时标志：

- `temperature` → `--temp`
- `top_p` → `--top-p`
- `max_tokens` → `--context-size`

显式的 `runtime_flags` 会覆盖自动映射的标志。

用于更快推理的推测解码：

```yaml
provider_opts:
  speculative_draft_model: ai/qwen3:0.6B-F16
  speculative_num_tokens: 16
  speculative_acceptance_rate: 0.8
```

## 工具

在 `toolsets` 数组中配置工具。三种类型：内置工具、MCP（本地/远程）和 Docker 网关。

> [!NOTE] 本节涵盖工具集配置语法。有关每个工具集的功能、可用工具和特定配置选项的详细文档，请参阅 [工具集参考](./toolsets.md)。

所有工具集都支持通用属性，如 `tools`（白名单）、`defer`（延迟加载）、`toon`（输出压缩）、`env`（环境变量）和 `instruction`（使用指南）。有关这些属性以及每个工具集功能的详细信息，请参阅 [工具集参考](./toolsets.md)。

### 内置工具

```yaml
toolsets:
  - type: filesystem
  - type: shell
  - type: think
  - type: todo
    shared: true
  - type: memory
    path: ./memory.db
```

### MCP 工具

本地进程：

```yaml
- type: mcp
  command: npx
  args:
    ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
  tools: ["read_file", "write_file"] # 可选：限制为特定工具
  env:
    NODE_OPTIONS: "--max-old-space-size=8192"
```

远程服务器：

```yaml
- type: mcp
  remote:
    url: https://mcp-server.example.com
    transport_type: sse
    headers:
      Authorization: Bearer token
```

### Docker MCP 网关

来自 [Docker MCP 目录](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md) 的容器化工具：

```yaml
- type: mcp
  ref: docker:duckduckgo
```

## RAG

用于文档知识库的检索增强生成。在顶层定义来源，并在代理中引用。

```yaml
rag:
  docs:
    docs: [./documents, ./README.md]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./embeddings.db

agents:
  root:
    rag: [docs]
```

### 检索策略

所有策略都支持分块配置。分块大小和重叠以字符（Unicode 码点）为单位测量，而不是令牌。

#### Chunked-embeddings

使用向量嵌入进行直接语义搜索。最适合理解意图、同义词和释义。

| 字段                              | 类型    | 默认值 |
| ---------------------------------- | ------- | ------ |
| `embedding_model`                  | string  | -      |
| `database`                         | string  | -      |
| `vector_dimensions`                | integer | -      |
| `similarity_metric`                | string  | cosine |
| `threshold`                        | float   | 0.5    |
| `limit`                            | integer | 5      |
| `chunking.size`                    | integer | 1000   |
| `chunking.overlap`                 | integer | 75     |
| `chunking.respect_word_boundaries` | boolean | true   |
| `chunking.code_aware`              | boolean | false  |

```yaml
- type: chunked-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  database: ./vector.db
  similarity_metric: cosine_similarity
  threshold: 0.5
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

#### Semantic-embeddings

LLM 增强的语义搜索。使用语言模型在嵌入之前为每个分块生成丰富的语义摘要，以捕获更深层的含义。

| 字段                              | 类型    | 默认值 |
| ---------------------------------- | ------- | ------ |
| `embedding_model`                  | string  | -      |
| `chat_model`                       | string  | -      |
| `database`                         | string  | -      |
| `vector_dimensions`                | integer | -      |
| `similarity_metric`                | string  | cosine |
| `threshold`                        | float   | 0.5    |
| `limit`                            | integer | 5      |
| `ast_context`                      | boolean | false  |
| `semantic_prompt`                  | string  | -      |
| `chunking.size`                    | integer | 1000   |
| `chunking.overlap`                 | integer | 75     |
| `chunking.respect_word_boundaries` | boolean | true   |
| `chunking.code_aware`              | boolean | false  |

```yaml
- type: semantic-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  chat_model: openai/gpt-5-mini
  database: ./semantic.db
  threshold: 0.3
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

#### BM25

使用 BM25 算法的基于关键字的搜索。最适合精确术语、技术术语和代码标识符。

| 字段                              | 类型    | 默认值 |
| ---------------------------------- | ------- | ------ |
| `database`                         | string  | -      |
| `k1`                               | float   | 1.5    |
| `b`                                | float   | 0.75   |
| `threshold`                        | float   | 0.0    |
| `limit`                            | integer | 5      |
| `chunking.size`                    | integer | 1000   |
| `chunking.overlap`                 | integer | 75     |
| `chunking.respect_word_boundaries` | boolean | true   |
| `chunking.code_aware`              | boolean | false  |

```yaml
- type: bm25
  database: ./bm25.db
  k1: 1.5
  b: 0.75
  threshold: 0.3
  limit: 10
  chunking:
    size: 1000
    overlap: 100
```

### 混合检索

使用融合组合多种策略：

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    vector_dimensions: 1536
    database: ./vector.db
    limit: 20
  - type: bm25
    database: ./bm25.db
    limit: 15

results:
  fusion:
    strategy: rrf # 选项: rrf, weighted, max
    k: 60 # RRF 平滑参数
  deduplicate: true
  limit: 5
```

融合策略：

- `rrf`：互逆排名融合（推荐，基于排名，无需归一化）
- `weighted`：加权组合（`fusion.weights: {chunked-embeddings: 0.7, bm25: 0.3}`）
- `max`：跨策略的最大分数

### 重新排序

使用专门的模型对结果进行重新评分，以提高相关性：

```yaml
results:
  reranking:
    model: openai/gpt-5-mini
    top_k: 10 # 仅重新排序前 K 个 (0 = 全部)
    threshold: 0.3 # 重新排序后的最低分数
    criteria: | # 可选的领域特定指导
      优先考虑官方文档而非博客文章
  limit: 5
```

DMR 原生重新排序：

```yaml
models:
  reranker:
    provider: dmr
    model: hf.co/ggml-org/qwen3-reranker-0.6b-q8_0-gguf

results:
  reranking:
    model: reranker
```

### 代码感知分块

对于源代码，使用基于 AST 的分块。使用语义嵌入时，可以在 LLM 提示中包含 AST 元数据：

```yaml
- type: semantic-embeddings
  embedding_model: openai/text-embedding-3-small
  vector_dimensions: 1536
  chat_model: openai/gpt-5-mini
  database: ./code.db
  ast_context: true # 在语义提示中包含 AST 元数据
  chunking:
    size: 2000
    code_aware: true # 启用基于 AST 的分块
```

### RAG 属性

顶级 RAG 来源：

| 字段         | 类型      | 描述                                                         |
| ------------ | --------- | ------------------------------------------------------------ |
| `docs`       | []string  | 文档路径（支持通配符模式，尊重 `.gitignore`）                |
| `tool`       | object    | 自定义 RAG 工具名称/描述/指令                                |
| `strategies` | []object  | 检索策略（有关策略特定字段，请参见上文）                     |
| `results`    | object    | 后处理（融合、重新排序、限制）                               |

结果：

| 字段                  | 类型    | 默认值 |
| --------------------- | ------- | ------ |
| `limit`               | integer | 15     |
| `deduplicate`         | boolean | true   |
| `include_score`       | boolean | false  |
| `fusion.strategy`     | string  | -      |
| `fusion.k`            | integer | 60     |
| `fusion.weights`      | object  | -      |
| `reranking.model`     | string  | -      |
| `reranking.top_k`     | integer | 0      |
| `reranking.threshold` | float   | 0.5    |
| `reranking.criteria`  | string  | ""     |
| `return_full_content` | boolean | false  |

## 元数据

文档和共享信息：

| 属性      | 类型   | 描述                     |
| --------- | ------ | ------------------------ |
| `author`  | string | 作者名称                 |
| `license` | string | 许可证（例如 MIT, Apache-2.0） |
| `readme`  | string | 使用文档                 |

```yaml
metadata:
  author: 您的姓名
  license: MIT
  readme: |
    描述和使用说明
```

## 示例配置

展示关键功能的完整配置：

```yaml
agents:
  root:
    model: claude
    description: 技术负责人
    instruction: 协调开发任务并委派给专家
    sub_agents: [developer, reviewer]
    toolsets:
      - type: filesystem
      - type: mcp
        ref: docker:duckduckgo
    rag: [readmes]
    commands:
      status: "检查项目状态"

  developer:
    model: gpt
    description: 软件开发人员
    instruction: 编写干净、可维护的代码
    toolsets:
      - type: filesystem
      - type: shell

  reviewer:
    model: claude
    description: 代码审查员
    instruction: 审查质量和安全性
    toolsets:
      - type: filesystem

models:
  gpt:
    provider: openai
    model: gpt-5

  claude:
    provider: anthropic
    model: claude-sonnet-4-5
    max_tokens: 64000

rag:
  readmes:
    docs: ["**/README.md"]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./embeddings.db
        limit: 10
      - type: bm25
        database: ./bm25.db
        limit: 10
    results:
      fusion:
        strategy: rrf
        k: 60
      limit: 5
```

## 下一步

- 阅读 [工具集参考](./toolsets.md) 以获取详细的工具集文档
- 查看 [CLI 参考](./cli.md) 以了解命令行选项
- 浏览 [示例配置](https://github.com/docker/cagent/tree/main/examples)
- 了解 [共享代理](../sharing-agents.md)
