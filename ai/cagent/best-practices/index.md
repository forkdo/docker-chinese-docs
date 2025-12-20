# 最佳实践

这些模式源自构建和运行 cagent 代理的经验。它们并非功能或配置选项，而是在实践中行之有效的方法。

## 处理大型命令输出

产生大量输出的 Shell 命令可能会超出代理的上下文窗口。验证工具、测试套件和构建日志通常会生成数千行内容。如果直接捕获此输出，它会消耗所有可用上下文，导致代理失败。

解决方案：将输出重定向到文件，然后读取该文件。Read 工具会自动将大文件截断为 2000 行，如果需要，代理可以浏览该文件。

**不要这样做：**

```yaml
reviewer:
  instruction: |
    运行验证：`docker buildx bake validate`
    检查输出是否有错误。
  toolsets:
    - type: shell
```

验证输出直接进入上下文。如果输出量很大，代理会因上下文溢出错误而失败。

**应该这样做：**

```yaml
reviewer:
  instruction: |
    运行验证并保存输出：
    `docker buildx bake validate > validation.log 2>&1`

    读取 validation.log 以检查错误。
    文件可能很大 - 读取前 2000 行。
    错误通常出现在开头。
  toolsets:
    - type: filesystem
    - type: shell
```

输出被发送到文件，而不是上下文。代理使用 filesystem 工具集读取所需内容。

## 构建代理团队

单个代理处理多个职责会使指令复杂化且行为不可预测。将工作拆分给专门的代理会产生更好的结果。

协调器模式效果很好：一个根代理理解整体任务并委派给专家。每个专家专注于一件事。

**示例：文档编写团队**

```yaml
agents:
  root:
    description: 技术写作协调器
    instruction: |
      协调文档工作：
      1. 委派给 writer 进行内容创作
      2. 委派给 editor 进行格式润色
      3. 委派给 reviewer 进行验证
      4. 如果 reviewer 发现问题，则循环返回 editor
    sub_agents: [writer, editor, reviewer]
    toolsets: [filesystem, todo]

  writer:
    description: 创建和编辑文档内容
    instruction: |
      编写清晰、实用的文档。
      专注于内容质量 - editor 处理格式。
    toolsets: [filesystem, think]

  editor:
    description: 润色格式和风格
    instruction: |
      修复格式问题，换行，运行 prettier。
      去除 AI 痕迹并润色风格。
      不要改变含义或添加内容。
    toolsets: [filesystem, shell]

  reviewer:
    description: 运行验证工具
    instruction: |
      运行验证套件，报告失败。
    toolsets: [filesystem, shell]
```

每个代理都有明确的职责。writer 不必担心换行。editor 不生成内容。reviewer 只运行工具。

**何时使用团队：**

- 工作流中有多个不同的步骤
- 需要不同的技能（写作 ↔ 编辑 ↔ 测试）
- 某个步骤可能需要根据后续反馈重试

**何时使用单个代理：**

- 简单、专注的任务
- 所有工作都在一个步骤中完成
- 增加协调开销没有帮助

## 优化 RAG 性能

当文件很多时，RAG 索引需要时间。索引整个代码库的配置可能需要几分钟才能启动。针对代理实际需要的内容进行优化。

**缩小范围：**

不要索引所有内容。索引与代理工作相关的内容。

```yaml
# 范围太广 - 索引整个代码库
rag:
  codebase:
    docs: [./]

# 更好 - 仅索引相关目录
rag:
  codebase:
    docs: [./src/api, ./docs, ./examples]
```

如果代理只处理 API 代码，就不要索引测试、供应商目录或生成的文件。

**增加批处理和并发性：**

每个 API 调用处理更多块，并发出并行请求。

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    batch_size: 50 # 每个 API 调用处理更多块
    max_embedding_concurrency: 10 # 并行请求
    chunking:
      size: 2000 # 更大的块 = 更少的总块数
      overlap: 150
```

这减少了 API 调用次数和索引时间。

**考虑使用 BM25 进行快速本地搜索：**

如果需要精确的术语匹配（函数名、错误消息、标识符），BM25 速度快且在本地运行，无需 API 调用。

```yaml
strategies:
  - type: bm25
    database: ./bm25.db
    chunking:
      size: 1500
```

当需要语义理解和精确匹配时，结合嵌入使用混合检索。

## 保留文档范围

在构建更新文档的代理时，一个常见问题是：代理将最小化的指南转变为教程。它会向所有内容添加先决条件、故障排除、最佳实践、示例和详细解释。

这些添加可能单独来看是好的，但它们改变了文档的特性。一个专注的 90 行操作指南变成了 200 行的参考文档。

**将其构建到指令中：**

```yaml
writer:
  instruction: |
    更新文档时：

    1. 了解当前文档的范围和长度
    2. 匹配其特性 - 不要将最小化的指南转变为教程
    3. 仅添加真正缺失的内容
    4. 珍惜简洁 - 并非每个主题都需要全面覆盖

    好的补充填补空白。坏的补充改变文档的特性。
    如有疑问，宁少勿多。
```

明确告诉代理保留现有文档的范围。没有此指导，它们默认会变得全面。

## 模型选择

根据代理的角色和复杂性选择模型。

**使用更大的模型（Sonnet, GPT-5）用于：**

- 复杂的推理和规划
- 写作和编辑内容
- 协调多个代理
- 需要判断力和创造力的任务

**使用更小的模型（Haiku, GPT-5 Mini）用于：**

- 运行验证工具
- 简单的结构化任务
- 读取日志和报告错误
- 高容量、低复杂性的工作

来自文档编写团队的示例：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5 # 复杂协调
  writer:
    model: anthropic/claude-sonnet-4-5 # 创造性内容工作
  editor:
    model: anthropic/claude-sonnet-4-5 # 风格判断
  reviewer:
    model: anthropic/claude-haiku-4-5 # 仅运行验证
```

reviewer 使用 Haiku，因为它运行命令并检查错误。不需要复杂的推理，而且 Haiku 更快、更便宜。

## 下一步

- 查阅[配置参考](./reference/config.md) 了解所有可用选项
- 查看[工具集参考](./reference/toolsets.md) 了解代理可以使用哪些工具
- 参见[示例配置](https://github.com/docker/cagent/tree/main/examples) 获取完整的工作代理
- 阅读[RAG 指南](./rag.md) 了解详细的检索优化
