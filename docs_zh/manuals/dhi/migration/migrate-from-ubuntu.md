---
title: 从 Ubuntu 迁移
description: 从基于 Ubuntu 的镜像迁移到 Docker Hardened Images 的分步指南
weight: 25
keywords: ubuntu, 迁移, dhi, debian, docker hardened images
---

Docker Hardened Images (DHI) 提供 [Alpine-based 和 Debian-based
variants](../explore/available.md)。当从基于 Ubuntu 的镜像迁移时，
你应该迁移到基于 Debian 的 DHI 变体，因为 Ubuntu 和 Debian
共享相同的包管理系统 (APT) 和底层架构，
使迁移变得简单。

本指南帮助你从现有的基于 Ubuntu 的镜像迁移到 DHI。

## 主要差异

当从基于 Ubuntu 的镜像迁移到 DHI Debian 时，请注意这些主要差异：

| 项目               | 基于 Ubuntu 的镜像                                                                                                                                                                                                                                                                                                         | Docker Hardened Images                                                                                                                                                                                                                                                                                                         |
|:-------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 包管理 | 因镜像而异。有些包含 APT 包管理器，有些则没有                                                                                                                                                                                                  | 包管理器通常只在带有 `dev` 标签的镜像中可用。运行时镜像不包含包管理器。使用多阶段构建并将必要的构件从构建阶段复制到运行时阶段。                                                                  |
| 非 root 用户      | 因镜像而异。有些以 root 身份运行，有些则以非 root 身份运行                                                                                                                                                                                                                                                                                                | 运行时变体默认以非 root 用户身份运行。确保必要的文件和目录对非 root 用户可访问。                                                                                                                                                                                                          |
| 多阶段构建  | 推荐使用                                                                                                                                                                                                                                                                                                                       | 推荐使用。在构建阶段使用带有 `dev` 或 `sdk` 标签的镜像，在运行时使用非 dev 镜像。                                                                                                                                                                                                                           |
| 端口              | 以 root 身份运行时可以绑定到特权端口（低于 1024）                                                                                                                                                                                                                                                                 | 默认以非 root 用户身份运行。在 Kubernetes 或低于 20.10 版本的 Docker Engine 中运行时，应用程序无法绑定到特权端口（低于 1024）。将你的应用程序配置为在容器内监听 1025 及以上的端口。                                                                        |
| 入口点        | 因镜像而异                                                                                                                                                                                                                                                                                                                | 可能与基于 Ubuntu 的镜像有不同的入口点。检查入口点并在必要时更新你的 Dockerfile。                                                                                                                                                                                                    |
| Shell              | 因镜像而异。有些包含 shell，有些则没有                                                                                                                                                                                                                                                                                                  | 运行时镜像不包含 shell。在构建阶段使用 `dev` 镜像来运行 shell 命令，然后将构件复制到运行时阶段。                                                                                                                                                                                      |
| 包仓库 | 使用 Ubuntu 包仓库                                                                                                                                                                                                                                                                                                  | 使用 Debian 包仓库。大多数包具有相似的名称，但有些可能不同。                                                                                                                                                                                      |

## 迁移步骤

### 步骤 1：更新 Dockerfile 中的基础镜像

将应用程序 Dockerfile 中的基础镜像更新为加固镜像。这
通常将是标记为 `dev` 或 `sdk` 的镜像，因为它具有
安装包和依赖项所需的工具。

以下来自 Dockerfile 的示例差异片段显示了旧的基于 Ubuntu 的镜像
被新的 DHI Debian 镜像替换。

> [!NOTE]
>
> 在可以拉取 Docker Hardened Images 之前，你必须对 `dhi.io` 进行身份验证。
> 使用你的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果你没有 Docker 账户，[创建
> 一个](../../accounts/create-account.md) 免费账户。
>
> 运行 `docker login dhi.io` 进行身份验证。


```diff
- ## Original Ubuntu-based image
- FROM ubuntu/go:1.22-24.04

+ ## Updated to use hardened Debian-based image
+ FROM dhi.io/golang:1-debian13-dev
```

要找到正确的标签，请在 [DHI
Catalog](https://hub.docker.com/hardened-images/catalog/) 中探索可用的标签。

### 步骤 2：更新包安装命令

由于 Ubuntu 和 Debian 都使用 APT 进行包管理，大多数包
安装命令保持相似。但是，你需要确保包
安装仅在 `dev` 或 `sdk` 镜像中发生，因为运行时镜像不
包含包管理器。

```diff
- ## Ubuntu: Installing packages
- FROM ubuntu/go:1.22-24.04
- RUN apt-get update && apt-get install -y \
-     git \
-     && rm -rf /var/lib/apt/lists/*

+ ## DHI: Use a language-specific dev image with package manager
+ FROM dhi.io/golang:1-debian13-dev
+ RUN apt-get update && apt-get install -y \
+     git \
+     && rm -rf /var/lib/apt/lists/*
```

大多数 Ubuntu 包在 Debian 中以相同名称提供。如果你
遇到缺失的包，可以使用
[Debian package search](https://packages.debian.org/) 网站搜索等效包。

### 步骤 3：更新 Dockerfile 中的运行时镜像

> [!NOTE]
>
> 建议使用多阶段构建以保持最终镜像最小化和
> 安全。支持单阶段构建，但它们包含完整的 `dev` 镜像
> 因此导致更大的镜像和更广泛的攻击面。

为确保最终镜像尽可能最小化，你应该使用
[multi-stage build](/manuals/build/building/multi-stage.md)。你
Dockerfile 中的所有阶段都应使用加固镜像。虽然中间阶段通常
将使用标记为 `dev` 或 `sdk` 的镜像，但你的最终运行时阶段应使用运行时镜像。

利用构建阶段安装依赖项并准备你的应用程序，
然后将生成的构件复制到最终运行时阶段。这确保了
你的最终镜像是最小化和安全的。

以下示例显示了从 Ubuntu 迁移到 DHI Debian 的多阶段 Dockerfile：

```dockerfile
# Build stage
FROM dhi.io/golang:1-debian13-dev AS builder
WORKDIR /app

# Install system dependencies (only available in dev images)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags="-s -w" -o main .

# Runtime stage
FROM dhi.io/golang:1-debian13
WORKDIR /app

# Copy compiled binary from builder
COPY --from=builder /app/main /app/main

# Run the application
ENTRYPOINT ["/app/main"]
```

## 语言特定示例

请参阅示例部分以获取语言特定的迁移示例：

- [Go](examples/go.md)
- [Python](examples/python.md)
- [Node.js](examples/node.md)