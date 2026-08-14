---
title: Vue.js 语言专项指南
linkTitle: Vue.js
description: 使用 Docker 容器化并开发 Vue.js 应用
keywords: getting started, vue, vuejs docker, language, Dockerfile
summary: |
  本指南介绍如何使用 Docker 容器化 Vue.js 应用。
aliases:
  - /frameworks/vue/
  - /guides/vuejs/configure-github-actions/
  - /guides/vuejs/containerize/
  - /guides/vuejs/deploy/
  - /guides/vuejs/develop/
  - /guides/vuejs/run-tests/
params:
  tags: [languages]
  time: 20 minutes
---

Vue.js 语言专项指南将向你展示如何使用 Docker 容器化 Vue.js 应用，并遵循创建高效、可用于生产的容器的最佳实践。

[Vue.js](https://vuejs.org/) 是一个渐进式且灵活的框架，用于构建现代化的交互式 Web 应用。然而随着应用规模扩大，管理依赖、环境和部署会变得复杂。Docker 通过为开发和生产提供一致、隔离的环境，简化了这些难题。

> **致谢**
>
> Docker 诚挚感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 撰写本指南。作为 Docker Captain 和技术精湛的前端工程师，Kristiyan 在现代 Web 开发、Docker 和 DevOps 方面带来了卓越的专业经验。他注重实操的方式和清晰、可落地的指引，使本指南成为那些希望用 Docker 构建、优化并保障 Vue.js 应用安全的开发者的重要资源。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 Vue.js 应用。
- 在容器内为 Vue.js 搭建本地开发环境。
- 在 Docker 容器中为你的 Vue.js 应用运行测试。

你将从容器化一个现有的 Vue.js 应用开始，逐步深入到生产级部署。

---

## 前提条件

开始之前，请确保你具备以下方面的实用知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 的基本理解。
- 熟悉使用 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 来管理依赖和运行脚本。
- 熟悉 [Vue.js](https://vuejs.org/) 基础知识。
- 理解镜像、容器和 Dockerfile 等 Docker 核心概念。如果你是 Docker 新手，请先阅读 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南。

完成 Vue.js 入门模块后，你就完全准备好参照本指南中详细的示例和最佳实践来容器化自己的 Vue.js 应用了。

## Containerize an Vue.js Application（容器化 Vue.js 应用）

### 前提条件

开始之前，请确保系统上已安装并可使用以下工具：

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你拥有一个 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但你可以使用任意客户端。

> **Docker 新手？**  
> 请先阅读 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南，熟悉镜像、容器和 Dockerfile 等关键概念。

---

### 概述

本指南将带你完整走完使用 Docker 容器化 Vue.js 应用的流程。你将学习如何遵循能够提升性能、安全性、可扩展性和部署效率的最佳实践，创建可用于生产的 Docker 镜像。

在本指南结束时，你将：

- 使用 Docker 容器化一个 Vue.js 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建最小化镜像体积。
- 通过自定义的 Nginx 配置高效地提供应用服务。
- 遵循最佳实践构建安全且易维护的 Docker 镜像。

---

### 获取示例应用

克隆本指南所使用的示例应用。打开终端，切换到你想要工作的目录，然后运行以下命令克隆该 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-vuejs-sample
```

---

### 构建 Docker 镜像

Vue.js 是一个会编译为静态资源的前端框架，因此该 Dockerfile 做了定制，以契合 Vue.js 应用在生产环境中的构建方式和高效服务方式。

> [!TIP]
>
> Docker 的 AI 助手 [Gordon](/ai/gordon/) 可以为你的项目生成 Docker 资产文件。你可以让 Gordon 创建适配你应用的 Dockerfile、Compose 文件和 `.dockerignore`。

#### 第 1 步：创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node)，也可以使用来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog)的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于获得一个轻量且安全、可用于生产的镜像。更多信息请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用了一个在撰写时被认为安全的稳定 Node.js LTS 镜像标签。由于新版本和安全补丁会定期发布，当你阅读本指南时这里展示的标签可能已不再是最安全的选择。在构建或部署应用之前，请务必查看最新可用的镜像标签，并选择一个安全、最新的版本。
>
> Node.js 官方 Docker 镜像：https://hub.docker.com/_/node

{{< tabs >}}
{{< tab name="Using Docker Hardened Images" >}}
[Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/node)中提供了 Node.js 的 Docker Hardened Images (DHIs)。Docker Hardened Images 对所有人免费开放，无需订阅。登录 DHI 镜像仓库后，你可以像使用其他 Docker 镜像一样拉取并使用它们。更多信息请参阅 [DHI 快速入门](/dhi/get-started/)指南。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（可用版本请查看目录）：

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. 拉取 Nginx DHI（可用版本请查看目录）：
   ```console
   $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
   ```

在下面的 Dockerfile 中，`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev` 和 `dhi.io/nginx:1.28.0-alpine3.21-dev` 作为基础镜像。

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
# Use a lightweight DHI Node.js image for building
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

{{< /tab >}}
{{< tab name="Using the Docker Official Image" >}}

创建一个名为 `Dockerfile` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

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

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> [!NOTE]
> 我们使用 nginx-unprivileged 而非标准 Nginx 镜像，以遵循安全最佳实践。
> 在最终镜像中以非 root 用户运行可以：
>
> - 减小攻击面
> - 契合 Docker 关于容器加固的建议
> - 有助于满足生产环境中更严格的安全策略

{{< /tab >}}
{{< /tabs >}}

#### 第 2 步：创建 compose.yaml 文件

创建一个名为 `compose.yaml` 的文件，内容如下：

```yaml {collapse=true,title=compose.yaml}
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
```

#### 第 3 步：创建 .dockerignore 文件

`.dockerignore` 文件通过指定哪些文件和目录应从构建上下文中排除，在优化 Docker 镜像方面起着关键作用。

> [!NOTE]
> 这有助于：
>
> - 减小镜像体积
> - 加快构建过程
> - 防止敏感或无用文件（例如 `.env`、`.git` 或 `node_modules`）被加入最终镜像。
>
> 要了解更多，请参阅 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

创建一个名为 `.dockerignore` 的文件，内容如下：

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

#### 第 4 步：创建 `nginx.conf` 文件

为了在容器内高效地提供 Vue.js 应用服务，你需要用自定义配置来设置 Nginx。该配置针对性能、浏览器缓存、gzip 压缩以及客户端路由支持做了优化。

在项目根目录中创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解更多关于配置 Nginx 的信息，请参阅 [Nginx 官方文档](https://nginx.org/en/docs/)。

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

#### 第 5 步：构建 Vue.js 应用镜像

自定义配置就位后，你现在可以为 Vue.js 应用构建 Docker 镜像了。

更新后的配置包括：

- 一份干净、可用于生产、专为 Vue.js 定制的 Nginx 配置。
- 高效的多阶段 Docker 构建，确保最终镜像小巧且安全。

完成前面的步骤后，你的项目目录中现在应包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

现在 Dockerfile 已配置完成，你可以为 Vue.js 应用构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令按照 Dockerfile 中的指令把你的应用打包成镜像。它会包含当前目录（即[构建上下文](/build/concepts/context/#what-is-a-build-context)）中所有必需的文件。

在项目根目录运行以下命令：

```console
$ docker build --tag docker-vuejs-sample .
```

该命令的作用：

- 使用当前目录 (.) 中的 Dockerfile
- 将应用及其依赖打包成 Docker 镜像
- 将镜像标记为 docker-vuejs-sample，方便你后续引用

#### 第 6 步：查看本地镜像

构建完 Docker 镜像后，你可以通过 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 查看本机上有哪些镜像可用。既然你已经在终端中操作，我们就使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-vuejs-sample       latest            8c9c199179d4   14 seconds ago   76.2MB
```

该输出提供了关于镜像的关键信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 用于区分不同构建的版本标签（例如 latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 表示镜像构建时间的时间戳。
- **Size** – 镜像占用的磁盘空间总量。

如果构建成功，你应该能在列表中看到 `docker-vuejs-sample` 镜像。

---

### 运行容器化应用

在上一步中，你为 Vue.js 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在该在容器中运行该镜像，并验证应用是否按预期工作了。

在 `docker-vuejs-sample` 目录内的终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器访问 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简单的 Vue.js Web 应用。

在终端中按 `ctrl+c` 停止应用。

#### 在后台运行应用

你可以通过添加 `-d` 选项让应用脱离终端在后台运行。在 `docker-vuejs-sample` 目录内的终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:8080](http://localhost:8080)。你应该能在浏览器中看到你的 Vue.js 应用正在运行。

要确认容器正在运行，使用 `docker ps` 命令：

```console
$ docker ps
```

这会列出所有活动容器及其端口、名称和状态。查找暴露 8080 端口的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
37a1fa85e4b0   docker-vuejs-sample-server     "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-vuejs-sample-server-1
```

要停止应用，运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

---

## Use containers for Vue.js development（使用容器进行 Vue.js 开发）

### 前提条件

完成[容器化 Vue.js 应用](#containerize-an-vuejs-application)。

---

### 概述

在本节中，你将使用 Docker Compose 为 Vue.js 应用同时搭建生产环境和开发环境。这种方式能精简你的工作流——在生产中通过 Nginx 提供轻量的静态站点，同时借助 Compose Watch 提供快速、实时重载的开发服务器以实现高效的本地开发。

你将学习如何：

- 配置隔离环境：为生产和开发用例分别搭建经过优化的独立容器。
- 开发中实时重载：使用 Compose Watch 自动同步文件改动，无需手动干预即可实时更新。
- 轻松预览与调试：在容器内开发，享受无缝的预览与调试体验——每次改动后无需重建。

---

### 自动更新服务（开发模式）

利用 Compose Watch，在你的本机与容器化的 Vue.js 开发环境之间实现实时文件同步。这项强大的功能省去了手动重建或重启容器的麻烦，带来快速、无缝且高效的开发工作流。

有了 Compose Watch，你的代码更新会立即反映到容器内——非常适合快速测试、调试和实时预览改动。

### 第 1 步：创建开发用 Dockerfile

在项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Develop the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine

# Use a lightweight Node.js image for development
FROM node:${NODE_VERSION} AS dev

# Set environment variable to indicate development mode
ENV NODE_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the application source code into the container
COPY . .

# Change ownership of the application directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port used by the Vite development server
EXPOSE 5173

# Use a default command, can be overridden in Docker compose.yml file
CMD [ "npm", "run", "dev", "--", "--host" ]

```

该文件使用开发服务器为你的 Vue.js 应用搭建了一个轻量的开发环境。

#### 第 2 步：更新你的 `compose.yaml` 文件

打开 `compose.yaml` 文件，定义两个服务：一个用于生产（`vuejs-prod`），一个用于开发（`vuejs-dev`）。

以下是 Vue.js 应用的示例配置：

```yaml
services:
  vuejs-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-vuejs-sample
    ports:
      - "8080:8080"

  vuejs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - path: ./src
          target: /app/src
          action: sync
        - path: ./package.json
          target: /app/package.json
          action: restart
        - path: ./vite.config.js
          target: /app/vite.config.js
          action: restart
```

- `vuejs-prod` 服务构建并通过 Nginx 提供你的静态生产应用服务。
- `vuejs-dev` 服务运行带有实时重载和热模块替换的 Vue.js 开发服务器。
- `watch` 会触发 Compose Watch 的文件同步。

> [!NOTE]
> 更多细节请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，你的项目目录中现在应包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 4 步：启动 Compose Watch

在项目根目录运行以下命令，以 watch 模式启动容器

```console
$ docker compose watch vuejs-dev
```

#### 第 5 步：在 Vue.js 中测试 Compose Watch

要确认 Compose Watch 正常工作：

1. 在文本编辑器中打开 `src/App.vue` 文件。

2. 找到以下这一行：

   ```html
   <HelloWorld msg="You did it!" />
   ```

3. 将其改为：

   ```html
   <HelloWorld msg="Hello from Docker Compose Watch" />
   ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:5173](http://localhost:5173)。

你应该会立刻看到更新后的文本，无需手动重建容器。这确认了文件监视和自动同步正按预期工作。

---

## 在容器中运行 Vue.js 测试

### 前提条件

完成本指南前面的所有章节，从[容器化 Vue.js 应用](#containerize-an-vuejs-application)开始。

### 概述

测试是开发流程中至关重要的一环。在本节中，你将学习如何：

- 在 Docker 容器内使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离、可复现的环境中运行测试。

你将使用 [Vitest](https://vitest.dev)（一个为 Vite 设计的极速测试运行器）配合 [@vue/test-utils](https://test-utils.vuejs.org/) 来编写单元测试，验证组件逻辑、props、事件和响应式行为。

这套配置确保你的 Vue.js 组件在一个贴近用户实际交互方式的环境中受到测试。

---

### 在开发过程中运行测试

`docker-vuejs-sample` 应用在以下位置包含一个示例测试文件：

```console
$ src/components/__tests__/HelloWorld.spec.ts
```

该测试使用 Vitest 和 Vue Test Utils 来验证 HelloWorld 组件的行为。

---

#### 第 1 步：更新 compose.yaml

在 `compose.yaml` 文件中添加一个名为 `vuejs-test` 的新服务。该服务让你能够在隔离的容器化环境中运行测试套件。

```yaml {hl_lines="22-26",linenos=true}
services:
  vuejs-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-vuejs-sample
    ports:
      - "8080:8080"

  vuejs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - action: sync
          path: .
          target: /app

  vuejs-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test:unit"]
```

vuejs-test 服务复用了[开发](#use-containers-for-vuejs-development)所用的同一个 `Dockerfile.dev`，并覆盖默认命令以通过 `npm run test` 运行测试。这种配置确保测试环境与本地开发配置保持一致。

完成前面的步骤后，你的项目目录中应包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 2 步：运行测试

要在容器内执行测试套件，请在项目根目录运行以下命令：

```console
$ docker compose run --rm vuejs-test
```

该命令会：

- 启动 `compose.yaml` 文件中定义的 `vuejs-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 通过 [`docker compose run --rm`](/reference/cli/docker/compose/run/) 命令，在测试完成后自动删除容器。

你应该会看到类似下面的输出：

```shell
Test Files: 1 passed (1)
Tests:      1 passed (1)
Start at:   16:50:55
Duration:   718ms
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

---

### 小结

在本节中，你学习了如何使用 Vitest 和 Docker Compose 在 Docker 容器内为 Vue.js 应用运行单元测试。

你完成的工作：

- 在 `compose.yaml` 中创建了 `vuejs-test` 服务以隔离测试执行。
- 复用开发用的 `Dockerfile.dev`，确保开发环境与测试环境一致。
- 使用 `docker compose run --rm vuejs-test` 在容器内运行测试。
- 实现了跨环境可靠、可重复的测试，不再依赖本机的环境配置。

---

### 相关资源

浏览官方参考资料和最佳实践，磨练你的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、易维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 学习在 `compose.yaml` 中配置服务的完整语法和可用选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。
