---
description: 了解如何优化 ZFS 驱动程序的使用。
keywords: 'container, storage, driver, ZFS '
title: ZFS 存储驱动程序
aliases:
- /storage/storagedriver/zfs-driver/
---

ZFS 是一个下一代文件系统，支持许多高级存储技术，如卷管理、快照、校验和、压缩和去重、复制等。

它由 Sun Microsystems（现为 Oracle Corporation）创建，并在 CDDL 许可证下开源。由于 CDDL 和 GPL 之间的许可不兼容，ZFS 不能作为主线 Linux 内核的一部分发布。然而，Linux 上的 ZFS (ZoL) 项目提供了一个树外内核模块和用户空间工具，可以单独安装。

Linux 上的 ZFS (ZoL) 移植版本运行良好且日趋成熟。但是，目前除非您在 Linux 上使用 ZFS 拥有丰富的经验，否则不建议在生产环境中使用 `zfs` Docker 存储驱动程序。

> [!NOTE]
>
> Linux 平台上也有 ZFS 的 FUSE 实现。不建议使用。原生 ZFS 驱动程序 (ZoL) 经过更充分的测试，性能更好，使用也更广泛。本文档的其余部分指的是原生的 ZoL 移植版本。

## 先决条件

- ZFS 需要一个或多个专用块设备，最好是固态硬盘 (SSD)。
- `/var/lib/docker/` 目录必须挂载在 ZFS 格式的文件系统上。
- 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，以便以后无需重新创建它们。

> [!NOTE]
>
> 无需使用 `MountFlags=slave`，因为 `dockerd` 和 `containerd` 处于不同的挂载命名空间中。

## 使用 `zfs` 存储驱动程序配置 Docker

1.  停止 Docker。

2.  将 `/var/lib/docker/` 的内容复制到 `/var/lib/docker.bk`，并删除 `/var/lib/docker/` 的内容。

    ```console
    $ sudo cp -au /var/lib/docker /var/lib/docker.bk

    $ sudo rm -rf /var/lib/docker/*
    ```

3.  在您的专用块设备或设备上创建一个新的 `zpool`，并将其挂载到 `/var/lib/docker/`。请确保您指定了正确的设备，因为这是一个破坏性操作。此示例向池中添加两个设备。

    ```console
    $ sudo zpool create -f zpool-docker -m /var/lib/docker /dev/xvdf /dev/xvdg
    ```

    该命令创建 `zpool` 并将其命名为 `zpool-docker`。该名称仅用于显示，您可以使用不同的名称。使用 `zfs list` 检查池是否已正确创建和挂载。

    ```console
    $ sudo zfs list

    NAME           USED  AVAIL  REFER  MOUNTPOINT
    zpool-docker    55K  96.4G    19K  /var/lib/docker
    ```

4.  配置 Docker 使用 `zfs`。编辑 `/etc/docker/daemon.json` 并将 `storage-driver` 设置为 `zfs`。如果文件之前为空，现在应如下所示：

    ```json
    {
      "storage-driver": "zfs"
    }
    ```

    保存并关闭文件。

5.  启动 Docker。使用 `docker info` 验证存储驱动程序是否为 `zfs`。

    ```console
    $ sudo docker info
      Containers: 0
       Running: 0
       Paused: 0
       Stopped: 0
      Images: 0
      Server Version: 17.03.1-ce
      Storage Driver: zfs
       Zpool: zpool-docker
       Zpool Health: ONLINE
       Parent Dataset: zpool-docker
       Space Used By Parent: 249856
       Space Available: 103498395648
       Parent Quota: no
       Compression: off
    <...>
    ```

## 管理 `zfs`

### 在正在运行的设备上增加容量

要增加 `zpool` 的大小，您需要向 Docker 主机添加一个专用块设备，然后使用 `zpool add` 命令将其添加到 `zpool` 中：

```console
$ sudo zpool add zpool-docker /dev/xvdh
```

### 限制容器的可写存储配额

如果您想在每个镜像/数据集的基础上实施配额，可以设置 `size` 存储选项以限制单个容器可用于其可写层的空间量。

编辑 `/etc/docker/daemon.json` 并添加以下内容：

```json
{
  "storage-driver": "zfs",
  "storage-opts": ["size=256M"]
}
```

请参阅 [守护程序参考文档](/reference/cli/dockerd/#daemon-storage-driver) 中每种存储驱动程序的所有存储选项。

保存并关闭文件，然后重新启动 Docker。

## `zfs` 存储驱动程序的工作原理

ZFS 使用以下对象：

- **文件系统**：精简配置，空间按需从 `zpool` 分配。
- **快照**：文件系统的只读、空间高效的即时副本。
- **克隆**：快照的读写副本。用于存储与前一层的差异。

创建克隆的过程：

![ZFS 快照和克隆](images/zfs_clones.webp?w=450)

1.  从文件系统创建一个只读快照。
2.  从快照创建一个可写克隆。这包含与父层的任何差异。

文件系统、快照和克隆都从底层 `zpool` 分配空间。

### 磁盘上的镜像和容器层

每个正在运行的容器的统一文件系统都挂载在 `/var/lib/docker/zfs/graph/` 中的一个挂载点上。请继续阅读以了解统一文件系统的组成方式。

### 镜像分层和共享

镜像的基础层是一个 ZFS 文件系统。每个子层都是基于其下层 ZFS 快照的 ZFS 克隆。容器是基于其创建自的镜像顶层 ZFS 快照的 ZFS 克隆。

下图显示了基于两层镜像的正在运行的容器是如何组合在一起的。

![用于 Docker 容器的 ZFS 池](images/zfs_zpool.webp?w=600)

当您启动一个容器时，会按顺序发生以下步骤：

1.  镜像的基础层作为 ZFS 文件系统存在于 Docker 主机上。

2.  额外的镜像层是直接托管其下镜像层的数据集的克隆。

    在图中，“Layer 1”是通过获取基础层的 ZFS 快照，然后从该快照创建克隆来添加的。克隆是可写的，并按需从 zpool 消耗空间。快照是只读的，将基础层保持为不可变对象。

3.  当容器启动时，会在镜像上方添加一个可写层。

    在图中，容器的读写层是通过制作镜像顶层（Layer 1）的快照并从该快照创建克隆来创建的。

4.  当容器修改其可写层的内容时，会为更改的块分配空间。默认情况下，这些块是 128k。

## 容器如何使用 `zfs` 进行读写

### 读取文件

每个容器的可写层都是一个 ZFS 克隆，它与其创建自的数据集（其父层的快照）共享所有数据。读取操作非常快，即使要读取的数据来自深层。此图说明了块共享的工作原理：

![ZFS 块共享](images/zpool_blocks.webp?w=450)

### 写入文件

**写入新文件**：按需从底层 `zpool` 分配空间，块直接写入容器的可写层。

**修改现有文件**：仅为更改的块分配空间，这些块使用写时复制 (CoW) 策略写入容器的可写层。这可以最小化层的大小并提高写入性能。

**删除文件或目录**：
  - 当您删除存在于较低层中的文件或目录时，ZFS 驱动程序会掩盖该文件或目录在容器可写层中的存在，即使该文件或目录在较低的只读层中仍然存在。
  - 如果您在容器的可写层中创建然后删除文件或目录，这些块将被 `zpool` 回收。

## ZFS 和 Docker 性能

有几个因素会影响使用 `zfs` 存储驱动程序的 Docker 性能。

- **内存**：内存对 ZFS 性能有重大影响。ZFS 最初是为具有大量内存的大型企业级服务器设计的。
- **ZFS 特性**：ZFS 包含去重功能。使用此功能可以节省磁盘空间，但会消耗大量内存。建议为您与 Docker 一起使用的 `zpool` 禁用此功能，除非您使用 SAN、NAS 或其他硬件 RAID 技术。
- **ZFS 缓存**：ZFS 将磁盘块缓存在称为自适应替换缓存 (ARC) 的内存结构中。ZFS 的*单副本 ARC* 功能允许多个克隆共享一个缓存块的单个副本。借助此功能，多个正在运行的容器可以共享缓存块的单个副本。此功能使 ZFS 成为 PaaS 和其他高密度用例的良好选择。
- **碎片化**：碎片化是像 ZFS 这样的写时复制文件系统的自然副产品。ZFS 通过使用 128k 的小块大小来缓解此问题。ZFS 意图日志 (ZIL) 和写入合并（延迟写入）也有助于减少碎片化。您可以使用 `zpool status` 监控碎片化。但是，除了重新格式化和恢复文件系统外，没有其他方法可以对 ZFS 进行碎片整理。
- **使用 Linux 的原生 ZFS 驱动程序**：不建议使用 ZFS FUSE 实现，因为其性能较差。

### 性能最佳实践

- **使用快速存储**：固态硬盘 (SSD) 比旋转磁盘提供更快的读写速度。
- **对写入密集型工作负载使用卷**：卷为写入密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过存储驱动程序，并且不会因精简配置和写时复制而产生任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使在没有正在运行的容器使用它们时也能持久保存。