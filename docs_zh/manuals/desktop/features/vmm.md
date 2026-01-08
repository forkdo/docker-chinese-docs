---
title: Docker Desktop for Mac 的虚拟机管理器
linkTitle: 虚拟机管理器
keywords: virtualization software, resource allocation, mac, docker desktop, vm monitoring, vm performance, apple silicon
description: 了解 Docker Desktop for Mac 的虚拟机管理器 (VMM) 选项，包括适用于 Apple Silicon 的新版 Docker VMM，可提供更强的性能和效率
weight: 110
aliases:
- /desktop/vmm/
---

Docker Desktop 支持多种虚拟机管理器 (VMM)，用于运行容器的 Linux 虚拟机。您可以根据系统架构（Intel 或 Apple Silicon）、性能需求和功能要求选择最合适的选项。本页概述了可用的选项。

要更改 VMM，请转到 **设置** > **常规** > **虚拟机管理器**。

## Docker VMM

{{< summary-bar feature_name="VMM" >}}

Docker VMM 是一种新的、针对容器优化的虚拟机管理程序。通过优化 Linux 内核和虚拟机管理程序层，Docker VMM 在常见的开发者任务中提供了显著的性能提升。

Docker VMM 提供的一些关键性能提升包括：
 - 更快的 I/O 操作：在冷缓存情况下，使用 `find` 遍历大型共享文件系统的速度比使用 Apple Virtualization 框架时快 2 倍。
 - 改进的缓存：在热缓存情况下，性能最多可提升 25 倍，甚至超过原生 Mac 操作。

这些改进直接影响那些在容器化开发过程中依赖频繁文件访问和整体系统响应性的开发者。Docker VMM 在速度上实现了显著飞跃，使工作流程更顺畅，迭代周期更快。

> [!NOTE]
>
> Docker VMM 要求至少为 Docker Linux 虚拟机分配 4GB 内存。在启用 Docker VMM 之前，需要增加内存，这可以在 **设置** 的 **资源** 选项卡中完成。

### 已知问题

由于 Docker VMM 仍处于 Beta 阶段，存在一些已知限制：

- Docker VMM 目前不支持 Rosetta，因此 amd64 架构的模拟速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库（如 MongoDB 和 Cassandra）在使用 Docker VMM 的 virtiofs 时可能会失败。预计此问题将在未来的版本中解决。

## Apple Virtualization 框架

Apple Virtualization 框架是 Mac 上管理虚拟机的稳定且成熟的选项。多年来，它一直是许多 Mac 用户的可靠选择。该框架最适合那些偏好经过验证的解决方案、具有良好性能和广泛兼容性的开发者。

## 适用于 Apple Silicon 的 QEMU（传统）

> [!NOTE]
>
> QEMU 已在 4.44 及更高版本中弃用。有关更多信息，请参阅 [博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/) 

QEMU 是 Apple Silicon Mac 的传统虚拟化选项，主要用于旧用例。

Docker 建议过渡到更新的替代方案，如 Docker VMM 或 Apple Virtualization 框架，因为它们提供了更优越的性能和持续的支持。特别是 Docker VMM，为使用 Apple Silicon 的开发者提供了显著的速度提升和更高效的开发环境，使其成为一个引人注目的选择。

请注意，这与在 [多平台构建](/manuals/build/building/multi-platform.md#qemu) 中使用 QEMU 模拟非原生架构无关。

## 适用于基于 Intel 的 Mac 的 HyperKit（传统）

> [!NOTE]
>
> HyperKit 将在未来的版本中弃用。

HyperKit 是另一个传统虚拟化选项，专门用于基于 Intel 的 Mac。与 QEMU 一样，它仍然可用，但已被视为弃用。Docker 建议切换到现代替代方案，以获得更好的性能并使您的设置面向未来。