# Docker 工作坊概览

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


<a class="button not-prose" href="https://docs.docker.com/get-started/workshop/02_our_app/">容器化一个应用</a>


- [容器化应用程序](https://docs.docker.com/get-started/workshop/02_our_app/)

- [更新应用程序](https://docs.docker.com/get-started/workshop/03_updating_app/)

- [共享应用程序](https://docs.docker.com/get-started/workshop/04_sharing_app/)

- [持久化数据库](https://docs.docker.com/get-started/workshop/05_persisting_data/)

- [使用 bind mounts](https://docs.docker.com/get-started/workshop/06_bind_mounts/)

- [多容器应用](https://docs.docker.com/get-started/workshop/07_multi_container/)

- [使用 Docker Compose](https://docs.docker.com/get-started/workshop/08_using_compose/)

- [镜像构建最佳实践](https://docs.docker.com/get-started/workshop/09_image_best/)

- [Docker 工作坊之后该做什么](https://docs.docker.com/get-started/workshop/10_what_next/)

