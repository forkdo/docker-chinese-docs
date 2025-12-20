# Device Mapper 存储驱动程序（已弃用）

> **已弃用**
>
> Device Mapper 驱动程序[已被弃用](/manuals/engine/deprecated.md#device-mapper-storage-driver)，
> 并已在 Docker Engine v25.0 中移除。如果您正在使用 Device Mapper，
> 必须在升级到 Docker Engine v25.0 之前迁移到受支持的存储驱动程序。
> 请阅读 [Docker 存储驱动程序](select-storage-driver.md)页面以了解受支持的存储驱动程序。

Device Mapper 是一个基于内核的框架，支撑着 Linux 上许多高级卷管理技术。Docker 的 `devicemapper` 存储驱动程序利用此框架的精简配置和快照功能进行镜像和容器管理。本文将 Device Mapper 存储驱动程序称为 `devicemapper`，将内核框架称为 _Device Mapper_。

在受支持的系统上，`devicemapper` 支持包含在 Linux 内核中。但是，需要特定配置才能将其与 Docker 一起使用。

`devicemapper` 驱动程序使用专用于 Docker 的块设备，并在块级别而非文件级别运行。这些设备可以通过向 Docker 主机添加物理存储来扩展，并且它们比在操作系统 (OS) 级别使用文件系统性能更好。

## 先决条件

- `devicemapper` 支持在 CentOS、Fedora、SLES 15、Ubuntu、Debian 或 RHEL 上运行的 Docker Engine - Community。
- `devicemapper` 需要安装 `lvm2` 和 `device-mapper-persistent-data` 软件包。
- 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您以后就不需要重新创建它们。

## 使用 `devicemapper` 存储驱动程序配置 Docker

在执行以下步骤之前，您必须首先满足所有[先决条件](#先决条件)。

### 为测试配置 `loop-lvm` 模式

此配置仅适用于测试。`loop-lvm` 模式利用“环回”机制，允许将本地磁盘上的文件当作实际的物理磁盘或块设备进行读写。
但是，环回机制的增加以及与操作系统文件系统层的交互意味着 IO 操作可能很慢且资源密集。使用环回设备也可能引入竞争条件。
但是，设置 `loop-lvm` 模式可以帮助在尝试更复杂的设置（以启用 `direct-lvm` 模式）之前识别基本问题（例如缺少用户空间包、内核驱动程序等）。因此，`loop-lvm` 模式应仅用于在配置 `direct-lvm` 之前执行基本测试。

对于生产系统，请参阅[为生产配置 direct-lvm 模式](#为生产配置-direct-lvm-模式)。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2. 编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件为空，请添加以下内容。

    ```json
    {
      "storage-driver": "devicemapper"
    }
    ```

    请参阅 [daemon 参考文档](/reference/cli/dockerd/#options-per-storage-driver)中每种存储驱动程序的所有存储选项。

    如果 `daemon.json` 文件包含格式错误的 JSON，Docker 将不会启动。

3. 启动 Docker。

    ```console
    $ sudo systemctl start docker
    ```

4. 验证守护程序是否正在使用 `devicemapper` 存储驱动程序。使用 `docker info` 命令并查找 `Storage Driver`。

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

  此主机正在 `loop-lvm` 模式下运行，该模式在生产系统上**不受支持**。这由 `Data loop file` 和 `Metadata loop file` 位于 `/var/lib/docker/devicemapper` 下的文件中这一事实表明。这些是环回安装的稀疏文件。对于生产系统，请参阅[为生产配置 direct-lvm 模式](#为生产配置-direct-lvm-模式)。

### 为生产配置 direct-lvm 模式

使用 `devicemapper` 存储驱动程序的生产主机必须使用 `direct-lvm` 模式。此模式使用块设备创建精简池。这比使用环回设备更快，更有效地利用系统资源，并且块设备可以根据需要增长。但是，与 `loop-lvm` 模式相比，需要更多的设置。

在满足[先决条件](#先决条件)后，请按照以下步骤配置 Docker 以在 `direct-lvm` 模式下使用 `devicemapper` 存储驱动程序。

> [!WARNING]
> 更改存储驱动程序会使您已创建的任何容器在本地系统上无法访问。使用 `docker save` 保存容器，并将现有镜像推送到 Docker Hub 或私有仓库，这样您以后就不需要重新创建它们。

#### 允许 Docker 配置 direct-lvm 模式

Docker 可以为您管理块设备，从而简化 `direct-lvm` 模式的配置。**这仅适用于全新的 Docker 安装。** 您只能使用单个块设备。如果您需要使用多个块设备，请改为[手动配置 direct-lvm 模式](#手动配置-direct-lvm-模式)。提供以下新的配置选项：

| 选项                          | 描述                                                                                                                                 | 是否必需？ | 默认值 | 示例                               |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:----------|:--------|:-----------------------------------|
| `dm.directlvm_device`           | 用于配置 `direct-lvm` 的块设备的路径。                                                                                              | 是        |         | `dm.directlvm_device="/dev/xvdf"`  |
| `dm.thinp_percent`              | 从传入的块设备中用于存储的空间百分比。                                                                                              | 否        | 95      | `dm.thinp_percent=95`              |
| `dm.thinp_metapercent`          | 从传入的块设备中用于元数据存储的空间百分比。                                                                                        | 否        | 1       | `dm.thinp_metapercent=1`           |
| `dm.thinp_autoextend_threshold` | lvm 应自动扩展精简池的阈值，占总存储空间的百分比。                                                                                  | 否        | 80      | `dm.thinp_autoextend_threshold=80` |
| `dm.thinp_autoextend_percent`   | 当触发自动扩展时，精简池增加的百分比。                                                                                              | 否        | 20      | `dm.thinp_autoextend_percent=20`   |
| `dm.directlvm_device_force`     | 即使块设备上已存在文件系统，是否也要格式化它。如果设置为 `false` 且存在文件系统，则会记录错误并且文件系统保持原样。                  | 否        | false   | `dm.directlvm_device_force=true`   |

编辑 `daemon.json` 文件并设置适当的选项，然后重新启动 Docker 以使更改生效。以下 `daemon.json` 配置设置了上表中的所有选项。

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

请参阅 [daemon 参考文档](/reference/cli/dockerd/#options-per-storage-driver)中每种存储驱动程序的所有存储选项。

重新启动 Docker 以使更改生效。Docker 调用命令为您配置块设备。

> [!WARNING]
> Docker 为您准备好块设备后，更改这些值不受支持，并会导致错误。

您仍然需要[执行定期维护任务](#管理-devicemapper)。

#### 手动配置 direct-lvm 模式

以下过程创建一个配置为精简池的逻辑卷，用作存储池的后备。它假设您在 `/dev/xvdf` 处有一个备用块设备，该设备有足够的可用空间来完成任务。设备标识符和卷大小在您的环境中可能不同，您应在整个过程中替换为您自己的值。该过程还假设 Docker 守护程序处于 `stopped` 状态。

1.  识别您要使用的块设备。该设备位于 `/dev/` 下（例如 `/dev/xvdf`），并且需要足够的可用空间来存储主机运行工作负载的镜像和容器层。固态驱动器是理想的选择。

2.  停止 Docker。

    ```console
    $ sudo systemctl stop docker
    ```

3.  安装以下软件包：

    - **RHEL / CentOS**：`device-mapper-persistent-data`、`lvm2` 及其所有依赖项

    - **Ubuntu / Debian / SLES 15**：`thin-provisioning-tools`、`lvm2` 及其所有依赖项

4.  使用 `pvcreate` 命令在步骤 1 中的块设备上创建物理卷。将您的设备名称替换为 `/dev/xvdf`。

    > [!WARNING]
    > 接下来的几个步骤具有破坏性，因此请确保您指定了正确的设备。

    ```console
    $ sudo pvcreate /dev/xvdf

    Physical volume "/dev/xvdf" successfully created.
    ```

5.  使用 `vgcreate` 命令在同一设备上创建一个 `docker` 卷组。

    ```console
    $ sudo vgcreate docker /dev/xvdf

    Volume group "docker" successfully created
    ```

6.  使用 `lvcreate` 命令创建两个名为 `thinpool` 和 `thinpoolmeta` 的逻辑卷。最后一个参数指定允许用于数据或元数据自动扩展的可用空间量（以防空间不足），作为临时的权宜之计。这些是推荐值。

    ```console
    $ sudo lvcreate --wipesignatures y -n thinpool docker -l 95%VG

    Logical volume "thinpool" created.

    $ sudo lvcreate --wipesignatures y -n thinpoolmeta docker -l 1%VG

    Logical volume "thinpoolmeta" created.
    ```

7.  使用 `lvconvert` 命令将卷转换为精简池和用于精简池元数据的存储位置。

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

    `thin_pool_autoextend_threshold` 是在 `lvm` 尝试自动扩展可用空间之前已使用空间的百分比（100 = 禁用，不推荐）。

    `thin_pool_autoextend_percent` 是自动扩展时添加到设备的空间量（0 = 禁用）。

    下面的示例在磁盘使用率达到 80% 时增加 20% 的容量。

    ```text
    activation {
      thin_pool_autoextend_threshold=80
      thin_pool_autoextend_percent=20
    }
    ```

    保存文件。

10. 使用 `lvchange` 命令应用 LVM 配置文件。

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

    如果 `Monitor` 列的输出如上所示，报告卷是 `not monitored`（未监控），则需要显式启用监控。没有此步骤，逻辑卷的自动扩展将不会发生，无论应用的配置文件中有任何设置。

    ```console
    $ sudo lvchange --monitor y docker/thinpool
    ```

    再次运行 `sudo lvs -o+seg_monitor` 命令，仔细检查监控是否已启用。`Monitor` 列现在应报告逻辑卷正在被 `monitored`（监控）。

12. 如果您之前曾在此主机上运行过 Docker，或者 `/var/lib/docker/` 存在，请将其移开，以便 Docker 可以使用新的 LVM 池来存储镜像和容器的内容。

    ```console
    $ sudo su -
    # mkdir /var/lib/docker.bk
    # mv /var/lib/docker/* /var/lib/docker.bk
    # exit
    ```

    如果以下任何步骤失败并且您需要恢复，可以删除 `/var/lib/docker` 并用 `/var/lib/docker.bk` 替换它。

13. 编辑 `/etc/docker/daemon.json` 并配置 `devicemapper` 存储驱动程序所需的选项。如果该文件之前为空，它现在应包含以下内容：

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

    **systemd**：

    ```console
    $ sudo systemctl start docker
    ```

    **service**：

    ```console
    $ sudo service docker start
    ```

15. 使用 `docker info` 验证 Docker 是否正在使用新配置。

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

    如果 Docker 配置正确，`Data file` 和 `Metadata file` 为空，并且池名称为 `docker-thinpool`。

16. 验证配置正确后，可以删除包含先前配置的 `/var/lib/docker.bk` 目录。

    ```console
    $ sudo rm -rf /var/lib/docker.bk
    ```

## 管理 devicemapper

### 监控精简池

不要仅依赖 LVM 自动扩展。卷组会自动扩展，但卷仍可能被填满。您可以使用 `lvs` 或 `lvs -a` 监控卷上的可用空间。考虑在操作系统级别使用监控工具，例如 Nagios。

要查看 LVM 日志，您可以使用 `journalctl`：

```console
$ sudo journalctl -fu dm-event.service
```

如果您反复遇到精简池的问题，可以在 `/etc/docker/daemon.json` 中将存储选项 `dm.min_free_space` 设置为一个值（代表百分比）。例如，将其设置为 `10` 可确保当可用空间达到或接近 10% 时，操作会失败并发出警告。请参阅 [Engine daemon 参考中的存储驱动程序选项](/reference/cli/dockerd/#daemon-storage-driver)。

### 增加正在运行的设备的容量

您可以增加正在运行的精简池设备的池容量。如果数据的逻辑卷已满且卷组已达到最大容量，这非常有用。具体过程取决于您使用的是 [loop-lvm 精简池](#调整-loop-lvm-精简池的大小)还是 [direct-lvm 精简池](#调整-direct-lvm-精简池的大小)。

#### 调整 loop-lvm 精简池的大小

调整 `loop-lvm` 精简池大小的最简单方法是[使用 device_tool 实用程序](#使用-device_tool-实用程序)，但您也可以改为[使用操作系统实用程序](#使用操作系统实用程序)。

##### 使用 device_tool 实用程序

一个名为 `device_tool.go` 的社区贡献脚本可在 [moby/moby](https://github.com/moby/moby/tree/master/contrib/docker-device-tool) Github 仓库中找到。您可以使用此工具调整 `loop-lvm` 精简池的大小，从而避免上述漫长的过程。不能保证此工具有效，但您应该仅在非生产系统上使用 `loop-lvm`。

如果您不想使用 `device_tool`，可以改为[手动调整精简池的大小](#使用操作系统实用程序)。

1.  要使用该工具，请克隆 Github 仓库，切换到 `contrib/docker-device-tool`，然后按照 `README.md` 中的说明编译该工具。

2.  使用该工具。以下示例将精简池大小调整为 200GB。

    ```console
    $ ./device_tool resize 200GB
    ```

##### 使用操作系统实用程序

如果您不想[使用 device-tool 实用程序](#使用-device_tool-实用程序)，可以使用以下过程手动调整 `loop-lvm` 精简池的大小。

在 `loop-lvm` 模式下，使用一个环回设备存储数据，另一个环回设备存储元数据。`loop-lvm` 模式仅受支持用于测试，因为它具有显著的性能和稳定性缺陷。

如果您正在使用 `loop-lvm` 模式，`docker info` 的输出会显示 `Data loop file` 和 `Metadata loop file` 的文件路径：

```console
$ docker info |grep 'loop file'

 Data loop file: /var/lib/docker/devicemapper/data
 Metadata loop file: /var/lib/docker/devicemapper/metadata
```

请按照以下步骤增加精简池的大小。在此示例中，精简池为 100 GB，并增加到 200 GB。

1.  列出设备的大小。

    ```console
    $ sudo ls -lh /var/lib/docker/devicemapper/

    total 1175492
    -rw------- 1 root root 100G Mar 30 05:22 data
    -rw------- 1 root root 2.0G Mar 31 11:17 metadata
    ```

2.  使用 `truncate` 命令将 `data` 文件的大小增加到 200 G，该命令用于增加**或**减小文件大小。请注意，减小大小是破坏性操作。

    ```console
    $ sudo truncate -s 200G /var/lib/docker/devicemapper/data
    ```

3.  验证文件大小是否已更改。

    ```console
    $ sudo ls -lh /var/lib/docker/devicemapper/

    total 1.2G
    -rw------- 1 root root 200G Apr 14 08:47 data
    -rw------- 1 root root 2.0G Apr 19 13:27 metadata
    ```

4.  环回文件已在磁盘上更改，但在内存中尚未更改。列出内存中环回设备的大小（以 GB 为单位）。重新加载它，然后再次列出大小。重新加载后，大小为 200 GB。

    ```console
    $ echo $[ $(sudo blockdev --getsize64 /dev/loop0) / 1024 / 1024 / 1024 ]

    100

    $ sudo losetup -c /dev/loop0

    $ echo $[ $(sudo blockdev --getsize64 /dev/loop0) / 1024 / 1024 / 1024 ]

    200
    ```

5.  重新加载 devicemapper 精简池。

    a. 首先获取池名称。池名称是第一个字段，以 `:` 分隔。此命令提取它。

    ```console
    $ sudo dmsetup status | grep ' thin-pool ' | awk -F ': ' {'print $1'}
    docker-8:1-123141-pool
    ```

    b. 转储精简池的设备映射器表。

    ```console
    $ sudo dmsetup table docker-8:1-123141-pool
    0 209715200 thin-pool 7:1 7:0 128 32768 1 skip_block_zeroing
    ```

    c. 使用输出的第二个字段计算精简池的总扇区数。该数字以 512-k 扇区表示。一个 100G 的文件有 209715200 个 512-k 扇区。如果您将此数字加倍到 200G，您将得到 419430400 个 512-k 扇区。

    d. 使用以下三个 `dmsetup` 命令，使用新的扇区数重新加载精简池。

    ```console
    $ sudo dmsetup suspend docker-8:1-123141-pool
    $ sudo dmsetup reload docker-8:1-123141-pool --table '0 419430400 thin-pool 7:1 7:0 128 32768 1 skip_block_zeroing'
    $ sudo dmsetup resume docker-8:1-123141-pool
    ```

#### 调整 direct-lvm 精简池的大小

要扩展 `direct-lvm` 精简池，您需要首先将一个新块设备附加到 Docker 主机，并记下内核分配给它的名称。在此示例中，新块设备是 `/dev/xvdg`。

请按照此过程扩展 `direct-lvm` 精简池，替换您的块设备和其他参数以适应您的情况。

1.  收集有关卷组的信息。

    使用 `pvdisplay` 命令查找精简池当前使用的物理块设备以及卷组的名称。

    ```console
    $ sudo pvdisplay |grep 'VG Name'

    PV Name               /dev/xvdf
    VG Name               docker
    ```

    在以下步骤中，请根据需要替换您的块设备或卷组名称。

2.  使用 `vgextend` 命令扩展卷组，使用上一步中的 `VG Name` 和您的**新**块设备的名称。

    ```console
    $ sudo vgextend docker /dev/xvdg

    Physical volume "/dev/xvdg" successfully created.
    Volume group "docker" successfully extended
    ```

3.  扩展 `docker/thinpool` 逻辑卷。此命令立即使用 100% 的卷，无需自动扩展。要扩展元数据精简池，请使用 `docker/thinpool_tmeta`。

    ```console
    $ sudo lvextend -l+100%FREE -n docker/thinpool

    Size of logical volume docker/thinpool_tdata changed from 95.00 GiB (24319 extents) to 198.00 GiB (50688 extents).
    Logical volume docker/thinpool_tdata successfully resized.
    ```

4.  使用 `docker info` 输出中的 `Data Space Available` 字段验证新的精简池大小。如果您扩展了 `docker/thinpool_tmeta` 逻辑卷，请查找 `Metadata Space Available`。

    ```bash
    Storage Driver: devicemapper
     Pool Name: docker-thinpool
     Pool Blocksize: 524.3 kB
     Base Device Size: 10.74 GB
     Backing Filesystem: xfs
     Data file:
     Metadata file:
     Data Space Used: 212.3 MB
     Data Space Total: 212.6 GB
     Data Space Available: 212.4 GB
     Metadata Space Used: 286.7 kB
     Metadata Space Total: 1.07 GB
     Metadata Space Available: 1.069 GB
    <...>
    ```

### 重启后激活 `devicemapper`

如果您重新启动主机并发现 `docker` 服务启动失败，请查找错误“Non existing device”。您需要使用以下命令重新激活逻辑卷：

```console
$ sudo lvchange -ay docker/thinpool
```

## `devicemapper` 存储驱动程序的工作原理

> [!WARNING]
> 请勿直接操作 `/var/lib/docker/` 中的任何文件或目录。这些文件和目录由 Docker 管理。

使用 `lsblk` 命令从操作系统的角度查看设备及其池：

```console
$ sudo lsblk

NAME                    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
xvda                    202:0    0    8G  0 disk
└─xvda1                 202:1    0    8G  0 part /
xvdf                    202:80   0  100G  0 disk
├─docker-thinpool_tmeta 253:0    0 1020M  0 lvm
│ └─docker-thinpool     253:2    0   95G  0 lvm
└─docker-thinpool_tdata 253:1    0   95G  0 lvm
  └─docker-thinpool     253:2    0   95G  0 lvm
```

使用 `mount` 命令查看 Docker 正在使用的挂载点：

```console
$ mount |grep devicemapper
/dev/xvda1 on /var/lib/docker/devicemapper type xfs (rw,relatime,seclabel,attr2,inode64,noquota)
```

当您使用 `devicemapper` 时，Docker 将镜像和层内容存储在精简池中，并通过将它们挂载到 `/var/lib/docker/devicemapper/` 的子目录下，将它们暴露给容器。

### 磁盘上的镜像和容器层

`/var/lib/docker/devicemapper/metadata/` 目录包含有关 Devicemapper 配置本身以及存在的每个镜像和容器层的元数据。`devicemapper` 存储驱动程序使用快照，这些元数据包括有关这些快照的信息。这些文件采用 JSON 格式。

`/var/lib/docker/devicemapper/mnt/` 目录包含每个存在的镜像和容器层的挂载点。镜像层挂载点为空，但容器的挂载点显示从容器内部看到的容器文件系统。

### 镜像分层和共享

`devicemapper` 存储驱动程序使用专用的块设备而不是格式化的文件系统，并在块级别操作文件以在写时复制 (CoW) 操作期间获得最佳性能。

#### 快照

`devicemapper` 的另一个特性是使用快照（有时也称为_精简设备_或_虚拟设备_），它们以非常小、轻量级的精简池存储每层引入的差异。快照提供了许多好处：

- 容器之间共享的层仅在磁盘上存储一次，除非它们是可写的。例如，如果您有 10 个不同的镜像都基于 `alpine`，则 `alpine` 镜像及其所有父镜像在磁盘上仅存储一次。

- 快照是写时复制 (CoW) 策略的实现。这意味着只有当文件或目录被容器修改或删除时，才会将其复制到容器的可写层。

- 因为 `devicemapper` 在块级别运行，所以可写层中的多个块可以同时修改。

- 可以使用标准操作系统级别的备份实用程序备份快照。只需复制 `/var/lib/docker/devicemapper/` 即可。

#### Devicemapper 工作流程

当您使用 `devicemapper` 存储驱动程序启动 Docker 时，所有与镜像和容器层相关的对象都存储在 `/var/lib/docker/devicemapper/` 中，该目录由一个或多个块级设备（环回设备（仅用于测试）或物理磁盘）支持。

- _基础设备_是最低级别的对象。这是精简池本身。您可以使用 `docker info` 检查它。它包含一个文件系统。此基础设备是每个镜像和容器层的起点。基础设备是 Device Mapper 实现细节，而不是 Docker 层。

- 有关基础设备和每个镜像或容器层的元数据以 JSON 格式存储在 `/var/lib/docker/devicemapper/metadata/` 中。这些层是写时复制快照，这意味着在它们与父层分叉之前它们是空的。

- 每个容器的可写层挂载在 `/var/lib/docker/devicemapper/mnt/` 中的挂载点上。每个只读镜像层和每个已停止的容器都存在一个空目录。

每个镜像层都是其下方层的快照。每个镜像的最低层是池中存在的基础设备的快照。当您运行容器时，它是容器所基于镜像的快照。以下示例显示了一个 Docker 主机，其中有两个正在运行的容器。第一个是 `ubuntu` 容器，第二个是 `busybox` 容器。

![Ubuntu 和 busybox 镜像层](images/two_dm_container.webp?w=450&h=100)

## 容器读写如何与 `devicemapper` 配合工作

### 读取文件

使用 `devicemapper` 时，读取发生在块级别。下图显示了在示例容器中读取单个块 (`0x44f`) 的高级过程。

![使用 devicemapper 读取块](images/dm_container.webp?w=650)

应用程序请求读取容器中的块 `0x44f`。因为容器是镜像的精简快照，它没有该块，但它有一个指向最近父镜像中该块的指针，并从那里读取该块。该块现在存在于容器的内存中。

### 写入文件

**写入新文件**：使用 `devicemapper` 驱动程序，将新数据写入容器是通过*按需分配*操作完成的。新文件的每个块都分配在容器的可写层中，并且该块被写入那里。

**更新现有文件**：从文件存在的最近层读取文件的相关块。当容器写入文件时，只有修改的块才会写入容器的可写层。

**删除文件或目录**：当您在容器的可写层中删除文件或目录时，或者当镜像层删除其父层中存在的文件时，`devicemapper` 存储驱动程序会拦截对该文件或目录的进一步读取尝试，并响应文件或目录不存在。

**写入然后删除文件**：如果容器写入文件然后删除该文件，所有这些操作都发生在容器的可写层中。在这种情况下，如果您使用 `direct-lvm`，则会释放块。如果您使用 `loop-lvm`，则可能不会释放块。这是不在生产中使用 `loop-lvm` 的另一个原因。

## Device Mapper 和 Docker 性能

- **`allocate-on demand` 性能影响**：

  `devicemapper` 存储驱动程序使用 `allocate-on-demand` 操作从精简池中将新块分配到容器的可写层。每个块为 64KB，因此这是写入使用的最小空间量。

- **写时复制性能影响**：容器第一次修改特定块时，该块会被写入容器的可写层。因为这些写入发生在块级别而不是文件级别，所以性能影响被最小化。但是，写入大量块仍然会对性能产生负面影响，并且 `devicemapper` 存储驱动程序在此场景下实际上可能比其他存储驱动程序性能更差。对于写入密集型工作负载，您应使用数据卷，这会完全绕过存储驱动程序。

### 性能最佳实践

请牢记以下几点，以在使用 `devicemapper` 存储驱动程序时最大化性能。

- **使用 `direct-lvm`**：`loop-lvm` 模式性能不佳，绝不应在生产中使用。

- **使用快速存储**：固态驱动器 (SSD) 比旋转磁盘提供更快的读写速度。

- **内存使用**：`devicemapper` 比某些其他存储驱动程序使用更多内存。每个启动的容器都会将其文件的一个或多个副本加载到内存中，具体取决于同时修改的同一文件的块数。由于内存压力，在高密度用例中，`devicemapper` 存储驱动程序可能不是某些工作负载的正确选择。

- **对写入密集型工作负载使用卷**：卷为写入密集型工作负载提供最佳和最可预测的性能。这是因为它们绕过存储驱动程序，并且不会产生由精简配置和写时复制引入的任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并在没有正在运行的容器使用它们时持久保存。

  > [!NOTE]
  >
  > 当使用 `dev
