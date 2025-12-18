---
title: Go 语言特定指南
linkTitle: Go
description: 使用 Docker 容器化 Go 应用
keywords: docker, 入门, go, golang, 语言, dockerfile
summary: |
  本指南将教您如何使用 Docker 容器化 Go 应用程序。
toc_min: 1
toc_max: 2
aliases:
  - /language/golang/
  - /guides/language/golang/
languages: [go]
params:
  time: 30 分钟
---

本指南将向您展示如何使用 Docker 创建、测试和部署容器化的 Go 应用程序。

> **致谢**
>
> Docker 感谢 [Oliver Frolovs](https://www.linkedin.com/in/ofr/) 为本指南做出的贡献。

## 您将学到什么？

在本指南中，您将学会如何：

- 创建一个 `Dockerfile`，其中包含为 Go 程序构建容器镜像的指令。
- 在本地 Docker 实例中将镜像作为容器运行并管理容器的生命周期。
- 使用多阶段构建高效地构建小型镜像，同时保持 Dockerfile 易于阅读和维护。
- 使用 Docker Compose 在开发环境中协调运行多个相关容器。
- 使用 [GitHub Actions](https://docs.github.com/en/actions) 为您的应用配置 CI/CD 管道。
- 部署您的容器化 Go 应用。

## 先决条件

假设您对 Go 及其工具链有一些基本了解。本指南不是 Go 教程。如果您是 :languages: 新手，[Go 官网](https://golang.org/) 是一个很好的探索起点，
所以 _去_（双关）看看吧！

您还必须了解一些基本的 [Docker 概念](/get-started/docker-concepts/the-basics/what-is-a-container.md)，并至少对 [Dockerfile 格式](/manuals/build/concepts/dockerfile.md) 有基本了解。

您的 Docker 环境必须启用 BuildKit。Docker Desktop 用户默认已启用 BuildKit。如果您已安装 Docker Desktop，则无需手动启用 BuildKit。如果您在 Linux 上运行 Docker，
请查看 BuildKit [入门](/manuals/build/buildkit/_index.md#getting-started) 页面。

同时，您需要具备一些命令行的基础知识。

## 接下来做什么？

本指南的目标是提供足够的示例和说明，帮助您容器化自己的 Go 应用并将其部署到云端。

首先，构建您的第一个 Go 镜像。