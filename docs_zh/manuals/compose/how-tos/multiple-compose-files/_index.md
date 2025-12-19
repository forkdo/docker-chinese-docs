---
description: 本文概述了在 Docker Compose 中处理多个 Compose 文件的不同方法
keywords: compose, compose file, merge, extends, include, docker compose, -f flag
linkTitle: 使用多个 Compose 文件
title: 使用多个 Compose 文件
weight: 80
aliases:
- /compose/multiple-compose-files/
---

本节包含关于处理多个 Compose 文件的方法的信息。

使用多个 Compose 文件可以让你为不同的环境或工作流自定义 Compose 应用程序。这对于可能使用数十个容器的大型应用程序非常有用，其所有权分布在多个团队中。例如，如果你的组织或团队使用单体仓库（monorepo），每个团队可能都有自己的“本地”Compose 文件来运行应用程序的子集。然后他们需要依赖其他团队提供一个参考 Compose 文件，该文件定义了运行他们自己子集的预期方式。复杂性从代码转移到了基础设施和配置文件中。

处理多个 Compose 文件的最快方法是使用命令行中的 `-f` 标志来[合并](merge.md) Compose 文件，列出你所需的 Compose 文件。然而，[合并规则](merge.md#merging-rules)意味着这可能很快变得相当复杂。

Docker Compose 提供了另外两个选项来在处理多个 Compose 文件时管理这种复杂性。根据你项目的需求，你可以：

- 通过引用另一个 Compose 文件并选择你想要在自己应用程序中使用的部分，来[扩展一个 Compose 文件](extends.md)，并能够覆盖某些属性。
- 直接在你的 Compose 文件中[包含其他 Compose 文件](include.md)。