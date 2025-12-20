# Docker Compose 的历史与发展

本页提供：
 - Docker Compose CLI 发展历程的简要介绍
 - 构成 Compose v1 和 Compose v2 的主要版本及文件格式的清晰说明
 - Compose v1 与 Compose v2 之间的主要差异

## 简介

![显示 Compose v1 与 Compose v2 主要差异的图片](../images/v1-versus-v2.png)

上图显示，当前支持的 Docker Compose CLI 版本是 Compose v2，其定义基于 [Compose 规范](/reference/compose-file/_index.md)。

该图还简要展示了文件格式、命令行语法和顶级元素之间的差异。以下章节将对此进行更详细的说明。

### Docker Compose CLI 版本控制

Docker Compose 命令行二进制文件的第一个版本于 2014 年首次发布。它使用 Python 编写，通过 `docker-compose` 命令调用。
通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级 `version` 元素，其取值范围从 `2.0` 到 `3.8`，这些值指向特定的[文件格式](#compose-file-format-versioning)。

Docker Compose 命令行二进制文件的第二个版本于 2020 年发布，使用 Go 语言编写，通过 `docker compose` 命令调用。
Compose v2 会忽略 `compose.yaml` 文件中的 `version` 顶级元素。

### Compose 文件格式版本控制

Docker Compose CLI 由特定的文件格式定义。

Compose v1 的文件格式发布了三个主要版本：
- 2014 年随 Compose 1.0.0 发布的 Compose 文件格式 1
- 2016 年随 Compose 1.6.0 发布的 Compose 文件格式 2.x
- 2017 年随 Compose 1.10.0 发布的 Compose 文件格式 3.x

Compose 文件格式 1 与后续所有格式有显著不同，因为它缺少顶级 `services` 键。
该格式仅用于历史参考，使用此格式编写的文件无法在 Compose v2 中运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决 Compose CLI 版本控制、Compose 文件格式版本控制以及 Swarm 模式使用与否导致的特性差异等问题，文件格式 2.x 和 3.x 被合并为 [Compose 规范](/reference/compose-file/_index.md)。

Compose v2 使用 Compose 规范进行项目定义。与之前的文件格式不同，Compose 规范是持续演进的，并且使 `version` 顶级元素成为可选。Compose v2 还使用了可选规范 - [Deploy](/reference/compose-file/deploy.md)、[Develop](/reference/compose-file/develop.md) 和 [Build](/reference/compose-file/build.md)。

为了简化[migration](/manuals/compose/releases/migrate.md)迁移过程，Compose v2 对某些在 Compose 文件格式 2.x/3.x 与 Compose 规范之间已被弃用或更改的元素提供了向后兼容性。

## 下一步

- [Compose 如何工作](compose-application-model.md)
- [Compose 规范参考](/reference/compose-file/_index.md)
- [从 Compose v1 迁移到 v2](/manuals/compose/releases/migrate.md)
