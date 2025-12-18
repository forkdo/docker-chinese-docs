---
title: Ruby on Rails 语言特定指南
linkTitle: Ruby
description: 使用 Docker 容器化 Ruby on Rails 应用
keywords: Docker, 入门, ruby, 语言
summary: |
  本指南介绍如何使用 Docker 容器化 Ruby on Rails 应用。
toc_min: 1
toc_max: 2
aliases:
  - /language/ruby/
  - /guides/language/ruby/
languages: [ruby]
tags: [frameworks]
params:
  time: 20 分钟
---

Ruby 语言特定指南将教你如何使用 Docker 容器化 Ruby on Rails 应用。通过本指南，你将学会：

- 容器化并运行 Ruby on Rails 应用
- 配置 GitHub Actions 工作流以构建并推送 Docker 镜像到 Docker Hub
- 设置本地环境，使用容器开发 Ruby on Rails 应用
- 将容器化的 Ruby on Rails 应用本地部署到 Kubernetes，以测试和调试你的部署

首先，让我们容器化一个现有的 Ruby on Rails 应用。