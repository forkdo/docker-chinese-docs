---
title: Node.js 语言专属指南
linkTitle: Node.js
description: 使用 Docker 容器化并开发 Node.js 应用
keywords: getting started, node, node.js
summary: '本指南介绍如何使用 Docker 容器化 Node.js 应用程序。

  '
toc_min: 1
toc_max: 2
aliases:
- /language/nodejs/
- /guides/language/nodejs/
languages:
- js
tags: []
params:
  time: 20 minutes
---

[Node.js](https://nodejs.org/en) 是一个用于构建 Web 应用程序的 JavaScript 运行时。本指南将展示如何容器化一个包含 React 前端和 PostgreSQL 数据库的 TypeScript Node.js 应用程序。

该示例应用程序是一个现代化的全栈 Todo 应用，包含：

- **后端**：使用 TypeScript 的 Express.js、PostgreSQL 数据库和 RESTful API
- **前端**：使用 Vite 和 Tailwind CSS 4 的 React.js


> **致谢**
>
> Docker 向 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 表示诚挚的感谢，感谢他编写本指南。作为 Docker Captain 和经验丰富的全栈工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源对社区具有无价的价值，帮助开发者优化其 Docker 工作流程。

---

## 你将学到什么？

在本指南中，你将学习如何：

- 使用 Docker 容器化并运行 Node.js 应用程序。
- 在 Docker 容器中运行测试。
- 设置开发容器环境。
- 配置 GitHub Actions 以实现基于 Docker 的 CI/CD。
- 将容器化的 Node.js 应用部署到 Kubernetes。

首先，你将从容器化一个现有的 Node.js 应用程序开始。

---

## 前提条件

在开始之前，请确保你熟悉以下内容：

- 基本了解 [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 和 [TypeScript](https://www.typescriptlang.org/)。
- 具备 [Node.js](https://nodejs.org/en)、[npm](https://docs.npmjs.com/about-npm) 和 [React](https://react.dev/) 的基础知识，用于现代 Web 开发。
- 理解 Docker 的核心概念，如镜像、容器和 Dockerfile。如果你是 Docker 新手，请从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。
- 熟悉用于后端 API 开发的 [Express.js](https://expressjs.com/)。

完成 Node.js 入门模块后，你就可以使用本指南提供的示例和说明来容器化你自己的 Node.js 应用程序了。