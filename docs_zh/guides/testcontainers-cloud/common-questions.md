---
title: 常见挑战与问题
description: 探索与 Docker Testcontainers Cloud 相关的常见挑战与问题。
weight: 40
---

<!-- vale Docker.HeadingLength = NO -->

### Testcontainers Cloud 与开源 Testcontainers 框架有何不同？

开源 Testcontainers 是一个库，它提供了轻量级的 API，用于通过 Docker 容器来引导本地开发和测试所需的依赖项（这些依赖项被真实的服务所包裹）。而 Testcontainers Cloud 则为这些容器提供了一个云运行时环境。这减轻了本地环境的资源压力，并提供了更强的可扩展性，尤其是在 CI/CD 工作流中，从而在整个组织内实现一致的 Testcontainers 体验。

### 我可以使用 Testcontainers Cloud 运行哪些类型的容器？

Testcontainers Cloud 支持您通常会与 Testcontainers 框架一起使用的任何容器，包括数据库（PostgreSQL、MySQL、MongoDB）、消息代理（Kafka、RabbitMQ）以及集成测试所需的其他服务。

### 我需要修改现有的测试代码才能使用 Testcontainers Cloud 吗？

不需要，您无需修改现有的测试代码。Testcontainers Cloud 与开源 Testcontainers 框架无缝集成。一旦云配置设置完成，它会自动在云端管理容器，无需更改代码。

### 如何将 Testcontainers Cloud 集成到我的项目中？

要集成 Testcontainers Cloud，您需要安装 Testcontainers Desktop 应用，并在菜单中选择使用 Testcontainers Cloud 运行的选项。在 CI 中，您需要添加一个下载 Testcontainers Cloud 代理的工作流步骤。除了在本地通过 Testcontainers Desktop 应用启用云运行时或在 CI 中安装 Testcontainers Cloud 代理外，无需进行任何代码更改。

### 我可以在 CI/CD 流水线中使用 Testcontainers Cloud 吗？

是的，Testcontainers Cloud 旨在高效地在 CI/CD 流水线中工作。它通过将您使用 Testcontainers 库启动的容器卸载到云端，从而帮助减少构建时间和资源瓶颈，是持续测试环境的完美选择。

### 使用 Testcontainers Cloud 有哪些好处？

主要好处包括：减少本地机器和 CI 服务器的资源使用；可扩展性（无需性能下降即可运行更多容器）；一致的测试环境；集中监控；简化的 CI 配置，并消除了在 Docker-in-Docker 或特权守护进程中运行的安全顾虑。

### Testcontainers Cloud 支持所有编程语言吗？

Testcontainers Cloud 支持任何可与开源 Testcontainers 库协同工作的语言，包括 Java、Python、Node.js、Go 等。只要您的项目使用 Testcontainers，就可以将其卸载到 Testcontainers Cloud。

### Testcontainers Cloud 如何处理容器清理？

Testcontainers 库会自动处理容器的生命周期管理，而 Testcontainers Cloud 则管理所分配的云工作节点的生命周期。这意味着容器由 Testcontainers 库负责启动、监控并在测试完成后进行清理，而这些容器所在的工作节点则会在大约 35 分钟闲置后由 Testcontainers Cloud 自动移除。这种方法让开发者无需手动管理容器和相关的云资源。

### Testcontainers Cloud 是否有免费套餐或定价模式？

Testcontainers Cloud 的定价详情可在[定价页面](https://testcontainers.com/cloud/pricing/)找到。