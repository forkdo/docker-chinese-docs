---
title: 关于 Docker Offload
linktitle: 关于
weight: 15
description: 了解 Docker Offload 的功能和工作原理。
keywords: cloud, offload, vdi
---

Docker Offload 是一项完全托管的服务，用于在云端构建和运行容器，使用您已熟悉的 Docker 工具，包括 Docker Desktop、Docker CLI 和 Docker Compose。它将您的本地开发工作流扩展到一个可扩展、由云驱动的环境，使开发者即使在虚拟桌面基础架构（VDI）环境或不支持嵌套虚拟化的系统中也能高效工作。



## 主要功能

Docker Offload 包含以下功能，以支持现代容器工作流：

- 临时云运行器：为每个容器会话自动配置和拆除云环境。
- 混合工作流：使用 Docker Desktop 或 CLI 无缝切换本地和远程执行。
- 安全通信：在 Docker Desktop 和云环境之间使用加密隧道，支持安全密钥和镜像拉取。
- 端口转发和绑定挂载：即使容器在云端运行，也能保持本地开发体验。
- VDI 友好：在虚拟桌面环境或不支持嵌套虚拟化的系统中[使用 Docker Desktop](../desktop/setup/vm-vdi.md)。

## 为什么使用 Docker Offload？

Docker Offload 旨在支持在本地和云环境中工作的现代开发团队。它帮助您：

- 将繁重的构建和运行任务卸载到快速、可扩展的基础设施
- 运行超出本地设置资源限制的容器
- 使用 Docker Compose 管理需要云资源的复杂多服务应用
- 在不管理自定义基础设施的情况下保持一致的环境
- 在受限或低功耗环境中（如 VDI）高效开发

Docker Offload 适用于需要云灵活性而不牺牲本地工具简单性的高效率开发工作流。

## Docker Offload 如何工作

Docker Offload 通过将 Docker Desktop 连接到安全、专用的云资源，消除了在本地构建或运行容器的需求。

### 使用 Docker Offload 运行容器

当您使用 Docker Offload 构建或运行容器时，Docker Desktop 会创建一个安全的 SSH 隧道连接到云端运行的 Docker 守护进程。您的容器完全在该远程环境中启动和管理。

以下是工作流程：

1. Docker Desktop 连接到云端并触发容器创建。
2. Docker Offload 在云端构建或拉取所需镜像并启动容器。
3. 容器运行期间，连接保持打开状态。
4. 容器停止后，环境自动关闭并清理。

这种设置避免了在本地运行容器的开销，即使在低功耗机器（包括不支持嵌套虚拟化的机器）上也能实现快速、可靠的容器。这使得 Docker Offload 成为在虚拟桌面、云托管开发机或旧硬件等环境中工作的开发者的理想选择。

尽管在远程运行，绑定挂载和端口转发等功能仍能无缝工作，通过 Docker Desktop 和 CLI 提供类似本地的体验。

Docker Offload 根据使用情况自动在活跃和空闲状态之间切换。您仅在活跃构建或运行容器时被计费。空闲超过 5 分钟后，会话结束，资源被清理。有关详细信息和空闲超时配置，请参阅 [活跃和空闲状态](configuration.md#understand-active-and-idle-states)。

## 下一步

通过阅读 [Docker Offload 快速开始](/offload/quickstart/) 亲身体验 Docker Offload。