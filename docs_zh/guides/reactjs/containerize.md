---
title: 为 React.js 应用程序创建容器
linkTitle: Containerize
weight: 10
keywords: react.js, node, image, initialize, build
description: 通过使用 Docker 创建优化、生产就绪的镜像，了解如何使用最佳实践为 React.js 应用程序创建容器，从而提高性能、安全性和可扩展性。

---

## 先决条件

开始之前，请确保系统上已安装并可用以下工具：

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您已安装 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您也可以使用任何客户端。

> **Docker 新手？**  
> 从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，了解镜像、容器等核心概念。

---

## 概述

本指南将引导您完成使用 Docker 为 React.js 应用程序创建容器的完整过程。您将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提高性能、安全性、可扩展性和部署效率。

通过本指南，您将能够：

- 使用 Docker 为 React.js 应用程序创建容器。
- 创建并优化用于生产构建的 Dockerfile。
- 使用多阶段构建来最小化镜像大小。
- 使用自定义 NGINX 配置高效地提供应用程序。
- 遵循构建安全且可维护的 Docker 镜像的最佳实践。

---

## 获取示例应用程序

克隆一个示例应用程序来配合本指南使用。打开终端，切换到您想工作的目录，运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-reactjs-sample
```
---

## 生成 Dockerfile

Docker 提供了一个交互式的 CLI 工具 `docker init`，可以帮助您为容器化应用程序生成必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

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
欢迎使用 Docker Init CLI！

此工具将引导您创建以下文件，为您的项目提供合理的默认配置：
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

让我们开始吧！
```

CLI 会就您的应用设置提出几个问题。
为了保持一致，请在提示时使用以下示例中显示的相同回答：
| 问题                                                   | 回答          |
|------------------------------------------------------------|-----------------|
| 您的项目使用什么应用平台？           | Node            |
| 您希望使用什么版本的 Node？                   | 24.12.0-alpine  |
| 您希望使用什么包管理器？                  | npm             |
| 您希望在启动服务器前运行 "npm run build" 吗？ | yes             |
| 您的构建输出目录是什么？                    | dist            |
| 您希望使用什么命令来启动应用？          | npm run dev     |
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

`docker init` 生成的默认 Dockerfile 为一般的 Node.js 应用程序提供了一个良好的起点。然而，React.js 是一个前端库，会编译成静态资源，因此我们需要定制 Dockerfile 来优化 React 应用在生产环境中的构建和提供方式。

### 第 1 步：查看生成的文件

在本步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建来保持最终镜像干净且小巧
- 使用 NGINX（一个快速且安全的 Web 服务器）提供应用程序
- 通过仅包含必要的内容来提高性能和安全性

这些更新有助于确保您的应用易于部署、加载速度快且生产就绪。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的逐步指令。它自动化打包您的应用程序及其依赖项和运行时环境。  
> 有关详细信息，请参阅 [Dockerfile 参考文档](/reference/dockerfile/)。

### 第 2 步：配置 Dockerfile 文件 

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node) 或从 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 获取 Docker Hardened Image（DHI）。

选择 DHI 的优势在于它提供了一个轻量且安全的生产就绪镜像。更多信息请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用了一个在撰写指南时被认为安全的稳定 Node.js LTS 镜像标签。由于新版本和安全补丁会定期发布，此处显示的标签在您遵循指南时可能不再是最佳选择。始终检查最新的可用镜像标签，并在构建或部署应用程序前选择一个安全且最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node

{{< tabs >}}
{{< tab name="使用 Docker Hardened Images" >}}
Docker Hardened Images（DHIs）可在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/node) 中为 Node.js 提供。Docker Hardened Images 对所有人免费，无需订阅。登录 DHI 注册表后，您可以像使用其他 Docker 镜像一样拉取和使用它们。有关更多信息，请参阅 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录 DHI 注册表：
   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（检查目录以获取可用版本）：
   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. 拉取 Nginx DHI（检查目录以获取可用版本）：
   ```console
   $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
   ```

在以下 Dockerfile 中，`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev` 和 `dhi.io/nginx:1.28.0-alpine3.21-dev` 作为基础镜像。

```dockerfile
# =========================================
# 阶段 1：构建 React.js 应用程序
# =========================================

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM dhi.io/node:24-alpine3.22-dev AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制包相关文件以利用 Docker 的缓存机制
COPY package.json package-lock.json* ./

# 使用 npm ci 安装项目依赖（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将其余应用程序源代码复制到容器中
COPY . .

# 构建 React.js 应用程序（输出到 /app/dist）
RUN npm run build

# =========================================
# 阶段 2：准备 Nginx 以提供静态文件
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 从构建阶段复制静态构建输出到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# 使用非根用户以符合安全最佳实践
USER nginx

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 NGINX 容器现在在端口 8080 上监听而非 80
EXPOSE 8080

# 直接使用自定义配置启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

{{< /tab >}}
{{< tab name="使用 Docker 官方镜像" >}}

现在您需要创建一个生产就绪的多阶段 Dockerfile。用以下优化配置替换生成的 Dockerfile：

```dockerfile
# =========================================
# 阶段 1：构建 React.js 应用程序
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# 使用轻量级 Node.js 镜像进行构建（可通过 ARG 自定义）
FROM node:${NODE_VERSION} AS builder

# 设置容器内的工作目录
WORKDIR /app

# 首先复制包相关文件以利用 Docker 的缓存机制
COPY package.json package-lock.json* ./

# 使用 npm ci 安装项目依赖（确保干净、可重现的安装）
RUN --mount=type=cache,target=/root/.npm npm ci

# 将其余应用程序源代码复制到容器中
COPY . .

# 构建 React.js 应用程序（输出到 /app/dist）
RUN npm run build

# =========================================
# 阶段 2：准备 Nginx 以提供静态文件
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 从构建阶段复制静态构建输出到 Nginx 的默认 HTML 服务目录
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# 使用内置的非根用户以符合安全最佳实践
USER nginx

# 暴露端口 8080 以允许 HTTP 流量
# 注意：默认 NGINX 容器现在在端口 8080 上监听而非 80
EXPOSE 8080

# 直接使用自定义配置启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> [!NOTE]
> 我们使用 nginx-unprivileged 而不是标准 NGINX 镜像以遵循安全最佳实践。
> 在最终镜像中以非根用户运行：
>- 减少攻击面
>- 符合 Docker 关于容器加固的建议
>- 有助于符合生产环境中更严格的安全策略

{{< /tab >}}
{{< /tabs >}}

### 第 3 步：配置 .dockerignore 文件

.dockerignore 文件告诉 Docker 在构建镜像时排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>- 减少镜像大小  
>- 加速构建过程  
>- 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 有关更多信息，请访问 [.dockerignore 参考文档](/reference/dockerfile.md#dockerignore-file)。

复制并替换现有 .dockerignore 文件的内容为以下配置：

```dockerignore
# 忽略依赖项和构建输出
node_modules/
dist/
out/
.tmp/
.cache/

# 忽略 Vite、Webpack 和 React 特定的构建工件
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

# 忽略 TypeScript 构建工件（如果使用 TypeScript）
*.tsbuildinfo

# 忽略锁定文件（如果使用 Docker 安装包，可选）
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

# 忽略构建特定的缓存文件
*.lock

```

### 第 4 步：创建 `nginx.conf` 文件

为了在容器内高效地提供您的 React.js 应用程序，您将使用自定义设置配置 NGINX。此配置针对性能、浏览器缓存、gzip 压缩和客户端路由支持进行了优化。

在项目目录的根目录下创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 有关配置 NGINX 的更多信息，请参阅 [官方 NGINX 文档](https://nginx.org/en/docs/)。

```nginx
worker_processes auto;

# 在 /tmp 中存储 PID（始终可写）
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # 禁用日志记录以避免权限问题
    access_log off;
    error_log  /dev/stderr warn;

    # 优化静态文件提供
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # 为优化传递启用 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    gzip_vary on;

    server {
        listen       8080;
        server_name  localhost;

        # 存放 React.js 构建文件的根目录
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

### 第 5 步：构建 React.js 应用程序镜像

在自定义配置就位后，您现在可以为 React.js 应用程序构建 Docker 镜像。

更新的设置包括：

- 优化的浏览器缓存和 gzip 压缩  
- 安全的非根日志记录以避免权限问题  
- 通过将未匹配的路由重定向到 `index.html` 来支持 React 客户端路由  

完成上一步后，您的项目目录现在应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

现在 Dockerfile 已配置，您可以为 React.js 应用程序构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将您的应用程序打包成镜像。它包含来自当前目录的所有必要文件（称为[构建上下文](/build/concepts/context/#what-is-a-build-context)）。

从项目的根目录运行以下命令：

```console
$ docker build --tag docker-reactjs-sample .
```

此命令的作用：
- 使用当前目录（.）中的 Dockerfile
- 将应用程序及其依赖项打包成 Docker 镜像
- 将镜像标记为 docker-reactjs-sample，以便稍后引用


#### 第 6 步：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 查看本地机器上可用的镜像。由于您已经在终端中工作，让我们使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-reactjs-sample     latest            f39b47a97156   14 seconds ago   75.8MB
```

此输出提供了关于您的镜像的关键信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 有助于标识不同构建版本的标签（例如 latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 表示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该能看到列出的 `docker-reactjs-sample` 镜像。

---

## 运行容器化应用程序

在上一步中，您为 React.js 应用程序创建了 Dockerfile 并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用程序是否按预期工作。

在 `docker-reactjs-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该看到一个简单的 React.js 网页应用。

按 `ctrl+c` 停止应用程序。

### 在后台运行应用程序

通过添加 `-d` 选项，您可以将应用程序与终端分离运行。在 `docker-reactjs-sample` 目录内，在终端中运行以下命令。

```console
$ docker compose up --build -d
```

在浏览器中访问 [http://localhost:8080](http://localhost:8080) 查看应用程序。您应该看到一个简单的网页应用预览。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动的容器及其端口、名称和状态。查找暴露端口 8080 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
88bced6ade95   docker-reactjs-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-reactjs-sample-server-1
```


要停止应用程序，请运行：

```console
$ docker compose down
```


> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> 参考文档](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 React.js 应用程序。通过遵循最佳实践，您创建了一个安全、优化且生产就绪的设置。

您完成的内容：
- 使用 `docker init` 初始化项目以生成必要的 Docker 配置文件。
- 用多阶段构建替换了默认的 `Dockerfile`，该构建编译 React.js 应用程序并使用 Nginx 提供静态文件。
- 用自定义 `.dockerignore` 文件替换了默认文件，以排除不必要的文件并保持镜像干净高效。
- 使用 `docker build` 构建了 Docker 镜像。
- 以前台和分离模式运行容器。
- 通过访问 [http://localhost:8080](http://localhost:8080) 验证了应用程序正在运行。
- 学会了如何使用 `docker compose down` 停止容器化应用程序。

现在您拥有了一个完全容器化的 React.js 应用程序，在 Docker 容器中运行，并准备好在任何环境中进行部署，具有信心和一致性。

---

## 相关资源

探索官方参考和最佳实践，以提升您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。  
- [Docker 中的构建上下文](/build/concepts/context/) – 了解构建上下文如何影响镜像构建。  
- [`docker init` CLI 参考文档](/reference/cli/docker/init/) – 自动生成 Docker 资产。
- [`docker build` CLI 参考文档](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考文档](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考文档](/reference/cli/docker/compose/up/) – 启动和运行多容器应用程序。
- [`docker compose down` CLI 参考文档](/reference/cli/docker/compose/down/) – 停止并删除容器、网络和卷。

---

## 下一步

您的 React.js 应用程序现在已经容器化，您已准备好进行下一步。

在下一部分中，您将学习如何使用 Docker 容器开发您的应用程序，从而在任何机器上实现一致、隔离且可重现的开发环境。