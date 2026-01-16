---
title: Python 语言专属指南
url: /guides/python/
parent:
  title: Docker 指南
  url: /guides/
breadcrumbs:
  - title: Docker 指南
    url: /guides/
  - title: Python 语言专属指南
    url: /guides/python/
children:
  - title: 容器化 Python 应用程序
    url: /guides/python/containerize/
    description: 学习如何将 Python 应用程序容器化。
  - title: 使用容器进行 Python 开发
    url: /guides/python/develop/
    description: 了解如何在本地开发 Python 应用程序。
  - title: Python 的代码检查、格式化与类型检查
    url: /guides/python/lint-format-typing/
    description: 了解如何为您的 Python 应用程序设置代码检查、格式化和类型检查。
  - title: 使用 GitHub Actions 自动化构建
    url: /guides/python/configure-github-actions/
    description: 了解如何为 Python 应用程序配置基于 GitHub Actions 的 CI/CD。
  - title: 测试您的 Python 部署
    url: /guides/python/deploy/
    description: 学习如何使用 Kubernetes 进行本地开发
---


> **致谢**
>
> 本指南是社区贡献。Docker 感谢
> [Esteban Maya](https://www.linkedin.com/in/esteban-x64/) 和 [Igor Aleksandrov](https://www.linkedin.com/in/igor-aleksandrov/) 对本指南的贡献。

Python 语言专属指南将教你如何使用 Docker 容器化一个 Python 应用。在本指南中，你将学习如何：

- 容器化并运行一个 Python 应用
- 设置本地环境，使用容器来开发 Python 应用
- 代码检查、格式化、类型提示与最佳实践
- 使用 GitHub Actions 为容器化的 Python 应用配置 CI/CD 流水线
- 将你容器化的 Python 应用本地部署到 Kubernetes，以测试和调试你的部署

从容器化一个现有的 Python 应用开始。
