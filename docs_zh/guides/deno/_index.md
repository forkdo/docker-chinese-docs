---
description: 使用 Docker 容器化和开发 Deno 应用程序。
keywords: 入门, deno
title: Deno 语言特定指南
linkTitle: Deno
languages: [js]
tags: []
params:
  time: 10 分钟
---

Deno 入门指南将教你如何使用 Docker 为 Deno 运行时创建容器化 JavaScript 应用程序。

> **致谢**
>
> Docker 感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 你将学到什么？

* 使用 Docker 容器化和运行 Deno 应用程序
* 使用容器设置本地环境以开发 Deno 应用程序
* 使用 Docker Compose 运行应用程序
* 使用 GitHub Actions 为容器化 Deno 应用程序配置 CI/CD 管道
* 将容器化应用程序本地部署到 Kubernetes 以测试和调试你的部署

## 前置条件

- 假设你具备 JavaScript 的基础知识。
- 你必须熟悉 Docker 概念，如容器、镜像和 Dockerfile。如果你是 Docker 新手，可以从 [Docker 基础知识](/get-started/docker-concepts/the-basics/what-is-a-container.md) 指南开始。

完成 Deno 入门模块后，你应该能够基于本指南中提供的示例和说明，将你自己的 Deno 应用程序容器化。

首先从容器化一个现有的 Deno 应用程序开始。