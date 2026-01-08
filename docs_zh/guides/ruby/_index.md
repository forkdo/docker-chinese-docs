---
title: Ruby on Rails 语言特定指南
linkTitle: Ruby
description: 使用 Docker 容器化 Ruby on Rails 应用
keywords: Docker, getting started, ruby, language
summary: '本指南介绍了如何使用 Docker 容器化 Ruby on Rails 应用程序。

  '
toc_min: 1
toc_max: 2
aliases:
- /language/ruby/
- /guides/language/ruby/
languages:
- ruby
tags:
- frameworks
params:
  time: 20 分钟
---

Ruby 语言特定指南将教你如何使用 Docker 容器化一个 Ruby on Rails 应用程序。在本指南中，你将学习如何：

- 容器化并运行一个 Ruby on Rails 应用程序
- 配置 GitHub Actions 工作流以构建 Docker 镜像并推送到 Docker Hub
- 设置一个使用容器来开发 Ruby on Rails 应用程序的本地环境
- 将容器化的 Ruby on Rails 应用程序部署到本地的 Kubernetes 上，以测试和调试你的部署

从容器化一个现有的 Ruby on Rails 应用程序开始。