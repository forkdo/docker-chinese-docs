# 容器化一个 Golang 应用

容器化可以帮助你将应用及其依赖打包到一个称为容器的单一包中。该包可以在任何平台上运行，而无需担心环境问题。在本节中，你将学习如何使用 Docker 容器化一个 Golang 应用。

要容器化一个 Golang 应用，你首先需要创建一个 Dockerfile。Dockerfile 包含在容器中构建和运行应用的指令。此外，在创建 Dockerfile 时，你可以遵循不同的最佳实践来优化镜像大小并增强安全性。

## 创建 Dockerfile

在你的 Golang 应用根目录中创建一个名为 `Dockerfile` 的新文件。Dockerfile 包含在容器中构建和运行应用的指令。

以下是一个用于 Golang 应用的 Dockerfile。你也可以在 `go-prometheus-monitoring` 目录中找到此文件。

```dockerfile
# Use the official Golang image as the base
FROM golang:1.24-alpine AS builder

# Set environment variables
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Set working directory inside the container
WORKDIR /build

# Copy go.mod and go.sum files for dependency installation
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the entire application source
COPY . .

# Build the Go binary
RUN go build -o /app .

# Final lightweight stage
FROM alpine:3.21 AS final

# Copy the compiled binary from the builder stage
COPY --from=builder /app /bin/app

# Expose the application's port
EXPOSE 8000

# Run the application
CMD ["bin/app"]
```

## 理解 Dockerfile

该 Dockerfile 包含两个阶段：

1.  **构建阶段**：此阶段使用官方的 Golang 镜像作为基础，并设置必要的环境变量。它还会在容器内设置工作目录，复制 `go.mod` 和 `go.sum` 文件以安装依赖项，下载依赖项，复制整个应用源代码，并构建 Go 二进制文件。

    你使用 `golang:1.24-alpine` 镜像作为构建阶段的基础镜像。`CGO_ENABLED=0` 环境变量禁用了 CGO，这对于构建静态二进制文件非常有用。你还将 `GOOS` 和 `GOARCH` 环境变量分别设置为 `linux` 和 `amd64`，以为 Linux 平台构建二进制文件。

2.  **最终阶段**：此阶段使用官方的 Alpine 镜像作为基础，并从构建阶段复制编译好的二进制文件。它还会暴露应用的端口并运行应用。

    你使用 `alpine:3.21` 镜像作为最终阶段的基础镜像。你将编译好的二进制文件从构建阶段复制到最终镜像中。你使用 `EXPOSE` 指令暴露应用的端口，并使用 `CMD` 指令运行应用。

    除了多阶段构建之外，该 Dockerfile 也遵循了诸如使用官方镜像、设置工作目录以及仅将必要文件复制到最终镜像等最佳实践。你也可以通过其他最佳实践来进一步优化 Dockerfile。

## 构建 Docker 镜像并运行应用

一旦你有了 Dockerfile，就可以构建 Docker 镜像并在容器中运行应用。

要构建 Docker 镜像，请在终端中运行以下命令：

```console
$ docker build -t go-api:latest .
```

构建镜像后，你可以使用以下命令在容器中运行应用：

```console
$ docker run -p 8000:8000 go-api:latest
```

应用将开始在容器内运行，你可以通过 `http://localhost:8000` 访问它。你也可以使用 `docker ps` 命令检查正在运行的容器。

```console
$ docker ps
```

## 小结

在本节中，你学习了如何使用 Dockerfile 容器化一个 Golang 应用。你创建了一个多阶段的 Dockerfile 来在容器中构建和运行应用。你还学习了用于优化 Docker 镜像大小并增强安全性的最佳实践。

相关信息：

 - [Dockerfile 参考](/reference/dockerfile.md)
 - [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)

## 后续步骤

在下一节中，你将学习如何使用 Docker Compose 连接并运行多个服务，以使用 Prometheus 和 Grafana 监控 Golang 应用。
