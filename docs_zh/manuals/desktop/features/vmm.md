---
title: Docker Desktop for Mac 的虚拟机管理器
linkTitle: Virtual Machine Manager 
keywords: virtualization software, resource allocation, mac, docker desktop, vm monitoring, vm performance, apple silicon
description: 了解 Docker Desktop for Mac 支持的多种虚拟机管理器 (VMM) 选项，包括为 Apple Silicon 设计的新 Docker VMM，提供更强的性能和效率
weight: 110
aliases:
- /desktop/vmm/
---

Docker Desktop 支持多种虚拟机管理器 (VMM) 来驱动运行容器的 Linux 虚拟机。您可以根据系统架构（Intel 或 Apple Silicon）、性能需求和功能要求选择最合适的选项。本文档概述了可用的选项。

要更改 VMM，请前往 **Settings** > **General** > **Virtual Machine Manager**。

## Docker VMM

{{< summary-bar feature_name="VMM" >}}

Docker VMM 是一个全新、专为容器优化的虚拟机管理程序。通过优化 Linux 内核和虚拟化层，Docker VMM 在常见的开发任务中提供了显著的性能提升。

Docker VMM 提供的一些关键性能提升包括：
 - 更快的 I/O 操作：使用冷缓存时，使用 `find` 遍历大型共享文件系统比使用 Apple Virtualization 框架快 2 倍。
 - 改进的缓存：使用热缓存时，性能可提升高达 25 倍，甚至超过原生 Mac 操作。

这些改进直接影响依赖频繁文件访问和整体系统响应速度进行容器化开发的开发者。Docker VMM 标志着速度上的重大飞跃，实现了更流畅的工作流程和更快的迭代周期。

> [!NOTE]
>
> Docker VMM 要求为 Docker Linux 虚拟机分配至少 4GB 内存。需要在启用 Docker VMM 之前增加内存，这可以在 **Settings** 的 **Resources** 选项卡中完成。

### 已知问题

由于 Docker VMM 仍处于 Beta 阶段，存在一些已知限制：

- Docker VMM 当前不支持 Rosetta，因此 amd64 架构的仿真速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库（如 MongoDB 和 Cassandra）在 Docker VMM 上使用 virtiofs 时可能会失败。此问题预计将在未来的版本中得到解决。

## Apple Virtualization 框架

Apple Virtualization 框架是 Mac 上管理虚拟机的稳定且成熟的选择。多年来，它一直是许多 Mac 用户的可靠选择。该框架最适合偏好经过验证、性能稳定且兼容性广泛的解决方案的开发者。

## Apple Silicon 的 QEMU（遗留）

> [!NOTE]
>
> QEMU 在 4.44 及更高版本中已被弃用。更多信息请参阅[博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/)

QEMU 是 Apple Silicon Mac 的遗留虚拟化选项，主要支持较旧的用例。

Docker 建议过渡到更新的替代方案，例如 Docker VMM 或 Apple Virtualization 框架，因为它们提供更优的性能和持续支持。特别是 Docker VMM，它提供了显著的速度改进和更高效的开发环境，是 Apple Silicon 开发者的理想选择。

注意：这与在[多平台构建](/manuals/build/building/multi-platform.md#qemu)中使用 QEMU 仿真非原生架构无关。

## Intel Mac 的 HyperKit（遗留）

> [!NOTE]
>
> HyperKit 将在未来的版本中被弃用。

HyperKit 是另一个遗留虚拟化选项，专门针对 Intel Mac。与 QEMU 类似，它仍然可用但已被弃用。Docker 建议切换到现代替代方案，以获得更好的性能并确保系统的未来兼容性。