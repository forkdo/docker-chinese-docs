# Go


本示例展示了如何将 Go 应用程序迁移到 Docker 强化镜像。

以下示例展示了迁移到 Docker 强化镜像前后的 Dockerfile。每个示例包含五个变体：

- 迁移前（Ubuntu）：使用基于 Ubuntu 的镜像的示例 Dockerfile，在迁移到 DHI 之前
- 迁移前（Wolfi）：使用 Wolfi 发行版镜像的示例 Dockerfile，在迁移到 DHI 之前
- 迁移前（DOI）：使用 Docker 官方镜像的示例 Dockerfile，在迁移到 DHI 之前
- 迁移后（多阶段）：迁移到 DHI 并使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后（单阶段）：迁移到 DHI 并使用单阶段构建的示例 Dockerfile（更简单，但生成的镜像更大，攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建支持简化操作，但在大小和安全性方面存在权衡。
>
> 在拉取 Docker 强化镜像之前，您必须向 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与您在 Docker Hub 上使用的用户名和密码相同）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

**Before (Ubuntu)**



```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu/go:1.22-24.04

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

**Before (Wolfi)**



```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/go:latest-dev

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

**Before (DOI)**



```dockerfile
#syntax=docker/dockerfile:1

FROM golang:latest

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```

**After (multi-stage)**



```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Compile Go application ===
FROM dhi.io/golang:1.25-alpine3.23-dev AS builder

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

# === Final stage: Create minimal runtime image ===
FROM dhi.io/golang:1.25-alpine3.23

WORKDIR /app
COPY --from=builder /app/main  /app/main

ENTRYPOINT ["/app/main"]
```

**After (single-stage)**



```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/golang:1.25-alpine3.23-dev

WORKDIR /app
ADD . ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache git

RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" --installsuffix cgo -o main .

ENTRYPOINT ["/app/main"]
```



