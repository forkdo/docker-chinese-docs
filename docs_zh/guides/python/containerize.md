---
title: 容器化 Python 应用程序
linkTitle: 容器化你的应用
weight: 10
keywords: python, flask, containerize, initialize
description: 学习如何将 Python 应用程序容器化。
aliases:
  - /language/python/build-images/
  - /language/python/run-containers/
  - /language/python/containerize/
  - /guides/language/python/containerize/
---

## 先决条件

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概览

本节将引导你完成容器化和运行 Python 应用程序的过程。

## 获取示例应用程序

示例应用程序使用了流行的 [FastAPI](https://fastapi.tiangolo.com) 框架。

克隆示例应用程序以配合本指南使用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/estebanx64/python-docker-example && cd python-docker-example
```

## 初始化 Docker 资源

现在你已经有了一个应用程序，可以创建必要的 Docker 资源来容器化你的应用程序。你可以使用 Docker Desktop 内置的 Docker Init 功能来帮助简化这个过程，也可以手动创建这些资源。

{{< tabs >}}
{{< tab name="使用 Docker Init" >}}

在 `python-docker-example` 目录中，运行 `docker init` 命令。`docker init` 会提供一些默认配置，但你需要回答一些关于你的应用程序的问题。例如，这个应用程序使用 FastAPI 来运行。参考以下示例来回答 `docker init` 的提示，并在你的提示中使用相同的答案。

在编辑 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Python Docker 官方镜像](https://hub.docker.com/_/python)，或者 [Docker 加固镜像 (DHI)](https://hub.docker.com/hardened-images/catalog/dhi/python)。

Docker 加固镜像 (DHIs) 是由 Docker 维护的最小、安全且生产就绪的基础镜像。它们有助于减少漏洞并简化合规性。更多详情，请参阅 [Docker 加固镜像](/dhi/)。

```console
$ docker init
欢迎使用 Docker Init CLI！

此工具将引导你创建以下文件，并为你的项目设置合理的默认值：
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

让我们开始吧！

? 你的项目使用什么应用程序平台？Python
? 你想使用哪个版本的 Python？3.12
? 你的应用程序要监听哪个端口？8000
? 运行你的应用程序的命令是什么？python3 -m uvicorn app:app --host=0.0.0.0 --port=8000
```

创建一个名为 `.gitignore` 的文件，内容如下：

```text {collapse=true,title=".gitignore"}
# 字节编译 / 优化 / DLL 文件
__pycache__/
*.py[cod]
*$py.class

# C 扩展
*.so

# 分发 / 打包
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# 单元测试 / 覆盖率报告
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
__pypackages__/

# 环境
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

{{< /tab >}}
{{< tab name="使用官方 Docker 镜像" >}}

如果你没有安装 Docker Desktop 或更喜欢手动创建资源，你可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，内容如下：

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# 此文件中提供了注释以帮助你入门。
# 如果你需要更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

# 想帮助我们改进此模板？请在此处分享你的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7

# 此 Dockerfile 使用 Docker 加固镜像 (DHI) 以增强安全性。
# 更多信息，请参阅 https://docs.docker.com/dhi/
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# 阻止 Python 写入 pyc 文件。
ENV PYTHONDONTWRITEBYTECODE=1

# 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 创建一个非特权用户，应用程序将以此用户身份运行。
# 参见 https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。
# 利用缓存挂载到 /root/.cache/pip 以加速后续构建。
# 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# 切换到非特权用户以运行应用程序。
USER appuser

# 将源代码复制到容器中。
COPY . .

# 暴露应用程序监听的端口。
EXPOSE 8000

# 运行应用程序。
CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

创建一个名为 `compose.yaml` 的文件，内容如下：

```yaml {collapse=true,title=compose.yaml}
# 此文件中提供了注释以帮助你入门。
# 如果你需要更多帮助，请访问 Docker Compose 参考指南：
# https://docs.docker.com/go/compose-spec-reference/

# 这里的指令将你的应用程序定义为一个名为 "server" 的服务。
# 此服务从当前目录中的 Dockerfile 构建。
# 你可以在这里添加你的应用程序可能依赖的其他服务，例如数据库或缓存。
# 有关示例，请参阅 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

创建一个名为 `.dockerignore` 的文件，内容如下：

```text {collapse=true,title=".dockerignore"}
# 在此处包含你不想复制到容器中的任何文件或目录（例如本地构建产物、临时文件等）。
#
# 有关更多帮助，请访问 .dockerignore 文件参考指南：
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

创建一个名为 `.gitignore` 的文件，内容如下：

```text {collapse=true,title=".gitignore"}
# 字节编译 / 优化 / DLL 文件
__pycache__/
*.py[cod]
*$py.class

# C 扩展
*.so

# 分发 / 打包
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# 单元测试 / 覆盖率报告
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
__pypackages__/

# 环境
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

{{< /tab >}}
{{< tab name="使用 Docker 加固镜像" >}}

如果你没有安装 Docker Desktop 或更喜欢手动创建资源，你可以在项目目录中创建以下文件。

创建一个名为 `Dockerfile` 的文件，内容如下：

```dockerfile {collapse=true,title=Dockerfile}
# syntax=docker/dockerfile:1

# 此文件中提供了注释以帮助你入门。
# 如果你需要更多帮助，请访问 Dockerfile 参考指南：
# https://docs.docker.com/go/dockerfile-reference/

# 想帮助我们改进此模板？请在此处分享你的反馈：https://forms.gle/ybq9Krt8jtBL3iCk7

# 此 Dockerfile 使用 Docker 加固镜像 (DHI) 以增强安全性。
# 更多信息，请参阅 https://docs.docker.com/dhi/
ARG PYTHON_VERSION=3.12.12-debian13-fips-dev
FROM <your-workspace>/dhi-python:${PYTHON_VERSION}

# 阻止 Python 写入 pyc 文件。
ENV PYTHONDONTWRITEBYTECODE=1

# 防止 Python 缓冲 stdout 和 stderr，以避免由于缓冲而导致应用程序崩溃时没有发出任何日志的情况。
ENV PYTHONUNBUFFERED=1

# 为 adduser 添加依赖
RUN apt update -y && apt install adduser -y

WORKDIR /app

# 创建一个非特权用户，应用程序将以此用户身份运行。
# 参见 https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# 将下载依赖项作为单独的步骤，以利用 Docker 的缓存。
# 利用缓存挂载到 /root/.cache/pip 以加速后续构建。
# 利用绑定挂载到 requirements.txt 以避免必须将它们复制到此层中。
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# 切换到非特权用户以运行应用程序。
USER appuser

# 将源代码复制到容器中。
COPY . .

# 暴露应用程序监听的端口。
EXPOSE 8000

# 运行应用程序。
CMD ["python3", "-m", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]
```

创建一个名为 `compose.yaml` 的文件，内容如下：

```yaml {collapse=true,title=compose.yaml}
# 此文件中提供了注释以帮助你入门。
# 如果你需要更多帮助，请访问 Docker Compose 参考指南：
# https://docs.docker.com/go/compose-spec-reference/

# 这里的指令将你的应用程序定义为一个名为 "server" 的服务。
# 此服务从当前目录中的 Dockerfile 构建。
# 你可以在这里添加你的应用程序可能依赖的其他服务，例如数据库或缓存。
# 有关示例，请参阅 Awesome Compose 仓库：
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8000:8000
```

创建一个名为 `.dockerignore` 的文件，内容如下：

```text {collapse=true,title=".dockerignore"}
# 在此处包含你不想复制到容器中的任何文件或目录（例如本地构建产物、临时文件等）。
#
# 有关更多帮助，请访问 .dockerignore 文件参考指南：
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

创建一个名为 `.gitignore` 的文件，内容如下：

```text {collapse=true,title=".gitignore"}
# 字节编译 / 优化 / DLL 文件
__pycache__/
*.py[cod]
*$py.class

# C 扩展
*.so

# 分发 / 打包
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# 单元测试 / 覆盖率报告
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# PEP 582；例如 github.com/David-OConnor/pyflow 和 github.com/pdm-project/pdm 使用
__pypackages__/

# 环境
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
```

{{< /tab >}}
{{< /tabs >}}

现在你的 `python-docker-example` 目录中应该包含以下内容：

```text
├── python-docker-example/
│ ├── app.py
│ ├── requirements.txt
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解这些文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [.gitignore](https://git-scm.com/docs/gitignore)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `python-docker-example` 目录中，在终端中运行以下命令：

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。你应该会看到一个简单的 FastAPI 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

你可以通过添加 `-d` 选项来让应用程序在终端后台运行。在 `python-docker-example` 目录中，在终端中运行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8000](http://localhost:8000) 查看应用程序。

要查看 OpenAPI 文档，你可以访问 [http://localhost:8000/docs](http://localhost:8000/docs)。

你应该会看到一个简单的 FastAPI 应用程序。

在终端中，运行以下命令停止应用程序：

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，你学习了如何使用 Docker 容器化和运行你的 Python 应用程序。

相关信息：

- [Docker Compose 概览](/manuals/compose/_index.md)

## 下一步

在下一节中，你将了解如何使用 Docker 容器设置本地开发环境。