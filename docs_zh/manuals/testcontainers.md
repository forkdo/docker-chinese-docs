---
title: Testcontainers
weight: 40
description: 了解如何在您首选的编程语言中以编程方式使用 Testcontainers 运行容器。
keywords: docker APIs, docker, testcontainers documentation, testcontainers, testcontainers oss, testcontainers oss documentation,
  docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: 开源项目
intro:
- title: Testcontainers 是什么？
  description: 了解 Testcontainers 的功能及其主要优势
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流程
  description: 了解 Testcontainers 的工作流程
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Go 版 Testcontainers
  description: 一个 Go 语言包，可简化基于容器的依赖项的创建和清理，用于自动化集成/冒烟测试。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Java 版 Testcontainers
  description: 一个支持 JUnit 测试的 Java 库，提供可在 Docker 容器中运行的任何内容的轻量级、一次性实例。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一组开源库，提供了简单且轻量级的 API，用于通过 Docker 容器封装的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，您可以编写依赖于生产环境中使用的相同服务的测试，而无需使用模拟或内存服务。

{{< grid items=intro >}}

## 快速入门

### 支持的语言

Testcontainers 为最流行的语言提供支持，Docker 赞助了以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余版本由社区驱动，并由独立贡献者维护。

### 先决条件

Testcontainers 需要一个兼容 Docker API 的容器运行时。
在开发过程中，Testcontainers 会针对 Linux 上的最新 Docker 版本以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。
Testcontainers 会自动检测并使用这些 Docker 环境，无需进行任何额外配置。

可以配置 Testcontainers 以适用于其他 Docker 设置，例如远程 Docker 主机或 Docker 替代方案。
但是，这些设置不会在主开发工作流程中积极测试，因此可能无法使用所有 Testcontainers 功能，
并且可能需要额外的手动配置。

如果您对您的设置配置细节或是否支持运行基于 Testcontainers 的测试有进一步疑问，
请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队以及 Testcontainers 社区的其他用户。

 {{< grid items=quickstart >}}