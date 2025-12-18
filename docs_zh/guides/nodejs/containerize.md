---
title: 容器化 Node.js 应用
linkTitle: 容器化
weight: 10
keywords: node.js, node, containerize, initialize
description: 学习如何使用 Docker 通过创建优化的、可用于生产的镜像来容器化 Node.js 应用，遵循最佳实践以提高性能、安全性和可扩展性。
aliases:
  - /get-started/nodejs/build-images/
  - /language/nodejs/build-images/
  - /language/nodejs/run-containers/
  - /language/nodejs/containerize/
  - /guides/language/nodejs/containerize/
---

## 前置要求

开始之前，请确保以下工具已安装并在系统上可用：

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **刚接触 Docker？**  
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 Node.js 应用的完整过程。您将学习如何创建针对 Node.js 环境优化的生产就绪 Docker 镜像，遵循最佳实践以提高性能、安全性、可扩展性和运行效率。

完成本指南后，您将能够：

- 使用 Docker 容器化 Node.js 应用。
- 创建并优化适用于 Node.js 环境的 Dockerfile。
- 使用多阶段构建分离依赖项并减小镜像大小。
- 配置容器以非 root 用户身份安全、高效地运行。
- 遵循构建安全、轻量且可维护的 Docker 镜像的最佳实践。

## 获取示例应用

克隆示例应用以配合本指南使用。打开终端，将目录更改为要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-nodejs-sample
```

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助搭建容器化应用所需的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

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

CLI 将提示您几个关于应用设置的问题。为保持一致性，当提示时使用下表示例中显示的相同响应：

| 问题 | 答案 |
|------------------------------------------------------------|-----------------|
| 您的项目使用什么应用平台？ | Node |
| 您想使用哪个版本的 Node？ | 24.11.1-alpine |
| 您想使用哪个包管理器？ | npm |
| 您是否想在启动服务器之前运行 "npm run build"？ | yes |
| 您的构建输出目录是什么？ | dist |
| 您想使用什么命令启动应用？ | npm run dev |
| 您的服务器监听哪个端口？ | 3000 |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

## 创建 Docker Compose 文件

虽然 `docker init` 生成了一个基本的 `compose.yaml` 文件，但您需要为此全栈应用创建一个更全面的配置。用生产就绪的配置替换生成的 `compose.yaml`。

在项目根目录创建一个名为 `compose.yml` 的新文件：

```yaml
# ========================================
# Docker Compose Configuration
# Modern Node.js Todo Application
# ========================================

services:
  # ========================================
  # Development Service
  # ========================================
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: todoapp-dev
    ports:
      - '${APP_PORT:-3000}:3000' # API server
      - '${VITE_PORT:-5173}:5173' # Vite dev server
      - '${DEBUG_PORT:-9229}:9229' # Node.js debugger
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
  # Production Service
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
  # PostgreSQL Database Service
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
# Volume Configuration
# ========================================
volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

# ========================================
# Network Configuration
# ========================================
networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

此 Docker Compose 配置包括：

- **开发服务** (`app-dev`)：具有热重载、调试支持和绑定挂载的完整开发环境
- **生产服务** (`app-prod`)：具有资源限制和安全加固的优化生产部署
- **数据库服务** (`db`)：具有持久存储和健康检查的 PostgreSQL 16
- **网络**：用于安全服务通信的隔离网络
- **卷**：数据库数据的持久存储

## 创建环境配置

创建一个 `.env` 文件来配置应用设置：

```console
$ cp .env.example .env
```

使用首选设置更新 `.env` 文件：

```env
# Application Configuration
NODE_ENV=development
APP_PORT=3000
VITE_PORT=5173
DEBUG_PORT=9229

# Production Configuration
PROD_PORT=8080
PROD_MEMORY_LIMIT=2G
PROD_CPU_LIMIT=1.0
PROD_MEMORY_RESERVATION=512M
PROD_CPU_RESERVATION=0.25

# Database Configuration
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=todoapp
POSTGRES_USER=todoapp
POSTGRES_PASSWORD=todoapp_password
DB_PORT=5432

# Security Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 为标准 Node.js 应用提供了可靠的基线。但是，由于此项目是一个包含后端 API 和前端 React 组件的全栈 TypeScript 应用，Dockerfile 应进行自定义以更好地支持和优化此特定架构。

### 审查生成的文件

在下一步中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建保持最终镜像清洁和小巧
- 通过仅包含所需内容来提高性能和安全性

这些更新使您的应用更易于部署且加载更快。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的逐步说明。它自动化打包您的应用及其依赖项和运行时环境的过程。  
> 详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 1：配置 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node) 或 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 中的 Docker Hardened Image (DHI)。

选择 DHI 具有生产就绪镜像的优势，该镜像轻量且安全。更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用在编写指南时被认为是安全的稳定 Node.js LTS 镜像标签。由于新版本和安全补丁定期发布，当您遵循本指南时，此处显示的标签可能不再是安全的选择。在构建或部署应用之前，请始终查看最新的可用镜像标签并选择安全、最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images (DHIs) 可在 [Docker Hub](https://hub.docker.com/hardened-images/catalog/dhi/node) 上获得 Node.js 的镜像。与使用 Docker 官方镜像不同，您必须首先将 Node.js 镜像镜像到您的组织中，然后将其用作基础镜像。请按照 [DHI 快速入门](/dhi/get-started/) 中的说明为 Node.js 创建镜像仓库。

镜像仓库必须以 `dhi-` 开头，例如：`FROM <your-namespace>/dhi-node:<tag>`。在以下 Dockerfile 中，`FROM` 指令使用 `<your-namespace>/dhi-node:24-alpine3.22-dev` 作为基础镜像。

```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Node.js TypeScript Application (Using DHI)
# ========================================

FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Build Dependencies Stage
# ========================================
FROM base AS build-deps

# Copy package files
COPY package*.json ./

# Install all dependencies with build optimizations
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# Create necessary directories and set permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# Build Stage
# ========================================
FROM build-deps AS build

# Copy only necessary files for building (respects .dockerignore)
COPY --chown=nodejs:nodejs . .

# Build the application
RUN npm run build

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Development Stage
# ========================================
FROM build-deps AS development

# Set environment
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# Copy source files
COPY . .

# Ensure all directories have proper permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# Switch to non-root user
USER nodejs

# Expose ports
EXPOSE 3000 5173 9229

# Start development server
CMD ["npm", "run", "dev:docker"]

# ========================================
# Production Stage
# ========================================
FROM <your-namespace>/dhi-node:24-alpine3.22-dev AS production

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# Set optimized environment variables
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=256 --no-warnings" \
    NPM_CONFIG_LOGLEVEL=silent

# Copy production dependencies from deps stage
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=deps --chown=nodejs:nodejs /app/package*.json ./
# Copy built application from build stage
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist

# Switch to non-root user for security
USER nodejs

# Expose port
EXPOSE 3000

# Start production server
CMD ["node", "dist/server.js"]

# ========================================
# Test Stage
# ========================================
FROM build-deps AS test

# Set environment
ENV NODE_ENV=test \
    CI=true

# Copy source files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

# Run tests with coverage
CMD ["npm", "run", "test:coverage"]
```

{{< /tab >}}
{{< tab name="使用 Docker 官方镜像" >}}

现在您需要创建一个生产就绪的多阶段 Dockerfile。用以下优化配置替换生成的 Dockerfile：

```dockerfile
# ========================================
# Optimized Multi-Stage Dockerfile
# Node.js TypeScript Application
# ========================================

ARG NODE_VERSION=24.11.1-alpine
FROM node:${NODE_VERSION} AS base

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs && \
    chown -R nodejs:nodejs /app

# ========================================
# Dependencies Stage
# ========================================
FROM base AS deps

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --omit=dev && \
    npm cache clean --force

# Set proper ownership
RUN chown -R nodejs:nodejs /app

# ========================================
# Build Dependencies Stage
# ========================================
FROM base AS build-deps

# Copy package files
COPY package*.json ./

# Install all dependencies with build optimizations
RUN --mount=type=cache,target=/root/.npm,sharing=locked \
    npm ci --no-audit --no-fund && \
    npm cache clean --force

# Create necessary directories and set permissions
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app

# ========================================
# Build Stage
# ========================================
FROM build-deps AS build

# Copy only necessary files for building (respects .dockerignore)
COPY --chown=nodejs:nodejs . .

# Build the application
RUN npm run build

# Set proper ownership
RUN chown -R