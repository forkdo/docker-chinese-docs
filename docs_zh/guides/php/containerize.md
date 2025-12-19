---
title: 容器化 PHP 应用
linkTitle: 容器化你的应用
weight: 10
keywords: php, containerize, initialize, apache, composer
description: 了解如何容器化 PHP 应用。
aliases:
  - /language/php/containerize/
  - /guides/language/php/containerize/
---

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你拥有 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但你可以使用任意客户端。

## 概述

本节将引导你完成容器化并运行 PHP 应用的步骤。

## 获取示例应用

在本指南中，你将使用一个预构建的 PHP 应用。该应用使用 Composer 管理库依赖，并通过 Apache Web 服务器提供服务。

打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库。

```console
$ git clone https://github.com/docker/docker-php-sample
```

示例应用是一个基础的 Hello World 应用和一个在数据库中递增计数器的应用。此外，应用使用 PHPUnit 进行测试。

## 初始化 Docker 资产

现在你有了应用，可以使用 `docker init` 创建必要的 Docker 资产来容器化你的应用。在 `docker-php-sample` 目录中，于终端运行 `docker init` 命令。`docker init` 提供一些默认配置，但你需要回答几个关于你应用的问题。例如，此应用使用 PHP 8.2 版本。请参考以下 `docker init` 示例，并对你的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? PHP with Apache
? What version of PHP do you want to use? 8.2
? What's the relative directory (with a leading .) for your app? ./src
? What local port do you want to use to access your server? 9000
```

现在你的 `docker-php-sample` 目录中应包含以下内容。

```text
├── docker-php-sample/
│ ├── .git/
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ ├── README.Docker.md
│ └── README.md
```

要了解 `docker init` 添加的文件的详细信息，请参阅：

- [Dockerfile](/reference/dockerfile.md)
- [.dockerignore](/reference/dockerfile.md#dockerignore-file)
- [compose.yaml](/reference/compose-file/_index.md)

## 运行应用

在 `docker-php-sample` 目录中，于终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:9000/hello.php](http://localhost:9000/hello.php)。你应该能看到一个简单的 Hello World 应用。

在终端中，按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以添加 `-d` 选项使应用在终端外以分离模式运行。在 `docker-php-sample` 目录中，于终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:9000/hello.php](http://localhost:9000/hello.php)。你应该能看到一个简单的 Hello World 应用。

在终端中，运行以下命令停止应用。

```console
$ docker compose down
```

有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

## 小结

在本节中，你学习了如何使用 Docker 容器化并运行一个简单的 PHP 应用。

相关信息：

- [docker init 参考](/reference/cli/docker/init.md)

## 下一步

在下一节中，你将学习如何使用 Docker 容器开发你的应用。