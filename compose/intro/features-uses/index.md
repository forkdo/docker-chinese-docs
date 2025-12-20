# 为什么使用 Compose？

## Docker Compose 的主要优势

使用 Docker Compose 具有诸多优势，能够简化容器化应用程序的开发、部署和管理：

- **简化控制**：在一个 YAML 文件中定义和管理多容器应用，简化编排和复制过程。

- **高效协作**：可共享的 YAML 文件支持开发人员和运维人员之间的顺畅协作，改进工作流程和问题解决，从而提高整体效率。

- **快速应用程序开发**：Compose 会缓存用于创建容器的配置。当您重启未更改的服务时，Compose 会复用现有容器。复用容器意味着您可以非常快速地对环境进行更改。

- **跨环境可移植性**：Compose 支持 Compose 文件中的变量。您可以使用这些变量为不同的环境或不同的用户自定义您的组合。

## Docker Compose 的常见用例

Compose 可以多种方式使用。下面概述了一些常见用例。

### 开发环境

在开发软件时，能够在隔离的环境中运行应用程序并与之交互至关重要。Compose 命令行工具可用于创建环境并与之交互。

[Compose 文件](/reference/compose-file/_index.md) 提供了一种记录和配置应用程序所有服务依赖项（数据库、队列、缓存、Web 服务 API 等）的方法。使用 Compose 命令行工具，您只需一个命令 (`docker compose up`) 即可为每个依赖项创建并启动一个或多个容器。

这些功能共同为您启动项目提供了一种便捷的方式。Compose 可以将多页的“开发者入门指南”简化为一个机器可读的 Compose 文件和几个命令。

### 自动化测试环境

任何持续部署或持续集成流程的一个重要部分是自动化测试套件。自动化端到端测试需要一个运行测试的环境。Compose 提供了一种便捷的方法来为您的测试套件创建和销毁隔离的测试环境。通过在 [Compose 文件](/reference/compose-file/_index.md) 中定义完整的环境，您只需几个命令即可创建和销毁这些环境：

```console
$ docker compose up -d
$ ./run_tests
$ docker compose down
```

### 单主机部署

Compose 传统上专注于开发和测试工作流，但随着每个版本的发布，我们都在面向生产的特性方面取得进展。

有关使用面向生产特性的详细信息，请参阅 [生产环境中的 Compose](/manuals/compose/how-tos/production.md)。

## 下一步是什么？

- [了解 Compose 的历史](history.md)
- [理解 Compose 的工作原理](compose-application-model.md)
- [尝试快速入门指南](../gettingstarted.md)
