---
title: Docker Engine
url: /engine/
parent:
  title: 手册
  url: /manuals/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Engine
    url: /engine/
children:
  - title: 安装 Docker Engine
    url: /engine/install/
    description: 了解如何选择最适合您的 Docker Engine 安装方法。这个客户端-服务器应用程序可在 Linux、Mac、Windows 上使用，也可作为静态二进制文件使用。
  - title: 存储
    url: /engine/storage/
    description: 容器中持久化数据的概述
  - title: 网络概述
    url: /engine/network/
    description: 从容器的角度了解网络工作原理
  - title: Docker 守护进程配置概述
    url: /engine/daemon/
    description: 配置 Docker 守护进程
  - title: 查看容器日志
    url: /engine/logging/
    description: 了解如何写入、查看和配置容器的日志
  - title: Swarm 模式
    url: /engine/swarm/
    description: Docker Engine Swarm 模式概述
  - title: Docker Engine 安全
    url: /engine/security/
    description: Docker 守护进程攻击面综述
  - title: Deprecated Docker Engine features
    url: /engine/deprecated/
    description: Deprecated Features.
  - title: Docker Engine managed plugin system
    url: /engine/extend/
    description: Develop and use a plugin with the managed plugin system
---


Docker Engine 是一种开源容器化技术，用于构建和容器化您的应用程序。Docker Engine 作为一个客户端-服务器应用程序运行，包含：

- 一个长期运行的守护进程 [`dockerd`](/reference/cli/dockerd) 的服务器
- 定义程序可用于与 Docker 守护进程通信和指示其操作的接口的 API
- 一个命令行界面（CLI）客户端 [`docker`](/reference/cli/docker/)

CLI 使用 [Docker API](/reference/api/engine/_index.md) 通过脚本或直接 CLI 命令来控制或与 Docker 守护进程交互。许多其他 Docker 应用程序使用底层的 API 和 CLI。守护进程创建和管理 Docker 对象，例如镜像、容器、网络和卷。

有关更多详细信息，请参阅 [Docker 架构](/get-started/docker-overview.md#docker-architecture)。



## 许可

在大型企业（员工超过 250 人或年收入超过 1000 万美元）中通过 Docker Desktop 获得的 Docker Engine 的商业使用，需要[付费订阅](https://www.docker.com/pricing/)。Apache 许可证 2.0 版。完整许可证请参见 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。
