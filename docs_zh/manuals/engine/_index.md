---
title: Docker Engine
weight: 10
description: 全面了解 Docker Engine，包括如何安装、存储细节、网络配置等内容
keywords: Engine
params:
  sidebar:
    group: 开源
grid:
- title: 安装 Docker Engine
  description: 了解如何为您的发行版安装开源 Docker Engine。
  icon: download
  link: /engine/install
- title: 存储
  description: 在 Docker 容器中使用持久化数据。
  icon: database
  link: /storage
- title: 网络
  description: 管理容器之间的网络连接。
  icon: network_node
  link: /network
- title: 容器日志
  description: 了解如何查看和读取容器日志。
  icon: text_snippet
  link: /config/containers/logging/
- title: 清理
  description: 清理未使用的资源。
  icon: content_cut
  link: /config/pruning
- title: 配置守护进程
  description: 深入了解 Docker 守护进程的配置选项。
  icon: tune
  link: /config/daemon
- title: Rootless 模式
  description: 无需 root 权限运行 Docker。
  icon: security
  link: /engine/security/rootless
- title: 已弃用功能
  description: 了解您应停止使用的 Docker Engine 功能。
  icon: folder_delete
  link: /engine/deprecated/
- title: 发行说明
  description: 阅读最新版本的发行说明。
  icon: note_add
  link: /engine/release-notes
aliases:
- /edge/
- /engine/ce-ee-node-activate/
- /engine/migration/
- /engine/misc/
- /linux/
---

Docker Engine 是一种开源容器化技术，用于构建和容器化您的应用程序。Docker Engine 作为一个客户端-服务器应用程序运行，包含：

- 一个长期运行的守护进程 [`dockerd`](/reference/cli/dockerd) 的服务器
- 定义程序可用于与 Docker 守护进程通信和指示其操作的接口的 API
- 一个命令行界面（CLI）客户端 [`docker`](/reference/cli/docker/)

CLI 使用 [Docker API](/reference/api/engine/_index.md) 通过脚本或直接 CLI 命令来控制或与 Docker 守护进程交互。许多其他 Docker 应用程序使用底层的 API 和 CLI。守护进程创建和管理 Docker 对象，例如镜像、容器、网络和卷。

有关更多详细信息，请参阅 [Docker 架构](/get-started/docker-overview.md#docker-architecture)。

{{< grid >}}

## 许可

在大型企业（员工超过 250 人或年收入超过 1000 万美元）中通过 Docker Desktop 获得的 Docker Engine 的商业使用，需要[付费订阅](https://www.docker.com/pricing/)。Apache 许可证 2.0 版。完整许可证请参见 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。