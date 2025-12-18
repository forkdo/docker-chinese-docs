---
description: 了解 Docker Compose 在容器化应用开发和部署中的优势和典型使用场景
keywords: docker compose, compose 使用场景, compose 优势, 容器编排, 开发环境, 测试容器, yaml 文件
title: 为什么使用 Compose？
weight: 20
aliases: 
- /compose/features-uses/
---

## Docker Compose 的主要优势

使用 Docker Compose 提供了多种优势，可简化容器化应用的开发、部署和管理：

- 简化控制：通过单个 YAML 文件定义和管理多容器应用，简化编排和复制流程。

- 高效协作：可共享的 YAML 文件支持开发和运维之间的顺畅协作，改善工作流程和问题解决，提高整体效率。

- 快速应用开发：Compose 会缓存用于创建容器的配置。当你重启未更改的服务时，Compose 会复用现有容器。复用容器意味着你可以快速更改环境。

- 跨环境可移植性：Compose 支持 Compose 文件中的变量。你可以使用这些变量为不同环境或不同用户自定义组合。

## Docker Compose 的常见使用场景

Compose 可以以多种不同方式使用。以下概述了一些常见使用场景。

### 开发环境

开发软件时，能够在隔离环境中运行应用并与之交互至关重要。Compose 命令行工具可用于创建环境并与之交互。

[Compose 文件](/reference/compose-file/_index.md) 提供了一种记录和配置应用所有服务依赖项（数据库、队列、缓存、Web 服务 API 等）的方法。使用 Compose 命令行工具，你可以通过单个命令（`docker compose up`）为每个依赖项创建并启动一个或多个容器。

这些功能共同为项目启动提供了便捷方式。Compose 可将多页的“开发者入门指南”简化为单个机器可读的 Compose 文件和几条命令。

### 自动化测试环境

持续部署或持续集成流程的重要组成部分是自动化测试套件。自动化端到端测试需要一个运行测试的环境。Compose 为创建和销毁测试套件的隔离测试环境提供了便捷方式。通过在 [Compose 文件](/reference/compose-file/_index.md) 中定义完整环境，你可以仅用几条命令创建和销毁这些环境：

```console
$ docker compose up -d
$ ./run_tests
$ docker compose down
```

### 单主机部署

Compose 传统上专注于开发和测试工作流，但随着每个版本的发布，我们在更多面向生产的功能方面不断进步。

有关使用面向生产功能的详细信息，请参阅
[生产环境中的 Compose](/manuals/compose/how-tos/production.md)。

## 接下来做什么？

- [了解 Compose 的历史](history.md)
- [理解 Compose 的工作原理](compose-application-model.md)
- [尝试快速入门指南](../gettingstarted.md)