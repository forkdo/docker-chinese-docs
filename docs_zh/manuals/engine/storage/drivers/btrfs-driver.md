---
description: 了解如何优化使用 Btrfs 驱动程序。
keywords: 容器, 存储, 驱动, Btrfs
title: BTRFS 存储驱动
aliases:
  - /storage/storagedriver/btrfs-driver/
---

> [!IMPORTANT]
>
> 在大多数情况下，你应该使用 `overlay2` 存储驱动 —— 仅仅因为你的系统使用 Btrfs 作为根文件系统，并不意味着必须使用 `btrfs` 存储驱动。
>
> Btrfs 驱动存在已知问题。更多信息请参阅 [Moby issue #27653](https://github.com/moby/moby/issues/27653)。

Btrfs 是一个支持写时复制的文件系统，支持许多高级存储技术，使其非常适合 Docker。Btrfs 已包含在主线 Linux 内核中。

Docker 的 `btrfs` 存储驱动利用了许多 Btrfs 功能来管理镜像和容器。这些功能包括块级操作、精简配置、写时复制快照以及易于管理。你可以将多个物理块设备组合成一个 Btrfs 文件系统。

本文档将 Docker 的 Btrfs 存储驱动称为 `btrfs`，将整体 Btrfs 文件系统称为 Btrfs。

> [!NOTE]
>
> `btrfs` 存储驱动仅在 SLES、Ubuntu 和 Debian 系统上的 Docker Engine CE 上受支持。

## 前置条件

要使用 `btrfs`，需满足以下前置条件：

- `btrfs` 仅推荐在 Ubuntu 或 Debian 系统上的 Docker CE 上使用。

- 更改存储驱动会使你在本地系统上已创建的任何容器无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，以便稍后无需重新创建。

- `btrfs` 需要专用的块存储设备，例如物理磁盘。此块设备必须格式化为 Btrfs 并挂载到 `/var/lib/docker/`。下面的配置说明将引导你完成此过程。默认情况下，SLES 的 `/` 文件系统使用 Btrfs 格式化，因此对于 SLES，你不需要使用单独的块设备，但出于性能原因，你可以选择这样做。

- 内核必须支持 `btrfs`。检查方法是运行以下命令：

  ```console
  $ grep btrfs /proc/filesystems

  btrfs
  ```

- 要在操作系统级别管理 Btrfs 文件系统，你需要 `btrfs` 命令。如果还没有此命令，请安装 `btrfsprogs` 包（SLES）或 `btrfs-tools` 包（Ubuntu）。

## 配置 Docker 使用 btrfs 存储驱动

在 SLES 和 Ubuntu 上，此过程基本相同。

1. 停止 Docker。

2. 将 `/var/lib/docker/` 的内容复制到备份位置，然后清空 `/var/lib/docker/` 的内容：

   ```console
   $ sudo cp -au /var/lib/docker /var/lib/docker.bk
   $ sudo rm -rf /var/lib/docker/*
   ```

3. 将专用块设备或设备格式化为 Btrfs 文件系统。本示例假设你使用两个名为 `/dev/xvdf` 和 `/dev/xvdg` 的块设备。请仔细检查块设备名称，因为这是一个破坏性操作。

   ```console
   $ sudo mkfs.btrfs -f /dev/xvdf /dev/xvdg
   ```

   Btrfs 有许多选项，包括条带化和 RAID。请参阅 [Btrfs 文档](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices)。

4. 将新的 Btrfs 文件系统挂载到 `/var/lib/docker/` 挂载点。你可以指定用于创建 Btrfs 文件系统的任何块设备。

   ```console
   $ sudo mount -t btrfs /dev/xvdf /var/lib/docker
   ```

   > [!NOTE]
   >
   > 通过在 `/etc/fstab` 中添加条目，使更改在重启后保持不变。

5. 将 `/var/lib/docker.bk` 的内容复制到 `/var/lib/docker/`。

   ```console
   $ sudo cp -au /var/lib/docker.bk/* /var/lib/docker/
   ```

6. 配置 Docker 使用 `btrfs` 存储驱动。即使 `/var/lib/docker/` 现在使用 Btrfs 文件系统，这也是必需的。编辑或创建文件 `/etc/docker/daemon.json`。如果是新文件，请添加以下内容。如果是现有文件，请仅添加键和值，如果它不是结束大括号 (`}`) 前的最后一行，请注意在行尾添加逗号。

   ```json
   {
     "storage-driver": "btrfs"
   }
   ```

   请参阅 [daemon 参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中每个存储驱动的所有存储选项。

7. 启动 Docker。运行后，验证 `btrfs` 是否被用作存储驱动。

   ```console
   $ docker info

   Containers: 0
    Running: 0
    Paused: 0
    Stopped: 0
   Images: 0
   Server Version: 17.03.1-ce
   Storage Driver: btrfs
    Build Version: Btrfs v4.4
    Library Version: 101
   <...>
   ```

8. 准备就绪后，删除 `/var/lib/docker.bk` 目录。

## 管理 Btrfs 卷

Btrfs 的优势之一是无需卸载文件系统或重启 Docker 即可轻松管理 Btrfs 文件系统。

当空间不足时，Btrfs 会自动以大约 1 GB 的块扩展卷。

要向 Btrfs 卷添加块设备，请使用 `btrfs device add` 和 `btrfs filesystem balance` 命令。

```console
$ sudo btrfs device add /dev/svdh /var/lib/docker

$ sudo btrfs filesystem balance /var/lib/docker
```

> [!NOTE]
>
> 虽然你可以在 Docker 运行时执行这些操作，但性能会受到影响。最好计划一个停机窗口来平衡 Btrfs 文件系统。

## `btrfs` 存储驱动的工作原理

`btrfs` 存储驱动与其他存储驱动的工作方式不同，因为你的整个 `/var/lib/docker/` 目录都存储在 Btrfs 卷上。

### 磁盘上的镜像和容器层

有关镜像层和可写容器层的信息存储在 `/var/lib/docker/btrfs/subvolumes/` 中。此子目录包含每个镜像或容器层的一个目录，其中包含从一层及其所有父层构建的统一文件系统。子卷是原生的写时复制，从底层存储池按需分配空间。它们也可以嵌套和快照。下图显示了 4 个子卷。"子卷 2" 和 "子卷 3" 是嵌套的，而 "子卷 4" 显示其自己的内部目录树。

![子卷示例](images/btfs_subvolume.webp?w=350&h=100)

只有镜像的底层存储为真正的子卷。所有其他层都存储为快照，只包含该层引入的差异。你可以像下图所示那样创建快照的快照。

![快照图](images/btfs_snapshots.webp?w=350&h=100)

在磁盘上，快照看起来和感觉起来都像子卷，但实际上它们要小得多且更高效。使用写时复制来最大化存储效率并最小化层大小，容器可写层中的写入在块级别管理。下图显示了一个子卷及其快照共享数据。

![快照和子卷共享数据](images/btfs_pool.webp?w=450&h=200)

为了获得最大效率，当容器需要更多空间时，会以大约 1 GB 大小的块分配。

Docker 的 `btrfs` 存储驱动将每个镜像层和容器存储在其自己的 Btrfs 子卷或快照中。镜像的底层存储为子卷，而子镜像层和容器存储为快照。如下图所示。

![Btrfs 容器层](images/btfs_container_layer.webp?w=600)

在运行 `btrfs` 驱动的 Docker 主机上创建镜像和容器的高级过程如下：

1. 镜像的底层存储在 `/var/lib/docker/btrfs/subvolumes` 下的 Btrfs _子卷_ 中。

2. 后续镜像层存储为父层子卷或快照的 Btrfs _快照_，但包含此层引入的更改。这些差异在块级别存储。

3. 容器的可写层是最终镜像层的 Btrfs 快照，包含运行中容器引入的差异。这些差异在块级别存储。

## `btrfs` 的容器读写工作原理

### 读取文件

容器是镜像的高效空间快照。快照中的元数据指向存储池中的实际数据块。这与子卷相同。因此，对快照执行的读取本质上与对子卷执行的读取相同。

### 写入文件

作为一般警告，使用 Btrfs 写入和更新大量小文件可能导致性能缓慢。

考虑容器以 Btrfs 打开文件进行写访问的三种情况。

#### 写入新文件

将新文件写入容器会调用按需分配操作，为容器的快照分配新的数据块。然后将文件写入此新空间。按需分配操作是 Btrfs 所有写入的原生操作，与向子卷写入新数据相同。因此，向容器快照写入新文件以原生 Btrfs 速度运行。

#### 修改现有文件

更新容器中的现有文件是写时复制操作（Btrfs 术语中的重定向写入）。从文件当前存在的层读取原始数据，只有修改的块被写入容器的可写层。然后，Btrfs 驱动更新快照中的文件系统元数据以指向此新数据。此行为带来轻微开销。

#### 删除文件或目录

如果容器删除较低层中存在的文件或目录，Btrfs 会屏蔽较低层中文件或目录的存在。如果容器创建文件然后删除它，此操作在 Btrfs 文件系统本身中执行，空间被回收。

## Btrfs 和 Docker 性能

有几个因素会影响 Docker 在 `btrfs` 存储驱动下的性能。

> [!NOTE]
>
> 许多这些因素通过为写密集工作负载使用 Docker 卷来缓解，而不是依赖于在容器的可写层中存储数据。然而，在 Btrfs 的情况下，除非 `/var/lib/docker/volumes/` 不由 Btrfs 支持，否则 Docker 卷仍然会遭受这些缺点。

### 页面缓存

Btrfs 不支持页面缓存共享。这意味着每个访问同一文件的进程都会将该文件复制到 Docker 主机的内存中。因此，`btrfs` 驱动可能不是高密度用例（如 PaaS）的最佳选择。

### 小写入

执行大量小写入的容器（这种使用模式与你在短时间内启动和停止许多容器时发生的情况匹配）会导致 Btrfs 块的使用不佳。这可能过早地填满 Btrfs 文件系统，并导致 Docker 主机上的空间不足条件。使用 `btrfs filesys show` 密切监控 Btrfs 设备上的可用空间量。

### 顺序写入

Btrfs 在写入磁盘时使用日志记录技术。这可能会影响顺序写入的性能，使性能降低多达 50%。

### 碎片化

碎片化是 Btrfs 等写时复制文件系统的自然副产品。许多小的随机写入会加剧此问题。碎片化可能表现为 SSD 上的 CPU 尖峰或旋转磁盘上的磁头抖动。这些问题都可能损害性能。

如果你的 Linux 内核版本是 3.9 或更高版本，你可以在挂载 Btrfs 卷时启用 `autodefrag` 功能。在将其部署到生产环境之前，请在你自己的工作负载上测试此功能，因为一些测试显示它对性能有负面影响。

### SSD 性能

Btrfs 包含针对 SSD 介质的原生存储优化。要启用这些功能，请使用 `-o ssd` 挂载选项挂载 Btrfs 文件系统。这些优化包括通过避免对固态介质不适用的寻道优化来增强 SSD 写入性能。

### 经常平衡 Btrfs 文件系统

使用操作系统实用程序（如在非高峰时段运行的 `cron` 作业）定期平衡 Btrfs 文件系统。这会回收未分配的块，并有助于防止文件系统不必要地填满。除非你向文件系统添加额外的物理块设备，否则你不能平衡一个完全填满的 Btrfs 文件系统。

请参阅 [Btrfs Wiki](https://btrfs.wiki.kernel.org/index.php/Balance_Filters#Balancing_to_fix_filesystem_full_errors)。

### 使用快速存储

固态驱动器 (SSD) 提供比旋转磁盘更快的读写速度。

### 为写密集工作负载使用卷

卷为写密集工作负载提供最佳且最可预测的性能。这是因为它们绕过存储驱动，不会产生精简配置和写时复制引入的任何潜在开销。卷还有其他好处，例如允许你在容器之间共享数据，即使在没有运行的容器使用它们时也能保持。

## 相关信息

- [卷](../volumes.md)
- [了解镜像、容器和存储驱动](index.md)
- [选择存储驱动](select-storage-driver.md)