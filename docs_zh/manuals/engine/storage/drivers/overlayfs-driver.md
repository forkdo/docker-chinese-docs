---
description: 了解如何优化 OverlayFS 驱动的使用。
keywords: 容器, 存储, 驱动, OverlayFS, overlay2, overlay
title: OverlayFS 存储驱动
aliases:
  - /storage/storagedriver/overlayfs-driver/
---

OverlayFS 是一个联合文件系统。

本文档将 Linux 内核驱动称为 `OverlayFS`，将 Docker 存储驱动称为 `overlay2`。

> [!NOTE]
> Docker Engine 29.0 及更高版本默认使用 [containerd 镜像存储](/manuals/engine/storage/containerd.md)。
> `overlay2` 驱动是一个旧版存储驱动，已被 `overlayfs` containerd 快照器取代。
> 有关详细信息，请参阅 [选择存储驱动](/manuals/engine/storage/drivers/select-storage-driver.md)。

> [!NOTE]
> 有关 `fuse-overlayfs` 驱动，请查看 [无根模式文档](/manuals/engine/security/rootless.md)。

## 前提条件

使用 `overlay2` 驱动需要满足以下前提条件：

- Linux 内核版本 4.0 或更高，或者使用内核版本 3.10.0-514 或更高的 RHEL 或 CentOS。
- `overlay2` 驱动在 `xfs` 底层文件系统上受支持，但仅在启用了 `d_type=true` 时支持。

  使用 `xfs_info` 验证 `ftype` 选项是否设置为 `1`。要正确格式化 `xfs` 文件系统，请使用标志 `-n ftype=1`。

- 更改存储驱动会使本地系统上现有的容器和镜像无法访问。
  在更改存储驱动之前，请使用 `docker save` 保存您构建的任何镜像，或将其推送到 Docker Hub 或私有注册表，以便稍后无需重新创建它们。

## 使用 `overlay2` 存储驱动配置 Docker

<a name="configure-docker-with-the-overlay-or-overlay2-storage-driver"></a>

在执行此过程之前，您必须首先满足所有 [前提条件](#prerequisites)。

以下步骤概述了如何配置 `overlay2` 存储驱动。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2. 将 `/var/lib/docker` 的内容复制到临时位置。

   ```console
   $ cp -au /var/lib/docker /var/lib/docker.bk
   ```

3. 如果您想使用与 `/var/lib/` 不同的底层文件系统，请格式化文件系统并将其挂载到 `/var/lib/docker`。
   确保将此挂载添加到 `/etc/fstab` 以使其永久化。

4. 编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。
   假设文件为空，请添加以下内容。

   ```json
   {
     "storage-driver": "overlay2"
   }
   ```

   如果 `daemon.json` 文件包含无效的 JSON，Docker 将无法启动。

5. 启动 Docker。

   ```console
   $ sudo systemctl start docker
   ```

6. 验证守护进程正在使用 `overlay2` 存储驱动。
   使用 `docker info` 命令并查找 `Storage Driver` 和 `Backing filesystem`。

   ```console
   $ docker info

   Containers: 0
   Images: 0
   Storage Driver: overlay2
    Backing Filesystem: xfs
    Supports d_type: true
    Native Overlay Diff: true
   <...>
   ```

Docker 现在正在使用 `overlay2` 存储驱动，并已自动创建具有所需 `lowerdir`、`upperdir`、`merged` 和 `workdir` 结构的 overlay 挂载。

继续阅读以了解 OverlayFS 在您的 Docker 容器中的工作原理，以及有关其与不同底层文件系统的兼容性限制的性能建议和信息。

## `overlay2` 驱动的工作原理

OverlayFS 在单个 Linux 主机上叠加两个目录，并将它们显示为单个目录。这些目录称为层，统一过程称为联合挂载。OverlayFS 将较低的目录称为 `lowerdir`，较高的目录称为 `upperdir`。统一视图通过其自己的目录 `merged` 暴露。

`overlay2` 驱动原生支持最多 128 个较低的 OverlayFS 层。此功能为与层相关的 Docker 命令（如 `docker build` 和 `docker commit`）提供了更好的性能，并在底层文件系统上消耗更少的 inode。

### 磁盘上的镜像和容器层

使用 `docker pull ubuntu` 下载五层镜像后，您可以在 `/var/lib/docker/overlay2` 下看到六个目录。

> [!WARNING]
>
> 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay2

total 24
drwx------ 5 root root 4096 Jun 20 07:36 223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7
drwx------ 3 root root 4096 Jun 20 07:36 3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b
drwx------ 5 root root 4096 Jun 20 07:36 4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1
drwx------ 5 root root 4096 Jun 20 07:36 e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5
drwx------ 5 root root 4096 Jun 20 07:36 eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed
drwx------ 2 root root 4096 Jun 20 07:36 l
```

新的 `l` 目录（小写 `L`）包含作为符号链接的缩短层标识符。这些标识符用于避免在 `mount` 命令的参数上命中页面大小限制。

```console
$ ls -l /var/lib/docker/overlay2/l

total 20
lrwxrwxrwx 1 root root 72 Jun 20 07:36 6Y5IM2XC7TSNIJZZFLJCS6I4I4 -> ../3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 B3WWEFKBG3PLLV737KZFIASSW7 -> ../4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 JEYMODZYFCZFYSDABYXD5MF6YO -> ../eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 NFYKDW6APBCCUCTOUSYDH4DXAT -> ../223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 UL2MW33MSE3Q5VYIKBRN4ZAGQP -> ../e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5/diff
```

最低层包含一个名为 `link` 的文件，其中包含缩短的标识符名称，以及一个名为 `diff` 的目录，其中包含该层的内容。

```console
$ ls /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/

diff  link

$ cat /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/link

6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls  /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff

bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

第二低层及每个更高层都包含一个名为 `lower` 的文件，表示其父层，以及一个名为 `diff` 的目录，包含其内容。它还包含一个 `merged` 目录，包含其父层和自身的统一内容，以及一个 `work` 目录，由 OverlayFS 内部使用。

```console
$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7

diff  link  lower  merged  work

$ cat /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/lower

l/6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff/

etc  sbin  usr  var
```

要查看使用 `overlay` 存储驱动与 Docker 时存在的挂载，请使用 `mount` 命令。以下输出为便于阅读已截断。

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/merged
type overlay (rw,relatime,
lowerdir=l/DJA75GUWHWG7EWICFYX54FIOVT:l/B3WWEFKBG3PLLV737KZFIASSW7:l/JEYMODZYFCZFYSDABYXD5MF6YO:l/UL2MW33MSE3Q5VYIKBRN4ZAGQP:l/NFYKDW6APBCCUCTOUSYDH4DXAT:l/6Y5IM2XC7TSNIJZZFLJCS6I4I4,
upperdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/diff,
workdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/work)
```

第二行的 `rw` 显示 `overlay` 挂载是读写模式的。

下图显示了 Docker 镜像和 Docker 容器是如何分层的。镜像层是 `lowerdir`，容器层是 `upperdir`。如果镜像有多个层，会使用多个 `lowerdir` 目录。统一视图通过一个名为 `merged` 的目录暴露，这实际上是容器的挂载点。

![Docker 构造如何映射到 OverlayFS 构造](images/overlay_constructs.webp)

当镜像层和容器层包含相同文件时，容器层 (`upperdir`) 优先，并遮蔽镜像层中相同文件的存在。

要创建容器，`overlay2` 驱动会组合表示镜像顶层的目录和容器的新目录。镜像的层是 overlay 的 `lowerdirs`，并且是只读的。容器的新目录是 `upperdir`，并且是可写的。

### 磁盘上的镜像和容器层

以下 `docker pull` 命令显示 Docker 主机下载一个由五层组成的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu

5ba4f30e5bea: Pull complete
9d7d19c9dc56: Pull complete
ac6ad7efd0f9: Pull complete
e7491a747824: Pull complete
a3ed95caeb02: Pull complete
Digest: sha256:46fb5d001b88ad904c5c732b086b596b92cfb4a4840a3abd0e35dbb6870585e4
Status: Downloaded newer image for ubuntu:latest
```

#### 镜像层

每个镜像层在 `/var/lib/docker/overlay/` 中都有自己的目录，其中包含其内容，如下例所示。镜像层 ID 与目录 ID 不对应。

> [!WARNING]
>
> 不要直接操作 `/var/lib/docker/` 内的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay/

total 20
drwx------ 3 root root 4096 Jun 20 16:11 38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8
drwx------ 3 root root 4096 Jun 20 16:11 55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
drwx------ 3 root root 4096 Jun 20 16:11 824c8a961a4f5e8fe4f4243dab57c5be798e7fd195f6d88ab06aea92ba931654
drwx------ 3 root root 4096 Jun 20 16:11 ad0fe55125ebf599da124da175174a4b8c1878afe6907bf7c78570341f308461
drwx------ 3 root root 4096 Jun 20 16:11 edab9b5e5bf73f2997524eebeac1de4cf9c8b904fa8ad3ec43b3504196aa3801
```

镜像层目录包含该层独有的文件以及与较低层共享数据的硬链接。这允许高效使用磁盘空间。

```console
$ ls -i /var/lib/docker/overlay2/