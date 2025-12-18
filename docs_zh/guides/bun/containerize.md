---
title: 容器化 Bun 应用
linkTitle: 容器化你的应用
weight: 10
keywords: bun, containerize, initialize
description: 了解如何容器化一个 Bun 应用。
aliases:
  - /language/bun/containerize/
---

## 前置条件

* 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任意客户端。

## 概述

长期以来，Node.js 一直是服务端 JavaScript 应用的事实运行时。近年来，生态系统中涌现出多种新的替代运行时，包括 [Bun 官网](https://bun.sh/)。与 Node.js 一样，Bun 也是一种 JavaScript 运行时。Bun 是一个相对轻量级的运行时，设计目标是快速高效。

为什么使用 Docker 开发 Bun 应用？可选的运行时越多越好，但随着运行时数量的增加，跨环境一致地管理不同运行时及其依赖变得困难。Docker 正好解决了这个问题。按需创建和销毁容器是管理不同运行时及其依赖的有效方式。此外，作为一个较新的运行时，为 Bun 搭建一致的开发环境可能具有挑战性，而 Docker 可以帮助你建立一致的 Bun 开发环境。

## 获取示例应用

克隆示例应用以配合本指南使用。打开终端，切换到你想工作的目录，运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

此时，你的 `bun-docker` 目录中应包含以下内容：

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

## 创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Bun Docker 官方镜像](https://hub.docker.com/r/oven/bun)，也可以使用 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 中的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它提供了可用于生产的轻量级且安全的镜像。更多信息，请参见 [Docker Hardened Images](https://docs.docker.com/dhi/)。

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images (DHIs) 在 [Docker Hub](https://hub.docker.com/hardened-images/catalog/dhi/bun) 上为 Bun 提供了镜像。与使用 Docker 官方镜像不同，你必须先将 Bun 镜像镜像到你的组织中，然后将其用作基础镜像。请按照 [DHI 快速入门](/dhi/get-started/) 中的说明为 Bun 创建镜像仓库。

镜像仓库名称必须以 `dhi-` 开头，例如：`FROM <your-namespace>/dhi-bun:<tag>`。在以下 Dockerfile 中，`FROM` 指令使用 `<your-namespace>/dhi-bun:1` 作为基础镜像。

```dockerfile
# 使用 DHI Bun 镜像作为基础镜像
FROM <your-namespace>/dhi-bun:1

# 在容器中设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的 /app 目录
COPY . .

# 暴露 API 监听的端口
EXPOSE 3000

# 启动容器时运行服务器
CMD ["bun", "server.js"]
```

{{< /tab >}}
{{< tab name="使用官方镜像" >}}

使用 Docker 官方镜像非常直接。在以下 Dockerfile 中，你会注意到 `FROM` 指令使用 `oven/bun` 作为基础镜像。

你可以在 [Docker Hub](https://hub.docker.com/r/oven/bun) 上找到该镜像。这是由 Oven（Bun 背后的公司）创建的 Bun 官方 Docker 镜像，可在 Docker Hub 上获取。

```dockerfile
# 使用官方 Bun 镜像
FROM oven/bun:latest

# 在容器中设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的 /app 目录
COPY . .

# 暴露 API 监听的端口
EXPOSE 3000

# 启动容器时运行服务器
CMD ["bun", "server.js"]
```

{{< /tab >}}
{{< /tabs >}}

除了指定基础镜像外，Dockerfile 还：

- 将容器中的工作目录设置为 `/app`。
- 将当前目录内容复制到容器中的 `/app` 目录。
- 暴露端口 3000，API 在此监听请求。
- 最后，在容器启动时使用命令 `bun server.js` 运行服务器。

## 运行应用

在 `bun-docker` 目录中，终端执行以下命令：

```console
$ docker compose up --build
```

打开浏览器，访问 [http://localhost:3000](http://localhost:3000)。你将在浏览器中看到消息 `{"Status" : "OK"}`。

在终端中，按 `ctrl`+`c` 停止应用。

### 在后台运行应用

你可以通过添加 `-d` 选项使应用在后台运行，与终端分离。在 `bun-docker` 目录中，终端执行以下命令：

```console
$ docker compose up --build -d
```

打开浏览器，访问 [http://localhost:3000](http://localhost:3000)。

在终端中，执行以下命令停止应用：

```console
$ docker compose down
```

## 小结

在本节中，你学会了如何使用 Docker 容器化并运行你的 Bun 应用。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)
 - [Docker Hardened Images](/dhi/)

## 后续步骤

在下一节中，你将学习如何使用容器开发你的应用。