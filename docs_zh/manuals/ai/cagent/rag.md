---
title: RAG
description: RAG 如何为 cagent 智能体提供代码库和文档的访问能力
keywords: [cagent, rag, retrieval, embeddings, semantic search]
weight: 70
---

当你在 cagent 中配置一个 RAG 源时，你的智能体会自动获得一个针对该知识库的搜索工具。智能体自行决定何时进行搜索，仅检索相关信息，并使用这些信息来回答问题或完成任务——所有这些都无需你手动管理提示词中的内容。

本指南解释了 cagent 的 RAG 系统如何工作、何时使用它，以及如何为你的内容有效配置。

> [!NOTE]
> RAG 是一个高级功能，需要配置和调优。默认设置足以入门，但针对你的特定内容和使用场景定制配置能显著改善结果。

## 问题：上下文过多

你的智能体可以处理整个代码库，但无法将所有内容都放入其上下文窗口。即使有 200K token 的限制，中等规模的项目仍然过大。在数百个文件中查找相关代码会浪费上下文。

文件系统工具帮助智能体读取文件，但智能体必须猜测要读取哪些文件。它无法按含义搜索，只能按文件名搜索。当你要求"查找重试逻辑"时，智能体会读取文件，希望能偶然找到正确的代码。

Grep 可以找到精确的文本匹配，但会错过相关概念。搜索"authentication"不会找到使用"auth"或"login"的代码。你要么得到数百个匹配结果，要么一个都没有，而且 grep 不理解代码结构——它只是匹配任何位置出现的字符串。

RAG 提前为你的内容建立索引并支持语义搜索。智能体按含义而非精确词汇搜索预索引内容。它只检索尊重代码结构的相关片段。不会在探索中浪费上下文。

## RAG 在 cagent 中如何工作

在你的 cagent 配置中配置一个 RAG 源：

```yaml
rag:
  codebase:
    docs: [./src, ./pkg]
    strategies:
      - type: chunked-embeddings
        embedding_model: openai/text-embedding-3-small
        vector_dimensions: 1536
        database: ./code.db

agents:
  root:
    model: openai/gpt-5
    instruction: You are a coding assistant. Search the codebase when needed.
    rag: [codebase]
```

当你引用 `rag: [codebase]` 时，cagent 会：

1. **启动时** - 为你的文档建立索引（仅在首次运行时，会阻塞直到完成）
2. **对话期间** - 为智能体提供搜索工具
3. **智能体搜索时** - 检索相关片段并将其添加到上下文
4. **文件变更时** - 自动重新索引修改的文件

智能体根据对话情况决定何时搜索。你不需要管理上下文中包含的内容——智能体会自己管理。

### 索引过程

首次运行时，cagent 会：

- 从配置的路径读取文件
- 遵守 `.gitignore` 模式（可以禁用）
- 将文档分割成片段
- 使用你选择的策略创建可搜索的表示
- 将所有内容存储在本地数据库中

后续运行会重用索引。如果文件发生更改，cagent 会检测到并仅重新索引更改的内容，使你的知识库保持最新，无需手动干预。

## 检索策略

不同的内容需要不同的检索方法。cagent 支持三种策略，每种都针对不同的使用场景进行了优化。默认设置效果良好，但理解其中的权衡有助于你选择正确的方法。

### 语义搜索（chunked-embeddings）

将文本转换为表示含义的向量，支持按概念而非精确词汇搜索：

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    vector_dimensions: 1536
    database: ./docs.db
    chunking:
      size: 1000
      overlap: 100
```

在索引期间，文档被分割成片段，每个片段由嵌入模型转换为 1536 维的向量。这些向量本质上是高维空间中的坐标，相似的概念在其中位置相近。

当你搜索"如何验证用户身份？"时，你的查询会变成一个向量，数据库使用余弦相似度（测量向量之间的角度）找到向量邻近的片段。嵌入模型学习到"authentication"、"auth"和"login"是相关概念，因此搜索其中一个会找到其他的。

示例：查询"如何验证用户身份？"会同时找到"用户身份验证需要有效的 API token"和"基于 token 的 auth 验证请求"，尽管措辞不同。它不会找到"身份验证测试失败了"，因为尽管包含这个词，但含义不同。

这适用于用户使用的术语与文档不同的文档搜索。缺点是可能错过精确的技术术语，有时你需要字面匹配而不是语义匹配。在索引期间需要调用嵌入 API。

### 关键词搜索（BM25）

通过词频和稀有度进行匹配和排名的统计算法：

```yaml
strategies:
  - type: bm25
    database: ./bm25.db
    k1: 1.5
    b: 0.75
    chunking:
      size: 1000
      overlap: 100
```

在索引期间，文档被分词，算法计算每个术语的出现频率（词频）以及它在所有文档中的稀有程度（逆文档频率）。评分索引存储在本地 SQLite 数据库中。

当你搜索"HandleRequest function"时，算法会找到包含这些精确术语的片段，并根据词频、术语稀有度和文档长度对它们进行评分。找到"HandleRequest"比找到常见词如"function"更重要。可以把它看作是有统计排名的 grep。

示例：搜索"HandleRequest function"会找到 `func HandleRequest(w http.ResponseWriter, r *http.Request)` 和"HandleRequest function 处理传入请求"，但不会找到"处理 HTTP 请求"，尽管语义上相似。

`k1` 参数（默认 1.5）控制重复术语的重要性——较高的值更加强调重复。`b` 参数（默认 0.75）控制长度归一化——较高的值更惩罚较长的文档。

这种方法速度快、本地运行（无 API 成本）、对于查找函数名、类名、API 端点和任何逐字出现的标识符是可预测的。权衡是对含义零理解——"RetryHandler"和"retry logic"尽管相关但不会匹配。是语义搜索的重要补充。

### LLM 增强的语义搜索（semantic-embeddings）

在嵌入之前使用 LLM 生成语义摘要，支持按代码功能而不是名称搜索：

```yaml
strategies:
  - type: semantic-embeddings
    embedding_model: openai/text-embedding-3-small
    chat_model: openai/gpt-5-mini
    vector_dimensions: 1536
    database: ./code.db
    ast_context: true
    chunking:
      size: 1000
      code_aware: true
```

在索引期间，代码使用 AST 结构分割（函数保持完整），然后 `chat_model` 为每个片段生成语义摘要。嵌入的是摘要，而不是原始代码。当你搜索时，你的查询匹配这些摘要，但返回的是原始代码。

这解决了常规嵌入的一个问题：原始代码嵌入被变量名和实现细节主导。一个名为 `processData` 的函数实现了重试逻辑，不会在语义上匹配"retry"。但是当 LLM 首先对其进行摘要时，摘要明确提到"retry logic"，使其变得可搜索。

示例：考虑这段代码：

```go
func (c *Client) Do(req *Request) (*Response, error) {
    for i := 0; i < 3; i++ {
        resp, err := c.attempt(req)
        if err == nil { return resp, nil }
        time.Sleep(time.Duration(1<<i) * time.Second)
    }
    return nil, errors.New("max retries exceeded")
}
```

LLM 摘要是："为 HTTP 请求实现指数退避重试逻辑，在失败前尝试最多 3 次，延迟为 1s、2s、4s。"

现在搜索"retry logic exponential backoff"会找到这段代码，尽管代码从未使用这些词。`ast_context: true` 选项在提示中包含 AST 元数据以便更好理解。`code_aware: true` 分割防止在实现中途分割函数。

这种方法在命名不一致的大型代码库中按行为查找代码方面表现出色。权衡是索引速度显著变慢（每个片段一次 LLM 调用）和更高的 API 成本（聊天和嵌入模型都需要）。对于文档良好的代码或简单项目来说，通常有些过度。

## 使用混合检索组合策略

每种策略都有优缺点。组合它们可以同时捕获语义理解和精确术语匹配：

```yaml
rag:
  knowledge:
    docs: [./documentation, ./src]
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
        strategy: rrf
        k: 60
      deduplicate: true
      limit: 5
```

### 融合如何工作

两种策略并行运行，各自返回其顶级候选（此例中为 20 和 15）。融合使用基于排名的评分组合结果，移除重复项，并返回前 5 个最终结果。你的智能体获得的结果既适用于语义查询（"如何..."），也适用于精确术语搜索（"查找 `configure_auth` 函数"）。

### 融合策略

推荐使用 RRF（Reciprocal Rank Fusion）。它基于排名而非绝对分数组合结果，这在策略使用不同评分标准时效果可靠。无需调优。

对于加权融合，你可以给某个策略更高的重要性：

```yaml
fusion:
  strategy: weighted
  weights:
    chunked-embeddings: 0.7
    bm25: 0.3
```

这需要为你的内容进行调优。当你知道某种方法对你的使用场景更有效时使用它。

最高分融合取各策略中的最高分：

```yaml
fusion:
  strategy: max
```

这仅在策略使用可比的评分标准时才有效。简单但不如 RRF 复杂。

## 提高检索质量

### 重排序结果

初始检索优化了速度。重排序使用更复杂的模型重新评分结果以获得更好的相关性：

```yaml
results:
  reranking:
    model: openai/gpt-5-mini
    threshold: 0.3
    criteria: |
      评分相关性时，优先考虑：
      - 官方文档优于社区内容
      - 最新信息优于过时材料
      - 实际示例优于理论解释
      - 代码实现优于设计讨论
  limit: 5
```

`criteria` 字段非常强大——用它来编码关于什么结果对你的特定使用场景相关的领域知识。你的标准越具体，重排序效果越好。

权衡：显著更好的结果，但增加了延迟和 API 成本（每个结果评分都需要 LLM 调用）。

### 分块配置

你分割文档的方式极大地影响检索质量。根据你的内容类型定制分块。分块大小以字符（Unicode 码点）而非 token 为单位。

对于文档和散文，使用中等大小有重叠的分块：

```yaml
chunking:
  size: 1000
  overlap: 100
  respect_word_boundaries: true
```

重叠保留分块边界的上下文。尊重词边界防止单词被截断。

对于代码，使用更大的基于 AST 分割的分块：

```yaml
chunking:
  size: 2000
  code_aware: true
```

这保持函数完整。`code_aware` 设置使用 tree-sitter 尊重代码结构。

> [!NOTE] <!-- TODO: update this when we add support for more languages. -->
> 目前仅支持 Go；计划支持更多语言。

对于简短、专注的内容如 API 参考：

```yaml
chunking:
  size: 500
  overlap: 50
```

简短部分需要较少重叠，因为它们天然是自包含的。

试验这些值。如果检索遗漏上下文，增加分块大小或重叠。如果结果太宽泛，减少分块大小。

## 关于 RAG 的决策

### 何时使用 RAG

在以下情况使用 RAG：

- 你的内容太大，无法放入上下文窗口
- 你需要定向检索，而不是一次性获取所有内容
- 内容会更改并需要保持最新
- 智能体需要搜索多个文件

在以下情况不要使用 RAG：

- 内容足够小，可以包含在智能体指令中
- 信息很少更改（考虑使用提示工程代替）
- 你需要实时数据（RAG 使用预索引的快照）
- 内容已经是智能体可以直接查询的可搜索格式

### 选择检索策略

对面向用户的文档、术语多样的内容以及用户提问方式与文档不同的概念搜索，使用语义搜索（chunked-embeddings）。

对代码标识符、函数名、API 端点、错误消息以及精确术语匹配重要的任何内容，使用关键词搜索（BM25）。对于技术术语和专有名词必不可少。

对按功能搜索代码、通过行为而不是名称查找实现，或需要深入理解的复杂技术内容，使用 LLM 增强的语义（semantic-embeddings）。当准确性比索引速度更重要时选择此方法。

对混合内容的通用搜索、不确定哪种方法效果最好，或质量最重要的生产系统，使用混合（多种策略）。以复杂性为代价获得最大覆盖范围。

### 为你的项目调优

从默认设置开始，然后根据结果调整。

如果检索遗漏了相关内容：

- 增加策略中的 `limit` 以检索更多候选
- 调整 `threshold` 使其不那么严格
- 增加分块 `size` 以捕获更多上下文
- 添加更多检索策略

如果检索返回不相关内容：

- 减少 `limit` 以获得更少候选
- 增加 `threshold` 使其更严格
- 添加带有特定标准的重排序
- 减少分块 `size` 以获得更专注的结果

如果索引太慢：

- 增加 `batch_size` 以减少 API 调用
- 增加 `max_embedding_concurrency` 以实现并行
- 考虑使用 BM25 代替嵌入（本地，无 API）
- 使用更小的嵌入模型

如果结果缺乏上下文：

- 增加分块 `overlap`
- 增加分块 `size`
- 使用 `return_full_content: true` 返回整个文档
- 将相邻分块添加到结果中

## 延伸阅读

- [配置参考](reference/config.md#rag) - 完整的 RAG 选项和参数
- [RAG 示例](https://github.com/docker/cagent/tree/main/examples/rag) - 不同场景的工作配置
- [工具参考](reference/toolsets.md) - RAG 搜索工具如何在智能体工作流中工作