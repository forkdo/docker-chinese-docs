# Vue.js 语言专用指南

Vue.js 语言专用指南向您展示如何使用 Docker 容器化 Vue.js 应用程序，遵循创建高效、生产就绪容器的最佳实践。

[Vue.js](https://vuejs.org/) 是一个渐进式且灵活的框架，用于构建现代交互式 Web 应用程序。然而，随着应用程序规模的扩大，管理依赖项、环境和部署可能会变得复杂。Docker 通过为开发和生产提供一致、隔离的环境来简化这些挑战。

> 
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 致以诚挚的谢意，感谢他撰写本指南。作为一名 Docker Captain 和经验丰富的前端工程师，Kristiyan 在现代 Web 开发、Docker 和 DevOps 方面拥有卓越的专业知识。他的实践方法和清晰、可操作的指导使本指南成为开发人员使用 Docker 构建、优化和保护 Vue.js 应用程序的重要资源。
---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 Vue.js 应用程序。
- 在容器内为 Vue.js 设置本地开发环境。
- 在 Docker 容器中运行 Vue.js 应用程序的测试。
- 使用 GitHub Actions 为您的容器化应用程序配置 CI/CD 流水线。
- 将容器化的 Vue.js 应用程序部署到本地 Kubernetes 集群以进行测试和调试。

您将从容器化现有的 Vue.js 应用程序开始，逐步实现生产级部署。

---

## 先决条件

在开始之前，请确保您具备以下知识：

- 对 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/) 有基本的了解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm)，用于管理依赖项和运行脚本。
- 熟悉 [Vue.js](https://vuejs.org/) 基础知识。
- 了解 Docker 核心概念，例如镜像、容器和 Dockerfile。如果您是 Docker 新手，请从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Vue.js 入门模块后，您将完全准备好使用本指南中详细介绍的示例和最佳实践来容器化您自己的 Vue.js 应用程序。

- [容器化 Vue.js 应用程序](https://docs.docker.com/guides/vuejs/containerize/)

- [使用容器进行 Vue.js 开发](https://docs.docker.com/guides/vuejs/develop/)

- [在容器中运行 Vue.js 测试](https://docs.docker.com/guides/vuejs/run-tests/)

- [使用 GitHub Actions 自动化构建](https://docs.docker.com/guides/vuejs/configure-github-actions/)

- [测试 Vue.js 部署](https://docs.docker.com/guides/vuejs/deploy/)

