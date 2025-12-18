---
title: 容器化 R 应用
linkTitle: 容器化你的应用
weight: 10
keywords: R, containerize, initialize
description: 学习如何容器化 R 应用。
aliases:
  - /language/R/build-images/
  - /language/R/run-containers/
  - /language/r/containerize/
  - /guides/language/r/containerize/
---

## 前置条件

- 你已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但你可以使用任何客户端。

## 概述

本节将引导你完成容器化并运行 R 应用的步骤。

## 获取示例应用

示例应用使用了流行的 [Shiny](https://shiny.posit.co/) 框架。

克隆示例应用仓库以配合本指南使用。打开终端，切换到你想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git && cd r-docker-dev
```

现在你的 `r-docker-dev` 目录中应包含以下内容：

```text
├── r-docker-dev/
│ ├── src/
│ │ └── app.R
│ ├── src_db/
│ │ └── app_db.R
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

要了解仓库中文件的更多信息，请查看以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用

在 `r-docker-dev` 目录中，终端执行以下命令：

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3838](http://localhost:3838) 查看应用。你应该能看到一个简单的 Shiny 应用。

在终端中按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以通过添加 `-d` 选项使应用在后台运行，脱离终端控制。在 `r-docker-dev` 目录中，终端执行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:3838](http://localhost:3838) 查看应用。你应该能看到一个简单的 Shiny 应用。

在终端中执行以下命令停止应用：

```console
$ docker compose down
```

关于 Compose 命令的更多信息，请参阅 [Compose CLI 参考文档](/reference/cli/docker/compose/_index.md)。

## 小结

在本节中，你学会了如何使用 Docker 容器化并运行你的 R 应用。

相关信息：

- [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，你将学习如何使用容器开发你的应用。