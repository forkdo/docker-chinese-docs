---
description: 使用绑定挂载
title: 绑定挂载
weight: 20
keywords: storage, persistence, data persistence, mounts, bind mounts
aliases:
- /engine/admin/volumes/bind-mounts/
- /storage/bind-mounts/
---

当您使用绑定挂载时，主机上的文件或目录会从主机挂载到容器中。相比之下，当您使用卷时，会在主机上的 Docker 存储目录中创建一个新目录，Docker 会管理该目录的内容。

## 何时使用绑定挂载

绑定挂载适用于以下类型的用例：

- 在 Docker 主机上的开发环境与容器之间共享源代码或构建产物。

- 当您希望在容器中创建或生成文件，并将这些文件持久化到主机的文件系统上时。

- 从主机向容器共享配置文件。Docker 默认就是通过将主机上的 `/etc/resolv.conf` 挂载到每个容器中来为容器提供 DNS 解析的。

绑定挂载也可用于构建：您可以将主机上的源代码绑定挂载到构建容器中，以测试、检查或编译项目。

## 在现有数据上进行绑定挂载

如果您将文件或目录绑定挂载到容器中一个已存在文件或目录的目录中，预先存在的文件会被挂载遮蔽。这类似于您在 Linux 主机上将文件保存到 `/mnt`，然后将 U 盘挂载到 `/mnt`。在 U 盘被卸载之前，`/mnt` 的内容会被 U 盘的内容遮蔽。

对于容器，没有直接的方法可以通过移除挂载来重新显示被遮蔽的文件。您最好的选择是不带挂载地重新创建容器。

## 注意事项和约束

- 绑定挂载默认对主机上的文件具有写入权限。

  使用绑定挂载的一个副作用是，您可以通过容器中运行的进程来更改主机文件系统，包括创建、修改或删除重要的系统文件或目录。此功能可能会带来安全影响。例如，它可能会影响主机系统上的非 Docker 进程。

  您可以使用 `readonly` 或 `ro` 选项来阻止容器写入挂载。

- 绑定挂载是创建到 Docker 守护进程主机，而不是客户端。

  如果您使用的是远程 Docker 守护进程，则无法创建绑定挂载来在容器中访问客户端机器上的文件。

  对于 Docker Desktop，守护进程在 Linux 虚拟机内运行，而不是直接在本机主机上运行。Docker Desktop 具有内置机制，可以透明地处理绑定挂载，允许您将本机主机文件系统路径与在虚拟机中运行的容器共享。

- 带有绑定挂载的容器与主机紧密绑定。

  绑定挂载依赖于主机文件系统具有特定的可用目录结构。这种依赖意味着，如果在不具有相同目录结构的不同主机上运行，带有绑定挂载的容器可能会失败。

## 语法

要创建绑定挂载，您可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

通常，`--mount` 是首选。主要区别在于 `--mount` 标志更明确，并支持所有可用的选项。

如果您使用 `--volume` 来绑定挂载一个在 Docker 主机上尚不存在的文件或目录，Docker 会自动为您在主机上创建该目录。它总是被创建为目录。

如果指定的挂载路径在主机上不存在，`--mount` 不会自动创建目录。相反，它会产生一个错误：

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

### --mount 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由一个 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

`--mount type=bind` 的有效选项包括：

| 选项                          | 描述                                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| `source`, `src`               | 主机上文件或目录的位置。可以是绝对路径或相对路径。                                                       |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。必须是绝对路径。                                                           |
| `readonly`, `ro`              | 如果存在，则使绑定挂载以只读方式[挂载到容器中](#use-a-read-only-bind-mount)。                               |
| `bind-propagation`            | 如果存在，则更改[绑定传播](#configure-bind-propagation)。                                                 |

```console {title="示例"}
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### --volume 的选项

`--volume` 或 `-v` 标志由三个字段组成，用冒号字符（`:`）分隔。字段必须按正确顺序排列。

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

第一个字段是要绑定挂载到容器中的主机路径。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是一个逗号分隔的选项列表。绑定挂载的 `--volume` 有效选项包括：

| 选项                  | 描述                                                                                                          |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| `readonly`, `ro`      | 如果存在，则使绑定挂载以只读方式[挂载到容器中](#use-a-read-only-bind-mount)。                                    |
| `z`, `Z`              | 配置 SELinux 标签。请参阅[配置 SELinux 标签](#configure-the-selinux-label)                                      |
| `rprivate` (默认值)  | 将此挂载的绑定传播设置为 `rprivate`。请参阅[配置绑定传播](#configure-bind-propagation)。                        |
| `private`             | 将此挂载的绑定传播设置为 `private`。请参阅[配置绑定传播](#configure-bind-propagation)。                         |
| `rshared`             | 将此挂载的绑定传播设置为 `rshared`。请参阅[配置绑定传播](#configure-bind-propagation)。                         |
| `shared`              | 将此挂载的绑定传播设置为 `shared`。请参阅[配置绑定传播](#configure-bind-propagation)。                          |
| `rslave`              | 将此挂载的绑定传播设置为 `rslave`。请参阅[配置绑定传播](#configure-bind-propagation)。                          |
| `slave`               | 将此挂载的绑定传播设置为 `slave`。请参阅[配置绑定传播](#configure-bind-propagation)。                           |

```console {title="示例"}
$ docker run -v .:/project:ro,rshared
```

## 使用绑定挂载启动容器

考虑这样一种情况：您有一个目录 `source`，并且在构建源代码时，构建产物被保存到另一个目录 `source/target/` 中。您希望这些构建产物在容器中的 `/app/` 下可用，并且您希望每次在开发主机上构建源代码时，容器都能访问到新的构建。使用以下命令将 `target/` 目录绑定挂载到容器中的 `/app/`。在 `source` 目录内运行该命令。`$(pwd)` 子命令在 Linux 或 macOS 主机上会扩展为当前工作目录。如果您使用的是 Windows，另请参阅 [Windows 上的路径转换](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

以下 `--mount` 和 `-v` 示例产生相同的结果。除非在运行第一个示例后移除了 `devtest` 容器，否则您无法同时运行它们。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 来验证绑定挂载是否已正确创建。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```

这表明该挂载是一个 `bind` 挂载，显示了正确的源和目标，表明挂载是可读写的，并且传播设置为 `rprivate`。

停止并移除容器：

```console
$ docker container rm -fv devtest
```

### 挂载到容器中的一个非空目录

如果您将目录绑定挂载到容器中的一个非空目录，该目录的现有内容会被绑定挂载遮蔽。这可能是有益的，例如当您希望在不构建新镜像的情况下测试应用程序的新版本时。但是，这也可能令人意外，并且这种行为与[卷](volumes.md)的行为不同。

此示例设计得比较极端，它用主机上的 `/tmp/` 目录替换了容器的 `/usr/` 目录的内容。在大多数情况下，这会导致容器无法正常工作。

`--mount` 和 `-v` 示例的最终结果相同。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name broken-container \
  --mount type=bind,source=/tmp,target=/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name broken-container \
  -v /tmp:/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

{{< /tab >}}
{{< /tabs >}}

容器已创建但未启动。将其移除：

```console
$ docker container rm broken-container
```

## 使用只读绑定挂载

对于某些开发应用程序，容器需要写入绑定挂载，以便更改可以传播回 Docker 主机。而在其他时候，容器只需要读取访问权限。

此示例修改了前一个示例，但通过在容器内的挂载点之后，向（默认为空的）选项列表中添加 `ro`，将目录作为只读绑定挂载进行挂载。如果有多个选项，请用逗号分隔它们。

`--mount` 和 `-v` 示例的结果相同。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app,readonly \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:ro \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 来验证绑定挂载是否已正确创建。查找 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "ro",
        "RW": false,
        "Propagation": "rprivate"
    }
],
```

停止并移除容器：

```console
$ docker container rm -fv devtest
```

## 递归挂载

当您绑定挂载一个本身包含挂载的路径时，这些子挂载默认也会被包含在绑定挂载中。此行为是可配置的，使用 `--mount` 的 `bind-recursive` 选项。此选项仅支持 `--mount` 标志，不支持 `-v` 或 `--volume`。

如果绑定挂载是只读的，Docker 引擎会尽力尝试使子挂载也成为只读的。这被称为递归只读挂载。递归只读挂载需要 Linux 内核版本 5.12 或更高版本。如果您运行的是较旧的内核版本，子挂载默认会自动挂载为可读写。在早于 5.12 的内核版本上，尝试使用 `bind-recursive=readonly` 选项将子挂载设置为只读会导致错误。

`bind-recursive` 选项支持的值包括：

| 值                   | 描述                                                                                                       |
| :------------------- | :--------------------------------------------------------------------------------------------------------- |
| `enabled` (默认值)  | 如果内核是 v5.12 或更高版本，只读挂载将递归设置为只读。否则，子挂载为可读写。                               |
| `disabled`           | 子挂载被忽略（不包含在绑定挂载中）。                                                                       |
| `writable`           | 子挂载为可读写。                                                                                           |
| `readonly`           | 子挂载为只读。需要内核 v5.12 或更高版本。                                                                  |

## 配置绑定传播

绑定挂载和卷的绑定传播默认都为 `rprivate`。它仅对绑定挂载可配置，且仅限在 Linux 主机上。绑定传播是一个高级主题，许多用户永远不需要配置它。

绑定传播指的是在给定绑定挂载中创建的挂载是否可以传播到该挂载的副本。考虑一个挂载点 `/mnt`，它也被挂载在 `/tmp` 上。传播设置控制着 `/tmp/a` 上的挂载是否也会在 `/mnt/a` 上可用。每个传播设置都有一个递归的对应项。在递归的情况下，考虑 `/tmp/a` 也被挂载为 `/foo`。传播设置控制着 `/mnt/a` 和/或 `/tmp/a` 是否会存在。

> [!NOTE]
> 挂载传播不适用于 Docker Desktop。

| 传播设置     | 描述                                                                                                                                                                                                           |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `shared`     | 原始挂载的子挂载会暴露给副本挂载，副本挂载的子挂载也会传播回原始挂载。                                                                                                                                         |
| `slave`      | 类似于共享挂载，但仅是单向的。如果原始挂载暴露了一个子挂载，副本挂载可以看到它。但是，如果副本挂载暴露了一个子挂载，原始挂载无法看到它。                                                                       |
| `private`    | 该挂载是私有的。其中的子挂载不会暴露给副本挂载，副本挂载的子挂载也不会暴露给原始挂载。                                                                                                                       |
| `rshared`    | 与 shared 相同，但传播也扩展到嵌套在任何原始或副本挂载点内的挂载点，并从这些挂载点扩展出来。                                                                                                                  |
| `rslave`     | 与 slave 相同，但传播也扩展到嵌套在任何原始或副本挂载点内的挂载点，并从这些挂载点扩展出来。                                                                                                                   |
| `rprivate`   | 默认值。与 private 相同，意味着原始或副本挂载点内的任何挂载点都不会向任一方向传播。                                                                                                                           |

在您可以在挂载点上设置绑定传播之前，主机文件系统需要已经支持绑定传播。

有关绑定传播的更多信息，请参阅 [Linux 内核关于共享子树的文档](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)。

以下示例将 `target/` 目录两次挂载到容器中，第二次挂载同时设置了 `ro` 选项和 `rslave` 绑定传播选项。

`--mount` 和 `-v` 示例的结果相同。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}