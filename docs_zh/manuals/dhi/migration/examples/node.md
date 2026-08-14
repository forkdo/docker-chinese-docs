---
title: Node.js
description: 将 Node.js 应用程序迁移到 Docker 强化镜像
weight: 30
keywords: nodejs, node, migration, dhi
---

此示例展示了如何将 Node.js 应用程序迁移到 Docker 强化镜像。

以下示例展示了迁移到 Docker 强化镜像之前和之后的 Dockerfile。每个示例包含五种变体：

- **Before (Ubuntu)**：使用基于 Ubuntu 的镜像的示例 Dockerfile，迁移到 DHI 之前
- **Before (Wolfi)**：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- **Before (DOI)**：使用 Docker Official Images 的示例 Dockerfile，迁移到 DHI 之前
- **After (multi-stage)**：使用多阶段构建迁移到 DHI 后的示例 Dockerfile（推荐用于最小、安全的镜像）
- **After (single-stage)**：使用单阶段构建迁移到 DHI 后的示例 Dockerfile（更简单，但会导致镜像更大、攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建出于简单性而受支持，但在大小和安全性方面存在权衡。
>
> 您必须先对 `dhi.io` 进行身份验证，才能拉取 Docker 强化镜像。
> 使用您的 Docker ID 凭据（与您用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。

{{< tabs >}}
{{< tab name="Before (Ubuntu)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM ubuntu:24.04

RUN apt-get update && apt-get install -y nodejs npm --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD ["index.js"]
```

{{< /tab >}}
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
FROM dhi.io/node:22-alpine3.23-dev AS builder
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

# === Final stage: Create minimal runtime image ===
FROM dhi.io/node:22-alpine3.23
ENV PATH=/app/node_modules/.bin:$PATH

COPY --from=builder --chown=node:node /usr/src/app /app

WORKDIR /app

CMD ["index.js"]
```

{{< /tab >}}
{{< tab name="After (single-stage)" >}}

```dockerfile
#syntax=docker/dockerfile:1

FROM dhi.io/node:22-alpine3.23-dev
WORKDIR /usr/src/app

COPY package*.json ./

# Install any additional packages if needed using apk
# RUN apk add --no-cache python3 make g++

RUN npm install

COPY . .

CMD ["index.js"]
```

{{< /tab >}}
{{< /tabs >}}
