---
title: Node.js
description: 将 Node.js 应用程序迁移到 Docker Hardened Images
weight: 30
keywords: nodejs, node, migration, dhi
---

本示例展示了如何将 Node.js 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- 迁移前（Wolfi）：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移前状态
- 迁移前（DOI）：使用 Docker 官方镜像的示例 Dockerfile，迁移前状态
- 迁移后（多阶段）：使用多阶段构建迁移到 DHI 的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后（单阶段）：使用单阶段构建迁移到 DHI 的示例 Dockerfile（更简单但会产生更大的镜像和更广的攻击面）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建为简化而提供，但会在大小和安全性方面有所权衡。
>
> 在拉取 Docker Hardened Images 之前，必须先对 `dhi.io` 进行身份验证。使用你的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果你没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="Before (Wolfi)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM cgr.dev/chainguard/node:latest-dev
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
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

# Install any additional packages if needed using apt
# RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< tab name="After (multi-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

# === Build stage: Install dependencies and build application ===
FROM dhi.io/node:23-alpine3.21-dev AS builder
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

# === Final stage: Create minimal runtime image ===
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

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["node", "index.js"]
```

{{< /tab >}}
{{< /tabs >}}