---
title: 容器化 Vue.js 应用
linkTitle: 容器化
weight: 10
keywords: vue.js, vue, js, node, image, initialize, build
description: 了解如何使用 Docker 通过创建优化的、生产就绪的镜像来容器化 Vue.js 应用，采用最佳实践以提升性能、安全性和可扩展性。

---


## 前置条件

开始之前，请确保系统已安装以下工具：

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但您可以使用任意客户端。

> **首次使用 Docker？**  
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将带您完整了解如何使用 Docker 容器化 Vue.js 应用。您将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提升性能、安全性、可扩展性和部署效率。

完成本指南后，您将能够：

- 使用 Docker 容器化 Vue.js 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建最小化镜像大小。
- 使用自定义 NGINX 配置高效提供应用服务。
- 遵循最佳实践构建安全且可维护的 Docker 镜像。

---

## 获取示例应用

克隆本指南使用的示例应用。打开终端，导航到您要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-vuejs-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助搭建容器化应用所需的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到项目根目录：

```console
$ cd docker-vuejs-sample
```

然后运行以下命令：

```console
$ docker init
```
您将看到类似以下的输出：

```text
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!
```

CLI 将提示您几个关于应用设置的问题。
为保持一致性，当提示时请使用下表中显示的相同响应：
| 问题                                                   | 答案          |
|------------------------------------------------------------|-----------------|
| What application platform does your project use?           | Node            |
| What version of Node do you want to use?                   | 23.11.0-alpine  |
| Which package manager do you want to use?                  | npm             |
| Do you want to run "npm run build" before starting server? | yes             |
| What directory is your build output to?                    | dist            |
| What command do you want to use to start the app?          | npm run build   |
| What port does your server listen on?                      | 8080            |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 为典型的 Node.js 应用提供了坚实的基础。然而，Vue.js 是一个前端框架，会编译为静态资源，这意味着 Dockerfile 需要定制，以符合 Vue.js 应用在生产环境中的构建和高效服务方式。正确调整它可确保更好的性能、更小的镜像大小和更顺畅的部署过程。

### 步骤 1：查看生成的文件

在此步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建保持最终镜像的清洁和小巧
- 使用 NGINX 提供应用服务，这是一个快速且安全的 Web 服务器
- 仅包含必要的内容以提升性能和安全性

这些更新有助于确保您的应用易于部署、快速加载且为生产就绪。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的逐步说明。它自动化打包您的应用及其依赖项和运行时环境的过程。  
> 详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 2：配置 Dockerfile

用以下优化配置替换当前 `Dockerfile` 的内容。此设置专门为在清洁、高效且生产就绪的环境中构建和服务 Vue.js 应用而定制。

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
ARG NODE_VERSION=23.11.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Use a built-in non-root user for security best practices
USER nginx

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf


# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Expose port 8080 to allow HTTP traffic
# Note: The default NGINX container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]

```

### 步骤 3：配置 .dockerignore 文件

`.dockerignore` 文件通过指定应从构建上下文中排除的文件和目录，在优化 Docker 镜像方面发挥着关键作用。

> [!NOTE]
> 这有助于：
>- 减小镜像大小
>- 加快构建过程
>- 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

用以下配置替换现有 `.dockerignore` 的内容：

```dockerignore
# -------------------------------
# Dependency directories
# -------------------------------
node_modules/

# -------------------------------
# Production and build outputs
# -------------------------------
dist/
out/
build/
public/build/

# -------------------------------
# Vite, VuePress, and cache dirs
# -------------------------------
.vite/
.vitepress/
.cache/
.tmp/

# -------------------------------
# Test output and coverage
# -------------------------------
coverage/
reports/
jest/
cypress/
cypress/screenshots/
cypress/videos/

# -------------------------------
# Environment and config files
# -------------------------------
*.env*
!.env.production    # Keep production env if needed
*.local
*.log

# -------------------------------
# TypeScript artifacts
# -------------------------------
*.tsbuildinfo

# -------------------------------
# Editor and IDE config
# -------------------------------
.vscode/
.idea/
*.swp

# -------------------------------
# System files
# -------------------------------
.DS_Store
Thumbs.db

# -------------------------------
# Lockfiles (optional)
# -------------------------------
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# -------------------------------
# Git files
# -------------------------------
.git/
.gitignore

# -------------------------------
# Docker-related files
# -------------------------------
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml
```

### 步骤 4：创建 `nginx.conf` 文件

为了在容器内高效提供 Vue.js 应用服务，您将使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩和支持客户端路由进行了优化。

在项目根目录创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 了解有关配置 NGINX 的更多信息，请参阅 [官方 NGINX 文档](https://nginx.org/en/docs/)。

```nginx
worker_processes auto;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    charset       utf-8;

    access_log    off;
    error_log     /dev/stderr warn;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    gzip on;
    gzip_comp_level 6;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root   /usr/share/nginx/html;
        index  index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        error_page 404 /index.html;
    }
}
```

### 步骤 5：构建 Vue.js 应用镜像

配置完成后，您现在可以为 Vue.js 应用构建 Docker 镜像。

更新的设置包括：

- 更新的设置包括一个专为 Vue.js 定制的清洁、生产就绪的 NGINX 配置。
- 高效的多阶段 Docker 构建，确保最终镜像小巧且安全。

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在 Dockerfile 已配置好，您可以为 Vue.js 应用构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将您的应用打包成镜像。它包括当前目录中的所有必要文件（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）。

从项目根目录运行以下命令：

```console
$ docker build --tag docker-vuejs-sample .
```

此命令的作用：
- 使用当前目录（.）中的 Dockerfile
- 将应用及其依赖项打包成 Docker 镜像
- 将镜像标记为 docker-vuejs-sample，以便稍后引用

#### 步骤 6：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上可用的镜像。由于您已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-vuejs-sample       latest            8c9c199179d4   14 seconds ago   76.2MB
```

此输出提供有关镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 帮助标识不同构建的版本标签（例如 latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该看到 `docker-vuejs-sample` 镜像已列出。

---

## 运行容器化应用

在前面的步骤中，您为 Vue.js 应用创建了 Dockerfile 并使用 `docker build` 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证应用是否按预期工作。

在 `docker-vuejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用。您应该看到一个简单的 Vue.js Web 应用。

在终端中按 `ctrl+c` 停止应用。

### 在后台运行应用

您可以通过添加 `-d` 选项在终端外以分离模式运行应用。在 `docker-vuejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用。您应该看到 Vue.js 应用在浏览器中运行。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活跃的容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
37a1fa85e4b0   docker-vuejs-sample-server     "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-vuejs-sample-server-1
```

要停止应用，请运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Vue.js 应用。通过遵循最佳实践，您创建了一个安全、优化且生产就绪的设置。

您完成的内容：
- 使用 `docker init` 初始化项目以搭建必要的 Docker 配置文件。
- 用多阶段构建替换默认 `Dockerfile`，编译 Vue.js 应用并使用 Nginx 提供静态文件服务。
- 替换默认 `.dockerignore` 文件以排除不必要的文件，保持镜像清洁高效。
- 使用 `docker build` 构建 Docker 镜像。
- 使用 `docker compose up` 在前台和分离模式下运行容器。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证应用正在运行。
- 学习如何使用 `docker compose down` 停止容器化应用。

现在您拥有一个完全容器化的 Vue.js 应用，正在 Docker 容器中运行，并准备好在任何环境中一致地部署。

---

## 相关资源

探索官方参考和最佳实践以优化您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 后续步骤

您的 Vue.js 应用现已容器化，接下来您将学习如何使用 Docker 容器开发应用，从而在任何机器上实现一致、隔离且可重现的开发环境。