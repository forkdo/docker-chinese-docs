---
title: Docker Compose 的历史与发展
linkTitle: 历史与发展
description: 探索 Docker Compose 从 v1 到 v2 的演进历程，包括 CLI 变化、YAML 版本控制以及 Compose 规范。
keywords: compose, compose yaml, swarm, 迁移, 兼容性, docker compose vs docker-compose
weight: 30
aliases:
- /compose/history/
---

本页面提供以下内容：
 - Docker Compose CLI 开发历程的简要概述
 - 对构成 Compose v1 和 Compose v2 的主要版本和文件格式的清晰解释
 - Compose v1 和 Compose v2 之间的主要区别

## 介绍

![显示 Compose v1 和 Compose v2 之间主要区别的图片](../images/v1-versus-v2.png)

上图显示了当前受支持的 Docker Compose CLI 版本是 Compose v2，它由 [Compose 规范](/reference/compose-file/_index.md) 定义。

它还快速展示了文件格式、命令行语法和顶级元素之间的差异快照。以下部分将详细介绍这些内容。

### Docker Compose CLI 版本控制

Docker Compose 命令行二进制文件的第一个版本于 2014 年发布。它使用 Python 编写，通过 `docker-compose` 命令调用。
通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级 `version` 元素，值范围从 `2.0` 到 `3.8`，这些值指的是特定的 [文件格式](#compose-file-format-versioning)。

Docker Compose 命令行二进制文件的第二个版本于 2020 年宣布，使用 Go 编写，通过 `docker compose` 命令调用。
Compose v2 忽略 `compose.yaml` 文件中的 `version` 顶级元素。

### Compose 文件格式版本控制

Docker Compose CLI 由特定的文件格式定义。

Compose v1 发布了三个主要版本的 Compose 文件格式：
- Compose 1.0.0 于 2014 年发布 Compose 文件格式 1
- Compose 1.6.0 于 2016 年发布 Compose 文件格式 2.x
- Compose 1.10.0 于 2017 年发布 Compose 文件格式 3.x

Compose 文件格式 1 与所有后续格式有显著不同，因为它缺少顶级 `services` 键。
其使用具有历史性，使用此格式编写的文件无法与 Compose v2 一起运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决 Compose CLI 版本控制、Compose 文件格式版本控制以及是否使用 Swarm 模式时功能兼容性方面的混淆，文件格式 2.x 和 3.x 被合并到 [Compose 规范](/reference/compose-file/_index.md) 中。

Compose v2 使用 Compose 规范进行项目定义。与之前的文件格式不同，Compose 规范是滚动更新的，使 `version` 顶级元素成为可选项。Compose v2 还利用了可选规范 —— [Deploy](/reference/compose-file/deploy.md)、[Develop](/reference/compose-file/develop.md) 和 [Build](/reference/compose-file/build.md)。

为了便于 [迁移](/manuals/compose/releases/migrate.md)，Compose v2 对 Compose 文件格式 2.x/3.x 与 Compose 规范之间已弃用或更改的某些元素具有向后兼容性。

## 接下来是什么？

- [Compose 如何工作](compose-application-model.md)
- [Compose 规范参考](/reference/compose-file/_index.md)
- [从 Compose v1 迁移到 v2](/manuals/compose/releases/migrate.md)