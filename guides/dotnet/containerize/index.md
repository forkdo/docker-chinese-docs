# 容器化 .NET 应用程序

## 先决条件

* 您已安装最新版本的 [Docker
  Desktop](/get-started/get-docker.md)。
* 您拥有 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

## 概述

本节将引导您完成容器化和运行 .NET 应用程序的过程。

## 获取示例应用程序

在本指南中，您将使用一个预先构建的 .NET 应用程序。该应用程序类似于 Docker 博客文章 [使用 Docker Desktop 构建多容器 .NET 应用](https://www.docker.com/blog/building-multi-container-net-app-using-docker-desktop/) 中构建的应用程序。

打开终端，切换到您想要工作的目录，然后运行以下命令克隆仓库。

```console
$ git clone https://github.com/docker/docker-dotnet-sample
```

## 初始化 Docker 资产

现在您有了一个应用程序，可以使用 `docker init` 创建容器化应用程序所需的 Docker 资产。在 `docker-dotnet-sample` 目录中，在终端中运行 `docker init` 命令。`docker init` 提供了一些默认配置，但您需要回答一些关于您的应用程序的问题。参考以下示例来回答 `docker init` 的提示，并为您的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? ASP.NET Core
? What's the name of your solution's main project? myWebApp
? What version of .NET do you want to use? 8.0
? What local port do you want to use to access your server? 8080
```

现在，您的 `docker-dotnet-sample` 目录中应该包含以下内容。

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

要了解更多关于 `docker init` 添加的文件的信息，请参阅以下内容：
 - [Dockerfile](/reference/dockerfile.md)
 - [.dockerignore](/reference/dockerfile.md#dockerignore-file)
 - [compose.yaml](/reference/compose-file/_index.md)

## 运行应用程序

在 `docker-dotnet-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到一个简单的 Web 应用程序。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端后台运行应用程序。在 `docker-dotnet-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到一个简单的 Web 应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 总结

在本节中，您学习了如何使用 Docker 容器化和运行 .NET 应用程序。

相关信息：
 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件参考](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)

## 下一步

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序。
