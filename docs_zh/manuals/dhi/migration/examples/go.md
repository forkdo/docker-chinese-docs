---
title: Go
description: 将 Go 应用程序迁移到 Docker Hardened Images
weight: 10
keywords: go, golang, migration, dhi
---

本示例展示了如何将 Go 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移至 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- Before (Wolfi)：迁移前使用 Wolfi 发行版镜像的示例 Dockerfile
- Before (DOI)：迁移前使用 Docker 官方镜像的示例 Dockerfile
- After (multi-stage)：迁移后使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- After (single-stage)：迁移后使用单阶段构建的示例 Dockerfile（更简单，但会导致镜像更大、攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数场景。单阶段构建为简化而提供，但存在体积和安全性的权衡。
>
> 在拉取 Docker Hardened Images 之前，您必须对 `dhi.io` 进行身份验证。使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果您没有 Docker 账户，请[免费注册](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="Before (Wolfi)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/go:latest-dev

WORKDIR /app
ADD . ./

# 如需安装其他包，请使用 apk
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

# 如需安装其他包，请使用 apt
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

# 如需安装其他包，请使用 apk
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

# 如需安装其他包，请使用 apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

{{< /tab >}}
{{< /tabs >}}
