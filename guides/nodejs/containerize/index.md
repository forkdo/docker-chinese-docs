# 容器化 Node.js 应用

## 前提条件

在开始之前，请确保您的系统上已安装并可用以下工具：

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

> **初次接触 Docker？**  
> 请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始，熟悉镜像、容器和 Dockerfile 等关键概念。

---

## 概述

本指南将引导您完成使用 Docker 容器化 Node.js 应用的完整过程。您将学习如何使用最佳实践创建生产就绪的 Docker 镜像，以提升性能、安全性、可扩展性和操作效率。

本指南结束时，您将能够：

- 使用 Docker 容器化 Node.js 应用。
- 创建并优化专为 Node.js 环境定制的 Dockerfile。
- 使用多阶段构建来分离依赖项并减小镜像体积。
- 配置容器使用非 root 用户，以实现安全、高效的运行时环境。
- 遵循最佳实践构建安全、轻量且易于维护的 Docker 镜像。

## 获取示例应用

克隆示例应用以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令克隆 git 仓库：

```console
$ git clone https://github.com/kristiyan-velkov/docker-nodejs-sample
```

## 生成 Dockerfile

Docker 提供了一个名为 `docker init` 的交互式 CLI 工具，可帮助您为容器化应用搭建必要的配置文件。这包括生成 `Dockerfile`、`.dockerignore`、`compose.yaml` 和 `README.Docker.md`。

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

CLI 会提示您回答一些关于应用设置的问题。
为保持一致性，请在提示时使用与下表相同的回答：
| 问题 | 回答 |
|------------------------------------------------------------|-----------------|
| What application platform does your project use? | Node |
| What version of Node do you want to use? | 24.11.1-alpine |
| Which package manager do you want to use? | npm |
| Do you want to run "npm run build" before starting server? | yes |
| What directory is your build output to? | dist |
| What command do you want to use to start the app? | npm run dev |
| What port does your server listen on? | 3000 |

完成后，您的项目目录将包含以下新文件：

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── README.Docker.md
```

## 创建 Docker Compose 文件

虽然 `docker init` 生成了一个基本的 `compose.yaml` 文件，但您需要为此全栈应用创建一个更全面的配置。请用生产就绪的配置替换生成的 `compose.yaml`。

在项目根目录中创建一个名为 `compose.yml` 的新文件：

```yaml
# ========================================
# Docker Compose 配置
# 现代 Node.js Todo 应用
# ========================================

services:
  # ========================================
  # 开发服务
  # ========================================
  app-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: todoapp-dev
    ports:
      - '${APP_PORT:-3000}:3000' # API 服务器
      - '${VITE_PORT:-5173}:5173' # Vite 开发服务器
      - '${DEBUG_PORT:-9229}:9229' # Node.js 调试器
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
  # 生产服务
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
  # PostgreSQL 数据库服务
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
# 卷配置
# ========================================
volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

# ========================================
# 网络配置
# ========================================
networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

此 Docker Compose 配置包括：

- **开发服务** (`app-dev`): 包含热重载、调试支持和绑定挂载的完整开发环境
- **生产服务** (`app-prod`): 优化的生产部署，包含资源限制和安全加固
- **数据库服务** (`db`): PostgreSQL 18，带有持久化存储和健康检查
- **网络**: 用于安全服务通信的隔离网络
- **卷**: 用于数据库数据的持久化存储

## 创建环境配置

创建一个 `.env` 文件来配置您的应用设置：

```console
$ cp .env.example .env
```

使用您首选的设置更新 `.env` 文件：

```env
# 应用配置
NODE_ENV=development
APP_PORT=3000
VITE_PORT=5173
DEBUG_PORT=9229

# 生产配置
PROD_PORT=8080
PROD_MEMORY_LIMIT=2G
PROD_CPU_LIMIT=1.0
PROD_MEMORY_RESERVATION=512M
PROD_CPU_RESERVATION=0.25

# 数据库配置
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=todoapp
POSTGRES_USER=todoapp
POSTGRES_PASSWORD=todoapp_password
DB_PORT=5432

# 安全配置
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 构建 Docker 镜像

`docker init` 生成的默认 Dockerfile 为标准 Node.js 应用提供了可靠的基础。然而，由于此项目是一个包含后端 API 和前端 React 组件的全栈 TypeScript 应用，因此应自定义 Dockerfile 以更好地支持和优化此特定架构。

### 查看生成的文件

在接下来的步骤中，您将通过遵循最佳实践来改进 Dockerfile 和配置文件：

- 使用多阶段构建以保持最终镜像干净且体积小
- 仅包含所需内容以提高性能和安全性

这些更新使您的应用更易于部署且加载速度更快。

> [!NOTE]
> `Dockerfile` 是一个纯文本文件，包含构建 Docker 镜像的分步说明。它会自动打包您的应用程序及其依赖项和运行时环境。
> 有关完整详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

### 步骤 1：配置 Dockerfile

在创建 Dockerfile 之前，您需要选择一个基础镜像。您可以使用 [Node.js 官方镜像](https://hub.docker.com/_/node) 或来自 [Hardened Image 目录](https://hub.docker.com/hardened-images/catalog) 的 Docker Hardened Image (DHI)。

选择 DHI 的优势在于它提供了生产就绪、轻量且安全的镜像。有关更多信息，请参阅 [Docker Hardened Images](https://docs.docker.com/dhi/)。

> [!IMPORTANT]
> 本指南使用了一个稳定的 Node.js LTS 镜像标签，该标签在编写本指南时被认为是安全的。由于会定期发布新版本和安全补丁，当您遵循本指南时，此处显示的标签可能不再是安全选项。在构建或部署应用程序之前，请务必查看最新的可用镜像标签，并选择安全、最新的版本。
>
> 官方 Node.js Docker 镜像：https://hub.docker.com/_/node








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images'"
        
      >
        使用 Docker Hardened Images
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-Docker-%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-Docker-%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F'"
        
      >
        使用 Docker 官方镜像
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-Hardened-Images' && 'hidden'"
      >
        <p>Docker Hardened Images (DHIs) 可在 <a class="link" href="https://hub.docker.com/hardened-images/catalog/dhi/node" rel="noopener">Docker Hub</a> 上用于 Node.js。与使用 Docker 官方镜像不同，您必须首先将 Node.js 镜像镜像到您的组织中，然后将其用作基础镜像。请按照 
  <a class="link" href="/dhi/get-started/">DHI 快速入门</a> 中的说明为 Node.js 创建镜像仓库。</p>
<p>镜像仓库必须以 <code>dhi-</code> 开头，例如：<code>FROM &lt;your-namespace&gt;/dhi-node:&lt;tag&gt;</code>。在下面的 Dockerfile 中，<code>FROM</code> 指令使用 <code>&lt;your-namespace&gt;/dhi-node:24-alpine3.22-dev</code> 作为基础镜像。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5LyY5YyW55qE5aSa6Zi25q61IERvY2tlcmZpbGUKIyBOb2RlLmpzIFR5cGVTY3JpcHQg5bqU55SoICjkvb/nlKggREhJKQojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KCkZST00gPHlvdXItbmFtZXNwYWNlPi9kaGktbm9kZToyNC1hbHBpbmUzLjIyLWRldiBBUyBiYXNlCgojIOiuvue9ruW3peS9nOebruW9lQpXT1JLRElSIC9hcHAKCiMg5Yib5bu66Z2eIHJvb3Qg55So5oi35Lul5o&#43;Q6auY5a6J5YWo5oCnClJVTiBhZGRncm91cCAtZyAxMDAxIC1TIG5vZGVqcyAmJiBcCiAgICBhZGR1c2VyIC1TIG5vZGVqcyAtdSAxMDAxIC1HIG5vZGVqcyAmJiBcCiAgICBjaG93biAtUiBub2RlanM6bm9kZWpzIC9hcHAKCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQojIOS&#43;nei1lumYtuautQojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KRlJPTSBiYXNlIEFTIGRlcHMKCiMg5aSN5Yi25YyF5paH5Lu2CkNPUFkgcGFja2FnZSouanNvbiAuLwoKIyDlronoo4XnlJ/kuqfkvp3otZbpobkKUlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Jvb3QvLm5wbSxzaGFyaW5nPWxvY2tlZCBcCiAgICBucG0gY2kgLS1vbWl0PWRldiAmJiBcCiAgICBucG0gY2FjaGUgY2xlYW4gLS1mb3JjZQoKIyDorr7nva7mraPnoa7nmoTmiYDmnInmnYMKUlVOIGNob3duIC1SIG5vZGVqczpub2RlanMgL2FwcAoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5p6E5bu65L6d6LWW6Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIGJhc2UgQVMgYnVpbGQtZGVwcwoKIyDlpI3liLbljIXmlofku7YKQ09QWSBwYWNrYWdlKi5qc29uIC4vCgojIOWuieijheaJgOacieS&#43;nei1lumhueW5tui/m&#43;ihjOaehOW7uuS8mOWMlgpSVU4gLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8ubnBtLHNoYXJpbmc9bG9ja2VkIFwKICAgIG5wbSBjaSAtLW5vLWF1ZGl0IC0tbm8tZnVuZCAmJiBcCiAgICBucG0gY2FjaGUgY2xlYW4gLS1mb3JjZQoKIyDliJvlu7rlv4XopoHnmoTnm67lvZXlubborr7nva7mnYPpmZAKUlVOIG1rZGlyIC1wIC9hcHAvbm9kZV9tb2R1bGVzLy52aXRlICYmIFwKICAgIGNob3duIC1SIG5vZGVqczpub2RlanMgL2FwcAoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5p6E5bu66Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIGJ1aWxkLWRlcHMgQVMgYnVpbGQKCiMg5LuF5aSN5Yi25p6E5bu65omA6ZyA55qE5paH5Lu277yI6YG15b6qIC5kb2NrZXJpZ25vcmXvvIkKQ09QWSAtLWNob3duPW5vZGVqczpub2RlanMgLiAuCgojIOaehOW7uuW6lOeUqOeoi&#43;W6jwpSVU4gbnBtIHJ1biBidWlsZAoKIyDorr7nva7mraPnoa7nmoTmiYDmnInmnYMKUlVOIGNob3duIC1SIG5vZGVqczpub2RlanMgL2FwcAoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5byA5Y&#43;R6Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIGJ1aWxkLWRlcHMgQVMgZGV2ZWxvcG1lbnQKCiMg6K6&#43;572u546v5aKDCkVOViBOT0RFX0VOVj1kZXZlbG9wbWVudCBcCiAgICBOUE1fQ09ORklHX0xPR0xFVkVMPXdhcm4KCiMg5aSN5Yi25rqQ5paH5Lu2CkNPUFkgLiAuCgojIOehruS/neaJgOacieebruW9leWFt&#43;acieato&#43;ehrueahOadg&#43;mZkApSVU4gbWtkaXIgLXAgL2FwcC9ub2RlX21vZHVsZXMvLnZpdGUgJiYgXAogICAgY2hvd24gLVIgbm9kZWpzOm5vZGVqcyAvYXBwICYmIFwKICAgIGNobW9kIC1SIDc1NSAvYXBwCgojIOWIh&#43;aNouWIsOmdniByb290IOeUqOaItwpVU0VSIG5vZGVqcwoKIyDmmrTpnLLnq6/lj6MKRVhQT1NFIDMwMDAgNTE3MyA5MjI5CgojIOWQr&#43;WKqOW8gOWPkeacjeWKoeWZqApDTUQgWyJucG0iLCAicnVuIiwgImRldjpkb2NrZXIiXQoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg55Sf5Lqn6Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIDx5b3VyLW5hbWVzcGFjZT4vZGhpLW5vZGU6MjQtYWxwaW5lMy4yMi1kZXYgQVMgcHJvZHVjdGlvbgoKIyDorr7nva7lt6XkvZznm67lvZUKV09SS0RJUiAvYXBwCgojIOWIm&#43;W7uumdniByb290IOeUqOaIt&#43;S7peaPkOmrmOWuieWFqOaApwpSVU4gYWRkZ3JvdXAgLWcgMTAwMSAtUyBub2RlanMgJiYgXAogICAgYWRkdXNlciAtUyBub2RlanMgLXUgMTAwMSAtRyBub2RlanMgJiYgXAogICAgY2hvd24gLVIgbm9kZWpzOm5vZGVqcyAvYXBwCgojIOiuvue9ruS8mOWMlueahOeOr&#43;Wig&#43;WPmOmHjwpFTlYgTk9ERV9FTlY9cHJvZHVjdGlvbiBcCiAgICBOT0RFX09QVElPTlM9Ii0tbWF4LW9sZC1zcGFjZS1zaXplPTI1NiAtLW5vLXdhcm5pbmdzIiBcCiAgICBOUE1fQ09ORklHX0xPR0xFVkVMPXNpbGVudAoKIyDku44gZGVwcyDpmLbmrrXlpI3liLbnlJ/kuqfkvp3otZbpobkKQ09QWSAtLWZyb209ZGVwcyAtLWNob3duPW5vZGVqczpub2RlanMgL2FwcC9ub2RlX21vZHVsZXMgLi9ub2RlX21vZHVsZXMKQ09QWSAtLWZyb209ZGVwcyAtLWNob3duPW5vZGVqczpub2RlanMgL2FwcC9wYWNrYWdlKi5qc29uIC4vCiMg5LuOIGJ1aWxkIOmYtuauteWkjeWItuaehOW7uuWlveeahOW6lOeUqOeoi&#43;W6jwpDT1BZIC0tZnJvbT1idWlsZCAtLWNob3duPW5vZGVqczpub2RlanMgL2FwcC9kaXN0IC4vZGlzdAoKIyDliIfmjaLliLDpnZ4gcm9vdCDnlKjmiLfku6Xmj5Dpq5jlronlhajmgKcKVVNFUiBub2RlanMKCiMg5pq06Zyy56uv5Y&#43;jCkVYUE9TRSAzMDAwCgojIOWQr&#43;WKqOeUn&#43;S6p&#43;acjeWKoeWZqApDTUQgWyJub2RlIiwgImRpc3Qvc2VydmVyLmpzIl0KCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQojIOa1i&#43;ivlemYtuautQojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KRlJPTSBidWlsZC1kZXBzIEFTIHRlc3QKCiMg6K6&#43;572u546v5aKDCkVOViBOT0RFX0VOVj10ZXN0IFwKICAgIENJPXRydWUKCiMg5aSN5Yi25rqQ5paH5Lu2CkNPUFkgLS1jaG93bj1ub2RlanM6bm9kZWpzIC4gLgoKIyDliIfmjaLliLDpnZ4gcm9vdCDnlKjmiLcKVVNFUiBub2RlanMKCiMg6L&#43;Q6KGM5bim6KaG55uW546H55qE5rWL6K&#43;VCkNNRCBbIm5wbSIsICJydW4iLCAidGVzdDpjb3ZlcmFnZSJd', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 优化的多阶段 Dockerfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># Node.js TypeScript 应用 (使用 DHI)</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> &lt;your-namespace&gt;/dhi-node:24-alpine3.22-dev AS base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> addgroup -g <span class="m">1001</span> -S nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    adduser -S nodejs -u <span class="m">1001</span> -G nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 依赖阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制包文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装生产依赖项</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.npm,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm ci --omit<span class="o">=</span>dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm cache clean --force<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置正确的所有权</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建依赖阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS build-deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制包文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装所有依赖项并进行构建优化</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.npm,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm ci --no-audit --no-fund <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm cache clean --force<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建必要的目录并设置权限</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> mkdir -p /app/node_modules/.vite <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 仅复制构建所需的文件（遵循 .dockerignore）</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --chown<span class="o">=</span>nodejs:nodejs . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> npm run build<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置正确的所有权</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 开发阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS development</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span>development <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NPM_CONFIG_LOGLEVEL</span><span class="o">=</span>warn
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 复制源文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 确保所有目录具有正确的权限</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> mkdir -p /app/node_modules/.vite <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chmod -R <span class="m">755</span> /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 3000 5173 9229</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 启动开发服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;npm&#34;</span><span class="p">,</span> <span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;dev:docker&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 生产阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> &lt;your-namespace&gt;/dhi-node:24-alpine3.22-dev AS production</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> addgroup -g <span class="m">1001</span> -S nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    adduser -S nodejs -u <span class="m">1001</span> -G nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置优化的环境变量</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span>production <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NODE_OPTIONS</span><span class="o">=</span><span class="s2">&#34;--max-old-space-size=256 --no-warnings&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NPM_CONFIG_LOGLEVEL</span><span class="o">=</span>silent<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 从 deps 阶段复制生产依赖项</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>deps --chown<span class="o">=</span>nodejs:nodejs /app/node_modules ./node_modules<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>deps --chown<span class="o">=</span>nodejs:nodejs /app/package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 从 build 阶段复制构建好的应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build --chown<span class="o">=</span>nodejs:nodejs /app/dist ./dist<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 3000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 启动生产服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;node&#34;</span><span class="p">,</span> <span class="s2">&#34;dist/server.js&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 测试阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS test</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span><span class="nb">test</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">CI</span><span class="o">=</span><span class="nb">true</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 复制源文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --chown<span class="o">=</span>nodejs:nodejs . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 运行带覆盖率的测试</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;npm&#34;</span><span class="p">,</span> <span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;test:coverage&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-Docker-%E5%AE%98%E6%96%B9%E9%95%9C%E5%83%8F' && 'hidden'"
      >
        <p>现在您需要创建一个生产就绪的多阶段 Dockerfile。用以下优化配置替换生成的 Dockerfile：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5LyY5YyW55qE5aSa6Zi25q61IERvY2tlcmZpbGUKIyBOb2RlLmpzIFR5cGVTY3JpcHQg5bqU55SoCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQoKQVJHIE5PREVfVkVSU0lPTj0yNC4xMS4xLWFscGluZQpGUk9NIG5vZGU6JHtOT0RFX1ZFUlNJT059IEFTIGJhc2UKCiMg6K6&#43;572u5bel5L2c55uu5b2VCldPUktESVIgL2FwcAoKIyDliJvlu7rpnZ4gcm9vdCDnlKjmiLfku6Xmj5Dpq5jlronlhajmgKcKUlVOIGFkZGdyb3VwIC1nIDEwMDEgLVMgbm9kZWpzICYmIFwKICAgIGFkZHVzZXIgLVMgbm9kZWpzIC11IDEwMDEgLUcgbm9kZWpzICYmIFwKICAgIGNob3duIC1SIG5vZGVqczpub2RlanMgL2FwcAoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5L6d6LWW6Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIGJhc2UgQVMgZGVwcwoKIyDlpI3liLbljIXmlofku7YKQ09QWSBwYWNrYWdlKi5qc29uIC4vCgojIOWuieijheeUn&#43;S6p&#43;S&#43;nei1lumhuQpSVU4gLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vcm9vdC8ubnBtLHNoYXJpbmc9bG9ja2VkIFwKICAgIG5wbSBjaSAtLW9taXQ9ZGV2ICYmIFwKICAgIG5wbSBjYWNoZSBjbGVhbiAtLWZvcmNlCgojIOiuvue9ruato&#43;ehrueahOaJgOacieadgwpSVU4gY2hvd24gLVIgbm9kZWpzOm5vZGVqcyAvYXBwCgojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KIyDmnoTlu7rkvp3otZbpmLbmrrUKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CkZST00gYmFzZSBBUyBidWlsZC1kZXBzCgojIOWkjeWItuWMheaWh&#43;S7tgpDT1BZIHBhY2thZ2UqLmpzb24gLi8KCiMg5a6J6KOF5omA5pyJ5L6d6LWW6aG55bm26L&#43;b6KGM5p6E5bu65LyY5YyWClJVTiAtLW1vdW50PXR5cGU9Y2FjaGUsdGFyZ2V0PS9yb290Ly5ucG0sc2hhcmluZz1sb2NrZWQgXAogICAgbnBtIGNpIC0tbm8tYXVkaXQgLS1uby1mdW5kICYmIFwKICAgIG5wbSBjYWNoZSBjbGVhbiAtLWZvcmNlCgojIOWIm&#43;W7uuW/heimgeeahOebruW9leW5tuiuvue9ruadg&#43;mZkApSVU4gbWtkaXIgLXAgL2FwcC9ub2RlX21vZHVsZXMvLnZpdGUgJiYgXAogICAgY2hvd24gLVIgbm9kZWpzOm5vZGVqcyAvYXBwCgojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KIyDmnoTlu7rpmLbmrrUKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CkZST00gYnVpbGQtZGVwcyBBUyBidWlsZAoKIyDku4XlpI3liLbmnoTlu7rmiYDpnIDnmoTmlofku7bvvIjpgbXlvqogLmRvY2tlcmlnbm9yZe&#43;8iQpDT1BZIC0tY2hvd249bm9kZWpzOm5vZGVqcyAuIC4KCiMg5p6E5bu65bqU55So56iL5bqPClJVTiBucG0gcnVuIGJ1aWxkCgojIOiuvue9ruato&#43;ehrueahOaJgOacieadgwpSVU4gY2hvd24gLVIgbm9kZWpzOm5vZGVqcyAvYXBwCgojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KIyDlvIDlj5HpmLbmrrUKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CkZST00gYnVpbGQtZGVwcyBBUyBkZXZlbG9wbWVudAoKIyDorr7nva7njq/looMKRU5WIE5PREVfRU5WPWRldmVsb3BtZW50IFwKICAgIE5QTV9DT05GSUdfTE9HTEVWRUw9d2FybgoKIyDlpI3liLbmupDmlofku7YKQ09QWSAuIC4KCiMg56Gu5L&#43;d5omA5pyJ55uu5b2V5YW35pyJ5q2j56Gu55qE5p2D6ZmQClJVTiBta2RpciAtcCAvYXBwL25vZGVfbW9kdWxlcy8udml0ZSAmJiBcCiAgICBjaG93biAtUiBub2RlanM6bm9kZWpzIC9hcHAgJiYgXAogICAgY2htb2QgLVIgNzU1IC9hcHAKCiMg5YiH5o2i5Yiw6Z2eIHJvb3Qg55So5oi3ClVTRVIgbm9kZWpzCgojIOaatOmcsuerr&#43;WPowpFWFBPU0UgMzAwMCA1MTczIDkyMjkKCiMg5ZCv5Yqo5byA5Y&#43;R5pyN5Yqh5ZmoCkNNRCBbIm5wbSIsICJydW4iLCAiZGV2OmRvY2tlciJdCgojID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KIyDnlJ/kuqfpmLbmrrUKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CkFSRyBOT0RFX1ZFUlNJT049MjQuMTEuMS1hbHBpbmUKRlJPTSBub2RlOiR7Tk9ERV9WRVJTSU9OfSBBUyBwcm9kdWN0aW9uCgojIOiuvue9ruW3peS9nOebruW9lQpXT1JLRElSIC9hcHAKCiMg5Yib5bu66Z2eIHJvb3Qg55So5oi35Lul5o&#43;Q6auY5a6J5YWo5oCnClJVTiBhZGRncm91cCAtZyAxMDAxIC1TIG5vZGVqcyAmJiBcCiAgICBhZGR1c2VyIC1TIG5vZGVqcyAtdSAxMDAxIC1HIG5vZGVqcyAmJiBcCiAgICBjaG93biAtUiBub2RlanM6bm9kZWpzIC9hcHAKCiMg6K6&#43;572u5LyY5YyW55qE546v5aKD5Y&#43;Y6YePCkVOViBOT0RFX0VOVj1wcm9kdWN0aW9uIFwKICAgIE5PREVfT1BUSU9OUz0iLS1tYXgtb2xkLXNwYWNlLXNpemU9MjU2IC0tbm8td2FybmluZ3MiIFwKICAgIE5QTV9DT05GSUdfTE9HTEVWRUw9c2lsZW50CgojIOS7jiBkZXBzIOmYtuauteWkjeWItueUn&#43;S6p&#43;S&#43;nei1lumhuQpDT1BZIC0tZnJvbT1kZXBzIC0tY2hvd249bm9kZWpzOm5vZGVqcyAvYXBwL25vZGVfbW9kdWxlcyAuL25vZGVfbW9kdWxlcwpDT1BZIC0tZnJvbT1kZXBzIC0tY2hvd249bm9kZWpzOm5vZGVqcyAvYXBwL3BhY2thZ2UqLmpzb24gLi8KIyDku44gYnVpbGQg6Zi25q615aSN5Yi25p6E5bu65aW955qE5bqU55So56iL5bqPCkNPUFkgLS1mcm9tPWJ1aWxkIC0tY2hvd249bm9kZWpzOm5vZGVqcyAvYXBwL2Rpc3QgLi9kaXN0CgojIOWIh&#43;aNouWIsOmdniByb290IOeUqOaIt&#43;S7peaPkOmrmOWuieWFqOaApwpVU0VSIG5vZGVqcwoKIyDmmrTpnLLnq6/lj6MKRVhQT1NFIDMwMDAKCiMg5ZCv5Yqo55Sf5Lqn5pyN5Yqh5ZmoCkNNRCBbIm5vZGUiLCAiZGlzdC9zZXJ2ZXIuanMiXQoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09CiMg5rWL6K&#43;V6Zi25q61CiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQpGUk9NIGJ1aWxkLWRlcHMgQVMgdGVzdAoKIyDorr7nva7njq/looMKRU5WIE5PREVfRU5WPXRlc3QgXAogICAgQ0k9dHJ1ZQoKIyDlpI3liLbmupDmlofku7YKQ09QWSAtLWNob3duPW5vZGVqczpub2RlanMgLiAuCgojIOWIh&#43;aNouWIsOmdniByb290IOeUqOaItwpVU0VSIG5vZGVqcwoKIyDov5DooYzluKbopobnm5bnjofnmoTmtYvor5UKQ01EIFsibnBtIiwgInJ1biIsICJ0ZXN0OmNvdmVyYWdlIl0=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 优化的多阶段 Dockerfile</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># Node.js TypeScript 应用</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">NODE_VERSION</span><span class="o">=</span><span class="m">24</span>.11.1-alpine<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> node:${NODE_VERSION} AS base</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> addgroup -g <span class="m">1001</span> -S nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    adduser -S nodejs -u <span class="m">1001</span> -G nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 依赖阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制包文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装生产依赖项</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.npm,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm ci --omit<span class="o">=</span>dev <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm cache clean --force<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置正确的所有权</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建依赖阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> base AS build-deps</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 复制包文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 安装所有依赖项并进行构建优化</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.npm,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm ci --no-audit --no-fund <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    npm cache clean --force<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建必要的目录并设置权限</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> mkdir -p /app/node_modules/.vite <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 仅复制构建所需的文件（遵循 .dockerignore）</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --chown<span class="o">=</span>nodejs:nodejs . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 构建应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> npm run build<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置正确的所有权</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 开发阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS development</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span>development <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NPM_CONFIG_LOGLEVEL</span><span class="o">=</span>warn
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 复制源文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 确保所有目录具有正确的权限</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> mkdir -p /app/node_modules/.vite <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chmod -R <span class="m">755</span> /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 3000 5173 9229</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 启动开发服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;npm&#34;</span><span class="p">,</span> <span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;dev:docker&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 生产阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> <span class="nv">NODE_VERSION</span><span class="o">=</span><span class="m">24</span>.11.1-alpine<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> node:${NODE_VERSION} AS production</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置工作目录</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 创建非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> addgroup -g <span class="m">1001</span> -S nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    adduser -S nodejs -u <span class="m">1001</span> -G nodejs <span class="o">&amp;&amp;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    chown -R nodejs:nodejs /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置优化的环境变量</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span>production <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NODE_OPTIONS</span><span class="o">=</span><span class="s2">&#34;--max-old-space-size=256 --no-warnings&#34;</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">NPM_CONFIG_LOGLEVEL</span><span class="o">=</span>silent<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 从 deps 阶段复制生产依赖项</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>deps --chown<span class="o">=</span>nodejs:nodejs /app/node_modules ./node_modules<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>deps --chown<span class="o">=</span>nodejs:nodejs /app/package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 从 build 阶段复制构建好的应用程序</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build --chown<span class="o">=</span>nodejs:nodejs /app/dist ./dist<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户以提高安全性</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 暴露端口</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">EXPOSE</span><span class="s"> 3000</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 启动生产服务器</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;node&#34;</span><span class="p">,</span> <span class="s2">&#34;dist/server.js&#34;</span><span class="p">]</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 测试阶段</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># ========================================</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> build-deps AS test</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 设置环境</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENV</span> <span class="nv">NODE_ENV</span><span class="o">=</span><span class="nb">test</span> <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    <span class="nv">CI</span><span class="o">=</span><span class="nb">true</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c"># 复制源文件</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --chown<span class="o">=</span>nodejs:nodejs . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 切换到非 root 用户</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">USER</span><span class="s"> nodejs</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="c"># 运行带覆盖率的测试</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;npm&#34;</span><span class="p">,</span> <span class="s2">&#34;run&#34;</span><span class="p">,</span> <span class="s2">&#34;test:coverage&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


此 Dockerfile 的主要特点：
- **多阶段结构** — 为依赖项、构建、开发、生产、测试分离阶段，保持每个阶段的干净和高效。
- **精简的生产镜像** — 优化的分层减少了体积，并仅保留运行应用所需的内容。
- **安全导向的设置** — 使用专用的非 root 用户，并排除不必要的包。
- **性能友好的设计** — 有效利用缓存和结构良好的层，实现更快的构建。
- **干净的运行时环境** — 删除生产中不需要的文件，如文档、测试和构建缓存。
- **直接的端口使用** — 应用在内部端口 3000 运行，外部暴露为端口 8080。
- **内存优化的运行时** — Node.js 配置为以比默认值更小的内存限制运行。

### 步骤 2：配置 .dockerignore 文件

`.dockerignore` 文件告诉 Docker 在构建镜像时要排除哪些文件和文件夹。

> [!NOTE]
> 这有助于：
>
> - 减小镜像体积
> - 加快构建过程
> - 防止敏感或不必要的文件（如 `.env`、`.git` 或 `node_modules`）被添加到最终镜像中。
>
> 要了解更多信息，请访问 [.dockerignore 参考](/reference/dockerfile.md#dockerignore-file)。

复制并用优化配置替换您现有的 `.dockerignore` 内容：

```dockerignore
# Node.js + React Todo 应用的优化 .dockerignore
# 基于实际项目结构

# 版本控制
.git/
.github/
.gitignore

# 依赖项（在容器中安装）
node_modules/

# 构建输出（在容器中构建）
dist/

# 环境文件
.env*

# 开发文件
.vscode/
*.log
coverage/
.eslintcache

# 操作系统文件
.DS_Store
Thumbs.db

# 文档
*.md
docs/

# 部署配置
compose.yml
Taskfile.yml
nodejs-sample-kubernetes.yaml

# 非必要配置（保留构建配置）
*.config.js
!vite.config.ts
!esbuild.config.js
!tailwind.config.js
!postcss.config.js
!tsconfig.json
```

### 步骤 3：构建 Node.js 应用镜像

创建所有配置文件后，您的项目目录现在应包含所有必要的 Docker 配置文件：

```text
├── docker-nodejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yml
│ └── README.Docker.md
```

现在您可以为您的 Node.js 应用构建 Docker 镜像。

> [!NOTE]
> `docker build` 命令使用 Dockerfile 中的说明将您的应用程序打包到镜像中。它包括来自当前目录（称为 [构建上下文](/build/concepts/context/#what-is-a-build-context)）的所有必要文件。

从项目根目录运行以下命令：

```console
$ docker build --target production --tag docker-nodejs-sample .
```

此命令的作用：

- 使用当前目录 (.) 中的 Dockerfile
- 以多阶段构建的生产阶段为目标
- 将应用程序及其依赖项打包到 Docker 镜像中
- 将镜像标记为 docker-nodejs-sample，以便稍后引用

#### 步骤 4：查看本地镜像

构建 Docker 镜像后，您可以使用 Docker CLI 或 [Docker Desktop](/manuals/desktop/use-desktop/images.md) 检查本地机器上可用的镜像。由于您已经在终端中工作，请使用 Docker CLI。

要列出所有本地可用的 Docker 镜像，请运行以下命令：

```console
$ docker images
```

示例输出：

```shell
REPOSITORY               TAG              IMAGE ID       CREATED         SIZE
docker-nodejs-sample     latest           423525528038   14 seconds ago  237.46MB
```

此输出提供有关镜像的关键详细信息：

- **Repository** – 分配给镜像的名称。
- **Tag** – 有助于识别不同构建的版本标签（例如，latest）。
- **Image ID** – 镜像的唯一标识符。
- **Created** – 指示镜像构建时间的时间戳。
- **Size** – 镜像使用的总磁盘空间。

如果构建成功，您应该会看到列出的 `docker-nodejs-sample` 镜像。

---

## 运行容器化应用

在上一步中，您为 Node.js 应用创建了 Dockerfile，并使用 docker build 命令构建了 Docker 镜像。现在是时候在容器中运行该镜像并验证您的应用是否按预期工作。

在 `docker-nodejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up app-dev --build
```

开发应用程序将启动两个服务器：

- **API 服务器**: [http://localhost:3000](http://localhost:3000) - 带有 REST API 的 Express.js 后端
- **前端**: [http://localhost:5173](http://localhost:5173) - 带有 React 前端的 Vite 开发服务器
- **健康检查**: [http://localhost:3000/health](http://localhost:3000/health) - 应用程序健康状态

对于生产部署，您可以使用：

```console
$ docker compose up app-prod --build
```

这将在 [http://localhost:8080](http://localhost:8080) 上提供全栈应用，Express 服务器在内部端口 3000 运行，映射到外部端口 8080。

您应该会看到一个带有 React 19 的现代 Todo List 应用程序和一个功能齐全的 REST API。

在终端中按 `CTRL + C` 停止您的应用程序。

### 在后台运行应用程序

您可以通过添加 `-d` 选项在终端分离的情况下运行应用程序。在 `docker-nodejs-sample` 目录中，在终端中运行以下命令。

```console
$ docker compose up app-dev --build -d
```

打开浏览器并查看应用程序，访问 [http://localhost:3000](http://localhost:3000) (API) 或 [http://localhost:5173](http://localhost:5173) (前端)。您应该会看到 Todo 应用程序正在运行。

要确认容器正在运行，请使用 `docker ps` 命令：

```console
$ docker ps
```

这将列出所有活动容器及其端口、名称和状态。查找为开发应用暴露端口 3000、5173 和 9229 的容器。

示例输出：

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED          STATUS                 PORTS                                                                                                                                   NAMES
93f3faee32c3   docker-nodejs-sample-app-dev   "docker-entrypoint.s…"   33 seconds ago   Up 31 seconds          0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp, 0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp, 0.0.0.0:9230->9229/tcp, [::]:9230->9229/tcp   todoapp-dev
```

### 运行不同的配置文件

您可以使用 Docker Compose 配置文件运行不同的配置：

```console
# 运行生产环境
$ docker compose up app-prod -d

# 运行测试
$ docker compose up app-test -d
```

要停止应用程序，请运行：

```console
$ docker compose down
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本指南中，您学习了如何使用 Docker 容器化、构建和运行 Node.js 应用。通过遵循最佳实践，您创建了一个安全、优化且生产就绪的设置。

您完成的任务：

- 使用 `docker init` 初始化项目以搭建基本的 Docker 配置文件。
- 创建了一个包含开发、生产、测试和数据库服务的 `compose.yml` 文件。
- 使用 `.env` 文件设置环境配置，以便灵活部署。
- 用针对 TypeScript 和 React 优化的多阶段构建替换了默认的 `dockerfile`。
- 用优化的配置替换了默认的 `.dockerignore` 文件，以排除不必要的文件并保持镜像干净高效。
- 使用 `docker build` 构建了您的 Docker 镜像。
- 使用 `docker compose up` 运行容器，包括前台运行和分离模式运行。
- 通过访问 [http://localhost:8080](http://localhost:8080) (生产环境) 或 [http://localhost:3000](http://localhost:3000) (开发环境) 验证应用正在运行。
- 学习了如何使用 `docker compose down` 停止容器化应用。

您现在拥有一个完全容器化的 Node.js 应用，运行在 Docker 容器中，并准备好以自信和一致性部署到任何环境。

---

## 相关资源

探索官方参考和最佳实践，以优化您的 Docker 工作流程：

- [多阶段构建](/build/building/multi-stage/) – 了解如何分离构建和运行时阶段。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Docker 中的构建上下文](/build/concepts/context/) – 了解上下文如何影响镜像构建。
- [`docker init` CLI 参考](/reference/cli/docker/init/) – 自动搭建 Docker 资产。
- [`docker build` CLI 参考](/reference/cli/docker/build/) – 从 Dockerfile 构建 Docker 镜像。
- [`docker images` CLI 参考](/reference/cli/docker/images/) – 管理和检查本地 Docker 镜像。
- [`docker compose up` CLI 参考](/reference/cli/docker/compose/up/) – 启动和运行多容器应用。
- [`docker compose down` CLI 参考](/reference/cli/docker/compose/down/) – 停止并移除容器、网络和卷。

---

## 下一步

您的 Node.js 应用现已容器化，您可以继续进行下一步。

在下一节中，您将学习如何使用 Docker 容器开发您的应用程序，从而在任何机器上实现一致、隔离且可复现的开发环境。
