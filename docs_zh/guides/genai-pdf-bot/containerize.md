---
title: 容器化生成式 AI 应用
linkTitle: 容器化你的应用
weight: 10
keywords: python, 生成式 ai, genai, llm, neo4j, ollama, 容器化, 初始化, langchain, openai
description: 了解如何容器化生成式 AI (GenAI) 应用。
aliases:
  - /guides/use-case/genai-pdf-bot/containerize/
---

## 前置条件

> [!NOTE]
>
> 生成式 AI 应用通常能从 GPU 加速中受益。目前，Docker Desktop 仅在使用 WSL2 后端的 [Windows](/manuals/desktop/features/gpu.md#using-nvidia-gpus-with-wsl2) 上支持 GPU 加速。Linux 用户也可以通过原生安装 [Docker Engine](/manuals/engine/install/_index.md) 来使用 GPU 加速。

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)，或者如果你是 Linux 用户并计划使用 GPU 加速，则已安装 [Docker Engine](/manuals/engine/install/_index.md)。Docker 定期添加新功能，本指南中的某些部分可能仅与最新版本的 Docker Desktop 兼容。
- 你已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概述

本节将指导你如何使用 Docker Desktop 容器化生成式 AI (GenAI) 应用。

> [!NOTE]
>
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

## 获取示例应用

本指南使用的示例应用是 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中 PDF Reader 应用的修改版本。该应用是一个全栈 Python 应用，允许你对 PDF 文件提出问题。

该应用使用 [LangChain](https://www.langchain.com/) 进行编排，[Streamlit](https://streamlit.io/) 用于 UI，[Ollama](https://ollama.ai/) 运行 LLM，[Neo4j](https://neo4j.com/) 存储向量。

克隆示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/craig-osterhout/docker-genai-sample
```

现在你的 `docker-genai-sample` 目录中应该有以下文件。

```text
├── docker-genai-sample/
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── LICENSE
│ └── README.md
```

## 初始化 Docker 资产

现在你有了应用，可以使用 `docker init` 创建必要的 Docker 资产来容器化你的应用。在 `docker-genai-sample` 目录中，运行 `docker init` 命令。`docker init` 提供一些默认配置，但你需要回答一些关于你应用的问题。例如，此应用使用 Streamlit 运行。参考以下 `docker init` 示例，并对你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.11.4
? What port do you want your app to listen on? 8000
? What is the command to run your app? streamlit run app.py --server.address=0.0.0.0 --server.port=8000
```

现在你的 `docker-genai-sample` 目录中应该有以下内容。

```text
├── docker-genai-sample/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── compose.yaml
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── Dockerfile
│ ├── LICENSE
│ ├── README.Docker.md
│ └── README.md
```

要了解 `docker init` 添加的文件的更多信息，请参阅以下内容：

- [Dockerfile](../../../reference/dockerfile.md)
- [.dockerignore](../../../reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用

在 `docker-genai-sample` 目录中，终端中运行以下命令。

```console
$ docker compose up --build
```

Docker 构建并运行你的应用。根据你的网络连接，下载所有依赖项可能需要几分钟。当应用运行时，你会在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8000
server-1  |
```

打开浏览器，访问 [http://localhost:8000](http://localhost:8000) 查看应用。你应该能看到一个简单的 Streamlit 应用。应用可能需要几分钟下载嵌入模型。下载过程中，右上角会显示 **Running**。

该应用需要 Neo4j 数据库服务和 LLM 服务才能运行。如果你有在 Docker 外运行的服务，指定连接信息并尝试使用。如果你没有运行这些服务，继续阅读本指南，了解如何使用 Docker 本地运行部分或全部这些服务。

在终端中按 `ctrl`+`c` 停止应用。

## 总结

在本节中，你学会了如何使用 Docker 容器化并运行你的 GenAI 应用。

相关信息：

- [docker init CLI 参考](../../../reference/cli/docker/init.md)

## 下一步

在下一节中，你将学习如何使用 Docker 在本地运行你的应用、数据库和 LLM 服务。