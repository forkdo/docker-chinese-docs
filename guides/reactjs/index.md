# React.js 语言专项指南


React.js 语言专项指南将向你展示如何使用 Docker 容器化 React.js 应用，并遵循最佳实践来创建高效、可投入生产的容器。

[React.js](https://react.dev/) 是一个被广泛用于构建交互式用户界面的库。然而，高效地管理依赖、环境和部署可能相当复杂。Docker 通过提供一致、容器化的环境简化了这一过程。

> **致谢**
>
> Docker 诚挚感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 撰写本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专长让本资源对社区极具价值，帮助开发者驾驭并优化他们的 Docker 工作流。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行一个 React.js 应用。
- 在容器内搭建 React.js 本地开发环境。
- 在 Docker 容器内为你的 React.js 应用运行测试。

首先，你将从容器化一个已有的 React.js 应用开始。

---

## 先决条件

在开始之前，请确保你已熟悉以下内容：

- 对 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 或 [TypeScript](https://www.typescriptlang.org/) 的基本了解。
- 对用于管理依赖和运行脚本的 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 的基本知识。
- 熟悉 [React.js](https://react.dev/) 基础知识。
- 理解镜像、容器和 Dockerfile 等 Docker 概念。如果你刚接触 Docker，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 React.js 入门模块后，你就可以使用本指南提供的示例和说明来容器化你自己的 React.js 应用了。

## Containerize a React.js Application

### 先决条件

在开始之前，请确保你的系统上已安装并可用以下工具：

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你也可以使用任意客户端。

> **刚接触 Docker？**
> 从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等核心概念。

---

### 概述

本指南将带你完整走一遍使用 Docker 容器化 React.js 应用的过程。你将学习如何使用最佳实践创建可用于生产环境的 Docker 镜像，从而提升性能、安全性、可扩展性和部署效率。

完成本指南后，你将能够：

- 使用 Docker 容器化一个 React.js 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建来最小化镜像体积。
- 通过自定义的 NGINX 配置高效地提供应用服务。
- 遵循构建安全、可维护的 Docker 镜像的最佳实践。

---

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想在此工作的目录，并运行以下命令来克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-reactjs-sample
```

---

### 构建 Docker 镜像

React.js 是一个会被编译成静态资源的前端库，因此 Dockerfile 专门针对生产环境中 React 应用的构建和提供服务进行了优化。

> [!TIP]
>
> [Gordon](/ai/gordon/)，Docker 的 AI 助手，可以为你的项目生成 Docker 相关文件。让 Gordon 创建专为你的应用定制的 Dockerfile、Compose 文件以及 `.dockerignore`。

#### 第 1 步：创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node)，也可以使用来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image（DHI）。

选择 DHI 的优势在于它提供轻量且安全的、可投入生产的镜像。更多信息请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用的是编写时被认为安全的稳定版 Node.js LTS 镜像标签。由于新版本和安全补丁会定期发布，当你参考本指南时，此处显示的标签可能已不再是最安全的选择。在构建或部署你的应用之前，请始终查看最新的可用镜像标签，并选择安全、最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node

**使用 Docker Hardened Images**


Docker Hardened Images（DHI）在 [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/node) 中提供 Node.js 版本。Docker Hardened Images 对所有人免费提供，无需订阅。登录 DHI 镜像仓库后，你可以像使用任何其他 Docker 镜像一样拉取和使用它们。更多信息请参阅 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（请查看目录中可用的版本）：

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. 拉取 Nginx DHI（请查看目录中可用的版本）：

   ```console
   $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
   ```

在下面的 Dockerfile 中，`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev` 和 `dhi.io/nginx:1.28.0-alpine3.21-dev` 作为基础镜像。

```dockerfile
# =========================================
# Stage 1: Build the React.js Application
# =========================================

# Use a lightweight Node.js image for building (customizable via ARG)
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the React.js application (outputs to /app/dist)
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default NGINX container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

**使用 Docker Official Image**



创建一个名为 `Dockerfile` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Build the React.js Application
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

# Build the React.js application (outputs to /app/dist)
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
# Note: The default NGINX container now listens on port 8080 instead of 80
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> [!NOTE]
> 我们使用 nginx-unprivileged 而非标准 NGINX 镜像，以遵循安全最佳实践。
> 在最终镜像中以非 root 用户身份运行：
>
> - 缩小攻击面
> - 符合 Docker 关于容器加固的建议
> - 有助于在生产环境中遵守更严格的安全策略



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

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>
> - 减小镜像体积
> - 加速构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被加入最终镜像。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

创建一个名为 `.dockerignore` 的文件，内容如下：

```dockerignore
# Ignore dependencies and build output
node_modules/
dist/
out/
.tmp/
.cache/

# Ignore Vite, Webpack, and React-specific build artifacts
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

# Ignore environment and config files (sensitive data)
*.env*
*.log

# Ignore TypeScript build artifacts (if using TypeScript)
*.tsbuildinfo

# Ignore lockfiles (optional if using Docker for package installation)
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Ignore local development files
.git/
.gitignore
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db

# Ignore Docker-related files (to avoid copying unnecessary configs)
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml

# Ignore build-specific cache files
*.lock

```

#### 第 4 步：创建 `nginx.conf` 文件

为了在容器内高效地提供你的 React.js 应用，你将使用自定义配置来设置 NGINX。该配置针对性能、浏览器缓存、gzip 压缩以及客户端路由支持进行了优化。

在你的项目目录根目录下创建一个名为 `nginx.conf` 的文件，并添加以下内容：

> [!NOTE]
> 要了解更多关于配置 NGINX 的信息，请参阅 [NGINX 官方文档](https://nginx.org/en/docs/)。

```nginx
worker_processes auto;

# Store PID in /tmp (always writable)
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Disable logging to avoid permission issues
    access_log off;
    error_log  /dev/stderr warn;

    # Optimize static file serving
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # Gzip compression for optimized delivery
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    gzip_vary on;

    server {
        listen       8080;
        server_name  localhost;

        # Root directory where React.js build files are placed
        root /usr/share/nginx/html;
        index index.html;

        # Serve React.js static files with proper caching
        location / {
            try_files $uri /index.html;
        }

        # Serve static assets with long cache expiration
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # Handle React.js client-side routing
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

#### 第 5 步：构建 React.js 应用镜像

在完成自定义配置后，你现在可以构建 React.js 应用的 Docker 镜像了。

更新后的设置包含：

- 优化的浏览器缓存和 gzip 压缩
- 安全的、非 root 的日志记录，以避免权限问题
- 通过把未匹配的路由重定向到 `index.html` 来支持 React 客户端路由

完成前面的步骤后，你的项目目录现在应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

既然你的 Dockerfile 已配置完成，你可以构建 React.js 应用的 Docker 镜像了。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将你的应用打包成一个镜像。它包含当前目录（称为 [build context](/build/concepts/context/#what-is-a-build-context)）中的所有必要文件。

从你的项目根目录运行以下命令：

```console
$ docker build --tag docker-reactjs-sample .
```

该命令的作用：

- 使用当前目录（.）中的 Dockerfile
- 将应用及其依赖打包成一个 Docker 镜像
- 将镜像标记为 docker-reactjs-sample，以便你后续引用

#### 第 6 步：查看本地镜像

构建 Docker 镜像后，你可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 查看本地机器上可用的镜像。既然你已经在终端中工作，我们就使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-reactjs-sample     latest            f39b47a97156   14 seconds ago   75.8MB
```

该输出提供了关于你的镜像的关键信息：

- **Repository** —— 分配给镜像的名称。
- **Tag** —— 用于标识不同构建的版本标签（例如 latest）。
- **Image ID** —— 镜像的唯一标识符。
- **Created** —— 镜像构建时的时间戳。
- **Size** —— 镜像占用的总磁盘空间。

如果构建成功，你应该会看到 `docker-reactjs-sample` 镜像被列出。

---

### 运行容器化的应用

在上一步中，你为 React.js 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像，并验证你的应用是否按预期工作。

在 `docker-reactjs-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 React.js Web 应用。

在终端中按 `ctrl+c` 停止你的应用。

#### 在后台运行应用

你可以通过添加 `-d` 选项，让应用在终端之外以分离（detached）模式运行。在 `docker-reactjs-sample` 目录中，在终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器，在 [http://localhost:8080](http://localhost:8080) 查看应用。你应该会看到一个简易的 Web 应用预览。

要确认容器正在运行，使用 `docker ps` 命令：

```console
$ docker ps
```

这会列出所有活动容器及其端口、名称和状态。请寻找暴露了 8080 端口的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
88bced6ade95   docker-reactjs-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-reactjs-sample-server-1
```

要停止应用，运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> reference](/reference/cli/docker/compose/)。

---

## Use containers for React.js development

### 先决条件

完成 [Containerize React.js application](#containerize-a-reactjs-application)。

---

### 概述

在本节中，你将学习如何使用 Docker Compose 为容器化的 React.js 应用搭建生产环境和开发环境。该设置允许你通过 Nginx 提供静态生产构建，并使用带有 Compose Watch 的实时重载开发服务器在容器内高效开发。

你将学习如何：

- 为生产和开发配置独立的容器
- 在开发中使用 Compose Watch 启用自动文件同步
- 无需手动重建即可实时调试和实时预览你的修改

---

### 自动更新服务（开发模式）

使用 Compose Watch 自动将源文件变更同步到你的容器化开发环境。这提供了一种无缝、高效的开发体验，无需手动重启或重建容器。

### 第 1 步：创建开发用 Dockerfile

在你的项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下：

```dockerfile
# =========================================
# Stage 1: Develop the React.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine

# Use a lightweight Node.js image for development
FROM node:${NODE_VERSION} AS dev

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the application source code into the container
COPY . .

# Expose the port used by the Vite development server
EXPOSE 5173

# Use a default command, can be overridden in Docker compose.yml file
CMD ["npm", "run", "dev"]
```

该文件使用开发服务器为你的 React 应用搭建了一个轻量的开发环境。

#### 第 2 步：更新你的 `compose.yaml` 文件

打开你的 `compose.yaml` 文件，定义两个服务：一个用于生产（`react-prod`），一个用于开发（`react-dev`）。

下面是一个 React.js 应用的示例配置：

```yaml
services:
  react-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-reactjs-sample
    ports:
      - "8080:8080"

  react-dev:
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
```

- `react-prod` 服务使用 Nginx 构建并提供你的静态生产应用。
- `react-dev` 服务运行你的 React 开发服务器，支持实时重载和模块热替换。
- `watch` 触发与 Compose Watch 的文件同步。

> [!NOTE]
> 有关更多细节，请参阅官方指南：[Use Compose Watch](/manuals/compose/how-tos/file-watch.md)。

#### 第 3 步：更新 vite.config.ts 以确保其在 Docker 内正常工作

为了让 Vite 的开发服务器在 Docker 内可靠运行，你需要用正确的设置更新你的 vite.config.ts。

打开项目根目录下的 `vite.config.ts` 文件，并按如下方式更新：

```ts
/// <reference types="vitest" />

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/",
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
});
```

> [!NOTE]
> `vite.config.ts` 中的 `server` 选项对于在 Docker 内运行 Vite 至关重要：
>
> - `host: true` 允许开发服务器从容器外部访问。
> - `port: 5173` 设置一个一致开发端口（必须与 Docker 中暴露的端口匹配）。
> - `strictPort: true` 确保端口不可用时 Vite 明确失败，而不是静默切换。
>
> 更多细节请参阅 [Vite server 配置文档](https://vitejs.dev/config/server-options.html)。

完成前面的步骤后，你的项目目录现在应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 4 步：启动 Compose Watch

从你的项目根目录运行以下命令，以 watch 模式启动你的容器：

```console
$ docker compose watch react-dev
```

#### 第 5 步：用 React 测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在文本编辑器中打开 `src/App.tsx` 文件。

2. 找到以下这一行：

   ```html
   <h1>Vite + React</h1>
   ```

3. 将其改为：

   ```html
   <h1>Hello from Docker Compose Watch</h1>
   ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:5173](http://localhost:5173)。

你应该会看到更新后的文本立即出现，无需手动重建容器。这确认了文件监视和自动同步按预期工作。

---

## Run React.js tests in a container

### 先决条件

完成本指南之前的所有章节，从 [Containerize React.js application](#containerize-a-reactjs-application) 开始。

### 概述

测试是开发过程中至关重要的一部分。在本节中，你将学习如何：

- 在 Docker 容器内使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离、可复现的环境中运行测试。

你将使用 [Vitest](https://vitest.dev)（一个为 Vite 打造的极速测试运行器）以及 [Testing Library](https://testing-library.com/) 进行断言。

---

### 在开发期间运行测试

`docker-reactjs-sample` 应用包含一个位于如下位置的示例测试文件：

```console
$ src/App.test.tsx
```

该文件使用 Vitest 和 React Testing Library 来验证 `App` 组件的行为。

#### 第 1 步：安装 Vitest 和 React Testing Library

如果你尚未添加必要的测试工具，运行以下命令进行安装：

```console
$ npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

然后，更新你的 `package.json` 文件的 scripts 部分，加入以下内容：

```json
"scripts": {
  "test": "vitest run"
}
```

---

#### 第 2 步：配置 Vitest

用以下配置更新你项目根目录下的 `vitest.config.ts` 文件：

```ts {hl_lines="14-18",linenos=true}
/// <reference types="vitest" />

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/",
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/setupTests.ts",
    globals: true,
  },
});
```

> [!NOTE]
> `vitest.config.ts` 中的 `test` 选项对于在 Docker 内可靠测试至关重要：
>
> - `environment: "jsdom"` 模拟类似浏览器的环境用于渲染和 DOM 交互。
> - `setupFiles: "./src/setupTests.ts"` 在每个测试文件之前加载全局配置或 mock（可选但推荐）。
> - `globals: true` 启用全局测试函数，如 `describe`、`it` 和 `expect`，无需导入即可使用。
>
> 更多细节请参阅官方 [Vitest 配置文档](https://vitest.dev/config/)。

#### 第 3 步：更新 compose.yaml

向你的 `compose.yaml` 文件添加一个名为 `react-test` 的新服务。该服务让你在隔离的容器化环境中运行测试套件。

```yaml {hl_lines="22-26",linenos=true}
services:
  react-dev:
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

  react-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-reactjs-sample
    ports:
      - "8080:8080"

  react-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test"]
```

react-test 服务复用了与[开发](#use-containers-for-reactjs-development)相同的 `Dockerfile.dev`，并覆盖了默认命令，改用 `npm run test` 运行测试。该设置确保了与本地开发配置一致的测试环境。

完成前面的步骤后，你的项目目录应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

#### 第 4 步：运行测试

要在容器内执行你的测试套件，从项目根目录运行以下命令：

```console
$ docker compose run --rm react-test
```

该命令将：

- 启动你 `compose.yaml` 文件中定义的 `react-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 测试完成后自动移除容器（[`docker compose run --rm`](/reference/cli/docker/compose/run/) 命令）。

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> reference](/reference/cli/docker/compose/)。

---

### 小结

在本节中，你学习了如何使用 Vitest 和 Docker Compose 在 Docker 容器内为 React.js 应用运行单元测试。

你完成的工作：

- 安装并配置了 Vitest 和 React Testing Library 来测试 React 组件。
- 在 `compose.yaml` 中创建了 `react-test` 服务以隔离测试执行。
- 复用了开发用的 `Dockerfile.dev`，确保开发环境与测试环境一致。
- 使用 `docker compose run --rm react-test` 在容器内运行测试。
- 不依赖本地机器配置，即可在各环境间实现可靠、可重复的测试。

---

### 相关资源

探索官方参考和最佳实践，提升你的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) —— 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) —— 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) —— 学习在 `compose.yaml` 中配置服务可用的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) —— 在服务容器中运行一次性命令。

