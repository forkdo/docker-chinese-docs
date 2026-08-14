# GenAI 视频转写与对话


## 概述

本指南介绍一个视频转写与分析项目，它使用了一组与
[GenAI Stack](https://www.docker.com/blog/introducing-a-new-genai-stack/) 相关的技术。

该项目展示了以下技术：

- [Docker and Docker Compose](#docker-and-docker-compose)
- [OpenAI](#openai-api)
- [Whisper](#whisper)
- [Embeddings](#embeddings)
- [Chat completions](#chat-completions)
- [Pinecone](#pinecone)
- [Retrieval-Augmented Generation](#retrieval-augmented-generation)

> **致谢**
>
> 本指南是社区贡献。Docker 在此感谢
> [David Cardozo](https://www.davidcardozo.com/) 对本指南的贡献。

## 前提条件

- 你拥有 [OpenAI API 密钥](https://platform.openai.com/api-keys)。

  > [!NOTE]
  >
  > OpenAI 是第三方托管服务，可能会产生[费用](https://openai.com/pricing)。

- 你拥有 [Pinecone API 密钥](https://app.pinecone.io/)。
- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期加入新
  功能，本指南的部分内容可能只在最新版 Docker Desktop 上可用。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git
  客户端，但你可以使用任意客户端。

## 关于这个应用

该应用是一个聊天机器人，能够回答关于某个视频的问题。此外，它还会提供视频中的时间戳，
帮助你找到用于回答问题的信息来源。

## 获取并运行应用

1. 克隆示例应用的仓库。在终端中运行以下命令。

   ```console
   $ git clone https://github.com/Davidnet/docker-genai.git
   ```

   该项目包含以下目录和文件：

   ```text
   ├── docker-genai/
   │ ├── docker-bot/
   │ ├── yt-whisper/
   │ ├── .env.example
   │ ├── .gitignore
   │ ├── LICENSE
   │ ├── README.md
   │ └── docker-compose.yaml
   ```

2. 指定你的 API 密钥。在 `docker-genai` 目录中创建一个名为 `.env` 的文本文件，并在其中
   指定你的 API 密钥。下面是 `.env.example` 文件的内容，可作为参考示例。

   ```text
   #-------------------------------------------------------------------------
   # OpenAI
   #-------------------------------------------------------------------------
   OPENAI_TOKEN=your-api-key # Replace your-api-key with your personal API key

   #-------------------------------------------------------------------------
   # Pinecone
   #-------------------------------------------------------------------------
   PINECONE_TOKEN=your-api-key # Replace your-api-key with your personal API key
   ```

3. 构建并运行应用。在终端中切换到 `docker-genai` 目录，然后运行以下命令。

   ```console
   $ docker compose up --build
   ```

   Docker Compose 会根据 `docker-compose.yaml` 文件中定义的服务来构建并运行应用。应用
   运行起来后，你会在终端中看到 2 个服务的日志。

   在日志中，你会看到这些服务分别暴露在端口 `8503` 和 `8504` 上。这两个服务相互补充。

   `yt-whisper` 服务运行在端口 `8503` 上。该服务把你想归档到知识库中的视频写入 Pinecone
   数据库。下一节将介绍这个服务。

## 使用 yt-whisper 服务

yt-whisper 服务是一个 YouTube 视频处理服务，它使用 OpenAI Whisper 模型生成视频转写文本，
并将其存储到 Pinecone 数据库中。以下步骤展示如何使用该服务。

1. 打开浏览器，访问 [http://localhost:8503](http://localhost:8503) 上的 yt-whisper 服务。
2. 应用界面出现后，在 **Youtube URL** 字段中指定一个 YouTube 视频 URL，然后选择
   **Submit**。下面的示例使用
   [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![在 yt-whisper 服务中提交视频](images/genai-video-bot-yt-whisper.webp)

   yt-whisper 服务会下载视频的音频，使用 Whisper 把它转写为 WebVTT（`*.vtt`）格式
   （你可以下载该文件），然后使用 text-embedding-3-small 模型创建嵌入向量，最后把这些
   嵌入向量上传到 Pinecone 数据库。

   处理完视频后，Web 应用中会出现一个视频列表，告知你哪些视频已在 Pinecone 中建立索引。
   它还提供一个按钮用于下载转写文本。

   ![yt-whisper 服务中已处理的视频](images/genai-video-bot-yt-whisper-2.webp)

   现在你可以访问端口 `8504` 上的 dockerbot 服务，就这些视频提问了。

## 使用 dockerbot 服务

dockerbot 服务是一个问答服务，它同时利用 Pinecone 数据库和 AI 模型来提供回答。以下步骤
展示如何使用该服务。

> [!NOTE]
>
> 在使用 dockerbot 服务之前，你必须先通过
> [yt-whisper 服务](#using-the-yt-whisper-service)处理至少一个视频。

1. 打开浏览器，访问 [http://localhost:8504](http://localhost:8504) 上的服务。

2. 在 **What do you want to know about your videos?** 文本框中，向 Dockerbot 提出一个关于
   yt-whisper 服务已处理视频的问题。下面的示例提问：“What is a sugar cookie?”。该问题的
   答案存在于上一个示例处理过的视频中，即
   [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![向 Dockerbot 提问](images/genai-video-bot-bot.webp)

   在这个示例中，Dockerbot 回答了问题，并提供了带时间戳的视频链接，其中可能包含关于答案
   的更多信息。

   dockerbot 服务会接收问题，使用 text-embedding-3-small 模型把它转换为嵌入向量，查询
   Pinecone 数据库以找出相似的嵌入向量，然后把该上下文传给 gpt-4-turbo-preview 来生成答案。

3. 选择第一个链接，看看它提供了什么信息。基于上面的示例，选择
   [https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s](https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s)。

   在这个示例链接中，你可以看到该视频片段完美回答了“What is a sugar cookie?”这个问题。

## 了解应用架构

下图展示了应用的高层服务架构，其中包括：

- yt-whisper：由 Docker Compose 运行的本地服务，与远程 OpenAI 和 Pinecone 服务交互。
- dockerbot：由 Docker Compose 运行的本地服务，与远程 OpenAI 和 Pinecone 服务交互。
- OpenAI：远程第三方服务。
- Pinecone：远程第三方服务。

![应用架构图](images/genai-video-bot-architecture.webp)

## 了解所用技术及其作用

### Docker and Docker Compose（Docker 与 Docker Compose）

该应用使用 Docker 在容器中运行应用，为其提供一致且隔离的运行环境。这意味着无论底层系统
有何差异，应用都能在其 Docker 容器中按预期运行。要进一步了解 Docker，参阅
[入门概览](/get-started/introduction/_index.md)。

Docker Compose 是用于定义和运行多容器应用的工具。Compose 让你能用一条命令
`docker compose up` 轻松运行这个应用。更多细节参阅
[Compose 概览](/manuals/compose/_index.md)。

### OpenAI API

OpenAI API 提供 LLM 服务，以其前沿的 AI 与机器学习技术而闻名。在这个应用中，OpenAI 的
技术被用于从音频生成转写文本（使用 Whisper 模型）、为文本数据创建嵌入向量，以及生成对
用户查询的回答（使用 GPT 和 chat completions）。更多细节参阅
[openai.com](https://openai.com/product)。

### Whisper

Whisper 是 OpenAI 开发的自动语音识别系统，用于把口语转写为文本。在这个应用中，Whisper
被用于把 YouTube 视频的音频转写为文本，从而可以对视频内容做进一步处理和分析。更多细节
参阅 [Introducing Whisper](https://openai.com/research/whisper)。

### Embeddings（嵌入向量）

嵌入向量是文本或其他数据类型的数值表示，它以机器学习算法可处理的方式捕捉其含义。在这个
应用中，嵌入向量被用于把视频转写文本转换为向量格式，从而可以查询并分析它与用户输入的
相关性，便于应用中的高效检索和回答生成。更多细节参阅 OpenAI 的
[Embeddings](https://platform.openai.com/docs/guides/embeddings) 文档。

![嵌入向量示意图](images/genai-video-bot-embeddings.webp)

### Chat completions（对话补全）

本应用通过 OpenAI 的 API 使用的 chat completion，指的是基于给定上下文或提示生成对话式
回答。在这个应用中，它通过处理并整合来自视频转写文本及其他输入的信息，为用户查询提供
智能、感知上下文的答案，从而增强聊天机器人的交互能力。更多细节参阅 OpenAI 的
[Chat Completions API](https://platform.openai.com/docs/guides/text-generation) 文档。

### Pinecone

Pinecone 是一个针对相似度检索优化的向量数据库服务，用于构建和部署大规模向量检索应用。
在这个应用中，Pinecone 被用于存储和检索视频转写文本的嵌入向量，从而基于用户查询在应用
内实现高效、相关的检索功能。更多细节参阅
[pincone.io](https://www.pinecone.io/)。

### Retrieval-Augmented Generation（检索增强生成）

检索增强生成（RAG）是一种把信息检索与语言模型结合起来、基于检索到的文档或数据生成回答的
技术。在 RAG 中，系统先检索相关信息（本例中通过视频转写文本的嵌入向量），然后使用语言
模型基于检索到的数据生成回答。更多细节参阅 OpenAI 的 cookbook
[Retrieval Augmented Generative Question Answering with Pinecone](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa)。

## 下一步

探索如何使用生成式 AI [创建一个 PDF 机器人应用](/guides/genai-pdf-bot/_index.md)，或在
[GenAI Stack](https://github.com/docker/genai-stack) 仓库中查看更多 GenAI 示例。

