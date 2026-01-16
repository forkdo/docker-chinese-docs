---
title: Ruby on Rails 语言特定指南
url: /guides/ruby/
parent:
  title: Docker 指南
  url: /guides/
breadcrumbs:
  - title: Docker 指南
    url: /guides/
  - title: Ruby on Rails 语言特定指南
    url: /guides/ruby/
children:
  - title: 容器化 Ruby on Rails 应用程序
    url: /guides/ruby/containerize/
    description: 了解如何容器化 Ruby on Rails 应用程序。
  - title: 使用 GitHub Actions 自动化构建
    url: /guides/ruby/configure-github-actions/
    description: 了解如何为 Ruby on Rails 应用程序配置使用 GitHub Actions 的 CI/CD 流程。
  - title: 使用容器进行 Ruby on Rails 开发
    url: /guides/ruby/develop/
    description: 学习如何在本地开发你的 Ruby on Rails 应用程序。
  - title: 测试您的 Ruby on Rails 部署
    url: /guides/ruby/deploy/
    description: 了解如何使用 Kubernetes 进行本地开发
---


Ruby 语言特定指南将教你如何使用 Docker 容器化一个 Ruby on Rails 应用程序。在本指南中，你将学习如何：

- 容器化并运行一个 Ruby on Rails 应用程序
- 配置 GitHub Actions 工作流以构建 Docker 镜像并推送到 Docker Hub
- 设置一个使用容器来开发 Ruby on Rails 应用程序的本地环境
- 将容器化的 Ruby on Rails 应用程序部署到本地的 Kubernetes 上，以测试和调试你的部署

从容器化一个现有的 Ruby on Rails 应用程序开始。
