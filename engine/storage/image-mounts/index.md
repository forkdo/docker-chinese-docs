# 镜像挂载


[卷](volumes.md)、[绑定挂载](bind-mounts.md) 和 [tmpfs 挂载](tmpfs.md) 都为容器提供了一个读写数据的位置。镜像挂载则不同：它不是挂载一个目录或基于内存的文件系统，而是将另一个镜像的内容挂载到容器中。

当你使用镜像挂载时，第二个镜像的文件系统会被挂载到容器中你选择的路径下。容器可以在其自身文件系统旁边读取该镜像中的文件，而这些文件并不属于容器自身的镜像。当你希望将一个镜像中的工具或资源引入到运行着不同镜像的容器时，这很有用。

镜像挂载是只读的。被挂载的镜像永远不会被修改，容器也无法写入该挂载。

> [!NOTE]
> 镜像挂载需要 [containerd 镜像存储](containerd.md)。

## 何时使用镜像挂载

镜像挂载适用于以下类型的用例：

- 调试一个不包含 shell 或常用工具的极简镜像或加固镜像。你可以将一个工具丰富的镜像（例如 `busybox`）挂载到正在运行的容器命名空间中，并在不修改原始镜像的情况下运行这些工具。有关完整示例，请参阅 [使用 Docker 加固镜像进行调试](/manuals/dhi/how-to/troubleshoot.md)。

- 共享只读资源，例如以镜像形式分发、并由运行不同镜像的容器所消费的 datasets、模型或静态内容。

- 通过将可选工具打包到单独的镜像中、仅在需要时挂载它，来保持应用镜像的体积小巧。

## 挂载到现有数据之上

如果你将镜像挂载到容器中存在文件或目录的目录中，原有的文件会被挂载遮蔽。这类似于你在 Linux 主机上将文件保存到 `/mnt`，然后将一个 USB 驱动器挂载到 `/mnt`。在 USB 驱动器卸载之前，`/mnt` 的内容会被 USB 驱动器的内容遮蔽。

对于容器，没有简便的方法移除挂载以重新显示被遮蔽的文件。你最好的选择是不带该挂载地重新创建容器。

## 注意事项与限制

- 镜像挂载始终是只读的。容器无法修改被挂载的镜像，更改也不会持久化到任何地方。

- 源镜像必须已存在于守护进程的镜像存储中。创建挂载时，Docker 不会自动拉取源镜像。如果镜像不存在，命令会失败：

  ```console
  $ docker run --mount type=image,source=busybox:musl,destination=/dbg alpine
  docker: Error response from daemon: No such image: busybox:musl
  ```

  请先用 `docker pull` 拉取镜像，然后再创建挂载。

- 镜像挂载需要 [containerd 镜像存储](containerd.md)。当守护进程使用经典存储驱动程序时，它们不可用。

- 你只能使用 `--mount` 标志创建镜像挂载。没有等价的 `--volume`（`-v`）方式。

- 从挂载的镜像中运行可执行文件，需要容器中存在兼容的运行时。动态链接的二进制文件只有在容器提供匹配的动态链接器和共享库时才能运行。例如，基于 glibc 的二进制文件在基于 musl 的镜像（如 Alpine）中会失败。静态链接的二进制文件，或仅从镜像挂载数据，可以避免此限制。

## 语法

要使用 `docker run` 命令挂载镜像，请使用带有 `type=image` 的 `--mount` 标志。

```console
$ docker run --mount type=image,src=<image-reference>,dst=<container-path>
```

`--mount` 标志由多个键值对组成，以逗号分隔，每个键值对由一个 `<key>=<value>` 元组构成。键的顺序无关紧要。

```console
$ docker run --mount type=image,src=<image-reference>,dst=<container-path>[,<key>=<value>...]
```

### --mount 的选项

`--mount type=image` 的有效选项包括：

| 选项                         | 描述                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| `source`, `src`             | 要挂载的镜像引用，例如 `busybox` 或 `busybox:musl`。该镜像必须已存在于本地。              |
| `destination`, `dst`, `target` | 镜像在容器中挂载的路径。必须是绝对路径。                                                 |
| `image-subpath`              | 改用源镜像中挂载的路径，而不是镜像根目录。请参阅[挂载镜像的子路径](#挂载镜像的子路径)。 |

```console {title="示例"}
$ docker run --mount type=image,src=busybox,dst=/dbg,image-subpath=bin
```

## 在容器中使用镜像挂载

以下示例运行一个 Alpine 容器，并将 `busybox:musl` 镜像挂载到 `/dbg`。请先拉取源镜像，因为 Docker 在创建挂载时不会为你拉取它。本示例使用基于 musl 的 BusyBox 镜像，以便其二进制文件与基于 musl 的 Alpine 容器兼容。

```console
$ docker pull busybox:musl
$ docker run -d \
  -it \
  --name imgtest \
  --mount type=image,source=busybox:musl,destination=/dbg \
  alpine:latest
```

容器现在可以在运行 Alpine 镜像的同时，从 `/dbg` 读取 BusyBox 工具：

```console
$ docker exec imgtest /dbg/bin/echo "hello from busybox"
hello from busybox
```

通过在 `docker inspect` 输出的 `Mounts` 部分查看，验证该挂载是否为 `image` 挂载：

```console
$ docker inspect imgtest --format '{{ json .Mounts }}'
[{"Type":"image","Name":"busybox:musl","Source":"/var/lib/docker/rootfs/overlayfs/...","Destination":"/dbg","Mode":"","RW":false,"Propagation":"rprivate"}]
```

这表明该挂载是一个 `image` 挂载，其源是 `busybox:musl` 镜像，并且是只读的（`"RW":false`）。

停止并移除容器：

```console
$ docker container rm -fv imgtest
```

## 挂载镜像的子路径

使用 `image-subpath` 选项挂载源镜像中的特定目录，而不是其根目录。例如，要将 `busybox` 镜像的 `bin` 目录挂载到 `/tools`：

```console
$ docker run -d \
  -it \
  --name imgtest \
  --mount type=image,source=busybox,destination=/tools,image-subpath=bin \
  alpine:latest
```

容器会在 `/tools` 处看到镜像 `bin` 目录的内容。

## 在 Docker Compose 中使用镜像挂载

带有镜像挂载的单个 Docker Compose 服务如下所示：

```yaml
services:
  app:
    image: alpine:latest
    volumes:
      - type: image
        source: busybox
        target: /dbg
```

要挂载镜像的子路径，请在 `image` 下使用 `subpath` 选项：

```yaml
services:
  app:
    image: alpine:latest
    volumes:
      - type: image
        source: busybox
        target: /tools
        image:
          subpath: bin
```

`image.subpath` 选项在 Docker Compose 2.35.0 及更高版本中可用。有关在 Compose 中使用 `image` 类型挂载的更多信息，请参阅 [Compose 关于 volume 属性的参考](/reference/compose-file/services.md#volumes)。

## 下一步

- 了解 [卷](./volumes.md)。
- 了解 [绑定挂载](./bind-mounts.md)。
- 了解 [tmpfs 挂载](./tmpfs.md)。
- 了解 [存储驱动程序](/engine/storage/drivers/)。

