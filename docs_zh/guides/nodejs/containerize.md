---
title: 容器化 Node.js 应用
linkTitle: 容器化
weight: 10
keywords: node.js, node, containerize, initialize
description: 了解如何使用 Docker 容器化 Node.js 应用，通过创建优化的、生产就绪的镜像，并遵循性能、安全性和可扩展性的最佳实践。
aliases:
- /get-started/nodejs/build-images/
- /language/nodejs/build-images/
- /language/nodejs/run-containers/
- /language/nodejs/containerize/
- /guides/language/nodejs/containerize/
---

## 前提条件

在开始之前，请确保您的系统上已安装并可用以下工具：

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **初次接触 Docker？**  
> 请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 Node.js 应用的完整过程。您将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提升性能、安全性、可扩展性和操作效率。

本指南结束时，您将能够：

- 使用 Docker 容器化 Node.js 应用。
- 创建并优化专为 Node.js 环境定制的 Dockerfile。
- 使用多阶段构建来分离依赖项并减小镜像体积。
- 配置容器使用非 root 用户，以实现安全、高效的运行时环境。
- 遵循最佳实践构建安全、轻量且易于维护的 Docker 镜像。

## 获取示例应用

克隆示例应用以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-nodejs-sample
```

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助您为容器化应用搭建必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到项目目录的根目录：

```console
$ cd docker-nodejs-sample
```

然后运行以下命令：

```console
$ docker init
```

您将看到类似以下的输出：

```text
Welcome to the Docker Init CLI

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

CLI 会提示您回答一些关于应用设置的问题。
为保持一致性，请在提示时使用与下表相同的回答：
| 问题 | 回答 |
|------------------------------------------------------------|-----------------|
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 24.11.1-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run dev |
| What port does your server listen on? | 3000 |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

## 创建 Docker Compose 文件

虽然 `docker init` 生成了一个基本的 `compose.yaml` 文件，但您需要为此全栈应用创建一个更全面的配置。请用生产就绪的配置替换生成的 `compose.yaml`。

在项目根目录中创建一个名为 `compose.yml` 的新文件：

```yaml
# ========================================
# Docker Compose 配置
# 现代 Node.js Todo 应用
# ========================================

services:
  # ========================================
  # 开发服务
  # ========================================
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: todoapp-dev
    ports:
      - '${APP_PORT:-3000}:3000' # API 服务器
      - '${VITE_PORT:-5173}:5173' # Vite 开发服务器
      - '${DEBUG_PORT:-9229}:9229' # Node.js 调试器
    environment:
      NODE_ENV: development
      DOCKER_ENV: 'true'
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
      ALLOWED_ORIGINS: '${ALLOWED_ORIGINS:-http://localhost:3000,http://localhost:5173}'
    volumes:
      - ./src:/app/src:ro
      - ./package.json:/app/package.json
      - ./vite.config.ts:/app/vite.config.ts:ro
      - ./tailwind.config.js:/app/tailwind.config.js:ro
      - ./postcss.config.js:/app/postcss.config.js:ro
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - '**/*.test.*'
            - '**/__tests__/**'
        - action: rebuild
          path: ./package.json
        - action: sync
          path: ./vite.config.ts
          target: /app/vite.config.ts
        - action: sync
          path: ./tailwind.config.js
          target: /app/tailwind.config.js
        - action: sync
          path: ./postcss.config.js
          target: /app/postcss.config.js
    restart: unless-stopped
    networks:
      - todoapp-network

  # ========================================
  # 生产服务
  # ========================================
  app-prod:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    container_name: todoapp-prod
    ports:
      - '${PROD_PORT:-8080}:3000'
    environment:
      NODE_ENV: production
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
      ALLOWED_ORIGINS: '${ALLOWED_ORIGINS:-https://yourdomain.com}'
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: '${PROD_MEMORY_LIMIT:-2G}'
          cpus: '${PROD_CPU_LIMIT:-1.0}'
        reservations:
          memory: '${PROD_MEMORY_RESERVATION:-512M}'
          cpus: '${PROD_CPU_RESERVATION:-0.25}'
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - todoapp-network
    profiles:
      - prod

  # ========================================
  # PostgreSQL 数据库服务
  # ========================================
  db:
    image: postgres:18-alpine
    container_name: todoapp-db
    environment:
      POSTGRES_DB: '${POSTGRES_DB:-todoapp}'
      POSTGRES_USER: '${POSTGRES_USER:-todoapp}'
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - '${DB_PORT:-5432}:5432'
    restart: unless-stopped
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER:-todoapp} -d ${POSTGRES_DB:-todoapp}']
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 5s
    networks:
      - todoapp-network

# ========================================
# 卷配置
# ========================================
volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

# ========================================
# 网络配置
# ========================================
networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

此 Docker Compose 配置包括：

- **开发服务** (`app-dev`): 包含热重载、调试支持和绑定挂载的完整开发环境
- **生产服务** (`app-prod`): 优化的生产部署，包含资源限制和安全加固
- **数据库服务** (`db`): PostgreSQL 18，带有持久化存储和健康检查
- **网络**: 用于安全服务通信的隔离网络
- **卷**: 用于数据库数据的持久化存储

## 创建环境配置

创建一个 `.env` 文件来配置您的应用设置：

```console
$ cp .env.example .env
```

使用您首选的设置更新 `.env` 文件：

```env
# 应用配置
NODE_ENV=development
APP_PORT=3000
VITE_PORT=5173
DEBUG_PORT=9229

# 生产配置
PROD_PORT=8080
PROD_MEMORY_LIMIT=2G
PROD_CPU_LIMIT=1.0
PROD_MEMORY_RESERVATION=512M
PROD_CPU_RESERVATION=0.25

# 数据库配置
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=todoapp
POSTGRES_USER=todoapp
POSTGRES_PASSWORD=todoapp_password
DB_PORT=5432

# 安全配置
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 为标准 Node.js 应用提供了可靠的基础。然而，由于此项目是一个包含后端 API 和前端 React 组件的全栈 TypeScript 应用，因此应自定义 Dockerfile 以更好地支持和优化此特定架构。

### 查看生成的文件

在接下来的步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建以保持最终镜像干净且体积小
- 仅包含所需内容以提高性能和安全性

这些更新使您的应用更易于部署且加载速度更快。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的分步说明。它会自动打包您的应用程序及其依赖项和运行时环境。
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 1：配置 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它提供了生产就绪、轻量且安全的镜像。有关更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用了一个稳定的 Node.js LTS 镜像标签，该标签在编写本指南时被认为是安全的。由于会定期发布新版本和安全补丁，当您遵循本指南时，此处显示的标签可能不再是安全选项。在构建或部署应用程序之前，请务必查看最新的可用镜像标签，并选择安全、最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images (DHIs) 可在 [Docker Hub](https://hub.docker.com/hardened-images/catalog/dhi/node) 上用于 Node.js。与使用 Docker 官方镜像不同，您必须首先将 Node.js 镜像镜像到您的组织中，然后将其用作基础镜像。请按照 [DHI 快速入门](/dhi/get-started/) 中的说明为 Node.js 创建镜像仓库。

镜像仓库必须以 `dhi-` 开头，例如：`FROM <your-namespace>/dhi-node:<tag>`。在下面的 Dockerfile 中，`FROM` 指令使用 `<your-namespace>/dhi-node:24-alpine3.22-dev` 作为基础镜像。

```dockerfile
# ========================================
# 优化的多阶段 Dockerfile
# Node.js TypeScript 应用 (使用 DHI)
# ========================================

FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS base

# 设置工作目录
WORKDIR /app

# 创建非 root 用户以提高安全性
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# 依赖阶段
# ========================================
FROM base AS deps

# 复制包文件
COPY package*.json ./

# 安装生产依赖项
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# 设置正确的所有权
RUN chown -R nodejs:nodejs /app

# ========================================
# 构建依赖阶段
# ========================================
FROM base AS build-deps

# 复制包文件
COPY package*.json ./

# 安装所有依赖项并进行构建优化
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# 创建必要的目录并设置权限
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# 构建阶段
# ========================================
FROM build-deps AS build

# 仅复制构建所需的文件（遵循 .dockerignore）
COPY --chown=nodejs:nodejs . .

# 构建应用程序
RUN npm run build

# 设置正确的所有权
RUN chown -R nodejs:nodejs /app

# ========================================
# 开发阶段
# ========================================
FROM build-deps AS development

# 设置环境
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# 复制源文件
COPY . .

# 确保所有目录具有正确的权限
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# 切换到非 root 用户
USER nodejs

# 暴露端口
EXPOSE 3000 5173 9229

# 启动开发服务器
CMD ["npm", "run", "dev:docker"]

# ========================================
# 生产阶段
# ========================================
FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS production

# 设置工作目录
WORKDIR /app

# 创建非 root 用户以提高安全性
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# 设置优化的环境变量
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# 从 deps 阶段复制生产依赖项
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# 从 build 阶段复制构建好的应用程序
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# 切换到非 root 用户以提高安全性
USER nodejs

# 暴露端口
EXPOSE 3000

# 启动生产服务器
CMD ["node", "dist/server.js"]

# ========================================
# 测试阶段
# ========================================
FROM build-deps AS test

# 设置环境
ENV NODE_ENV=test \
    CI=true

# 复制源文件
COPY --chown=nodejs:nodejs . .

# 切换到非 root 用户
USER nodejs

# 运行带覆盖率的测试
CMD ["npm", "run", "test:coverage"]
```

{{< /tab >}}
{{< tab name="使用 Docker 官方镜像" >}}

现在您需要创建一个生产就绪的多阶段 Dockerfile。用以下优化配置替换生成的 Dockerfile：

```dockerfile
# ========================================
# 优化的多阶段 Dockerfile
# Node.js TypeScript 应用
# ========================================

ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS base

# 设置工作目录
WORKDIR /app

# 创建非 root 用户以提高安全性
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# 依赖阶段
# ========================================
FROM base AS deps

# 复制包文件
COPY package*.json ./

# 安装生产依赖项
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# 设置正确的所有权
RUN chown -R nodejs:nodejs /app

# ========================================
# 构建依赖阶段
# ========================================
FROM base AS build-deps

# 复制包文件
COPY package*.json ./

# 安装所有依赖项并进行构建优化
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# 创建必要的目录并设置权限
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# 构建阶段
# ========================================
FROM build-deps AS build

# 仅复制构建所需的文件（遵循 .dockerignore）
COPY --chown=nodejs:nodejs . .

# 构建应用程序
RUN npm run build

# 设置正确的所有权
RUN chown -R nodejs:nodejs /app

# ========================================
# 开发阶段
# ========================================
FROM build-deps AS development

# 设置环境
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# 复制源文件
COPY . .

# 确保所有目录具有正确的权限
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# 切换到非 root 用户
USER nodejs

# 暴露端口
EXPOSE 3000 5173 9229

# 启动开发服务器
CMD ["npm", "run", "dev:docker"]

# ========================================
# 生产阶段
# ========================================
ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS production

# 设置工作目录
WORKDIR /app

# 创建非 root 用户以提高安全性
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# 设置优化的环境变量
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# 从 deps 阶段复制生产依赖项
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# 从 build 阶段复制构建好的应用程序
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# 切换到非 root 用户以提高安全性
USER nodejs

# 暴露端口
EXPOSE 3000

# 启动生产服务器
CMD ["node", "dist/server.js"]

# ========================================
# 测试阶段
# ========================================
FROM build-deps AS test

# 设置环境
ENV NODE_ENV=test \
    CI=true

# 复制源文件
COPY --chown=nodejs:nodejs . .

# 切换到非 root 用户
USER nodejs

# 运行带覆盖率的测试
CMD ["npm", "run", "test:coverage"]
```
{{< /tab >}}

{{< /tabs >}}

此 Dockerfile 的主要特点：
- **多阶段结构** — 为依赖项、构建、开发、生产、测试分离阶段，保持每个阶段的干净和高效。
- **精简的生产镜像** — 优化的分层减少了体积，并仅保留运行应用所需的内容。
- **安全导向的设置** — 使用专用的非 root 用户，并排除不必要的包。
- **性能友好的设计** — 有效利用缓存和结构良好的层，实现更快的构建。
- **干净的运行时环境** — 删除生产中不需要的文件，如文档、测试和构建缓存。
- **直接的端口使用** — 应用在内部端口 3000 运行，外部暴露为端口 8080。
- **内存优化的运行时** — Node.js 配置为以比默认值更小的内存限制运行。

### 步骤 2：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>
> - 减小镜像体积
> - 加快构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并用优化配置替换您现有的 `.dockerignore` 内容：

```dockerignore
# Node.js + React Todo 应用的优化 .dockerignore
# 基于实际项目结构

# 版本控制
.git/
.github/
.gitignore

# 依赖项（在容器中安装）
node_modules/

# 构建输出（在容器中构建）
dist/

# 环境文件
.env*

# 开发文件
.vscode/
*.log
coverage/
.eslintcache

# 操作系统文件
.DS_Store
Thumbs.db

# 文档
*.md
docs/

# 部署配置
compose.yml
Taskfile.yml
nodejs-sample-kubernetes.yaml

# 非必要配置（保留构建配置）
*.config.js
!vite.config.ts
!esbuild.config.js
!tailwind.config.js
!postcss.config.js
!tsconfig.json
```

### 步骤 3：构建 Node.js 应用镜像

创建所有配置文件后，您的项目目录现在应包含所有必要的 Docker 配置文件：

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yml
│ └── README.Docker.md
```

现在您可以为您的 Node.js 应用构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将您的应用程序打包到镜像中。它包括来自当前目录（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）的所有必要文件。

从项目根目录运行以下命令：

```console
$ docker build --target production --tag docker-nodejs-sample .
```

此命令的作用：

- 使用当前目录 (.) 中的 Dockerfile
- 以多阶段构建的生产阶段为目标
- 将应用程序及其依赖项打包到 Docker 镜像中
- 将镜像标记为 docker-nodejs-sample，以便稍后引用

#### 步骤 4：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上可用的镜像。由于您已经在终端中工作，请使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY               TAG              IMAGE ID       CREATED         SIZE
docker-nodejs-sample     latest           423525528038   14 seconds ago  237.46MB
```

此输出提供有关镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 有助于识别不同构建的版本标签（例如，latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该会看到列出的 `docker-nodejs-sample` 镜像。

---

## 运行容器化应用

在上一步中，您为 Node.js 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用是否按预期工作。

在 `docker-nodejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up app-dev --build
```

开发应用程序将启动两个服务器：

- **API 服务器**: [http://localhost:3000](http://localhost:3000) - 带有 REST API 的 Express.js 后端
- **前端**: [http://localhost:5173](http://localhost:5173) - 带有 React 前端的 Vite 开发服务器
- **健康检查**: [http://localhost:3000/health](http://localhost:3000/health) - 应用程序健康状态

对于生产部署，您可以使用：

```console
$ docker compose up app-prod --build
```

这将在 [http://localhost:8080](http://localhost:8080) 上提供全栈应用，Express 服务器在内部端口 3000 运行，映射到外部端口 8080。

您应该会看到一个带有 React 19 的现代 Todo List 应用程序和一个功能齐全的 REST API。

在终端中按 `CTRL + C` 停止您的应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端分离的情况下运行应用程序。在 `docker-nodejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up app-dev --build -d
```

打开浏览器并查看应用程序，访问 [http://localhost:3000](http://localhost:3000) (API) 或 [http://localhost:5173](http://localhost:5173) (前端)。您应该会看到 Todo 应用程序正在运行。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找为开发应用暴露端口 3000、5173 和 9229 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                 PORTS                                                                                                                                   NAMES
93f3faee32c3   docker-nodejs-sample-app-dev   "docker-entrypoint.s…"   33 seconds ago   Up 31 seconds          0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp, 0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp, 0.0.0.0:9230->9229/tcp, [::]:9230->9229/tcp   todoapp-dev
```

### 运行不同的配置文件

您可以使用 Docker Compose 配置文件运行不同的配置：

```console
# 运行生产环境
$ docker compose up app-prod -d

# 运行测试
$ docker compose up app-test -d
```

要停止应用程序，请运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Node.js 应用。通过遵循最佳实践，您创建了一个安全、优化且生产就绪的设置。

您完成的任务：

- 使用 `docker init` 初始化项目以搭建基本的 Docker 配置文件。
- 创建了一个包含开发、生产、测试和数据库服务的 `compose.yml` 文件。
- 使用 `.env` 文件设置环境配置，以便灵活部署。
- 用针对 TypeScript 和 React 优化的多阶段构建替换了默认的 `dockerfile`。
- 用优化的配置替换了默认的 `.dockerignore` 文件，以排除不必要的文件并保持镜像干净高效。
- 使用 `docker build` 构建了您的 Docker 镜像。
- 使用 `docker compose up` 运行容器，包括前台运行和分离模式运行。
- 通过访问 [http://localhost:8080](http://localhost:8080) (生产环境) 或 [http://localhost:3000](http://localhost:3000) (开发环境) 验证应用正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用。

您现在拥有一个完全容器化的 Node.js 应用，运行在 Docker 容器中，并准备好以自信和一致性部署到任何环境。

---

## 相关资源

探索官方参考和最佳实践，以优化您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 下一步

您的 Node.js 应用现已容器化，您可以继续进行下一步。

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序，从而在任何机器上实现一致、隔离且可复现的开发环境。