---
title: Node.js
description: 将 Node.js 应用迁移到 Docker Hardened Images
weight: 30
keywords: nodejs, node, migration, dhi
---

本示例演示如何将 Node.js 应用迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- Before (Wolfi)：使用 Wolfi 发行版镜像的 Dockerfile 示例，迁移到 DHI 之前
- Before (DOI)：使用 Docker 官方镜像的 Dockerfile 示例，迁移到 DHI 之前
- After (multi-stage)：迁移到 DHI 后使用多阶段构建的 Dockerfile 示例（推荐用于最小化、安全的镜像）
- After (single-stage)：迁移到 DHI 后使用单阶段构建的 Dockerfile 示例（更简单，但会导致镜像更大，攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建为简化操作而支持，但在镜像大小和安全性方面存在权衡。
>
> 在拉取 Docker Hardened Images 之前，您必须对 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="Before (Wolfi)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/node:latest-dev
WORKDIR /usr/src/app

COPY package*.json ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< tab name="Before (DOI)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM node:latest
WORKDIR /usr/src/app

COPY package*.json ./

# 如果需要，使用 apt 安装其他软件包
# RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< tab name="After (multi-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === 构建阶段：安装依赖并构建应用 ===
FROM dhi.io/node:23-alpine3.21-dev AS builder
WORKDIR /usr/src/app

COPY package*.json ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

# === 最终阶段：创建最小化运行时镜像 ===
FROM dhi.io/node:23-alpine3.21
ENV PATH=/app/node_modules/.bin:$PATH

COPY --from=builder --chown=node:node /usr/src/app /app

WORKDIR /app

CMD ["index.js"]
```

{{< /tab >}}
{{< tab name="After (single-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/node:23-alpine3.21-dev
WORKDIR /usr/src/app

COPY package*.json ./

# 如果需要，使用 apk 安装其他软件包
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< /tabs >}}