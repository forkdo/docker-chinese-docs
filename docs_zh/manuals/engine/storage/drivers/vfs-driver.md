---
description: 了解如何优化 VFS 驱动的使用。
keywords: container, storage, driver, vfs
title: VFS 存储驱动
aliases:
- /storage/storagedriver/vfs-driver/
---

VFS 存储驱动不是联合文件系统。每一层都是磁盘上的一个目录，不支持写时复制（copy-on-write）。要创建新层，需要对其上一层执行“深度复制”。这会导致性能低于其他存储驱动，并且占用更多磁盘空间。不过，它很稳健、稳定，可在任何环境中运行。在测试环境中，它还可用于验证其他存储后端。

## 配置 Docker 使用 `vfs` 存储驱动

1. 停止 Docker。

   ```console
   $ sudo systemctl stop docker
   ```

2. 编辑 `/etc/docker/daemon.json`。如果该文件尚不存在，请创建它。假设该文件为空，请添加以下内容：

    ```json
    {
      "storage-driver": "vfs"
    }
    ```

    如果要设置配额以控制 VFS 存储驱动可使用的最大空间，请在 `storage-opts` 键上设置 `size` 选项。

    ```json
    {
      "storage-driver": "vfs",
      "storage-opts": ["size=256M"]
    }
    ```

    如果 `daemon.json` 文件包含无效的 JSON，Docker 将无法启动。

3. 启动 Docker。

    ```console
    $ sudo systemctl start docker
    ```

4. 验证守护进程是否正在使用 `vfs` 存储驱动。
   使用 `docker info` 命令并查找 `Storage Driver`。

    ```console
    $ docker info

    Storage Driver: vfs
    ...
    ```

Docker 现在正在使用 `vfs` 存储驱动。Docker 已自动创建 `/var/lib/docker/vfs/` 目录，其中包含运行容器所使用的所有层。

## `vfs` 存储驱动的工作原理

每个镜像层和容器可写层在 Docker 主机上都表示为 `/var/lib/docker/` 下的子目录。联合挂载提供所有层的统一视图。目录名称与层本身的 ID 并不直接对应。

VFS 不支持写时复制（COW）。每次创建新层时，都会对其父层执行深度复制。这些层都位于 `/var/lib/docker/vfs/dir/` 下。

### 示例：磁盘上的镜像和容器结构

以下 `docker pull` 命令显示 Docker 主机正在下载由五层组成的 Docker 镜像。

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
e0a742c2abfd: Pull complete
486cb8339a27: Pull complete
dc6f0d824617: Pull complete
4f7a5649a30e: Pull complete
672363445ad2: Pull complete
Digest: sha256:84c334414e2bfdcae99509a6add166bbb4fa4041dc3fa6af08046a66fed3005f
Status: Downloaded newer image for ubuntu:latest
```

拉取后，每一层都表示为 `/var/lib/docker/vfs/dir/` 的子目录。目录名称与 `docker pull` 命令中显示的镜像层 ID 不相关。要查看每层在磁盘上占用的空间大小，可以使用 `du -sh` 命令，该命令以人类可读的格式显示大小。

```console
$ ls -l /var/lib/docker/vfs/dir/

total 0
drwxr-xr-x.  2 root root  19 Aug  2 18:19 3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
drwxr-xr-x. 21 root root 224 Aug  2 18:23 6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
drwxr-xr-x. 21 root root 224 Aug  2 18:23 9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
drwxr-xr-x. 21 root root 224 Aug  2 18:23 a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
drwxr-xr-x. 21 root root 224 Aug  2 18:23 e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

```console
$ du -sh /var/lib/docker/vfs/dir/*

4.0K	/var/lib/docker/vfs/dir/3262dfbe53dac3e1ab7dcc8ad5d8c4d586a11d2ac3c4234892e34bff7f6b821e
125M	/var/lib/docker/vfs/dir/6af21814449345f55d88c403e66564faad965d6afa84b294ae6e740c9ded2561
104M	/var/lib/docker/vfs/dir/6d3be4585ba32f9f5cbff0110e8d07aea5f5b9fbb1439677c27e7dfee263171c
125M	/var/lib/docker/vfs/dir/9ecd2d88ca177413ab89f987e1507325285a7418fc76d0dcb4bc021447ba2bab
104M	/var/lib/docker/vfs/dir/a292ac6341a65bf3a5da7b7c251e19de1294bd2ec32828de621d41c7ad31f895
104M	/var/lib/docker/vfs/dir/e92be7a4a4e3ccbb7dd87695bca1a0ea373d4f673f455491b1342b33ed91446b
```

上述输出显示有三层各占用 104M，两层各占用 125M。这些目录之间只有细微差异，但都消耗相同的磁盘空间。这是使用 `vfs` 存储驱动的一个缺点。

## 相关信息

- [了解镜像、容器和存储驱动](index.md)
- [选择存储驱动](select-storage-driver.md)