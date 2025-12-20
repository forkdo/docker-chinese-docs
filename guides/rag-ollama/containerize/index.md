# 容器化 RAG 应用程序

## 概述

本节将引导您使用 Docker 容器化 RAG 应用程序。

> [!NOTE]
> 您可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中查看更多容器化的 GenAI 应用程序示例。

## 获取示例应用程序

本指南使用的示例应用程序是一个 RAG 应用程序示例，由三个主要组件构成，这些组件是每个 RAG 应用程序的构建块。一个托管在某处的大型语言模型，在本例中，它托管在容器中并通过 [Ollama](https://ollama.ai/) 提供服务。一个向量数据库 [Qdrant](https://qdrant.tech/)，用于存储本地数据的嵌入；以及一个使用 [Streamlit](https://streamlit.io/) 的 Web 应用程序，为用户提供最佳的用户体验。

克隆示例应用程序。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/mfranzon/winy.git
```

现在您的 `winy` 目录中应该有以下文件。

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

## 容器化您的应用程序：基础知识

容器化应用程序涉及将其及其依赖项打包到一个容器中，以确保在不同环境中的一致性。以下是容器化像 Winy 这样的应用程序所需的内容：

1.  **Dockerfile**：一个包含如何为您的应用程序构建 Docker 镜像的指令的 Dockerfile。它指定了基础镜像、依赖项、配置文件以及运行应用程序的命令。

2.  **Docker Compose 文件**：Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。Compose 文件允许您在单个文件中配置应用程序的服务、网络和卷。

## 运行应用程序

在 `winy` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

Docker 将构建并运行您的应用程序。根据您的网络连接，下载所有依赖项可能需要几分钟时间。当应用程序运行时，您将在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

打开浏览器，在 [http://localhost:8501](http://localhost:8501) 查看应用程序。您应该会看到一个简单的 Streamlit 应用程序。

该应用程序需要一个 Qdrant 数据库服务和一个 LLM 服务才能正常工作。如果您可以访问在 Docker 外部运行的服务，请在 `docker-compose.yaml` 中指定连接信息。

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

如果您没有运行这些服务，请继续本指南，了解如何使用 Docker 运行部分或全部这些服务。
请记住，`ollama` 服务是空的；它没有任何模型。因此，在开始使用 RAG 应用程序之前，您需要拉取一个模型。所有说明都在下一页中。

在终端中，按 `ctrl`+`c` 停止应用程序。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行您的 RAG 应用程序。

## 下一步

在下一节中，您将学习如何使用您首选的 LLM 模型（完全在本地）通过 Docker 正确配置应用程序。
