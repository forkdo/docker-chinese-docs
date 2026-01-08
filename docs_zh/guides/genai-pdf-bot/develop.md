---
title: 使用容器进行生成式 AI 开发
linkTitle: 开发您的应用
weight: 20
keywords: python, local, development, generative ai, genai, llm, neo4j, ollama, langchain, openai
description: 学习如何在本地开发您的生成式 AI (GenAI) 应用程序。
aliases:
- /guides/use-case/genai-pdf-bot/develop/
---

## 先决条件

完成 [容器化生成式 AI 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何设置开发环境，以访问生成式 AI (GenAI) 应用程序所需的所有服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
>
> 您可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用程序中看到更多容器化 GenAI 应用程序的示例。

## 添加本地数据库

您可以使用容器来设置本地服务，例如数据库。在本节中，您将更新 `compose.yaml` 文件以定义数据库服务。此外，您还将指定一个环境变量文件，以加载数据库连接信息，而不是每次都手动输入信息。

要运行数据库服务：

1. 在克隆的仓库目录中，将 `env.example` 文件重命名为 `.env`。
   该文件包含容器将使用的环境变量。
2. 在克隆的仓库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。
3. 在 `compose.yaml` 文件中，添加以下内容：

   - 添加运行 Neo4j 数据库的指令
   - 在服务器服务下指定环境文件，以便传入连接的环境变量

   以下是更新后的 `compose.yaml` 文件。所有注释已被移除。

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
   > 要了解有关 Neo4j 的更多信息，请参阅 [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)。

4. 运行应用程序。在 `docker-genai-sample` 目录中，
   在终端中运行以下命令。

   ```console
   $ docker compose up --build
   ```

5. 访问应用程序。打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 上的应用程序。您应该看到一个简单的 Streamlit 应用程序。请注意，向 PDF 提问会导致应用程序失败，因为 `.env` 文件中指定的 LLM 服务尚未运行。

6. 停止应用程序。在终端中，按 `ctrl`+`c` 停止应用程序。

## 添加本地或远程 LLM 服务

示例应用程序支持 [Ollama](https://ollama.ai/) 和 [OpenAI](https://openai.com/)。本指南为以下场景提供说明：

- 在容器中运行 Ollama
- 在容器外运行 Ollama
- 使用 OpenAI

虽然所有平台都可以使用上述任何场景，但性能和 GPU 支持可能会有所不同。您可以使用以下指南帮助您选择适当的选项：

- 如果您使用的是 Linux 和 Docker Engine 的原生安装，或 Windows 10/11 和 Docker Desktop，并且您有支持 CUDA 的 GPU，且系统至少有 8 GB RAM，请在容器中运行 Ollama。
- 如果您使用的是 Apple silicon Mac，请在容器外运行 Ollama。
- 如果前两个场景不适用于您，请使用 OpenAI。

为您的 LLM 服务选择以下选项之一。

{{< tabs >}}
{{< tab name="在容器中运行 Ollama" >}}

在容器中运行 Ollama 时，您应该有一个支持 CUDA 的 GPU。虽然您可以在没有支持 GPU 的容器中运行 Ollama，但性能可能不可接受。只有 Linux 和 Windows 11 支持容器的 GPU 访问。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装先决条件。
   - 对于 Linux 上的 Docker Engine，安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，安装最新的 [NVIDIA 驱动程序](https://www.nvidia.com/Download/index.aspx)，并确保您使用的是 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)
2. 在 `compose.yaml` 中添加 Ollama 服务和卷。以下是
   更新后的 `compose.yaml`：

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
   > 有关 Compose 指令的更多详细信息，请参阅 [使用 Docker Compose 启用 GPU 访问](/manuals/compose/how-tos/gpu-support.md)。

3. 在 `compose.yaml` 文件中添加 ollama-pull 服务。此服务使用
   `docker/genai:ollama-pull` 镜像，基于 GenAI Stack 的
   [pull_model.Dockerfile](https://github.com/docker/genai-stack/blob/main/pull_model.Dockerfile)。
   该服务将自动为您的 Ollama 容器拉取模型。以下是 `compose.yaml` 文件的更新部分：

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

要在容器外运行 Ollama：

1. [安装](https://github.com/jmorganca/ollama) 并在您的主机上运行 Ollama。
2. 在 `.env` 文件中更新 `OLLAMA_BASE_URL` 值为
   `http://host.docker.internal:11434`。
3. 使用以下命令将模型拉取到 Ollama。
   ```console
   $ ollama pull llama2
   ```

{{< /tab >}}
{{< tab name="使用 OpenAI" >}}

> [!IMPORTANT]
>
> 使用 OpenAI 需要 [OpenAI 账户](https://platform.openai.com/login)。OpenAI 是第三方托管服务，可能会产生费用。

1. 在 `.env` 文件中更新 `LLM` 值为
   `gpt-3.5`。
2. 取消注释并更新 `.env` 文件中的 `OPENAI_API_KEY` 值
   为您的 [OpenAI API 密钥](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)。

{{< /tab >}}
{{< /tabs >}}

## 运行您的 GenAI 应用程序

此时，您的 Compose 文件中包含以下服务：

- 用于主 GenAI 应用程序的服务器服务
- 用于在 Neo4j 数据库中存储向量的数据库服务
- （可选）用于运行 LLM 的 Ollama 服务
- （可选）用于自动为 Ollama 服务拉取模型的 Ollama-pull 服务

要运行所有服务，请在 `docker-genai-sample` 目录中运行以下命令：

```console
$ docker compose up --build
```

如果您的 Compose 文件包含 ollama-pull 服务，则 ollama-pull 服务可能需要几分钟才能拉取模型。ollama-pull 服务将持续更新控制台状态。拉取模型后，ollama-pull 服务容器将停止，您可以访问应用程序。

应用程序运行后，打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 上的应用程序。

上传一个 PDF 文件，例如 [Docker CLI 速查表](https://docs.docker.com/get-started/docker_cheatsheet.pdf)，并询问有关 PDF 的问题。

根据您的系统和您选择的 LLM 服务，回答可能需要几分钟。如果您使用的是 Ollama 且性能不可接受，请尝试使用 OpenAI。

## 总结

在本节中，您学习了如何设置开发环境，以提供对 GenAI 应用程序所需的所有服务的访问。

相关信息：

- [Dockerfile 参考](../../../reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)
- [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack)

## 下一步

在 [GenAI Stack 演示应用程序](https://github.com/docker/genai-stack) 中查看更多的 GenAI 应用程序示例。