---
title: React.js 语言特定指南
linkTitle: React.js
description: 使用 Docker 容器化并开发 React.js 应用
keywords: 入门, React.js, react.js, docker, 语言, Dockerfile
summary: |
  本指南介绍如何使用 Docker 容器化 React.js 应用，遵循创建高效、生产就绪容器的最佳实践。
toc_min: 1
toc_max: 2
languages: [js]
params:
  time: 20 分钟

---

React.js 语言特定指南向您展示如何使用 Docker 容器化 React.js 应用，并遵循创建高效、生产就绪容器的最佳实践。

[React.js](https://react.dev/) 是一个广泛使用的库，用于构建交互式用户界面。然而，高效地管理依赖项、环境和部署可能很复杂。Docker 通过提供一致且容器化的环境来简化此过程。

> 
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 致以诚挚的感谢，感谢他编写了本指南。作为 Docker Captain 和经验丰富的前端工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源对社区来说弥足珍贵，帮助开发者驾驭并优化其 Docker 工作流。

---

## 您将学到什么？

在本指南中，您将学习如何：

- 使用 Docker 容器化并运行 React.js 应用。
- 在容器内为 React.js 设置本地开发环境。
- 在 Docker 容器内运行 React.js 应用的测试。
- 为您的容器化应用配置使用 GitHub Actions 的 CI/CD 管道。
- 将容器化的 React.js 应用部署到本地 Kubernetes 集群以进行测试和调试。

开始之前，您将先从容器化一个现有的 React.js 应用开始。

---

## 前提条件

在开始之前，请确保您熟悉以下内容：

- 对 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 或 [TypeScript](https://www.typescriptlang.org/) 的基本理解。
- 对 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 的基本知识，用于管理依赖项和运行脚本。
- 熟悉 [React.js](https://react.dev/) 基础知识。
- 了解 Docker 概念，如镜像、容器和 Dockerfile。如果您是 Docker 新手，请先从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 React.js 入门模块后，您就可以使用本指南中提供的示例和说明来容器化自己的 React.js 应用。

---