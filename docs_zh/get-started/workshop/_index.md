---
title: Docker 工作坊概述
linkTitle: Docker 工作坊
keywords: docker 基础知识, 如何启动 docker 容器, 容器设置, 安装 docker, 如何安装 docker, docker 安装, docker 容器指南, 如何开始使用 docker
description: 通过这个工作坊开始学习 Docker 基础知识。你将学习容器、镜像，以及如何将你的第一个应用程序容器化。
aliases:
- /guides/get-started/
- /get-started/hands-on-overview/
- /guides/workshop/
---

这个 45 分钟的工作坊包含开始使用 Docker 的分步说明。你将学习如何：

- 构建并运行一个作为容器的镜像。
- 使用 Docker Hub 共享镜像。
- 使用包含数据库的多个容器部署 Docker 应用程序。
- 使用 Docker Compose 运行应用程序。

> [!NOTE]
>
> 如需对 Docker 和容器化应用程序的优势进行快速介绍，请参阅[入门指南](/get-started/introduction/_index.md)。

## 什么是容器？

容器是在主机上运行的沙盒进程，与其他在该主机上运行的所有进程隔离。这种隔离利用了 [内核命名空间和 cgroups](https://medium.com/@saschagrunert/demystifying-containers-part-i-kernel-space-2c53d6979504)，
这些功能在 Linux 中已存在很长时间。Docker 让这些功能变得易于理解和使用。总结来说，容器：

- 是镜像的可运行实例。你可以使用 Docker API 或 CLI 创建、启动、停止、移动或删除容器。
- 可以在本地机器、虚拟机或云环境中运行。
- 具有可移植性（可以在任何操作系统上运行）。
- 与其他容器隔离，运行自己的软件、二进制文件、配置等。

如果你熟悉 `chroot`，那么可以把容器看作是 `chroot` 的扩展版本。文件系统来自镜像，但容器增加了 `chroot` 所不具备的额外隔离功能。

## 什么是镜像？

运行中的容器使用隔离的文件系统。这个隔离的文件系统由镜像提供，镜像必须包含运行应用程序所需的一切——所有依赖项、配置、脚本、二进制文件等。镜像还包含容器的其他配置，例如环境变量、默认运行命令以及其他元数据。

## 后续步骤

在本节中，你了解了容器和镜像。

接下来，你将把一个简单应用程序容器化，并亲自动手实践这些概念。

{{< button text="容器化应用程序" url="02_our_app.md" >}}