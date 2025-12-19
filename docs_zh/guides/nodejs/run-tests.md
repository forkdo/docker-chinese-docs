---
title: 在容器中运行 Node.js 测试
linkTitle: 运行测试
weight: 30
keywords: node.js, node, test
description: 学习如何在容器中运行 Node.js 测试。
aliases:
  - /language/nodejs/run-tests/
  - /guides/language/nodejs/run-tests/
---

## 先决条件

完成本指南的所有先前章节，从[容器化 Node.js 应用程序](containerize.md)开始。

## 概述

测试是构建可靠软件的核心部分。无论您编写的是单元测试、集成测试还是端到端测试，在不同环境中一致地运行测试都至关重要。Docker 通过为您提供本地、CI/CD 和镜像构建期间相同的设置，使这变得简单。

## 本地开发时运行测试

示例应用程序使用 Vitest 进行测试，并且已经包含针对 React 组件、自定义钩子、API 路由、数据库操作和工具函数的测试。

### 本地运行测试（不使用 Docker）

```console
$ npm run test
```

### 在 Docker Compose 中添加测试服务

要在容器化环境中运行测试，您需要在 `compose.yml` 文件中添加专用的测试服务。添加以下服务配置：

```yaml
services:
  # ... 现有服务 ...

  # ========================================
  # 测试服务
  # ========================================
  app-test:
    build:
      context: .
      dockerfile: Dockerfile
      target: test
    container_name: todoapp-test
    environment:
      NODE_ENV: test
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
      POSTGRES_DB: todoapp_test
      POSTGRES_USER: todoapp
      POSTGRES_PASSWORD: '${POSTGRES_PASSWORD:-todoapp_password}'
    depends_on:
      db:
        condition: service_healthy
    command: ['npm', 'run', 'test:coverage']
    networks:
      - todoapp-network
    profiles:
      - test
```

此测试服务配置：

- **从测试阶段构建**：使用多阶段 Dockerfile 中的 `test` 目标
- **隔离的测试数据库**：使用单独的 `todoapp_test` 数据库进行测试
- **基于配置文件**：使用 `test` 配置文件，因此仅在明确要求时才运行
- **健康依赖**：在启动测试前等待数据库健康

### 在容器中运行测试

您可以使用专用测试服务运行测试：

```console
$ docker compose up app-test --build
```

或针对开发服务运行测试：

```console
$ docker compose run --rm app-dev npm run test
```

对于一次性带覆盖率的测试运行：

```console
$ docker compose run --rm app-dev npm run test:coverage
```

### 运行带覆盖率的测试

要生成覆盖率报告：

```console
$ npm run test:coverage
```

您应该看到类似以下输出：

```console
> docker-nodejs-sample@1.0.0 test
> vitest --run

 ✓ src/server/__tests__/routes/todos.test.ts (5 tests) 16ms
 ✓ src/shared/utils/__tests__/validation.test.ts (15 tests) 6ms
 ✓ src/client/components/__tests__/LoadingSpinner.test.tsx (8 tests) 67ms
 ✓ src/server/database/__tests__/postgres.test.ts (13 tests) 136ms
 ✓ src/client/components/__tests__/ErrorMessage.test.tsx (8 tests) 127ms
 ✓ src/client/components/__tests__/TodoList.test.tsx (8 tests) 147ms
 ✓ src/client/components/__tests__/TodoItem.test.tsx (8 tests) 218ms
 ✓ src/client/__tests__/App.test.tsx (13 tests) 259ms
 ✓ src/client/components/__tests__/AddTodoForm.test.tsx (12 tests) 323ms
 ✓ src/client/hooks/__tests__/useTodos.test.ts (11 tests) 569ms

 Test Files  9 passed (9)
      Tests  88 passed (88)
   Start at  20:57:19
   Duration  4.41s (transform 1.79s, setup 2.66s, collect 5.38s, tests 4.61s, environment 14.07s, prepare 4.34s)
```

### 测试结构

测试套件涵盖：

- **客户端组件** (`src/client/components/__tests__/`)：使用 React Testing Library 进行 React 组件测试
- **自定义钩子** (`src/client/hooks/__tests__/`)：使用适当模拟进行 React 钩子测试
- **服务器路由** (`src/server/__tests__/routes/`)：API 端点测试
- **数据库层** (`src/server/database/__tests__/`)：PostgreSQL 数据库操作测试
- **工具函数** (`src/shared/utils/__tests__/`)：验证和辅助函数测试
- **集成测试** (`src/client/__tests__/`)：完整应用程序集成测试

## 构建时运行测试

要在 Docker 构建过程中运行测试，您需要在 Dockerfile 中添加专用的测试阶段。如果您尚未添加此阶段，请将以下内容添加到您的多阶段 Dockerfile：

```dockerfile
# ========================================
# 测试阶段
# ========================================
FROM build-deps AS test

# 设置环境
ENV NODE_ENV=test \
    CI=true

# 复制源文件
COPY --chown=nodejs:nodejs . .

# 切换到非 root 用户
USER nodejs

# 运行带覆盖率的测试
CMD ["npm", "run", "test:coverage"]
```

此测试阶段：

- **测试环境**：设置 `NODE_ENV=test` 和 `CI=true` 以正确执行测试
- **非 root 用户**：以 `nodejs` 用户身份运行测试以确保安全
- **灵活执行**：使用 `CMD` 而不是 `RUN`，以允许在构建期间或作为独立容器运行测试
- **覆盖率支持**：配置为运行带覆盖率报告的测试

### 构建并在镜像构建期间运行测试

要构建在构建过程中运行测试的镜像，您可以创建自定义 Dockerfile 或临时修改现有 Dockerfile：

```console
$ docker build --target test -t node-docker-image-test .
```

### 在专用测试容器中运行测试

推荐的方法是使用 `compose.yml` 中定义的测试服务：

```console
$ docker compose --profile test up app-test --build
```

或将其作为一次性容器运行：

```console
$ docker compose run --rm app-test
```

### 在 CI/CD 中运行带覆盖率的测试

对于持续集成，您可以运行带覆盖率的测试：

```console
$ docker build --target test --progress=plain --no-cache -t test-image .
$ docker run --rm test-image npm run test:coverage
```

您应该看到包含以下内容的输出：

```console
 ✓ src/server/__tests__/routes/todos.test.ts (5 tests) 16ms
 ✓ src/shared/utils/__tests__/validation.test.ts (15 tests) 6ms
 ✓ src/client/components/__tests__/LoadingSpinner.test.tsx (8 tests) 67ms
 ✓ src/server/database/__tests__/postgres.test.ts (13 tests) 136ms
 ✓ src/client/components/__tests__/ErrorMessage.test.tsx (8 tests) 127ms
 ✓ src/client/components/__tests__/TodoList.test.tsx (8 tests) 147ms
 ✓ src/client/components/__tests__/TodoItem.test.tsx (8 tests) 218ms
 ✓ src/client/__tests__/App.test.tsx (13 tests) 259ms
 ✓ src/client/components/__tests__/AddTodoForm.test.tsx (12 tests) 323ms
 ✓ src/client/hooks/__tests__/useTodos.test.ts (11 tests) 569ms

 Test Files  9 passed (9)
      Tests  88 passed (88)
   Start at  20:57:19
   Duration  4.41s (transform 1.79s, setup 2.66s, collect 5.38s, tests 4.61s, environment 14.07s, prepare 4.34s)
```

## 总结

在本节中，您学习了如何使用 Docker Compose 在本地开发时运行测试，以及如何在构建镜像时运行测试。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 学习配置 `compose.yaml` 中服务的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。

## 下一步

接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 流水线。