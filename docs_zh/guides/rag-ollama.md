---
description: 使用 Ollama 和 Docker 容器化 RAG 应用
keywords: python, generative ai, genai, llm, ollama, rag, qdrant
title: 使用 Ollama 和 Docker 构建 RAG 应用
linkTitle: RAG Ollama 应用
summary: |
  本指南演示如何使用 Docker 部署基于 Ollama 的检索增强生成（RAG）模型。
aliases:
  - /guides/use-case/rag-ollama/
  - /guides/rag-ollama/containerize/
  - /guides/rag-ollama/develop/
params:
  tags: [ai]
  time: 20 minutes
---


这份检索增强生成（RAG）指南将教你如何使用 Docker 容器化一个现有的 RAG 应用。示例应用是
一个像侍酒师一样工作的 RAG，能为你推荐葡萄酒与食物的最佳搭配。在本指南中，你将学会：

- 容器化并运行 RAG 应用
- 搭建本地环境，在本地运行完整的 RAG 技术栈以便开发

首先从容器化一个现有的 RAG 应用开始。

## Containerize a RAG application（容器化 RAG 应用）

### 概述

本节将带你使用 Docker 完成 RAG 应用的容器化。

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化
> GenAI 应用的示例。

### 获取示例应用

本指南使用的示例应用是一个 RAG 应用示例，由三个主要组件构成，它们是每个 RAG 应用的基本
构件。一个托管在某处的大语言模型，本例中它托管在容器里并通过 [Ollama](https://ollama.ai/)
提供服务。一个向量数据库 [Qdrant](https://qdrant.tech/)，用于存储本地数据的嵌入向量。
以及一个使用 [Streamlit](https://streamlit.io/) 构建的 Web 应用，为用户提供最佳体验。

克隆示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/mfranzon/winy.git
```

现在你的 `winy` 目录中应该有以下文件。

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

### 容器化应用：要点

容器化应用意味着把应用及其依赖一起打包进容器，从而确保在不同环境中的一致性。要容器化
像 Winy 这样的应用，你需要：

1. Dockerfile：Dockerfile 包含了如何为你的应用构建 Docker 镜像的指令。它指定基础镜像、
   依赖、配置文件以及运行应用的命令。

2. Docker Compose 文件：Docker Compose 是用于定义和运行多容器 Docker 应用的工具。
   Compose 文件让你可以在单个文件中配置应用的服务、网络和卷。

### 运行应用

在 `winy` 目录中，于终端运行以下命令。

```console
$ docker compose up --build
```

Docker 会构建并运行你的应用。取决于你的网络连接，下载所有依赖可能需要几分钟。应用运行
起来后，你会在终端中看到类似下面的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

打开浏览器访问 [http://localhost:8501](http://localhost:8501) 查看应用。你应该会看到一个
简单的 Streamlit 应用。

该应用需要 Qdrant 数据库服务和一个 LLM 服务才能正常工作。如果你能访问在 Docker 之外运行
的这些服务，请在 `docker-compose.yaml` 中指定连接信息。

```yaml
winy:
  build:
    context: ./app
    dockerfile: Dockerfile
  environment:
    - QDRANT_CLIENT=http://qdrant:6333 # Specifies the url for the qdrant database
    - OLLAMA=http://ollama:11434 # Specifies the url for the ollama service
  container_name: winy
  ports:
    - "8501:8501"
  depends_on:
    - qdrant
    - ollama
```

如果你没有正在运行的这些服务，请继续阅读本指南，了解如何用 Docker 运行其中部分或全部
服务。请记住，`ollama` 服务是空的；它没有任何模型。因此，在开始使用 RAG 应用之前，你需要
先拉取一个模型。所有说明都在下一页中。

在终端中按 `ctrl`+`c` 停止应用。

### 小结

在本节中，你学会了如何使用 Docker 容器化并运行 RAG 应用。

### 下一步

在下一节中，你将学习如何完全在本地使用 Docker，为应用正确配置你偏好的 LLM 模型。

## 使用容器进行 RAG 开发

### 前提条件

完成 [Containerize a RAG application](#containerize-a-rag-application)。

### 概述

在本节中，你将学习如何搭建开发环境，以访问生成式 RAG 应用所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化
> GenAI 应用的示例。

### 添加本地数据库

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将了解 `docker-compose.yaml` 文件
中的数据库服务。

要运行该数据库服务：

1. 在克隆下来的仓库目录中，用 IDE 或文本编辑器打开 `docker-compose.yaml` 文件。

2. 在 `docker-compose.yaml` 文件中，你会看到以下内容：

   ```yaml
   services:
     qdrant:
       image: qdrant/qdrant
       container_name: qdrant
       ports:
         - "6333:6333"
       volumes:
         - qdrant_data:/qdrant/storage
   ```

   > [!NOTE]
   > 要进一步了解 Qdrant，参阅 [Qdrant 官方 Docker 镜像](https://hub.docker.com/r/qdrant/qdrant)。

3. 启动应用。在 `winy` 目录中，于终端运行以下命令。

   ```console
   $ docker compose up --build
   ```

4. 访问应用。打开浏览器访问 [http://localhost:8501](http://localhost:8501) 查看应用。
   你应该会看到一个简单的 Streamlit 应用。

5. 停止应用。在终端中按 `ctrl`+`c` 停止应用。

### 添加本地或远程 LLM 服务

示例应用支持 [Ollama](https://ollama.ai/)。本指南提供以下场景的说明：

- 在容器中运行 Ollama
- 在容器之外运行 Ollama

虽然所有平台都可以使用上述任一场景，但性能和 GPU 支持可能有所不同。你可以参考以下准则
来选择合适的方案：

- 如果你使用 Linux 并原生安装了 Docker Engine，或使用 Windows 10/11 并安装了 Docker
  Desktop，同时拥有支持 CUDA 的 GPU，且系统至少有 8 GB 内存，那么可以在容器中运行 Ollama。
- 如果在 Linux 机器上运行 Docker Desktop，则在容器之外运行 Ollama。

为你的 LLM 服务选择以下方案之一。

{{< tabs >}}
{{< tab name="Run Ollama in a container" >}}

在容器中运行 Ollama 时，你应该拥有支持 CUDA 的 GPU。虽然没有受支持的 GPU 也能在容器中
运行 Ollama，但性能可能无法接受。只有 Linux 和 Windows 11 支持容器访问 GPU。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装前置组件。
   - 对于 Linux 上的 Docker Engine，安装 [NVIDIA Container Toolkilt](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，安装最新的 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)，
     并确保你使用的是 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)。
2. `docker-compose.yaml` 文件中已包含必要的配置。在你自己的应用中，你需要在
   `docker-compose.yaml` 中添加 Ollama 服务。以下是更新后的 `docker-compose.yaml`：

   ```yaml
   ollama:
     image: ollama/ollama
     container_name: ollama
     ports:
       - "8000:8000"
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: 1
               capabilities: [gpu]
   ```

   > [!NOTE]
   > 有关这些 Compose 配置的更多细节，参阅[使用 Docker Compose 开启 GPU 访问](/manuals/compose/how-tos/gpu-support.md)。

3. Ollama 容器启动运行后，就可以用以下命令使用 `tools` 文件夹中的 `download_model.sh`：

   ```console
   . ./download_model.sh <model-name>
   ```

拉取一个 Ollama 模型可能需要几分钟。

{{< /tab >}}
{{< tab name="Run Ollama outside of a container" >}}

要在容器之外运行 Ollama：

1. 在你的宿主机上[安装](https://github.com/jmorganca/ollama)并运行 Ollama。
2. 使用以下命令把模型拉取到 Ollama。

   ```console
   $ ollama pull llama2
   ```

3. 从 `docker-compose.yaml` 中移除 `ollama` 服务，并正确更新 `winy` 服务中的连接变量：

   ```diff
   - OLLAMA=http://ollama:11434
   + OLLAMA=<your-url>
   ```

{{< /tab >}}
{{< /tabs >}}

### 运行你的 RAG 应用

至此，你的 Compose 文件中包含以下服务：

- 用于主 RAG 应用的 server 服务
- 用于在 Qdrant 数据库中存储向量的数据库服务
- （可选）用于运行 LLM 服务的 Ollama 服务

应用运行起来后，打开浏览器访问 [http://localhost:8501](http://localhost:8501)。

取决于你的系统和所选的 LLM 服务，回答可能需要几分钟。

### 小结

在本节中，你学会了如何搭建开发环境，以便访问 GenAI 应用所需的所有服务。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [GenAI Stack 演示应用](https://github.com/docker/genai-stack)

### 下一步

在 [GenAI Stack 演示应用](https://github.com/docker/genai-stack)中查看更多 GenAI 应用示例。
