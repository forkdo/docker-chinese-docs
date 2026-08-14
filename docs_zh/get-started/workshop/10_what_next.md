---
title: Docker 工作坊之后该做什么
weight: 100
linkTitle: 第 9 部分：下一步
keywords: get started, setup, orientation, quickstart, intro, concepts, containers, docker desktop, AI, model runner, MCP, agents, hardened images, security
description: 探索完成 Docker 工作坊之后接下来要做的事情，包括加固您的镜像、AI 开发以及特定语言的指南。
aliases:
- /get-started/11_what_next/
- /guides/workshop/10_what_next/
summary: |
  既然您已经完成了 Docker 工作坊，您已经准备好探索使用 Docker Hardened Images 加固您的镜像、
  构建 AI 驱动的应用程序，以及深入了解特定语言的指南。
notoc: true
secure-images:
- title: 什么是 Docker Hardened Images？
  description: 了解安全的、最小的、生产就绪的基础镜像，具有近乎为零的 CVE。
  link: /dhi/explore/what/
- title: 开始使用 DHI
  description: 在几分钟内拉取并运行您的第一个 Docker Hardened Image。
  link: /dhi/get-started/
- title: 使用加固镜像
  description: 学习如何在您的 Dockerfile 和 CI/CD 流水线中使用 DHI。
  link: /dhi/how-to/use/
- title: 探索 DHI 目录
  description: 浏览可用的加固镜像、变体和安全证明。
  link: /dhi/how-to/explore/
ai-development:
- title: Docker Model Runner
  description: 使用熟悉的 Docker 命令和兼容 OpenAI 的 API 在本地运行和管理 AI 模型。
  link: /ai/model-runner/
- title: MCP Toolkit
  description: 设置、管理和运行容器化的 MCP 服务器，为您的 AI 代理提供动力。
  link: /ai/mcp-catalog-and-toolkit/toolkit/
- title: 使用 Docker Agent 构建 AI 代理
  description: 创建协作解决复杂问题的专业化 AI 代理团队。
  link: /ai/docker-agent/
- title: 在 Compose 中使用 AI 模型
  description: 在您的 Docker Compose 应用中定义 AI 模型依赖。
  link: /ai/compose/models-and-compose/
language-guides:
- title: Node.js
  description: 学习如何对 Node.js 应用程序进行容器化和开发。
  link: /guides/language/nodejs/
- title: Python
  description: 在容器中构建并运行 Python 应用程序。
  link: /guides/language/python/
- title: Java
  description: 使用最佳实践对 Java 应用程序进行容器化。
  link: /guides/language/java/
- title: Go
  description: 使用 Docker 开发和部署 Go 应用程序。
  link: /guides/language/golang/
---

恭喜您完成了 Docker 工作坊。您已经学习了如何对应用程序进行容器化、使用多容器设置、使用 Docker Compose，以及应用镜像构建最佳实践。

以下是接下来要探索的内容。

## 加固您的镜像

通过 Docker Hardened Images 将您的镜像构建技能提升到新的水平——这些安全、最小化且生产就绪的基础镜像现在对所有人免费。

{{< grid items="secure-images" >}}

## 使用 AI 进行构建

Docker 让在本地运行 AI 模型并构建智能体式 AI 应用程序变得轻松。探索 Docker 的 AI 工具并开始构建由 AI 驱动的应用程序。

{{< grid items="ai-development" >}}

## 特定语言指南

通过动手教程，将您学到的知识应用到您喜欢的编程语言上。

{{< grid items="language-guides" >}}
