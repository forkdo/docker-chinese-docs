---
title: 容器化 React.js 应用
linkTitle: 容器化
weight: 10
keywords: react.js, node, image, initialize, build
description: 了解如何使用 Docker 通过创建优化的、可用于生产的镜像来容器化 React.js 应用，采用最佳实践以提升性能、安全性和可扩展性。

---

## 前置条件

开始之前，请确保系统上已安装以下工具：

- 已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 已安装 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但您可以使用任意客户端。

> **首次使用 Docker？**  
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，了解镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 React.js 应用的完整过程。您将学习如何使用最佳实践创建可用于生产的 Docker 镜像，这些实践可提升性能、安全性、可扩展性和部署效率。

完成本指南后，您将能够：

- 使用 Docker 容器化 React.js 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建最小化镜像大小。
- 使用自定义 NGINX 配置高效地提供应用服务。
- 遵循构建安全且可维护的 Docker 镜像的最佳实践。

---

## 获取示例应用

克隆本指南使用的示例应用。打开终端，将目录切换到您想要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-reactjs-sample
```
---

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助搭建容器化应用所需的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

首先，导航到项目目录的根目录：

```console
$ cd docker-reactjs-sample
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
为保持一致，请在提示时使用下表示例中显示的相同响应：
| 问题                                                   | 答案          |
|------------------------------------------------------------|-----------------|
| 您的项目使用什么应用平台？           | Node            |
| 您想使用哪个版本的 Node？                   | 24.7.0-alpine  |
| 您想使用哪个包管理器？                  | npm             |
| 您是否想在启动服务器之前运行 "npm run build"？ | yes             |
| 您的构建输出目录是什么？                    | dist            |
| 您想使用什么命令启动应用？          | npm run dev     |
| 您的服务器监听哪个端口？                      | 8080            |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 为 Node.js 应用提供了一个良好的起点。但是，React.js 是一个前端库，会编译成静态资源，因此我们需要定制 Dockerfile 以优化 React 应用在生产环境中的构建和提供方式。

### 步骤 1：查看生成的文件

在此步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建保持最终镜像的清洁和小巧
- 使用 NGINX 提供应用服务，这是一个快速且安全的 Web 服务器
- 仅包含所需内容以提升性能和安全性

这些更新有助于确保您的应用易于部署、快速加载且可用于生产。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的逐步说明。它自动化打包您的应用及其依赖项和运行时环境的过程。  
> 详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 2：配置 Dockerfile 文件

复制并用以下配置替换现有 `Dockerfile` 的内容：

```dockerfile
# =========================================
# 阶段 1：构建 React.js 应用
# =========================================
ARG NODE_VERSION=24.7.0-alpine
ARG NGINX_VERSION=alpine3.22

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制包相关文件以利用 Docker 的缓存机制
COPY package.json package-lock.json ./

# 使用 npm ci 安装项目依赖（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将应用的其余源代码复制到容器中
COPY . .

# 构建 React.js 应用（输出到 /app/dist）
RUN npm run build

# =========================================
# 阶段 2：准备 Nginx 提供静态文件
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 使用内置的非 root 用户以遵循安全最佳实践
USER nginx

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态输出从构建阶段复制到 Nginx 的默认 HTML 提供目录
COPY --chown=nginx:nginx  --from=builder /app/dist /usr/share/nginx/html

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 NGINX 容器现在监听端口 8080 而不是 80
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

### 步骤 3：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>- 减小镜像大小
>- 加快构建过程
>- 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 详细信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并用以下配置替换现有 `.dockerignore` 的内容：

```dockerignore
# 忽略依赖和构建输出
node_modules/
dist/
out/
.tmp/
.cache/

# 忽略 Vite、Webpack 和 React 特定的构建产物
.vite/
.vitepress/
.eslintcache
.npm/
coverage/
jest/
cypress/
cypress/screenshots/
cypress/videos/
reports/

# 忽略环境和配置文件（敏感数据）
*.env*
*.log

# 忽略 TypeScript 构建产物（如果使用 TypeScript）
*.tsbuildinfo

# 忽略锁定文件（如果使用 Docker 进行包安装则可选）
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# 忽略本地开发文件
.git/
.gitignore
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db

# 忽略 Docker 相关文件（避免复制不必要的配置）
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml

# 忽略特定于构建的缓存文件
*.lock

```

### 步骤 4：创建 `nginx.conf` 文件

为了在容器内高效地提供您的 React.js 应用服务，您将使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩和支持客户端路由进行了优化。

在项目目录的根目录中创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 了解有关配置 NGINX 的更多信息，请参阅 [官方 NGINX 文档](https://nginx.org/en/docs/)。

```nginx
worker_processes auto;

# 将 PID 存储在 /tmp（始终可写）
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 禁用日志以避免权限问题
    access_log off;
    error_log  /dev/stderr warn;

    # 优化静态文件提供
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # 优化交付的 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    gzip_vary on;

    server {
        listen       8080;
        server_name  localhost;

        # 放置 React.js 构建文件的根目录
        root /usr/share/nginx/html;
        index index.html;

        # 使用适当的缓存提供 React.js 静态文件
        location / {
            try_files $uri /index.html;
        }

        # 使用长缓存过期时间提供静态资源
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # 处理 React.js 客户端路由
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 步骤 5：构建 React.js 应用镜像

配置完成后，您现在可以为 React.js 应用构建 Docker 镜像了。

更新的设置包括：

- 优化的浏览器缓存和 gzip 压缩
- 安全的非 root 日志记录以避免权限问题
- 通过将不匹配的路由重定向到 `index.html` 支持 React 客户端路由

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在 Dockerfile 已配置好，您可以为 React.js 应用构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将您的应用打包成镜像。它包括当前目录中的所有必要文件（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）。

从项目根目录运行以下命令：

```console
$ docker build --tag docker-reactjs-sample .
```

此命令的作用：
- 使用当前目录（.）中的 Dockerfile
- 将应用及其依赖项打包成 Docker 镜像
- 将镜像标记为 docker-reactjs-sample 以便稍后引用

#### 步骤 6：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上可用的镜像。由于您已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-reactjs-sample     latest            f39b47a97156   14 seconds ago   75.8MB
```

此输出提供有关镜像的关键详细信息：

- **仓库** – 分配给镜像的名称。
- **标签** – 帮助标识不同构建的版本标签（例如 latest）。
- **镜像 ID** – 镜像的唯一标识符。
- **创建时间** – 镜像构建的时间戳。
- **大小** – 镜像使用的总磁盘空间。

如果构建成功，您应该在列表中看到 `docker-reactjs-sample` 镜像。

---

## 运行容器化应用

在前面的步骤中，您为 React.js 应用创建了 Dockerfile 并使用 `docker build` 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用是否按预期工作。

在 `docker-reactjs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用。您应该看到一个简单的 React.js Web 应用。

按 `ctrl+c` 停止应用。

### 在后台运行应用

您可以通过添加 `-d` 选项在终端外以分离模式运行应用。在 `docker-reactjs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用。您应该看到一个简单的 Web 应用预览。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
88bced6ade95   docker-reactjs-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-reactjs-sample-server-1
```

要停止容器化应用，请运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 React.js 应用。通过遵循最佳实践，您创建了一个安全、优化且可用于生产的设置。

您完成的内容：
- 使用 `docker init` 初始化项目以搭建必要的 Docker 配置文件。
- 用多阶段构建替换默认 `Dockerfile`，该构建编译 React.js 应用并使用 Nginx 提供静态文件。
- 用默认 `.dockerignore` 文件替换以排除不必要的文件并保持镜像清洁高效。
- 使用 `docker build` 构建 Docker 镜像。
- 使用 `docker compose up` 在前台和分离模式下运行容器。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证应用正在运行。
- 学习如何使用 `docker compose down` 停止容器化应用。

您现在拥有一个完全容器化的 React.js 应用，在 Docker 容器中运行，并准备好在任何环境中一致地部署。

---

## 相关资源

探索官方参考和最佳实践以优化您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并删除容器、网络和卷。

---

## 后续步骤

您的 React.js 应用现在已容器化，您已准备好进入下一步。

在下一节中，您将学习如何使用 Docker 容器开发应用，从而在任何机器上实现一致、隔离且可重现的开发环境。