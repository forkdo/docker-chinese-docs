# OverlayFS 存储驱动程序

OverlayFS 是一种联合文件系统。

本文档将 Linux 内核驱动称为 `OverlayFS`，将 Docker 存储驱动称为 `overlay2`。

> [!NOTE]
> Docker Engine 29.0 及更高版本默认使用 [containerd 镜像存储](/manuals/engine/storage/containerd.md)。
> `overlay2` 驱动是传统的存储驱动，已被 `overlayfs` containerd 快照程序取代。更多信息，请参阅[选择存储驱动程序](/manuals/engine/storage/drivers/select-storage-driver.md)。

> [!NOTE]
> 有关 `fuse-overlayfs` 驱动，请参阅[无根模式文档](/manuals/engine/security/rootless.md)。

## 先决条件

如果您满足以下先决条件，则支持 `overlay2` 驱动：

- Linux 内核版本 4.0 或更高版本，或者使用内核版本 3.10.0-514 或更高版本的 RHEL 或 CentOS。
- `overlay2` 驱动在 `xfs` 后备文件系统上受支持，但仅在启用 `d_type=true` 时受支持。

  使用 `xfs_info` 验证 `ftype` 选项是否设置为 `1`。要正确格式化 `xfs` 文件系统，请使用标志 `-n ftype=1`。

- 更改存储驱动会使本地系统上现有的容器和镜像无法访问。在更改存储驱动之前，请使用 `docker save` 保存您构建的任何镜像，或将它们推送到 Docker Hub 或私有注册表，这样您以后就不需要重新创建它们。

## 使用 `overlay2` 存储驱动配置 Docker

<a name="configure-docker-with-the-overlay-or-overlay2-storage-driver"></a>

在执行此过程之前，您必须首先满足所有[先决条件](#prerequisites)。

以下步骤概述了如何配置 `overlay2` 存储驱动。

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2. 将 `/var/lib/docker` 的内容复制到临时位置。

   ```console
   $ cp -au /var/lib/docker /var/lib/docker.bk
   ```

3. 如果您想使用与 `/var/lib/` 所用文件系统不同的后备文件系统，请格式化该文件系统并将其挂载到 `/var/lib/docker` 中。确保将此挂载添加到 `/etc/fstab` 以使其永久生效。

4. 编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件为空，请添加以下内容。

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

6. 验证守护进程是否正在使用 `overlay2` 存储驱动。使用 `docker info` 命令并查找 `Storage Driver` 和 `Backing filesystem`。

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

Docker 现在正在使用 `overlay2` 存储驱动，并已自动使用所需的 `lowerdir`、`upperdir`、`merged` 和 `workdir` 结构创建了叠加挂载。

继续阅读以了解 OverlayFS 在 Docker 容器内如何工作，以及性能建议和其与不同后备文件系统兼容性的限制信息。

## `overlay2` 驱动的工作原理

OverlayFS 将两个目录叠加在单个 Linux 主机上，并将它们呈现为一个目录。这些目录称为层，合并过程称为联合挂载。OverlayFS 将下层目录称为 `lowerdir`，将上层目录称为 `upperdir`。统一视图通过其自己的目录 `merged` 暴露出来。

`overlay2` 驱动程序原生支持最多 128 个下层 OverlayFS 层。此功能为与层相关的 Docker 命令（如 `docker build` 和 `docker commit`）提供了更好的性能，并减少了后备文件系统上的 inode 消耗。

### 磁盘上的镜像和容器层

使用 `docker pull ubuntu` 下载五层镜像后，您可以在 `/var/lib/docker/overlay2` 下看到六个目录。

> [!WARNING]
>
> 请勿直接操作 `/var/lib/docker/` 中的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay2

total 24
drwx
------ 5 root root 4096 Jun 20 07:36 223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7
drwx
------ 3 root root 4096 Jun 20 07:36 3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b
drwx
------ 5 root root 4096 Jun 20 07:36 4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1
drwx
------ 5 root root 4096 Jun 20 07:36 e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5
drwx
------ 5 root root 4096 Jun 20 07:36 eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed
drwx
------ 2 root root 4096 Jun 20 07:36 l
```

新的 `l`（小写 `L`）目录包含缩短的层标识符作为符号链接。这些标识符用于避免达到 `mount` 命令参数的页面大小限制。

```console
$ ls -l /var/lib/docker/overlay2/l

total 20
lrwxrwxrwx 1 root root 72 Jun 20 07:36 6Y5IM2XC7TSNIJZZFLJCS6I4I4 -> ../3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 B3WWEFKBG3PLLV737KZFIASSW7 -> ../4e9fa83caff3e8f4cc83693fa407a4a9fac9573deaf481506c102d484dd1e6a1/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 JEYMODZYFCZFYSDABYXD5MF6YO -> ../eca1e4e1694283e001f200a667bb3cb40853cf2d1b12c29feda7422fed78afed/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 NFYKDW6APBCCUCTOUSYDH4DXAT -> ../223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff
lrwxrwxrwx 1 root root 72 Jun 20 07:36 UL2MW33MSE3Q5VYIKBRN4ZAGQP -> ../e8876a226237217ec61c4baf238a32992291d059fdac95ed6303bdff3f59cff5/diff
```

最底层包含一个名为 `link` 的文件，其中包含缩短标识符的名称，以及一个名为 `diff` 的目录，其中包含该层的内容。

```console
$ ls /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/

diff  link

$ cat /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/link

6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls  /var/lib/docker/overlay2/3a36935c9df35472229c57f4a27105a136f5e4dbef0f87905b2e506e494e348b/diff

bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

倒数第二层和每个更高层都包含一个名为 `lower` 的文件，用于表示其父层，以及一个名为 `diff` 的目录，其中包含其内容。它还包含一个 `merged` 目录，其中包含其父层和自身的统一内容，以及一个 `work` 目录，该目录由 OverlayFS 在内部使用。

```console
$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7

diff  link  lower  merged  work

$ cat /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/lower

l/6Y5IM2XC7TSNIJZZFLJCS6I4I4

$ ls /var/lib/docker/overlay2/223c2864175491657d238e2664251df13b63adb8d050924fd1bfcdb278b866f7/diff/

etc  sbin  usr  var
```

要查看使用 `overlay` 存储驱动与 Docker 时存在的挂载，请使用 `mount` 命令。为便于阅读，下面的输出已截断。

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/merged
type overlay (rw,relatime,
lowerdir=l/DJA75GUWHWG7EWICFYX54FIOVT:l/B3WWEFKBG3PLLV737KZFIASSW7:l/JEYMODZYFCZFYSDABYXD5MF6YO:l/UL2MW33MSE3Q5VYIKBRN4ZAGQP:l/NFYKDW6APBCCUCTOUSYDH4DXAT:l/6Y5IM2XC7TSNIJZZFLJCS6I4I4,
upperdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/diff,
workdir=9186877cdf386d0a3b016149cf30c208f326dca307529e646afce5b3f83f5304/work)
```

第二行中的 `rw` 显示 `overlay` 挂载是读写的。

下图显示了 Docker 镜像和 Docker 容器如何分层。镜像层是 `lowerdir`，容器层是 `upperdir`。如果镜像有多层，则使用多个 `lowerdir` 目录。统一视图通过名为 `merged` 的目录暴露出来，该目录实际上是容器的挂载点。

![Docker 构造如何映射到 OverlayFS 构造](images/overlay_constructs.webp)

如果镜像层和容器层包含相同的文件，则容器层 (`upperdir`) 优先，并掩盖镜像层中相同文件的存在。

要创建容器，`overlay2` 驱动会组合表示镜像顶层的目录和容器的新目录。镜像的层是叠加层中的 `lowerdirs`，是只读的。容器的新目录是 `upperdir`，是可写的。

### 磁盘上的镜像和容器层

以下 `docker pull` 命令显示 Docker 主机正在下载包含五层的 Docker 镜像。

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
> 请勿直接操作 `/var/lib/docker/` 中的任何文件或目录。这些文件和目录由 Docker 管理。

```console
$ ls -l /var/lib/docker/overlay/

total 20
drwx------ 3 root root 4096 Jun 20 16:11 38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8
drwx------ 3 root root 4096 Jun 20 16:11 55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
drwx------ 3 root root 4096 Jun 20 16:11 824c8a961a4f5e8fe4f4243dab57c5be798e7fd195f6d88ab06aea92ba931654
drwx------ 3 root root 4096 Jun 20 16:11 ad0fe55125ebf599da124da175174a4b8c1878afe6907bf7c78570341f308461
drwx------ 3 root root 4096 Jun 20 16:11 edab9b5e5bf73f2997524eebeac1de4cf9c8b904fa8ad3ec43b3504196aa3801
```

镜像层目录包含该层独有的文件，以及与较低层共享数据的硬链接。这样可以有效地利用磁盘空间。

```console
$ ls -i /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

19793696 /var/lib/docker/overlay2/38f3ed2eac129654acef11c32670b534670c3a06e483fce313d72e3e0a15baa8/root/bin/ls

$ ls -i /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls

19793696 /var/lib/docker/overlay2/55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358/root/bin/ls
```

#### 容器层

容器也以磁盘形式存在于 Docker 主机的文件系统中，位于 `/var/lib/docker/overlay/` 下。如果您使用 `ls -l` 命令列出正在运行的容器的子目录，会存在三个目录和一个文件：

```console
$ ls -l /var/lib/docker/overlay2/<directory-of-running-container>

total 16
-rw-r--r-- 1 root root   64 Jun 20 16:39 lower-id
drwxr-xr-x 1 root root 4096 Jun 20 16:39 merged
drwxr-xr-x 4 root root 4096 Jun 20 16:39 upper
drwx------ 3 root root 4096 Jun 20 16:39 work
```

`lower-id` 文件包含容器所基于镜像的顶层 ID，即 OverlayFS 的 `lowerdir`。

```console
$ cat /var/lib/docker/overlay2/ec444863a55a9f1ca2df72223d459c5d940a721b2288ff86a3f27be28b53be6c/lower-id

55f1e14c361b90570df46371b20ce6d480c434981cbda5fd68c6ff61aa0a5358
```

`upper` 目录包含容器读写层的内容，对应于 OverlayFS 的 `upperdir`。

`merged` 目录是 `lowerdir` 和 `upperdirs` 的联合挂载，包含运行中容器内部的文件系统视图。

`work` 目录是 OverlayFS 内部使用的。

要查看使用 `overlay2` 存储驱动与 Docker 时存在的挂载，请使用 `mount` 命令。为便于阅读，下面的输出已截断。

```console
$ mount | grep overlay

overlay on /var/lib/docker/overlay2/l/ec444863a55a.../merged
type overlay (rw,relatime,lowerdir=/var/lib/docker/overlay2/l/55f1e14c361b.../root,
upperdir=/var/lib/docker/overlay2/l/ec444863a55a.../upper,
workdir=/var/lib/docker/overlay2/l/ec444863a55a.../work)
```

第二行中的 `rw` 显示 `overlay` 挂载是读写的。

## 容器如何使用 `overlay2` 进行读写

<a name="how-container-reads-and-writes-work-with-overlay-or-overlay2"></a>

### 读取文件

考虑容器使用叠加层为读取访问打开文件的三种情况。

#### 文件在容器层中不存在

如果容器为读取访问打开一个文件，且该文件在容器 (`upperdir`) 中尚不存在，则从镜像 (`lowerdir`) 中读取。这产生的性能开销非常小。

#### 文件仅存在于容器层中

如果容器为读取访问打开一个文件，且该文件存在于容器 (`upperdir`) 中而不存在于镜像 (`lowerdir`) 中，则直接从容器中读取。

#### 文件同时存在于容器层和镜像层中

如果容器为读取访问打开一个文件，且该文件同时存在于镜像层和容器层中，则读取容器层中的文件版本。容器层 (`upperdir`) 中的文件会掩盖镜像层 (`lowerdir`) 中同名的文件。

### 修改文件或目录

考虑在容器中修改文件的一些情况。

#### 第一次写入文件

容器第一次写入现有文件时，该文件在容器 (`upperdir`) 中不存在。`overlay2` 驱动执行 `copy_up` 操作，将文件从镜像 (`lowerdir`) 复制到容器 (`upperdir`)。然后容器将更改写入容器层中文件的新副本。

但是，OverlayFS 在文件级别而不是块级别工作。这意味着所有 OverlayFS `copy_up` 操作都会复制整个文件，即使文件很大且只修改了一小部分。这可能对容器写入性能产生明显影响。但是，有两点值得注意：

- `copy_up` 操作仅在第一次写入给定文件时发生。随后对同一文件的写入操作针对已复制到容器中的文件副本进行。

- OverlayFS 与多层一起工作。这意味着在具有许多层的镜像中搜索文件时，性能可能会受到影响。

#### 删除文件和目录

- 当在容器内删除一个*文件*时，会在容器 (`upperdir`) 中创建一个*白化*文件。镜像层 (`lowerdir`) 中的文件版本不会被删除（因为 `lowerdir` 是只读的）。但是，白化文件会阻止容器访问它。

- 当在容器内删除一个*目录*时，会在容器 (`upperdir`) 中创建一个*不透明目录*。这与白化文件的工作方式相同，可有效阻止访问该目录，即使它仍然存在于镜像 (`lowerdir`) 中。

#### 重命名目录

仅当源路径和目标路径都在顶层时，才允许为目录调用 `rename(2)`。否则，它会返回 `EXDEV` 错误（“不允许跨设备链接”）。您的应用程序需要设计为处理 `EXDEV` 并回退到“复制并取消链接”策略。

## OverlayFS 和 Docker 性能

`overlay2` 的性能可能优于 `btrfs`。但是，请注意以下细节：

### 页面缓存

OverlayFS 支持页面缓存共享。访问同一文件的多个容器共享该文件的单个页面缓存条目。这使得 `overlay2` 驱动程序在内存使用方面非常高效，并且是高密度用例（如 PaaS）的良好选择。

### 复制（Copyup）

与其他写时复制文件系统一样，OverlayFS 在容器首次写入文件时执行复制操作。这可能会增加写入操作的延迟，尤其是对于大文件。但是，一旦文件被复制，对该文件的所有后续写入都发生在上层，无需进一步的复制操作。

### 性能最佳实践

以下通用性能最佳实践适用于 OverlayFS。

#### 使用快速存储

固态硬盘 (SSD) 比旋转磁盘提供更快的读写速度。

#### 对写入密集型工作负载使用卷

卷为写入密集型工作负载提供最佳和最可预测的性能。这是因为它们绕过存储驱动程序，并且不会因精简配置和写时复制而产生任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并在没有正在运行的容器使用它们时持久保存数据。

## OverlayFS 兼容性的限制

总结 OverlayFS 与其他文件系统不兼容的方面：

[`open(2)`](https://linux.die.net/man/2/open)
: OverlayFS 仅实现了 POSIX 标准的一个子集。这可能导致某些 OverlayFS 操作违反 POSIX 标准。其中一个操作是复制操作。假设您的应用程序调用 `fd1=open("foo", O_RDONLY)`，然后调用 `fd2=open("foo", O_RDWR)`。在这种情况下，您的应用程序期望 `fd1` 和 `fd2` 引用同一个文件。但是，由于在第二次调用 `open(2)` 后发生复制操作，描述符引用的是不同的文件。`fd1` 继续引用镜像 (`lowerdir`) 中的文件，而 `fd2` 引用容器 (`upperdir`) 中的文件。解决此问题的方法是 `touch` 文件，这会导致发生复制操作。所有后续的 `open(2)` 操作，无论读写访问模式如何，都将引用容器 (`upperdir`) 中的文件。

  已知 `yum` 会受到影响，除非安装了 `yum-plugin-ovl` 包。如果您的发行版（如 6.8 或 7.2 之前的 RHEL/CentOS）中没有 `yum-plugin-ovl` 包，您可能需要在运行 `yum install` 之前运行 `touch /var/lib/rpm/*`。该包为 `yum` 实现了上述 `touch` 解决方法。

[`rename(2)`](https://linux.die.net/man/2/rename)
: OverlayFS 不完全支持 `rename(2)` 系统调用。您的应用程序需要检测其故障并回退到“复制并取消链接”策略。
