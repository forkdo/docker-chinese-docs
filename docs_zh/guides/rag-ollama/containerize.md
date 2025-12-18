---
title: 容器化 RAG 应用
linkTitle: 容器化你的应用
weight: 10
keywords: python, 生成式 AI, genai, llm, ollama, containerize, initialize, qdrant
description: 了解如何容器化 RAG 应用。
aliases:
  - /guides/use-case/rag-ollama/containerize/
---

## 概述

本节将指导你如何使用 Docker 容器化 RAG 应用。

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

## 获取示例应用

本指南使用的示例应用是一个 RAG 应用的示例，由三个主要组件构成，这些组件是每个 RAG 应用的构建块。一个托管在某处的大语言模型，在本例中它托管在容器中并通过 [Ollama](https://ollama.ai/) 提供服务。一个向量数据库 [Qdrant](https://qdrant.tech/)，用于存储本地数据的嵌入，以及一个使用 [Streamlit](https://streamlit.io/) 的 Web 应用，为用户提供最佳用户体验。

克隆示例应用。打开终端，切换到你想工作的目录，运行以下命令克隆仓库：

```console
$ git clone https://github.com/mfranzon/winy.git
```

你现在应该在 `winy` 目录中有以下文件。

```text
├── winy/
│ ├── .gitignore
│ ├── app/
│ │ ├── main.py
│ │ ├── Dockerfile
| | └── requirements.txt
│ ├── tools/
│ │ ├── create_db.py
│ │ ├── create_embeddings.py
│ │ ├── requirements.txt
│ │ ├── test.py
| | └── download_model.sh
│ ├── docker-compose.yaml
│ ├── wine_database.db
│ ├── LICENSE
│ └── README.md
```

## 容器化你的应用：基础

容器化应用涉及将应用及其依赖项打包到容器中，以确保在不同环境中的一致性。以下是容器化像 Winy 这样的应用所需的内容：

1. Dockerfile：包含如何为你的应用构建 Docker 镜像的指令。它指定了基础镜像、依赖项、配置文件和运行应用的命令。

2. Docker Compose 文件：Docker Compose 是一个用于定义和运行多容器 Docker 应用的工具。Compose 文件允许你在单个文件中配置应用的服务、网络和卷。

## 运行应用

在 `winy` 目录中，终端中运行以下命令。

```console
$ docker compose up --build
```

Docker 构建并运行你的应用。根据你的网络连接，下载所有依赖项可能需要几分钟。当应用运行时，你会在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

打开浏览器，在 [http://localhost:8501](http://localhost:8501) 查看应用。你应该看到一个简单的 Streamlit 应用。

该应用需要 Qdrant 数据库服务和 LLM 服务才能正常工作。如果你有在 Docker 外部运行的服务，可以在 `docker-compose.yaml` 中指定连接信息。

```yaml
winy:
  build:
    context: ./app
    dockerfile: Dockerfile
  environment:
    - QDRANT_CLIENT=http://qdrant:6333 # 指定 qdrant 数据库的 url
    - OLLAMA=http://ollama:11434 # 指定 ollama 服务的 url
  container_name: winy
  ports:
    - "8501:8501"
  depends_on:
    - qdrant
    - ollama
```

如果你没有运行这些服务，继续阅读本指南，了解如何使用 Docker 运行部分或全部这些服务。
请记住，`ollama` 服务是空的；它没有任何模型。因此，你需要在开始使用 RAG 应用之前拉取一个模型。所有说明都在下一页。

在终端中，按 `ctrl`+`c` 停止应用。

## 总结

在本节中，你学会了如何使用 Docker 容器化并运行你的 RAG 应用。

## 下一步

在下一节中，你将学习如何使用 Docker 完全在本地配置应用，使用你首选的 LLM 模型。