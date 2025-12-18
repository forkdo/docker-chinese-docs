---
title: 常见挑战与问题
description: 探索与 Docker Build Cloud 相关的常见挑战和问题
weight: 40
---

### Docker Build Cloud 是独立产品还是 Docker Desktop 的一部分？

Docker Build Cloud 是一项服务，既可与 Docker Desktop 配合使用，也可独立使用。它通过在云基础设施上运行构建，帮助您在本地和 CI 环境中更快地构建容器镜像。该服务使用远程构建缓存，确保在任何地方、所有团队成员都能获得快速的构建体验。

与 Docker Desktop 配合使用时，[Builds 视图](/desktop/use-desktop/builds/) 开箱即用地支持 Docker Build Cloud。它显示您和团队成员使用同一构建器发起的构建信息，便于协作排查问题。

要在不使用 Docker Desktop 的情况下使用 Docker Build Cloud，您必须[下载并安装](/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop)支持 Docker Build Cloud 的 Buildx 版本（`cloud` 驱动）。如果您计划使用 `docker compose build` 命令构建，还需要支持 Docker Build Cloud 的 Docker Compose 版本。

### Docker Build Cloud 如何与 Docker Compose 配合使用？

Docker Compose 开箱即用地支持 Docker Build Cloud。安装 Docker Build Cloud 兼容客户端（buildx）后，两条命令均可正常工作。

### Docker Build Cloud 团队计划包含多少分钟？

Docker Build Cloud 的定价详情请见[定价页面](https://www.docker.com/pricing/)。

### 我是 Docker 个人用户。我可以试用 Docker Build Cloud 吗？

Docker 订阅用户（Pro、Team、Business）每月可获得一定数量的共享构建分钟数，用于使用 Build Cloud。

如果您没有 Docker 订阅，可以注册免费的个人账户并开始试用 Docker Build Cloud。个人账户仅限单个用户使用。

团队要享受共享缓存的优势，必须订阅 Docker Team 或 Docker Business。

### Docker Build Cloud 是否支持 CI 平台？是否支持 GitHub Actions？

是的，Docker Build Cloud 可与多种 CI 平台配合使用，包括 GitHub Actions、CircleCI、Jenkins 等。它可以加速您的构建流水线，减少等待和上下文切换的时间。

Docker Build Cloud 可与 GitHub Actions 配合使用，自动化您的构建、测试和部署流水线。Docker 提供了一套官方 GitHub Actions，您可以在工作流中使用。

将 GitHub Actions 与 Docker Build Cloud 配合使用非常简单。只需在 GitHub Actions 配置中修改一行代码，其余部分保持不变，无需创建新的流水线。更多详细信息请参阅 Docker Build Cloud 的 [CI 文档](/build-cloud/ci/)。

<div id="dbc-lp-survey-anchor"></div>