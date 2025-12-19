---
title: 在容器中运行 Vue.js 测试
linkTitle: 运行测试
weight: 40
keywords: vue.js, vue, test, vitest
description: 了解如何在容器中运行 Vue.js 测试。

---

## 先决条件

请完成本指南的所有先前部分，从 [容器化 Vue.js 应用程序](containerize.md) 开始。

## 概述

测试是开发过程中的关键部分。在本节中，您将学习如何：

- 在 Docker 容器中使用 Vitest 运行单元测试。
- 使用 Docker Compose 在隔离、可重现的环境中运行测试。

您将使用 [Vitest](https://vitest.dev) — 一个为 Vite 设计的超快测试运行器 — 与 [@vue/test-utils](https://test-utils.vuejs.org/) 结合使用，编写单元测试来验证您的组件逻辑、props、事件和响应式行为。

此设置确保您的 Vue.js 组件在反映用户实际与应用程序交互方式的环境中进行测试。

---

## 在开发过程中运行测试

`docker-vuejs-sample` 应用程序在以下位置包含一个示例测试文件：

```console
$ src/components/__tests__/HelloWorld.spec.ts
```

此测试使用 Vitest 和 Vue Test Utils 来验证 HelloWorld 组件的行为。

---

### 步骤 1：更新 compose.yaml

在您的 `compose.yaml` 文件中添加一个名为 `vuejs-test` 的新服务。此服务允许您在隔离的容器化环境中运行您的测试套件。

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

`vuejs-test` 服务重用用于 [开发](develop.md) 的同一个 `Dockerfile.dev`，并覆盖默认命令以使用 `npm run test` 运行测试。此设置确保了与本地开发配置相匹配的一致测试环境。

完成前面的步骤后，您的项目目录应包含以下文件：

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

要从项目根目录在容器内执行您的测试套件，请运行以下命令：

```console
$ docker compose run --rm vuejs-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `vuejs-test` 服务。
- 使用与开发相同的环境执行 `npm run test` 脚本。
- 在测试完成后自动移除容器 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令。

您应该会看到类似于以下内容的输出：

```shell
Test Files: 1 passed (1)
Tests:      1 passed (1)
Start at:   16:50:55
Duration:   718ms
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI 参考](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，您学习了如何使用 Vitest 和 Docker Compose 在 Docker 容器中为您的 Vue.js 应用程序运行单元测试。

您完成的任务：
- 在 `compose.yaml` 中创建了 `vuejs-test` 服务以隔离测试执行。
- 重用了开发 `Dockerfile.dev` 以确保开发和测试环境之间的一致性。
- 使用 `docker compose run --rm vuejs-test` 在容器内运行测试。
- 确保了跨环境可靠、可重复的测试，而不依赖于您的本地机器设置。

---

## 相关资源

探索官方参考资料和最佳实践，以优化您的 Docker 测试工作流程：

- [Dockerfile 参考](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考](/compose/compose-file/) – 了解用于在 `compose.yaml` 中配置服务的完整语法和可用选项。
- [`docker compose run` CLI 参考](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。

---

## 下一步

接下来，您将学习如何使用 GitHub Actions 设置 CI/CD 管道，以在容器化环境中自动构建和测试您的 Vue.js 应用程序。这可确保您的代码在每次推送或拉取请求时都得到验证，从而在您的开发工作流程中保持一致性和可靠性。