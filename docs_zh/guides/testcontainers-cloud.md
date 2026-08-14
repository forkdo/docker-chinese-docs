---
title: |
  Mastering Testcontainers Cloud by Docker：通过容器简化集成测试
linkTitle: Testcontainers Cloud by Docker
summary: |
  使用 Testcontainers Cloud 自动化、扩展并优化测试工作流
description: |
  Docker 的 Testcontainers Cloud 通过将容器管理转移到云端来简化集成测试。它能为数据库等容器化服务提供更快、更一致的测试，提升 CI/CD 流水线的性能与可扩展性，而不会给本地或 CI 资源带来压力。非常适合需要高效、可靠测试环境的开发者。
keywords: testcontainers cloud, integration testing, ci/cd, containerized tests, cloud testing, scalable testing
aliases:
  - /guides/testcontainers-cloud/common-questions/
  - /guides/testcontainers-cloud/demo-ci/
  - /guides/testcontainers-cloud/demo-local/
  - /guides/testcontainers-cloud/why/
params:
  tags: [testing]
  image: images/learning-paths/testcontainers-cloud-learning-path.png
  time: 12 minutes
---


Testcontainers Cloud 是一项基于云的解决方案，旨在简化并增强使用 Testcontainers 运行集成测试的过程。Testcontainers 是一个开源框架，允许开发者轻松启动容器化的依赖项，例如数据库、消息代理以及其他测试所需的服务。通过将基于 Testcontainers 的服务管理转移到云端，Testcontainers Cloud 优化了性能，减少了本地机器或 CI 服务器的资源限制，并确保一致的测试环境。该解决方案对于构建复杂分布式系统的团队尤为有益，因为它无需承担本地管理容器的典型开销即可实现可扩展、隔离且可靠的测试。

## 你将学到什么

- 理解 Docker Testcontainers Cloud 的基础知识及其在集成测试中的作用。
- 学习如何为各种环境中的自动化测试设置并配置 Docker Testcontainers Cloud。
- 探索 Testcontainers Cloud 如何与 CI/CD 流水线集成以简化测试工作流。

## 工具集成

与 Docker Desktop、GitHub Actions、Jenkins、Kubernetes 以及其他 CI 解决方案良好配合

Docker Pro、Team 和 Business 订阅包含 Testcontainers Cloud 运行时分钟数，额外分钟数可通过按量计费获取。Testcontainers Cloud 运行时分钟数不会逐月结转。

## 这适合谁？

- 构建云原生应用、且已经在使用 Testcontainers 开源框架的团队。
- 将基于容器的自动化测试集成到 CI/CD 流水线中以实现持续测试的 DevOps 团队。
- 寻求可扩展、一致测试环境以进行全面集成和端到端测试的 QA 团队。
- 需要可靠的容器化测试环境来测试微服务和数据库的开发者。

## 为什么选择 Testcontainers Cloud？

{{< youtube-embed "6dRRlk5Vd0E" >}}

Testcontainers Cloud 是一项强大的基于云的解决方案，旨在通过将其容器管理转移到云端来优化使用 Testcontainers 的集成测试。它帮助开发者和团队克服传统本地及基于 CI 的测试的局限，确保一致的环境、更快的测试执行以及可扩展的工作流。无论你是 Testcontainers 的新手，还是希望增强现有设置，Testcontainers Cloud 都提供了一种无缝管理容器化测试的方式，从而提升开发流水线的效率与可靠性。

Testcontainers Cloud 提供了以下多项优势：

- **卸载到云端：** 通过将容器管理转移到云端释放本地资源，让你的笔记本保持响应迅速。
- **一致的测试环境：** 确保测试在隔离、可靠的环境中运行，减少从开发到 CI 各平台间的不一致。
- **可扩展性：** 允许同时运行大量容器，而不受本地或 CI 资源的限制。
- **更快的 CI/CD 流水线：** 借助 Turbo 模式特性，将容器卸载到多个按需云工作节点，减少配置瓶颈并加快构建速度。

Testcontainers Cloud 通过将容器管理卸载到云端来简化集成测试，确保一致的环境和更快的测试执行，从而减轻资源压力，是提升基于 Testcontainers 工作流稳定性的必备工具。

## 设置 Docker Testcontainers Cloud

{{< youtube-embed "7c3xLAG560U" >}}

本演示展示了如何使用 Testcontainers Desktop 应用在本地开发环境中设置 Docker Testcontainers Cloud。
完成本演练后，你将使 Docker Testcontainers Cloud 启动并运行，准备好将容器管理从本地机器卸载到云端，从而实现更高效的测试。

- 安装并配置 Testcontainers Cloud 和 CLI，使其与你的本地开发环境无缝集成。
- 设置并配置 Testcontainers Desktop 应用，以在本地测试期间监控和管理基于云的容器。
- 使用 Testcontainers 创建并运行利用基于云的容器资源的集成测试。
- 高效监控和管理容器，理解 Testcontainers Cloud 如何自动清理并确保一致的测试环境。
- 查看 Testcontainers Cloud Dashboard 中用于监控和故障排查的选项。

## 在 CI 流水线中配置 Testcontainers Cloud

{{< youtube-embed "NlZY9aumKJU" >}}

本演示展示了如何使用 GitHub Workflows 将 Testcontainers Cloud 无缝集成到持续集成（CI）流水线中，提供了一种无需压垮本地或 CI 运行器资源即可运行容器化集成测试的强大方案。通过利用 GitHub Actions，开发者可以自动化在云中启动和管理用于测试的容器的过程，确保更快、更可靠的测试执行。只需几个配置步骤，包括设置 Testcontainers Cloud 身份验证并将其添加到你的工作流中，你就可以将容器编排卸载到云端。这种方法提升了流水线的可扩展性，确保测试间的一致性，并简化了资源管理，是现代容器化开发工作流的理想方案。

- 理解如何设置 GitHub Actions 工作流以自动化项目的构建和测试。
- 学习如何在 GitHub Actions 中配置 Testcontainers Cloud，将容器化测试卸载到云端，从而提升效率和资源管理。
- 探索 Testcontainers Cloud 如何与 GitHub 工作流集成，运行需要容器化服务（如数据库和消息代理）的集成测试。

## 常见挑战与问题

<!-- vale Docker.HeadingLength = NO -->

#### Testcontainers Cloud 与开源 Testcontainers 框架有何不同？

开源 Testcontainers 是一个库，提供轻量级的 API，用于通过包裹在 Docker 容器中的真实服务来引导本地开发和测试依赖；而 Testcontainers Cloud 为这些容器提供云端运行时。这减轻了本地环境的资源压力，并提供了更强的可扩展性，尤其在 CI/CD 工作流中，使整个组织获得一致的 Testcontainers 体验。

#### 我可以使用 Testcontainers Cloud 运行哪些类型的容器？

Testcontainers Cloud 支持你通常会与 Testcontainers 框架一起使用的任何容器，包括数据库（PostgreSQL、MySQL、MongoDB）、消息代理（Kafka、RabbitMQ），以及其他集成测试所需的服务。

#### 我是否需要更改现有的测试代码才能使用 Testcontainers Cloud？

不需要，你无需更改现有的测试代码。Testcontainers Cloud 与开源 Testcontainers 框架无缝集成。一旦设置了云配置，它会自动在云端管理容器，无需更改代码。

#### 如何将 Testcontainers Cloud 集成到我的项目中？

要集成 Testcontainers Cloud，你需要安装 Testcontainers Desktop 应用，并在菜单中选择“使用 Testcontainers Cloud 运行”选项。在 CI 中，你需要添加一个下载 Testcontainers Cloud agent 的工作流步骤。除了在本地通过 Testcontainers Desktop 应用启用 Cloud 运行时，或在 CI 中安装 Testcontainers Cloud agent 之外，无需更改代码。

#### 我可以在 CI/CD 流水线中使用 Testcontainers Cloud 吗？

可以，Testcontainers Cloud 被设计用于高效运行在 CI/CD 流水线中。它通过将你用 Testcontainers 库启动的容器卸载到云端来减少构建时间和资源瓶颈，是持续测试环境的绝佳选择。

#### 使用 Testcontainers Cloud 有哪些好处？

主要好处包括：减少本地机器和 CI 服务器的资源使用、可扩展性（在不降低性能的情况下运行更多容器）、一致的测试环境、集中监控，以及免除了运行 Docker-in-Docker 或特权守护进程的安全顾虑的简易 CI 配置。

#### Testcontainers Cloud 是否支持所有编程语言？

Testcontainers Cloud 支持任何可与开源 Testcontainers 库配合使用的语言，包括 Java、Python、Node.js、Go 等。只要你的项目使用了 Testcontainers，就可以将其卸载到 Testcontainers Cloud。

#### Testcontainers Cloud 中如何处理容器清理？

Testcontainers 库会自动处理容器生命周期管理，而 Testcontainers Cloud 管理已分配的云工作节点的生命周期。这意味着容器由 Testcontainers 库在测试完成后启动、监控并清理，而这些容器运行的的工作节点会在约 35 分钟空闲期后由 Testcontainers Cloud 自动移除。这种方式使开发者免于手动管理容器及相关的云资源。

#### Testcontainers Cloud 有免费套餐或定价模式吗？

Testcontainers Cloud 的定价详情可在 [定价页面](https://testcontainers.com/cloud/pricing/) 找到。
