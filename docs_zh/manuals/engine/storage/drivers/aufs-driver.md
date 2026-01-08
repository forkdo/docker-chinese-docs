---
description: 了解如何优化 AUFS 驱动程序的使用。
keywords: '容器, 存储, 驱动程序, AUFS '
title: AUFS 存储驱动程序
sitemap: false
aliases:
- /storage/storagedriver/aufs-driver/
---

> **已弃用**
>
> AUFS 存储驱动程序已被弃用，并已在 Docker Engine v24.0 中移除。如果您正在使用 AUFS，必须在升级到 Docker Engine v24.0 之前迁移到受支持的存储驱动程序。请阅读 [Docker 存储驱动程序](select-storage-driver.md) 页面以了解受支持的存储驱动程序。

AUFS 是一种*联合文件系统*。`aufs` 存储驱动程序曾是 Docker 在 Ubuntu 以及 Stretch 之前的 Debian 版本上用于管理镜像和层的默认存储驱动程序。如果您的 Linux 内核版本为 4.0 或更高，并且您使用 Docker Engine - Community，请考虑使用较新的 [overlay2](overlayfs-driver.md)，它比 `aufs` 存储驱动程序具有潜在的性能优势。

## 先决条件

- 对于 Docker Engine - Community，AUFS 在 Ubuntu 以及 Stretch 之前的 Debian 版本上受支持。
- 如果您使用 Ubuntu，则需要将 AUFS 模块添加到内核中。如果您不安装这些包，则需要使用 `overlay2`。
- AUFS 不能使用以下后端文件系统：`aufs`、`btrfs` 或 `ecryptfs`。这意味着包含 `/var/lib/docker/aufs` 的文件系统不能是这些文件系统类型之一。

## 使用 `aufs` 存储驱动程序配置 Docker

如果在启动 Docker 时 AUFS 驱动程序已加载到内核中，并且未配置其他存储驱动程序，Docker 会默认使用它。

1.  使用以下命令验证您的内核是否支持 AUFS。

    ```console
    $ grep aufs /proc/filesystems

    nodev   aufs
    ```

2.  检查 Docker 正在使用哪个存储驱动程序。

    ```console
    $ docker info

    <截断的输出>
    Storage Driver: aufs
     Root Dir: /var/lib/docker/aufs
     Backing Filesystem: extfs
     Dirs: 0
     Dirperm1 Supported: true
    <截断的输出>
    ```

3.  如果您正在使用不同的存储驱动程序，则可能是内核中未包含 AUFS（在这种情况下会使用不同的默认驱动程序），或者 Docker 已被显式配置为使用不同的驱动程序。检查 `/etc/docker/daemon.json` 或 `ps auxw | grep dockerd` 的输出，以查看 Docker 是否已使用 `--storage-driver` 标志启动。

## `aufs` 存储驱动程序的工作原理

AUFS 是一种*联合文件系统*，这意味着它将多个目录分层放置在单个 Linux 主机上，并将它们呈现为单个目录。这些目录在 AUFS 术语中称为*分支*，在 Docker 术语中称为*层*。

统一过程称为*联合挂载*。

下图显示了一个基于 `ubuntu:latest` 镜像的 Docker 容器。

![Ubuntu 容器的层](images/aufs_layers.webp)

每个镜像层和容器层在 Docker 主机上都表示为 `/var/lib/docker/` 内的子目录。联合挂载提供了所有层的统一视图。目录名称不直接对应于层本身的 ID。

AUFS 使用写时复制 (CoW) 策略来最大化存储效率并最小化开销。

### 示例：镜像和容器的磁盘结构

以下 `docker pull` 命令显示 Docker 主机正在下载一个包含五个层的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
b6f892c0043b: Pull complete
55010f332b04: Pull complete
2955fb827c94: Pull complete
3deef3fcbd30: Pull complete
cf9722e506aa: Pull complete
Digest: sha256:382452f82a8bbd34443b2c727650af46aced0f94a44463c62a9848133ecb1aa8
Status: Downloaded newer image for ubuntu:latest
```

#### 镜像层

> [!警告]：请勿直接操作 `/var/lib/docker/` 中的任何文件或目录。这些文件和目录由 Docker 管理。

有关镜像和容器层的所有信息都存储在 `/var/lib/docker/aufs/` 的子目录中。

- `diff/`：每个层的**内容**，每个内容存储在一个单独的子目录中。
- `layers/`：关于镜像层如何堆叠的元数据。此目录包含 Docker 主机上每个镜像或容器层的一个文件。每个文件包含其在堆栈下方所有层的 ID（其父级）。
- `mnt/`：挂载点，每个镜像或容器层一个，用于为容器组装和挂载联合文件系统。对于只读的镜像，这些目录始终为空。

#### 容器层

如果容器正在运行，`/var/lib/docker/aufs/` 的内容会以以下方式更改：

- `diff/`：可写容器层中引入的差异，例如新的或修改的文件。
- `layers/`：关于可写容器层父层的元数据。
- `mnt/`：每个正在运行的容器的联合文件系统的挂载点，与从容器内部看到的完全一致。

## 容器如何使用 `aufs` 进行读写

### 读取文件

考虑容器使用 aufs 打开文件进行读取访问的三种情况。

- **文件在容器层中不存在**：如果容器打开文件进行读取访问，且该文件尚不存在于容器层中，存储驱动程序会从镜像层中搜索该文件，从容器层正下方的层开始。从找到该文件的层进行读取。

- **文件仅存在于容器层中**：如果容器打开文件进行读取访问，且该文件存在于容器层中，则从容器层读取。

- **文件同时存在于容器层和镜像层中**：如果容器打开文件进行读取访问，且该文件存在于容器层和一个或多个镜像层中，则从容器层读取该文件。容器层中的文件会遮蔽镜像层中同名的文件。

### 修改文件或目录

考虑在容器中修改文件的一些情况。

- **首次写入文件**：容器首次写入现有文件时，该文件不存在于容器 (`upperdir`) 中。`aufs` 驱动程序执行 *copy_up* 操作，将文件从其所在的镜像层复制到可写的容器层。然后容器将更改写入容器层中该文件的新副本。

  但是，AUFS 在文件级别而非块级别工作。这意味着所有 copy_up 操作都会复制整个文件，即使该文件非常大且只修改了一小部分。这可能会对容器写入性能产生明显影响。当在具有许多层的镜像中搜索文件时，AUFS 可能会出现明显的延迟。但是，值得注意的是，copy_up 操作仅在首次写入给定文件时发生。后续对同一文件的写入操作会针对已复制到容器中的文件副本进行。

- **删除文件和目录**：

  - 当在容器内删除*文件*时，会在容器层中创建一个*白化 (whiteout)* 文件。镜像层中的文件版本不会被删除（因为镜像层是只读的）。但是，白化文件会阻止容器访问它。

  - 当在容器内删除*目录*时，会在容器层中创建一个*不透明文件*。这与白化文件的工作方式相同，可有效阻止访问该目录，即使它仍然存在于镜像层中。

- **重命名目录**：在 AUFS 上调用目录的 `rename(2)` 并未得到完全支持。它会返回 `EXDEV`（“不允许跨设备链接”），即使源路径和目标路径都在同一 AUFS 层上，除非该目录没有子项。您的应用程序需要设计为处理 `EXDEV` 并回退到“复制并取消链接”策略。

## AUFS 和 Docker 性能

总结一些已经提到的与性能相关的方面：

- AUFS 存储驱动程序的性能不如 `overlay2` 驱动程序，但对于容器密度很重要的 PaaS 和其他类似用例来说，它是一个不错的选择。这是因为 AUFS 可以在多个正在运行的容器之间高效共享镜像，从而实现快速的容器启动时间和最小的磁盘空间使用量。

- AUFS 在镜像层和容器之间共享文件的底层机制非常高效地使用了页面缓存。

- AUFS 存储驱动程序可能会给容器写入性能带来显著的延迟。这是因为容器首次写入任何文件时，都需要定位该文件并将其复制到容器的顶层可写层中。当这些文件存在于许多镜像层之下且文件本身很大时，这些延迟会增加并叠加。

### 性能最佳实践

以下通用性能最佳实践也适用于 AUFS。

- **固态硬盘 (SSD)** 比旋转磁盘提供更快的读写速度。

- **对写入密集型工作负载使用卷**：卷为写入密集型工作负载提供最佳和最可预测的性能。这是因为它们绕过了存储驱动程序，并且不会因精简配置和写时复制而产生任何潜在开销。卷还有其他好处，例如允许您在容器之间共享数据，并且即使没有正在运行的容器使用它们也能持久保存。

## 相关信息

- [卷](../volumes.md)
- [了解镜像、容器和存储驱动程序](index.md)
- [选择存储驱动程序](select-storage-driver.md)