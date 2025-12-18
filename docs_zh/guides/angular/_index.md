---
title: Angular 语言特定指南
linkTitle: Angular
description: 使用 Docker 容器化并开发 Angular 应用
keywords: 入门, angular, docker, 语言, Dockerfile
summary: |
  本指南介绍如何使用 Docker 容器化 Angular 应用，遵循创建高效、生产就绪容器的最佳实践。
toc_min: 1
toc_max: 2
languages: [js]
params:
  time: 20 分钟

---

Angular 语言特定指南向您展示如何使用 Docker 容器化 Angular 应用，并遵循创建高效、生产就绪容器的最佳实践。

[Angular](https://angular.dev/) 是一个强大且被广泛采用的框架，用于构建动态、企业级的 Web 应用。然而，随着应用规模的扩大，管理依赖、环境和部署可能变得复杂。Docker 通过提供一致且隔离的开发和生产环境，简化了这些挑战。

> 
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 致以诚挚的感谢，感谢他撰写了本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源成为社区的必备指南，帮助开发者导航并优化其 Docker 工作流。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 Angular 应用。
- 在容器内设置 Angular 的本地开发环境。
- 在 Docker 容器内运行 Angular 应用的测试。
- 使用 GitHub Actions 为您的容器化应用配置 CI/CD 管道。
- 将容器化的 Angular 应用部署到本地 Kubernetes 集群进行测试和调试。

您将从容器化现有的 Angular 应用开始，逐步掌握生产级部署。

---

## 先决条件

在开始之前，请确保您具备以下基础知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 的基本理解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 以管理依赖和运行脚本。
- 熟悉 [Angular](https://angular.io/) 基础知识。
- 了解 Docker 的核心概念，如镜像、容器和 Dockerfile。如果您是 Docker 新手，请先阅读 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南。

完成 Angular 入门模块后，您将完全准备好使用本指南中详述的详细示例和最佳实践来容器化您自己的 Angular 应用。