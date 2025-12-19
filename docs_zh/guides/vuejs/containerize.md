---
title: 容器化 Vue.js 应用程序
linkTitle: 容器化
weight: 10
keywords: vue.js, vue, js, node, image, initialize, build
description: 了解如何使用 Docker 容器化 Vue.js 应用程序，通过遵循最佳实践创建一个针对性能、安全性和可扩展性进行优化的、可用于生产的镜像。

---


## 先决条件

在开始之前，请确保系统上已安装并可使用以下工具：

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 拥有 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **初次接触 Docker？**  
> 请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 Vue.js 应用程序的完整过程。您将学习如何使用最佳实践创建一个可用于生产的 Docker 镜像，以提高性能、安全性、可扩展性和部署效率。

在本指南结束时，您将能够：

- 使用 Docker 容器化 Vue.js 应用程序。
- 创建并优化用于生产构建的 Dockerfile。
- 使用多阶段构建来最小化镜像大小。
- 使用自定义 NGINX 配置高效提供应用程序服务。
- 通过遵循最佳实践构建安全且可维护的 Docker 镜像。

---

## 获取示例应用程序

克隆示例应用程序以供本指南使用。打开终端，导航到您想要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-vuejs-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助为容器化应用程序搭建必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到项目目录的根目录：

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

CLI 将提示您回答一些关于应用设置的问题。
为保持一致性，请在提示时使用与以下示例中显示的相同回答：
| 问题 | 回答 |
|------------------------------------------------------------|-----------------|
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 23.11.0-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run build |
| What port does your server listen on? | 8080 |

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

`docker init` 生成的默认 Dockerfile 为典型的 Node.js 应用程序提供了坚实的基础。然而，Vue.js 是一个前端框架，会编译成静态资源，这意味着需要定制 Dockerfile 以符合 Vue.js 应用程序在生产环境中的构建和服务方式。正确地调整它可以确保更好的性能、更小的镜像大小以及更顺畅的部署过程。

### 步骤 1：检查生成的文件

在此步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建来保持最终镜像干净且小巧
- 使用 NGINX（一种快速且安全的 Web 服务器）提供应用程序服务
- 通过仅包含所需内容来提高性能和安全性

这些更新有助于确保您的应用程序易于部署、加载快速且可用于生产。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的分步说明。它会自动将您的应用程序及其依赖项和运行时环境打包。
> 有关完整详情，请参阅 [Dockerfile 参考](/reference/dockerfile/)。


### 步骤 2：配置 Dockerfile

用下面的优化配置替换当前 `Dockerfile` 的内容。此设置专门针对在干净、高效且可用于生产的环境中构建和提供 Vue.js 应用程序而定制。

```dockerfile
# =========================================
# 阶段 1：构建 Vue.js 应用程序
# =========================================
ARG NODE_VERSION=23.11.0-alpine
ARG NGINX_VERSION=alpine3.22

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 在容器内设置工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 使用 npm ci 安装项目依赖项（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 构建 Vue.js 应用程序
RUN npm run build

# =========================================
# 阶段 2：准备 Nginx 以提供静态文件
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 使用内置的非 root 用户以遵循安全最佳实践
USER nginx

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态构建输出复制到 Nginx 的默认 HTML 提供目录
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认的 NGINX 容体现在在端口 8080 上监听，而不是 80
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]

```

### 步骤 3：配置 .dockerignore 文件

`.dockerignore` 文件在优化 Docker 镜像方面起着至关重要的作用，它指定了应从构建上下文中排除哪些文件和目录。

> [!NOTE]
> 这有助于：
> - 减小镜像大小
> - 加快构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并替换您现有的 `.dockerignore` 内容为以下配置：

```dockerignore
# -------------------------------
# 依赖目录
# -------------------------------
node_modules/

# -------------------------------
# 生产和构建输出
# -------------------------------
dist/
out/
build/
public/build/

# -------------------------------
# Vite、VuePress 和缓存目录
# -------------------------------
.vite/
.vitepress/
.cache/
.tmp/

# -------------------------------
# 测试输出和覆盖率
# -------------------------------
coverage/
reports/
jest/
cypress/
cypress/screenshots/
cypress/videos/

# -------------------------------
# 环境和配置文件
# -------------------------------
*.env*
!.env.production    # 如果需要，保留生产环境变量
*.local
*.log

# -------------------------------
# TypeScript 产物
# -------------------------------
*.tsbuildinfo

# -------------------------------
# 编辑器和 IDE 配置
# -------------------------------
.vscode/
.idea/
*.swp

# -------------------------------
# 系统文件
# -------------------------------
.DS_Store
Thumbs.db

# -------------------------------
# 锁文件（可选）
# -------------------------------
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# -------------------------------
# Git 文件
# -------------------------------
.git/
.gitignore

# -------------------------------
# Docker 相关文件
# -------------------------------
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml
```

### 步骤 4：创建 `nginx.conf` 文件

为了在容器内高效地提供您的 Vue.js 应用程序，您需要使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩以及对客户端路由的支持进行了优化。

在项目目录的根目录下创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解有关配置 NGINX 的更多信息，请参阅 [官方 NGINX 文档](https://nginx.org/en/docs/)。

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

### 步骤 5：构建 Vue.js 应用程序镜像

将您的自定义配置放置到位后，您现在可以为您的 Vue.js 应用程序构建 Docker 镜像了。

更新后的设置包括：

- 更新后的设置包括一个干净、可用于生产的 NGINX 配置，专门针对 Vue.js 进行了定制。
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

现在您的 Dockerfile 已配置好，您可以为您的 Vue.js 应用程序构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将您的应用程序打包到镜像中。它包括来自当前目录（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）的所有必要文件。

从项目根目录运行以下命令：

```console
$ docker build --tag docker-vuejs-sample .
```

此命令的作用：
- 使用当前目录 (.) 中的 Dockerfile
- 将应用程序及其依赖项打包到 Docker 镜像中
- 将镜像标记为 docker-vuejs-sample，以便稍后引用


#### 步骤 6：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上有哪些可用镜像。由于您已经在终端中工作，让我们使用 Docker CLI。

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
- **Tag** – 有助于标识不同构建的版本标签（例如，latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该会看到列出的 `docker-vuejs-sample` 镜像。

---

## 运行容器化应用程序

在上一步中，您为您的 Vue.js 应用程序创建了一个 Dockerfile，并使用 docker build 命令构建了一个 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用程序是否按预期工作了。

在 `docker-vuejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到一个简单的 Vue.js Web 应用程序。

在终端中按 `ctrl+c` 停止您的应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端分离的情况下运行应用程序。在 `docker-vuejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会在浏览器中看到您的 Vue.js 应用程序正在运行。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
37a1fa85e4b0   docker-vuejs-sample-server     "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-vuejs-sample-server-1
```


要停止应用程序，请运行：

```console
$ docker compose down
```


> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Vue.js 应用程序。通过遵循最佳实践，您创建了一个安全、优化且可用于生产的设置。

您完成的任务：
- 使用 `docker init` 初始化项目以搭建基本的 Docker 配置文件。
- 用多阶段构建替换了默认的 `Dockerfile`，该构建会编译 Vue.js 应用程序并使用 Nginx 提供静态文件。
- 替换了默认的 `.dockerignore` 文件以排除不必要的文件，保持镜像干净高效。
- 使用 `docker build` 构建了您的 Docker 镜像。
- 使用 `docker compose up` 运行了容器，包括前台运行和分离模式运行。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证了应用程序正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用程序。

您现在拥有一个完全容器化的 Vue.js 应用程序，它在 Docker 容器中运行，并准备好以信心和一致性部署到任何环境。

---

## 相关资源

探索官方参考和最佳实践以提升您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 学习如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用程序。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 下一步

您的 Vue.js 应用程序现已容器化，您可以继续进行下一步了。

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序，从而在任何机器上实现一致、隔离且可重现的开发环境。