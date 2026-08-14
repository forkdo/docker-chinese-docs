---
title: "Docker Build Cloud：用快速的多架构构建夺回你的时间"
linkTitle: Docker Build Cloud
description: |
  了解如何使用 Docker Build
  Cloud 构建 Docker 镜像并部署到云端。
summary: |
  借助基于云的资源、团队共享
  缓存和原生多架构支持，把应用构建速度提升至多 39 倍。
keywords: docker build cloud, cloud builds, multi-architecture, shared cache, ci/cd, build performance
aliases:
  - /learning-paths/docker-build-cloud/
  - /guides/docker-build-cloud/ci/
  - /guides/docker-build-cloud/common-questions/
  - /guides/docker-build-cloud/dev/
  - /guides/docker-build-cloud/why/
params:
  tags: [cicd]
  image: images/learning-paths/build-cloud.png
  time: 10 minutes
---


<!-- vale Vale.Spelling = NO -->

98% 的开发者每天要花费多达一小时等待构建完成
（[Incredibuild：2022 Big Dev Build Times](https://www.incredibuild.com/survey-report-2022)）。
繁重、复杂的构建会成为开发团队的重大障碍，
拖慢本地开发和 CI/CD 流水线。

<!-- vale Vale.Spelling = YES -->

Docker Build Cloud 加快镜像构建速度，从而提升开发者
生产力、减少挫败感，并帮助你缩短发布周期。

## 适合谁阅读？

- 想要解决镜像构建缓慢常见成因的所有人：本地资源
  有限、模拟执行缓慢，以及团队之间缺乏构建协作。
- 使用较老旧机器、希望构建更快的开发者。
- 在同一个仓库上协作、希望通过共享缓存缩短等待时间的
  开发团队。
- 需要进行多架构构建、又不想花数小时为模拟器
  做配置和重复构建的开发者。

## 你将学到什么

- 在本地和 CI 中更快地构建容器镜像
- 加速多平台镜像的构建
- 复用预构建镜像以加快工作流

## 工具集成

与 Docker Compose、GitHub Actions 及其他 CI 方案配合良好

<div id="dbc-lp-survey-anchor"></div>

## 为什么选择 Docker Build Cloud？

Docker Build Cloud 是一项让你在本地和 CI 中都能更快构建容器镜像的
服务。构建运行在为你的工作负载优化配置的云基础设施上，
无需任何配置。该服务
使用远程构建缓存，确保在任何地方、对所有团队成员
都能实现快速构建。

相比本地构建，Docker Build Cloud 具备多项优势：

- 更快的构建速度
- 共享构建缓存
- 原生多平台构建

无需操心构建器或基础设施的管理——只需
连接到你的构建器即可开始构建。分配给某个组织的每个云构建器
都完全隔离在单独的 Amazon EC2 实例中，配有
专用的 EBS 卷用于构建缓存，并对传输过程加密。这意味着
各云构建器之间不存在共享的进程或数据。

{{< youtube-embed "8AqKhEO2PQA" >}}

<div id="dbc-lp-survey-anchor"></div>

## 演示：在开发中设置并使用 Docker Build Cloud

借助 Docker Build Cloud，你可以轻松地把构建负载从本地机器
转移到云端，从而获得更快的构建速度，多平台构建尤其明显。

在本演示中，你将看到：

- 如何在本地设置构建器
- 如何将 Docker Build Cloud 与 Docker Compose 配合使用
- 镜像缓存如何为团队中其他成员加速构建

{{< youtube-embed "oPGq2AP5OtQ" >}}

<div id="dbc-lp-survey-anchor"></div>

## 演示：在 CI 中使用 Docker Build Cloud

Docker Build Cloud 能显著缩短 CI 构建的运行时间，
为你节省时间和成本。

由于构建在远程运行，你的 CI runner 仍可使用 Docker 工具链 CLI，
且无需提升权限，从而让构建默认更安全。

在本演示中，你将看到：

- 如何将 Docker Build Cloud 集成到各类 CI 平台
- 如何在 GitHub Actions 中使用 Docker Build Cloud 构建多架构镜像
- 使用 Docker Build Cloud 的工作流与原生运行的工作流之间的速度差异
- 如何在 GitLab Pipeline 中使用 Docker Build Cloud

{{< youtube-embed "wvLdInoVBGg" >}}

<div id="dbc-lp-survey-anchor"></div>

## 常见挑战与问题

#### Docker Build Cloud 是独立产品还是 Docker Desktop 的一部分？

Docker Build Cloud 是一项既可以配合 Docker Desktop 使用、也可以
独立使用的服务。它让你在本地和 CI 中都能更快地构建容器镜像，
构建运行在云基础设施上。该服务使用远程
构建缓存，确保在任何地方、对所有团队成员都能实现快速构建。

与 Docker Desktop 配合使用时，[Builds 视图](/desktop/use-desktop/builds/)
开箱即用地支持 Docker Build Cloud。它会展示你的构建信息，
以及团队成员使用同一构建器发起的构建信息，
便于协同排查问题。

若要在不使用 Docker Desktop 的情况下使用 Docker Build Cloud，你必须
[下载并安装](/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop)
支持 Docker Build Cloud（`cloud` 驱动）的 Buildx 版本。
如果你打算使用 `docker compose build` 命令通过 Docker Build Cloud
构建，还需要一个支持 Docker
Build Cloud 的 Docker Compose 版本。

#### Docker Build Cloud 如何与 Docker Compose 协同工作？

Docker Compose 与 Docker Build Cloud 开箱即用。安装兼容 Docker
Build Cloud 的客户端（buildx），两个命令都能正常工作。

#### Docker Build Cloud 的 Team 套餐包含多少分钟？

Docker Build Cloud 的定价详情请见 [定价页面](https://www.docker.com/pricing?ref=Docs&refAction=DocsGuidesBuildCloudFaq)。

#### 我是 Docker 个人用户。可以试用 Docker Build Cloud 吗？

Docker 订阅用户（Pro、Team、Business）每月会获得一定数量的
分钟数，供账号内共享使用于 Build Cloud。

如果你没有 Docker 订阅，可以注册免费的 Personal
账号并开始 Docker Build Cloud 试用。Personal 账号仅限
单个用户。

团队若要享受共享缓存带来的收益，必须订阅 Docker
Team 或 Docker Business。

#### Docker Build Cloud 支持 CI 平台吗？它能与 GitHub Actions 一起用吗？

可以，Docker Build Cloud 可与多种 CI 平台配合使用，包括 GitHub
Actions、CircleCI、Jenkins 等。它能加速你的构建流水线，
从而减少等待和上下文切换的时间。

Docker Build Cloud 可以与 GitHub Actions 一起使用，实现构建、
测试和部署流水线的自动化。Docker 提供了一组官方 GitHub Actions
供你在工作流中使用。

在 GitHub Actions 中使用 Docker Build Cloud 非常简单。只需在
GitHub Actions 配置中改动一行，其余部分保持
不变。你无需新建流水线。详见 Docker Build Cloud 的 [CI
文档](/build-cloud/ci/)。

<div id="dbc-lp-survey-anchor"></div>
