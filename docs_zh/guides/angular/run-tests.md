---
title: 在容器中运行 Angular 测试
linkTitle: 运行测试
weight: 40
keywords: angular, test, jasmine
description: 学习如何在容器中运行 Angular 测试。
---

## 先决条件

完成本指南的所有前面部分，从 [容器化 Angular 应用](containerize.md) 开始。

## 概述

测试是开发过程中的关键环节。在本节中，你将学习如何：

- 在 Docker 容器内使用 Angular CLI 运行 Jasmine 单元测试。
- 使用 Docker Compose 隔离测试环境。
- 确保本地测试与基于容器的测试之间的一致性。

`docker-angular-sample` 项目已预配置 Jasmine，因此无需额外设置即可快速开始测试。

---

## 在开发期间运行测试

`docker-angular-sample` 应用包含一个示例测试文件，位于以下位置：

```console
$ src/app/app.component.spec.ts
```

该测试使用 Jasmine 验证 AppComponent 的逻辑。

### 步骤 1：更新 compose.yaml

在 `compose.yaml` 文件中添加一个名为 `angular-test` 的新服务。该服务允许你在隔离的容器化环境中运行测试套件。

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

`angular-test` 服务复用了 [开发环境](develop.md) 中使用的 `Dockerfile.dev`，并覆盖默认命令以通过 `npm run test` 运行测试。此设置确保测试环境与本地开发配置保持一致。

完成上述步骤后，你的项目目录应包含以下文件：

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── nginx.conf
│ └── README.Docker.md
```

### 步骤 2：运行测试

要从项目根目录在容器内执行测试套件，请运行以下命令：

```console
$ docker compose run --rm angular-test
```

该命令将：
- 启动 `compose.yaml` 文件中定义的 `angular-test` 服务。
- 使用与开发环境相同的配置执行 `npm run test` 脚本。
- 测试完成后自动删除容器，使用 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令。

你应该会看到类似以下的输出：

```shell
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.529 s
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参见 [Compose CLI 参考文档](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，你学习了如何使用 Jasmine 和 Docker Compose 在 Docker 容器内为 Angular 应用运行单元测试。

你已完成以下任务：
- 在 `compose.yaml` 中创建 `angular-test` 服务以隔离测试执行。
- 复用开发环境的 `Dockerfile.dev`，确保开发与测试环境的一致性。
- 使用 `docker compose run --rm angular-test` 在容器内运行测试。
- 确保跨环境测试的可靠性和可重复性，无需依赖本地机器配置。

---

## 相关资源

探索官方参考和最佳实践，以优化你的 Docker 测试工作流：

- [Dockerfile 参考文档](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考文档](/compose/compose-file/) – 学习 `compose.yaml` 中服务配置的完整语法和选项。  
- [`docker compose run` CLI 参考文档](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。
---

## 下一步

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 流水线，以在容器化环境中自动构建和测试 Angular 应用。这能确保每次推送或拉取请求时都验证代码，保持开发工作流的一致性和可靠性。