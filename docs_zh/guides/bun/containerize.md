---
title: 容器化 Bun 应用程序
linkTitle: 容器化您的应用
weight: 10
keywords: bun, containerize, initialize
description: 了解如何容器化 Bun 应用程序。
aliases:
  - /language/bun/containerize/
---

## 先决条件

* 您拥有 [Git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 概述

长期以来，Node.js 一直是服务器端 JavaScript 应用程序的事实标准运行时。近年来，生态系统中出现了许多新的替代运行时，包括 [Bun 网站](https://bun.sh/)。与 Node.js 一样，Bun 是一个 JavaScript 运行时。Bun 是一个相对轻量级的运行时，旨在快速且高效。

为什么使用 Docker 开发 Bun 应用程序？拥有多种运行时可供选择固然很棒。但随着运行时数量的增加，在不同环境中一致地管理不同的运行时及其依赖项变得具有挑战性。这正是 Docker 的用武之地。按需创建和销毁容器是管理不同运行时及其依赖项的绝佳方式。此外，由于它是一个相当新的运行时，为 Bun 建立一致的开发环境可能具有挑战性。Docker 可以帮助您为 Bun 建立一致的开发环境。

## 获取示例应用程序

克隆示例应用程序以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆存储库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

现在，您的 `bun-docker` 目录中应包含以下内容。

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

## 创建 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Bun Docker 官方镜像](https://hub.docker.com/r/oven/bun) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它提供了生产就绪、轻量级且安全的镜像。更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}

Docker Hardened Images (DHIs) 可在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/bun) 中找到。您可以直接从 `dhi.io` 注册表拉取 DHIs。

1. 登录 DHI 注册表：
   ```console
   $ docker login dhi.io
   ```

2. 将 Bun DHI 拉取为 `dhi.io/bun:1`。此示例中的标签 (`1`) 指的是 Bun 的最新 1.x 版本。

   ```console
   $ docker pull dhi.io/bun:1
   ```

有关其他可用版本，请参阅 [目录](https://hub.docker.com/hardened-images/catalog/dhi/bun)。

```dockerfile
# 使用 DHI Bun 镜像作为基础镜像
FROM dhi.io/bun:1

# 设置容器中的工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app
COPY . .

# 暴露 API 将监听的端口
EXPOSE 3000

# 在容器启动时运行服务器
CMD ["bun", "server.js"]
```

{{< /tab >}}
{{< tab name="使用官方镜像" >}}

使用 Docker 官方镜像非常简单。在下面的 Dockerfile 中，您会注意到 `FROM` 指令使用 `oven/bun` 作为基础镜像。

您可以在 [Docker Hub](https://hub.docker.com/r/oven/bun) 上找到该镜像。这是由 Bun 背后的公司 Oven 创建的 Bun 的 Docker 官方镜像，并且可在 Docker Hub 上使用。

```dockerfile
# 使用官方的 Bun 镜像
FROM oven/bun:latest

# 设置容器中的工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app
COPY . .

# 暴露 API 将监听的端口
EXPOSE 3000

# 在容器启动时运行服务器
CMD ["bun", "server.js"]
```

{{< /tab >}}
{{< /tabs >}}

除了指定基础镜像之外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将当前目录的内容复制到容器中的 `/app` 目录。
- 暴露 API 正在监听请求的端口 3000。
- 最后，在容器启动时使用命令 `bun server.js` 启动服务器。

## 运行应用程序

在 `bun-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。您将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端后台运行应用程序。在 `bun-docker` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:3000](http://localhost:3000) 查看应用程序。

在终端中，运行以下命令停止应用程序。

```console
$ docker compose down
```

## 总结

在本节中，您学习了如何使用 Docker 容器化并运行您的 Bun 应用程序。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 下一步

在下一节中，您将学习如何使用容器开发您的应用程序。