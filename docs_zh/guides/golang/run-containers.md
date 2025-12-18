---
title: 以容器方式运行你的 Go 镜像
linkTitle: 运行容器
weight: 10
keywords: get started, go, golang, run, container
description: 学习如何以容器方式运行镜像。
aliases:
  - /get-started/golang/run-containers/
  - /language/golang/run-containers/
  - /guides/language/golang/run-containers/
---

## 前置条件

请先完成前一模块的步骤，为示例应用程序创建 Dockerfile 并使用 `docker build` 命令构建 Docker 镜像，详见 [构建你的 Go 镜像](build-images.md)。

## 概述

在上一模块中，你为示例应用程序创建了 `Dockerfile`，并使用 `docker build` 命令构建了 Docker 镜像。现在有了镜像，你就可以运行该镜像，验证应用程序是否正常工作。

容器本质上是一个普通的操作系统进程，但该进程是被隔离的，拥有自己的文件系统、自己的网络和独立于宿主机的进程树。

要在容器中运行镜像，你需要使用 `docker run` 命令。该命令至少需要一个参数，即镜像名称。运行以下命令启动你的镜像并确认应用程序正常运行：

```console
$ docker run docker-gs-ping
```

```text
   ____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.10.2
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______
                                    O\
⇨ http server started on [::]:8080
```

执行该命令后，你会注意到命令行提示符没有返回。这是因为你的应用程序是一个 REST 服务器，它会持续循环等待传入请求，直到你停止容器才会将控制权交还给操作系统。

使用 curl 命令向服务器发送一个 GET 请求：

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

curl 命令失败了，因为连接被拒绝。这意味着你无法连接到宿主机 8080 端口上的本地服务。这是预期的，因为容器运行在隔离环境中，包括网络也是隔离的。停止容器，然后以发布 8080 端口到本地网络的方式重新启动。

按 ctrl-c 停止容器，回到终端提示符。

要发布容器的端口，你需要在 `docker run` 命令中使用 `--publish` 标志（简写为 `-p`）。`--publish` 的格式是 `[宿主机端口]:[容器端口]`。如果你想将容器内的 8080 端口映射到宿主机的 3000 端口，就需要传入 `3000:8080`。

启动容器，并将容器的 8080 端口发布到宿主机的 8080 端口：

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

现在，再次运行 curl 命令：

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

成功！你成功连接到容器内运行在 8080 端口的应用程序。切换回容器运行的终端，你应该能看到 `GET` 请求已记录到控制台。

按 `ctrl-c` 停止容器。

## 以分离模式运行

到目前为止一切顺利，但你的示例应用程序是一个 Web 服务器，你不应该让终端一直连接到容器。Docker 可以让容器在后台以分离模式运行。为此，你可以使用 `--detach` 标志（简写为 `-d`）。Docker 会像之前一样启动你的容器，但这次会从容器中分离并返回终端提示符。

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker 在后台启动了你的容器，并在终端打印出容器 ID。

再次确认容器正在运行。执行相同的 `curl` 命令：

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

## 列出容器

由于你的容器在后台运行，你如何知道容器是否正在运行，或者你的机器上还有哪些其他容器在运行？要查看机器上运行的容器列表，运行 `docker ps` 命令。这类似于在 Linux 机器上使用 `ps` 命令查看进程列表。

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

`ps` 命令会显示你的运行中容器的大量信息。你可以看到容器 ID、容器内运行的镜像、启动容器时使用的命令、创建时间、状态、暴露的端口以及容器名称。

你可能想知道容器名称是从哪里来的。由于你启动容器时没有指定名称，Docker 自动生成了一个随机名称。稍后你会修复这个问题，但首先需要停止容器。要停止容器，运行 `docker stop` 命令，并传入容器名称或 ID。

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在再次运行 `docker ps` 命令查看运行中容器的列表：

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## 停止、启动和命名容器

Docker 容器可以被启动、停止和重启。当你停止一个容器时，它不会被删除，但状态会变为已停止，容器内的进程也会停止。当你运行 `docker ps` 命令时，默认只显示运行中的容器。如果你传入 `--all` 或简写 `-a`，你将看到系统上所有容器，包括已停止和正在运行的容器。

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

如果你一直跟着操作，你应该能看到列出的几个容器。这些都是你启动并停止过但尚未删除的容器。

重启你刚停止的容器。找到容器名称，并在以下 `restart` 命令中替换为你的容器名称：

```console
$ docker restart inspiring_ishizaka
```

现在，再次使用 `ps` 命令列出所有容器：

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

注意，你刚重启的容器是以分离模式启动的，并且暴露了 8080 端口。另外，注意容器状态是 `Up X seconds`。当你重启容器时，它会使用最初启动时的相同标志或命令启动。

停止并删除所有容器，然后解决随机命名的问题。

停止你刚启动的容器。找到你运行中容器的名称，并在以下命令中替换为你的容器名称：

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在所有容器都已停止，接下来删除它们。删除容器后，它既不是运行状态，也不是停止状态，而是容器内的进程被终止，容器的元数据也被移除。

要删除容器，运行 `docker rm` 命令并传入容器名称。你可以在一个命令中传入多个容器名称：

同样，确保以下命令中的容器名称替换为你系统上的容器名称：

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

再次运行 `docker ps --all` 命令验证所有容器都已删除。

现在，解决随机命名的问题。最佳实践是为容器命名，原因很简单：这样更容易识别容器中运行的内容以及它关联的应用程序或服务。就像代码中变量的良好命名约定能让代码更易读一样，给容器命名也是如此。

要为容器命名，你必须在 `run` 命令中传入 `--name` 标志：

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

现在，你可以根据名称轻松识别你的容器。

## 下一步

在本模块中，你学会了如何运行容器和发布端口，还学会了如何管理容器的生命周期。然后，你了解了为容器命名的重要性，以便更容易识别。在下一模块中，你将学习如何在容器中运行数据库，并将其连接到你的应用程序。