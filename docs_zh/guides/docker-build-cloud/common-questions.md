---
title: 常见挑战与问题
description: 探索与 Docker Build Cloud 相关的常见挑战与问题。
weight: 40
---

### Docker Build Cloud 是独立产品还是 Docker Desktop 的一部分？

Docker Build Cloud 是一项服务，既可与 Docker Desktop 搭配使用，也可独立使用。它能让你在本地和 CI 中更快地构建容器镜像，构建任务在云基础设施上运行。该服务使用远程构建缓存，确保无论何时何地、所有团队成员都能快速构建。

当与 Docker Desktop 一起使用时，[构建视图](/desktop/use-desktop/builds/) 与 Docker Build Cloud 开箱即用。它会显示有关您的构建以及由使用同一构建器的团队成员发起的构建的信息，从而实现协作故障排除。

要在没有 Docker Build Cloud 的情况下使用 Docker Desktop，您必须[下载并安装](/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop) 支持 Docker Build Cloud（`cloud` 驱动程序）的 Buildx 版本。如果您计划使用 `docker compose build` 命令通过 Docker Build Cloud 进行构建，您还需要一个支持 Docker Build Cloud 的 Docker Compose 版本。

### Docker Build Cloud 如何与 Docker Compose 协同工作？

Docker Compose 与 Docker Build Cloud 开箱即用。安装兼容 Docker Build Cloud 的客户端 (buildx)，它即可与这两个命令协同工作。

### Docker Build Cloud Team 计划包含多少分钟？

Docker Build Cloud 的定价详情可在[定价页面](https://www.docker.com/pricing/)找到。

### 我是 Docker 个人用户。可以试用 Docker Build Cloud 吗？

Docker 订阅用户（Pro、Team、Business）每月会获得一定数量的分钟数，在账户内共享，用于使用 Build Cloud。

如果您没有 Docker 订阅，可以注册一个免费的个人账户并开始试用 Docker Build Cloud。个人账户仅限单个用户使用。

为了让团队获得共享缓存的优势，他们必须使用 Docker Team 或 Docker Business 订阅。

### Docker Build Cloud 支持 CI 平台吗？它能与 GitHub Actions 一起使用吗？

是的，Docker Build Cloud 可与各种 CI 平台一起使用，包括 GitHub Actions、CircleCI、Jenkins 等。它可以加快您的构建管道，这意味着减少等待时间和上下文切换。

Docker Build Cloud 可与 GitHub Actions 一起使用，以自动化您的构建、测试和部署管道。Docker 提供了一套官方的 GitHub Actions，您可以在工作流中使用。

将 GitHub Actions 与 Docker Build Cloud 一起使用非常简单。只需在您的 GitHub Actions 配置中进行一行更改，其余一切保持不变。您无需创建新的管道。在 Docker Build Cloud 的 [CI 文档](/build-cloud/ci/) 中了解更多信息。

<div id="dbc-lp-survey-anchor"></div>