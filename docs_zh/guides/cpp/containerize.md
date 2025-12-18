---
title: 容器化 C++ 应用
linkTitle: 使用 Docker Compose 构建和运行 C++ 应用
weight: 10
keywords: C++, 容器化, 初始化
description: 了解如何使用 Docker Compose 构建和运行 C++ 应用。
aliases:
  - /language/cpp/containerize/
  - /guides/language/cpp/containerize/
---

## 前置条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你也可以使用任意客户端。

## 概述

本节将指导你如何使用 Docker Compose 容器化并运行一个 C++ 应用。

## 获取示例应用

我们使用与本指南前面章节相同的示例仓库。如果你尚未克隆该仓库，请先克隆：

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

现在，你的 `c-plus-plus-docker`（根）目录中应包含以下内容：

```text
├── c-plus-plus-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── ok_api.cpp
│ └── README.md

```

要了解仓库中文件的详细信息，请参阅：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yml](/reference/compose-file/_index.md)

## 运行应用

在 `c-plus-plus-docker` 目录中，终端执行以下命令：

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:8080](http://localhost:8080)。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以通过添加 `-d` 选项，使应用在后台脱离终端运行。在 `c-plus-plus-docker` 目录中，终端执行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:8080](http://localhost:8080)。

在终端中执行以下命令停止应用：

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考文档](/reference/cli/docker/compose/_index.md)。

## 小结

在本节中，你学会了如何使用 Docker 容器化并运行 C++ 应用。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将学习如何使用容器开发应用。