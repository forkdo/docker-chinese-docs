---
title: Bun 语言特定指南
url: /guides/bun/
parent:
  title: Docker 指南
  url: /guides/
breadcrumbs:
  - title: Docker 指南
    url: /guides/
  - title: Bun 语言特定指南
    url: /guides/bun/
children:
  - title: 容器化 Bun 应用程序
    url: /guides/bun/containerize/
    description: 了解如何容器化 Bun 应用程序。
  - title: 为 Bun 开发使用容器
    url: /guides/bun/develop/
    description: 了解如何在本地开发您的 Bun 应用程序。
  - title: 为你的 Bun 应用程序配置 CI/CD
    url: /guides/bun/configure-ci-cd/
    description: 学习如何使用 GitHub Actions 为你的 Bun 应用程序配置 CI/CD。
  - title: 测试你的 Bun 部署
    url: /guides/bun/deploy/
    description: 学习如何使用 Kubernetes 在本地进行开发
---


Bun 入门指南教你如何使用 Docker 创建容器化的 Bun 应用程序。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对此指南的贡献。

## 你将学到什么？

* 使用 Docker 容器化并运行 Bun 应用程序
* 搭建本地环境以使用容器开发 Bun 应用程序
* 使用 GitHub Actions 为容器化的 Bun 应用程序配置 CI/CD 流水线
* 将容器化应用程序本地部署到 Kubernetes 以测试和调试部署

## 先决条件

- 假定你已具备 JavaScript 基础知识。
- 你必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果你是 Docker 新手，可以从 [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始学习。

完成 Bun 入门模块后，你应该能够根据本指南提供的示例和说明，将你自己的 Bun 应用程序容器化。

首先，将一个现有的 Bun 应用程序容器化。
