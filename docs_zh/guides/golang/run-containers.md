---
title: 以容器形式运行 Go 镜像
linkTitle: 运行容器
weight: 10
keywords: 入门, go, golang, 运行, 容器
description: 学习如何以容器形式运行镜像。
aliases:
  - /get-started/golang/run-containers/
  - /language/golang/run-containers/
  - /guides/language/golang/run-containers/
---

## 前提条件

请先完成 [构建 Go 镜像](build-images.md) 中的步骤，将 Go 应用程序容器化。

## 概览

在上一模块中，你为示例应用程序创建了 `Dockerfile`，然后使用 `docker build` 命令创建了 Docker 镜像。现在你已经拥有了镜像，可以运行该镜像并查看应用程序是否正常运行。

容器是一个常规的操作系统进程，不同之处在于该进程是隔离的，拥有自己的文件系统、自己的网络以及独立于主机的隔离进程树。

要在容器内运行镜像，需使用 `docker run` 命令。该命令需要一个参数，即镜像名称。启动你的镜像并确保其正常运行。在终端中运行以下命令。

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

运行此命令时，你会注意到没有返回到命令提示符。这是因为你的应用程序是一个 REST 服务器，它将在循环中运行以等待传入的请求，直到你停止容器才会将控制权交还给操作系统。

使用 curl 命令向服务器发出 GET 请求。

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

你的 curl 命令失败了，因为连接到服务器的请求被拒绝。这意味着你无法连接到本地主机（localhost）的 8080 端口。这是预期的，因为你的容器在隔离环境中运行，这包括网络。停止容器，并在本地网络上发布 8080 端口后重新启动。

要停止容器，请按 `ctrl-c`。这将使你返回到终端提示符。

要为容器发布端口，你可以在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式是 `[主机端口]:[容器端口]`。因此，如果你想将容器内部的 `8080` 端口暴露给容器外部的 `3000` 端口，你需要向 `--publish` 标志传递 `3000:8080`。

启动容器，并将 `8080` 端口暴露给主机的 `8080` 端口。

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

现在，重新运行 curl 命令。

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

成功！你能够连接到容器内运行在 8080 端口上的应用程序了。切换回运行容器的终端，你应该会看到 `GET` 请求被记录到控制台。

按 `ctrl-c` 停止容器。

## 以后台模式运行

到目前为止一切顺利，但你的示例应用程序是一个 Web 服务器，你无需让终端一直连接到容器。Docker 可以在后台以分离模式运行你的容器。为此，你可以使用 `--detach` 或简写 `-d`。Docker 将像以前一样启动你的容器，但这次会与容器分离，并将你返回到终端提示符。

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker 在后台启动了你的容器，并在终端上打印了容器 ID。

再次确保你的容器正在运行。运行相同的 `curl` 命令：

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

## 列出容器

由于你在后台运行了容器，你如何知道容器是否正在运行，或者你的机器上正在运行哪些其他容器？要查看机器上运行的容器列表，请运行 `docker ps`。这类似于在 Linux 机器上使用 `ps` 命令查看进程列表。

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

`ps` 命令会告诉你很多关于正在运行的容器的信息。你可以看到容器 ID、容器内运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口以及容器的名称。

你可能想知道容器的名称从何而来。由于你在启动容器时没有提供名称，Docker 生成了一个随机名称。你稍后会解决这个问题，但首先需要停止容器。要停止容器，请运行 `docker stop` 命令，并传递容器的名称或 ID。

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在重新运行 `docker ps` 命令以查看正在运行的容器列表。

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## 停止、启动和命名容器

Docker 容器可以启动、停止和重启。当你停止容器时，它不会被移除，但状态会变为已停止，容器内的进程也会停止。当你运行 `docker ps` 命令时，默认输出仅显示正在运行的容器。如果你传递 `--all` 或简写 `-a`，你将看到系统上的所有容器，包括已停止和正在运行的容器。

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

如果你一直在跟着操作，你应该会看到列出了几个容器。这些是你启动和停止但尚未移除的容器。

重启你刚刚停止的容器。找到容器的名称，并在以下 `restart` 命令中替换为你的容器名称：

```console
$ docker restart inspiring_ishizaka
```

现在，使用 `ps` 命令再次列出所有容器：

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

注意，你刚刚重启的容器已在分离模式下启动，并且暴露了 `8080` 端口。另外，请注意容器的状态是 `Up X seconds`。当你重启容器时，它将使用最初启动时的相同标志或命令启动。

停止并移除所有容器，然后解决随机命名问题。

停止你刚刚启动的容器。找到你正在运行的容器的名称，并在以下命令中替换为你系统上的容器名称：

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

现在你所有的容器都已停止，将它们移除。当容器被移除时，它不再运行，也不再处于停止状态。相反，容器内的进程被终止，容器的元数据被移除。

要移除容器，请运行 `docker rm` 命令并传递容器名称。你可以在一个命令中向该命令传递多个容器名称。

再次确保在以下命令中用你系统上的容器名称替换容器名称：

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

再次运行 `docker ps --all` 命令以验证所有容器都已消失。

现在，解决烦人的随机名称问题。标准做法是为容器命名，原因很简单，这样更容易识别容器中运行的内容以及它与哪个应用程序或服务相关联。就像代码中良好的变量命名约定使阅读更简单一样，为容器命名也是如此。

要为容器命名，你必须向 `run` 命令传递 `--name` 标志：

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

现在，你可以根据名称轻松识别你的容器了。

## 下一步

在本模块中，你学习了如何运行容器和发布端口。你还学习了如何管理容器的生命周期。然后你了解了为容器命名的重要性，以便更容易识别它们。在下一个模块中，你将学习如何在容器中运行数据库并将其连接到你的应用程序。