---
description: 使用 tmpfs 挂载
title: tmpfs 挂载
weight: 30
keywords: storage, persistence, data persistence, tmpfs
aliases:
- /engine/admin/volumes/tmpfs/
- /storage/tmpfs/
---

[Volumes](volumes.md) 和 [bind mounts](bind-mounts.md) 允许你在主机和容器之间共享文件，以便在容器停止后仍能保留数据。

如果你在 Linux 上运行 Docker，还有第三种选择：tmpfs 挂载。
当你使用 tmpfs 挂载创建容器时，容器可以在容器的可写层之外创建文件。

与 volumes 和 bind mounts 不同，tmpfs 挂载是临时的，仅保留在主机内存中。当容器停止时，tmpfs 挂载会被移除，写入其中的文件不会被保留。

tmpfs 挂载最适合用于你既不希望数据保留在主机上，也不希望保留在容器内的情况。这可能是出于安全原因，或当你的应用程序需要写入大量非持久状态数据时，为了保护容器性能。

> [!IMPORTANT]
> Docker 中的 tmpfs 挂载直接映射到 Linux 内核中的
> [tmpfs](https://en.wikipedia.org/wiki/Tmpfs)。因此，
> 临时数据可能会被写入交换文件，从而持久化到
> 文件系统中。

## 覆盖现有数据的挂载

如果你在容器中已存在文件或目录的目录中创建 tmpfs 挂载，则预先存在的文件会被挂载掩盖。这类似于在 Linux 主机上将文件保存到 `/mnt`，然后将 USB 驱动器挂载到 `/mnt`。在卸载 USB 驱动器之前，`/mnt` 的内容会被 USB 驱动器的内容掩盖。

对于容器，没有直接的方法可以移除挂载以再次显示被掩盖的文件。你最好的选择是重新创建容器而不使用挂载。

## tmpfs 挂载的限制

- 与 volumes 和 bind mounts 不同，你无法在容器之间共享 tmpfs 挂载。
- 此功能仅在你运行 Docker on Linux 时可用。
- 在 tmpfs 上设置权限可能会导致它们在[容器重启后重置](https://github.com/docker/for-linux/issues/138)。在某些情况下，[设置 uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) 可以作为解决方法。

## 语法

要使用 `docker run` 命令挂载 tmpfs，你可以使用 `--mount` 或 `--tmpfs` 标志。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

通常，推荐使用 `--mount`。主要区别在于 `--mount` 标志更明确。另一方面，`--tmpfs` 更简洁，并提供了更多灵活性，因为它允许你设置更多挂载选项。

`--tmpfs` 标志不能与 swarm services 一起使用。你必须使用 `--mount`。

### `--tmpfs` 的选项

`--tmpfs` 标志由两个字段组成，用冒号字符（`:`）分隔。

```console
$ docker run --tmpfs <mount-path>[:opts]
```

第一个字段是要挂载到 tmpfs 的容器路径。第二个字段是可选的，允许你设置挂载选项。`--tmpfs` 的有效挂载选项包括：

| 选项         | 描述                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | 创建只读 tmpfs 挂载。                                                            |
| `rw`         | 创建读写 tmpfs 挂载（默认行为）。                                        |
| `nosuid`     | 防止在执行期间识别 `setuid` 和 `setgid` 位。                    |
| `suid`       | 允许在执行期间识别 `setuid` 和 `setgid` 位（默认行为）。        |
| `nodev`      | 可以创建设备文件，但这些设备文件不可用（访问会导致错误）。            |
| `dev`        | 可以创建设备文件，并且这些设备文件完全可用。                                       |
| `exec`       | 允许在挂载的文件系统中执行可执行二进制文件。                     |
| `noexec`     | 不允许在挂载的文件系统中执行可执行二进制文件。             |
| `sync`       | 对文件系统的所有 I/O 操作同步进行。                                           |
| `async`      | 对文件系统的所有 I/O 操作异步进行（默认行为）。                       |
| `dirsync`    | 对文件系统中的目录更新同步进行。                            |
| `atime`      | 每次访问文件时更新文件访问时间。                                    |
| `noatime`    | 访问文件时不更新文件访问时间。                                |
| `diratime`   | 每次访问目录时更新目录访问时间。                         |
| `nodiratime` | 访问目录时不更新目录访问时间。                      |
| `size`       | 指定 tmpfs 挂载的大小，例如 `size=64m`。                             |
| `mode`       | 指定 tmpfs 挂载的文件模式（权限），例如 `mode=1777`。       |
| `uid`        | 指定 tmpfs 挂载所有者的用户 ID，例如 `uid=1000`。           |
| `gid`        | 指定 tmpfs 挂载所有者的组 ID，例如 `gid=1000`。          |
| `nr_inodes`  | 指定 tmpfs 挂载的最大 inode 数，例如 `nr_inodes=400k`。 |
| `nr_blocks`  | 指定 tmpfs 挂载的最大块数，例如 `nr_blocks=1024`。 |

```console {title="示例"}
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

并非 Linux mount 命令中所有可用的 tmpfs 挂载功能都支持 `--tmpfs` 标志。如果你需要高级 tmpfs 选项或功能，你可能需要使用特权容器或在 Docker 外部配置挂载。

> [!CAUTION]
> 使用 `--privileged` 运行容器会授予提升的权限，并可能
> 使主机系统面临安全风险。仅在绝对必要且可信的环境中使用此选项。

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### `--mount` 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

`--mount type=tmpfs` 的有效选项包括：

| 选项                         | 描述                                                                                                            |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | 要挂载到 tmpfs 的容器路径。                                                                                  |
| `tmpfs-size`                   | tmpfs 挂载的大小（以字节为单位）。如果未设置，tmpfs 卷的默认最大大小为主机总 RAM 的 50%。 |
| `tmpfs-mode`                   | tmpfs 的文件模式（八进制）。例如 `700` 或 `0770`。默认为 `1777` 或全局可写。                  |

```console {title="示例"}
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## 在容器中使用 tmpfs 挂载

要在容器中使用 `tmpfs` 挂载，请使用 `--tmpfs` 标志，或使用带有 `type=tmpfs` 和 `destination` 选项的 `--mount` 标志。`tmpfs` 挂载没有 `source`。以下示例在 Nginx 容器中的 `/app` 处创建了一个 `tmpfs` 挂载。第一个示例使用 `--mount` 标志，第二个使用 `--tmpfs` 标志。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name tmptest \
  --mount type=tmpfs,destination=/app \
  nginx:latest
```

通过在 `docker inspect` 输出的 `Mounts` 部分中查找来验证挂载是否为 `tmpfs` 挂载：

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

通过在 `docker inspect` 输出的 `Mounts` 部分中查找来验证挂载是否为 `tmpfs` 挂载：

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

- 了解 [volumes](volumes.md)
- 了解 [bind mounts](bind-mounts.md)
- 了解 [storage drivers](/engine/storage/drivers/)