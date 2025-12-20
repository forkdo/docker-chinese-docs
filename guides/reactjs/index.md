# React.js 语言特定指南

React.js 语言特定指南将向您展示如何使用 Docker 容器化 React.js 应用程序，并遵循创建高效、生产就绪容器的最佳实践。

[React.js](https://react.dev/) 是一个广泛用于构建交互式用户界面的库。然而，高效管理依赖项、环境和部署可能很复杂。Docker 通过提供一致的容器化环境简化了这一过程。

>
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 表示诚挚的感谢，感谢他编写了本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使该资源对社区来说非常宝贵，帮助开发人员导航并优化其 Docker 工作流程。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 React.js 应用程序。
- 在容器内为 React.js 设置本地开发环境。
- 在 Docker 容器内为您的 React.js 应用程序运行测试。
- 使用 GitHub Actions 为您的容器化应用配置 CI/CD 管道。
- 将容器化的 React.js 应用程序部署到本地 Kubernetes 集群以进行测试和调试。

首先，您将从容器化现有的 React.js 应用程序开始。

---

## 先决条件

在开始之前，请确保您熟悉以下内容：

- 基本了解 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 或 [TypeScript](https://www.typescriptlang.org/)。
- 基本了解 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm)，用于管理依赖项和运行脚本。
- 熟悉 [React.js](https://react.dev/) 基础知识。
- 了解 Docker 概念，例如镜像、容器和 Dockerfile。如果您是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 React.js 入门模块后，您就可以使用本指南中提供的示例和说明来容器化您自己的 React.js 应用程序了。

- [容器化 React.js 应用程序](/guides/reactjs/containerize/)

- [使用容器进行 React.js 开发](/guides/reactjs/develop/)

- [在容器中运行 React.js 测试](/guides/reactjs/run-tests/)

- [使用 GitHub Actions 自动化构建](/guides/reactjs/configure-github-actions/)

- [测试您的 React.js 部署](/guides/reactjs/deploy/)

