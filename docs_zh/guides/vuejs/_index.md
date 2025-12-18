---
title: Vue.js 语言特定指南
linkTitle: Vue.js
description: 使用 Docker 容器化并开发 Vue.js 应用
keywords: 入门, vue, vuejs docker, 语言, Dockerfile
summary: |
  本指南说明如何使用 Docker 容器化 Vue.js 应用。
toc_min: 1
toc_max: 2
languages: [js]
tags: [frameworks]
aliases:
  - /frameworks/vue/
params:
  time: 20 分钟

---

Vue.js 语言特定指南展示了如何使用 Docker 容器化 Vue.js 应用，并遵循创建高效、生产就绪容器的最佳实践。

[Vue.js](https://vuejs.org/) 是一个渐进式且灵活的框架，用于构建现代、交互式 Web 应用。然而，随着应用规模扩大，管理依赖项、环境和部署可能变得复杂。Docker 通过为开发和生产提供一致、隔离的环境来简化这些挑战。

> 
> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 致以诚挚的感谢，感谢他撰写了本指南。作为 Docker Captain 和技术精湛的前端工程师，Kristiyan 在现代 Web 开发、Docker 和 DevOps 方面拥有卓越的专业知识。他注重实践的方法和清晰、可操作的指导使本指南成为开发者构建、优化和保护 Vue.js 应用的必备资源。
---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 Vue.js 应用。
- 在容器内为 Vue.js 设置本地开发环境。
- 在 Docker 容器内运行 Vue.js 应用的测试。
- 使用 GitHub Actions 为你的容器化应用配置 CI/CD 管道。
- 将容器化的 Vue.js 应用部署到本地 Kubernetes 集群进行测试和调试。

你将从容器化现有的 Vue.js 应用开始，逐步掌握生产级别的部署。

---

## 前置条件

开始之前，请确保你具备以下基础知识：

- 基本的 [TypeScript](https://www.typescriptlang.org/) 和 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 理解。
- 熟悉 [Node.js](https://nodejs.org/en) 和 [npm](https://docs.npmjs.com/about-npm) 用于管理依赖项和运行脚本。
- 熟悉 [Vue.js](https://vuejs.org/) 基础知识。
- 理解核心 Docker 概念，如镜像、容器和 Dockerfile。如果你是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Vue.js 入门模块后，你将完全准备好使用本指南中详述的示例和最佳实践来容器化你自己的 Vue.js 应用。