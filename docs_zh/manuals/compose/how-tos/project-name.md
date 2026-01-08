---
title: 指定项目名称
weight: 10
description: 了解如何在 Compose 中设置自定义项目名称，以及理解每种方法的优先级。
keywords: name, compose, project, -p flag, name top-level element
aliases:
- /compose/project-name/
---

默认情况下，Compose 会根据存放 Compose 文件的目录名称来分配项目名称。您可以通过多种方法覆盖此设置。

本页面提供了自定义项目名称可能有益的场景示例，概述了设置项目名称的各种方法，并提供了每种方法的优先顺序。

> [!NOTE]
>
> 默认的项目目录是 Compose 文件所在的基础目录。也可以使用 [`--project-directory` 命令行选项](/reference/cli/docker/compose.md#options)为其设置自定义值。

## 示例用例

Compose 使用项目名称来隔离不同的环境。在多种情况下，项目名称都非常有用：

- 在开发主机上：为单个环境创建多个副本，这对于为项目的每个功能分支运行稳定副本非常有用。
- 在 CI 服务器上：通过将项目名称设置为唯一的构建编号，防止构建之间相互干扰。
- 在共享或开发主机上：避免可能共享相同服务名称的不同项目之间发生干扰。

## 设置项目名称

项目名称必须仅包含小写字母、十进制数字、短横线和下划线，并且必须以小写字母或十进制数字开头。如果项目目录或当前目录的基本名称违反此约束，则可以使用其他机制。

每种方法的优先顺序（从高到低）如下：

1. `-p` 命令行标志。
2. [COMPOSE_PROJECT_NAME 环境变量](environment-variables/envvars.md)。
3. Compose 文件中的[顶层 `name:` 属性](/reference/compose-file/version-and-name.md)。或者，如果在命令行中使用 `-f` 标志[指定了多个 Compose 文件](multiple-compose-files/merge.md)，则为最后一个 `name:`。
4. 包含 Compose 文件的项目目录的基本名称。或者，如果在命令行中使用 `-f` 标志[指定了多个 Compose 文件](multiple-compose-files/merge.md)，则为第一个 Compose 文件的基本名称。
5. 如果未指定 Compose 文件，则为当前目录的基本名称。

## 下一步是什么？

- 阅读[使用多个 Compose 文件](multiple-compose-files/_index.md)。
- 探索一些[示例应用](https://github.com/docker/awesome-compose)。