---
title: 常见挑战与问题
description: 探索与 Docker Testcontainers Cloud 相关的常见挑战和问题。
weight: 40
---

<!-- vale Docker.HeadingLength = NO -->

### Testcontainers Cloud 与开源 Testcontainers 框架有何区别？

开源 Testcontainers 是一个提供轻量级 API 的库，用于通过 Docker 容器封装的真实服务来引导本地开发和测试依赖项，而 Testcontainers Cloud 则为这些容器提供了云运行时。这减少了对本地环境的资源压力，并提供了更好的可扩展性，特别是在 CI/CD 工作流中，能够在组织内实现一致的 Testcontainers 体验。

### 我可以在 Testcontainers Cloud 中运行哪些类型的容器？

Testcontainers Cloud 支持您通常与 Testcontainers 框架一起使用的任何容器，包括数据库（PostgreSQL、MySQL、MongoDB）、消息代理（Kafka、RabbitMQ）以及其他集成测试所需的服务。

### 使用 Testcontainers Cloud 是否需要更改现有测试代码？

不需要，您无需更改现有测试代码。Testcontainers Cloud 与开源 Testcontainers 框架无缝集成。一旦完成云配置，它会自动在云中管理容器，无需代码更改。

### 如何将 Testcontainers Cloud 集成到我的项目中？

要集成 Testcontainers Cloud，您需要安装 Testcontainers Desktop 应用程序，并在菜单中选择“使用 Testcontainers Cloud 运行”选项。在 CI 中，您需要添加一个工作流步骤来下载 Testcontainers Cloud 代理。除了通过 Testcontainers Desktop 应用程序在本地启用云运行时或在 CI 中安装 Testcontainers Cloud 代理外，无需其他代码更改。

### 我可以在 CI/CD 管道中使用 Testcontainers Cloud 吗？

可以，Testcontainers Cloud 专为在 CI/CD 管道中高效工作而设计。它通过将使用 Testcontainers 库启动的容器卸载到云端，帮助减少构建时间和资源瓶颈，非常适合持续测试环境。

### 使用 Testcontainers Cloud 有哪些优势？

主要优势包括减少本地机器和 CI 服务器的资源使用、提高可扩展性（运行更多容器而不会降低性能）、提供一致的测试环境、集中监控，以及简化 CI 配置，避免 Docker-in-Docker 或特权守护进程运行的安全隐患。

### Testcontainers Cloud 是否支持所有编程语言？

Testcontainers Cloud 支持任何与开源 Testcontainers 库兼容的语言，包括 Java、Python、Node.js、Go 等。只要您的项目使用 Testcontainers，就可以将其卸载到 Testcontainers Cloud。

### Testcontainers Cloud 如何处理容器清理？

虽然 Testcontainers 库会自动处理容器生命周期管理，但 Testcontainers Cloud 管理已分配的云工作节点的生命周期。这意味着容器由 Testcontainers 库在测试完成后启动、监控和清理，而运行这些容器的工作节点将在约 35 分钟空闲期后由 Testcontainers Cloud 自动移除。这种方法使开发人员无需手动管理容器和相关云资源。

### Testcontainers Cloud 是否提供免费套餐或定价模式？

Testcontainers Cloud 的定价详情请参阅 [定价页面](https://testcontainers.com/cloud/pricing/)。