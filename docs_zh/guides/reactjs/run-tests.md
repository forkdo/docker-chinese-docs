---
title: 在容器中运行 React.js 测试
linkTitle: 运行你的测试
weight: 40
keywords: react.js, react, test, vitest
description: 了解如何在容器中运行 React.js 测试。

---

## 前置条件

完成本指南的所有前面章节，从 [容器化 React.js 应用](containerize.md) 开始。

## 概述

测试是开发流程中的关键环节。在本节中，你将学习如何：

- 在 Docker 容器内使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离、可复现的环境中运行测试。

你将使用 [Vitest](https://vitest.dev) —— 一个专为 Vite 设计的极速测试运行器，结合 [Testing Library](https://testing-library.com/) 进行断言。

---

## 在开发期间运行测试

`docker-reactjs-sample` 应用在以下位置包含一个示例测试文件：

```console
$ src/App.test.tsx
```

该文件使用 Vitest 和 React Testing Library 验证 `App` 组件的行为。

### 步骤 1：安装 Vitest 和 React Testing Library

如果尚未添加必要的测试工具，请运行以下命令安装：

```console
$ npm install --save-dev vitest @testing-library/react @testing-library/jest-dom jsdom
```

然后，更新 `package.json` 文件的 scripts 部分，添加以下内容：

```json
"scripts": {
  "test": "vitest run"
}
```

---

### 步骤 2：配置 Vitest

在项目根目录更新 `vitest.config.ts` 文件，添加以下配置：

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
> - `environment: "jsdom"` 为渲染和 DOM 交互模拟浏览器环境。
> - `setupFiles: "./src/setupTests.ts"` 在每个测试文件之前加载全局配置或模拟（可选但推荐）。
> - `globals: true` 启用全局测试函数（如 `describe`、`it` 和 `expect`），无需导入。
>
> 更多详情，请参阅官方 [Vitest 配置文档](https://vitest.dev/config/)。

### 步骤 3：更新 compose.yaml

在 `compose.yaml` 文件中添加一个名为 `react-test` 的新服务。该服务允许你在隔离的容器化环境中运行测试套件。

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

`react-test` 服务复用了开发阶段使用的相同 `Dockerfile.dev`，并覆盖默认命令以 `npm run test` 运行测试。此设置确保测试环境与你的本地开发配置一致。

完成上述步骤后，你的项目目录应包含以下文件：

```text
├── docker-reactjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 4：运行测试

从项目根目录运行以下命令，在容器内执行测试套件：

```console
$ docker compose run --rm react-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `react-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 测试完成后自动删除容器（使用 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令）。

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，你学习了如何在 Docker 容器中使用 Vitest 和 Docker Compose 运行 React.js 应用的单元测试。

你的收获：
- 安装并配置 Vitest 和 React Testing Library 以测试 React 组件。
- 在 `compose.yaml` 中创建 `react-test` 服务以隔离测试执行。
- 复用开发用的 `Dockerfile.dev`，确保开发和测试环境的一致性。
- 使用 `docker compose run --rm react-test` 在容器内运行测试。
- 确保跨环境的测试可靠性和可重复性，不依赖本地机器配置。

---

## 相关资源

探索官方参考和最佳实践，优化你的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) – 理解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 学习 `compose.yaml` 中配置服务的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。

---

## 后续步骤

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 管道，自动在容器化环境中构建和测试你的 React.js 应用。这确保你的代码在每次推送或拉取请求时得到验证，保持开发工作流的一致性和可靠性。