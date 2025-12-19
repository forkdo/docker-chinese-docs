---
title: 为 Node.js 开发使用容器
linkTitle: 开发您的应用
weight: 30
keywords: node, node.js, development
description: 了解如何使用容器在本地开发 Node.js 应用程序。
aliases:
  - /get-started/nodejs/develop/
  - /language/nodejs/develop/
  - /guides/language/nodejs/develop/
---

## 先决条件

完成 [容器化 Node.js 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 添加本地数据库并持久化数据
- 配置容器以运行开发环境
- 调试容器化应用程序

## 添加本地数据库并持久化数据

该应用程序使用 PostgreSQL 进行数据持久化。向您的 Docker Compose 配置中添加一个数据库服务。

### 向 Docker Compose 添加数据库服务

如果您在上一节中尚未创建 `compose.yml` 文件，或者需要添加数据库服务，请更新您的 `compose.yml` 文件以包含 PostgreSQL 数据库服务：

```yaml
services:
  # ... 现有的应用服务 ...

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

### 更新您的应用服务

确保 `compose.yml` 中的应用服务配置为连接到数据库：

```yaml {hl_lines="18-20,42-44",collapse=true,title=compose.yml}
services:
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

volumes:
  postgres_data:
    name: todoapp-postgres-data
    driver: local

networks:
  todoapp-network:
    name: todoapp-network
    driver: bridge
```

1. PostgreSQL 数据库配置由应用程序自动处理。数据库在应用程序启动时创建和初始化，数据使用 `postgres_data` 卷进行持久化。

1. 通过复制示例文件来配置您的环境：

   ```console
   $ cp .env.example .env
   ```

   使用您首选的设置更新 `.env` 文件：

   ```env
   # 应用程序配置
   NODE_ENV=development
   APP_PORT=3000
   VITE_PORT=5173
   DEBUG_PORT=9230

   # 数据库配置
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   POSTGRES_DB=todoapp
   POSTGRES_USER=todoapp
   POSTGRES_PASSWORD=todoapp_password

   # 安全配置
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

1. 运行以下命令以开发模式启动您的应用程序：

   ```console
   $ docker compose up app-dev --build
   ```

1. 打开浏览器并验证应用程序是否在 [http://localhost:5173](http://localhost:5173)（前端）或 [http://localhost:3000](http://localhost:3000)（API）运行。React 前端由端口 5173 上的 Vite 开发服务器提供服务，API 调用被代理到端口 3000 上的 Express 服务器。

1. 向待办事项列表添加一些项目以测试数据持久化。

1. 向待办事项列表添加一些项目后，在终端中按 `CTRL + C` 停止您的应用程序。

1. 再次运行应用程序：
   ```console
   $ docker compose up app-dev
   ```

1. 在浏览器中刷新 [http://localhost:5173](http://localhost:5173) 并验证待办事项是否持久存在，即使在容器被移除并再次运行之后也是如此。

## 配置并运行开发容器

您可以使用绑定挂载将源代码挂载到容器中。然后，容器可以在您保存文件后立即看到您对代码所做的更改。这意味着您可以在容器中运行诸如 nodemon 之类的进程，这些进程会监视文件系统更改并对其做出响应。要了解有关绑定挂载的更多信息，请参阅 [存储概览](/manuals/engine/storage/_index.md)。

除了添加绑定挂载之外，您还可以配置您的 Dockerfile 和 `compose.yaml` 文件以安装开发依赖项并运行开发工具。

### 为开发更新您的 Dockerfile

您的 Dockerfile 应配置为多阶段构建，具有用于开发、生产和测试的单独阶段。如果您遵循了上一节，您的 Dockerfile 已经包含一个开发阶段，该阶段具有所有开发依赖项，并在启用热重载的情况下运行应用程序。

以下是您的多阶段 Dockerfile 中的开发阶段：

```dockerfile {hl_lines="5-26",collapse=true,title=Dockerfile}
# ========================================
# 开发阶段
# ========================================
FROM build-deps AS development

# 设置环境
ENV NODE_ENV=development \
    NPM_CONFIG_LOGLEVEL=warn

# 复制源文件
COPY . .

# 确保所有目录具有适当的权限
RUN mkdir -p /app/node_modules/.vite && \
    chown -R nodejs:nodejs /app && \
    chmod -R 755 /app

# 切换到非 root 用户
USER nodejs

# 暴露端口
EXPOSE 3000 5173 9229

# 启动开发服务器
CMD ["npm", "run", "dev:docker"]
```

开发阶段：

- 安装所有依赖项，包括开发依赖项
- 暴露 API 服务器 (3000)、Vite 开发服务器 (5173) 和 Node.js 调试器 (9229) 的端口
- 运行 `npm run dev`，该命令同时启动 Express 服务器和 Vite 开发服务器
- 包含用于监控容器状态的健康检查

接下来，您需要更新您的 Compose 文件以使用新阶段。

### 为开发更新您的 Compose 文件

更新您的 `compose.yml` 文件以运行开发阶段，并使用绑定挂载实现热重载：

```yaml {hl_lines=[5,8-10,20-27],collapse=true,title=compose.yml}
services:
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
```

开发配置的关键特性：

- **多端口暴露**：API 服务器 (3000)、Vite 开发服务器 (5173) 和调试器 (9229)
- **全面的绑定挂载**：源代码、配置文件和包文件，用于热重载
- **环境变量**：可通过 `.env` 文件或默认值进行配置
- **PostgreSQL 数据库**：具有持久存储的生产就绪数据库
- **Docker Compose watch**：自动文件同步和容器重建
- **健康检查**：数据库健康监控，具有自动依赖管理

### 运行您的开发容器并调试您的应用程序

运行以下命令以使用开发配置运行您的应用程序：

```console
$ docker compose up app-dev --build
```

或使用文件监视以实现自动更新：

```console
$ docker compose up app-dev --watch
```

对于不使用 Docker 的本地开发：

```console
$ npm run dev:with-db
```

或单独启动服务：

```console
$ npm run db:start    # 启动 PostgreSQL 容器
$ npm run dev         # 同时启动服务器和客户端
```

### 使用任务运行器（替代方案）

该项目包含一个用于高级工作流的 Taskfile.yml：

```console
# 开发
$ task dev              # 启动开发环境
$ task dev:build        # 构建开发镜像
$ task dev:run          # 运行开发容器

# 生产
$ task build            # 构建生产镜像
$ task run              # 运行生产容器
$ task build-run        # 一步构建并运行

# 测试
$ task test             # 运行所有测试
$ task test:unit        # 运行带覆盖率的单元测试
$ task test:lint        # 运行代码检查

# Kubernetes
$ task k8s:deploy       # 部署到 Kubernetes
$ task k8s:status       # 检查部署状态
$ task k8s:logs         # 查看 Pod 日志

# 实用工具
$ task clean            # 清理容器和镜像
$ task health           # 检查应用程序健康状况
$ task logs             # 查看容器日志
```

应用程序将同时启动 Express API 服务器和 Vite 开发服务器：

- **API 服务器**：[http://localhost:3000](http://localhost:3000) - 带有 REST API 的 Express.js 后端
- **前端**：[http://localhost:5173](http://localhost:5173) - 带有热模块替换的 Vite 开发服务器
- **健康检查**：[http://localhost:3000/health](http://localhost:3000/health) - 应用程序健康状态

由于绑定挂载，您本地机器上对应用程序源文件的任何更改现在都会立即反映在正在运行的容器中。

尝试进行更改以测试热重载：

1. 在 IDE 或文本编辑器中打开 `src/client/components/TodoApp.tsx`。
2. 更新主标题文本：

    ```diff
    - <h1 className="text-3xl font-bold text-gray-900 mb-8">
    -   Modern Todo App
    - </h1>
    + <h1 className="text-3xl font-bold text-gray-900 mb-8">
    +   My Todo App
    + </h1>
    ```

3. 保存文件，Vite 开发服务器将自动使用您的更改重新加载页面。

**调试支持：**

您可以在端口 9229 上将调试器连接到您的应用程序。Node.js 检查器在开发脚本 (`dev:server`) 中通过 `--inspect=0.0.0.0:9230` 启用。

### VS Code 调试器设置

1. 在 `.vscode/launch.json` 中创建一个启动配置：

    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Attach to Docker Container",
          "type": "node",
          "request": "attach",
          "port": 9229,
          "address": "localhost",
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/app",
          "protocol": "inspector",
          "restart": true,
          "sourceMaps": true,
          "skipFiles": ["<node_internals>/**"]
        }
      ]
    }
    ```

2. 启动您的开发容器：

    ```console
    docker compose up app-dev --build
    ```

3. 附加调试器：
   - 打开 VS Code
   - 从调试面板 (Ctrl/Cmd + Shift + D)，从下拉菜单中选择 **Attach to Docker Container**
   - 选择绿色播放按钮或按 F5

### Chrome DevTools（替代方案）

您也可以使用 Chrome DevTools 进行调试：

1. 启动您的容器（如果尚未运行）：

    ```console
    docker compose up app-dev --build
    ```

2. 打开 Chrome 并转到 `chrome://inspect`。

3. 从 **Configure** 选项中，添加：

    ```text
    localhost:9229
    ```

4. 当您的 Node.js 目标出现时，选择 **inspect**。

### 调试配置详情

调试器配置：

- **容器端口**：9230（内部调试器端口）
- **主机端口**：9229（映射的外部端口）
- **脚本**：`tsx watch --inspect=0.0.0.0:9230 src/server/index.ts`

调试器在容器内部的所有接口 (`0.0.0.0`) 上的端口 9230 监听，并可从您的主机机器通过端口 9229 访问。

### 调试器连接故障排除

如果调试器无法连接：

1. 检查容器是否正在运行：

    ```console
    docker ps
    ```

2. 检查端口是否已暴露：

    ```console
    docker port todoapp-dev
    ```

3. 检查容器日志：

    ```console
    docker compose logs app-dev
    ```

    您应该会看到类似以下的消息：

    ```text
    Debugger listening on ws://0.0.0.0:9230/...
    ```

现在，您可以在 TypeScript 源文件中设置断点并调试您的容器化 Node.js 应用程序。

有关 Node.js 调试的更多详细信息，请参阅 [Node.js 文档](https://nodejs.org/en/docs/guides/debugging-getting-started)。

## 总结

您已在 Compose 文件中设置了 PostgreSQL 数据库和数据持久化。您还创建了一个多阶段 Dockerfile 并为开发配置了绑定挂载。

相关信息：

- [Volumes 顶层元素](/reference/compose-file/volumes/)
- [Services 顶层元素](/reference/compose-file/services/)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将学习如何使用 Docker 运行单元测试。