---
---
title: History and development of Docker Compose
linkTitle: History and development
description: "Explore the evolution of Docker Compose from v1 to v5, including CLI changes, YAML versioning, and the Compose Specification."
weight: 30
aliases:
  - /compose/history/
keywords: "compose, compose yaml, swarm, migration, compatibility, docker compose vs docker-compose"---
title: Docker Compose 的历史与发展
linkTitle: 历史与发展
description: "探索 Docker Compose 从 v1 到 v5 的演进历程，包括 CLI 变更、YAML 版本控制以及 Compose 规范。"
weight: 30---
本页面提供：
 - Docker Compose CLI 开发历程的简要回顾
 - 关于构成 Compose v1、v2 和 v5 的主要版本及文件格式的清晰说明
 - Compose v1、v2 和 v5 之间的主要区别

## 简介

![展示 Compose v1、Compose v2 和 Compose v5 主要区别的图片](../images/v1-versus-v2-versus-v5.png)

上图展示了 Docker Compose v1、v2 和 v5 之间的关键区别。目前，受支持的 Docker Compose CLI 版本是 Compose v2 和 Compose v5，这两个版本都由 [Compose 规范](/reference/compose-file/_index.md) 定义。

该图对文件格式、命令行语法以及支持的一级元素进行了高层次比较。后续章节将对此进行更详细的阐述。

### Docker Compose CLI 版本控制

Compose v1 于 2014 年首次发布。它由 Python 编写，通过 `docker-compose` 命令调用。
通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级的 `version` 元素，其值范围从 `2.0` 到 `3.8`，这指的是特定的[文件格式](#compose-file-format-versioning)。

于 2020 年发布的 Compose v2 由 Go 编写，通过 `docker compose` 命令调用。
与 v1 不同，Compose v2 会忽略 `compose.yaml` 文件中的 `version` 顶级元素，并完全依赖 Compose 规范来解析文件。

于 2025 年发布的 Compose v5 在功能上与 Compose v2 相同。其主要区别是引入了一个官方的 [Go SDK](/manuals/compose/compose-sdk.md)。该 SDK 提供了一个全面的 API，允许您将 Compose 功能直接集成到您的应用程序中，从而无需依赖 Compose CLI 即可加载、验证和管理多容器环境。为了避免与标记为“v2”和“v3”的传统 Compose 文件格式混淆，版本号直接升级到了 v5。

### Compose 文件格式版本控制

Docker Compose CLI 由特定的文件格式定义。 

为 Compose v1 发布了三个主要版本的 Compose 文件格式：
- 2014 年随 Compose 1.0.0 发布的 Compose 文件格式 1
- 2016 年随 Compose 1.6.0 发布的 Compose 文件格式 2.x
- 2017 年随 Compose 1.10.0 发布的 Compose 文件格式 3.x

Compose 文件格式 1 与所有后续格式有显著不同，因为它缺少一个顶级的 `services` 键。
它的使用已成为历史，使用此格式编写的文件无法在 Compose v2 上运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决围绕 Compose CLI 版本控制、Compose 文件格式版本控制以及是否使用 Swarm 模式所带来的功能对等问题的困惑，文件格式 2.x 和 3.x 被合并到了 [Compose 规范](/reference/compose-file/_index.md) 中。 

Compose v2 和 v5 使用 Compose 规范进行项目定义。与先前的文件格式不同，Compose 规范是持续更新的，并将 `version` 顶级元素设为可选。Compose v2 和 v5 还利用了可选规范 - [Deploy](/reference/compose-file/deploy.md)、[Develop](/reference/compose-file/develop.md) 和 [Build](/reference/compose-file/build.md)。

为了简化迁移，对于在 Compose 文件格式 2.x/3.x 和 Compose 规范之间已被弃用或更改的某些元素，Compose v2 和 v5 提供了向后兼容性。

## 接下来？

- [Compose 的工作原理](compose-application-model.md)
- [Compose 规范参考](/reference/compose-file/_index.md)