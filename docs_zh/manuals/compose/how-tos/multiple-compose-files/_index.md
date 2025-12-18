---
description: Docker Compose 中处理多个 Compose 文件的不同方式的总体概述
keywords: compose, compose file, merge, extends, include, docker compose, -f flag
linkTitle: 使用多个 Compose 文件
title: 使用多个 Compose 文件
weight: 80
aliases:
- /compose/multiple-compose-files/
---

本节包含有关如何使用多个 Compose 文件的详细信息。

使用多个 Compose 文件可以让你为不同的环境或工作流自定义 Compose 应用。这对于可能使用数十个容器的大型应用非常有用，这些容器的所有权分布在多个团队之间。例如，如果你的组织或团队使用 monorepo，每个团队可能都有自己的“本地” Compose 文件来运行应用的子集。然后，他们需要依赖其他团队提供定义其子集预期运行方式的参考 Compose 文件。复杂性从代码转移到基础设施和配置文件中。

使用多个 Compose 文件的最快方法是使用命令行中的 `-f` 标志[合并](merge.md) Compose 文件，列出你想要的 Compose 文件。但是，[合并规则](merge.md#merging-rules) 意味着这很快就会变得相当复杂。

Docker Compose 提供了两种其他选项来管理使用多个 Compose 文件时的复杂性。根据你项目的需要，你可以：

- [扩展 Compose 文件](extends.md)，通过引用另一个 Compose 文件并选择你想要在自己的应用中使用的部分，同时能够覆盖某些属性。
- 在你的 Compose 文件中直接[包含其他 Compose 文件](include.md)。