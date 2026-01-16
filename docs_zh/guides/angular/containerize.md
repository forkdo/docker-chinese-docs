---
title: 容器化 Angular 应用程序
linkTitle: 容器化
weight: 10
keywords: angular, node, image, initialize, build
description: 了解如何使用 Docker 容器化 Angular 应用程序，通过遵循性能、安全性和可扩展性的最佳实践，创建优化的、可用于生产的镜像。

---

## 先决条件

在开始之前，请确保以下工具已安装并在您的系统上可用：

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **Docker 新手？**  
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概览

本指南将引导您完成使用 Docker 容器化 Angular 应用程序的完整过程。您将学习如何创建可用于生产的 Docker 镜像，并采用能够提升性能、安全性、可扩展性和部署效率的最佳实践。

在本指南结束时，您将能够：

- 使用 Docker 容器化 Angular 应用程序。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建以最小化镜像大小。
- 使用自定义 Nginx 配置高效地提供应用程序服务。
- 通过遵循最佳实践构建安全且可维护的 Docker 镜像。

---

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，导航到您希望工作的目录，然后运行以下命令以克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-angular-sample
```

---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助为您的应用程序容器化搭建必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到您的项目根目录：

```console
$ cd docker-angular-sample
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

CLI 将提示您回答一些关于应用程序设置的问题。
为保持一致性，请在提示时按照下方示例所示使用相同的回答：

| 问题 | 回答 |
|------|------|
| 您的项目使用什么应用程序平台？ | Node |
| 您希望使用哪个版本的 Node？ | 24.12.0-alpine |
| 您希望使用哪个包管理器？ | npm |
| 您是否希望在启动服务器之前运行 "npm run build"？ | yes |
| 您的构建输出目录是什么？ | dist |
| 您希望使用什么命令来启动应用程序？ | npm run start |
| 您的服务器监听哪个端口？ | 8080 |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 是通用 Node.js 应用程序的良好起点。然而，Angular 是一个前端框架，会编译成静态资源，因此我们需要定制 Dockerfile 以优化 Angular 应用程序在**生产环境**中的构建和提供服务的方式。

### 步骤 1：改进生成的 Dockerfile 和配置

在此步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建以保持最终镜像干净且体积小  
- 使用 Nginx（一个快速且安全的 Web 服务器）来提供应用程序服务  
- 通过仅包含所需内容来提高性能和安全性  

这些更新有助于确保您的应用程序易于部署、加载快速，并可用于生产环境。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的分步指令。它自动化地将您的应用程序及其依赖项和运行时环境打包在一起。  
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 2：配置 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它是一个可用于生产的镜像，既轻量又安全。有关更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用在编写指南时被认为是安全的稳定 Node.js LTS 镜像标签。由于新版本和安全补丁会定期发布，因此此处显示的标签在您遵循本指南时可能不再是安全的选择。在构建或部署应用程序之前，请务必查看最新可用的镜像标签，并选择一个安全、最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images (DHIs) 可用于 Node.js，位于 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/node)。Docker Hardened Images 对所有人免费开放，无需订阅。您可以在登录 DHI 注册表后像任何其他 Docker 镜像一样拉取和使用它们。有关更多信息，请参阅 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录 DHI 注册表：
   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（请查看目录以了解可用版本）：
   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

在以下 Dockerfile 中，`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev` 作为基础镜像。

```dockerfile
# =========================================
# 阶段 1：构建 Angular 应用程序
# =========================================

# 使用轻量级 DHI Node.js 镜像进行构建
FROM dhi.io/node:24-alpine3.22-dev AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json package-lock.json* ./

# 使用 npm ci 安装项目依赖项（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 构建 Angular 应用程序
RUN npm run build 

# =========================================
# 阶段 2：准备 Nginx 以提供静态文件服务
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态构建输出复制到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# 为了安全最佳实践，使用非 root 用户
USER nginx

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 Nginx 容器现在监听端口 8080 而不是 80
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

{{< /tab >}}
{{< tab name="使用 Docker 官方镜像" >}}

现在您需要创建一个可用于生产的多阶段 Dockerfile。将生成的 Dockerfile 替换为以下优化配置：

```dockerfile
# =========================================
# 阶段 1：构建 Angular 应用程序
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制与包相关的文件以利用 Docker 的缓存机制
COPY package.json *package-lock.json* ./

# 使用 npm ci 安装项目依赖项（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将应用程序源代码的其余部分复制到容器中
COPY . .

# 构建 Angular 应用程序
RUN npm run build 

# =========================================
# 阶段 2：准备 Nginx 以提供静态文件服务
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态构建输出复制到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# 为了安全最佳实践，使用内置的非 root 用户
USER nginx

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 Nginx 容器现在监听端口 8080 而不是 80
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> [!NOTE]
> 我们使用 nginx-unprivileged 而不是标准 Nginx 镜像以遵循安全最佳实践。
> 在最终镜像中以非 root 用户身份运行：
> - 减少攻击面
> - 符合 Docker 关于容器加固的建议
> - 有助于在**生产环境**中遵守更严格的安全策略

{{< /tab >}}
{{< /tabs >}}

### 步骤 3：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
> - 减小镜像大小  
> - 加快构建过程  
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并将您现有 `.dockerignore` 的内容替换为以下配置：

```dockerignore
# ================================
# Node 和构建输出
# ================================
node_modules
dist
out-tsc
.angular
.cache
.tmp

# ================================
# 测试与覆盖率
# ================================
coverage
jest
cypress
cypress/screenshots
cypress/videos
reports
playwright-report
.vite
.vitepress

# ================================
# 环境与日志文件
# ================================
*.env*
!*.env.production
*.log
*.tsbuildinfo

# ================================
# IDE 与操作系统特定文件
# ================================
.vscode
.idea
.DS_Store
Thumbs.db
*.swp

# ================================
# 版本控制与 CI 文件
# ================================
.git
.gitignore

# ================================
# Docker 与本地编排
# ================================
Dockerfile
Dockerfile.*
.dockerignore
docker-compose.yml
docker-compose*.yml

# ================================
# 杂项
# ================================
*.bak
*.old
*.tmp
```

### 步骤 4：创建 `nginx.conf` 文件

为了在容器内高效地提供您的 Angular 应用程序服务，您将使用自定义设置配置 Nginx。此配置针对性能、浏览器缓存、gzip 压缩以及对客户端路由的支持进行了优化。

在您的项目根目录中创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解有关配置 Nginx 的更多信息，请参阅 [官方 Nginx 文档](https://nginx.org/en/docs/)。

```nginx
worker_processes auto;

pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    client_body_temp_path /tmp/client_temp;
    proxy_temp_path       /tmp/proxy_temp_path;
    fastcgi_temp_path     /tmp/fastcgi_temp;
    uwsgi_temp_path       /tmp/uwsgi_temp;
    scgi_temp_path        /tmp/scgi_temp;

    # 日志记录
    access_log off;
    error_log  /dev/stderr warn;

    # 性能
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/x-javascript
        application/json
        application/xml
        application/xml+rss
        font/ttf
        font/otf
        image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root /usr/share/nginx/html;
        index index.html;

        # Angular 路由
        location / {
            try_files $uri $uri/ /index.html;
        }

        # 静态资源缓存
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # 可选：显式资源路由
        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 步骤 5：构建 Angular 应用程序镜像

使用您的自定义配置，您现在可以为 Angular 应用程序构建 Docker 镜像。

更新后的设置包括：

- 针对 Angular 专门定制的干净、可用于生产的 Nginx 配置。
- 高效的多阶段 Docker 构建，确保最终镜像小巧且安全。

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在您的 Dockerfile 已配置完成，您可以为 Angular 应用程序构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将您的应用程序打包成镜像。它包含当前目录（称为[构建上下文](/build/concepts/context/#what-is-a-build-context)）中的所有必要文件。

从您的项目根目录运行以下命令：

```console
$ docker build --tag docker-angular-sample .
```

此命令的作用：
- 使用当前目录 (.) 中的 Dockerfile
- 将应用程序及其依赖项打包到 Docker 镜像中
- 将镜像标记为 docker-angular-sample，以便您稍后引用

#### 步骤 6：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上有哪些镜像可用。由于您已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-angular-sample     latest            34e66bdb9d40   14 seconds ago   76.4MB
```

此输出提供有关镜像的关键详细信息：

- **Repository（仓库）** – 分配给镜像的名称。
- **Tag（标签）** – 帮助识别不同构建的版本标签（例如 latest）。
- **Image ID（镜像 ID）** – 镜像的唯一标识符。
- **Created（创建时间）** – 指示镜像构建时的时间戳。
- **Size（大小）** – 镜像使用的总磁盘空间。

如果构建成功，您应该会看到列出的 `docker-angular-sample` 镜像。

---

## 运行容器化应用程序

在上一步中，您为 Angular 应用程序创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用程序是否按预期工作。

在 `docker-angular-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到一个简单的 Angular Web 应用程序。

在终端中按 `ctrl+c` 以停止您的应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项使应用程序与终端分离运行。在 `docker-angular-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器并在 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该会看到 Angular 应用程序在浏览器中运行。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
eb13026806d1   docker-angular-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-angular-sample-server-1
```

要停止应用程序，请运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Angular 应用程序。通过遵循最佳实践，您创建了一个安全、优化且可用于生产的设置。

您完成了以下工作：
- 使用 `docker init` 初始化项目，搭建必要的 Docker 配置文件。
- 将默认的 `Dockerfile` 替换为多阶段构建，该构建编译 Angular 应用程序并使用 Nginx 提供静态文件服务。
- 替换默认的 `.dockerignore` 文件以排除不必要的文件，保持镜像干净高效。
- 使用 `docker build` 构建 Docker 镜像。
- 使用 `docker compose up` 运行容器，既在前台也在分离模式下运行。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证应用程序正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用程序。

您现在拥有一个完全容器化的 Angular 应用程序，运行在 Docker 容器中，并准备好在任何环境中自信且一致地部署。

---

## 相关资源

探索官方参考和最佳实践，以提升您的 Docker 工作流：

- [多阶段构建](/build/building/multi-stage/) – 学习如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资源。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用程序。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 后续步骤

现在您的 Angular 应用程序已完成容器化，您可以继续下一步。

在下一节中，您将学习如何使用 Docker 容器开发应用程序，从而在任何机器上实现一致、隔离且可重现的开发环境。