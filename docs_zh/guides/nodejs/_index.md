---
title: Node.js 语言专用指南
linkTitle: Node.js
description: 使用 Docker 容器化并开发 Node.js 应用
keywords: 入门, node, node.js
summary: |
  本指南介绍如何使用 Docker 容器化 Node.js 应用。
toc_min: 1
toc_max: 2
aliases:
  - /language/nodejs/
  - /guides/language/nodejs/
languages: [js]
tags: []
params:
  time: 20 分钟
---

[Node.js](https://nodejs.org/en) 是用于构建 Web 应用的 JavaScript 运行时。本指南将向您展示如何使用 Docker 容器化基于 TypeScript 的 Node.js 应用（包含 React 前端和 PostgreSQL 数据库）。

示例应用是一个现代全栈待办事项（Todo）应用，具有以下特性：

- **后端**：Express.js + TypeScript，PostgreSQL 数据库和 RESTful API
- **前端**：React.js + Vite 和 Tailwind CSS 4


> **致谢**
>
> Docker 衷心感谢 [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) 编写本指南。作为 Docker Captain 和经验丰富的全栈工程师，他在 Docker、DevOps 和现代 Web 开发方面的专业知识使本资源对社区极具价值，帮助开发者驾驭并优化其 Docker 工作流。

---

## 您将学到什么？

在本指南中，您将学会如何：

- 使用 Docker 容器化并运行 Node.js 应用。
- 在 Docker 容器内运行测试。
- 设置开发容器环境。
- 配置 GitHub Actions 实现 Docker 的 CI/CD。
- 将 Docker 化的 Node.js 应用部署到 Kubernetes。

开始时，您将先容器化一个现有的 Node.js 应用。

---

## 前置条件

开始之前，请确保您熟悉以下内容：

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) 和 [TypeScript](https://www.typescriptlang.org/) 的基础知识。
- [Node.js](https://nodejs.org/en)、[npm](https://docs.npmjs.com/about-npm) 和 [React](https://react.dev/) 的基本知识，用于现代 Web 开发。
- 了解 Docker 概念，如镜像、容器和 Dockerfile。如果您是 Docker 新手，请先阅读 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南。
- 熟悉 [Express.js](https://expressjs.com/) 用于后端 API 开发。

完成 Node.js 入门模块后，您就可以使用本指南提供的示例和说明来容器化自己的 Node.js 应用。

---