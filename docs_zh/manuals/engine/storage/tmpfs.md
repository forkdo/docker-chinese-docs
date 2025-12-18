---
description: 使用 tmpfs 挂载
title: tmpfs 挂载
weight: 30
keywords: 存储, 持久化, 数据持久化, tmpfs
aliases:
  - /engine/admin/volumes/tmpfs/
  - /storage/tmpfs/
---

[卷](volumes.md) 和 [绑定挂载](bind-mounts.md) 允许你在宿主机和容器之间共享文件，
这样即使容器停止后，数据也能被保留。

如果你在 Linux 上运行 Docker，你还有第三种选择：tmpfs 挂载。
当你创建带有 tmpfs 挂载的容器时，容器可以在容器的可写层之外创建文件。

与卷和绑定挂载不同，tmpfs 挂载是临时的，仅保留在宿主机内存中。
当容器停止时，tmpfs 挂载会被移除，写入其中的文件不会被持久化。

tmpfs 挂载最适合用于你不想让数据在宿主机或容器内持久化的场景。
这可能是出于安全考虑，或者是为了保护容器性能，当你的应用需要写入大量非持久化状态数据时。

> [!IMPORTANT]
> Docker 中的 tmpfs 挂载直接映射到 Linux 内核中的
> [tmpfs](https://en.wikipedia.org/wiki/Tmpfs)。因此，
> 临时数据可能会被写入交换文件，从而持久化到文件系统中。

## 挂载到现有数据上

如果你将 tmpfs 挂载到容器中已存在文件或目录的目录，预先存在的文件将被挂载遮蔽。
这类似于在 Linux 宿主机上将文件保存到 `/mnt`，然后将 U 盘挂载到 `/mnt`。
U 盘卸载之前，`/mnt` 的内容会被 U 盘的内容遮蔽。

对于容器，没有简单的方法可以移除挂载来再次显示被遮蔽的文件。
你最好的选择是重新创建一个没有挂载的容器。

## tmpfs 挂载的限制

- 与卷和绑定挂载不同，你不能在容器之间共享 tmpfs 挂载。
- 此功能仅在你在 Linux 上运行 Docker 时可用。
- 在 tmpfs 上设置权限可能会导致它们在容器重启后[重置](https://github.com/docker/for-linux/issues/138)。在某些情况下，[设置 uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) 可以作为解决方法。

## 语法

要使用 `docker run` 命令挂载 tmpfs，你可以使用 `--mount` 或 `--tmpfs` 标志。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

一般来说，更推荐使用 `--mount`。主要区别是 `--mount` 标志更明确。
另一方面，`--tmpfs` 更简洁，并且给你更多灵活性，因为它允许你设置更多挂载选项。

`--tmpfs` 标志不能与 Swarm 服务一起使用。你必须使用 `--mount`。

### --tmpfs 的选项

`--tmpfs` 标志由两个字段组成，用冒号字符 (`:`) 分隔。

```console
$ docker run --tmpfs <mount-path>[:opts]
```

第一个字段是容器中挂载 tmpfs 的路径。第二个字段是可选的，允许你设置挂载选项。
`--tmpfs` 的有效挂载选项包括：

| 选项       | 描述                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | 创建只读的 tmpfs 挂载。                                                            |
| `rw`         | 创建读写 tmpfs 挂载（默认行为）。                                        |
| `nosuid`     | 防止在执行期间尊重 `setuid` 和 `setgid` 位。                    |
| `suid`       | 允许在执行期间尊重 `setuid` 和 `setgid` 位（默认行为）。        |
| `nodev`      | 可以创建设备文件，但不工作（访问会导致错误）。            |
| `dev`        | 可以创建设备文件，并且完全工作。                                       |
| `exec`       | 允许在挂载的文件系统中执行可执行二进制文件。                     |
| `noexec`     | 不允许在挂载的文件系统中执行可执行二进制文件。             |
| `sync`       | 所有到文件系统的 I/O 都是同步进行的。                                           |
| `async`      | 所有到文件系统的 I/O 都是异步进行的（默认行为）。                       |
| `dirsync`    | 文件系统内的目录更新是同步进行的。                            |
| `atime`      | 每次访问文件时都会更新文件访问时间。                                    |
| `noatime`    | 访问文件时不会更新文件访问时间。                                |
| `diratime`   | 每次访问目录时都会更新目录访问时间。                         |
| `nodiratime` | 访问目录时不会更新目录访问时间。                      |
| `size`       | 指定 tmpfs 挂载的大小，例如 `size=64m`。                             |
| `mode`       | 指定 tmpfs 挂载的文件模式（权限），例如 `mode=1777`。       |
| `uid`        | 指定 tmpfs 挂载所有者的用户 ID，例如 `uid=1000`。           |
| `gid`        | 指定 tmpfs 挂载所有者的组 ID，例如 `gid=1000`。          |
| `nr_inodes`  | 指定 tmpfs 挂载的最大 inode 数，例如 `nr_inodes=400k`。 |
| `nr_blocks`  | 指定 tmpfs 挂载的最大块数，例如 `nr_blocks=1024`。 |

```console {title="示例"}
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

Linux mount 命令中可用的并非所有 tmpfs 挂载功能都受 `--tmpfs` 标志支持。
如果你需要高级 tmpfs 选项或功能，你可能需要使用特权容器或在 Docker 外配置挂载。

> [!CAUTION]
> 使用 `--privileged` 运行容器会授予提升的权限，并可能将宿主机系统暴露于安全风险中。
> 仅在绝对必要且在受信任的环境中使用此选项。

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### --mount 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由 `<key>=<value>` 元组组成。
键的顺序不重要。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

`--mount type=tmpfs` 的有效选项包括：

| 选项                         | 描述                                                                                                            |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | 容器中挂载 tmpfs 的路径。                                                                                  |
| `tmpfs-size`                   | tmpfs 挂载的大小（以字节为单位）。如果未设置，默认 tmpfs 卷的最大大小为主机总 RAM 的 50%。 |
| `tmpfs-mode`                   | tmpfs 的八进制文件模式。例如 `700` 或 `0770`。默认为 `1777` 或全局可写。                  |

```console {title="示例"}
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## 在容器中使用 tmpfs 挂载

要在容器中使用 `tmpfs` 挂载，请使用 `--tmpfs` 标志，或使用带有 `type=tmpfs` 和 `destination` 选项的 `--mount` 标志。
`tmpfs` 挂载没有 `source`。以下示例在 Nginx 容器中的 `/app` 处创建一个 `tmpfs` 挂载。
第一个示例使用 `--mount` 标志，第二个使用 `--tmpfs` 标志。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --mount type=tmpfs,destination=/app \
  nginx:latest
```

通过查看 `docker inspect` 输出的 `Mounts` 部分来验证挂载是 `tmpfs` 挂载：

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
[{"Type":"tmpfs","Source":"","Destination":"/app","Mode":"","RW":true,"Propagation":""}]
```

{{< /tab >}}
{{< tab name="`--tmpfs`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --tmpfs /app \
  nginx:latest
```

通过查看 `docker inspect` 输出的 `Mounts` 部分来验证挂载是 `tmpfs` 挂载：

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
{"/app":""}
```

{{< /tab >}}
{{< /tabs >}}

停止并移除容器：

```console
$ docker stop tmptest
$ docker rm tmptest
```

## 下一步

- 了解 [卷](volumes.md)
- 了解 [绑定挂载](bind-mounts.md)
- 了解 [存储驱动](/engine/storage/drivers/)