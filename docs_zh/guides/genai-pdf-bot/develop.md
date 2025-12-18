---
title: 为生成式 AI 开发使用容器
linkTitle: 开发你的应用
weight: 20
keywords: python, local, development, generative ai, genai, llm, neo4j, ollama, langchain, openai
description: 了解如何在本地开发你的生成式 AI（GenAI）应用。
aliases:
  - /guides/use-case/genai-pdf-bot/develop/
---

## 前置条件

完成 [Containerize a generative AI application](containerize.md)。

## 概述

在本节中，你将学习如何设置开发环境，以访问你的生成式 AI（GenAI）应用所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
>
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

## 添加本地数据库

你可以使用容器来设置本地服务，比如数据库。在本节中，你将更新 `compose.yaml` 文件以定义数据库服务。此外，你将指定一个环境变量文件来加载数据库连接信息，而不是每次都手动输入。

运行数据库服务的步骤如下：

1. 在克隆的仓库目录中，将 `env.example` 文件重命名为 `.env`。
   此文件包含容器将使用的环境变量。
2. 在克隆的仓库目录中，使用 IDE 或文本编辑器打开 `compose.yaml` 文件。
3. 在 `compose.yaml` 文件中，添加以下内容：

   - 添加运行 Neo4j 数据库的指令
   - 在服务器服务下指定环境文件，以便传入连接所需的环境变量

   以下是更新后的 `compose.yaml` 文件。所有注释已删除。

   ```yaml{hl_lines=["7-23"]}
   services:
     server:
       build:
         context: .
       ports:
         - 8000:8000
       env_file:
         - .env
       depends_on:
         database:
           condition: service_healthy
     database:
       image: neo4j:5.11
       ports:
         - "7474:7474"
         - "7687:7687"
       environment:
         - NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}
       healthcheck:
         test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider localhost:7474 || exit 1"]
         interval: 5s
         timeout: 3s
         retries: 5
   ```

   > [!NOTE]
   >
   > 要了解有关 Neo4j 的更多信息，请参阅 [Neo4j Official Docker Image](https://hub.docker.com/_/neo4j)。

4. 运行应用。在 `docker-genai-sample` 目录中，终端中运行以下命令。

   ```console
   $ docker compose up --build
   ```

5. 访问应用。打开浏览器，在 [http://localhost:8000](http://localhost:8000) 查看应用。你应该能看到一个简单的 Streamlit 应用。注意，向 PDF 提问会导致应用失败，因为 `.env` 文件中指定的 LLM 服务尚未运行。

6. 停止应用。在终端中按 `ctrl`+`c` 停止应用。

## 添加本地或远程 LLM 服务

示例应用支持 [Ollama](https://ollama.ai/) 和 [OpenAI](https://openai.com/)。本指南为以下场景提供说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama
- 使用 OpenAI

虽然所有平台都可以使用上述任一场景，但性能和 GPU 支持可能有所不同。你可以参考以下指南选择合适的选项：

- 如果你在 Linux 上，使用原生 Docker Engine 安装，或在 Windows 10/11 上使用 Docker Desktop，你有 CUDA 支持的 GPU，且系统至少有 8 GB RAM，则在容器中运行 Ollama。
- 如果你在 Apple Silicon Mac 上，则在容器外运行 Ollama。
- 如果上述两种情况都不适用，则使用 OpenAI。

为你的 LLM 服务选择以下选项之一。

{{< tabs >}}
{{< tab name="在容器中运行 Ollama" >}}

在容器中运行 Ollama 时，你应该有 CUDA 支持的 GPU。虽然你可以在没有支持的 GPU 的情况下在容器中运行 Ollama，但性能可能无法接受。只有 Linux 和 Windows 11 支持容器的 GPU 访问。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装前置条件。
   - 对于 Linux 上的 Docker Engine，安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，安装最新的 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)，并确保你使用的是 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)
2. 在你的 `compose.yaml` 中添加 Ollama 服务和卷。以下是更新后的 `compose.yaml`：

   ```yaml {hl_lines=["24-38"]}
   services:
     server:
       build:
         context: .
       ports:
         - 8000:8000
       env_file:
         - .env
       depends_on:
         database:
           condition: service_healthy
     database:
       image: neo4j:5.11
       ports:
         - "7474:7474"
         - "7687:7687"
       environment:
         - NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}
       healthcheck:
         test:
           [
             "CMD-SHELL",
             "wget --no-verbose --tries=1 --spider localhost:7474 || exit 1",
           ]
         interval: 5s
         timeout: 3s
         retries: 5
     ollama:
       image: ollama/ollama:latest
       ports:
         - "11434:11434"
       volumes:
         - ollama_volume:/root/.ollama
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: all
                 capabilities: [gpu]
   volumes:
     ollama_volume:
   ```

   > [!NOTE]
   >
   > 有关 Compose 指令的更多详细信息，请参阅 [Turn on GPU access with Docker Compose](/manuals/compose/how-tos/gpu-support.md)。

3. 在你的 `compose.yaml` 文件中添加 ollama-pull 服务。该服务使用 `docker/genai:ollama-pull` 镜像，基于 GenAI Stack 的 [pull_model.Dockerfile](https://github.com/docker/genai-stack/blob/main/pull_model.Dockerfile)。该服务将自动为你的 Ollama 容器拉取模型。以下是更新后的 `compose.yaml` 文件片段：

   ```yaml {hl_lines=["12-17"]}
   services:
     server:
       build:
         context: .
       ports:
         - 8000:8000
       env_file:
         - .env
       depends_on:
         database:
           condition: service_healthy
         ollama-pull:
           condition: service_completed_successfully
     ollama-pull:
       image: docker/genai:ollama-pull
       env_file:
         - .env
     # ...
   ```

{{< /tab >}}
{{< tab name="在容器外运行 Ollama" >}}

在容器外运行 Ollama：

1. 在主机上 [安装](https://github.com/jmorganca/ollama) 并运行 Ollama。
2. 在你的 `.env` 文件中将 `OLLAMA_BASE_URL` 值更新为 `http://host.docker.internal:11434`。
3. 使用以下命令将模型拉取到 Ollama。
   ```console
   $ ollama pull llama2
   ```

{{< /tab >}}
{{< tab name="使用 OpenAI" >}}

> [!IMPORTANT]
>
> 使用 OpenAI 需要 [OpenAI 账户](https://platform.openai.com/login)。OpenAI 是第三方托管服务，可能会产生费用。

1. 在你的 `.env` 文件中将 `LLM` 值更新为 `gpt-3.5`。
2. 取消注释并更新 `.env` 文件中的 `OPENAI_API_KEY` 值为你自己的 [OpenAI API 密钥](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)。

{{< /tab >}}
{{< /tabs >}}

## 运行你的 GenAI 应用

此时，你的 Compose 文件中已有以下服务：

- 你的主要 GenAI 应用的服务器服务
- 在 Neo4j 数据库中存储向量的数据库服务
- （可选）运行 LLM 的 Ollama 服务
- （可选）为 Ollama 服务自动拉取模型的 ollama-pull 服务

要运行所有服务，在你的 `docker-genai-sample` 目录中运行以下命令：

```console
$ docker compose up --build
```

如果你的 Compose 文件中有 ollama-pull 服务，ollama-pull 服务可能需要几分钟才能拉取模型。ollama-pull 服务会持续更新控制台状态。拉取模型后，ollama-pull 服务容器将停止，然后你就可以访问应用了。

应用运行后，打开浏览器，在 [http://localhost:8000](http://localhost:8000) 访问应用。

上传一个 PDF 文件，例如 [Docker CLI Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)，并询问关于 PDF 的问题。

根据你的系统和选择的 LLM 服务，可能需要几分钟才能回答。如果你使用 Ollama 且性能不理想，尝试使用 OpenAI。

## 总结

在本节中，你学习了如何设置开发环境，以提供访问你的 GenAI 应用所需的所有服务。

相关信息：

- [Dockerfile 参考](../../../reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [Neo4j Official Docker Image](https://hub.docker.com/_/neo4j)
- [GenAI Stack 演示应用](https://github.com/docker/genai-stack)

## 后续步骤

查看 [GenAI Stack 演示应用](https://github.com/docker/genai-stack) 中更多 GenAI 应用的示例。