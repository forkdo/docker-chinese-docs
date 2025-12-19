---
description: 深入了解 Docker 平台，包括其用途、采用的架构以及底层技术。
keywords: what is a docker, docker daemon, why use docker, docker architecture, what to use docker for, docker client, what is docker for, why docker, uses for docker, what is docker container used for, what are docker containers used for
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

Docker 是一个用于开发、交付和运行应用程序的开放平台。
Docker 能够将应用程序与基础设施分离，从而
让你可以快速交付软件。借助 Docker，你可以
用管理应用程序的方式来管理基础设施。通过利用 Docker
交付、测试和部署代码的方法论，你可以
显著减少编写代码和在生产环境中运行代码之间的延迟。

## Docker 平台

Docker 提供了将应用程序打包并运行在一个称为容器的松散隔离
环境中的能力。隔离和安全性让你可以在给定的主机上同时运行
许多容器。容器是轻量级的，包含
运行应用程序所需的一切，因此你无需依赖主机上
已安装的内容。你可以共享容器，同时
确保与你共享的每个人都能获得以相同方式工作的相同容器。

Docker 提供了工具和平台来管理容器的生命周期：

* 使用容器开发应用程序及其支持组件。
* 容器成为分发和测试应用程序的单元。
* 当你准备好时，将应用程序部署到生产环境，
  可以作为容器或编排服务。无论你的
  生产环境是本地数据中心、云提供商，还是两者的
  混合，其工作原理都相同。

## 我可以使用 Docker 做什么？

### 快速、一致地交付你的应用程序

Docker 通过允许开发人员使用本地容器在标准化环境中工作来简化
开发生命周期，这些容器提供你的应用程序和服务。容器非常适合持续集成和持续
交付 (CI/CD) 工作流。

考虑以下示例场景：

- 你的开发人员在本地编写代码，并使用 Docker 容器与同事
  共享他们的工作。
- 他们使用 Docker 将应用程序推送到测试环境，并运行
  自动化和手动测试。
- 当开发人员发现错误时，他们可以在开发环境中修复
  错误，并重新部署到测试环境进行测试和验证。
- 当测试完成后，将修复程序交付给客户就像将
  更新的镜像推送到生产环境一样简单。

### 响应式部署和扩展

Docker 基于容器的平台允许高度可移植的工作负载。Docker
容器可以在开发人员的本地笔记本电脑、数据中心中的物理或虚拟
机器、云提供商或混合环境中运行。

Docker 的可移植性和轻量级特性还使其易于动态
管理工作负载，根据业务需求在近乎实时的时间内
扩展或缩减应用程序和服务。

### 在相同硬件上运行更多工作负载

Docker 轻量且快速。它提供了一种可行的、具有成本效益的
基于虚拟机管理程序的虚拟机替代方案，因此你可以使用更多的服务器
容量来实现业务目标。Docker 完美适用于高密度
环境以及需要利用更少资源做更多事情的中小型部署。

## Docker 架构

Docker 使用客户端-服务器架构。Docker 客户端与
Docker 守护进程通信，后者负责构建、运行和
分发 Docker 容器的繁重工作。Docker 客户端和守护进程可以
在同一系统上运行，或者你可以将 Docker 客户端连接到远程 Docker
守护进程。Docker 客户端和守护进程使用 REST API 进行通信，通过 UNIX
套接字或网络接口。另一个 Docker 客户端是 Docker Compose，
它让你可以处理由一组容器组成的应用程序。

![Docker 架构图](images/docker-architecture.webp)

### Docker 守护进程

Docker 守护进程 (`dockerd`) 监听 Docker API 请求并管理 Docker
对象，如镜像、容器、网络和卷。守护进程还可以
与其他守护进程通信以管理 Docker 服务。

### Docker 客户端

Docker 客户端 (`docker`) 是许多 Docker 用户与 Docker 交互的主要方式。
当你使用 `docker run` 等命令时，客户端会将这些命令发送给
`dockerd`，由其执行。`docker` 命令使用 Docker API。
Docker 客户端可以与多个守护进程通信。

### Docker Desktop

Docker Desktop 是一个易于安装的应用程序，适用于你的 Mac、Windows 或 Linux 环境，使你能够构建和共享容器化应用程序和微服务。Docker Desktop 包括 Docker 守护进程 (`dockerd`)、Docker 客户端 (`docker`)、Docker Compose、Docker Content Trust、Kubernetes 和 Credential Helper。有关更多信息，请参阅 [Docker Desktop](/manuals/desktop/_index.md)。

### Docker 注册中心

Docker 注册中心存储 Docker 镜像。Docker Hub 是一个
任何人都可以使用的公共注册中心，Docker 默认在
Docker Hub 上查找镜像。你甚至可以运行自己的私有注册中心。

当你使用 `docker pull` 或 `docker run` 命令时，Docker 会从你配置的注册中心拉取所需的镜像。当你使用 `docker push` 命令时，Docker 会将
你的镜像推送到你配置的注册中心。

### Docker 对象

当你使用 Docker 时，你正在创建和使用镜像、容器、网络、
卷、插件和其他对象。本节简要概述了其中一些对象。

#### 镜像

镜像是一个只读模板，包含用于创建 Docker
容器的指令。通常，一个镜像基于另一个镜像，并进行一些额外的
定制。例如，你可以构建一个基于 Ubuntu 镜像的
镜像，但包含 Apache Web 服务器和你的应用程序，以及
使你的应用程序运行所需的配置详细信息。

你可以创建自己的镜像，或者只使用其他人创建并发布在注册中心中的镜像。要构建你自己的镜像，你需要创建一个 Dockerfile，
使用简单的语法来定义创建镜像和运行
它所需的步骤。Dockerfile 中的每条指令都会在镜像中创建一个层。
当你更改 Dockerfile 并重新构建镜像时，只有那些
已更改的层才会被重新构建。这使得镜像与其他虚拟化技术相比
如此轻量、小巧和快速的部分原因。

#### 容器

容器是镜像的一个可运行实例。你可以使用 Docker API 或 CLI
创建、启动、停止、移动或删除容器。你可以将容器
连接到一个或多个网络，附加存储，甚至基于其当前状态
创建一个新镜像。

默认情况下，容器与其他容器及其主机机器
相对隔离。你可以控制容器的网络、存储或其他底层子系统
与其他容器或主机机器的隔离程度。

容器由其镜像以及你在创建或启动时提供的任何配置选项定义。当容器被移除时，其状态中未存储在持久性存储中的任何更改都会消失。

##### `docker run` 命令示例

以下命令运行一个 `ubuntu` 容器，以交互方式附加到你的
本地命令行会话，并运行 `/bin/bash`。

```console
$ docker run -i -t ubuntu /bin/bash
```

当你运行此命令时，会发生以下情况（假设你使用
默认注册中心配置）：

1.  如果你本地没有 `ubuntu` 镜像，Docker 会从你配置的注册中心拉取它，就像你手动运行了 `docker pull ubuntu` 一样。

2.  Docker 创建一个新容器，就像你手动运行了 `docker container create`
    命令一样。

3.  Docker 为容器分配一个读写文件系统，作为其最终
    层。这允许正在运行的容器在其本地文件系统中创建或修改文件和
    目录。

4.  Docker 创建一个网络接口以将容器连接到默认
    网络，因为你没有指定任何网络选项。这包括
    为容器分配 IP 地址。默认情况下，容器可以
    使用主机机器的网络连接连接到外部网络。

5.  Docker 启动容器并执行 `/bin/bash`。由于容器
    以交互方式运行并附加到你的终端（由于 `-i` 和 `-t`
    标志），你可以在 Docker 将输出记录到你的终端时使用键盘提供输入。

6.  当你运行 `exit` 来终止 `/bin/bash` 命令时，容器
    停止但不会被移除。你可以再次启动它或将其移除。

## 底层技术

Docker 用 [Go 编程语言](https://golang.org/) 编写，并利用
Linux 内核的多个特性来提供其功能。
Docker 使用一种称为 `namespaces` 的技术来提供称为容器的隔离工作区。
当你运行容器时，Docker 会为该容器创建一组
命名空间。

这些命名空间提供了一层隔离。容器的每个方面都在
单独的命名空间中运行，其访问仅限于该命名空间。

## 下一步

- [安装 Docker](/get-started/get-docker.md)
- [Docker 入门](/get-started/introduction/_index.md)