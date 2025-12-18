---
description: 了解如何优化 ZFS 驱动的使用。
keywords: '容器, 存储, 驱动, ZFS '
title: ZFS 存储驱动
aliases:
  - /storage/storagedriver/zfs-driver/
---

ZFS 是一个下一代文件系统，支持许多高级存储技术，如卷管理、快照、校验和、压缩和去重、复制等。

它由 Sun Microsystems（现为 Oracle Corporation）创建，并以 CDDL 许可证开源。由于 CDDL 与 GPL 之间的许可不兼容性，ZFS 无法作为 Linux 主线内核的一部分发布。但是，ZFS On Linux（ZoL）项目提供了一个独立于内核的模块和用户空间工具，可以单独安装。

ZFS on Linux（ZoL）端口运行稳定且日趋成熟。不过，目前尚不建议在生产环境中使用 `zfs` Docker 存储驱动，除非您对 Linux 上的 ZFS 有丰富的使用经验。

> [!NOTE]
>
> Linux 平台上还有一个 ZFS 的 FUSE 实现。不建议使用此实现。原生 ZFS 驱动（ZoL）经过更多测试，性能更好，使用更广泛。本文档的其余部分均指原生 ZoL 端口。

## 前置条件

- ZFS 需要一个或多个专用块设备，最好是固态硬盘（SSD）。
- `/var/lib/docker/` 目录必须挂载在 ZFS 格式的文件系统上。
- 更改存储驱动会使您已创建的容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，以便稍后无需重新创建。

> [!NOTE]
>
> 无需使用 `MountFlags=slave`，因为 `dockerd` 和 `containerd` 位于不同的挂载命名空间中。

## 配置 Docker 使用 `zfs` 存储驱动

1.  停止 Docker。

2.  将 `/var/lib/docker/` 的内容复制到 `/var/lib/docker.bk`，并清空 `/var/lib/docker/` 的内容。

    ```console
    $ sudo cp -au /var/lib/docker /var/lib/docker.bk

    $ sudo rm -rf /var/lib/docker/*
    ```

3.  在您的专用块设备上创建新的 `zpool`，并将其挂载到 `/var/lib/docker/`。确保您指定了正确的设备，因为这是一个破坏性操作。此示例将两个设备添加到池中。

    ```console
    $ sudo zpool create -f zpool-docker -m /var/lib/docker /dev/xvdf /dev/xvdg
    ```

    该命令创建 `zpool` 并将其命名为 `zpool-docker`。名称仅用于显示目的，您可以使用不同的名称。使用 `zfs list` 检查池是否已正确创建和挂载。

    ```console
    $ sudo zfs list

    NAME           USED  AVAIL  REFER  MOUNTPOINT
    zpool-docker    55K  96.4G    19K  /var/lib/docker
    ```

4.  配置 Docker 使用 `zfs`。编辑 `/etc/docker/daemon.json`，将 `storage-driver` 设置为 `zfs`。如果文件之前为空，现在应如下所示：

    ```json
    {
      "storage-driver": "zfs"
    }
    ```

    保存并关闭文件。

5.  启动 Docker。使用 `docker info` 验证存储驱动是否为 `zfs`。

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

### 增加运行中设备的容量

要增加 `zpool` 的大小，您需要向 Docker 主机添加一个专用块设备，然后使用 `zpool add` 命令将其添加到 `zpool`：

```console
$ sudo zpool add zpool-docker /dev/xvdh
```

### 限制容器的可写存储配额

如果您想基于每个镜像/数据集实现配额，可以设置 `size` 存储选项来限制单个容器的可写层使用的空间。

编辑 `/etc/docker/daemon.json` 并添加以下内容：

```json
{
  "storage-driver": "zfs",
  "storage-opts": ["size=256M"]
}
```

请参阅 [daemon 参考文档](/reference/cli/dockerd/#daemon-storage-driver) 中每个存储驱动的所有存储选项。

保存并关闭文件，然后重启 Docker。

## `zfs` 存储驱动的工作原理

ZFS 使用以下对象：

- **文件系统**：薄配置，根据需要从 `zpool` 分配空间。
- **快照**：高效利用空间的只读时间点副本。
- **克隆**：快照的读写副本。用于存储与父层的差异。

创建克隆的过程：

![ZFS 快照和克隆](images/zfs_clones.webp?w=450)


1.  从文件系统创建一个只读快照。
2.  从快照创建一个可写克隆。这包含与父层的任何差异。

文件系统、快照和克隆都从底层 `zpool` 分配空间。

### 磁盘上的镜像和容器层

每个运行中容器的统一文件系统挂载在 `/var/lib/docker/zfs/graph/` 中的挂载点上。继续阅读以了解统一文件系统是如何组成的。

### 镜像分层和共享

镜像的底层是 ZFS 文件系统。每个子层是基于下层镜像 ZFS 快照的 ZFS 克隆。容器是基于其创建来源镜像顶层 ZFS 快照的 ZFS 克隆。

下图展示了基于两层镜像运行的容器如何组合在一起。

![Docker 容器的 ZFS 池](images/zfs_zpool.webp?w=600)

启动容器时，按以下顺序发生：

1.  镜像的底层作为 ZFS 文件系统存在于 Docker 主机上。

2.  额外的镜像层是基于其下层镜像数据集的 ZFS 克隆。

    在图中，“Layer 1”通过对底层取 ZFS 快照，然后从该快照创建克隆来添加。克隆是可写的，根据需要从 zpool 消耗空间。快照是只读的，保持底层作为不可变对象。

3.  容器启动时，在镜像上方添加一个可写层。

    在图中，容器的读写层通过创建顶层镜像（Layer 1）的快照并从该快照创建克隆来实现。

4.  当容器修改其可写层的内容时，为更改的块分配空间。默认情况下，这些块为 128k。


## `zfs` 上容器读写的工作原理

### 读取文件

每个容器的可写层是 ZFS 克隆，与其创建来源的数据集（其父层的快照）共享所有数据。即使读取的数据来自深层，读操作也很快。此图说明了块共享的工作原理：

![ZFS 块共享](images/zpool_blocks.webp?w=450)


### 写入文件

**写入新文件**：根据需要从底层 `zpool` 分配空间，块直接写入容器的可写层。

**修改现有文件**：仅为更改的块分配空间，这些块使用写时复制（CoW）策略写入容器的可写层。这最小化了层的大小并提高了写入性能。

**删除文件或目录**：
  - 当您删除存在于较低层的文件或目录时，ZFS 驱动会屏蔽容器可写层中该文件或目录的存在，即使该文件或目录仍存在于较低的只读层中。
  - 如果您在容器的可写层内创建然后删除文件或目录，块会被 `zpool` 回收。


## ZFS 和 Docker 性能

有几个因素会影响使用 `zfs` 存储驱动的 Docker 性能。

- **内存**：内存对 ZFS 性能有重大影响。ZFS 最初是为具有大量内存的大型企业级服务器设计的。

- **ZFS 特性**：ZFS 包含一个去重功能。使用此功能可能节省磁盘空间，但会使用大量内存。建议您对 Docker 使用的 `zpool` 禁用此功能，除非您使用 SAN、NAS 或其他硬件 RAID 技术。

- **ZFS 缓存**：ZFS 在一个称为自适应替换缓存（ARC）的内存结构中缓存磁盘块。ZFS 的 *Single Copy ARC* 特性允许单个缓存块副本被多个克隆共享。使用此特性，多个运行中的容器可以共享单个缓存块副本。这使得 ZFS 成为 PaaS 和其他高密度用例的良好选择。

- **碎片化**：碎片化是 ZFS 等写时复制文件系统的自然副产品。ZFS 通过使用 128k 的小块大小来缓解此问题。ZFS 意图日志（ZIL）和写入合并（延迟写入）也有助于减少碎片化。您可以使用 `zpool status` 监控碎片化。但是，除非重新格式化和恢复文件系统，否则无法对 ZFS 进行碎片整理。

- **使用 Linux 的原生 ZFS 驱动**：不建议使用 ZFS FUSE 实现，因其性能较差。

### 性能最佳实践

- **使用快速存储**：固态硬盘（SSD）比旋转磁盘提供更快的读写速度。

- **对写入密集型工作负载使用卷**：卷为写入密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过了存储驱动，不会产生薄配置和写时复制引入的潜在开销。卷还有其他好处，例如允许您在容器间共享数据，即使没有运行中的容器使用它们也能持久化。