---
title: 容器化 R 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: R, 容器化, 初始化
description: 了解如何容器化 R 应用程序。
aliases:
- /language/R/build-images/
- /language/R/run-containers/
- /language/r/容器化/
- /guides/language/r/容器化/
---

## 先决条件

- 您需要安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用的是基于命令行的 git 客户端，但您也可以使用其他任意客户端。

## 概览

本节将指导您完成 R 应用程序的容器化和运行过程。

## 获取示例应用程序

该示例应用程序使用了流行的 [Shiny](https://shiny.posit.co/) 框架。

克隆此示例应用程序以配合本指南使用。打开终端，切换到您希望工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/mfranzon/r-docker-dev.git && cd r-docker-dev
```

现在，您的 `r-docker-dev` 目录中应包含以下内容：

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

要了解仓库中文件的更多信息，请参阅以下内容：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `r-docker-dev` 目录中，于终端运行以下命令：

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:3838](http://localhost:3838) 查看应用程序。您应该会看到一个简单的 Shiny 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项让应用程序在终端后台运行。在 `r-docker-dev` 目录中，于终端运行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:3838](http://localhost:3838)。

您应该会看到一个简单的 Shiny 应用程序。

在终端中，运行以下命令停止应用程序：

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考文档](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行 R 应用程序。

相关信息：

- [Docker Compose 概览](/manuals/compose/_index.md)

## 后续步骤

在下一节中，您将学习如何使用容器开发应用程序。