---
title: 容器化 Golang 应用
linkTitle: 容器化你的应用
weight: 20
keywords: go, golang, containerize, initialize
description: 了解如何容器化 Golang 应用。
---

容器化技术可以帮助你将应用程序及其依赖项打包成一个称为容器的单一软件包。这个软件包可以在任何平台上运行，无需担心环境差异。在本节中，你将学习如何使用 Docker 容器化 Golang 应用。

要容器化 Golang 应用，首先需要创建一个 Dockerfile。Dockerfile 包含在容器中构建和运行应用程序的指令。此外，在创建 Dockerfile 时，你可以遵循不同的最佳实践来优化镜像大小并提高安全性。

## 创建 Dockerfile

在 Golang 应用的根目录中创建一个名为 `Dockerfile` 的新文件。Dockerfile 包含在容器中构建和运行应用程序的指令。

以下是一个 Golang 应用的 Dockerfile。你也可以在 `go-prometheus-monitoring` 目录中找到此文件。

```dockerfile
# 使用官方 Golang 镜像作为基础镜像
FROM golang:1.24-alpine AS builder

# 设置环境变量
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# 在容器内设置工作目录
WORKDIR /build

# 复制 go.mod 和 go.sum 文件以安装依赖
COPY go.mod go.sum ./

# 下载依赖
RUN go mod download

# 复制整个应用程序源码
COPY . .

# 构建 Go 二进制文件
RUN go build -o /app .

# 最终轻量级阶段
FROM alpine:3.21 AS final

# 从构建阶段复制编译后的二进制文件
COPY --from=builder /app /bin/app

# 暴露应用程序端口
EXPOSE 8000

# 运行应用程序
CMD ["bin/app"]
```

## 理解 Dockerfile

Dockerfile 由两个阶段组成：

1. **构建阶段**：此阶段使用官方 Golang 镜像作为基础镜像，并设置必要的环境变量。它还在容器内设置工作目录，复制 `go.mod` 和 `go.sum` 文件以安装依赖，下载依赖，复制整个应用程序源码，并构建 Go 二进制文件。

   你使用 `golang:1.24-alpine` 镜像作为构建阶段的基础镜像。`CGO_ENABLED=0` 环境变量禁用 CGO，这有助于构建静态二进制文件。你还将 `GOOS` 和 `GOARCH` 环境变量分别设置为 `linux` 和 `amd64`，以针对 Linux 平台构建二进制文件。

2. **最终阶段**：此阶段使用官方 Alpine 镜像作为基础镜像，并从构建阶段复制编译后的二进制文件。它还暴露应用程序端口并运行应用程序。

   你使用 `alpine:3.21` 镜像作为最终阶段的基础镜像。你将编译后的二进制文件从构建阶段复制到最终镜像中。你使用 `EXPOSE` 指令暴露应用程序端口，并使用 `CMD` 指令运行应用程序。

   除了多阶段构建外，Dockerfile 还遵循最佳实践，例如使用官方镜像、设置工作目录，以及仅将必要的文件复制到最终镜像中。你可以通过其他最佳实践进一步优化 Dockerfile。

## 构建 Docker 镜像并运行应用程序

有了 Dockerfile 后，你可以构建 Docker 镜像并在容器中运行应用程序。

要构建 Docker 镜像，请在终端中运行以下命令：

```console
$ docker build -t go-api:latest .
```

构建镜像后，你可以使用以下命令在容器中运行应用程序：

```console
$ docker run -p 8000:8000 go-api:latest
```

应用程序将在容器内启动，你可以在 `http://localhost:8000` 访问它。你也可以使用 `docker ps` 命令检查正在运行的容器。

```console
$ docker ps
```

## 总结

在本节中，你学习了如何使用 Dockerfile 容器化 Golang 应用。你创建了一个多阶段 Dockerfile 来在容器中构建和运行应用程序。你还了解了优化 Docker 镜像大小和提高安全性的最佳实践。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)

## 下一步

在下一节中，你将学习如何使用 Docker Compose 连接和运行多个服务，以使用 Prometheus 和 Grafana 监控 Golang 应用。