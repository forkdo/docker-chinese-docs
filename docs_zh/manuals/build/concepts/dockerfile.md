---
title: Dockerfile 概述
weight: 20
description: 了解 Dockerfile 以及如何在 Docker 镜像中使用它们来构建和打包你的软件
keywords: build, buildx, buildkit, getting started, dockerfile
aliases:
  - /build/hellobuild/
  - /build/building/packaging/
---

<!-- vale Docker.We = NO -->

## Dockerfile

一切都从 Dockerfile 开始。

Docker 通过读取 Dockerfile 中的指令来构建镜像。Dockerfile 是一个文本文件，包含用于构建源代码的指令。Dockerfile 指令语法由 [Dockerfile 参考](/reference/dockerfile.md)中的规范参考定义。

以下是最常见的指令类型：

| 指令                                                      | 说明                                                                                                                                                    |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FROM <image>`](/reference/dockerfile.md#from)           | 为你的镜像定义基础。                                                                                                                                    |
| [`RUN <command>`](/reference/dockerfile.md#run)           | 在当前镜像之上的新层中执行任意命令，并提交结果。`RUN` 还具有用于运行命令的 shell 形式。                                                                 |
| [`WORKDIR <directory>`](/reference/dockerfile.md#workdir) | 为 Dockerfile 中其后跟随的任何 `RUN`、`CMD`、`ENTRYPOINT`、`COPY` 和 `ADD` 指令设置工作目录。                                                          |
| [`COPY <src> <dest>`](/reference/dockerfile.md#copy)      | 从 `<src>` 复制新文件或目录，并将其添加到容器文件系统中 `<dest>` 路径处。                                                                               |
| [`CMD <command>`](/reference/dockerfile.md#cmd)           | 让你定义启动基于此镜像的容器时默认运行的程序。每个 Dockerfile 只有一个 `CMD`，当存在多个时，只有最后一个 `CMD` 实例会被采纳。                          |

Dockerfile 是镜像构建的关键输入，可以根据你的独特配置实现自动化、多层的镜像构建。Dockerfile 可以从简单开始，并随着你的需求增长以支持更复杂的场景。

### Filename

Dockerfile 的默认文件名是 `Dockerfile`，不带文件扩展名。使用默认名称可以让你运行 `docker build` 命令时无需指定额外的命令标志。

某些项目可能需要用于特定用途的独立 Dockerfile。常见的约定是将它们命名为 `<something>.Dockerfile`。你可以使用 `docker build` 命令的 `--file` 标志来指定 Dockerfile 文件名。请参阅 [`docker build` CLI 参考](/reference/cli/docker/buildx/build/#file) 了解 `--file` 标志。

> [!NOTE]
>
> 我们建议为项目的主要 Dockerfile 使用默认名称（`Dockerfile`）。

## Docker images

Docker 镜像由层组成。每一层都是 Dockerfile 中一条构建指令的结果。这些层按顺序堆叠，每一层都是一个增量（delta），表示应用于上一层所做的更改。

### Example

以下是使用 Docker 构建应用程序的典型工作流。

下面的示例代码展示了一个用 Python 编写的、使用 Flask 框架的小型 "Hello World" 应用程序。

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

如果不使用 Docker Build 来交付和部署此应用程序，你需要确保：

- 服务器上已安装所需的运行时依赖
- Python 代码已上传到服务器的文件系统
- 服务器使用必要参数启动你的应用程序

下面这个 Dockerfile 创建了一个容器镜像，其中安装了所有依赖，并会自动启动你的应用程序。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.*

# install app
COPY hello.py /

# final configuration
ENV FLASK_APP=hello
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

以下是对这个 Dockerfile 各部分作用的拆解：

- [Dockerfile 语法](#dockerfile-syntax)
- [基础镜像](#base-image)
- [环境设置](#environment-setup)
- [注释](#comments)
- [安装依赖](#installing-dependencies)
- [复制文件](#copying-files)
- [设置环境变量](#setting-environment-variables)
- [暴露端口](#exposed-ports)
- [启动应用程序](#starting-the-application)

### Dockerfile syntax

要添加到 Dockerfile 的第一行是 [`# syntax` 解析器指令](/reference/dockerfile.md#syntax)。虽然它是可选的，但该指令指示 Docker 构建器在解析 Dockerfile 时使用什么语法，并允许启用了 [BuildKit](../buildkit/_index.md#getting-started) 的旧版 Docker 在开始构建前使用特定的 [Dockerfile 前端](../buildkit/frontend.md)。[解析器指令](/reference/dockerfile.md#parser-directives) 必须出现在 Dockerfile 中任何其他注释、空白或 Dockerfile 指令之前，并且应当是 Dockerfile 的第一行。

```dockerfile
# syntax=docker/dockerfile:1
```

> [!TIP]
>
> 我们建议使用 `docker/dockerfile:1`，它始终指向版本 1 语法的最新发布版本。BuildKit 会在构建前自动检查该语法的更新，确保你使用的是最新版本。

### Base image

语法指令之后的那一行定义了要使用的基础镜像：

```dockerfile
FROM ubuntu:22.04
```

[`FROM` 指令](/reference/dockerfile.md#from) 将你的基础镜像设置为 Ubuntu 的 22.04 版本。其后跟随的所有指令都在这个基础镜像——一个 Ubuntu 环境中——执行。符号 `ubuntu:22.04` 遵循 Docker 镜像命名的 `name:tag` 标准。构建镜像时，你使用这种符号来命名你的镜像。你可以将许多公共镜像导入到构建步骤中（通过 Dockerfile 的 `FROM` 指令）以在你的项目中使用。

[Docker Hub](https://hub.docker.com/search?badges=official) 包含大量可供此用途使用的官方镜像。

### Environment setup

下面这行在基础镜像内部执行一条构建命令。

```dockerfile
# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
```

这条 [`RUN` 指令](/reference/dockerfile.md#run) 在 Ubuntu 中执行一个 shell，更新 APT 包索引并在容器中安装 Python 工具。

### Comments

注意 `# install app dependencies` 这一行。这是一条注释。Dockerfile 中的注释以 `#` 符号开头。随着你的 Dockerfile 不断演进，注释对于记录 Dockerfile 的工作原理非常有用，便于文件未来的任何读者和编辑者（包括未来的你自己）理解。

> [!NOTE]
>
> 你可能已经注意到，注释使用的符号与文件第一行的 [语法指令](#dockerfile-syntax) 相同。只有当该模式匹配某条指令且出现在 Dockerfile 开头时，该符号才会被解释为指令。否则，它会被视为注释。

### Installing dependencies

第二条 `RUN` 指令安装 Python 应用程序所需的 `flask` 依赖。

```dockerfile
RUN pip install flask==3.0.*
```

这条指令的前提是 `pip` 已安装到构建容器中。第一条 `RUN` 命令安装了 `pip`，从而确保我们可以使用该命令来安装 flask Web 框架。

### Copying files

下一条指令使用 [`COPY` 指令](/reference/dockerfile.md#copy) 将 `hello.py` 文件从本地构建上下文复制到镜像的根目录。

```dockerfile
COPY hello.py /
```

[构建上下文](./context.md) 是你在 `COPY` 和 `ADD` 等 Dockerfile 指令中可以访问的文件集合。

在 `COPY` 指令之后，`hello.py` 文件被添加到构建容器的文件系统中。

### Setting environment variables

如果你的应用程序使用环境变量，可以在 Docker 构建中使用 [`ENV` 指令](/reference/dockerfile.md#env) 设置环境变量。

```dockerfile
ENV FLASK_APP=hello
```

这会设置一个我们稍后需要用到的 Linux 环境变量。本示例中使用的框架 Flask 使用该变量来启动应用程序。如果没有它，flask 将无法知道去哪里找到我们的应用程序以运行它。

### Exposed ports

[`EXPOSE` 指令](/reference/dockerfile.md#expose) 标记我们的最终镜像有一个服务正在端口 `8000` 上监听。

```dockerfile
EXPOSE 8000
```

这条指令不是必需的，但它是一个好习惯，有助于工具和团队成员理解这个应用程序在做什么。

### Starting the application

最后，[`CMD` 指令](/reference/dockerfile.md#cmd) 设置了当用户启动基于此镜像的容器时所运行的命令。

```dockerfile
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
```

该命令启动 flask 开发服务器，监听端口 `8000` 上的所有地址。此处的示例使用了 `CMD` 的 "exec 形式" 版本。也可以使用 "shell 形式"：

```dockerfile
CMD flask run --host 0.0.0.0 --port 8000
```

这两个版本之间存在细微差别，例如在它们如何捕获 `SIGTERM` 和 `SIGKILL` 等信号方面。有关这些差别的更多信息，请参阅 [Shell 与 exec 形式](/reference/dockerfile.md#shell-and-exec-form)。

## Building

要使用 [上一节](#example) 中的 Dockerfile 示例构建容器镜像，你需要使用 `docker build` 命令：

```console
$ docker build -t test:latest .
```

`-t test:latest` 选项指定镜像的名称和标签。

命令末尾的单个点（`.`）将 [构建上下文](./context.md) 设置为当前目录。这意味着构建期望在调用命令的目录中找到 Dockerfile 和 `hello.py` 文件。如果这些文件不在那里，构建将失败。

镜像构建完成后，你可以使用 `docker run` 指定镜像名称，将其作为容器运行：

```console
$ docker run -p 127.0.0.1:8000:8000 test:latest
```

这会将容器的 8000 端口发布到 Docker 主机上的 `http://localhost:8000`。

> [!TIP]
>
> 要改进你在 Visual Studio Code 中对 Dockerfile 的代码检查、代码导航和漏洞扫描，请参阅 [Docker DX](https://marketplace.visualstudio.com/items?itemName=docker.docker) 扩展。
