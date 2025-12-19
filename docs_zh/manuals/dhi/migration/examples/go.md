---
title: Go
description: 将 Go 应用程序迁移到 Docker Hardened Images
weight: 10
keywords: go, golang, migration, dhi
---

本示例展示了如何将 Go 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- Before (Wolfi)：使用 Wolfi 发行版镜像的 Dockerfile 示例，迁移到 DHI 之前
- Before (DOI)：使用 Docker 官方镜像的 Dockerfile 示例，迁移到 DHI 之前
- After (multi-stage)：迁移到 DHI 后使用多阶段构建的 Dockerfile 示例（推荐用于最小化、安全的镜像）
- After (single-stage)：迁移到 DHI 后使用单阶段构建的 Dockerfile 示例（更简单，但会导致镜像更大，攻击面更广）

> [!NOTE]
>
> 对于大多数用例，推荐使用多阶段构建。单阶段构建为了简化而支持，但在大小和安全性方面有所权衡。
>
> 在拉取 Docker Hardened Images 之前，您必须对 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，可以免费[创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="Before (Wolfi)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/go:latest-dev

WORKDIR /app
ADD . ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< tab name="Before (DOI)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM golang:latest

WORKDIR /app
ADD . ./

# 如果需要，使用 apt 安装其他软件包
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< tab name="After (multi-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === 构建阶段：编译 Go 应用程序 ===
FROM dhi.io/golang:1-alpine3.21-dev AS builder

WORKDIR /app
ADD . ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

# === 最终阶段：创建最小运行时镜像 ===
FROM dhi.io/golang:1-alpine3.21

WORKDIR /app
COPY --from=builder /app/main  /app/main

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< tab name="After (single-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/golang:1-alpine3.21-dev

WORKDIR /app
ADD . ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< /tabs >}}