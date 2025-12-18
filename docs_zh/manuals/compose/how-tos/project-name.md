---
title: 指定项目名称
weight: 10
description: 了解如何在 Compose 中设置自定义项目名称，以及每种方法的优先级。
keywords: name, compose, project, -p flag, name top-level element
aliases:
- /compose/project-name/
---

默认情况下，Compose 会根据包含 Compose 文件的目录名称来分配项目名称。你可以通过多种方法来覆盖此默认行为。

本文提供了自定义项目名称可能有用的场景示例，概述了设置项目名称的各种方法，并说明了每种方法的优先级顺序。

> [!NOTE]
>
> 默认的项目目录是 Compose 文件所在的根目录。也可以使用 [`--project-directory` 命令行选项](/reference/cli/docker/compose.md#options) 来设置自定义值。

## 示例使用场景

Compose 使用项目名称来隔离不同的环境。在以下场景中，项目名称非常有用：

- 在开发主机上：创建单个环境的多个副本，这对于为项目的每个功能分支运行稳定的副本很有用。
- 在 CI 服务器上：通过将项目名称设置为唯一的构建编号来防止构建之间的干扰。
- 在共享或开发主机上：避免不同项目之间可能共享相同服务名称时的相互干扰。

## 设置项目名称

项目名称必须仅包含小写字母、十进制数字、连字符和下划线，并且必须以小写字母或十进制数字开头。如果项目目录或当前目录的基名称违反了此约束，则可以使用其他机制。

每种方法的优先级顺序从高到低如下：

1. `-p` 命令行标志。
2. [COMPOSE_PROJECT_NAME 环境变量](environment-variables/envvars.md)。
3. Compose 文件中的 [顶级 `name:` 属性](/reference/compose-file/version-and-name.md)。或者，如果你使用 `-f` 标志在命令行中 [指定多个 Compose 文件](multiple-compose-files/merge.md)，则为最后一个 `name:`。
4. 包含 Compose 文件的项目目录的基名称。或者，如果你使用 `-f` 标志在命令行中 [指定多个 Compose 文件](multiple-compose-files/merge.md)，则为第一个 Compose 文件的基名称。
5. 如果未指定 Compose 文件，则为当前目录的基名称。

## 下一步

- 阅读 [使用多个 Compose 文件](multiple-compose-files/_index.md) 的相关内容。
- 探索一些 [Compose 示例应用](samples-for-compose.md)。