# 以容器方式运行你的 Rust 镜像

## 前置条件

你已完成 [构建你的 Rust 镜像](build-images.md) 并已构建出镜像。

## 概述

容器是一个普通的操作系统进程，但 Docker 会隔离该进程，使其拥有自己的文件系统、自己的网络以及与主机分离的独立进程树。

要在容器中运行镜像，你需要使用 `docker run` 命令。`docker run` 命令需要一个参数，即镜像的名称。

## 运行镜像

使用 `docker run` 运行你在 [构建你的 Rust 镜像](build-images.md) 中构建的镜像。

```console
$ docker run docker-rust-image
```

运行此命令后，你会注意到你没有回到命令提示符。这是因为你的应用程序是一个服务器，它在循环中运行，等待传入的请求，直到你停止容器才会将控制权交还给操作系统。

打开一个新终端，然后使用 `curl` 命令向服务器发出请求。

```console
$ curl http://localhost:8000
```

你应该看到如下输出。

```console
curl: (7) Failed to connect to localhost port 8000 after 2236 ms: Couldn't connect to server
```

如你所见，你的 `curl` 命令失败了。这意味着你无法连接到本地主机的 8000 端口。这是正常的，因为你的容器是隔离运行的，包括网络。停止容器并以 8000 端口发布到本地网络的方式重新启动。

要停止容器，按 ctrl-c。这将让你回到终端提示符。

要在容器上发布端口，你需要在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式是 `[host port]:[container port]`。因此，如果你想将容器内的 8000 端口暴露到容器外的 3001 端口，你需要向 `--publish` 标志传递 `3001:8000`。

你在容器中运行应用程序时没有指定端口，默认端口是 8000。如果你想让之前请求 8000 端口的命令生效，你可以将主机的 3001 端口映射到容器的 8000 端口：

```console
$ docker run --publish 3001:8000 docker-rust-image
```

现在，重新运行 curl 命令。记得打开一个新终端。

```console
$ curl http://localhost:3001
```

你应该看到如下输出。

```console
Hello, Docker!
```

成功！你已成功连接到在容器内 8000 端口运行的应用程序。切换回容器运行的终端并停止它。

按 ctrl-c 停止容器。

## 以分离模式运行

到目前为止这很好，但你的示例应用程序是一个 Web 服务器，你不需要连接到容器。Docker 可以让你的容器以分离模式或后台模式运行。为此，你可以使用 `--detach` 标志，简写为 `-d`。Docker 会像之前一样启动你的容器，但这次会从容器“分离”并让你回到终端提示符。

```console
$ docker run -d -p 3001:8000 docker-rust-image
ce02b3179f0f10085db9edfccd731101868f58631bdf918ca490ff6fd223a93b
```

Docker 在后台启动了你的容器并在终端打印了容器 ID。

再次确保你的容器正常运行。重新运行 curl 命令。

```console
$ curl http://localhost:3001
```

你应该看到如下输出。

```console
Hello, Docker!
```

## 列出容器

由于你在后台运行了容器，你怎么知道容器是否在运行，或者你的机器上还有哪些其他容器在运行？要查看机器上运行的容器列表，运行 `docker ps`。这类似于在 Linux 中使用 ps 命令查看进程列表。

你应该看到如下输出。

```console
CONTAINER ID   IMAGE                   COMMAND         CREATED         STATUS         PORTS                    NAMES
3074745e412c   docker-rust-image       "/bin/server"   8 seconds ago   Up 7 seconds   0.0.0.0:3001->8000/tcp   wonderful_kalam
```

`docker ps` 命令提供了关于你运行的容器的大量信息。你可以看到容器 ID、容器内运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口以及容器名称。

你可能想知道容器名称是从哪里来的。由于你在启动容器时没有提供名称，Docker 生成了一个随机名称。你很快会修复这个问题，但首先需要停止容器。要停止容器，运行 `docker stop` 命令，它会停止容器。你需要传递容器名称，或者可以使用容器 ID。

```console
$ docker stop wonderful_kalam
wonderful_kalam
```

现在，重新运行 `docker ps` 命令查看运行中的容器列表。

```console
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

## 停止、启动和命名容器

你可以启动、停止和重启 Docker 容器。当你停止容器时，它不会被删除，但状态会变为已停止，容器内的进程也会停止。当你在上一模块运行 `docker ps` 命令时，默认输出只显示运行中的容器。当你传递 `--all` 或简写 `-a` 时，你会看到机器上的所有容器，无论其启动或停止状态如何。

```console
$ docker ps -a
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                      PORTS
     NAMES
3074745e412c   docker-rust-image       "/bin/server"            3 minutes ago    Exited (0) 6 seconds ago
     wonderful_kalam
6cfa26e2e3c9   docker-rust-image       "/bin/server"            14 minutes ago   Exited (0) 5 minutes ago
     friendly_montalcini
4cbe94b2ea0e   docker-rust-image       "/bin/server"            15 minutes ago   Exited (0) 14 minutes ago
     tender_bose
```

现在你应该看到列出了几个容器。这些是你启动并停止的容器，但你还没有删除它们。

重启你刚停止的容器。找到你刚停止的容器的名称，并在以下重启命令中替换容器名称。

```console
$ docker restart wonderful_kalam
```

现在再次使用 `docker ps` 命令列出所有容器。

```console
$ docker ps --all
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS                      PORTS
     NAMES
3074745e412c   docker-rust-image       "/bin/server"            6 minutes ago    Up 4 seconds                0.0.0.0:3001->8000/tcp           wonderful_kalam
6cfa26e2e3c9   docker-rust-image       "/bin/server"            16 minutes ago   Exited (0) 7 minutes ago
     friendly_montalcini
4cbe94b2ea0e   docker-rust-image       "/bin/server"            18 minutes ago   Exited (0) 17 minutes ago
     tender_bose
```

注意，你刚重启的容器已以分离模式启动。另外，观察容器的状态是“Up X seconds”。当你重启容器时，它会使用最初启动时的相同标志或命令启动。

现在，停止并删除你的所有容器，并查看如何修复随机命名问题。停止你刚启动的容器。找到你运行的容器的名称，并在以下命令中替换为你系统上的容器名称。

```console
$ docker stop wonderful_kalam
wonderful_kalam
```

现在你已停止所有容器，删除它们。当你删除容器时，它不再运行，也不再处于停止状态，但容器内的进程已停止，容器的元数据已被删除。

要删除容器，使用 `docker rm` 命令并传递容器名称。你可以使用单个命令传递多个容器名称。同样，在以下命令中用你系统上的容器名称替换容器名称。

```console
$ docker rm wonderful_kalam friendly_montalcini tender_bose
wonderful_kalam
friendly_montalcini
tender_bose
```

再次运行 `docker ps --all` 命令，查看 Docker 是否删除了所有容器。

现在，是时候解决随机命名问题了。标准做法是为容器命名，原因很简单，这样更容易识别容器中运行的内容以及它与哪个应用程序或服务相关联。

要命名容器，你只需要向 `docker run` 命令传递 `--name` 标志。

```console
$ docker run -d -p 3001:8000 --name docker-rust-container docker-rust-image
1aa5d46418a68705c81782a58456a4ccdb56a309cb5e6bd399478d01eaa5cdda
$ docker ps
CONTAINER ID   IMAGE                   COMMAND         CREATED         STATUS         PORTS                    NAMES
c68fa18de1f6   docker-rust-image       "/bin/server"   7 seconds ago   Up 6 seconds   0.0.0.0:3001->8000/tcp   docker-rust-container
```

好多了！现在你可以根据名称轻松识别你的容器。

## 总结

在本节中，你了解了如何运行容器。你还了解了如何通过启动、停止和重启来管理容器。最后，你了解了如何为容器命名，以便更容易识别。

相关信息：

- [docker run CLI 参考](/reference/cli/docker/container/run.md)

## 下一步

在下一节中，你将学习如何在容器中运行数据库并将其连接到 Rust 应用程序。
