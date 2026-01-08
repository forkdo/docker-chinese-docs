---
title: GenAI 视频转录与对话
linkTitle: 视频转录与对话
description: 探索一个使用 Docker、OpenAI 和 Pinecone 的生成式人工智能视频分析应用。
keywords: python, generative ai, genai, llm, whisper, pinecone, openai, whisper
summary: '了解如何使用 Docker 构建并部署一个生成式人工智能视频分析与转录机器人。

  '
tags:
- ai
aliases:
- /guides/use-case/genai-video-bot/
params:
  time: 20 分钟
---

## 概述

本指南介绍了一个基于 [GenAI Stack](https://www.docker.com/blog/introducing-a-new-genai-stack/) 相关技术的视频转录与分析项目。

该项目展示了以下技术：

- [Docker 和 Docker Compose](#docker-and-docker-compose)
- [OpenAI](#openai-api)
- [Whisper](#whisper)
- [Embeddings](#embeddings)
- [Chat completions](#chat-completions)
- [Pinecone](#pinecone)
- [Retrieval-Augmented Generation](#retrieval-augmented-generation)

> **致谢**
>
> 本指南为社区贡献。Docker 感谢 [David Cardozo](https://www.davidcardozo.com/) 对本指南的贡献。

## 前置条件

- 您已拥有 [OpenAI API Key](https://platform.openai.com/api-keys)。

  > [!NOTE]
  >
  > OpenAI 是第三方托管服务，[可能产生费用](https://openai.com/pricing)。

- 您已拥有 [Pinecone API Key](https://app.pinecone.io/)。
- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南中的部分内容可能仅在最新版本的 Docker Desktop 中可用。
- 您已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但您可以使用任意客户端。

## 关于应用

该应用是一个聊天机器人，可以回答来自视频的问题，并提供视频的时间戳，帮助您找到回答问题所使用的来源。

## 获取并运行应用

1. 克隆示例应用的仓库。在终端中运行以下命令：

   ```console
   $ git clone https://github.com/Davidnet/docker-genai.git
   ```

   项目包含以下目录和文件：

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

2. 指定您的 API 密钥。在 `docker-genai` 目录中，创建一个名为 `.env` 的文本文件，并在其中指定您的 API 密钥。以下为 `.env.example` 文件的内容，可作为示例参考：

   ```text
   #----------------------------------------------------------------------------
   # OpenAI
   #----------------------------------------------------------------------------
   OPENAI_TOKEN=your-api-key # 将 your-api-key 替换为您的个人 API 密钥

   #----------------------------------------------------------------------------
   # Pinecone
   #----------------------------------------------------------------------------
   PINECONE_TOKEN=your-api-key # 将 your-api-key 替换为您的个人 API 密钥
   ```

3. 构建并运行应用。在终端中，切换到 `docker-genai` 目录，运行以下命令：

   ```console
   $ docker compose up --build
   ```

   Docker Compose 根据 `docker-compose.yaml` 文件中定义的服务构建并运行应用。应用运行时，您将在终端中看到两个服务的日志。

   在日志中，您会看到服务在端口 `8503` 和 `8504` 上暴露。这两个服务相互补充。

   `yt-whisper` 服务运行在端口 `8503` 上。该服务将您想要归档到知识库中的视频提供给 Pinecone 数据库。下一节将探讨此服务。

## 使用 yt-whisper 服务

yt-whisper 服务是一个 YouTube 视频处理服务，使用 OpenAI Whisper 模型生成视频转录，并将其存储在 Pinecone 数据库中。以下步骤展示如何使用该服务。

1. 打开浏览器，访问 [http://localhost:8503](http://localhost:8503) 上的 yt-whisper 服务。
2. 应用出现后，在 **Youtube URL** 字段中指定一个 YouTube 视频 URL，然后选择 **Submit**。以下示例使用 [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![在 yt-whisper 服务中提交视频](images/yt-whisper.webp)

   yt-whisper 服务下载视频的音频，使用 Whisper 将其转录为 WebVTT（`*.vtt`）格式（可下载），然后使用 text-embedding-3-small 模型创建嵌入，最后将这些嵌入上传到 Pinecone 数据库。

   处理视频后，网页应用中会出现一个视频列表，告知您哪些视频已索引到 Pinecone 中。它还提供了一个下载转录的按钮。

   ![yt-whisper 服务中已处理的视频](images/yt-whisper-2.webp)

   现在，您可以访问端口 `8504` 上的 dockerbot 服务，并询问有关视频的问题。

## 使用 dockerbot 服务

dockerbot 服务是一个问答服务，利用 Pinecone 数据库和 AI 模型提供响应。以下步骤展示如何使用该服务。

> [!NOTE]
>
> 在使用 dockerbot 服务之前，必须先通过 [yt-whisper 服务](#using-the-yt-whisper-service) 处理至少一个视频。

1. 打开浏览器，访问 [http://localhost:8504](http://localhost:8504) 上的服务。

2. 在 **What do you want to know about your videos?** 文本框中，向 Dockerbot 询问关于通过 yt-whisper 服务处理的视频的问题。以下示例询问“什么是糖饼干？”。该问题的答案存在于上一示例中处理的视频中，即 [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU)。

   ![向 Dockerbot 询问问题](images/bot.webp)

   在此示例中，Dockerbot 回答问题，并提供带有时间戳的视频链接，这些链接可能包含有关答案的更多信息。

   dockerbot 服务将问题转换为嵌入（使用 text-embedding-3-small 模型），查询 Pinecone 数据库以找到相似的嵌入，然后将该上下文传递给 gpt-4-turbo-preview 以生成答案。

3. 选择第一个链接，查看其提供的信息。基于上一示例，选择 [https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s](https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s)。

   在示例链接中，您可以看到该视频片段完美地回答了“什么是糖饼干？”这一问题。

## 探索应用架构

下图展示了应用的高级服务架构，包括：

- yt-whisper：一个本地服务，由 Docker Compose 运行，与远程 OpenAI 和 Pinecone 服务交互。
- dockerbot：一个本地服务，由 Docker Compose 运行，与远程 OpenAI 和 Pinecone 服务交互。
- OpenAI：一个远程第三方服务。
- Pinecone：一个远程第三方服务。

![应用架构图](images/architecture.webp)

## 探索使用的技术及其作用

### Docker 和 Docker Compose

应用使用 Docker 在容器中运行，提供一致且隔离的环境。这意味着无论底层系统差异如何，应用都将在其 Docker 容器内按预期运行。要了解更多关于 Docker 的信息，请参阅 [入门概述](/get-started/introduction/_index.md)。

Docker Compose 是定义和运行多容器应用的工具。Compose 使您能够通过单个命令 `docker compose up` 运行此应用。更多详情，请参阅 [Compose 概述](/manuals/compose/_index.md)。

### OpenAI API

OpenAI API 提供了一个以尖端 AI 和机器学习技术著称的 LLM 服务。在本应用中，OpenAI 的技术用于从音频生成转录（使用 Whisper 模型）、为文本数据创建嵌入，以及生成用户查询的响应（使用 GPT 和 chat completions）。更多详情，请参阅 [openai.com](https://openai.com/product)。

### Whisper

Whisper 是 OpenAI 开发的自动语音识别系统，旨在将口语转换为文本。在本应用中，Whisper 用于将 YouTube 视频的音频转录为文本，从而实现对视频内容的进一步处理和分析。更多详情，请参阅 [Introducing Whisper](https://openai.com/research/whisper)。

### Embeddings

嵌入是文本或其他数据类型的数值表示，以机器学习算法可处理的方式捕获其含义。在本应用中，嵌入用于将视频转录转换为可查询和分析的向量格式，从而基于用户输入实现高效的相关性搜索和响应生成。更多详情，请参阅 OpenAI 的 [Embeddings](https://platform.openai.com/docs/guides/embeddings) 文档。

![嵌入图](images/embeddings.webp)

### Chat completions

聊天完成（chat completion）通过 OpenAI API 在本应用中使用，指的是基于给定上下文或提示生成对话式响应。在应用中，它通过处理和整合视频转录和其他输入的信息，为用户查询提供智能、上下文感知的答案，增强聊天机器人的交互能力。更多详情，请参阅 OpenAI 的 [Chat Completions API](https://platform.openai.com/docs/guides/text-generation) 文档。

### Pinecone

Pinecone 是一个优化用于相似性搜索的向量数据库服务，用于构建和部署大规模向量搜索应用。在本应用中，Pinecone 用于存储和检索视频转录的嵌入，从而基于用户查询实现高效且相关的搜索功能。更多详情，请参阅 [pincone.io](https://www.pinecone.io/)。

### Retrieval-Augmented Generation

检索增强生成（Retrieval-Augmented Generation，RAG）是一种结合信息检索和语言模型的技术，基于检索到的文档或数据生成响应。在 RAG 中，系统检索相关信息（在本例中通过视频转录的嵌入），然后使用语言模型基于检索到的数据生成响应。更多详情，请参阅 OpenAI 食谱中的 [Retrieval Augmented Generative Question Answering with Pinecone](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa)。

## 后续步骤

探索如何使用生成式人工智能 [创建 PDF 机器人应用](/guides/genai-pdf-bot/_index.md)，或在 [GenAI Stack](https://github.com/docker/genai-stack) 仓库中查看更多 GenAI 示例。