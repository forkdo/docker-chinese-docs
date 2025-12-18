---
title: R 语言特定指南
linkTitle: R
description: 使用 Docker 容器化 R 应用
keywords: Docker, 入门, R, 语言
summary: |
  本指南详细介绍如何使用 Docker 容器化 R 应用。
toc_min: 1
toc_max: 2
aliases:
  - /languages/r/
  - /guides/languages/r/
languages: [r]
params:
  time: 10 分钟
---

R 语言特定指南将教你如何使用 Docker 容器化 R 应用。在本指南中，你将学会：

- 容器化并运行一个 R 应用
- 使用容器设置本地开发环境来开发 R 应用
- 使用 GitHub Actions 为容器化的 R 应用配置 CI/CD 流水线
- 将你的容器化 R 应用本地部署到 Kubernetes，以测试和调试你的部署

首先从容器化一个现有的 R 应用开始。