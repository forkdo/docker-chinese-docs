---
title: 在容器中运行 Angular 测试
linkTitle: 运行你的测试
weight: 40
keywords: angular, test, jasmine
description: 了解如何在容器中使用 Angular CLI 运行你的 Angular 测试。

---

## 前置条件

完成本指南中之前的所有部分，从 [容器化 Angular 应用](containerize.md) 开始。

## 概述

测试是开发过程中至关重要的一环。在本节中，你将学习如何：

- 在 Docker 容器内使用 Angular CLI 运行 Jasmine 单元测试。
- 使用 Docker Compose 隔离你的测试环境。
- 确保本地测试和容器化测试之间的一致性。

---

## 在开发期间运行测试

`docker-angular-sample` 项目已预配置了 Jasmine，因此你可以快速开始，无需额外设置。

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

`angular-test` 服务复用了与 [开发](develop.md) 相同的 `Dockerfile.dev`，并覆盖默认命令，使用 `npm run test` 运行测试。此设置确保测试环境与你的本地开发配置保持一致。

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

要从项目根目录执行容器内的测试套件，请运行以下命令：

```console
$ docker compose run --rm angular-test
```

此命令将：
- 启动 `compose.yaml` 文件中定义的 `angular-test` 服务。
- 使用与开发环境相同的环境执行 `npm run test` 脚本。
- 使用 [`docker compose run --rm`](/engine/reference/commandline/compose_run) 命令在测试完成后自动移除容器。

你应该会看到类似以下的输出：

```shell
Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        1.529 s
```

> [!NOTE]
> 有关 Compose 命令的更多信息，请参阅 [Compose CLI
> 参考文档](/reference/cli/docker/compose/_index.md)。

---

## 总结

在本节中，你学习了如何在 Docker 容器中使用 Jasmine 和 Docker Compose 运行 Angular 应用的单元测试。

你完成的内容：
- 在 `compose.yaml` 中创建了 `angular-test` 服务以隔离测试执行。
- 复用开发用的 `Dockerfile.dev`，确保开发和测试环境之间的一致性。
- 使用 `docker compose run --rm angular-test` 在容器内运行测试。
- 确保测试在不同环境中可靠且可重复，不依赖于本地机器配置。

---

## 相关资源

探索官方参考文档和最佳实践，以优化你的 Docker 测试工作流：

- [Dockerfile 参考文档](/reference/dockerfile/) – 了解所有 Dockerfile 指令和语法。
- [编写 Dockerfile 的最佳实践](/develop/develop-images/dockerfile_best-practices/) – 编写高效、可维护且安全的 Dockerfile。
- [Compose 文件参考文档](/compose/compose-file/) – 学习 `compose.yaml` 中配置服务的完整语法和选项。
- [`docker compose run` CLI 参考文档](/reference/cli/docker/compose/run/) – 在服务容器中运行一次性命令。
---

## 下一步

接下来，你将学习如何使用 GitHub Actions 设置 CI/CD 管道，以在容器化环境中自动构建和测试你的 Angular 应用。这确保你的代码在每次推送或拉取请求时得到验证，从而在整个开发工作流中保持一致性和可靠性。