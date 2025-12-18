---
title: 选择存储驱动
weight: 10
description: 了解如何为容器选择合适的存储驱动。
keywords: container, storage, driver, btrfs, zfs, overlay, overlay2, containerd
aliases:
  - /storage/storagedriver/selectadriver/
  - /storage/storagedriver/select-storage-driver/
---

理想情况下，写入容器可写层的数据应该很少，你应该使用 Docker 卷来写入数据。但是，某些工作负载需要写入容器的可写层。这就是存储驱动发挥作用的地方。

> [!NOTE]
> Docker Engine 29.0 及更高版本默认使用
> [containerd 镜像存储](../containerd.md)（适用于全新安装）。
> 如果你从早期版本升级，你的守护进程将继续使用
> 本页描述的经典存储驱动。你可以按照
> [containerd 镜像存储](../containerd.md) 文档中的说明迁移到
> containerd 镜像存储。

Docker 支持多种存储驱动，采用可插拔架构。存储驱动控制镜像和容器如何在你的 Docker 主机上存储和管理。阅读完[存储驱动概述](./_index.md)后，下一步是为你的工作负载选择最佳的存储驱动。使用在最常见场景中性能和稳定性最佳的存储驱动。

> [!NOTE]
> 本文讨论的是 Linux 主机上 Docker Engine 的存储驱动。如果你在 Windows 主机上运行 Docker 守护进程，唯一支持的存储驱动是 windowsfilter。更多信息请参阅
> [windowsfilter](windowsfilter-driver.md)。

Docker Engine 在 Linux 上提供以下存储后端：

| 后端                      | 描述                                                                                                                                                                                                                                                |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `containerd` (快照器)     | Docker Engine 29.0 及更高版本的默认选项。使用 containerd 快照器存储镜像。支持多平台镜像和证明。详情请参阅 [containerd 镜像存储](../containerd.md)。                                                                                                 |
| `overlay2`                | 经典存储驱动。在所有当前支持的 Linux 发行版中兼容性最广泛，且无需额外配置。                                                                                                                                                                          |
| `fuse-overlayfs`          | 仅在主机不支持 rootless `overlay2` 时，才建议用于运行 Rootless Docker。Linux 内核 5.11 之后不再需要，因为 `overlay2` 在 rootless 模式下可以工作。详情请参阅 [rootless 模式文档](/manuals/engine/security/rootless.md)。                         |
| `btrfs` 和 `zfs`          | 允许高级选项，如创建快照，但需要更多维护和设置。每个都依赖于正确配置的底层文件系统。                                                                                                                                                                 |
| `vfs`                     | 用于测试目的，以及无法使用 copy-on-write 文件系统的情况。性能较差，一般不建议用于生产环境。                                                                                                                                                           |

<!-- markdownlint-disable reference-links-images -->

Docker Engine 有一个优先级列表，如果未显式配置存储驱动，且存储驱动满足先决条件，它会自动选择兼容的存储驱动。你可以在 [Docker Engine {{% param "docker_ce_version" %}} 的源代码](https://github.com/moby/moby/blob/v{{% param "docker_ce_version" %}}/daemon/graphdriver/driver_linux.go#L52-L53)中看到顺序。
{ #storage-driver-order }

<!-- markdownlint-enable reference-links-images -->

某些存储驱动要求你使用特定格式配置底层文件系统。如果你有外部要求必须使用特定的底层文件系统，这可能会限制你的选择。请参阅 [支持的底层文件系统](#supported-backing-filesystems)。

在缩小了可选择的存储驱动范围后，你的选择取决于工作负载的特性和你需要的稳定性级别。请参阅 [其他注意事项](#other-considerations) 以帮助做出最终决定。

## 每个 Linux 发行版支持的存储驱动

> [!NOTE]
> 通过编辑守护进程配置文件来修改存储驱动在 Docker Desktop 上不受支持。Docker Desktop 默认使用
> [containerd 镜像存储]（Docker Desktop 4.34 及更高版本的新安装）。下表也不适用于 rootless 模式下的 Docker Engine。有关 rootless 模式下可用的驱动，请参阅
> [Rootless 模式文档](/manuals/engine/security/rootless.md)。

本节仅适用于经典存储驱动。如果你使用 containerd 镜像存储（Docker Engine 29.0+ 的默认选项），请改用
[containerd 镜像存储文档](../containerd.md)。

你的操作系统和内核可能不支持每个经典存储驱动。例如，只有在系统使用 `btrfs` 作为存储时，才支持 `btrfs`。一般来说，以下配置在 Linux 发行版的最新版本上可以工作：

| Linux 发行版   | 默认经典驱动  | 替代驱动  |
| :------------- | :------------ | :-------- |
| Ubuntu         | `overlay2`    | `zfs`, `vfs` |
| Debian         | `overlay2`    | `vfs`     |
| CentOS         | `overlay2`    | `zfs`, `vfs` |
| Fedora         | `overlay2`    | `zfs`, `vfs` |
| SLES 15        | `overlay2`    | `vfs`     |
| RHEL           | `overlay2`    | `vfs`     |

对于使用经典存储驱动的系统，`overlay2` 在 Linux 发行版中提供了广泛的兼容性。对于写入密集型工作负载，应使用 Docker 卷而不是依赖于写入容器的可写层。

`vfs` 存储驱动通常不是最佳选择，主要用于在不支持其他存储驱动的情况下进行调试。在使用 `vfs` 存储驱动之前，请务必阅读
[其性能和存储特性及限制](vfs-driver.md)。

上表中的建议对大量用户有效。如果你使用推荐的配置并发现可重现的问题，它可能会很快得到修复。如果你想要使用的驱动未根据此表推荐，你可以自行承担风险使用它。你可以也应该报告遇到的任何问题。但是，这些问题的优先级低于使用推荐配置时遇到的问题。

根据你的 Linux 发行版，可能还有其他存储驱动可用，如 `btrfs`。这些存储驱动可能对特定用例有优势，但可能需要额外的设置或维护，这使得它们不推荐用于常见场景。请参阅这些存储驱动的文档了解详情。

## 支持的底层文件系统

就 Docker 而言，底层文件系统是 ` /var/lib/docker/` 所在的文件系统。某些存储驱动仅与特定的底层文件系统配合使用。

| 存储驱动   | 支持的底层文件系统                         |
| :--------- | :---------------------------------------- |
| `overlay2` | `xfs`（ftype=1）、`ext4`、`btrfs`（及更多）|
| `fuse-overlayfs` | 任何文件系统                          |
| `btrfs`    | `btrfs`                                   |
| `zfs`      | `zfs`                                     |
| `vfs`      | 任何文件系统                                |

> [!NOTE]
>
> 如果文件系统具有所需的功能，大多数文件系统应该可以工作。
> 请参阅 [OverlayFS](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html) 了解更多信息。

## 其他注意事项

### 工作负载的适用性

每个存储驱动都有自己的性能特征，使其更适合或不太适合不同的工作负载。考虑以下一般化：

- `overlay2` 在文件级别而不是块级别操作。这更高效地使用内存，但容器的可写层在写入密集型工作负载中可能变得相当大。
- `btrfs` 和 `zfs` 等块级存储驱动在写入密集型工作负载中表现更好（尽管不如 Docker 卷）。
- `btrfs` 和 `zfs` 需要大量内存。
- `zfs` 是高密度工作负载（如 PaaS）的良好选择。

有关性能、适用性和最佳实践的更多信息，请参阅每个存储驱动的文档。

### 共享存储系统和存储驱动

如果你使用 SAN、NAS、硬件 RAID 或其他共享存储系统，这些系统可能提供高可用性、提高性能、精简配置、去重和压缩。在许多情况下，Docker 可以在这些存储系统之上工作，但 Docker 不与它们紧密集成。

每个 Docker 存储驱动基于 Linux 文件系统或卷管理器。确保遵循在共享存储系统之上操作存储驱动（文件系统或卷管理器）的现有最佳实践。例如，如果在共享存储系统之上使用 ZFS 存储驱动，请确保遵循在特定共享存储系统之上操作 ZFS 文件系统的最佳实践。

### 稳定性

对于某些用户，稳定性比性能更重要。尽管 Docker 认为这里提到的所有存储驱动都是稳定的，但有些更新，仍在积极开发中。一般来说，`overlay2` 提供最高的稳定性。

### 使用你的工作负载进行测试

你可以测试 Docker 在不同存储驱动上运行你的工作负载时的性能。确保使用等效的硬件和工作负载来匹配生产条件，这样你就能看到哪个存储驱动提供最佳的整体性能。

## 检查当前存储驱动

每个单独存储驱动的详细文档详细说明了使用给定存储驱动的所有设置步骤。

要查看 Docker 当前使用的存储驱动，请使用 `docker info` 并查找 `Storage Driver` 行：

```console
$ docker info

Containers: 0
Images: 0
Storage Driver: overlay2
 Backing Filesystem: xfs
<...>
```

要更改存储驱动，请参阅新存储驱动的具体说明。某些驱动需要额外配置，包括对 Docker 主机上物理或逻辑磁盘的配置。

> [!IMPORTANT]
>
> 更改存储驱动时，任何现有镜像和容器将变得无法访问。这是因为它们的层不能被新存储驱动使用。如果你还原更改，你可以再次访问旧镜像和容器，但使用新驱动拉取或创建的任何镜像和容器将变得无法访问。

## 相关信息

- [存储驱动](./_index.md)
- [`overlay2` 存储驱动](overlayfs-driver.md)
- [`btrfs` 存储驱动](btrfs-driver.md)
- [`zfs` 存储驱动](zfs-driver.md)
- [`windowsfilter` 存储驱动](windowsfilter-driver.md)