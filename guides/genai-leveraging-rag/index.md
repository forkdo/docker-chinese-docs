# 在 GenAI 中利用 RAG 教会模型新知识


## 简介

检索增强生成（RAG）是一个强大的框架，它通过从外部知识源检索信息来增强大语言模型（LLM）。本指南聚焦于一种使用 Neo4j 等图数据库的专门化 RAG 实现，这类数据库擅长管理高度互联的关系型数据。与使用向量数据库的传统 RAG 方案不同，将 RAG 与图数据库结合能提供更好的上下文感知能力和基于关系驱动的洞察。

在本指南中，你将：

* 探索把图数据库集成到 RAG 框架中的优势。
* 使用 Docker 配置一套包含 Neo4j 和 AI 模型的 GenAI 技术栈。
* 分析一个真实案例，展示该方法在处理专业领域查询时的有效性。

## 理解 RAG

RAG 是一个混合式框架，它通过集成信息检索来增强大语言模型的能力。它由三个核心组件构成：

- 从外部知识库进行**信息检索**
- 用于生成回答的**大语言模型（LLM）**
- 支持语义搜索的**向量嵌入**

在 RAG 系统中，向量嵌入以机器可以理解和处理的方式表示文本的语义含义。例如，"dog" 和 "puppy" 这两个词会具有相似的嵌入，因为它们含义相近。通过将这些嵌入整合进 RAG 框架，系统就能把大语言模型的生成能力与从外部来源拉取高度相关、具备上下文感知的数据的能力结合起来。

系统的运作方式如下：
1. 问题被转换为能捕捉其含义的数学模式
2. 这些模式用于在数据库中查找匹配的信息
3. LLM 生成的回答融合了模型自身的知识与这些额外信息。

要高效地存放这些向量信息，你需要一种特殊类型的数据库。

## 图数据库简介

图数据库（例如 Neo4j）专为管理高度互联的数据而设计。与传统关系型数据库不同，图数据库同时重视实体本身及实体之间的关系，因此非常适合那些关系与数据本身同等重要的任务。

图数据库因其独特的数据存储与查询方式而与众不同。它们用节点（或称顶点）表示实体，用边表示这些实体之间的关系。这种结构能够高效处理高度互联的数据和复杂查询，而这些在传统数据库系统中很难应对。

SQL 数据库与图数据库在数据模型上有显著差异。SQL 数据库采用由行和列组成的表格结构，实体之间的关系通过外键建立。这种方式适合结构化数据和预先定义好的关系。相比之下，图数据库将数据表示为节点（实体）和边（关系），使关系的表达更加直观和灵活。这种结构对于复杂、相互关联的数据尤其有利。

另一个关键差异在于 schema 的灵活性。SQL 数据库基于严格的 schema 运行，这意味着对数据结构的任何变更（例如新增列或修改关系）通常都需要谨慎规划和迁移流程。而图数据库是 schema 可选的，具备更高的灵活性。新的节点、边或属性可以在不影响现有数据的情况下引入，从而更快地适应需求变化。

## 实践落地：检验 RAG 的效果

为了在实践中展示 RAG 系统的强大之处，我们来看一个以 Apache NiFi 为主题的真实实现案例。该案例研究展示了 RAG 如何提升 AI 就专业技术主题提供准确、贴合上下文信息的能力。

### 教会 AI 认识新技术

Apache NiFi 很好地体现了传统 LLM 的局限，以及 RAG 如何克服这些局限。作为一项相对较新的技术，许多 LLM 对它的了解有限或已过时，因此它非常适合用来展示 RAG 的能力。

在不使用 RAG 的情况下，当被问及超出其知识截止日期的信息时，LLM 可能给出泛泛的回答，或者直接承认自己知识有限。下面的例子说明了这一点。
```text
Question: What important events happened in 2024?
RAG: Disabled
I'm happy to help! Unfortunately, I'm a large language model, I don't have access to real-time information or events that occurred after my training data cutoff in 2024. Therefore, I cannot provide you with any important events that happened in 2024. My apologize for any inconvenience this may cause. Is there anything else I can help you with?
```

## 在 Linux 上搭建带 GPU 加速的 GenAI 技术栈

要在 Linux 主机上搭建并运行该 GenAI 技术栈，请执行下列命令之一，分别对应 GPU 或 CPU 驱动：

### GPU 驱动

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux-gpu up -d
mv env.example .env
nano .env
```
在 `.env` 文件中，确保以下几行未被注释。请设置你自己的凭据以确保安全

  ```txt
    NEO4J_URI=neo4j://database:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=password
    OLLAMA_BASE_URL=http://llm-gpu:11434
  ```

### CPU 驱动

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux up -d
mv env.example .env
nano .env
```
在 `.env` 文件中，确保以下几行未被注释。请设置你自己的凭据以确保安全

  ```txt
    NEO4J_URI=neo4j://database:7687
    NEO4J_USERNAME=neo4j
    NEO4J_PASSWORD=password
    OLLAMA_BASE_URL=http://llm:11434
  ```

### 在其他平台上搭建

有关如何在其他平台上搭建该技术栈的说明，请参阅[此页面](https://github.com/docker/genai-stack)。

### 首次启动

首次启动可能需要一些时间，因为系统需要下载一个大语言模型。

### 监控进度

你可以通过查看日志来监控下载和初始化进度。运行以下命令查看日志：

```bash
docker compose logs
```

等待日志中出现特定的行，表明下载已完成且技术栈已就绪。这些行通常确认了安装与初始化成功。

  ```text
    pull-model-1 exited with code 0
    database-1    | 2024-12-29 09:35:53.269+0000 INFO  Started.
    pdf_bot-1     |   You can now view your Streamlit app in your browser.
    loader-1      |   You can now view your Streamlit app in your browser.
    bot-1         |   You can now view your Streamlit app in your browser.
  ```

现在你可以访问 [http://localhost:8501/](http://localhost:8501/) 的界面来提问。例如，你可以试试示例问题：

当日志中出现上述那些行时，这些 Web 应用就可以使用了。

由于目标是教会 AI 它尚不知道的内容，我们先在 [http://localhost:8501/](http://localhost:8501/) 上问它一个关于 NiFi 的简单问题。
![alt text](images/genai-leveraging-rag-1.png)

```text
Question: What is Apache Nifi?
RAG: Disabled
Hello! I'm here to help you with your question about Apache NiFi. Unfortunately, I don't know the answer to that question. I'm just an AI and my knowledge cutoff is December 2022, so I may not be familiar with the latest technologies or software. Can you please provide more context or details about Apache NiFi? Maybe there's something I can help you with related to it.
```

如上所示，AI 对这个主题一无所知，因为它在模型训练时（即所谓的信息截止点）尚不存在。

现在该教 AI 一些新本领了。首先，连接到 [http://localhost:8502/](http://localhost:8502/)。不要使用 "neo4j" 标签，把它改为 "apache-nifi" 标签，然后点击 **Import** 按钮。

![alt text](images/genai-leveraging-rag-2.png)

导入成功后，你可以访问 Neo4j 来验证数据。

使用 `.env` 文件中的凭据登录 [http://localhost:7474/](http://localhost:7474/) 后，你就可以在 Neo4j 上执行查询。使用 Neo4j 的 Cypher 查询语言，你可以检查数据库中存储的数据。

要统计数据数量，运行以下查询：

```text
MATCH (n)
RETURN DISTINCT labels(n) AS NodeTypes, count(*) AS Count
ORDER BY Count DESC;
```

要执行该查询，请在顶部的输入框中输入内容，然后点击蓝色的运行按钮。

![alt text](images/genai-leveraging-rag-3.png)

结果会显示在下方。所展示的信息是从 Stack Overflow 下载并保存到图数据库中的。RAG 将利用这些信息来增强其回答。

你还可以运行以下查询来可视化数据：

```text
CALL db.schema.visualization()
```

要查看数据库中的关系，运行以下查询：

```text
CALL db.relationshipTypes()
```

现在你可以让 LLM 使用这些信息了。回到 [http://localhost:8501/](http://localhost:8501/)，勾选 **RAG** 复选框，然后再次提出同样的问题。LLM 将给出更详尽的答案。

![alt text](images/genai-leveraging-rag-4.png)

系统通过从最新技术文档中提取内容，提供了全面、准确的信息。
```text
Question: What is Apache Nifi?
RAG: Enabled

Answer:
Apache NiFi is an open-source, distributed data processing system that allows you to collect, transform, and transport data across various sources and sinks. It provides a graphical user interface for designing and managing data flows, as well as a set of APIs for integrating with other systems.
According to this Stack Overflow question, the free Neo4J JDBC driver doesn't understand SQL, only Cypher, so you would need to use a non-free BI Connector to connect to Neo4j from Apache Drill.
Additionally, this Stack Overflow question suggests that Apache POI does work in a Neo4j User Defined Function. However, there may be an unknown glitch in the standalone UDF mentioned in the initial question.
To export data from Neo4j to Excel using APOC Extended procedures, you can use apoc.export.xls.query which takes a Cypher query and exports the results to an Excel file.

References:
How to connect and query Neo4j Database on Apache Drill?
Is a Neo4j UDF compatible with Apache POI?
```

请注意，Stack Overflow 上会不断有新问题加入，而且由于大多数 AI 模型本身具有随机性，得到的答案可能有所不同，不会与本例完全一致。

你可以随意换一个 [Stack Overflow 标签](https://stackoverflow.com/tags)重新开始。要清空 Neo4j 中的所有数据，可以在 Neo4j Web UI 中使用以下命令：

```txt
MATCH (n)
DETACH DELETE n;
```

为获得最佳效果，请选择一个 LLM 不熟悉的标签。

### 何时利用 RAG 以获得最佳效果

检索增强生成（RAG）在标准大语言模型（LLM）表现不足的场景中尤为有效。RAG 擅长的三个关键领域是：知识局限、业务需求和成本效率。以下各节将更详细地探讨这些方面。

#### 克服知识局限

LLM 是在截至某个时间点的固定数据集上训练的。这意味着它们无法获取：

* 实时信息：LLM 不会持续更新其知识，因此可能不了解近期事件、新发布的研究或新兴技术。
* 专业知识：许多小众主题、专有框架或行业特定最佳实践在模型的训练语料中可能没有充分记录。
* 准确的上下文理解：LLM 在处理金融、网络安全或医学研究等动态领域中频繁变化的细微差别或不断演进的术语时可能会遇到困难。

通过将 RAG 与 Neo4j 这样的图数据库结合，AI 模型可以在生成回答之前访问并检索最新、相关且高度关联的数据。这确保了答案是最新的，并且基于事实信息而非推断出的近似结果。

#### 满足业务与合规需求

医疗、法律服务和金融分析等行业的机构要求其 AI 驱动的解决方案具备：

* 准确性：企业需要 AI 生成的内容真实可靠且与其特定领域相关。
* 合规性：许多行业必须遵守关于数据使用与安全的严格法规。
* 可追溯性：企业往往要求 AI 的回答可审计，这意味着需要引用来源材料。

使用 RAG，AI 生成的答案可以来自可信数据库，从而确保更高的准确性并符合行业标准。这可以降低诸如错误信息传播或违规等风险。

#### 提升成本效率与性能

训练和微调大型 AI 模型在计算上开销高昂且耗时。而集成 RAG 可以带来：

* 降低微调需求：无需在每次出现新数据时都重新训练 AI 模型，RAG 让模型能够动态获取并纳入更新后的信息。
* 小模型也能有更好表现：借助恰当的检索技术，即使是较小的 AI 模型也能通过高效利用外部知识而表现出色。
* 更低的运营成本：企业无需投入昂贵的基础设施来支撑大规模再训练，而可以利用 RAG 的实时检索能力优化资源。

按照本指南操作后，你现在已具备使用 Neo4j 实现 RAG 的基础知识，能够让你的 AI 系统提供更准确、更相关、更有洞察力的回答。下一步就是动手实验——选择一个数据集，配置你的技术栈，开始借助检索增强生成的力量增强你的 AI。

