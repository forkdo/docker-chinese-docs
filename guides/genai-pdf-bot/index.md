# PDF 分析与对话



生成式 AI（GenAI）指南将教你如何使用 Docker 将现有的 GenAI 应用容器化。在本指南中，你将学习如何：

- 将基于 Python 的 GenAI 应用容器化并运行
- 搭建本地环境以在本地运行完整的 GenAI 技术栈进行开发

首先，将一个现有的 GenAI 应用容器化。

## 将生成式 AI 应用容器化

### 先决条件

> [!NOTE]
>
> GenAI 应用通常可以从 GPU 加速中获益。目前 Docker Desktop 仅支持 [使用 WSL2 后端的 Windows](/manuals/desktop/features/gpu.md#using-nvidia-gpus-with-wsl2) 上的 GPU 加速。Linux 用户也可以通过原生安装 [Docker Engine](/manuals/engine/install/_index.md) 来使用 GPU 加速。

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)，或者，如果你是 Linux 用户并计划使用 GPU 加速，则已安装 [Docker Engine](/manuals/engine/install/_index.md)。Docker 会定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

### 概述

本节将带你使用 Docker Desktop 将生成式 AI（GenAI）应用容器化。

> [!NOTE]
>
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

### 获取示例应用

本指南中使用的示例应用是 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中 PDF Reader 应用的一个修改版本。该应用是一个全栈 Python 应用，可让你就一个 PDF 文件提问问题。

该应用使用 [LangChain](https://www.langchain.com/) 进行编排，[Streamlit](https://streamlit.io/) 作为 UI，[Ollama](https://ollama.ai/) 运行 LLM，以及 [Neo4j](https://neo4j.com/) 存储向量。

克隆示例应用。打开终端，切换到你想工作的目录，并运行以下命令克隆仓库：

```console
$ git clone https://github.com/craig-osterhout/docker-genai-sample
```

现在你的 `docker-genai-sample` 目录中应当包含以下文件。

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

### 创建 Docker 资源

既然已经有了一个应用，你就可以创建将其容器化所需的 Docker 资源。

> [!TIP]
>
> [Gordon](/ai/gordon/) 是 Docker 的 AI 助手，可以为你的项目生成 Docker 资源。让 Gordon 为你的应用创建 Dockerfile、Compose 文件和 `.dockerignore`。

在你的 `docker-genai-sample` 目录中创建以下文件。

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8000"]
```

```yaml {collapse=true,title=compose.yaml}
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000

# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql/data
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt
```

```text {collapse=true,title=".dockerignore"}
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.DS_Store
**/__pycache__
**/.venv
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/bin
**/charts
**/docker-compose*
**/compose.y*ml
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
```

现在你的 `docker-genai-sample` 目录中应当包含以下内容。

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
│ └── README.md
```

要了解这些文件的更多信息，请参阅以下内容：

- [Dockerfile](../../../reference/dockerfile.md)
- [.dockerignore](../../../reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

### 运行应用

在 `docker-genai-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

Docker 会构建并运行你的应用。取决于你的网络连接，下载所有依赖项可能需要几分钟时间。当应用运行时，你会在终端中看到类似以下的消息。

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8000
server-1  |
```

打开浏览器，在 [http://localhost:8000](http://localhost:8000) 查看应用。你应该会看到一个简单的 Streamlit 应用。该应用下载嵌入模型可能需要几分钟时间。在下载进行期间，右上角会显示 **Running**（运行中）。

该应用需要一个 Neo4j 数据库服务和一个 LLM 服务才能运行。如果你有权访问在 Docker 之外运行的服务，请指定连接信息并尝试使用。如果你没有运行这些服务，请继续阅读本指南，了解如何使用 Docker 运行其中部分或全部服务。

在终端中，按 `ctrl`+`c` 停止应用。

### 总结

在本节中，你学习了如何使用 Docker 将 GenAI 应用容器化并运行。

### 后续步骤

在下一节中，你将学习如何使用 Docker 在本地运行你的应用、数据库和 LLM 服务。

## 使用容器进行生成式 AI 开发

### 先决条件

完成 [将生成式 AI 应用容器化](#containerize-a-generative-ai-application)。

### 概述

在本节中，你将学习如何搭建开发环境，以访问生成式 AI（GenAI）应用所需的全部服务。这包括：

- 添加本地数据库
- 添加本地或远程 LLM 服务

> [!NOTE]
>
> 你可以在 [GenAI Stack](https://github.com/docker/genai-stack) 演示应用中看到更多容器化 GenAI 应用的示例。

### 添加本地数据库

你可以使用容器来搭建本地服务，例如数据库。在本节中，你将更新 `compose.yaml` 文件，定义一个数据库服务。此外，你将指定一个环境变量文件来加载数据库连接信息，而不是每次都手动输入这些信息。

要运行数据库服务：

1. 在克隆的仓库目录中，将 `env.example` 文件重命名为 `.env`。
   该文件包含容器将使用的环境变量。
2. 在克隆的仓库目录中，在 IDE 或文本编辑器中打开 `compose.yaml` 文件。
3. 在 `compose.yaml` 文件中，添加以下内容：

   - 添加运行 Neo4j 数据库的说明
   - 在 server 服务下指定环境变量文件，以传入连接所需的环境变量

   以下是更新后的 `compose.yaml` 文件。所有注释均已移除。

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
   > 要了解更多关于 Neo4j 的信息，请参阅 [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)。

4. 运行应用。在 `docker-genai-sample` 目录中，在终端运行以下命令。

   ```console
   $ docker compose up --build
   ```

5. 访问应用。打开浏览器，在 [http://localhost:8000](http://localhost:8000) 查看应用。你应该会看到一个简单的 Streamlit 应用。请注意，向 PDF 提问会导致应用失败，因为 `.env` 文件中指定的 LLM 服务尚未运行。

6. 停止应用。在终端中，按 `ctrl`+`c` 停止应用。

### 添加本地或远程 LLM 服务

示例应用同时支持 [Ollama](https://ollama.ai/) 和 [OpenAI](https://openai.com/)。本指南为以下场景提供说明：

- 在容器中运行 Ollama
- 在容器之外运行 Ollama
- 使用 OpenAI

虽然所有平台都可以使用上述任意场景，但性能和 GPU 支持可能有所不同。你可以使用以下准则来帮助你选择合适的选项：

- 如果你在 Linux 上使用原生安装的 Docker Engine，或在 Windows 10/11 上使用 Docker Desktop，拥有支持 CUDA 的 GPU，且系统至少有 8 GB 内存，则在容器中运行 Ollama。
- 如果你在 Apple 芯片 Mac 上，则在容器之外运行 Ollama。
- 如果前两种场景都不适用于你，则使用 OpenAI。

为你的 LLM 服务选择以下选项之一。

**在容器中运行 Ollama**



在容器中运行 Ollama 时，你应该拥有一块支持 CUDA 的 GPU。虽然你可以在没有支持 GPU 的情况下在容器中运行 Ollama，但性能可能不尽如人意。只有 Linux 和 Windows 11 支持容器访问 GPU。

要在容器中运行 Ollama 并提供 GPU 访问：

1. 安装先决条件。
   - 对于 Linux 上的 Docker Engine，请安装 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit)。
   - 对于 Windows 10/11 上的 Docker Desktop，请安装最新的 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)，并确保你正在使用 [WSL2 后端](/manuals/desktop/features/wsl/_index.md#turn-on-docker-desktop-wsl-2)
2. 在你的 `compose.yaml` 中添加 Ollama 服务和一个卷。以下是更新后的 `compose.yaml`：

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
   > 关于 Compose 说明的更多详情，请参阅 [使用 Docker Compose 开启 GPU 访问](/manuals/compose/how-tos/gpu-support.md)。

3. 在你的 `compose.yaml` 文件中添加 ollama-pull 服务。该服务使用基于 GenAI Stack 的 [pull_model.Dockerfile](https://github.com/docker/genai-stack/blob/main/pull_model.Dockerfile) 的 `docker/genai:ollama-pull` 镜像。该服务将自动为你的 Ollama 容器拉取模型。以下是 `compose.yaml` 文件的更新部分：

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

**在容器之外运行 Ollama**



要在容器之外运行 Ollama：

1. 在你的主机上 [安装](https://github.com/jmorganca/ollama) 并运行 Ollama。
2. 将 `.env` 文件中的 `OLLAMA_BASE_URL` 值更新为
   `http://host.docker.internal:11434`。
3. 使用以下命令将模型拉取至 Ollama。
   ```console
   $ ollama pull llama2
   ```

**使用 OpenAI**



> [!IMPORTANT]
>
> 使用 OpenAI 需要有一个 [OpenAI 账户](https://platform.openai.com/login)。OpenAI 是一项第三方托管服务，可能会产生费用。

1. 将 `.env` 文件中的 `LLM` 值更新为
   `gpt-3.5`。
2. 取消 `.env` 文件中 `OPENAI_API_KEY` 值的注释并更新为你自己的 [OpenAI API 密钥](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key)。



### 运行你的 GenAI 应用

此时，你的 Compose 文件中包含以下服务：

- 用于主 GenAI 应用的 server 服务
- 用于在 Neo4j 数据库中存储向量的数据库服务
- （可选）用于运行 LLM 的 Ollama 服务
- （可选）用于自动为 Ollama 服务拉取模型的 Ollama-pull 服务

要运行所有服务，在你的 `docker-genai-sample` 目录中运行以下命令：

```console
$ docker compose up --build
```

如果你的 Compose 文件包含 ollama-pull 服务，ollama-pull 服务拉取模型可能需要几分钟时间。ollama-pull 服务会持续向控制台更新其状态。拉取模型完成后，ollama-pull 服务容器将停止，届时你可以访问应用。

应用运行后，打开浏览器并在 [http://localhost:8000](http://localhost:8000) 访问应用。

上传一个 PDF 文件，例如 [Docker CLI 速查表](https://docs.docker.com/get-started/docker_cheatsheet.pdf)，并就该 PDF 提问。

取决于你的系统以及所选择的 LLM 服务，回答可能需要几分钟时间。如果你使用的是 Ollama 且性能不尽如人意，请尝试使用 OpenAI。

### 总结

在本节中，你学习了如何搭建开发环境，以提供对 GenAI 应用所需的全部服务的访问。

相关信息：

- [Dockerfile 参考](../../../reference/dockerfile.md)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Ollama Docker 镜像](https://hub.docker.com/r/ollama/ollama)
- [Neo4j 官方 Docker 镜像](https://hub.docker.com/_/neo4j)
- [GenAI Stack 演示应用](https://github.com/docker/genai-stack)

### 后续步骤

在 [GenAI Stack 演示应用](https://github.com/docker/genai-stack) 中查看更多 GenAI 应用的示例。

