---
title: 选择存储驱动程序
weight: 10
description: 了解如何为容器选择合适的存储驱动程序。
keywords: container, storage, driver, btrfs, zfs, overlay, overlay2, containerd
aliases:
- /storage/storagedriver/selectadriver/
- /storage/storagedriver/select-storage-driver/
---

理想情况下，写入容器可写层的数据非常少，您应该使用 Docker 卷来写入数据。但是，某些工作负载要求能够写入容器的可写层。这就是存储驱动程序的用武之地。

> [!NOTE]
> Docker Engine 29.0 及更高版本在全新安装时默认使用 [containerd 镜像存储](../containerd.md)。如果您是从早期版本升级的，您的守护进程将继续使用本页描述的经典存储驱动程序。您可以按照 [containerd 镜像存储](../containerd.md) 文档中的说明迁移到 containerd 镜像存储。

Docker 使用可插拔架构支持多种存储驱动程序。存储驱动程序控制镜像和容器在 Docker 主机上的存储和管理方式。在阅读了[存储驱动程序概述](./_index.md)之后，下一步是为您的工作负载选择最佳的存储驱动程序。使用在最常见场景下具有最佳整体性能和稳定性的存储驱动程序。

> [!NOTE]
> 本文讨论的是 Linux 上的 Docker Engine 存储驱动程序。如果您在 Windows 上运行 Docker 守护进程作为主机操作系统，唯一受支持的存储驱动程序是 `windowsfilter`。有关更多信息，请参阅 [windowsfilter](windowsfilter-driver.md)。

Docker Engine 在 Linux 上提供以下存储后端：

| 后端 (Backend)                     | 描述 (Description)                                                                                                                                                                                                                                                |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `containerd` (snapshotters) | Docker Engine 29.0 及更高版本的默认设置。使用 containerd 快照程序进行镜像存储。支持多平台镜像和证明。有关详细信息，请参阅 [containerd 镜像存储](../containerd.md)。                                                 |
| `overlay2`                  | 经典存储驱动程序。在所有当前支持的 Linux 发行版中具有最广泛的兼容性，且不需要额外配置。                                                                                                                    |
| `fuse-overlayfs`            | 仅建议在不支持无根 `overlay2` 的主机上运行无根 Docker 时使用。自 Linux 内核 5.11 起不再需要，因为 `overlay2` 可以在无根模式下工作。有关详细信息，请参阅[无根模式文档](/manuals/engine/security/rootless.md)。 |
| `btrfs` 和 `zfs`           | 允许使用高级选项，例如创建快照，但需要更多的维护和设置。每个都依赖于正确配置的后端文件系统。                                                                                          |
| `vfs`                       | 用于测试目的，以及无法使用写时复制 (copy-on-write) 文件系统的情况。性能较差，通常不建议在生产环境中使用。                                                                                    |

<!-- markdownlint-disable reference-links-images -->

如果没有明确配置存储驱动程序，Docker Engine 有一个优先列表来决定使用哪个存储驱动程序，前提是该存储驱动程序满足先决条件，并自动选择兼容的存储驱动程序。您可以在 [Docker Engine {{% param "docker_ce_version" %}} 的源代码](https://github.com/moby/moby/blob/v{{% param "docker_ce_version" %}}/daemon/graphdriver/driver_linux.go#L52-L53) 中查看顺序。
{ #storage-driver-order }

<!-- markdownlint-enable reference-links-images -->

某些存储驱动程序要求您对后端文件系统使用特定格式。如果您有使用特定后端文件系统的外部要求，这可能会限制您的选择。请参阅[支持的后端文件系统](#supported-backing-filesystems)。

在缩小了可以选择的存储驱动程序范围之后，您的选择将由工作负载的特征和所需的稳定性水平决定。请参阅[其他注意事项](#other-considerations)以帮助做出最终决定。

## 各 Linux 发行版支持的存储驱动程序

> [!NOTE]
> 通过编辑守护进程配置文件来修改存储驱动程序在 Docker Desktop 上不受支持。Docker Desktop 默认使用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)（全新安装的版本 4.34 及更高版本）。下表也不适用于无根模式下的 Docker Engine。有关无根模式下可用的驱动程序，请参阅[无根模式文档](/manuals/engine/security/rootless.md)。

本节仅适用于经典存储驱动程序。如果您使用的是 containerd 镜像存储（Docker Engine 29.0+ 的默认设置），请改阅 [containerd 镜像存储文档](../containerd.md)。

您的操作系统和内核可能不支持每个经典存储驱动程序。例如，仅当您的系统使用 `btrfs` 作为存储时才支持 `btrfs`。通常，以下配置适用于 Linux 发行版的最新版本：

| Linux 发行版   | 默认经典驱动程序  | 替代驱动程序  |
| :------------------- | :---------------------- | :------------------- |
| Ubuntu               | `overlay2`              | `zfs`, `vfs`         |
| Debian               | `overlay2`              | `vfs`                |
| CentOS               | `overlay2`              | `zfs`, `vfs`         |
| Fedora               | `overlay2`              | `zfs`, `vfs`         |
| SLES 15              | `overlay2`              | `vfs`                |
| RHEL                 | `overlay2`              | `vfs`                |

对于使用经典存储驱动程序的系统，`overlay2` 在 Linux 发行版之间提供了广泛的兼容性。对于写密集型工作负载，请使用 Docker 卷，而不是依赖将数据写入容器的可写层。

`vfs` 存储驱动程序通常不是最佳选择，主要用于在无其他存储驱动程序支持的情况下进行调试。在使用 `vfs` 存储驱动程序之前，请务必阅读[其性能、存储特征和限制](vfs-driver.md)。

上表中的建议已知适用于大量用户。如果您使用推荐配置并发现可复现的问题，很可能会很快得到修复。如果您想使用的驱动程序根据此表不被推荐，您可以自行承担风险运行它。您仍然可以并且应该报告遇到的任何问题。但是，此类问题的优先级低于使用推荐配置时遇到的问题。

根据您的 Linux 发行版，其他存储驱动程序（如 `btrfs`）可能可用。这些存储驱动程序对于特定用例可能具有优势，但可能需要额外的设置或维护，因此不建议在常见场景中使用。有关详细信息，请参阅这些存储驱动程序的文档。

## 支持的后端文件系统

对于 Docker 而言，后端文件系统是 `/var/lib/docker/` 所在的文件系统。某些存储驱动程序仅适用于特定的后端文件系统。

| 存储驱动程序   | 支持的后端文件系统                         |
| :--------------- | :-----------------------------------------------------|
| `overlay2`       | `xfs` (ftype=1), `ext4`, `btrfs`, (以及更多)     |
| `fuse-overlayfs` | 任何文件系统                                        |
| `btrfs`          | `btrfs`                                               |
| `zfs`            | `zfs`                                                 |
| `vfs`            | 任何文件系统                                        |

> [!NOTE]
>
> 大多数文件系统只要具备所需的功能就可以工作。
> 请查阅 [OverlayFS](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html)
> 以获取更多信息。


## 其他注意事项

### 适合您的工作负载

除其他外，每个存储驱动程序都有自己的性能特征，这使其或多或少地适合不同的工作负载。考虑以下概括：

- `overlay2` 在文件级别而不是块级别运行。这可以更有效地使用内存，但在写密集型工作负载中，容器的可写层可能会变得相当大。
- 块级存储驱动程序（如 `btrfs` 和 `zfs`）在写密集型工作负载中表现更好（尽管不如 Docker 卷）。
- `btrfs` 和 `zfs` 需要大量内存。
- `zfs` 是高密度工作负载（如 PaaS）的不错选择。

有关性能、适用性和最佳实践的更多信息，请参阅每个存储驱动程序的文档。

### 共享存储系统和存储驱动程序

如果您使用 SAN、NAS、硬件 RAID 或其他共享存储系统，这些系统可能提供高可用性、提高的性能、精简配置、重复数据删除和压缩。在许多情况下，Docker 可以在这些存储系统之上工作，但 Docker 不会与它们紧密集成。

每个 Docker 存储驱动程序都基于 Linux 文件系统或卷管理器。请务必遵循现有的最佳实践，在共享存储系统之上操作您的存储驱动程序（文件系统或卷管理器）。例如，如果在共享存储系统之上使用 ZFS 存储驱动程序，请务必遵循在该特定共享存储系统之上操作 ZFS 文件系统的最佳实践。

### 稳定性

对于某些用户来说，稳定性比性能更重要。尽管 Docker 认为这里提到的所有存储驱动程序都是稳定的，但有些较新且仍在积极开发中。通常，`overlay2` 提供最高的稳定性。

### 使用您自己的工作负载进行测试

您可以在不同的存储驱动程序上运行自己的工作负载时测试 Docker 的性能。确保使用等效的硬件和工作负载来匹配生产条件，以便您可以看到哪个存储驱动程序提供最佳的整体性能。

## 检查您当前的存储驱动程序

每个单独存储驱动程序的详细文档都详细说明了使用给定存储驱动程序的所有设置步骤。

要查看 Docker 当前正在使用哪个存储驱动程序，请使用 `docker info` 并查找 `Storage Driver` 行：

```console
$ docker info

Containers: 0
Images: 0
Storage Driver: overlay2
 Backing Filesystem: xfs
<...>
```

要更改存储驱动程序，请参阅新存储驱动程序的具体说明。某些驱动程序需要额外配置，包括对 Docker 主机上物理或逻辑磁盘的配置。

> [!IMPORTANT]
>
> 更改存储驱动程序时，任何现有的镜像和容器都将变得无法访问。这是因为它们的层无法被新的存储驱动程序使用。如果您撤消更改，则可以再次访问旧的镜像和容器，但使用新驱动程序拉取或创建的任何镜像和容器都将无法访问。

## 相关信息

- [存储驱动程序](./_index.md)
- [`overlay2` 存储驱动程序](overlayfs-driver.md)
- [`btrfs` 存储驱动程序](btrfs-driver.md)
- [`zfs` 存储驱动程序](zfs-driver.md)
- [`windowsfilter` 存储驱动程序](windowsfilter-driver.md)