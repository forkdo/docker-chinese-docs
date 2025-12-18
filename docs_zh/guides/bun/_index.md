---
description: 使用 Docker 容器化并开发 Bun 应用程序。
keywords: 入门，bun
title: Bun 语言特定指南
summary: |
  了解如何使用 Docker 容器化 JavaScript 应用程序（Bun 运行时）。
linkTitle: Bun
languages: [js]
tags: []
params:
  time: 10 分钟
---

Bun 入门指南将教您如何使用 Docker 创建容器化的 Bun 应用程序。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 您将学到什么？

* 使用 Docker 容器化并运行 Bun 应用程序
* 使用容器设置本地开发环境来开发 Bun 应用程序
* 使用 GitHub Actions 为容器化的 Bun 应用程序配置 CI/CD 管道
* 将您的容器化应用程序本地部署到 Kubernetes 以测试和调试您的部署

## 先决条件

- 假设您具备 JavaScript 的基础知识。
- 您必须熟悉 Docker 的概念，如容器、镜像和 Dockerfile。如果您是 Docker 新手，可以从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Bun 入门模块后，您应该能够根据本指南中提供的示例和说明容器化您自己的 Bun 应用程序。

首先从容器化一个现有的 Bun 应用程序开始。