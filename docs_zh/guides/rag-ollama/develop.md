---
title: 为 RAG 开发使用容器
linkTitle: 开发你的应用
weight: 10
keywords: python, local, development, generative ai, genai, llm, rag, ollama
description: 了解如何在本地开发你的生成式 RAG 应用。
aliases:
  - /guides/use-case/rag-ollama/develop/
---

## 前置条件

完成 [容器化 RAG 应用](containerize.md)。

## 概述

在本节中，你将学习如何设置开发环境，以访问生成式 RAG 应用所需的所有服务。包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

## 添加本地数据库

你可以使用容器来设置本地服务，例如数据库。在本节中，你将探索 `docker-compose.yaml` 文件中的数据库服务。

运行数据库服务：

1. 在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `docker-compose.yaml` 文件。

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
   > 要了解有关 Qdrant 的更多信息，请参阅 [Qdrant 官方 Docker 镜像](https://hub.docker.com/r/qdrant/qdrant)。

3. 启动应用。在 `winy` 目录中，终端运行以下命令：

   ```console
   $ docker compose up --build
   ```

4. 访问应用。打开浏览器，在 [http://localhost:8501](http://localhost:8501) 查看应用。你应该能看到一个简单的 Streamlit 应用。

5. 停止应用。在终端中按 `ctrl`+`c` 停止应用。

## 添加本地或远程 LLM 服务

示例应用支持 [Ollama](https://ollama.ai/)。本指南提供以下场景的说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama

虽然所有平台都可以使用上述任一场景，但性能和 GPU 支持可能有所不同。你可以参考以下指南选择合适的选项：

- 如果你在 Linux 上使用 Docker Engine 原生安装，或在 Windows 10/11 上使用 Docker Desktop，且你有 CUDA 支持的 GPU，系统至少有 8 GB RAM，则在容器中运行 Ollama。
- 如果在 Linux 机器上使用 Docker Desktop，则在容器外运行 Ollama。

为你的 LLM 服务选择以下选项之一。

{{< tabs >}}
{{< tab name="在容器中运行 Ollama" >}}

在容器中运行 Ollama 时，你应该有 CUDA 支持的 GPU。虽然你可以在没有支持的 GPU 的情况下在容器中运行 Ollama，但性能可能无法接受。只有 Linux 和 Windows 11 支持容器的 GPU 访问。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装前置条件。
   - 对于 Linux 上的 Docker Engine，安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，安装最新的 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)，并确保你使用 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)。
2. `docker-compose.yaml` 文件已包含必要的指令。在你自己的应用中，需要在 `docker-compose.yaml` 中添加 Ollama 服务。以下是更新后的 `docker-compose.yaml`：

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
   > 有关 Compose 指令的更多详细信息，请参阅 [使用 Docker Compose 启用 GPU 访问](/manuals/compose/how-tos/gpu-support.md)。

3. Ollama 容器启动并运行后，可以使用 `tools` 文件夹中的 `download_model.sh` 执行以下命令：

   ```console
   . ./download_model.sh <model-name>
   ```

拉取 Ollama 模型可能需要几分钟。

{{< /tab >}}
{{< tab name="在容器外运行 Ollama" >}}

在容器外运行 Ollama：

1. 在主机上 [安装](https://github.com/jmorganca/ollama) 并运行 Ollama。
2. 使用以下命令从 Ollama 拉取模型：

   ```console
   $ ollama pull llama2
   ```

3. 从 `docker-compose.yaml` 中移除 `ollama` 服务，并在 `winy` 服务中正确更新连接变量：

   ```diff
   - OLLAMA=http://ollama:11434
   + OLLAMA=<your-url>
   ```

{{< /tab >}}
{{< /tabs >}}

## 运行你的 RAG 应用

此时，你的 Compose 文件中已有以下服务：

- 主 RAG 应用的服务器服务
- 在 Qdrant 数据库中存储向量的数据库服务
- （可选）运行 LLM 服务的 Ollama 服务

应用启动后，打开浏览器在 [http://localhost:8501](http://localhost:8501) 访问应用。

根据你的系统和选择的 LLM 服务，回答可能需要几分钟。

## 小结

在本节中，你学习了如何设置开发环境，以提供访问 GenAI 应用所需的所有服务。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [GenAI Stack 演示应用](https://github.com/docker/genai-stack)

## 后续步骤

在 [GenAI Stack 演示应用](https://github.com/docker/genai-stack) 中查看更多 GenAI 应用的示例。