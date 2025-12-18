---
title: 在容器中运行 Vue.js 测试
linkTitle: 运行你的测试
weight: 40
keywords: vue.js, vue, test, vitest
description: 了解如何在容器中运行你的 Vue.js 测试。

---

## 前置条件

完成本指南的所有前置部分，从 [容器化 Vue.js 应用](containerize.md) 开始。

## 概述

测试是开发流程中的关键环节。在本节中，你将学习如何：

- 在 Docker 容器内使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离且可复现的环境中运行测试。

你将使用 [Vitest](https://vitest.dev) —— 一个专为 Vite 设计的超快测试运行器 —— 结合 [@vue/test-utils](https://test-utils.vuejs.org/) 编写单元测试，验证组件逻辑、属性、事件和响应式行为。

此设置确保你的 Vue.js 组件在与用户实际交互环境一致的条件下进行测试。

---

## 在开发过程中运行测试

`docker-vuejs-sample` 应用包含一个示例测试文件，位于：

```console
$ src/components/__tests__/HelloWorld.spec.ts
```

该测试使用 Vitest 和 Vue Test Utils 验证 HelloWorld 组件的行为。

---

### 步骤 1：更新 compose.yaml

在 `compose.yaml` 文件中添加一个名为 `vuejs-test` 的新服务。该服务允许你在隔离的容器化环境中运行测试套件。

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

`vuejs-test` 服务复用了与 [开发环境](develop.md) 相同的 `Dockerfile.dev`，并覆盖默认命令以 `npm run test` 执行测试。此设置确保测试环境与本地开发配置保持一致。

完成上述步骤后，你的项目目录应包含以下文件：

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 2：运行测试

从项目根目录执行以下命令，在容器中执行测试套件：

```console
$ docker compose run --rm vuejs-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `vuejs-test` 服务。
- 使用与开发环境相同的环境执行 `npm run test` 脚本。
- 测试完成后自动删除容器（通过 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令）。

你应该会看到类似以下的输出：

```shell
Test Files: 1 passed (1)
Tests:      1 passed (1)
Start at:   16:50:55
Duration:   718ms
```

> [!NOTE]
> 有关 Compose 命令的详细信息，请参阅 [Compose CLI
> 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，你学会了如何在 Docker 容器中使用 Vitest 和 Docker Compose 运行 Vue.js 应用的单元测试。

你的成果包括：
- 在 `compose.yaml` 中创建 `vuejs-test` 服务以隔离测试执行。
- 复用开发环境的 `Dockerfile.dev`，确保开发与测试环境的一致性。
- 使用 `docker compose run --rm vuejs-test` 在容器中运行测试。
- 确保测试在不同环境中可靠且可重复，不依赖本地机器配置。

---

## 相关资源

探索官方参考和最佳实践，优化你的 Docker 测试工作流：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 学习 `compose.yaml` 中配置服务的完整语法和选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。

---

## 后续步骤

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 管道，在容器化环境中自动构建和测试你的 Vue.js 应用。这确保你的代码在每次推送或拉取请求时得到验证，保持开发工作流的一致性和可靠性。