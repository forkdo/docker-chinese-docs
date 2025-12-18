---
title: Testcontainers
weight: 40
description: 了解如何使用 Testcontainers 在你首选的编程语言中以编程方式运行容器。
keywords: docker APIs, docker, testcontainers documentation, testcontainers, testcontainers oss, testcontainers oss documentation,
  docker compose, docker-compose, java, golang, go
params:
  sidebar:
    group: Open source
intro:
- title: 什么是 Testcontainers？
  description: 了解 Testcontainers 的功能及其主要优势
  icon: feature_search
  link: https://testcontainers.com/getting-started/#what-is-testcontainers
- title: Testcontainers 工作流
  description: 了解 Testcontainers 的工作流程
  icon: explore
  link: https://testcontainers.com/getting-started/#testcontainers-workflow
quickstart:
- title: Testcontainers for Go
  description: 一个 Go 包，可简化创建和清理基于容器的依赖项的过程，适用于自动化集成/冒烟测试。
  icon: /icons/go.svg
  link: https://golang.testcontainers.org/quickstart/
- title: Testcontainers for Java
  description: 一个 Java 库，支持 JUnit 测试，提供轻量级、一次性的 Docker 容器实例，可运行任何能在容器中运行的内容。
  icon: /icons/java.svg
  link: https://java.testcontainers.org/
---

Testcontainers 是一组开源库，提供简单且轻量级的 API，用于通过包装在 Docker 容器中的真实服务来引导本地开发和测试依赖项。
使用 Testcontainers，你可以编写依赖于与生产环境相同服务的测试，而无需使用模拟（mocks）或内存中的服务。

{{< grid items=intro >}}

## 快速开始

### 支持的语言

Testcontainers 为最流行的编程语言提供支持，Docker 赞助以下 Testcontainers 实现的开发：

- [Go](https://golang.testcontainers.org/quickstart/)
- [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

其余语言的实现由社区驱动，由独立贡献者维护。

### 先决条件

Testcontainers 需要 Docker API 兼容的容器运行时。
在开发过程中，Testcontainers 会主动针对 Linux 上的最新版本 Docker，以及 Mac 和 Windows 上的 Docker Desktop 进行测试。
这些 Docker 环境会被自动检测并由 Testcontainers 使用，无需额外配置。

Testcontainers 也可以配置为支持其他 Docker 设置，例如远程 Docker 主机或 Docker 替代方案。
但是，这些设置未在主要开发工作流中主动测试，因此并非所有 Testcontainers 功能都可用，
并且可能需要额外的手动配置。

如果你对设置的配置细节有疑问，或不确定你的环境是否支持运行基于 Testcontainers 的测试，
请在 [Slack](https://slack.testcontainers.org/) 上联系 Testcontainers 团队和其他 Testcontainers 社区用户。

 {{< grid items=quickstart >}}