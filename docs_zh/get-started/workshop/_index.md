---
title: Docker 工作坊概览
linkTitle: Docker 工作坊
keywords: docker basics, how to start a docker container, container settings, setup
  docker, how to setup docker, setting up docker, docker container guide, how to get
  started with docker
description: 在本工作坊中学习 Docker 基础知识。你将了解容器、镜像，以及如何将你的第一个应用容器化。
aliases:
- /guides/get-started/
- /get-started/hands-on-overview/
- /guides/workshop/
---

这个 45 分钟的工作坊包含分步指导，帮助你开始使用 Docker。本工作坊将向你展示如何：

- 构建镜像并将其作为容器运行。
- 使用 Docker Hub 共享镜像。
- 使用包含数据库的多个容器部署 Docker 应用。
- 使用 Docker Compose 运行应用。

> [!NOTE]
>
> 如需快速了解 Docker 以及将应用容器化的优势，请参阅 [入门指南](/get-started/introduction/_index.md)。

## 什么是容器？

容器是在主机上运行的沙盒化进程，与主机上运行的所有其他进程隔离。这种隔离利用了 [内核命名空间和 cgroups](https://medium.com/@saschagrunert/demystifying-containers-part-i-kernel-space-2c53d6979504)，这些是 Linux 长期以来一直具备的功能。Docker 让这些能力变得易于访问和使用。简而言之，容器：

- 是镜像的可运行实例。你可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。
- 可在本地机器、虚拟机上运行，或部署到云端。
- 是可移植的（可在任何操作系统上运行）。
- 与其他容器隔离，并运行自己的软件、二进制文件、配置等。

如果你熟悉 `chroot`，可以将容器视为 `chroot` 的扩展版本。文件系统来自镜像。然而，容器提供了使用 chroot 时无法获得的额外隔离。

## 什么是镜像？

运行的容器使用一个隔离的文件系统。这个隔离的文件系统由镜像提供，镜像必须包含运行应用所需的一切——所有依赖项、配置、脚本、二进制文件等。镜像还包含容器的其他配置，例如环境变量、默认运行的命令以及其他元数据。

## 下一步

在本节中，你学习了容器和镜像的相关知识。

接下来，你将容器化一个简单的应用，并动手实践这些概念。

{{< button text="容器化一个应用" url="02_our_app.md" >}}