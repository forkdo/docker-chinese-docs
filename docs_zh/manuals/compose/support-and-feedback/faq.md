---
description: 关于 Docker Compose 的常见问题解答，包括 v1 与 v2 的对比、命令、关闭行为以及开发环境设置。
keywords: docker compose 常见问题, docker compose 问题, docker-compose 与 docker compose 对比, docker compose json, docker compose 停止延迟, 运行多个 docker compose
title: Docker Compose 常见问题解答
linkTitle: 常见问题
weight: 10
tags:
- FAQ
aliases:
- /compose/faq/
---

### `docker compose` 和 `docker-compose` 有什么区别？

Docker Compose 命令行工具的第一个版本发布于 2014 年。它由 Python 编写，通过 `docker-compose` 命令调用。通常，Compose v1 的项目会在 `compose.yaml` 文件中包含一个顶级的 `version` 元素，其值范围从 2.0 到 3.8，这些值指的是特定的文件格式。

Docker Compose 命令行工具的第二个版本于 2020 年发布，由 Go 编写，通过 `docker compose` 命令调用。Compose v2 会忽略 `compose.yaml` 文件中顶级的 `version` 元素。

更多信息，请参阅 [Compose 的历史与开发](/manuals/compose/intro/history.md)。

### `up`、`run` 和 `start` 有什么区别？

通常情况下，你会使用 `docker compose up`。使用 `up` 可以启动或重启 `compose.yaml` 中定义的所有服务。在默认的“附加”模式下，你会看到所有容器的所有日志。在“分离”模式（`-d`）下，Compose 在启动容器后会立即退出，但容器会继续在后台运行。

`docker compose run` 命令用于运行“一次性”或“临时”任务。它需要指定要运行的服务名称，并且只启动该服务所依赖的服务的容器。使用 `run` 来运行测试或执行管理任务，例如向数据卷容器中添加或删除数据。`run` 命令的行为类似于 `docker run -ti`，它会打开一个连接到容器的交互式终端，并返回一个与容器内进程退出状态相匹配的退出状态。

`docker compose start` 命令仅用于重启先前已创建但被停止的容器。它永远不会创建新容器。

### 为什么我的服务重新创建或停止需要 10 秒钟？

`docker compose stop` 命令尝试通过发送 `SIGTERM` 信号来停止容器。之后它会等待一个 [默认 10 秒的超时时间](/reference/cli/docker/compose/stop.md)。超时后，一个 `SIGKILL` 信号会被发送到容器以强制终止它。如果你在等待这个超时，那意味着你的容器在接收到 `SIGTERM` 信号时并未正常关闭。

关于 [容器中的进程处理信号](https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86) 这个问题，已经有很多相关的文章。

要解决此问题，请尝试以下方法：

- 确保你在 Dockerfile 中使用了 `CMD` 和 `ENTRYPOINT` 的 exec 形式。

  例如使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。
  使用字符串形式会导致 Docker 使用 `bash` 来运行你的进程，而 `bash` 无法正确处理信号。Compose 总是使用 JSON 形式，所以如果你在 Compose 文件中覆盖了 command 或 entrypoint，则无需担心。

- 如果可以，请修改你正在运行的应用程序，为其添加一个明确的 `SIGTERM` 信号处理器。

- 将 `stop_signal` 设置为应用程序知道如何处理的信号：

  ```yaml
  services:
    web:
      build: .
      stop_signal: SIGINT
  ```

- 如果你无法修改应用程序，可以将应用程序包装在一个轻量级的 init 系统（如 [s6](https://skarnet.org/software/s6/)）或信号代理（如 [dumb-init](https://github.com/Yelp/dumb-init) 或 [tini](https://github.com/krallin/tini)）中。这些包装器中的任何一个都能正确处理 `SIGTERM`。

### 如何在同一主机上运行多个 Compose 文件副本？

Compose 使用项目名称为项目的所有容器和其他资源创建唯一标识符。要运行一个项目的多个副本，请使用 `-p` 命令行选项或 [`COMPOSE_PROJECT_NAME` 环境变量](/manuals/compose/how-tos/environment-variables/envvars.md#compose_project_name) 设置一个自定义项目名称。

### 我的 Compose 文件可以使用 JSON 而不是 YAML 吗？

可以。[YAML 是 JSON 的超集](https://stackoverflow.com/a/1729545/444646)，因此任何 JSON 文件都应该是有效的 YAML。要在 Compose 中使用 JSON 文件，请指定要使用的文件名，例如：

```console
$ docker compose -f compose.json up
```

### 我应该使用 `COPY`/`ADD` 还是数据卷来包含我的代码？

你可以通过在 `Dockerfile` 中使用 `COPY` 或 `ADD` 指令将代码添加到镜像中。如果你需要将代码连同 Docker 镜像一起迁移（例如，当代码需要发送到其他环境（如生产环境、CI 等）时），这会非常有用。

如果你希望修改代码并立即看到效果，请使用 `volume`，例如在开发代码且服务器支持热代码重载或实时重载时。

在某些情况下，你可能希望两者都使用。你可以让镜像通过 `COPY` 包含代码，并在开发时在 Compose 文件中使用 `volume` 来包含主机上的代码。数据卷会覆盖镜像中的目录内容。