---
title: 使用 Docker Compose 开发和部署 Laravel 应用
linkTitle: 使用 Docker Compose 进行 Laravel 应用开发
summary: 了解如何使用 Docker Compose 高效地设置 Laravel 开发和生产环境。
description: 本指南介绍如何使用 Docker Compose 管理 Laravel 应用的开发和生产环境，涵盖容器配置和服务管理。
tags: [frameworks]
languages: [php]
aliases:
  - /frameworks/laravel/
params:
  time: 30 分钟
  resource_links:
    - title: Laravel
      url: https://laravel.com/
    - title: Docker Compose
      url: /compose/
    - title: 在生产环境中使用 Compose
      url: /compose/how-tos/production/
    - title: 示例仓库
      url: https://github.com/dockersamples/laravel-docker-examples
---

Laravel 是一个流行的 PHP 框架，允许开发者快速高效地构建 Web 应用。Docker Compose 通过在单个 YAML 文件中定义必要的服务（如 PHP、Web 服务器和数据库）来简化开发和生产环境的管理。本指南提供了一种使用 Docker Compose 设置强大 Laravel 环境的简化方法，专注于简单性和高效性。

> **致谢**
>
> Docker 感谢 [Sergei Shitikov](https://github.com/rw4lll) 对本指南的贡献。

演示示例可以在 [这个 GitHub 仓库](https://github.com/dockersamples/laravel-docker-examples) 中找到。Docker Compose 为 Laravel 连接多个容器提供了简单的方法，尽管使用 Docker Swarm、Kubernetes 或独立 Docker 容器等工具也可以实现类似的设置。

本指南旨在用于教育目的，帮助开发者根据自己的特定用例调整和优化配置。此外，还有一些现有工具支持在容器中运行 Laravel：

- [Laravel Sail](https://laravel.com/docs/12.x/sail)：一个官方包，用于轻松在 Docker 中启动 Laravel。
- [Laradock](https://github.com/laradock/laradock)：一个社区项目，帮助在 Docker 中运行 Laravel 应用。

## 你将学到什么

- 如何使用 Docker Compose 设置 Laravel 开发和生产环境。
- 定义使 Laravel 开发更轻松的服务，包括 PHP-FPM、Nginx 和数据库容器。
- 使用容器化管理 Laravel 环境的最佳实践。

## 这适合谁？

- 使用 Laravel 并希望简化环境管理的开发者。
- 寻求高效管理与部署 Laravel 应用的 DevOps 工程师。