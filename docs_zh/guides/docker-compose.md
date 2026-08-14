---
title: 使用 Docker Compose 定义并运行多容器应用
linkTitle: Docker Compose
summary: |
  简化定义、配置和运行多容器
  Docker 应用的过程。
description: 了解如何使用 Docker Compose 定义并运行多容器 Docker 应用。
keywords: docker compose, multi-container, compose file, services, orchestration, yaml
aliases:
  - /learning-paths/docker-compose/
  - /guides/docker-compose/common-questions/
  - /guides/docker-compose/setup/
  - /guides/docker-compose/why/
params:
  tags: [cicd]
  image: images/learning-paths/compose.png
  time: 10 minutes
---


开发者在处理多容器 Docker 应用时面临诸多挑战，包括
复杂的配置、依赖管理，以及维持环境的
一致性。网络、资源分配、数据持久化、日志和
监控更增加了难度。安全问题和故障排查
让整个过程雪上加霜，因而需要有效的工具和实践来
进行高效管理。

Docker Compose 解决了多容器 Docker 应用的管理难题：
它提供了一种简单的方式，用单个 YAML 文件定义、配置并运行
应用所需的全部容器。这种方式
帮助开发者轻松搭建、共享并维护一致的开发、
测试和生产环境，确保复杂应用能够在其所有依赖和服务
都被正确配置和编排的前提下
完成部署。

## 你将学到什么

- Docker Compose 是什么以及它能做什么
- 如何定义服务
- Docker Compose 的使用场景
- 如果没有 Docker Compose，情况会有何不同

## 适合谁阅读？

- 需要在多个环境中高效定义、管理和编排
  多容器 Docker 应用的开发者和 DevOps 工程师。
- 希望通过优化开发工作流、缩短搭建时间来
  提升生产力的开发团队。

## 工具集成

与 Docker CLI、CI/CD 工具和容器编排工具配合良好。

<div id="compose-lp-survey-anchor"></div>

## 为什么选择 Docker Compose？

Docker Compose 是定义和运行多容器 Docker 应用的
必备工具。Docker Compose 简化了 Docker 的使用体验，通过 YAML
文件配置应用服务，让开发者更容易创建、管理和部署
应用。

Docker Compose 带来以下好处：

- 让你在单个 YAML 文件中定义多容器应用。
- 确保开发、测试和生产环境的一致性。
- 轻松管理多个容器的启动与关联。
- 优化开发工作流，缩短搭建时间。
- 确保每个服务在各自的容器中运行，避免冲突。

{{< youtube-embed 2EqarOM2V4U >}}

<div id="compose-lp-survey-anchor"></div>

## 演示：搭建并使用 Docker Compose

这个 Docker Compose 演示展示了如何编排多容器应用
环境，从而简化开发与部署流程。

- 将 Docker Compose 与 `docker run` 命令做对比
- 使用 Compose 文件配置多容器 Web 应用
- 用一条命令运行多容器 Web 应用

{{< youtube-embed P5RBKmOLPH4 >}}

<div id="compose-lp-survey-anchor"></div>

## 常见挑战与问题

<!-- vale Docker.HeadingLength = NO -->

#### 我需要为开发、测试和预发布环境分别维护独立的 Compose 文件吗？

你不一定需要为开发、测试和预发布环境
维护完全独立的 Compose 文件。你可以在单个 Compose 文件
（`compose.yaml`）中定义所有服务，并使用 profiles 将
各环境（`dev`、`test`、`staging`）专属的服务配置分组。

当你需要启动某个环境时，可以激活对应的
profile。例如，搭建开发环境：

```console
$ docker compose --profile dev up
```

该命令只启动与 `dev` profile 关联的服务，
其余服务保持不启动。

有关使用 profiles 的更多信息，请参阅 [在 Compose 中使用
profiles](/compose/how-tos/profiles/)。

#### 我如何确保数据库服务先于前端服务启动？

Docker Compose 通过 `depends_on` 属性确保服务按特定顺序
启动。这会告诉 Compose 在尝试启动前端服务之前
先启动数据库服务。这一点至关重要，因为
应用往往依赖数据库已经可以接受连接。

不过，`depends_on` 只保证顺序，并不保证数据库已完全
初始化。如果需要更稳妥的做法——尤其当你的应用依赖于
一个已准备就绪的数据库（例如已完成迁移）时——请考虑使用 [健康
检查](/reference/compose-file/services.md#healthcheck)。你可以
配置前端等到数据库通过健康检查后
再启动。这样不仅能保证数据库已启动，还能保证它已就绪、可以
处理请求。

有关设置服务启动顺序的更多信息，请参阅
[在 Compose 中控制启动与关闭顺序](/compose/how-tos/startup-order/)。

#### 我可以用 Compose 构建 Docker 镜像吗？

可以，你能够使用 Docker Compose 构建 Docker 镜像。Docker Compose 是一个
定义和运行多容器应用的工具。即便你的
应用不是多容器应用，Docker Compose 也能通过把所有 `docker run`
选项写入一个文件，让运行变得更简单。

要使用 Compose，你需要一个 `compose.yaml` 文件。在该文件中，你可以为每个服务
指定构建上下文和 Dockerfile。当你运行命令
`docker compose up --build` 时，Docker Compose 会为每个服务构建镜像，
然后启动容器。

有关使用 Compose 构建 Docker 镜像的更多信息，请参阅 [Compose
Build 规范](/compose/compose-file/build/)。

#### Docker Compose 和 Dockerfile 有什么区别？

Dockerfile 提供构建容器镜像的指令，而 Compose
文件定义运行中的容器。Compose 文件常常会引用某个
Dockerfile，为特定服务构建所用的镜像。

#### `docker compose up` 和 `docker compose run` 命令有什么区别？

`docker compose up` 命令会创建并启动你的所有服务。它
非常适合启动开发环境或运行整个
应用。`docker compose run` 命令则聚焦于单个服务。
它会启动指定的服务及其依赖，让你能在该容器中运行
测试或执行一次性任务。

<div id="compose-lp-survey-anchor"></div>
