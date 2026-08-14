# Angular 语言专项指南


Angular 语言专项指南将向你展示如何使用 Docker 容器化 Angular 应用，并遵循创建高效、可用于生产的容器的最佳实践。

[Angular](https://angular.dev/) 是一个健壮且被广泛采用的框架，用于构建动态的企业级 Web 应用。然而随着应用规模扩大，管理依赖、环境和部署会变得复杂。Docker 通过为开发和生产提供一致、隔离的环境，简化了这些难题。

> **致谢**
>
> Docker 诚挚感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 撰写本指南。作为 Docker Captain 和资深前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业经验使这份资源成为社区的重要参考，帮助开发者理清并优化他们的 Docker 工作流。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 Angular 应用。
- 在容器内为 Angular 搭建本地开发环境。
- 在 Docker 容器中为你的 Angular 应用运行测试。

你将从容器化一个现有的 Angular 应用开始，逐步深入到生产级部署。

---

## 前提条件

开始之前，请确保你具备以下方面的实用知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 的基本理解。
- 熟悉使用 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 来管理依赖和运行脚本。
- 熟悉 [Angular](https://angular.io/) 基础知识。
- 理解镜像、容器和 Dockerfile 等 Docker 核心概念。如果你是 Docker 新手，请先阅读 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南。

完成 Angular 入门模块后，你就完全准备好参照本指南中详细的示例和最佳实践来容器化自己的 Angular 应用了。

## Containerize an Angular Application（容器化 Angular 应用）

### 前提条件

开始之前，请确保系统上已安装并可使用以下工具：

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你拥有一个 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但你可以使用任意客户端。

> **Docker 新手？**  
> 请先阅读 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南，熟悉镜像、容器和 Dockerfile 等关键概念。

---

### 概述

本指南将带你完整走完使用 Docker 容器化 Angular 应用的流程。你将学习如何遵循能够提升性能、安全性、可扩展性和部署效率的最佳实践，创建可用于生产的 Docker 镜像。

在本指南结束时，你将：

- 使用 Docker 容器化一个 Angular 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建最小化镜像体积。
- 通过自定义的 Nginx 配置高效地提供应用服务。
- 遵循最佳实践构建安全且易维护的 Docker 镜像。

---

### 获取示例应用

克隆本指南所使用的示例应用。打开终端，切换到你想要工作的目录，然后运行以下命令克隆该 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-angular-sample
```

---

### 构建 Docker 镜像

Angular 是一个会编译为静态资源的前端框架，因此该 Dockerfile 使用多阶段构建：一个阶段用 Node.js 编译应用，第二个精简阶段用 Nginx 提供静态输出的服务。

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

**Using Docker Hardened Images**


[Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/node)中提供了 Node.js 的 Docker Hardened Images (DHIs)。Docker Hardened Images 对所有人免费开放，无需订阅。登录 DHI 镜像仓库后，你可以像使用其他 Docker 镜像一样拉取并使用它们。更多信息请参阅 [DHI 快速入门](/dhi/get-started/)指南。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（可用版本请查看目录）：
   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

在下面的 Dockerfile 中，`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev` 作为基础镜像。

```dockerfile
# =========================================
# Stage 1: Build the Angular Application
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

# Build the Angular application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# Use a non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

**Using the Docker Official Image**



创建一个名为 `Dockerfile` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Build the Angular Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json *package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Angular application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

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

`.dockerignore` 文件告诉 Docker 在构建镜像时排除哪些文件和目录。

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
# ================================
# Node and build output
# ================================
node_modules
dist
out-tsc
.angular
.cache
.tmp

# ================================
# Testing & Coverage
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
# Environment & log files
# ================================
*.env*
!*.env.production
*.log
*.tsbuildinfo

# ================================
# IDE & OS-specific files
# ================================
.vscode
.idea
.DS_Store
Thumbs.db
*.swp

# ================================
# Version control & CI files
# ================================
.git
.gitignore

# ================================
# Docker & local orchestration
# ================================
Dockerfile
Dockerfile.*
.dockerignore
docker-compose.yml
docker-compose*.yml

# ================================
# Miscellaneous
# ================================
*.bak
*.old
*.tmp
```

#### 第 4 步：创建 `nginx.conf` 文件

为了在容器内高效地提供 Angular 应用服务，你需要用自定义配置来设置 Nginx。该配置针对性能、浏览器缓存、gzip 压缩以及客户端路由支持做了优化。

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

    client_body_temp_path /tmp/client_temp;
    proxy_temp_path       /tmp/proxy_temp_path;
    fastcgi_temp_path     /tmp/fastcgi_temp;
    uwsgi_temp_path       /tmp/uwsgi_temp;
    scgi_temp_path        /tmp/scgi_temp;

    # Logging
    access_log off;
    error_log  /dev/stderr warn;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # Compression
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

        # Angular Routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Static Assets Caching
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # Optional: Explicit asset route
        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

#### 第 5 步：构建 Angular 应用镜像

自定义配置就位后，你现在可以为 Angular 应用构建 Docker 镜像了。

更新后的配置包括：

- 一份干净、可用于生产、专为 Angular 定制的 Nginx 配置。
- 高效的多阶段 Docker 构建，确保最终镜像小巧且安全。

完成前面的步骤后，你的项目目录中现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

现在 Dockerfile 已配置完成，你可以为 Angular 应用构建 Docker 镜像了。

> [!NOTE]
> `docker build` 命令按照 Dockerfile 中的指令把你的应用打包成镜像。它会包含当前目录（即[构建上下文](/build/concepts/context/#what-is-a-build-context)）中所有必需的文件。

在项目根目录运行以下命令：

```console
$ docker build --tag docker-angular-sample .
```

该命令的作用：

- 使用当前目录 (.) 中的 Dockerfile
- 将应用及其依赖打包成 Docker 镜像
- 将镜像标记为 docker-angular-sample，方便你后续引用

#### 第 6 步：查看本地镜像

构建完 Docker 镜像后，你可以通过 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 查看本机上有哪些镜像可用。既然你已经在终端中操作，我们就使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-angular-sample     latest            34e66bdb9d40   14 seconds ago   76.4MB
```

该输出提供了关于镜像的关键信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 用于区分不同构建的版本标签（例如 latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 表示镜像构建时间的时间戳。
- **Size** – 镜像占用的磁盘空间总量。

如果构建成功，你应该能在列表中看到 `docker-angular-sample` 镜像。

---

### 运行容器化应用

在上一步中，你为 Angular 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在该在容器中运行该镜像，并验证应用是否按预期工作了。

在 `docker-angular-sample` 目录内的终端中运行以下命令。

```console
$ docker compose up --build
```

打开浏览器访问 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简单的 Angular Web 应用。

在终端中按 `ctrl+c` 停止应用。

#### 在后台运行应用

你可以通过添加 `-d` 选项让应用脱离终端在后台运行。在 `docker-angular-sample` 目录内的终端中运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:8080](http://localhost:8080)。你应该能在浏览器中看到你的 Angular 应用正在运行。

要确认容器正在运行，使用 `docker ps` 命令：

```console
$ docker ps
```

这会列出所有活动容器及其端口、名称和状态。查找暴露 8080 端口的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
eb13026806d1   docker-angular-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-angular-sample-server-1
```

要停止应用，运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

---

## Use containers for Angular development（使用容器进行 Angular 开发）

### 前提条件

完成[容器化 Angular 应用](#containerize-an-angular-application)。

---

### 概述

在本节中，你将学习如何使用 Docker Compose 为容器化的 Angular 应用同时搭建生产环境和开发环境。这套配置让你既能通过 Nginx 提供静态生产构建的服务，又能借助 Compose Watch 的实时重载开发服务器在容器内高效开发。

你将学习如何：

- 为生产和开发分别配置独立的容器
- 在开发中使用 Compose Watch 启用自动文件同步
- 无需手动重建即可实时调试和预览你的改动

---

### 自动更新服务（开发模式）

使用 Compose Watch 自动将源文件变更同步到容器化的开发环境中。这提供了无缝高效的开发体验，无需手动重启或重建容器。

### 第 1 步：创建开发用 Dockerfile

在项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Development - Angular Application
# =========================================

# Define the Node.js version to use (Alpine for a small footprint)
ARG NODE_VERSION=24.12.0-alpine

# Set the base image for development
FROM node:${NODE_VERSION} AS dev

# Set environment variable to indicate development mode
ENV NODE_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependency files first to optimize Docker caching
COPY package.json package-lock.json* ./

# Install dependencies using npm with caching to speed up subsequent builds
RUN --mount=type=cache,target=/root/.npm npm install

# Copy all application source files into the container
COPY . .

# Expose the port Angular uses for the dev server (default is 4200)
EXPOSE 4200

# Start the Angular dev server and bind it to all network interfaces
CMD ["npm", "start", "--", "--host=0.0.0.0"]

```

该文件使用开发服务器为你的 Angular 应用搭建了一个轻量的开发环境。

#### 第 2 步：更新你的 `compose.yaml` 文件

打开 `compose.yaml` 文件，定义两个服务：一个用于生产（`angular-prod`），一个用于开发（`angular-dev`）。

以下是 Angular 应用的示例配置：

```yaml
services:
  angular-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-angular-sample
    ports:
      - "8080:8080"

  angular-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "4200:4200"
    develop:
      watch:
        - action: sync
          path: .
          target: /app
```

- `angular-prod` 服务构建并通过 Nginx 提供你的静态生产应用服务。
- `angular-dev` 服务运行带有实时重载和热模块替换的 Angular 开发服务器。
- `watch` 会触发 Compose Watch 的文件同步。

> [!NOTE]
> 更多细节请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

完成前面的步骤后，你的项目目录中现在应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 4 步：启动 Compose Watch

在项目根目录运行以下命令，以 watch 模式启动容器

```console
$ docker compose watch angular-dev
```

#### 第 5 步：在 Angular 中测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在文本编辑器中打开 `src/app/app.component.html` 文件。

2. 找到以下这一行：

   ```html
   <h1>Docker Angular Sample Application</h1>
   ```

3. 将其改为：

   ```html
   <h1>Hello from Docker Compose Watch</h1>
   ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:4200](http://localhost:4200)。

你应该会立刻看到更新后的文本，无需手动重建容器。这确认了文件监视和自动同步正按预期工作。

---

## 在容器中运行 Angular 测试

### 前提条件

完成本指南前面的所有章节，从[容器化 Angular 应用](#containerize-an-angular-application)开始。

### 概述

测试是开发流程中至关重要的一环。在本节中，你将学习如何：

- 在 Docker 容器内使用 Angular CLI 运行 Jasmine 单元测试。
- 使用 Docker Compose 隔离你的测试环境。
- 确保本地测试与基于容器的测试之间保持一致。

`docker-angular-sample` 项目已预先配置好 Jasmine，因此你无需额外设置即可快速上手。

---

### 在开发过程中运行测试

`docker-angular-sample` 应用在以下位置包含一个示例测试文件：

```console
$ src/app/app.component.spec.ts
```

该测试使用 Jasmine 来验证 AppComponent 的逻辑。

#### 第 1 步：更新 compose.yaml

在 `compose.yaml` 文件中添加一个名为 `angular-test` 的新服务。该服务让你能够在隔离的容器化环境中运行测试套件。

```yaml {hl_lines="22-26",linenos=true}
services:
  angular-dev:
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

  angular-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-angular-sample
    ports:
      - "8080:8080"

  angular-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test"]
```

angular-test 服务复用了[开发](#use-containers-for-angular-development)所用的同一个 `Dockerfile.dev`，并覆盖默认命令以通过 `npm run test` 运行测试。这种配置确保测试环境与本地开发配置保持一致。

完成前面的步骤后，你的项目目录中应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 2 步：运行测试

要在容器内执行测试套件，请在项目根目录运行以下命令：

```console
$ docker compose run --rm angular-test
```

该命令会：

- 启动 `compose.yaml` 文件中定义的 `angular-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 通过 [`docker compose run --rm`](/reference/cli/docker/compose/run/) 命令，在测试完成后自动删除容器。

你应该会看到类似下面的输出：

```shell
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.529 s
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

---

### 小结

在本节中，你学习了如何使用 Jasmine 和 Docker Compose 在 Docker 容器内为 Angular 应用运行单元测试。

你完成的工作：

- 在 `compose.yaml` 中创建了 `angular-test` 服务以隔离测试执行。
- 复用开发用的 `Dockerfile.dev`，确保开发环境与测试环境一致。
- 使用 `docker compose run --rm angular-test` 在容器内运行测试。
- 实现了跨环境可靠、可重复的测试，不再依赖本机的环境配置。

---

### 相关资源

浏览官方参考资料和最佳实践，磨练你的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、易维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 学习在 `compose.yaml` 中配置服务的完整语法和可用选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。

