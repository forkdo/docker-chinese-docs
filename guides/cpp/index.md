# C++ 语言专项指南


C++ 入门指南将教你如何使用 Docker 创建容器化的 C++ 应用。在本指南中，你将学习如何：

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 和 [Mohammad-Ali A'râbi](https://twitter.com/MohammadAliEN) 对本指南做出的贡献。

- 使用多阶段 Docker 构建来容器化并运行 C++ 应用
- 使用 Docker Compose 构建并运行 C++ 应用
- 使用容器搭建用于开发 C++ 应用的本地环境

完成 C++ 入门模块后，你应该能够参照本指南提供的示例和说明，容器化你自己的 C++ 应用。

首先从容器化一个已有的 C++ 应用开始。

## Create a multi-stage build for your C++ application（为 C++ 应用创建多阶段构建）

### 先决条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任意客户端。

### 概述

本节将引导你为 C++ 应用创建多阶段 Docker 构建。
多阶段构建是 Docker 的一项特性，允许你在构建过程的不同阶段使用不同的基础镜像，
从而优化最终镜像的体积，并将构建依赖与运行时依赖分离。

对于 C++ 这类编译型语言，标准做法是设置一个编译代码的构建阶段和一个运行编译产物的运行时阶段，
因为构建依赖在运行时并不需要。

### 获取示例应用

我们使用一个简单的 C++ 应用，它会在终端打印 `Hello, World!`。为此，克隆本指南使用的示例仓库：

```bash
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

本节的示例位于仓库的 `hello` 目录下。进入该目录并查看其中的文件：

```bash
$ cd c-plus-plus-docker/hello
$ ls
```

你应该会看到以下文件：

```text
Dockerfile  hello.cpp
```

### 查看 Dockerfile

在 IDE 或文本编辑器中打开 `Dockerfile`。该 `Dockerfile` 包含构建 Docker 镜像的指令。

```Dockerfile
# Stage 1: Build stage
FROM ubuntu:latest AS build

# Install build-essential for compiling C++ code
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the source code into the container
COPY hello.cpp .

# Compile the C++ code statically to ensure it doesn't depend on runtime libraries
RUN g++ -o hello hello.cpp -static

# Stage 2: Runtime stage
FROM scratch

# Copy the static binary from the build stage
COPY --from=build /app/hello /hello

# Command to run the binary
CMD ["/hello"]
```

该 `Dockerfile` 包含两个阶段：

1. **构建阶段**：该阶段使用 `ubuntu:latest` 镜像编译 C++ 代码并生成静态二进制文件。
2. **运行时阶段**：该阶段使用空镜像 `scratch`，从构建阶段复制静态二进制文件并运行它。

### 构建 Docker 镜像

要构建 Docker 镜像，请在 `hello` 目录中运行以下命令：

```bash
$ docker build -t hello .
```

`-t` 标志将镜像命名为 `hello`。

### 运行 Docker 容器

要运行 Docker 容器，请使用以下命令：

```bash
$ docker run hello
```

你应该会在终端看到输出 `Hello, World!`。

由于最终镜像使用空的 `scratch` 基础镜像，它只包含
静态二进制文件，不含任何构建依赖或常见的操作系统工具。例如，
你无法在容器中运行简单的 `ls` 命令：

```bash
$ docker run hello ls
```

没有 shell 和其他工具让镜像保持小巧，并减少了其
攻击面。

## Containerize a C++ application（容器化 C++ 应用）

### 先决条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任意客户端。

### 概述

本节将引导你使用 Docker Compose 容器化并运行 C++ 应用。

### 获取示例应用

我们使用本指南前面章节中用过的同一个示例仓库。如果你还没有克隆该仓库，现在克隆它：

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

现在你的 `c-plus-plus-docker`（根）目录中应该有以下内容。

```text
├── c-plus-plus-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── ok_api.cpp
│ └── README.md

```

要了解仓库中这些文件的更多信息，请参阅：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yml](/reference/compose-file/_index.md)

### 运行应用

在 `c-plus-plus-docker` 目录中，于终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用。你会在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以添加 `-d` 选项让应用脱离终端运行。
在 `c-plus-plus-docker` 目录中，于终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI
参考](/reference/cli/docker/compose/)。

## Use containers for C++ development（使用容器进行 C++ 开发）

### 先决条件

完成 [容器化 C++ 应用](#containerize-a-c-application)。

### 概述

在本节中，你将学习如何为容器化应用搭建开发环境。这包括：

- 配置 Compose，使其在你编辑并保存代码时自动更新正在运行的 Compose 服务

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git && cd c-plus-plus-docker
```

### 自动更新服务

使用 Compose Watch 在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详情，请参阅 [使用 Compose
Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开 `compose.yml` 文件，然后添加 Compose Watch 指令。以下示例展示了如何将 Compose Watch 添加到 `compose.yml` 文件中。

```yaml {hl_lines="11-14",linenos=true}
services:
  ok-api:
    image: ok-api
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令，通过 Compose Watch 运行你的应用。

```console
$ docker compose watch
```

现在，如果你修改 `ok_api.cpp`，无需重新构建镜像即可实时看到变更。

试试看：用你喜欢的文本编辑器打开 `ok_api.cpp` 文件，把消息从 `{"Status" : "OK"}` 改为 `{"Status" : "Updated"}`。保存文件并刷新浏览器 [http://localhost:8080](http://localhost:8080)。你应该会看到更新后的消息。

在终端中按 `ctrl+c` 停止你的应用。

### 小结

在本节中，你还学习了如何使用 Compose Watch 在更新代码时自动重新构建并运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

