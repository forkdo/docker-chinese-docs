---
title: 为你的 C++ 应用创建多阶段构建
linkTitle: 使用多阶段构建容器化你的应用
weight: 5
keywords: C++, 容器化, 多阶段
description: 学习如何为 C++ 应用创建多阶段构建。
aliases:
- /language/cpp/multistage/
- /guides/language/cpp/multistage/
---

## 前置条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 概述

本节将指导你为 C++ 应用创建一个多阶段 Docker 构建。
多阶段构建是 Docker 的一项功能，允许你在构建过程的不同阶段使用不同的基础镜像，
从而优化最终镜像的大小，并将构建依赖与运行时依赖分离。

对于 C++ 等编译型语言，标准实践是设置一个编译阶段来编译代码，以及一个运行阶段来运行编译后的二进制文件，
因为构建依赖在运行时并不需要。

## 获取示例应用

让我们使用一个简单的 C++ 应用，它会在终端打印 `Hello, World!`。首先，克隆示例仓库以供本指南使用：

```bash
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

本节的示例位于仓库的 `hello` 目录下。进入该目录并查看文件：

```bash
$ cd c-plus-plus-docker/hello
$ ls
```

你应该看到以下文件：

```text
Dockerfile  hello.cpp
```

## 检查 Dockerfile

在 IDE 或文本编辑器中打开 `Dockerfile`。`Dockerfile` 包含了构建 Docker 镜像的指令。

```Dockerfile
# 阶段 1：构建阶段
FROM ubuntu:latest AS build

# 安装 build-essential 以编译 C++ 代码
RUN apt-get update && apt-get install -y build-essential

# 设置工作目录
WORKDIR /app

# 将源代码复制到容器中
COPY hello.cpp .

# 静态编译 C++ 代码，确保不依赖运行时库
RUN g++ -o hello hello.cpp -static

# 阶段 2：运行阶段
FROM scratch

# 从构建阶段复制静态二进制文件
COPY --from=build /app/hello /hello

# 运行二进制文件的命令
CMD ["/hello"]
```

`Dockerfile` 包含两个阶段：

1. **构建阶段**：此阶段使用 `ubuntu:latest` 镜像来编译 C++ 代码并创建静态二进制文件。
2. **运行阶段**：此阶段使用 `scratch` 镜像（一个空镜像），从构建阶段复制静态二进制文件并运行它。

## 构建 Docker 镜像

要在 `hello` 目录中构建 Docker 镜像，请运行以下命令：

```bash
$ docker build -t hello .
```

`-t` 标志为镜像打上 `hello` 标签。

## 运行 Docker 容器

要运行 Docker 容器，请使用以下命令：

```bash
$ docker run hello
```

你应该在终端中看到输出 `Hello, World!`。

## 总结

在本节中，你学会了如何为 C++ 应用创建多阶段构建。多阶段构建帮助你优化最终镜像的大小，并将构建依赖与运行时依赖分离。
在此示例中，最终镜像仅包含静态二进制文件，不包含任何构建依赖。

由于镜像使用空的基础镜像，因此通常的系统工具也不存在。例如，你无法在容器中运行简单的 `ls` 命令：

```bash
$ docker run hello ls
```

这使得镜像非常轻量且安全。