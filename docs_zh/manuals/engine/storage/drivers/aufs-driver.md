---
description: 了解如何优化 AUFS 驱动的使用。
keywords: '容器, 存储, 驱动, AUFS '
title: AUFS 存储驱动
sitemap: false
aliases:
  - /storage/storagedriver/aufs-driver/
---

> **已弃用**
>
> AuFS 存储驱动已被弃用，并在 Docker Engine v24.0 中被移除。
> 如果你正在使用 AufS，必须在升级到 Docker Engine v24.0 之前迁移到受支持的存储驱动。
> 请阅读 [Docker 存储驱动](select-storage-driver.md) 页面了解受支持的存储驱动。

AUFS 是一种 *联合文件系统*。`aufs` 存储驱动之前是 Docker 在 Ubuntu 以及 Debian Stretch 之前版本上的默认存储驱动，用于管理镜像和层。如果你的 Linux 内核版本为 4.0 或更高，并且使用 Docker Engine - Community，建议使用更新的 [overlay2](overlayfs-driver.md)，它相比 `aufs` 存储驱动具有潜在的性能优势。

## 前置条件

- 对于 Docker Engine - Community，AUFS 支持 Ubuntu 以及 Debian Stretch 之前的版本。
- 如果你使用 Ubuntu，需要将 AUFS 模块添加到内核中。如果不安装这些包，则需要使用 `overlay2`。
- AUFS 不能使用以下底层文件系统：`aufs`、`btrfs` 或 `ecryptfs`。这意味着包含 `/var/lib/docker/aufs` 的文件系统不能是这些文件系统类型之一。

## 使用 `aufs` 存储驱动配置 Docker

如果你在启动 Docker 时内核已加载 AUFS 驱动，并且未配置其他存储驱动，Docker 将默认使用它。

1.  使用以下命令验证你的内核是否支持 AUFS。

    ```console
    $ grep aufs /proc/filesystems

    nodev   aufs
    ```

2.  检查 Docker 正在使用哪个存储驱动。

    ```console
    $ docker info

    <truncated output>
    Storage Driver: aufs
     Root Dir: /var/lib/docker/aufs
     Backing Filesystem: extfs
     Dirs: 0
     Dirperm1 Supported: true
    <truncated output>
    ```

3.  如果你使用的是其他存储驱动，要么 AUFS 未包含在内核中（此时会使用其他默认驱动），要么 Docker 被显式配置为使用其他驱动。检查 `/etc/docker/daemon.json` 或 `ps auxw | grep dockerd` 的输出，查看 Docker 是否使用 `--storage-driver` 标志启动。

## `aufs` 存储驱动的工作原理

AUFS 是一种 *联合文件系统*，这意味着它可以将单个 Linux 主机上的多个目录分层并呈现为单个目录。在 AUFS 术语中，这些目录被称为 _分支_，在 Docker 术语中被称为 _层_。

统一过程称为 _联合挂载_。

下图显示了一个基于 `ubuntu:latest` 镜像的 Docker 容器。

![Ubuntu 容器的层](images/aufs_layers.webp) 

每个镜像层和容器层在 Docker 主机上都表示为 `/var/lib/docker/` 中的子目录。联合挂载提供了所有层的统一视图。目录名称并不直接对应于层本身的 ID。

AUFS 使用写时复制（CoW）策略来最大化存储效率并最小化开销。

### 示例：磁盘上的镜像和容器结构

以下 `docker pull` 命令显示了一个 Docker 主机下载包含五个层的 Docker 镜像。

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

> [!WARNING]: 不要直接操作 `/var/lib/docker/` 中的任何文件或目录。这些文件和目录由 Docker 管理。

所有关于镜像和容器层的信息都存储在 `/var/lib/docker/aufs/` 的子目录中。

- `diff/`：每个层的**内容**，分别存储在单独的子目录中
- `layers/`：关于镜像层如何堆叠的元数据。此目录包含 Docker 主机上每个镜像或容器层的一个文件。每个文件包含其下方栈中所有层（其父层）的 ID。
- `mnt/`：挂载点，每个镜像或容器层一个，用于组装和挂载容器的统一文件系统。对于镜像（只读），这些目录始终为空。

#### 容器层

如果容器正在运行，`/var/lib/docker/aufs/` 的内容会以以下方式变化：

- `diff/`：在可写容器层中引入的差异，例如新文件或修改的文件。
- `layers/`：关于可写容器层父层的元数据。
- `mnt/`：每个运行中容器的统一文件系统的挂载点，完全如容器内所见。

## 使用 `aufs` 时容器的读写操作

### 读取文件

考虑使用 aufs 时容器以读取访问权限打开文件的三种情况。

- **容器层中不存在该文件**：如果容器以读取访问权限打开文件，而该文件在容器层中不存在，存储驱动会从容器层下方的层开始在镜像层中搜索该文件。文件从找到它的层中读取。

- **文件仅存在于容器层中**：如果容器以读取访问权限打开文件，而该文件存在于容器层中，则从那里读取。

- **文件同时存在于容器层和镜像层中**：如果容器以读取访问权限打开文件，而该文件存在于容器层和一个或多个镜像层中，则从容器层中读取。容器层中的文件会遮蔽镜像层中同名的文件。

### 修改文件或目录

考虑容器中修改文件的一些情况。

- **首次写入文件**：容器首次写入现有文件时，该文件在容器（`upperdir`）中不存在。`aufs` 驱动执行 *copy_up* 操作，将文件从其存在的镜像层复制到可写的容器层。然后容器将更改写入容器层中文件的新副本。

  然而，AUFS 在文件级别而不是块级别工作。这意味着所有 copy_up 操作都会复制整个文件，即使文件很大且只修改了一小部分。这可能对容器写入性能产生明显影响。当在具有许多层的镜像中搜索文件时，AUFS 可能会遭受明显的延迟。但值得注意的是，copy_up 操作仅在首次写入特定文件时发生。对同一文件的后续写入操作针对已复制到容器的文件副本进行。

- **删除文件和目录**：

  - 当容器内删除_文件_时，容器层中会创建一个 *whiteout* 文件。镜像层中的文件版本不会被删除（因为镜像层是只读的）。但是，whiteout 文件阻止它对容器可用。

  - 当容器内删除_目录_时，容器层中会创建一个 _opaque_ 文件。其工作方式与 whiteout 文件相同，有效阻止目录被访问，即使它仍然存在于镜像层中。

- **重命名目录**：对目录调用 `rename(2)` 在 AUFS 上不完全支持。即使源路径和目标路径都在同一 AUFS 层上，除非目录没有子项，否则它会返回 `EXDEV`（"跨设备链接不被允许"）。你的应用程序需要能够处理 `EXDEV` 并回退到"复制和删除"策略。

## AUFS 和 Docker 性能

总结一些前面提到的与性能相关的方面：

- AUFS 存储驱动相比 `overlay2` 驱动性能较差，但对于容器密度重要的 PaaS 和其他类似用例来说是一个不错的选择。这是因为 AUFS 在多个运行中的容器之间高效共享镜像，从而实现快速的容器启动时间和最小的磁盘空间使用。

- AUFS 在镜像层和容器之间共享文件的基础机制非常高效地使用页面缓存。

- AUFS 存储驱动可能在容器写入性能中引入显著的延迟。这是因为容器首次写入任何文件时，需要定位文件并将其复制到容器的顶部可写层。当这些文件位于许多镜像层下方且文件本身很大时，这些延迟会增加并累积。

### 性能最佳实践

以下通用性能最佳实践也适用于 AUFS。

- **固态设备 (SSD)** 提供比旋转磁盘更快的读写速度。

- **对写入密集型工作负载使用卷**：卷为写入密集型工作负载提供最佳且最可预测的性能。这是因为它们绕过了存储驱动，不会产生精简配置和写时复制引入的任何潜在开销。卷还有其他好处，例如允许你在容器之间共享数据，并在没有运行中的容器使用时仍然持久化。

## 相关信息

- [卷](../volumes.md)
- [了解镜像、容器和存储驱动](index.md)
- [选择存储驱动](select-storage-driver.md)
