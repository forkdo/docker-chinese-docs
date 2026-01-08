# 
title: Docker Compose
weight: 30
description: Learn how to use Docker Compose to define and run multi-container applications with this detailed introduction to the tool.
params:
  sidebar:
    group: Open source
grid:
  - title: Why use Compose?
    description: "Understand Docker Compose's key benefits"
    icon: feature_search
    link: /compose/intro/features-uses/
  - title: How Compose works
    description: Understand how Compose works
    icon: category
    link: /compose/intro/compose-application-model/
  - title: Install Compose
    description: Follow the instructions on how to install Docker Compose.
    icon: download
    link: /compose/install
  - title: Quickstart
    description: Learn the key concepts of Docker Compose whilst building a simple Python web application.
    icon: explore
    link: /compose/gettingstarted
  - title: View the release notes
    description: Find out about the latest enhancements and bug fixes.
    icon: note_add
    link: "https://github.com/docker/compose/releases"
  - title: Explore the Compose file reference
    description: "Find information on defining services, networks, and volumes for a Docker application."
    icon: polyline
    link: /reference/compose-file
  - title: Use Compose Bridge
    description: "Transform your Compose configuration file into configuration files for different platforms, such as Kubernetes."
    icon: move_down
    link: /compose/bridge
  - title: Browse common FAQs
    description: Explore general FAQs and find out how to give feedback.
    icon: help
    link: /compose/faq
keywords: "docker compose, docker-compose, compose.yaml, docker compose command, multi-container applications, container orchestration, docker cli"
aliases:
  - /compose/cli-command/
  - /compose/networking/swarm/
  - /compose/overview/
  - /compose/swarm/
  - /compose/completion/
  - /compose/releases/migrate/---
title: Docker Compose
weight: 30
description: 了解如何使用 Docker Compose 来定义和运行多容器应用，本文将详细介绍该工具。
params:
  sidebar:
    group: Open source
grid:
  - title: 为何使用 Compose？
    description: "了解 Docker Compose 的主要优势"
    icon: feature_search
    link: /compose/intro/features-uses/
  - title: Compose 的工作原理
    description: 了解 Compose 的工作原理
    icon: category
    link: /compose/intro/compose-application-model/
  - title: 安装 Compose
    description: 查看如何安装 Docker Compose 的说明。
    icon: download
    link: /compose/install
  - title: 快速入门
    description: 在构建一个简单的 Python Web 应用的同时，学习 Docker Compose 的核心概念。
    icon: explore
    link: /compose/gettingstarted
  - title: 查看发行说明
    description: 了解最新的功能增强和错误修复。
    icon: note_add
    link: "https://github.com/docker/compose/releases"
  - title: 浏览 Compose 文件参考
    description: "获取有关为 Docker 应用定义服务、网络和卷的信息。"
    icon: polyline
    link: /reference/compose-file
  - title: 使用 Compose Bridge
    description: "将您的 Compose 配置文件转换为不同平台（如 Kubernetes）的配置文件。"
    icon: move_down
    link: /compose/bridge
  - title: 浏览常见问题
    description: 探索常见问题并了解如何提供反馈。
    icon: help
    link: /compose/faq---
Docker Compose 是一款用于定义和运行多容器应用的工具。
它是开启流畅高效开发与部署体验的关键。

Compose 简化了对整个应用栈的控制，让您能够通过单个 YAML 配置文件轻松管理服务、网络和卷。然后，只需一条命令，即可根据配置文件创建并启动所有服务。

Compose 适用于所有环境——生产、预发布、开发、测试以及 CI 工作流。它还提供了用于管理应用整个生命周期的命令：

 - 启动、停止和重建服务
 - 查看正在运行的服务的状态
 - 流式传输正在运行的服务的日志输出
 - 在服务上运行一次性命令


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
</div>


- [Docker Compose 安装概述](/compose/install/)

- [Compose Bridge 概述](/compose/bridge/)

- [使用 Compose SDK](/compose/compose-sdk/)

- [](/compose/gettingstarted/)

- [](/compose/release-notes/)

