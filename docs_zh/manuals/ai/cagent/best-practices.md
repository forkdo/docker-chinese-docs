---
title: 最佳实践
description: 构建高效 cagent 代理的模式和技巧
keywords: [cagent, 最佳实践, 模式, 代理设计, 优化]
weight: 40
---

从构建和运行 cagent 代理中总结出的经验模式。这些不是功能或配置选项——而是实践中行之有效的方法。

## 处理大型命令输出

产生大量输出的 Shell 命令可能会超出代理的上下文窗口。验证工具、测试套件和构建日志通常会生成数千行输出。如果直接捕获这些输出，会消耗所有可用上下文，导致代理失败。

**解决方案：** 将输出重定向到文件，然后读取文件。Read 工具会自动将大文件截断为 2000 行，代理可以根据需要导航文件。

**不要这样做：**

```yaml
reviewer:
  instruction: |
    运行验证：`docker buildx bake validate`
    检查输出中的错误。
  toolsets:
    - type: shell
```

验证输出直接进入上下文。如果输出很大，代理会因上下文溢出错误而失败。

**应该这样做：**

```yaml
reviewer:
  instruction: |
    运行验证并保存输出：
    `docker buildx bake validate > validation.log 2>&1`

    读取 validation.log 检查错误。
    文件可能很大 - 读取前 2000 行。
    错误通常出现在开头。
  toolsets:
    - type: filesystem
    - type: shell
```

输出进入文件，而不是上下文。代理使用文件系统工具集读取所需内容。

## 构建代理团队

单个代理处理多个职责会使指令复杂化，行为变得不可预测。将工作分配给专业代理能产生更好的结果。

协调器模式效果很好：根代理理解整体任务并委托给专家。每个专家专注于一件事。

**示例：文档编写团队**

```yaml
agents:
  root:
    description: 技术写作协调员
    instruction: |
      协调文档工作：
      1. 委托给 writer 进行内容创建
      2. 委托给 editor 进行格式润色
      3. 委托给 reviewer 进行验证
      4. 如果 reviewer 发现问题，循环回到 editor
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
      修复格式问题，包装行，运行 prettier。
      删除 AI 式表达并润色风格。
      不要改变含义或添加内容。
    toolsets: [filesystem, shell]

  reviewer:
    description: 运行验证工具
    instruction: |
      运行验证套件，报告失败。
    toolsets: [filesystem, shell]
```

每个代理都有明确的职责。writer 不担心行包装。editor 不生成内容。reviewer 只运行工具。

**何时使用团队：**

- 工作流程中有多个不同步骤
- 需要不同技能（写作 ↔ 编辑 ↔ 测试）
- 某个步骤可能需要根据后续反馈重试

**何时使用单个代理：**

- 简单、专注的任务
- 所有工作在一个步骤中完成
- 添加协调开销没有帮助

## 优化 RAG 性能

当有大量文件时，RAG 索引需要时间。索引整个代码库的配置可能需要几分钟才能启动。针对代理实际需要的内容进行优化。

**缩小范围：**

不要索引所有内容。只索引与代理工作相关的部分。

```yaml
# 范围太大 - 索引整个代码库
rag:
  codebase:
    docs: [./]

# 更好 - 只索引相关目录
rag:
  codebase:
    docs: [./src/api, ./docs, ./examples]
```

如果代理只处理 API 代码，就不要索引测试、vendor 目录或生成的文件。

**增加批处理和并发：**

每个 API 调用处理更多块，并行请求。

```yaml
strategies:
  - type: chunked-embeddings
    embedding_model: openai/text-embedding-3-small
    batch_size: 50 # 每个 API 调用更多块
    max_embedding_concurrency: 10 # 并行请求
    chunking:
      size: 2000 # 更大块 = 更少总块数
      overlap: 150
```

这减少了 API 调用和索引时间。

**考虑使用 BM25 进行快速本地搜索：**

如果需要精确术语匹配（函数名、错误消息、标识符），BM25 快速且在本地运行，无需 API 调用。

```yaml
strategies:
  - type: bm25
    database: ./bm25.db
    chunking:
      size: 1500
```

当你需要语义理解和精确匹配时，结合使用嵌入和混合检索。

## 保持文档范围

构建更新文档的代理时，一个常见问题：代理将简明指南转换为教程。它添加先决条件、故障排除、最佳实践、示例和详细解释到所有内容。

这些添加可能单独看是好的，但它们改变了文档的特性。一个集中的 90 行教程变成了 200 行参考。

**在指令中构建这一点：**

```yaml
writer:
  instruction: |
    更新文档时：

    1. 理解当前文档的范围和长度
    2. 匹配其特性 - 不要将简明指南转换为教程
    3. 只添加真正缺失的内容
    4. 重视简洁 - 并非每个主题都需要全面覆盖

    好的添加填补空白。坏的添加改变文档特性。
    有疑问时，少添加而不是多添加。
```

明确告诉代理保持现有文档的范围。没有这个指导，它们默认会变得全面。

## 模型选择

根据代理的角色和复杂性选择模型。

**使用大型模型（Sonnet、GPT-5）处理：**

- 复杂推理和规划
- 编写和编辑内容
- 协调多个代理
- 需要判断力和创造力的任务

**使用小型模型（Haiku、GPT-5 Mini）处理：**

- 运行验证工具
- 简单的结构化任务
- 读取日志和报告错误
- 高量、低复杂度工作

文档编写团队示例：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5 # 复杂协调
  writer:
    model: anthropic/claude-sonnet-4-5 # 创意内容工作
  editor:
    model: anthropic/claude-sonnet-4-5 # 风格判断
  reviewer:
    model: anthropic/claude-haiku-4-5 # 只运行验证
```

reviewer 使用 Haiku，因为它运行命令并检查错误。不需要复杂推理，Haiku 更快更便宜。

## 接下来

- 查看 [配置参考](./reference/config.md) 了解所有可用选项
- 检查 [工具集参考](./reference/toolsets.md) 了解代理可以使用的工具
- 查看 [示例配置](https://github.com/docker/cagent/tree/main/examples) 了解完整的可工作代理
- 阅读 [RAG 指南](./rag.md) 了解详细的检索优化