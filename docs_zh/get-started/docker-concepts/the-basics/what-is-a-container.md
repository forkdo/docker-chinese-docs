---
title: 什么是容器？
weight: 10
keywords: concepts, build, images, container, docker desktop
description: 什么是容器？本概念页面将介绍容器，并提供快速动手实践，您将在其中运行第一个容器。
aliases:
- /guides/walkthroughs/what-is-a-container/
- /guides/walkthroughs/run-a-container/
- /guides/walkthroughs/
- /get-started/run-your-own-container/
- /get-started/what-is-a-container/
- /guides/docker-concepts/the-basics/what-is-a-container/
---

{{< youtube-embed W1kWqFkiu7k >}}

## 解释

想象一下，你正在开发一个功能强大的 Web 应用，该应用有三个主要组件：一个 React 前端、一个 Python API 和一个 PostgreSQL 数据库。如果你想要在该项目上工作，你就必须安装 Node、Python 和 PostgreSQL。

如何确保你与团队中的其他开发者使用相同版本？或者是你的 CI/CD 系统？又或者是生产环境中的版本？

如何确保你的应用所需的 Python（或 Node 或数据库）版本不会受到机器上已有内容的影响？如何管理潜在的冲突？

这就需要容器了！

什么是容器？简单来说，容器是你应用程序各个组件的隔离进程。每个组件——前端 React 应用、Python API 引擎和数据库——都在自己的隔离环境中运行，完全与机器上的其他内容隔离。

它们的厉害之处在于：

- 自包含。每个容器拥有其正常运行所需的一切，不依赖于主机上的任何预安装依赖。
- 隔离。由于容器在隔离环境中运行，它们对主机和其他容器的影响力很小，从而提高应用程序的安全性。
- 独立。每个容器独立管理。删除一个容器不会影响其他容器。
- 可移植。容器可以在任何地方运行！在你的开发机器上运行的容器在数据中心或云中的任何地方都会以相同的方式运行！

### 容器与虚拟机（VM）的对比

不深入探讨的话，虚拟机包含一个完整的操作系统，有自己的内核、硬件驱动、程序和应用。仅仅为了隔离一个应用程序就启动一个虚拟机，开销很大。

容器只是一个隔离进程，附带运行所需的所有文件。如果你运行多个容器，它们共享同一个内核，使你能够在更少的基础设施上运行更多应用。

> **容器与虚拟机的结合使用**
>
> 很多时候，你会看到容器和虚拟机被一起使用。例如，在云环境中，分配的机器通常都是虚拟机。然而，不再为每个应用分配一台机器，而是在一个虚拟机上运行容器运行时，从而运行多个容器化应用，提高资源利用率并降低成本。


## 动手实践

在本操作中，你将看到如何使用 Docker Desktop 图形界面运行一个 Docker 容器。

{{< tabs group=concept-usage persist=true >}}
{{< tab name="使用图形界面" >}}

请按照以下步骤运行一个容器。

1. 打开 Docker Desktop，选择顶部导航栏上的 **Search**（搜索）字段。

2. 在搜索框中输入 `welcome-to-docker`，然后选择 **Pull**（拉取）按钮。

    ![Docker Desktop 仪表板的截图，显示 welcome-to-docker Docker 镜像的搜索结果](images/search-the-docker-image.webp?border=true&w=1000&h=700)

3. 镜像成功拉取后，选择 **Run**（运行）按钮。

4. 展开 **Optional settings**（可选设置）。

5. 在 **Container name**（容器名称）中，输入 `welcome-to-docker`。

6. 在 **Host port**（主机端口）中，输入 `8080`。

    ![Docker Desktop 仪表板的截图，显示容器运行对话框，容器名称填写为 welcome-to-docker，端口号指定为 8080](images/run-a-new-container.webp?border=true&w=550&h=400)

7. 选择 **Run** 启动容器。

恭喜！你刚刚运行了你的第一个容器！🎉
 
### 查看你的容器

你可以通过进入 Docker Desktop 仪表板的 **Containers**（容器）视图查看所有容器。

![Docker Desktop GUI 的容器视图截图，显示 welcome-to-docker 容器在主机端口 8080 上运行](images/view-your-containers.webp?border=true&w=750&h=600)

此容器运行一个 Web 服务器，显示一个简单的网站。在处理更复杂的项目时，你将在不同的容器中运行不同的部分。例如，你可能会分别为前端、后端和数据库运行不同的容器。

### 访问前端

启动容器时，你将容器的一个端口暴露到你的机器上。可以将其看作是创建配置，以便让你通过容器的隔离环境进行连接。

对于此容器，前端可通过端口 `8080` 访问。要打开网站，请在容器的 **Port(s)**（端口）列中选择链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![运行中容器的登录页面截图](images/access-the-frontend.webp?border)

### 探索你的容器

Docker Desktop 允许你探索和与容器的不同方面进行交互。亲自试试吧。

1. 进入 Docker Desktop 仪表板的 **Containers**（容器）视图。

2. 选择你的容器。

3. 选择 **Files**（文件）标签页，探索容器的隔离文件系统。

    ![Docker Desktop 仪表板的截图，显示运行中容器内的文件和目录](images/explore-your-container.webp?border)

### 停止你的容器

`docker/welcome-to-docker` 容器将持续运行，直到你停止它。

1. 进入 Docker Desktop 仪表板的 **Containers**（容器）视图。

2. 找到你想要停止的容器。

3. 在 **Actions**（操作）列中选择 **Stop**（停止）操作。

    ![Docker Desktop 仪表板的截图，显示欢迎容器被选中并准备停止](images/stop-your-container.webp?border)

{{< /tab >}}
{{< tab name="使用命令行" >}}

请按照以下步骤使用命令行运行容器：

1. 打开你的命令行终端，使用 [`docker run`](/reference/cli/docker/container/run/) 命令启动一个容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    该命令的输出是完整的容器 ID。

恭喜！你刚刚启动了你的第一个容器！🎉

### 查看正在运行的容器

你可以使用 [`docker ps`](/reference/cli/docker/container/ls/) 命令验证容器是否在运行：

```console
docker ps
```

你将看到如下输出：

```console
 CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
 a1f7a4bb3a27   docker/welcome-to-docker   "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8080->80/tcp       gracious_keldysh
```

此容器运行一个 Web 服务器，显示一个简单的网站。在处理更复杂的项目时，你将在不同的容器中运行不同的部分。例如，分别为 `frontend`（前端）、`backend`（后端）和 `database`（数据库）运行不同的容器。

> [!TIP]
>
> `docker ps` 命令只会显示正在运行的容器。要查看已停止的容器，请添加 `-a` 标志以列出所有容器：`docker ps -a`


### 访问前端

启动容器时，你将容器的一个端口暴露到你的机器上。可以将其看作是创建配置，以便让你通过容器的隔离环境进行连接。

对于此容器，前端可通过端口 `8080` 访问。要打开网站，请在容器的 **Port(s)**（端口）列中选择链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![Nginx Web 服务器登录页面的截图，来自运行中的容器](images/access-the-frontend.webp?border)

### 停止你的容器

`docker/welcome-to-docker` 容器将持续运行，直到你停止它。你可以使用 `docker stop` 命令停止容器。

1. 运行 `docker ps` 获取容器的 ID

2. 将容器的 ID 或名称提供给 [`docker stop`](/reference/cli/docker/container/stop/) 命令：

    ```console
    docker stop <the-container-id>
    ```

> [!TIP]
>
> 在通过 ID 引用容器时，不需要提供完整的 ID。只要提供足够的 ID 以使其唯一即可。例如，可以通过运行以下命令停止之前提到的容器：
>
> ```console
> docker stop a1f
> ```

{{< /tab >}}
{{< /tabs >}}

## 额外资源

以下链接提供有关容器的更多指导：

- [运行一个容器](/engine/containers/run/)
- [容器概述](https://www.docker.com/resources/what-container/)
- [为什么选择 Docker？](https://www.docker.com/why-docker/)

## 下一步

既然你已经了解了 Docker 容器的基础知识，现在是时候学习 Docker 镜像了。

{{< button text="什么是镜像？" url="what-is-an-image" >}}