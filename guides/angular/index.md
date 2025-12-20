# Angular 语言专用指南

Angular 语言专用指南向您展示如何使用 Docker 容器化 Angular 应用程序，并遵循创建高效、生产就绪容器的最佳实践。

[Angular](https://angular.dev/) 是一个强大且广泛采用的框架，用于构建动态的企业级 Web 应用程序。然而，随着应用程序规模的扩大，管理依赖项、环境和部署可能会变得复杂。Docker 通过为开发和生产提供一致且隔离的环境，简化了这些挑战。

> 
> **致谢**
>
> Docker 衷心感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 撰写本指南。作为 Docker Captain 和经验丰富的全栈工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源成为社区的重要工具，帮助开发者优化其 Docker 工作流程。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 Angular 应用程序。
- 在容器内为 Angular 设置本地开发环境。
- 在 Docker 容器内运行 Angular 应用程序的测试。
- 使用 GitHub Actions 为容器化应用配置 CI/CD 流水线。
- 将容器化的 Angular 应用程序部署到本地 Kubernetes 集群进行测试和调试。

您将从容器化一个现有的 Angular 应用程序开始，逐步实现生产级部署。

---

## 先决条件

在开始之前，请确保您具备以下基础知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/) 的基本理解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm)，用于管理依赖项和运行脚本。
- 熟悉 [Angular](https://angular.io/) 基础知识。
- 理解 Docker 核心概念，例如镜像、容器和 Dockerfile。如果您是 Docker 新手，请从 [Docker 基础概念](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Angular 入门模块后，您将完全准备好使用本指南中详述的示例和最佳实践来容器化您自己的 Angular 应用程序。

- [容器化 Angular 应用程序](https://docs.docker.com/guides/angular/containerize/)

- [使用容器进行 Angular 开发](https://docs.docker.com/guides/angular/develop/)

- [在容器中运行 Angular 测试](https://docs.docker.com/guides/angular/run-tests/)

- [使用 GitHub Actions 自动化构建](https://docs.docker.com/guides/angular/configure-github-actions/)

- [测试你的 Angular 部署](https://docs.docker.com/guides/angular/deploy/)

