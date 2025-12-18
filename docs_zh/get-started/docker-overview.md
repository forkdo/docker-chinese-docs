---
description: 了解 Docker 平台的深入概述，包括它的用途、采用的架构以及底层技术。
keywords: 什么是 docker、docker 守护进程、为什么使用 docker、docker 架构、docker 的用途、docker 客户端、docker 容器的用途、为什么使用 docker、docker 的用途、docker 容器的用途
title: 什么是 Docker？
weight: 20
aliases:
 - /introduction/understanding-docker/
 - /engine/userguide/basics/
 - /engine/introduction/understanding-docker/
 - /engine/understanding-docker/
 - /engine/docker-overview/
 - /get-started/overview/
 - /guides/docker-overview/
---

Docker 是一个用于开发、分发和运行应用程序的开放平台。Docker 使你能够将应用程序与基础设施分离，从而快速交付软件。使用 Docker，你可以像管理应用程序一样管理你的基础设施。通过利用 Docker 的代码分发、测试和部署方法，你可以显著减少编写代码和在生产环境中运行代码之间的延迟。

## Docker 平台

Docker 提供了将应用程序打包并在一个称为容器的松散隔离环境中运行的能力。这种隔离和安全性使你可以在给定的主机上同时运行许多容器。容器是轻量级的，包含运行应用程序所需的一切，因此你不需要依赖主机上已安装的内容。你可以在工作时共享容器，并确保与你共享的每个人都能获得以相同方式运行的相同容器。

Docker 提供了工具和平台来管理容器的生命周期：

* 使用容器开发你的应用程序及其支持组件。
* 容器成为分发和测试你的应用程序的单元。
* 当你准备就绪时，将你的应用程序作为容器或编排服务部署到生产环境中。无论你的生产环境是本地数据中心、云提供商，还是两者的混合，这都同样适用。

## 我可以用 Docker 做什么？

### 快速、一致地交付你的应用程序

Docker 通过允许开发者使用提供你的应用程序和服务的本地容器，在标准化环境中工作，从而简化了开发周期。容器非常适合持续集成和持续交付（CI/CD）工作流。

考虑以下示例场景：

- 你的开发者在本地编写代码，并使用 Docker 容器与同事共享他们的工作。
- 他们使用 Docker 将应用程序推送到测试环境，并运行自动化和手动测试。
- 当开发者发现错误时，他们可以在开发环境中修复，并重新部署到测试环境进行测试和验证。
- 测试完成后，将修复推送到客户环境就像将更新的镜像推送到生产环境一样简单。

### 响应式部署和扩展

Docker 的基于容器的平台支持高度可移植的工作负载。Docker 容器可以在开发者的本地笔记本电脑上运行，也可以在数据中心的物理或虚拟机上、云提供商上，或在混合环境中运行。

Docker 的可移植性和轻量级特性也使其易于动态管理工作负载，根据业务需求近乎实时地扩展或缩减应用程序和服务。

### 在相同硬件上运行更多工作负载

Docker 轻量且快速。它为基于虚拟机管理器的虚拟机提供了可行且具有成本效益的替代方案，因此你可以利用更多的服务器容量来实现你的业务目标。Docker 非常适合高密度环境，以及需要以较少资源完成更多任务的小型和中型部署。

## Docker 架构

Docker 使用客户端-服务器架构。Docker 客户端与 Docker 守护进程通信，后者负责构建、运行和分发你的 Docker 容器。Docker 客户端和守护进程可以在同一系统上运行，或者你可以将 Docker 客户端连接到远程 Docker 守护进程。Docker 客户端和守护进程使用 REST API 通过 UNIX 套接字或网络接口进行通信。另一个 Docker 客户端是 Docker Compose，它可以让你处理由一组容器组成的应用程序。

![Docker 架构图](images/docker-architecture.webp)

### Docker 守护进程

Docker 守护进程（`dockerd`）监听 Docker API 请求并管理 Docker 对象，如镜像、容器、网络和卷。守护进程还可以与其他守护进程通信以管理 Docker 服务。

### Docker 客户端

Docker 客户端（`docker`）是许多 Docker 用户与 Docker 交互的主要方式。当你使用 `docker run` 等命令时，客户端会将这些命令发送给 `dockerd`，由它执行。`docker` 命令使用 Docker API。Docker 客户端可以与多个守护进程通信。

### Docker Desktop

Docker Desktop 是一个易于安装的应用程序，适用于你的 Mac、Windows 或 Linux 环境，使你能够构建和共享容器化应用程序和微服务。Docker Desktop 包括 Docker 守护进程（`dockerd`）、Docker 客户端（`docker`）、Docker Compose、Docker Content Trust、Kubernetes 和 Credential Helper。有关更多信息，请参阅 [Docker Desktop](/manuals/desktop/_index.md)。

### Docker 注册表

Docker 注册表存储 Docker 镜像。Docker Hub 是一个公共注册表，任何人都可以使用，Docker 默认会在 Docker Hub 上查找镜像。你甚至可以运行自己的私有注册表。

当你使用 `docker pull` 或 `docker run` 命令时，Docker 会从你配置的注册表中拉取所需的镜像。当你使用 `docker push` 命令时，Docker 会将你的镜像推送到你配置的注册表。

### Docker 对象

使用 Docker 时，你会创建和使用镜像、容器、网络、卷、插件和其他对象。本节是对其中一些对象的简要概述。

#### 镜像

镜像是创建 Docker 容器的只读模板，包含创建指令。通常，一个镜像是基于另一个镜像，并添加了一些自定义。例如，你可以构建一个基于 Ubuntu 镜像但包含 Apache Web 服务器和你的应用程序，以及使你的应用程序运行所需的配置详细信息的镜像。

你可以创建自己的镜像，也可以仅使用他人创建并发布在注册表中的镜像。要构建自己的镜像，你需要创建一个 Dockerfile，使用简单的语法定义创建镜像和运行它所需的步骤。Dockerfile 中的每条指令都会在镜像中创建一个层。当你更改 Dockerfile 并重新构建镜像时，只有那些已更改的层会被重建。这是使镜像相比其他虚拟化技术如此轻量、小巧和快速的部分原因。

#### 容器

容器是镜像的可运行实例。你可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。你可以将容器连接到一个或多个网络，附加存储，甚至基于其当前状态创建新镜像。

默认情况下，容器与其他容器和其主机相对隔离。你可以控制容器的网络、存储或其他底层子系统与其他容器或主机的隔离程度。

容器由其镜像以及你在创建或启动时提供的任何配置选项定义。当容器被移除时，对其状态的更改如果不存储在持久存储中，就会消失。

##### 示例 `docker run` 命令

以下命令运行一个 `ubuntu` 容器，交互式地附加到你的本地命令行会话，并运行 `/bin/bash`。

```console
$ docker run -i -t ubuntu /bin/bash
```

运行此命令时，会发生以下情况（假设你使用默认注册表配置）：

1.  如果你的本地没有 `ubuntu` 镜像，Docker 会从你配置的注册表中拉取它，就像你手动运行了 `docker pull ubuntu` 一样。

2.  Docker 创建一个新容器，就像你手动运行了 `docker container create` 命令一样。

3.  Docker 为容器分配一个读写文件系统，作为其最后一层。这允许运行中的容器在其本地文件系统中创建或修改文件和目录。

4.  Docker 创建一个网络接口将容器连接到默认网络，因为你没有指定任何网络选项。这包括为容器分配一个 IP 地址。默认情况下，容器可以使用主机的网络连接连接到外部网络。

5.  Docker 启动容器并执行 `/bin/bash`。由于容器以交互方式运行并附加到你的终端（由于 `-i` 和 `-t` 标志），你可以使用键盘提供输入，同时 Docker 将输出记录到你的终端。

6.  当你运行 `exit` 终止 `/bin/bash` 命令时，容器停止但不会被移除。你可以重新启动它或将其移除。

## 底层技术

Docker 使用 [Go 编程语言](https://golang.org/)编写，并利用 Linux 内核的多个特性来提供其功能。Docker 使用一种称为 `namespaces` 的技术来提供称为容器的隔离工作空间。当你运行容器时，Docker 会为该容器创建一组命名空间。

这些命名空间提供了一层隔离。容器的每个方面都在单独的命名空间中运行，其访问权限被限制在该命名空间内。

## 下一步

- [安装 Docker](/get-started/get-docker.md)
- [开始使用 Docker](/get-started/introduction/_index.md)