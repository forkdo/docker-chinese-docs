# Docker Compose 的历史和发展

本页提供：
 - Docker Compose CLI 的发展简史
 - 构成 Compose v1、v2 和 v5 的主要版本和文件格式的清晰解释
 - Compose v1、v2 和 v5 之间的主要区别

## 简介

![显示 Compose v1、Compose v2 和 Compose v5 之间主要区别的图示](../images/v1-versus-v2-versus-v5.png)

上图重点介绍了 Docker Compose v1、v2 和 v5 之间的关键区别。目前，受支持的 Docker Compose CLI 版本是 Compose v2 和 Compose v5，两者均由 [Compose 规范](/reference/compose-file/_index.md) 定义。

该图提供了文件格式、命令行语法和支持的顶级元素的高级比较。以下各节将更详细地介绍这些内容。

### Docker Compose CLI 版本控制

Compose v1 于 2014 年首次发布。它用 Python 编写，通过 `docker-compose` 调用。
通常，Compose v1 项目在 `compose.yaml` 文件中包含一个顶级 `version` 元素，其值范围从 `2.0` 到 `3.8`，这些值指的是特定的 [文件格式](#compose-file-format-versioning)。

Compose v2 于 2020 年宣布，用 Go 编写，通过 `docker compose` 调用。
与 v1 不同，Compose v2 忽略 `compose.yaml` 文件中的 `version` 顶级元素，并完全依赖 Compose 规范来解释文件。

Compose v5 于 2025 年发布，在功能上与 Compose v2 相同。其主要区别是引入了官方的 [Go SDK](/manuals/compose/compose-sdk.md)。该 SDK 提供了一个全面的 API，允许您将 Compose 功能直接集成到您的应用程序中，从而无需依赖 Compose CLI 即可加载、验证和管理多容器环境。为避免与标记为“v2”和“v3”的旧 Compose 文件格式混淆，版本号直接提升至 v5。

### Compose 文件格式版本控制

Docker Compose CLI 由特定的文件格式定义。

Compose v1 发布了三个主要版本的 Compose 文件格式：
- 2014 年随 Compose 1.0.0 发布的 Compose 文件格式 1
- 2016 年随 Compose 1.6.0 发布的 Compose 文件格式 2.x
- 2017 年随 Compose 1.10.0 发布的 Compose 文件格式 3.x

Compose 文件格式 1 与所有后续格式有显著不同，因为它缺少顶级 `services` 键。它的使用是历史性的，用此格式编写的文件无法在 Compose v2 上运行。

Compose 文件格式 2.x 和 3.x 彼此非常相似，但后者引入了许多针对 Swarm 部署的新选项。

为了解决 Compose CLI 版本控制、Compose 文件格式版本控制以及是否使用 Swarm 模式导致的功能对等性方面的混淆，文件格式 2.x 和 3.x 已合并到 [Compose 规范](/reference/compose-file/_index.md) 中。

Compose v2 和 v5 使用 Compose 规范进行项目定义。与之前的文件格式不同，Compose 规范是滚动更新的，并使 `version` 顶级元素成为可选。Compose v2 和 v5 还利用了可选规范 - [Deploy](/reference/compose-file/deploy.md)、[Develop](/reference/compose-file/develop.md) 和 [Build](/reference/compose-file/build.md)。

为了使迁移更容易，Compose v2 和 v5 对某些在 Compose 文件格式 2.x/3.x 和 Compose 规范之间已被弃用或更改的元素提供了向后兼容性。

## 下一步是什么？

- [Compose 的工作原理](compose-application-model.md)
- [Compose 规范参考](/reference/compose-file/_index.md)
