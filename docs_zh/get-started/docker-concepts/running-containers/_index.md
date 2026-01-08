---
build:
  render: never
title: 运行容器
weight: 30
---

# 运行容器

在本教程中，我们将使用 Docker 运行一个简单的容器。我们将使用 `docker run` 命令来启动一个容器，并查看其输出。

## 前提条件

在开始之前，请确保您已经安装了 Docker。您可以通过运行以下命令来检查 Docker 是否已安装：

```bash
docker --version
```

如果您还没有安装 Docker，请访问 [Docker 官方网站](https://www.docker.com/) 获取安装说明。

## 运行一个简单的容器

我们将从运行一个简单的 `hello-world` 容器开始。这个容器会输出一条欢迎消息，然后退出。

运行以下命令：

```bash
docker run hello-world
```

您应该会看到类似以下的输出：

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, visit https://docs.docker.com/get-started/.

Visit https://docs.docker.com/engine/userguide/ to learn about containers and images.
```

## 运行一个交互式容器

现在，让我们运行一个交互式容器。我们将使用 `ubuntu` 镜像，并在容器内启动一个 bash shell。

运行以下命令：

```bash
docker run -it ubuntu bash
```

这个命令会启动一个新的容器，并在容器内打开一个 bash shell。您现在可以在容器内执行命令，就像在普通的 Ubuntu 系统中一样。

要退出容器，只需在 bash 提示符下输入 `exit`。

## 运行一个后台容器

如果您想在后台运行一个容器，可以使用 `-d` 选项。让我们运行一个简单的 web 服务器。

首先，我们需要一个 web 服务器镜像。我们将使用 `nginx` 镜像。

运行以下命令：

```bash
docker run -d -p 8080:80 nginx
```

这个命令会启动一个后台容器，并将容器的 80 端口映射到主机的 8080 端口。您可以在浏览器中访问 `http://localhost:8080` 来查看 Nginx 的默认页面。

## 查看正在运行的容器

要查看当前正在运行的容器，可以使用 `docker ps` 命令：

```bash
docker ps
```

如果您想查看所有容器（包括已停止的），可以使用 `docker ps -a` 命令：

```bash
docker ps -a
```

## 停止和删除容器

要停止一个正在运行的容器，首先需要获取容器的 ID 或名称。使用 `docker ps` 命令查看正在运行的容器：

```bash
docker ps
```

然后使用 `docker stop` 命令停止容器：

```bash
docker stop <container_id_or_name>
```

要删除一个容器，使用 `docker rm` 命令：

```bash
docker rm <container_id_or_name>
```

如果您想停止并删除所有容器，可以使用以下命令：

```bash
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
```

## 总结

在本教程中，您学习了如何：
- 运行一个简单的容器
- 运行一个交互式容器
- 运行一个后台容器
- 查看正在运行的容器
- 停止和删除容器

现在您已经掌握了 Docker 容器的基本操作，可以继续探索更高级的 Docker 功能，如镜像管理、网络配置和数据卷管理。