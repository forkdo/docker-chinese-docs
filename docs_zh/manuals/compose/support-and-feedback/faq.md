---
description: Docker Compose 常见问题解答，包括 v1 与 v2 的区别、命令、关闭行为和开发环境设置。
keywords: docker compose faq, docker compose 常见问题, docker-compose vs docker compose, docker compose json, docker compose 停止延迟, 运行多个 docker compose
title: Docker Compose 常见问题解答
linkTitle: 常见问题
weight: 10
tags: [FAQ]
aliases:
- /compose/faq/
---

### `docker compose` 和 `docker-compose` 有什么区别？

Docker Compose 命令行二进制文件的第一个版本于 2014 年发布。它使用 Python 编写，通过 `docker-compose` 调用。通常，Compose v1 项目在 `compose.yaml` 文件中包含顶级 version 元素，值范围从 2.0 到 3.8，指的是特定的文件格式。

Docker Compose 命令行二进制文件的第二个版本于 2020 年宣布，使用 Go 编写，通过 `docker compose` 调用。Compose v2 会忽略 compose.yaml 文件中的 version 顶级元素。

更多信息，请参阅 [Compose 的历史与发展](/manuals/compose/intro/history.md)。

### `up`、`run` 和 `start` 之间有什么区别？

通常，你想要使用 `docker compose up`。使用 `up` 启动或重启 `compose.yaml` 中定义的所有服务。在默认的"附加"模式下，你可以看到所有容器的所有日志。在"分离"模式（`-d`）下，Compose 在启动容器后退出，但容器继续在后台运行。

`docker compose run` 命令用于运行"一次性"或"临时"任务。它需要你想要运行的服务名称，并且只启动运行服务所依赖的服务的容器。使用 `run` 来运行测试或执行管理任务，例如从数据卷容器中删除或添加数据。`run` 命令的行为类似于 `docker run -ti`，因为它会为容器打开一个交互式终端，并返回与容器中进程退出状态匹配的退出状态。

`docker compose start` 命令仅在重启之前已创建但已停止的容器时有用。它永远不会创建新的容器。

### 为什么我的服务需要 10 秒钟才能重新创建或停止？

`docker compose stop` 命令尝试通过发送 `SIGTERM` 来停止容器。然后它会等待 [默认 10 秒的超时时间](/reference/cli/docker/compose/stop.md)。超时后，会向容器发送 `SIGKILL` 以强制终止它。如果你正在等待这个超时，这意味着你的容器在接收到 `SIGTERM` 信号时没有正常关闭。

关于容器中[进程处理信号](https://medium.com/@gchudnov/trapping-signals-in-docker-containers-7a57fdda7d86)的问题，已经有很多讨论。

要解决这个问题，请尝试以下方法：

- 确保在 Dockerfile 中使用 `CMD` 和 `ENTRYPOINT` 的 exec 形式。

  例如使用 `["program", "arg1", "arg2"]` 而不是 `"program arg1 arg2"`。使用字符串形式会导致 Docker 使用 `bash` 运行你的进程，而 `bash` 不能正确处理信号。Compose 始终使用 JSON 形式，所以如果你在 Compose 文件中覆盖命令或入口点，不用担心。

- 如果可能，修改你正在运行的应用程序，为其添加显式的 `SIGTERM` 信号处理器：

  ```yaml
  services:
    web:
      build: .
      stop_signal: SIGINT
  ```

- 如果你无法修改应用程序，用轻量级 init 系统（如 [s6](https://skarnet.org/software/s6/)）或信号代理（如 [dumb-init](https://github.com/Yelp/dumb-init) 或 [tini](https://github.com/krallin/tini)）包装应用程序。这些包装器中的任何一个都能正确处理 `SIGTERM`。

### 如何在同一主机上运行多个 Compose 文件副本？

Compose 使用项目名称为项目的所有容器和其他资源创建唯一标识符。要运行项目的多个副本，请使用 `-p` 命令行选项或 [`COMPOSE_PROJECT_NAME` 环境变量](/manuals/compose/how-tos/environment-variables/envvars.md#compose_project_name) 设置自定义项目名称。

### 我可以对 Compose 文件使用 JSON 而不是 YAML 吗？

可以。[YAML 是 JSON 的超集](https://stackoverflow.com/a/1729545/444646)，所以任何 JSON 文件都应该是有效的 YAML。要在 Compose 中使用 JSON 文件，请指定要使用的文件名，例如：

```console
$ docker compose -f compose.json up
```

### 我应该使用 `COPY`/`ADD` 还是卷来包含我的代码？

你可以使用 `Dockerfile` 中的 `COPY` 或 `ADD` 指令将代码添加到镜像中。当你需要将代码与 Docker 镜像一起移动时，这很有用，例如当你将代码发送到另一个环境（生产、CI 等）时。

如果你想要修改代码并立即看到更改，请使用 `volume`，例如当你正在开发代码且服务器支持热代码重载或实时重载时。

在某些情况下，你可能想要同时使用两者。你可以让镜像使用 `COPY` 包含代码，并在你的 Compose 文件中使用 `volume` 在开发期间从主机包含代码。卷会覆盖镜像中目录的内容。