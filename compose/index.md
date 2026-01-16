---
title: Docker Compose
url: /compose/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Compose
    url: /compose/
children:
  - title: Docker Compose 安装概述
    url: /compose/install/
    description: 了解如何安装 Docker Compose。Compose 可原生用于 Docker Desktop，也可作为 Docker Engine 插件或独立工具使用。
  - title: Docker Compose 快速入门
    url: /compose/gettingstarted/
    description: 通过这个动手教程，学习如何使用 Docker Compose，从定义应用依赖到尝试各种命令。
  - title: Compose Bridge 概述
    url: /compose/bridge/
    description: 了解 Compose Bridge 如何将 Docker Compose 文件转换为 Kubernetes 清单，以实现无缝的平台迁移
  - title: 使用 Compose SDK
    url: /compose/compose-sdk/
    description: 使用 Compose SDK 将 Docker Compose 直接集成到您的应用程序中。
  - title: 发布说明
    url: /compose/release-notes/
---


Docker Compose 是一款用于定义和运行多容器应用的工具。
它是实现流畅高效开发与部署体验的关键。

Compose 简化了对整个应用栈的控制，让您能够通过单个 YAML 配置文件轻松管理服务、网络和卷。然后，只需一个命令，即可从您的配置文件中创建并启动所有服务。

Compose 适用于所有环境——生产、预发布、开发、测试以及 CI 工作流。它还提供了用于管理应用整个生命周期的命令：

 - 启动、停止和重建服务
 - 查看正在运行的服务的状态
 - 流式传输正在运行的服务的日志输出
 - 在服务上运行一次性命令


