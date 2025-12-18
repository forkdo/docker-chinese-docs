---
title: RAG
description: RAG 如何让您的 cagent 代理访问代码库和文档
keywords: [cagent, rag, 检索, embeddings, 语义搜索]
weight: 70
---

当您在 cagent 中配置 RAG 源时，您的代理会自动获得一个针对该知识库的搜索工具。代理决定何时搜索，只检索相关信息，并利用这些信息回答问题或完成任务——无需您手动管理提示内容。

本指南解释了 cagent 的 RAG 系统如何工作、何时使用以及如何为您的内容有效配置。

> [!NOTE]
> RAG 是一个高级功能，需要配置和调优。默认设置适合入门，但根据您的特定内容和用例调整配置会显著提升效果。

## 问题：上下文过多

您的代理可以处理整个代码库，但无法将所有内容放入其上下文窗口。即使有 200K 的 token 限制，中等规模项目也太大。在数百个文件中查找相关代码会浪费上下文。

文件系统工具帮助代理读取文件，但代理必须猜测要读取哪些文件。它只能按文件名搜索，无法按含义搜索。询问“找到重试逻辑”时，代理会读取文件，希望能偶然发现正确代码。

grep 可以找到精确的文本匹配，但会错过相关概念。搜索“authentication”不会找到使用“auth”或“login”的代码。您要么得到数百个匹配项，要么一个都没有，而且 grep 不理解代码结构——它只是匹配任何地方出现的字符串。

RAG 会预先索引您的内容并启用语义搜索。代理按含义而非精确单词搜索预索引内容。它只检索尊重代码结构的相关块。上下文不会浪费在探索上。

## cagent 中的 RAG 工作原理

在 cagent 配置中配置 RAG 源：

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

当您引用 `rag: [codebase]` 时，cagent 会：

1. **启动时** - 索引您的文档（仅首次运行，阻塞直到完成）
2. **对话期间** - 为代理提供搜索工具
3. **代理搜索时** - 检索相关块并添加到上下文
4. **文件更改时** - 自动重新索引修改的文件

代理根据对话决定何时搜索。您不需要管理上下文内容——代理会处理。

### 索引过程

首次运行时，cagent 会：

- 从配置路径读取文件
- 遵循 `.gitignore` 模式（可禁用）
- 将文档拆分为块
- 使用您选择的策略创建可搜索表示
- 将所有内容存储在本地数据库中

后续运行会重用索引。如果文件更改，cagent 会检测到这一点并仅重新索引更改的内容，无需手动干预即可保持知识库最新。

## 检索策略

不同的内容需要不同的检索方法。cagent 支持三种策略，每种都针对不同用例优化。默认设置效果良好，但了解权衡有助于您选择正确的方法。

### 语义搜索（chunked-embeddings）

将文本转换为表示含义的向量，实现按概念而非精确单词搜索：

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

索引期间，文档被拆分为块，每个块由嵌入模型转换为 1536 维向量。这些向量本质上是高维空间中的坐标，相似概念位于相近位置。

当您搜索“如何验证用户？”时，查询会变成向量，数据库使用余弦相似度（测量向量间角度）找到具有相近向量的块。嵌入模型学到“authentication”、“auth”和“login”是相关概念，因此搜索一个会找到其他。

示例：查询“如何验证用户？”会找到“用户验证需要有效 API token”和“基于 token 的验证会验证请求”，尽管措辞不同。它不会找到“验证测试失败”，因为含义不同，尽管包含该词。

这适用于用户使用与文档不同术语提问的文档。缺点是可能错过精确技术术语，有时您需要字面匹配而非语义匹配。索引期间需要嵌入 API 调用。

### 关键字搜索（BM25）

统计算法，通过词频和稀有度匹配和排序：

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

索引期间，文档被标记化，算法计算每个术语出现频率（词频）及其在所有文档中的稀有度（逆文档频率）。评分索引存储在本地 SQLite 数据库中。

当您搜索“HandleRequest 函数”时，算法找到包含这些精确术语的块，并根据词频、术语稀有度和文档长度评分。找到“HandleRequest”比找到“function”等常见词得分更高。可将其视为带统计排序的 grep。

示例：搜索“HandleRequest 函数”会找到 `func HandleRequest(w http.ResponseWriter, r *http.Request)` 和“The HandleRequest function processes incoming requests”，但不会找到“process HTTP requests”，尽管语义相似。

`k1` 参数（默认 1.5）控制重复术语的重要性——较高值更强调重复。`b` 参数（默认 0.75）控制长度归一化——较高值更惩罚较长文档。

这速度快、本地化（无 API 成本）且可预测，适合查找函数名、类名、API 端点和任何以原样出现的标识符。权衡是零理解含义——“RetryHandler”和“retry logic”不会匹配，尽管相关。是语义搜索的重要补充。

### LLM 增强语义搜索（semantic-embeddings）

使用 LLM 在嵌入前生成语义摘要，实现按代码功能而非名称搜索：

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

索引期间，代码使用 AST 结构拆分（函数保持完整），然后 `chat_model` 为每个块生成语义摘要。摘要被嵌入，而非原始代码。搜索时，查询与这些摘要匹配，但返回原始代码。

这解决了常规嵌入的问题：原始代码嵌入被变量名和实现细节主导。名为 `processData` 且实现重试逻辑的函数不会在语义上匹配“retry”。但 LLM 先摘要后，摘要明确提到“retry logic”，使其可被找到。

示例：考虑此代码：

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

LLM 摘要为：“实现 HTTP 请求的指数退避重试逻辑，最多尝试 3 次，延迟 1s、2s、4s 后失败。”

现在搜索“retry logic exponential backoff”会找到此代码，尽管代码从未使用这些词。`ast_context: true` 选项在提示中包含 AST 元数据以更好理解。`code_aware: true` 块拆分防止在函数中间拆分。

此方法擅长在命名不一致的大型代码库中按行为查找代码。权衡是索引显著变慢（每个块一次 LLM 调用）和更高 API 成本（聊天和嵌入模型）。对于文档完善的代码或简单项目通常过度。

## 使用混合检索组合策略

每种策略都有优缺点。组合它们可以捕获语义理解和精确术语匹配：

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

### 融合工作原理

两种策略并行运行，每种返回其顶级候选项（本例为 20 和 15）。融合使用基于排名的评分组合结果，删除重复项，返回前 5 个最终结果。您的代理获得适用于语义查询（“如何...”）和精确术语搜索（“查找 `configure_auth` 函数”）的结果。

### 融合策略

推荐 RRF（互逆排名融合）。它基于排名而非绝对分数组合结果，当策略使用不同评分尺度时效果可靠。无需调优。

对于加权融合，您给一种策略更多重要性：

```yaml
fusion:
  strategy: weighted
  weights:
    chunked-embeddings: 0.7
    bm25: 0.3
```

这需要针对您的内容调优。当您知道一种方法对您的用例效果更好时使用。<!-- TODO: add a link to the docs on when to use weighted fusion. -->

最大分数融合取各策略的最高分数：

```yaml
fusion:
  strategy: max
```

这只在策略使用可比评分尺度时有效。简单但不如 RRF 复杂。

## 提升检索质量

### 重新排序结果

初始检索优化速度。重新排序使用更复杂的模型重新评分结果以获得更好相关性：

```yaml
results:
  reranking:
    model: openai/gpt-5-mini
    threshold: 0.3
    criteria: |
      When scoring relevance, prioritize:
      - Official documentation over community content
      - Recent information over outdated material
      - Practical examples over theoretical explanations
      - Code implementations over design discussions
  limit: 5
```

`criteria` 字段功能强大——用于编码关于什么使结果与您的特定用例相关的领域知识。标准越具体，重新排序效果越好。

权衡：结果显著改善，但增加延迟和 API 成本（对每个结果评分的 LLM 调用）。

### 块拆分配置

如何拆分文档会显著影响检索质量。根据您的内容类型调整块拆分。块大小以字符（Unicode 代码点）而非 token 测量。

对于文档和散文，使用中等块和重叠：

```yaml
chunking:
  size: 1000
  overlap: 100
  respect_word_boundaries: true
```

重叠保留块边界的上下文。尊重词边界防止切分单词。

对于代码，使用更大的块和基于 AST 的拆分：

```yaml
chunking:
  size: 2000
  code_aware: true
```

这保持函数完整。`code_aware` 设置使用 tree-sitter 尊重代码结构。

> [!NOTE] <!-- TODO: update this when we add support for more languages. -->
> 目前仅支持 Go；计划支持更多语言。

对于 API 参考等简短、集中的内容：

```yaml
chunking:
  size: 500
  overlap: 50
```

简短部分需要较少重叠，因为它们自然自包含。

试验这些值。如果检索错过上下文，增加块大小或重叠。如果结果太宽泛，减小块大小。

## 关于 RAG 的决策

### 何时使用 RAG

在以下情况下使用 RAG：

- 您的内容太大，无法放入上下文窗口
- 您需要有针对性的检索，而非一次性全部
- 内容会变化且需要保持最新
- 代理需要跨多个文件搜索

在以下情况下不使用 RAG：

- 内容足够小，可包含在代理指令中
- 信息很少更改（考虑提示工程）
- 您需要实时数据（RAG 使用预索引快照）
- 内容已在代理可直接查询的可搜索格式中

### 选择检索策略

对面向用户的文档、术语多样的内容和用户以与文档不同方式表述问题的概念搜索使用语义搜索（chunked-embeddings）。

对代码标识符、函数名、API 端点、错误消息和任何需要精确术语匹配的内容使用关键字搜索（BM25）。对技术术语和专有名词至关重要。

对按功能的代码搜索、按行为而非名称查找实现或需要深度理解的复杂技术内容使用 LLM 增强语义（semantic-embeddings）。当准确性比索引速度更重要时选择此方法。

对跨混合内容的通用搜索、不确定哪种方法效果最好或质量至关重要的生产系统使用混合（多种策略）。以复杂性为代价获得最大覆盖范围。

### 针对您的项目调优

从默认值开始，然后根据结果调整。

如果检索错过相关内容：

- 增加策略中的 `limit` 以检索更多候选项
- 调整 `threshold` 使其更宽松
- 增加块 `size` 以捕获更多上下文
- 添加更多检索策略

如果检索返回不相关内容：

- 减少 `limit` 以减少候选项
- 增加 `threshold` 使其更严格
- 添加带特定标准的重新排序
- 减小块 `size` 以获得更集中的结果

如果索引太慢：

- 增加 `batch_size` 以减少 API 调用
- 增加 `max_embedding_concurrency` 以获得并行性
- 考虑用 BM25 代替嵌入（本地，无 API）
- 使用更小的嵌入模型

如果结果缺乏上下文：

- 增加块 `overlap`
- 增加块 `size`
- 使用 `return_full_content: true` 返回整个文档
- 向结果添加相邻块

## 延伸阅读

- [配置参考](reference/config.md#rag) - 完整的 RAG 选项和参数
- [RAG 示例](https://github.com/docker/cagent/tree/main/examples/rag) - 不同场景的工作配置
- [工具参考](reference/toolsets.md) - RAG 搜索工具在代理工作流中的工作原理