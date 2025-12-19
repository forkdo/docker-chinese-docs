---
title: 什么是容器？
weight: 10
keywords: 概念, 构建, 镜像, 容器, docker desktop
description: 什么是容器？本概念页面将为您介绍容器知识，并提供一个快速实践教程，帮助您运行您的第一个容器。
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

假设您正在开发一个杀手级的 Web 应用程序，它包含三个主要组件：一个 React 前端、一个 Python API 和一个 PostgreSQL 数据库。如果您想在这个项目上工作，您必须安装 Node、Python 和 PostgreSQL。

您如何确保您的版本与团队中的其他开发人员相同？或者与您的 CI/CD 系统相同？或者与生产环境中使用的版本相同？

您如何确保应用程序所需的 Python（或 Node 或数据库）版本不受您机器上已安装内容的影响？您如何管理潜在的冲突？

容器应运而生！

什么是容器？简单来说，容器是您应用程序每个组件的隔离进程。每个组件——前端 React 应用、Python API 引擎和数据库——都在其自己的隔离环境中运行，与您机器上的其他一切完全隔离。

以下是它们的过人之处。容器是：

- **自包含的**。每个容器都拥有其运行所需的一切，不依赖于主机机器上的任何预安装依赖项。
- **隔离的**。由于容器在隔离状态下运行，它们对主机和其他容器的影响最小，从而提高了应用程序的安全性。
- **独立的**。每个容器都是独立管理的。删除一个容器不会影响任何其他容器。
- **可移植的**。容器可以在任何地方运行！在您的开发机器上运行的容器，在数据中心或云中的任何地方都能以相同的方式工作！

### 容器与虚拟机 (VM)

无需深入探讨，虚拟机 (VM) 是一个完整的操作系统，拥有自己的内核、硬件驱动程序、程序和应用程序。仅为了隔离单个应用程序而启动一个虚拟机，开销非常大。

容器只是一个隔离的进程，附带其运行所需的所有文件。如果您运行多个容器，它们都共享同一个内核，这使得您可以在更少的基础设施上运行更多的应用程序。

> **同时使用虚拟机和容器**
>
> 很常见的情况是，您会看到容器和虚拟机一起使用。例如，在云环境中，配置的机器通常是虚拟机。但是，与其配置一台机器来运行一个应用程序，不如在一个装有容器运行时的虚拟机上运行多个容器化应用程序，这样可以提高资源利用率并降低成本。


## 尝试一下

在本实践教程中，您将学习如何使用 Docker Desktop GUI 运行一个 Docker 容器。

{{< tabs group=concept-usage persist=true >}}
{{< tab name="使用 GUI" >}}

请按照以下说明运行容器。

1. 打开 Docker Desktop 并选择顶部导航栏中的 **搜索** 字段。

2. 在搜索输入框中指定 `welcome-to-docker`，然后选择 **拉取 (Pull)** 按钮。

    ![Docker Desktop 仪表板的截图，显示 welcome-to-docker 镜像的搜索结果](images/search-the-docker-image.webp?border=true&w=1000&h=700)

3. 镜像成功拉取后，选择 **运行 (Run)** 按钮。

4. 展开 **可选设置 (Optional settings)**。

5. 在 **容器名称 (Container name)** 中，指定 `welcome-to-docker`。

6. 在 **主机端口 (Host port)** 中，指定 `8080`。

    ![Docker Desktop 仪表板的截图，显示容器运行对话框，容器名称为 welcome-to-docker，端口号指定为 8080](images/run-a-new-container.webp?border=true&w=550&h=400)

7. 选择 **运行 (Run)** 以启动您的容器。

恭喜！您刚刚运行了您的第一个容器！🎉
 
### 查看您的容器

您可以通过转到 Docker Desktop 仪表板的 **容器 (Containers)** 视图来查看所有容器。

![Docker Desktop GUI 容器视图的截图，显示 welcome-to-docker 容器正在主机端口 8080 上运行](images/view-your-containers.webp?border=true&w=750&h=600)

这个容器运行一个显示简单网站的 Web 服务器。在处理更复杂的项目时，您会在不同的容器中运行不同的部分。例如，您可能会为前端、后端和数据库分别运行不同的容器。

### 访问前端

当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将其视为创建配置，以允许您通过容器的隔离环境进行连接。

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请选择容器 **端口 (Port(s))** 列中的链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![来自正在运行的容器的登录页面截图](images/access-the-frontend.webp?border)

### 探索您的容器

Docker Desktop 允许您探索容器的不同方面并与之交互。请亲自尝试一下。

1. 转到 Docker Desktop 仪表板中的 **容器 (Containers)** 视图。

2. 选择您的容器。

3. 选择 **文件 (Files)** 标签页以探索容器的隔离文件系统。

    ![Docker Desktop 仪表板的截图，显示正在运行的容器内的文件和目录](images/explore-your-container.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器会持续运行，直到您将其停止。

1. 转到 Docker Desktop 仪表板中的 **容器 (Containers)** 视图。

2. 找到您想要停止的容器。

3. 在 **操作 (Actions)** 列中选择 **停止 (Stop)** 操作。

    ![Docker Desktop 仪表板的截图，已选择 welcome 容器并准备停止](images/stop-your-container.webp?border)

{{< /tab >}}
{{< tab name="使用 CLI" >}}

请按照以下说明使用 CLI 运行容器：

1. 打开您的 CLI 终端，并使用 [`docker run`](/reference/cli/docker/container/run/) 命令启动一个容器：

    ```console
    $ docker run -d -p 8080:80 docker/welcome-to-docker
    ```

    此命令的输出是完整的容器 ID。

恭喜！您刚刚启动了您的第一个容器！🎉

### 查看正在运行的容器

您可以使用 [`docker ps`](/reference/cli/docker/container/ls/) 命令来验证容器是否已启动并正在运行：

```console
docker ps
```

您将看到类似以下的输出：

```console
 CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                      NAMES
 a1f7a4bb3a27   docker/welcome-to-docker   "/docker-entrypoint.…"   11 seconds ago   Up 11 seconds   0.0.0.0:8080->80/tcp       gracious_keldysh
```

这个容器运行一个显示简单网站的 Web 服务器。在处理更复杂的项目时，您会在不同的容器中运行不同的部分。例如，为 `frontend`、`backend` 和 `database` 分别运行不同的容器。

> [!TIP]
>
> `docker ps` 命令将仅显示*正在运行的*容器。要查看已停止的容器，请添加 `-a` 标志以列出所有容器：`docker ps -a`


### 访问前端

当您启动容器时，您将容器的一个端口暴露到了您的机器上。可以将其视为创建配置，以允许您通过容器的隔离环境进行连接。

对于此容器，前端可在端口 `8080` 上访问。要打开网站，请选择容器 **端口 (Port(s))** 列中的链接，或在浏览器中访问 [http://localhost:8080](http://localhost:8080)。

![来自正在运行的容器的 Nginx Web 服务器登录页面截图](images/access-the-frontend.webp?border)

### 停止您的容器

`docker/welcome-to-docker` 容器会持续运行，直到您将其停止。您可以使用 `docker stop` 命令来停止容器。

1. 运行 `docker ps` 以获取容器的 ID

2. 将容器 ID 或名称提供给 [`docker stop`](/reference/cli/docker/container/stop/) 命令：

    ```console
    docker stop <the-container-id>
    ```

> [!TIP]
>
> 通过 ID 引用容器时，您不需要提供完整的 ID。您只需提供足够的 ID 使其唯一即可。例如，可以通过运行以下命令来停止上一个容器：
>
> ```console
> docker stop a1f
> ```

{{< /tab >}}
{{< /tabs >}}

## 其他资源

以下链接提供了关于容器的更多指导：

- [运行容器](/engine/containers/run/)
- [容器概述](https://www.docker.com/resources/what-container/)
- [为什么选择 Docker？](https://www.docker.com/why-docker/)

## 下一步

既然您已经了解了 Docker 容器的基础知识，是时候学习 Docker 镜像了。

{{< button text="什么是镜像？" url="what-is-an-image" >}}