---
description: 了解如何优化 device mapper 驱动的使用。
keywords: 容器, 存储, 驱动, device mapper
title: Device Mapper 存储驱动（已弃用）
aliases:
  - /storage/storagedriver/device-mapper-driver/
---

> **已弃用**
>
> Device Mapper 驱动 [已被弃用](/manuals/engine/deprecated.md#device-mapper-storage-driver)，
> 并在 Docker Engine v25.0 中被移除。如果您正在使用 Device Mapper，
> 则必须在升级到 Docker Engine v25.0 之前迁移到受支持的存储驱动。请阅读 [Docker 存储驱动](select-storage-driver.md)
> 页面以了解受支持的存储驱动。

Device Mapper 是一个基于内核的框架，支撑着 Linux 上的许多高级卷管理技术。Docker 的 `devicemapper` 存储驱动利用了该框架的精简配置和快照功能来管理镜像和容器。本文将 Device Mapper 存储驱动称为 `devicemapper`，将内核框架称为 _Device Mapper_。

对于支持它的系统，`devicemapper` 支持已包含在 Linux 内核中。但是，需要特定的配置才能在 Docker 中使用它。

`devicemapper` 驱动使用专用于 Docker 的块设备，并在块级别而非文件级别运行。这些设备可以通过向 Docker 主机添加物理存储来扩展，并且它们的性能优于在操作系统 (OS) 级别使用文件系统。

## 前置条件

- `devicemapper` 支持在 CentOS、Fedora、SLES 15、Ubuntu、Debian 或 RHEL 上运行的 Docker Engine - Community。
- `devicemapper` 需要安装 `lvm2` 和 `device-mapper-persistent-data` 软件包。
- 更改存储驱动会使您已创建的任何容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您就不必稍后重新创建它们。

## 使用 `devicemapper` 存储驱动配置 Docker

在执行这些步骤之前，您必须首先满足所有[前置条件](#前置条件)。

### 为测试配置 `loop-lvm` 模式

此配置仅适用于测试。`loop-lvm` 模式使用“回环”机制，允许将本地磁盘上的文件作为实际的物理磁盘或块设备进行读写。
然而，回环机制的添加以及与操作系统文件系统层的交互意味着 I/O 操作可能较慢且占用资源。
使用回环设备还可能引入竞争条件。但是，在尝试更复杂的设置以启用 `direct-lvm` 模式之前，设置 `loop-lvm` 模式可以帮助识别基本问题（如缺少用户空间包、内核驱动等）。
因此，`loop-lvm` 模式应仅用于在配置 `direct-lvm` 之前执行基本测试。

对于生产系统，请参阅[为生产配置 direct-lvm 模式](#为生产配置-direct-lvm-模式)。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2.  编辑 `/etc/docker/daemon.json`。如果它尚不存在，请创建它。假设该文件为空，请添加以下内容。

    ```json
    {
      "storage-driver": "devicemapper"
    }
    ```

    请参阅 [daemon 参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中每个存储驱动的所有存储选项。

    如果 `daemon.json` 文件包含格式错误的 JSON，Docker 将无法启动。

3.  启动 Docker。

    ```console
    $ sudo systemctl start docker
    ```

4.  验证守护进程正在使用 `devicemapper` 存储驱动。使用 `docker info` 命令并查找 `Storage Driver`。

    ```console
    $ docker info

      Containers: 0
        Running: 0
        Paused: 0
        Stopped: 0
      Images: 0
      Server Version: 17.03.1-ce
      Storage Driver: devicemapper
      Pool Name: docker-202:1-8413957-pool
      Pool Blocksize: 65.54 kB
      Base Device Size: 10.74 GB
      Backing Filesystem: xfs
      Data file: /dev/loop0
      Metadata file: /dev/loop1
      Data Space Used: 11.8 MB
      Data Space Total: 107.4 GB
      Data Space Available: 7.44 GB
      Metadata Space Used: 581.6 KB
      Metadata Space Total: 2.147 GB
      Metadata Space Available: 2.147 GB
      Thin Pool Minimum Free Space: 10.74 GB
      Udev Sync Supported: true
      Deferred Removal Enabled: false
      Deferred Deletion Enabled: false
      Deferred Deleted Device Count: 0
      Data loop file: /var/lib/docker/devicemapper/data
      Metadata loop file: /var/lib/docker/devicemapper/metadata
      Library Version: 1.02.135-RHEL7 (2016-11-16)
    <...>
    ```

  此主机正在 `loop-lvm` 模式下运行，这在生产系统中**不**受支持。这由 `Data loop file` 和 `Metadata loop file` 在
  `/var/lib/docker/devicemapper` 下的文件指示。这些是回环挂载的稀疏文件。对于生产系统，请参阅
  [为生产配置 direct-lvm 模式](#为生产配置-direct-lvm-模式)。

### 为生产配置 direct-lvm 模式

使用 `devicemapper` 存储驱动的生产主机必须使用 `direct-lvm` 模式。此模式使用块设备创建精简池。这比使用回环设备更快，使用系统资源更高效，并且块设备可以按需增长。但是，与 `loop-lvm` 模式相比，需要更多的设置。

在满足[前置条件](#前置条件)后，请按照以下步骤配置 Docker 以在 `direct-lvm` 模式下使用 `devicemapper` 存储驱动。

> [!WARNING]
> 更改存储驱动会使您已创建的任何容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您就不必稍后重新创建它们。

#### 允许 Docker 配置 direct-lvm 模式

Docker 可以为您管理块设备，简化 `direct-lvm` 模式的配置。**这只适用于全新的 Docker 设置**。您只能使用单个块设备。如果您需要使用多个块设备，
请改为[手动配置 direct-lvm 模式](#手动配置-direct-lvm-模式)。以下新配置选项可用：

| 选项                          | 描述                                                                                                                                                                        | 是否必需 | 默认值 | 示例                            |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------|:--------|:-----------------------------------|
| `dm.directlvm_device`           | 要配置为 `direct-lvm` 的块设备的路径。                                                                                                                        | 是       |         | `dm.directlvm_device="/dev/xvdf"`  |
| `dm.thinp_percent`              | 要从传入的块设备用于存储的空间百分比。                                                                                                        | 否        | 95      | `dm.thinp_percent=95`              |
| `dm.thinp_metapercent`          | 要从传入的块设备用于元数据存储的空间百分比。                                                                                                   | 否        | 1       | `dm.thinp_metapercent=1`           |
| `dm.thinp_autoextend_threshold` | 当 lvm 应自动扩展精简池时的阈值，作为总存储空间的百分比。                                                                   | 否        | 80      | `dm.thinp_autoextend_threshold=80` |
| `dm.thinp_autoextend_percent`   | 触发自动扩展时增加精简池的百分比。                                                                                                       | 否        | 20      | `dm.thinp_autoextend_percent=20`   |
| `dm.directlvm_device_force`     | 是否格式化块设备，即使其上已存在文件系统。如果设置为 `false` 且存在文件系统，则会记录错误并且文件系统保持不变。 | 否        | false   | `dm.directlvm_device_force=true`   |

编辑 `daemon.json` 文件并设置适当的选项，然后重启 Docker 以使更改生效。以下 `daemon.json` 配置设置了上表中的所有选项：

```json
{
  "storage-driver": "devicemapper",
  "storage-opts": [
    "dm.directlvm_device=/dev/xdf",
    "dm.thinp_percent=95",
    "dm.thinp_metapercent=1",
    "dm.thinp_autoextend_threshold=80",
    "dm.thinp_autoextend_percent=20",
    "dm.directlvm_device_force=false"
  ]
}
```

请参阅 [daemon 参考文档](/reference/cli/dockerd/#options-per-storage-driver) 中每个存储驱动的所有存储选项。

重启 Docker 以使更改生效。Docker 会为您调用命令来配置块设备。

> [!WARNING]
> 在 Docker 为您准备块设备后更改这些值不受支持，并会导致错误。

您仍然需要[执行定期维护任务](#管理-devicemapper)。

#### 手动配置 direct-lvm 模式

下面的过程创建了一个配置为精简池的逻辑卷，用作存储池的后端。它假设您在 `/dev/xvdf` 处有一个备用的块设备，有足够的空闲空间来完成任务。
设备标识符和卷大小在您的环境中可能不同，您应该在整个过程中替换您自己的值。该过程还假设 Docker 守护进程处于 `stopped` 状态。

1.  确定您要使用的块设备。该设备位于 `/dev/`（如 `/dev/xvdf`），需要有足够的空闲空间来存储主机运行的工作负载的镜像和容器层。
    固态驱动器是理想选择。

2.  停止 Docker。

    ```console
    $ sudo systemctl stop docker
    ```

3.  安装以下软件包：

    - **RHEL / CentOS**: `device-mapper-persistent-data`, `lvm2` 和所有依赖项

    - **Ubuntu / Debian / SLES 15**: `thin-provisioning-tools`, `lvm2` 和所有依赖项

4.  使用 `pvcreate` 命令在第 1 步的块设备上创建物理卷。将 `/dev/xvdf` 替换为您的设备名称。

    > [!WARNING]
    > 接下来的几个步骤是破坏性的，因此请确保您已指定正确的设备。

    ```console
    $ sudo pvcreate /dev/xvdf

    Physical volume "/dev/xvdf" successfully created.
    ```

5.  在同一设备上使用 `vgcreate` 命令创建一个名为 `docker` 的卷组。

    ```console
    $ sudo vgcreate docker /dev/xvdf

    Volume group "docker" successfully created
    ```

6.  使用 `lvcreate` 命令创建两个名为 `thinpool` 和 `thinpoolmeta` 的逻辑卷。最后一个参数指定允许自动扩展数据或元数据的空闲空间量（如果空间不足），作为临时的权宜之计。这些是推荐值。

    ```console
    $ sudo lvcreate --wipesignatures y -n thinpool docker -l 95%VG

    Logical volume "thinpool" created.

    $ sudo lvcreate --wipesignatures y -n thinpoolmeta docker -l 1%VG

    Logical volume "thinpoolmeta" created.
    ```

7.  使用 `lvconvert` 命令将卷转换为精简池和精简池元数据的存储位置。

    ```console
    $ sudo lvconvert -y \
    --zero n \
    -c 512K \
    --thinpool docker/thinpool \
    --poolmetadata docker/thinpoolmeta

    WARNING: Converting logical volume docker/thinpool and docker/thinpoolmeta to
    thin pool's data and metadata volumes with metadata wiping.
    THIS WILL DESTROY CONTENT OF LOGICAL VOLUME (filesystem etc.)
    Converted docker/thinpool to thin pool.
    ```

8.  通过 `lvm` 配置文件配置精简池的自动扩展。

    ```console
    $ sudo vi /etc/lvm/profile/docker-thinpool.profile
    ```

9.  指定 `thin_pool_autoextend_threshold` 和 `thin_pool_autoextend_percent` 值。

    `thin_pool_autoextend_threshold` 是在 `lvm` 尝试自动扩展可用空间之前使用的空间百分比（100 = 已禁用，不推荐）。

    `thin_pool_autoextend_percent` 是自动扩展时添加到设备的空间量（0 = 已禁用）。

    下面的示例在磁盘使用率达到 80% 时添加 20% 的容量。

    ```text
    activation {
      thin_pool_autoextend_threshold=80
      thin_pool_autoextend_percent=20
    }
    ```

    保存文件。

10. 应用 LVM 配置文件，使用 `lvchange` 命令。

    ```console
    $ sudo lvchange --metadataprofile docker-thinpool docker/thinpool

    Logical volume docker/thinpool changed.
    ```

11. 确保启用了逻辑卷的监控。

    ```console
    $ sudo lvs -o+seg_monitor

    LV       VG     Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert Monitor
    thinpool docker twi-a-t--- 95.00g             0.00   0.01                             not monitored
    ```

    如果 `Monitor` 列中的输出如上所述报告卷为 `not monitored`，则需要显式启用监控。如果没有此步骤，无论应用的配置文件中的设置如何，都不会发生逻辑卷的自动扩展。

    ```console
    $ sudo lvchange --monitor y docker/thinpool
    ```

    通过再次运行 `sudo lvs -o+seg_monitor` 命令来双重检查监控是否已启用。`Monitor` 列现在应报告逻辑卷正在被 `monitored`。

12. 如果您之前在此主机上运行过 Docker，或者 `/var/lib/docker/` 存在，请将其移开，以便 Docker 可以使用新的 LVM 池来存储镜像和容器的内容。

    ```console
    $ sudo su -
    # mkdir /var/lib/docker.bk
    # mv /var/lib/docker/* /var/lib/docker.bk
    # exit
    ```

    如果以下任何步骤失败并且您需要恢复，您可以删除 `/var/lib/docker` 并用 `/var/lib/docker.bk` 替换它。

13. 编辑 `/etc/docker/daemon.json` 并配置 `devicemapper` 存储驱动所需的选项。如果文件之前为空，现在应包含以下内容：

    ```json
    {
        "storage-driver": "devicemapper",
        "storage-opts": [
        "dm.thinpooldev=/dev/mapper/docker-thinpool",
        "dm.use_deferred_removal=true",
        "dm.use_deferred_deletion=true"
        ]
    }
    ```

14. 启动 Docker。

    **systemd**:

    ```console
    $ sudo systemctl start docker
    ```

    **service**:

    ```console
    $ sudo service docker start
    ```

15. 使用 `docker info` 验证 Docker 正在使用新配置。

    ```console
    $ docker info

    Containers: 0
     Running: 0
     Paused: 0
     Stopped: 0
    Images: 0
    Server Version: 17.03.1-ce
    Storage Driver: devicemapper
     Pool Name: docker-thinpool
     Pool Blocksize: 524.3 kB
     Base Device Size: 10.74 GB
     Backing Filesystem: xfs
     Data file:
     Metadata file:
     Data Space Used: 19.92 MB
     Data Space Total: 102 GB
     Data Space Available: 102 GB
     Metadata Space Used: 147.5 kB
     Metadata Space Total: 1.07 GB
     Metadata Space Available: 1.069 GB
     Thin Pool Minimum Free Space: 10.2 GB
     Udev Sync Supported: true
     Deferred Removal Enabled: true
     Deferred Deletion Enabled: true
     Deferred Deleted Device Count: 0
     Library Version: 1.02.135-RHEL7 (2016-11-16)
    <...>
    ```

    如果 Docker 配置正确，`Data file` 和 `Metadata file` 为空，并且池名为 `docker-thinpool`。

16. 在验证配置正确后，您可以删除包含先前配置的 `/var/lib/docker.bk` 目录。

    ```console
    $ sudo rm -rf /var/lib/docker.bk
    ```

## 管理 devicemapper

### 监控精简池

不要仅依赖 LVM 自动扩展。卷组会自动扩展，但卷仍可能填满。您可以使用 `lvs` 或 `lvs -a` 监控卷上的空闲空间。考虑在操作系统级别使用监控工具，如 Nagios。

要查看 LVM 日志，您可以使用 `journalctl`：

```console
$ sudo journalctl -fu dm-event.service
```

如果您遇到精简池的重复问题，您可以在 `/etc/docker/daemon.json` 中设置存储选项 `dm.min_free_space` 为一个值（表示百分比）。例如，将其设置为 `10` 确保当空闲空间接近 10% 时操作会以警告失败。请参阅 [Engine 守护进程参考中的