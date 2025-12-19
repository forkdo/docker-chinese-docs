---
title: 关于 Docker Offload
linktitle: 关于
weight: 15
description: 了解 Docker Offload、其功能及工作原理。
keywords: cloud, offload, vdi
---

Docker Offload 是一项完全托管的服务，用于使用您已熟悉的 Docker 工具（包括 Docker Desktop、Docker CLI 和 Docker Compose）在云端构建和运行容器。它将您的本地开发工作流扩展到可扩展的、由云驱动的环境中，使开发者即使在虚拟桌面基础设施 (VDI) 环境或不支持嵌套虚拟化的系统中也能高效工作。

## 主要功能

Docker Offload 包含以下功能，以支持现代容器工作流：

- 临时云运行器：为每个容器会话自动配置和拆除云环境。
- 混合工作流：使用 Docker Desktop 或 CLI 在本地和远程执行之间无缝切换。
- 安全通信：使用 Docker Desktop 与云环境之间的加密隧道，并支持安全的 secrets 和镜像拉取。
- 端口转发和绑定挂载：即使在云端运行容器，也能保留本地开发体验。
- VDI 友好：在虚拟桌面环境或不支持嵌套虚拟化的系统中[使用 Docker Desktop](../desktop/setup/vm-vdi.md)。

## 为何使用 Docker Offload？

Docker Offload 旨在支持在本地和云环境中工作的现代开发团队。它帮助您：

- 将繁重的构建和运行任务卸载到快速、可扩展的基础设施上。
- 运行需要比本地设置更多资源的容器。
- 使用 Docker Compose 管理需要云资源的复杂多服务应用。
- 无需管理自定义基础设施即可保持环境一致。
- 在受限或低性能环境（如 VDI）中高效开发。

Docker Offload 非常适合需要云的灵活性又不牺牲本地工具简单性的高速开发工作流。

## Docker Offload 工作原理

Docker Offload 通过将 Docker Desktop 连接到安全、专用的云资源，取代了在本地构建或运行容器的需求。

### 使用 Docker Offload 运行容器

当您使用 Docker Offload 构建或运行容器时，Docker Desktop 会创建一条安全的 SSH 隧道连接到在云端运行的 Docker 守护进程。您的容器完全在该远程环境中启动和管理。

过程如下：

1. Docker Desktop 连接到云端并触发容器创建。
2. Docker Offload 构建或拉取所需的镜像，并在云端启动容器。
3. 连接在容器运行期间保持打开状态。
4. 当容器停止运行时，环境会自动关闭并清理。

这种设置避免了在本地运行容器的开销，即使在低性能机器（包括不支持嵌套虚拟化的机器）上也能实现快速、可靠的容器运行。这使得 Docker Offload 成为使用虚拟桌面、云托管开发机器或旧硬件等环境的开发者的理想选择。

尽管是远程运行，绑定挂载和端口转发等功能仍能无缝工作，在 Docker Desktop 和 CLI 中提供类似本地的体验。

Docker Offload 会根据使用情况在活动和空闲状态之间自动转换。仅在主动构建或运行容器时才会计费。当空闲超过 5 分钟时，会话将结束并清理资源。有关此工作原理及如何配置空闲超时的详细信息，请参阅[活动和空闲状态](configuration.md#understand-active-and-idle-states)。

## 下一步

通过 [Docker Offload 快速入门](/offload/quickstart/)开始动手实践 Docker Offload。