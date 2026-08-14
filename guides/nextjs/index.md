# 容器化一个 Next.js 应用


本指南介绍如何使用 Docker 容器化 Next.js 应用，遵循创建高效、可投入生产的容器的最佳实践。

[Next.js](https://nextjs.org/) 是一个 React 框架，支持服务器端渲染、静态站点生成以及全栈能力。Docker 提供了从开发到生产的一致的容器化环境。

> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 致以诚挚的谢意，感谢他撰写本指南，并将官方的 [Next.js Docker 示例](https://github.com/vercel/next.js/tree/canary/examples/with-docker) 贡献到 Vercel 的 Next.js 仓库，包括 standalone 与 export 输出示例。作为 Docker Captain 和资深工程师，他在 Docker、DevOps 以及现代 Web 开发方面的专长使本资源对社区极具价值，帮助开发者驾驭并优化他们的 Docker 工作流。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 Next.js 应用。
- 在容器内搭建 Next.js 的本地开发环境。
- 在 Docker 容器内运行 Next.js 应用的测试。

首先，您将从容器化一个已有的 Next.js 应用开始。

---

## 前提条件

在开始之前，请确保您熟悉以下内容：

- 对 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 或 [TypeScript](https://www.typescriptlang.org/) 有基本了解。
- 对 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 有基本了解，以便管理依赖和运行脚本。
- 熟悉 [React](https://react.dev/) 和 [Next.js](https://nextjs.org/) 的基础知识。
- 了解镜像、容器、Dockerfile 等 Docker 概念。如果您是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Next.js 入门模块后，您就可以使用本指南提供的示例和说明来容器化您自己的 Next.js 应用。

## 容器化一个 Next.js 应用

### 前提条件

在开始之前，请确保您的系统上已安装并可用以下工具：

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> [!NOTE]
> Docker 新手？请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

### 概述

本指南将引导您使用 Docker 容器化一个 Next.js 应用。您将学习如何创建生产就绪的 Docker 镜像，并运用能够提升性能、安全性、可扩展性和部署效率的最佳实践。

到本指南结束时，您将能够：

- 使用 Docker 容器化 Next.js 应用。
- 为生产构建创建并优化 Dockerfile。
- 使用多阶段构建来最小化镜像体积。
- 利用 Next.js 的 standalone 或 export 输出来实现高效容器化。
- 遵循构建安全、可维护 Docker 镜像的最佳实践。

---

### 获取示例应用

克隆与本指南配合使用的示例应用。打开终端，切换到您想工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-nextjs-sample
```

---

### 构建 Docker 镜像

Next.js 对生产部署有特定要求。本指南展示两种方法：`standalone` 输出（Node.js 服务器）和 `export` 输出（使用 Nginx 的静态文件）。

> [!TIP]
>
> [Gordon](/ai/gordon/)（Docker 的 AI 助手）可以为您的项目生成 Docker 资产。请 Gordon 为您创建适配您应用的 Dockerfile、Compose 文件和 `.dockerignore`。

#### 第 1 步：配置 Next.js 并创建 Dockerfile

在创建 Dockerfile 之前，请选择一个基础镜像：[Node.js 官方镜像](https://hub.docker.com/_/node) 或来自加固镜像（Hardened Image）目录的 [Docker Hardened Image (DHI)](https://hub.docker.com/hardened-images/catalog)。选择 DHI 可为您提供生产就绪、轻量且安全的镜像。更多信息请参见 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用稳定的 Node.js LTS 镜像标签，在撰写时被认为是安全的。由于新版本和安全补丁会定期发布，在构建或部署之前，请务必查阅 [官方 Node.js Docker 镜像](https://hub.docker.com/_/node) 并选择安全、最新的版本。

---

##### 1.1 使用 standalone 输出的 Next.js

standalone 输出（`output: "standalone"`）会让 Next.js 构建一个自包含的输出，其中仅包含运行应用所需的文件和依赖。单个 `node server.js` 即可为应用提供服务，非常适合 Docker，并支持服务器端渲染、API 路由以及增量静态再生。详情请参阅 [Next.js 输出配置文档](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)（包含 "standalone" 选项）。

容器会在端口 3000 上使用 Node.js 运行 Next.js 服务器。

配置 Next.js —— 在项目根目录打开或创建 `next.config.ts`：

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
};

export default nextConfig;
```

选择 Docker Hardened Image 或 Docker 官方镜像，然后使用所选标签页下方的内容创建 `Dockerfile`。

**使用 Docker Hardened Images**



Docker Hardened Images（DHI）已在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/node) 中提供 Node.js 版本。更多信息请参见 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（请查阅目录中可用的版本）：

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. 创建一个名为 `Dockerfile` 的文件，内容如下。`FROM` 指令使用 `dhi.io/node:24-alpine3.22-dev`。请查阅 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog) 获取最新版本，并根据安全与兼容性需要更新镜像标签。

   ```dockerfile
   # ============================================
   # 阶段 1：依赖安装阶段
   # ============================================

   # 重要：Docker Hardened Image (DHI) 版本维护
   # 本 Dockerfile 使用 dhi.io/node。请定期校验并更新到目录中最新的 DHI 版本，以确保安全与兼容。

   FROM dhi.io/node:24-alpine3.22-dev AS dependencies

   # 设置工作目录
   WORKDIR /app

   # 先复制与包相关的文件，以利用 Docker 的缓存机制
   COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

   # 使用 frozen lockfile 安装项目依赖，以保证构建可复现
   RUN --mount=type=cache,target=/root/.npm \
       --mount=type=cache,target=/usr/local/share/.cache/yarn \
       --mount=type=cache,target=/root/.local/share/pnpm/store \
     if [ -f package-lock.json ]; then \
       npm ci --no-audit --no-fund; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn install --frozen-lockfile --production=false; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm install --frozen-lockfile; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # 阶段 2：以 standalone 模式构建 Next.js 应用
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS builder

   # 设置工作目录
   WORKDIR /app

   # 从 dependencies 阶段复制项目依赖
   COPY --from=dependencies /app/node_modules ./node_modules

   # 复制应用源代码
   COPY . .

   ENV NODE_ENV=production

   # Next.js 会收集完全匿名的通用使用遥测数据。
   # 详情见：https://nextjs.org/telemetry
   # 若想在构建期间禁用遥测，请取消下面一行的注释。
   # ENV NEXT_TELEMETRY_DISABLED=1

   # 构建 Next.js 应用
   # 如果想加速 Docker 重建，可添加：--mount=type=cache,target=/app/.next/cache
   # 来缓存构建产物，但这会阻止 .next/cache/fetch-cache 被包含到最终镜像中，
   # 意味着构建期生成的缓存 fetch 响应在运行期将不可用。
   RUN if [ -f package-lock.json ]; then \
       npm run build; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn build; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm build; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # 阶段 3：运行 Next.js 应用
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS runner

   # 设置工作目录
   WORKDIR /app

   # 设置生产环境变量
   ENV NODE_ENV=production
   ENV PORT=3000
   ENV HOSTNAME="0.0.0.0"

   # Next.js 会收集完全匿名的通用使用遥测数据。
   # 详情见：https://nextjs.org/telemetry
   # 若想在运行期禁用遥测，请取消下面一行的注释。
   # ENV NEXT_TELEMETRY_DISABLED=1

   # 复制生产资源
   COPY --from=builder --chown=node:node /app/public ./public

   # 为预渲染缓存设置正确的权限
   RUN mkdir .next
   RUN chown node:node .next

   # 自动利用输出追踪以减小镜像体积
   # https://nextjs.org/docs/advanced-features/output-file-tracing
   COPY --from=builder --chown=node:node /app/.next/standalone ./
   COPY --from=builder --chown=node:node /app/.next/static ./.next/static

   # 若想保留构建期生成的 fetch 缓存，使缓存响应在启动时立即可用，请取消下面一行的注释：
   # COPY --from=builder --chown=node:node /app/.next/cache ./.next/cache

   # 切换到非 root 用户，遵循安全最佳实践
   USER node

   # 暴露端口 3000 以允许 HTTP 流量
   EXPOSE 3000

   # 启动 Next.js standalone 服务器
   CMD ["node", "server.js"]
   ```

**使用 Docker 官方镜像**



创建一个名为 `Dockerfile` 的文件，内容如下（使用 `node`）：

```dockerfile
  # ============================================
  # 阶段 1：依赖安装阶段
  # ============================================

  ARG NODE_VERSION=24.14.0-slim

  FROM node:${NODE_VERSION} AS dependencies

  # 设置工作目录
  WORKDIR /app

  # 先复制与包相关的文件，以利用 Docker 的缓存机制
  COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

  # 使用 frozen lockfile 安装项目依赖，以保证构建可复现
  RUN --mount=type=cache,target=/root/.npm \
      --mount=type=cache,target=/usr/local/share/.cache/yarn \
      --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f package-lock.json ]; then \
      npm ci --no-audit --no-fund; \
    elif [ -f yarn.lock ]; then \
      corepack enable yarn && yarn install --frozen-lockfile --production=false; \
    elif [ -f pnpm-lock.yaml ]; then \
      corepack enable pnpm && pnpm install --frozen-lockfile; \
    else \
      echo "No lockfile found." && exit 1; \
    fi

  # ============================================
  # 阶段 2：以 standalone 模式构建 Next.js 应用
  # ============================================

  FROM node:${NODE_VERSION} AS builder

  # 设置工作目录
  WORKDIR /app

  # 从 dependencies 阶段复制项目依赖
  COPY --from=dependencies /app/node_modules ./node_modules

  # 复制应用源代码
  COPY . .

  ENV NODE_ENV=production

  # Next.js 会收集完全匿名的通用使用遥测数据。
  # 详情见：https://nextjs.org/telemetry
  # 若想在构建期间禁用遥测，请取消下面一行的注释。
  # ENV NEXT_TELEMETRY_DISABLED=1

  # 构建 Next.js 应用
  # 如果想加速 Docker 重建，可添加：--mount=type=cache,target=/app/.next/cache
  # 来缓存构建产物，但这会阻止 .next/cache/fetch-cache 被包含到最终镜像中，
  # 意味着构建期生成的缓存 fetch 响应在运行期将不可用。
  RUN if [ -f package-lock.json ]; then \
      npm run build; \
    elif [ -f yarn.lock ]; then \
      corepack enable yarn && yarn build; \
    elif [ -f pnpm-lock.yaml ]; then \
      corepack enable pnpm && pnpm build; \
    else \
      echo "No lockfile found." && exit 1; \
    fi

  # ============================================
  # 阶段 3：运行 Next.js 应用
  # ============================================

  FROM node:${NODE_VERSION} AS runner

  # 设置工作目录
  WORKDIR /app

  # 设置生产环境变量
  ENV NODE_ENV=production
  ENV PORT=3000
  ENV HOSTNAME="0.0.0.0"

  # Next.js 会收集完全匿名的通用使用遥测数据。
  # 详情见：https://nextjs.org/telemetry
  # 若想在运行期禁用遥测，请取消下面一行的注释。
  # ENV NEXT_TELEMETRY_DISABLED=1

  # 复制生产资源
  COPY --from=builder --chown=node:node /app/public ./public

  # 为预渲染缓存设置正确的权限
  RUN mkdir .next
  RUN chown node:node .next

  # 自动利用输出追踪以减小镜像体积
  # https://nextjs.org/docs/advanced-features/output-file-tracing
  COPY --from=builder --chown=node:node /app/.next/standalone ./
  COPY --from=builder --chown=node:node /app/.next/static ./.next/static

  # 若想保留构建期生成的 fetch 缓存，使缓存响应在启动时立即可用，请取消下面一行的注释：
  # COPY --from=builder --chown=node:node /app/.next/cache ./.next/cache

  # 切换到非 root 用户，遵循安全最佳实践
  USER node

  # 暴露端口 3000 以允许 HTTP 流量
  EXPOSE 3000

  # 启动 Next.js standalone 服务器
  CMD ["node", "server.js"]
```

> [!NOTE]
> 本 Dockerfile 使用三个阶段：`dependencies`、`builder` 和 `runner`。最终镜像运行 `node server.js` 并监听端口 3000。



---

##### 1.2 使用 export 输出的 Next.js

输出导出（`output: "export"`）会让 Next.js 在构建时生成完全静态的站点。它将 HTML、CSS 和 JavaScript 生成到 `out` 目录，可由任何静态托管或 CDN 提供——运行期不需要 Node.js 服务器。当您不需要服务器端渲染或 API 路由时，请使用此方式。详情请参阅 [Next.js 输出配置文档](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)。

配置 Next.js —— 在项目根目录打开 `next.config.ts` 并添加以下代码：

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
```

选择 Docker Hardened Image 或 Docker 官方镜像，然后使用所选标签页下方的内容创建 `Dockerfile`。

**使用 Docker Hardened Images**



Docker Hardened Images（DHI）已在 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog) 中提供 Node.js 和 Nginx 版本。更多信息请参见 [DHI 快速入门](/dhi/get-started/) 指南。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Node.js DHI（请查阅目录中可用的版本）：

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. 拉取 Nginx DHI（请查阅目录中可用的版本）：

   ```console
   $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
   ```

4. 创建一个名为 `Dockerfile` 的文件，内容如下。`FROM` 指令使用 Docker Hardened Images：`dhi.io/node:24-alpine3.22-dev` 和 `dhi.io/nginx:1.28.0-alpine3.21-dev`。请查阅 [Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog) 获取最新版本，并根据安全与兼容性需要更新镜像标签。

   ```dockerfile
   # ============================================
   # 阶段 1：依赖安装阶段
   # ============================================

   # 重要：Docker Hardened Image (DHI) 版本维护
   # 本 Dockerfile 使用 dhi.io/node 和 dhi.io/nginx。请定期校验并更新到目录中最新的 DHI 版本，以确保安全与兼容。

   FROM dhi.io/node:24-alpine3.22-dev AS dependencies

   # 设置工作目录
   WORKDIR /app

   # 先复制与包相关的文件，以利用 Docker 的缓存机制
   COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

   # 使用 frozen lockfile 安装项目依赖，以保证构建可复现
   RUN --mount=type=cache,target=/root/.npm \
       --mount=type=cache,target=/usr/local/share/.cache/yarn \
       --mount=type=cache,target=/root/.local/share/pnpm/store \
     if [ -f package-lock.json ]; then \
       npm ci --no-audit --no-fund; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn install --frozen-lockfile --production=false; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm install --frozen-lockfile; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # 阶段 2：构建 Next.js 应用
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS builder

   # 设置工作目录
   WORKDIR /app

   # 从 dependencies 阶段复制项目依赖
   COPY --from=dependencies /app/node_modules ./node_modules

   # 复制应用源代码
   COPY . .

   ENV NODE_ENV=production

   # Next.js 会收集完全匿名的通用使用遥测数据。
   # 详情见：https://nextjs.org/telemetry
   # 若想在构建期间禁用遥测，请取消下面一行的注释。
   # ENV NEXT_TELEMETRY_DISABLED=1

   # 构建 Next.js 应用
   RUN --mount=type=cache,target=/app/.next/cache \
     if [ -f package-lock.json ]; then \
       npm run build; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn build; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm build; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # =========================================
   # 阶段 3：使用 Nginx 提供静态文件
   # =========================================

   FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

   # 设置工作目录
   WORKDIR /app

   # Next.js 会收集完全匿名的通用使用遥测数据。
   # 详情见：https://nextjs.org/telemetry
   # 若想在运行期禁用遥测，请取消下面一行的注释。
   # ENV NEXT_TELEMETRY_DISABLED=1

   # 复制自定义 Nginx 配置
   COPY nginx.conf /etc/nginx/nginx.conf

   # 将构建阶段的静态输出复制到 Nginx 默认的 HTML 服务目录
   COPY --chown=nginx:nginx --from=builder /app/out /usr/share/nginx/html

   # 为安全最佳实践使用非 root 用户
   USER nginx

   # 暴露端口 8080 以允许 HTTP 流量
   EXPOSE 8080

   # 使用自定义配置直接启动 Nginx
   ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
   CMD ["-g", "daemon off;"]
   ```

**使用 Docker 官方镜像**



创建一个名为 `Dockerfile` 的文件，内容如下（使用 `node` 和 `nginxinc/nginx-unprivileged`）：

```dockerfile
# ============================================
# 阶段 1：依赖安装阶段
# ============================================

ARG NODE_VERSION=24.14.0-slim
ARG NGINXINC_IMAGE_TAG=alpine3.22

FROM node:${NODE_VERSION} AS dependencies

# 设置工作目录
WORKDIR /app

# 先复制与包相关的文件，以利用 Docker 的缓存机制
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

# 使用 frozen lockfile 安装项目依赖，以保证构建可复现
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/usr/local/share/.cache/yarn \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
  if [ -f package-lock.json ]; then \
    npm ci --no-audit --no-fund; \
  elif [ -f yarn.lock ]; then \
    corepack enable yarn && yarn install --frozen-lockfile --production=false; \
  elif [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm install --frozen-lockfile; \
  else \
    echo "No lockfile found." && exit 1; \
  fi

# ============================================
# 阶段 2：构建 Next.js 应用
# ============================================

FROM node:${NODE_VERSION} AS builder

# 设置工作目录
WORKDIR /app

# 从 dependencies 阶段复制项目依赖
COPY --from=dependencies /app/node_modules ./node_modules

# 复制应用源代码
COPY . .

ENV NODE_ENV=production

# Next.js 会收集完全匿名的通用使用遥测数据。
# 详情见：https://nextjs.org/telemetry
# 若想在构建期间禁用遥测，请取消下面一行的注释。
# ENV NEXT_TELEMETRY_DISABLED=1

# 构建 Next.js 应用
RUN --mount=type=cache,target=/app/.next/cache \
  if [ -f package-lock.json ]; then \
    npm run build; \
  elif [ -f yarn.lock ]; then \
    corepack enable yarn && yarn build; \
  elif [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm build; \
  else \
    echo "No lockfile found." && exit 1; \
  fi

# =========================================
# 阶段 3：使用 Nginx 提供静态文件
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINXINC_IMAGE_TAG} AS runner

# 设置工作目录
WORKDIR /app

# Next.js 会收集完全匿名的通用使用遥测数据。
# 详情见：https://nextjs.org/telemetry
# 若想在运行期禁用遥测，请取消下面一行的注释。
# ENV NEXT_TELEMETRY_DISABLED=1

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 将构建阶段的静态输出复制到 Nginx 默认的 HTML 服务目录
COPY --from=builder /app/out /usr/share/nginx/html

# 为安全最佳实践使用非 root 用户
USER nginx

# 暴露端口 8080 以允许 HTTP 流量
EXPOSE 8080

# 使用自定义配置直接启动 Nginx
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> [!NOTE]
> 本指南使用 [nginx-unprivileged](https://hub.docker.com/r/nginxinc/nginx-unprivileged) 而非标准 Nginx 镜像，以非 root 用户运行，遵循安全最佳实践。



1. 创建 `nginx.conf`（仅 export 输出需要）—— 在项目根目录创建一个名为 `nginx.conf` 的文件：

   ```nginx
   # 静态 Next.js 应用的最小 Nginx 配置
   worker_processes 1;

   # 将 PID 存放在 /tmp（始终可写）
   pid /tmp/nginx.pid;

   events {
       worker_connections 1024;
   }

   http {
       include       /etc/nginx/mime.types;
       default_type  application/octet-stream;

       # 禁用日志以避免权限问题
       access_log off;
       error_log  /dev/stderr;

       # 优化静态文件服务
       sendfile        on;
       tcp_nopush      on;
       tcp_nodelay     on;
       keepalive_timeout  65;

       # Gzip 压缩
       gzip on;
       gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
       gzip_min_length 256;

       server {
           listen       8080;
           server_name  localhost;

           # 提供静态文件
           root /usr/share/nginx/html;
           index index.html;

           # 处理 Next.js 静态导出路由
           # 参见：https://nextjs.org/docs/app/guides/static-exports#deploying
           location / {
               try_files $uri $uri.html $uri/ =404;
           }

           # 当 `trailingSlash: false`（默认值）时需要此项。
           # 若 next.config 中设置了 `trailingSlash: true`，可省略此项。
           # 处理嵌套路由，如 /blog/post -> /blog/post.html
           location ~ ^/(.+)/$ {
               rewrite ^/(.+)/$ /$1.html break;
           }

           # 提供 Next.js 静态资源
           location ~ ^/_next/ {
               try_files $uri =404;
               expires 1y;
               add_header Cache-Control "public, immutable";
           }

           # 可选的 404 处理
           error_page 404 /404.html;
           location = /404.html {
               internal;
           }
       }
   }
   ```

   > [!NOTE]
   > export 使用端口 8080。更多详情，请参阅 [Next.js 输出配置](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) 和 [Nginx 文档](https://nginx.org/en/docs/)。

#### 第 2 步：创建 compose.yaml 文件

创建一个名为 `compose.yaml` 的文件，内容如下：

```yaml {collapse=true,title=compose.yaml}
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
```

> [!NOTE]
> 若使用 export 输出（Nginx），请将端口映射改为 `8080:8080`。

#### 第 3 步：创建 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>
> - 减小镜像体积
> - 加速构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被加入最终镜像。
>
> 了解更多，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

创建一个名为 `.dockerignore` 的文件，内容如下：

```dockerignore
# 依赖（在镜像内安装，切勿从主机复制）
node_modules/
.pnp/
.pnp.js
.pnpm-store/

# Next.js 构建输出（在镜像构建期间生成）
.next/
out/
dist/
build/
.vercel/

# 测试（生产镜像中不需要）
coverage/
.nyc_output/
__tests__/
__mocks__/
jest/
cypress/
playwright-report/
test-results/
.vitest/

# 环境文件（避免将密钥泄漏到构建上下文中）
.env
.env*
.env.local
.env.development.local
.env.test.local
.env.production.local

# 调试与日志文件
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*
*.log

# IDE 与编辑器文件
.vscode/
.idea/
.cursor/
.cursorrules
.copilot/
*.swp
*.swo
*~

# Git
.git/
.gitignore
.gitattributes

# Docker 文件（减小构建上下文；镜像内不需要）
Dockerfile*
.dockerignore
docker-compose*.yml
compose*.yaml

# 文档（镜像内不需要）
*.md
docs/

# CI/CD（镜像内不需要）
.github/
.gitlab-ci.yml
.travis.yml
.circleci/
Jenkinsfile

# TypeScript 与构建元数据
*.tsbuildinfo

# 缓存与临时目录
.cache/
.parcel-cache/
.eslintcache
.stylelintcache
.turbo/
.tmp/
.temp/

# 敏感或仅用于开发期的配置（可选；若构建需要这些文件可省略）
.pem
.editorconfig
.prettierrc*
.eslintrc*
.stylelintrc*
.babelrc*
*.iml

# 操作系统相关文件
.DS_Store
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini
```

#### 第 4 步：构建 Next.js 应用镜像

完成自定义配置后，您就可以构建 Docker 镜像了。请使用在第 1 步中创建的 Dockerfile（standalone 或 export）。

该配置包括：

- 用于优化镜像体积的多阶段构建
- standalone：Node.js 服务器运行在端口 3000；export：Nginx 在端口 8080 提供静态文件
- 用于增强安全性的非 root 用户
- 正确的文件权限与所有权

完成前面的步骤后，您的项目目录至少应包含以下文件（export 还需要 `nginx.conf`）：

```text
├── docker-nextjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── next.config.ts
```

现在 Dockerfile 已配置好，您可以为 Next.js 应用构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的指令将您的应用打包成镜像。它包含来自当前目录（称为[构建上下文](/build/concepts/context/#what-is-a-build-context)）的所有必要文件。

从项目根目录运行以下命令：

```console
$ docker build --tag nextjs-sample .
```

该命令的作用：

- 使用当前目录 (.) 中的 Dockerfile
- 将应用及其依赖打包进 Docker 镜像
- 将镜像标记为 nextjs-sample，以便日后引用

#### 第 5 步：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上可用的镜像。既然您已经在终端中工作，我们来使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
nextjs-sample             latest            8c5fc80f098e   14 seconds ago   130MB
```

该输出提供了关于镜像的关键细节：

- Repository（仓库）—— 分配给镜像的名称。
- Tag（标签）—— 用于标识不同构建的版本标签（如 latest）。
- Image ID（镜像 ID）—— 镜像的唯一标识符。
- Created（创建时间）—— 镜像构建的时间戳。
- Size（大小）—— 镜像使用的总磁盘空间。

如果构建成功，您应该会看到 `nextjs-sample` 镜像被列出。

---

### 运行容器化的应用

在上一步中，您为 Next.js 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像，并验证您的应用是否按预期工作。

在终端中运行以下命令。请使用与您的配置匹配的端口：standalone 使用端口 3000，export 使用端口 8080。

```console
$ docker run -p 3000:3000 nextjs-sample
```

对于 export 输出，请改用端口 8080：

```console
$ docker run -p 8080:8080 nextjs-sample
```

打开浏览器并查看应用：standalone 访问 [http://localhost:3000](http://localhost:3000)，export 访问 [http://localhost:8080](http://localhost:8080)。您应该会看到您的 Next.js Web 应用。

在终端中按 `ctrl+c` 停止应用。

#### 在后台运行应用

您可以通过添加 `-d` 选项和 `--name` 来给容器命名，使其在终端中脱离运行，以便日后停止：

```console
$ docker run -d -p 3000:3000 --name nextjs-app nextjs-sample
```

对于 export 输出，请使用端口 8080：

```console
$ docker run -d -p 8080:8080 --name nextjs-app nextjs-sample
```

打开浏览器并查看应用：standalone 访问 [http://localhost:3000](http://localhost:3000)，export 访问 [http://localhost:8080](http://localhost:8080)。您应该会看到您的 Web 应用。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找暴露端口 3000（standalone）或 8080（export）的容器。

示例输出：

```shell
CONTAINER ID   IMAGE           COMMAND                  CREATED             STATUS             PORTS                    NAMES
f49b74736a9d   nextjs-sample   "node server.js"         About a minute ago   Up About a minute   0.0.0.0:3000->3000/tcp nextjs-app
```

要停止应用，请运行：

```console
$ docker stop nextjs-app
```

> [!NOTE]
> 有关运行容器的更多信息，请参阅 [`docker run` CLI 参考](/reference/cli/docker/container/run/) 和 [`docker stop` CLI 参考](/reference/cli/docker/container/stop/)。

---

## 使用容器进行 Next.js 开发

### 前提条件

完成 [容器化 Next.js 应用](#containerize-a-nextjs-application)。

---

### 概述

在本节中，您将学习如何使用 Docker Compose 为容器化的 Next.js 应用搭建生产环境和开发环境。该配置允许您使用 standalone 服务器运行生产构建，并利用 Compose Watch 和 Next.js 内置的热重载在容器内高效开发。

您将学习如何：

- 为生产和开发配置独立的容器
- 在开发中使用 Compose Watch 启用自动文件同步
- 无需手动重建即可实时调试和预览更改

---

### 自动更新服务（开发模式）

使用 Compose Watch 自动将源文件的更改同步到您的容器化开发环境中。这会在无需手动重启或重建容器的情况下自动同步文件更改。

### 第 1 步：创建开发 Dockerfile

在项目根目录创建一个名为 `Dockerfile.dev` 的文件，内容如下（与[示例项目](https://github.com/kristiyan-velkov/docker-nextjs-sample)一致）：

```dockerfile
# ============================================
# Next.js 开发用 Dockerfile
# ============================================
ARG NODE_VERSION=24.14.0-slim

FROM node:${NODE_VERSION} AS dev

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/usr/local/share/.cache/yarn \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
  if [ -f package-lock.json ]; then \
    npm ci --no-audit --no-fund; \
  elif [ -f yarn.lock ]; then \
    corepack enable yarn && yarn install --frozen-lockfile --production=false; \
  elif [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm install --frozen-lockfile; \
  else \
    echo "No lockfile found." && exit 1; \
  fi

COPY . .

ENV WATCHPACK_POLLING=true
ENV HOSTNAME="0.0.0.0"

RUN chown -R node:node /app
USER node

EXPOSE 3000

CMD ["sh", "-c", "if [ -f package-lock.json ]; then npm run dev; elif [ -f yarn.lock ]; then yarn dev; elif [ -f pnpm-lock.yaml ]; then pnpm dev; else npm run dev; fi"]
```

该文件为您的 Next.js 应用设置了具备热模块替换（HMR）的开发环境，并支持 npm、yarn 和 pnpm。

#### 第 2 步：更新您的 `compose.yaml` 文件

打开您的 `compose.yaml` 文件并定义两个服务：一个用于生产（`nextjs-prod-standalone`），一个用于开发（`nextjs-dev`）。这与[示例项目](https://github.com/kristiyan-velkov/docker-nextjs-sample) 的结构一致。

以下是一个 Next.js 应用的示例配置：

```yaml
services:
  nextjs-prod-standalone:
    build:
      context: .
      dockerfile: Dockerfile
    image: nextjs-sample:prod
    container_name: nextjs-sample-prod
    ports:
      - "3000:3000"

  nextjs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-dev
    ports:
      - "3000:3000"
    environment:
      - WATCHPACK_POLLING=true
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          ignore:
            - node_modules/
            - .next/
        - action: rebuild
          path: package.json
```

- `nextjs-prod-standalone` 服务使用 standalone 输出构建并运行您的生产 Next.js 应用。
- `nextjs-dev` 服务运行您的 Next.js 开发服务器，并启用热模块替换。
- `watch` 触发与 Compose Watch 的文件同步。
- `WATCHPACK_POLLING=true` 确保 Docker 内部能够正确检测文件更改。
- 针对 `package.json` 的 `rebuild` 操作确保在文件更改时重新安装依赖。

> [!NOTE]
> 更多详情，请参阅官方指南：[使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

#### 第 3 步：为 Docker 开发配置 Next.js

Next.js 在 Docker 容器开箱即用地运行良好，但有一些配置可以改善开发体验。

您在容器化阶段创建的 `next.config.ts` 文件已经包含了用于生产的 `output: "standalone"` 选项。对于开发，Next.js 会自动使用其内置的、启用热重载的开发服务器。

> [!NOTE]
> Next.js 开发服务器会自动：
>
> - 启用热模块替换（HMR）以实现即时更新
> - 监视文件更改并自动重新编译
> - 在浏览器中提供详细的错误信息
>
> compose 文件中的 `WATCHPACK_POLLING=true` 环境变量确保文件监视在 Docker 容器内正常工作。

完成前面的步骤后，您的项目目录现在应包含以下文件：

```text
├── docker-nextjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── next.config.ts
```

#### 第 4 步：启动 Compose Watch

从项目根目录运行以下命令，以 watch 模式启动容器：

```console
$ docker compose watch nextjs-dev
```

#### 第 5 步：使用 Next.js 测试 Compose Watch

要验证 Compose Watch 是否正常工作：

1. 在文本编辑器中打开 `app/page.tsx` 文件（如果您的项目使用 `src` 目录，则为 `src/app/page.tsx`）。

2. 定位主内容区域并找到要修改的文本元素。

3. 做一个可见的更改，例如更新一个标题：

   ```tsx
   <h1>Hello from Docker Compose Watch!</h1>
   ```

4. 保存文件。

5. 在浏览器中打开 [http://localhost:3000](http://localhost:3000)。

您应该会看到更新后的文本立即出现，而无需手动重建容器。这确认了文件监视和自动同步按预期工作。

---

## 在容器中运行 Next.js 测试

### 前提条件

完成本指南的所有前面章节，从 [容器化 Next.js 应用](#containerize-a-nextjs-application) 开始。

### 概述

测试是开发过程的关键部分。在本节中，您将学习如何：

- 在 Docker 容器内使用 Vitest（或 Jest）运行单元测试。
- 在 Docker 容器内运行 lint（如 ESLint）。
- 使用 Docker Compose 在隔离、可复现的环境中运行测试和 lint。

[示例项目](https://github.com/kristiyan-velkov/docker-nextjs-sample) 使用 [Vitest](https://vitest.dev/) 配合 [Testing Library](https://testing-library.com/) 进行组件测试。您可以使用相同的设置，或稍后遵循 Jest 的替代配置。

---

### 在开发期间运行测试

[示例项目](https://github.com/kristiyan-velkov/docker-nextjs-sample) 已经内置了 lint（ESLint）和示例测试（Vitest，`app/page.test.tsx`）。如果您使用的是示例应用，可以跳到 **第 3 步：更新 compose.yaml** 并使用以下命令运行测试或 lint。如果您使用的是自己的项目，请按照安装和配置步骤添加包和脚本。

该示例包含一个位于以下路径的测试文件：

```text
app/page.test.tsx
```

该文件使用 Vitest 和 React Testing Library 来验证页面组件的行为。

#### 第 1 步：安装 Vitest 和 React Testing Library（自定义项目）

如果您使用的是自定义项目，并且尚未添加必要的测试工具，请运行以下命令安装它们：

```console
$ npm install --save-dev vitest @vitejs/plugin-react @testing-library/react @testing-library/dom jsdom
```

然后，更新您的 `package.json` 文件中的 scripts 部分，加入：

```json
"scripts": {
  "test": "vitest",
  "test:run": "vitest run"
}
```

对于 lint，添加一个 `lint` 脚本（以及可选的 `lint:fix`）。例如，使用 [ESLint](https://eslint.org/)：

```json
"scripts": {
  "test": "vitest",
  "test:run": "vitest run",
  "lint": "eslint .",
  "lint:fix": "eslint . --fix"
}
```

示例项目使用 `eslint` 和 `eslint-config-next` 用于 Next.js。在自定义项目中使用以下命令安装它们：

```console
$ npm install --save-dev eslint eslint-config-next @eslint/eslintrc
```

在项目根目录创建一个 ESLint 配置文件（如 `eslint.config.cjs`），包含 Next.js 规则和全局忽略：

```js
const { defineConfig, globalIgnores } = require("eslint/config");
const { FlatCompat } = require("@eslint/eslintrc");

const compat = new FlatCompat({ baseDirectory: __dirname });

module.exports = defineConfig([
  ...compat.extends(
    "eslint-config-next/core-web-vitals",
    "eslint-config-next/typescript",
  ),
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "node_modules/**",
    "eslint.config.cjs",
  ]),
]);
```

---

#### 第 2 步：配置 Vitest（自定义项目）

如果您使用的是自定义项目，请在项目根目录创建一个 `vitest.config.ts` 文件（与[示例项目](https://github.com/kristiyan-velkov/docker-nextjs-sample)一致）：

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    globals: true,
  },
});
```

在项目根目录创建一个 `vitest.setup.ts` 文件：

```ts
import "@testing-library/jest-dom/vitest";
```

> [!NOTE]
> Vitest 与 Next.js 配合良好，提供快速执行和 ESM 支持。更多详情，请参阅 [Next.js 测试文档](https://nextjs.org/docs/app/building-your-application/testing) 和 [Vitest 文档](https://vitest.dev/)。

#### 第 3 步：更新 compose.yaml

将 `nextjs-test` 和 `nextjs-lint` 服务添加到您的 `compose.yaml` 文件中。在示例项目中，这些服务使用 `tools` profile，因此它们不会随普通的 `docker compose up` 一起启动。两者都复用 `Dockerfile.dev` 并运行测试或 lint 命令：

```yaml
services:
  nextjs-prod-standalone:
    build:
      context: .
      dockerfile: Dockerfile
    image: nextjs-sample:prod
    container_name: nextjs-sample-prod
    ports:
      - "3000:3000"

  nextjs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-dev
    ports:
      - "3000:3000"
    environment:
      - WATCHPACK_POLLING=true
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          ignore:
            - node_modules/
            - .next/
        - action: rebuild
          path: package.json

  nextjs-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-test
    command:
      [
        "sh",
        "-c",
        "if [ -f package-lock.json ]; then npm run test:run 2>/dev/null || npm run test -- --run; elif [ -f yarn.lock ]; then yarn test:run 2>/dev/null || yarn test --run; elif [ -f pnpm-lock.yaml ]; then pnpm run test:run; else npm run test -- --run; fi",
      ]
    profiles:
      - tools

  nextjs-lint:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-lint
    command:
      [
        "sh",
        "-c",
        "if [ -f package-lock.json ]; then npm run lint; elif [ -f yarn.lock ]; then yarn lint; elif [ -f pnpm-lock.yaml ]; then pnpm lint; else npm run lint; fi",
      ]
    profiles:
      - tools
```

`nextjs-test` 和 `nextjs-lint` 服务复用与[开发](#use-containers-for-nextjs-development)相同的 `Dockerfile.dev`，并覆盖默认命令以运行测试或 lint。`profiles: [tools]` 意味着这些服务只有在您使用 `--profile tools` 选项时才会运行。

完成前面的步骤后，您的项目目录应包含：

```text
├── docker-nextjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── vitest.config.ts
│ ├── vitest.setup.ts
│ └── next.config.ts
```

#### 第 4 步：运行测试

要在容器内执行测试套件，请从项目根目录运行：

```console
$ docker compose --profile tools run --rm nextjs-test
```

该命令将：

- 启动 `nextjs-test` 服务（因为 `--profile tools`）。
- 在与开发相同的环境中运行您的测试脚本（`test:run` 或 `test -- --run`）。
- 测试完成后移除容器（[`docker compose run --rm`](/reference/cli/docker/compose/run/)）。

> [!NOTE]
> 有关 Compose 命令和 profile 的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/)。

#### 第 5 步：在容器中运行 lint

要在容器内运行您的 linter（如 ESLint），请使用 `nextjs-lint` 服务，并搭配相同的 `tools` profile：

```console
$ docker compose --profile tools run --rm nextjs-lint
```

该命令将：

- 启动 `nextjs-lint` 服务（因为 `--profile tools`）。
- 在与开发相同的环境中运行您的 lint 脚本（`npm run lint`、`yarn lint` 或 `pnpm lint`，取决于您的 lockfile）。
- lint 完成后移除容器。

请确保您的 `package.json` 包含 `lint` 脚本。示例项目已有 `"lint": "eslint ."` 和 `"lint:fix": "eslint . --fix"`；对于自定义项目，请添加相同的脚本，并在需要时安装 `eslint` 和 `eslint-config-next`。

---

### 总结

在本节中，您学习了如何使用 Vitest 和 Docker Compose 在 Docker 容器内运行 Next.js 应用的单元测试。

您完成的工作：

- 安装并配置了 Vitest 和 React Testing Library 用于测试 Next.js 组件。
- 在 `compose.yaml` 中创建了 `nextjs-test` 和 `nextjs-lint` 服务（使用 `tools` profile）以隔离测试和 lint 执行。
- 复用了开发用的 `Dockerfile.dev`，以确保开发、测试和 lint 环境之间的一致性。
- 使用 `docker compose --profile tools run --rm nextjs-test` 在容器内运行测试。
- 使用 `docker compose --profile tools run --rm nextjs-lint` 在容器内运行 lint。
- 确保跨环境的可靠、可重复的测试和 lint，而无需依赖本地机器配置。

---

### 相关资源

探索官方参考和最佳实践，以提升您的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) —— 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) —— 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) —— 了解在 `compose.yaml` 中配置服务可用的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) —— 在服务容器中运行一次性命令。
- [Next.js 测试文档](https://nextjs.org/docs/app/building-your-application/testing) —— 官方 Next.js 测试指南。
