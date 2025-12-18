---
description: 使用绑定挂载
title: 绑定挂载
weight: 20
keywords: 存储, 持久化, 数据持久化, 挂载, 绑定挂载
aliases:
  - /engine/admin/volumes/bind-mounts/
  - /storage/bind-mounts/
---

使用绑定挂载时，会将主机上的文件或目录从主机挂载到容器中。相比之下，使用卷时，会在主机上的 Docker 存储目录内创建一个新目录，Docker 管理该目录的内容。

## 何时使用绑定挂载

绑定挂载适用于以下使用场景：

- 在 Docker 主机上的开发环境和容器之间共享源代码或构建产物。

- 当你希望在容器中创建或生成文件，并将文件持久化到主机文件系统上时。

- 将主机上的配置文件共享到容器中。这是 Docker 默认向容器提供 DNS 解析的方式，通过将主机上的 `/etc/resolv.conf` 挂载到每个容器中实现。

绑定挂载也可用于构建：你可以将主机上的源代码绑定挂载到构建容器中，以测试、检查或编译项目。

## 覆盖现有数据的绑定挂载

如果你将文件或目录绑定挂载到容器中的某个目录，而该目录已存在文件或目录，则预先存在的文件会被挂载遮蔽。这类似于在 Linux 主机上将文件保存到 `/mnt`，然后将 U 盘挂载到 `/mnt`。在 U 盘卸载之前，`/mnt` 的内容会被 U 盘的内容遮蔽。

对于容器，没有直接的方法可以移除挂载以再次显示被遮蔽的文件。最好的选择是重新创建一个没有该挂载的容器。

## 考虑因素和约束

- 绑定挂载默认具有对主机文件的写入权限。

  使用绑定挂载的一个副作用是，你可以通过容器中运行的进程更改主机文件系统，包括创建、修改或删除重要的系统文件或目录。这种能力可能带来安全影响。例如，它可能影响主机系统上的非 Docker 进程。

  你可以使用 `readonly` 或 `ro` 选项来防止容器向挂载点写入。

- 绑定挂载是相对于 Docker 守护进程主机创建的，而不是客户端。

  如果你使用远程 Docker 守护进程，则无法创建绑定挂载来访问客户端机器上的文件到容器中。

  对于 Docker Desktop，守护进程在 Linux 虚拟机内运行，而不是直接在本机主机上运行。Docker Desktop 具有内置机制，可以透明地处理绑定挂载，允许你与虚拟机中运行的容器共享本机主机文件系统路径。

- 使用绑定挂载的容器与主机紧密耦合。

  绑定挂载依赖于主机文件系统具有特定的目录结构。这种依赖意味着使用绑定挂载的容器在运行于具有不同目录结构的其他主机上时可能会失败。

## 语法

要创建绑定挂载，你可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

通常，推荐使用 `--mount`。主要区别是 `--mount` 标志更明确，并支持所有可用选项。

如果你使用 `--volume` 绑定挂载一个在 Docker 主机上尚不存在的文件或目录，Docker 会自动为你在主机上创建该目录。它总是被创建为目录。

如果指定的挂载路径在主机上不存在，`--mount` 不会自动创建目录。相反，它会产生一个错误：

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

### --mount 的选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

`--mount type=bind` 的有效选项包括：

| 选项                         | 描述                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `source`, `src`                | 主机上文件或目录的位置。可以是绝对路径或相对路径。                    |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。必须是绝对路径。                     |
| `readonly`, `ro`               | 如果存在，会导致绑定挂载以[只读方式挂载到容器中](#use-a-read-only-bind-mount)。 |
| `bind-propagation`             | 如果存在，会更改[绑定传播](#configure-bind-propagation)。                                        |

```console {title="示例"}
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### --volume 的选项

`--volume` 或 `-v` 标志由三个字段组成，用冒号字符 (`:`) 分隔。字段必须按正确顺序排列。

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

第一个字段是主机上绑定挂载到容器中的文件或目录的路径。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是逗号分隔的选项列表。`--volume` 绑定挂载的有效选项包括：

| 选项               | 描述                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `readonly`, `ro`     | 如果存在，会导致绑定挂载以[只读方式挂载到容器中](#use-a-read-only-bind-mount)。    |
| `z`, `Z`             | 配置 SELinux 标签。参见 [配置 SELinux 标签](#configure-the-selinux-label)                       |
| `rprivate` (默认)    | 为该挂载设置绑定传播为 `rprivate`。参见 [配置绑定传播](#configure-bind-propagation)。 |
| `private`            | 为该挂载设置绑定传播为 `private`。参见 [配置绑定传播](#configure-bind-propagation)。  |
| `rshared`            | 为该挂载设置绑定传播为 `rshared`。参见 [配置绑定传播](#configure-bind-propagation)。  |
| `shared`             | 为该挂载设置绑定传播为 `shared`。参见 [配置绑定传播](#configure-bind-propagation)。   |
| `rslave`             | 为该挂载设置绑定传播为 `rslave`。参见 [配置绑定传播](#configure-bind-propagation)。   |
| `slave`              | 为该挂载设置绑定传播为 `slave`。参见 [配置绑定传播](#configure-bind-propagation)。    |

```console {title="示例"}
$ docker run -v .:/project:ro,rshared
```

## 使用绑定挂载启动容器

考虑一个场景，你有一个目录 `source`，当你构建源代码时，产物会保存到另一个目录 `source/target/` 中。你希望容器在 `/app/` 处可以访问这些产物，并且希望容器在主机上每次构建源代码时都能获得新构建的产物。使用以下命令将 `target/` 目录绑定挂载到容器的 `/app/` 中。在 `source` 目录中运行该命令。`$(pwd)` 子命令在 Linux 或 macOS 主机上展开为当前工作目录。如果你使用 Windows，请另见 [Windows 上的路径转换](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

以下 `--mount` 和 `-v` 示例产生相同的结果。除非你在运行第一个后移除 `devtest` 容器，否则无法同时运行它们。

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

使用 `docker inspect devtest` 验证绑定挂载是否正确创建。查找 `Mounts` 部分：

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

这显示挂载是 `bind` 挂载，显示了正确的源和目标，显示挂载是读写模式，且传播设置为 `rprivate`。

停止并移除容器：

```console
$ docker container rm -fv devtest
```

### 挂载到容器中的非空目录

如果你将目录绑定挂载到容器中的非空目录，目录的现有内容会被绑定挂载遮蔽。这可能是有益的，比如当你想在不构建新镜像的情况下测试应用程序的新版本时。但这也可能令人意外，且这种行为与 [卷](volumes.md) 的行为不同。

这个例子是人为极端的，但它用主机机器上的 `/tmp/` 目录替换了容器的 `/usr/` 目录的内容。在大多数情况下，这会导致容器无法正常运行。

`--mount` 和 `-v` 示例具有相同的最终结果。

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

容器被创建但未启动。移除它：

```console
$ docker container rm broken-container
```

## 使用只读绑定挂载

对于某些开发应用程序，容器需要写入绑定挂载，以便更改传播回 Docker 主机。在其他时候，容器只需要读取访问。

此示例修改了前面的示例，但将目录作为只读绑定挂载挂载，通过在（默认为空）容器内挂载点选项列表中添加 `ro` 来实现。当存在多个选项时，用逗号分隔它们。

`--mount` 和 `-v` 示例具有相同的结果。

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

使用 `docker inspect devtest` 验证绑定挂载是否正确创建。查找 `Mounts` 部分：

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

当你绑定挂载一个本身包含挂载的路径时，默认情况下这些子挂载也包含在绑定挂载中。这种行为是可配置的，使用 `--mount` 的 `bind-recursive` 选项。此选项仅支持 `--mount` 标志，不支持 `-v` 或 `--volume`。

如果绑定挂载是只读的，Docker Engine 会尽力将子挂载也设为只读。这被称为递归只读挂载。递归只读挂载需要 Linux 内核版本 5.12 或更高版本。如果你运行较旧的内核版本，子挂载默认自动以读写方式挂载。在早于 5.12 的内核版本上尝试使用 `bind-recursive=readonly` 选项将子挂载设为只读，会导致错误。

`bind-recursive` 选项的受支持值包括：

| 值               | 描述                                                                                                       |
| :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| `enabled` (默认)    | 如果内核是 v5.12 或更高版本，只读挂载被递归设为只读。否则，子挂载是读写的。 |
| `disabled`          | 子挂载被忽略（不包含在绑定挂载中）。                                                           |
| `writable`          | 子挂载是读写的。                                                                                         |
| `readonly`          | 子挂载是只读的。需要内核 v5.12 或更高版本。                                                          |

## 配置绑定传播

绑定传播默认为 `rprivate`，对绑定挂载和卷都是如此。它仅对绑定挂载可配置，且仅在 Linux 主机上。绑定传播是一个高级主题，许多用户永远不需要配置它。

绑定传播指的是在给定绑定挂载内创建的挂载是否可以传播到该挂载的副本。考虑一个挂载点 `/mnt`，它也被挂载到 `/tmp`。传播设置控制 `/tmp/a` 上的挂载是否在 `/mnt/a` 上也可用。每个传播设置都有一个递归对应项。在递归的情况下，考虑 `/tmp/a` 也被挂载为 `/foo`。传播设置控制 `/mnt/a` 和/或 `/tmp/a` 是否存在。

> [!NOTE]
> 挂载传播在 Docker Desktop 上不工作。

| 传播设置 | 描述                                                                                                                                                                                                         |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `shared`            | 原始挂载的子挂载暴露给副本挂载，副本挂载的子挂载也传播到原始挂载。                                                                         |
| `slave`             | 类似于共享挂载，但仅单向。如果原始挂载暴露子挂载，副本挂载可以看到它。但是，如果副本挂载暴露子挂载，原始挂载无法看到它。 |
| `private`           | 挂载是私有的。其内的子挂载不暴露给副本挂载，副本挂载的子挂载也不暴露给原始挂载。                                                               |
| `rshared`           | 与共享相同，但传播也扩展到原始或副本挂载点内嵌套的任何挂载点。                                                                            |
| `rslave`            | 与从属相同，但传播也扩展到原始或副本挂载点内嵌套的任何挂载点。                                                                             |
| `rprivate`          | 默认值。与私有相同，意味着原始或副本挂载点内的任何挂载点都不在任一方向上传播。                                                                  |

在你可以在挂载点上设置绑定传播之前，主机文件系统需要已经支持绑定传播。

有关绑定传播的更多信息，请参阅 [Linux 内核共享子树文档](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)。

以下示例将 `target/` 目录挂载到容器中两次，第二次挂载同时设置 `ro` 选项和 `rslave` 绑定传播选项。

`--mount` 和 `-v` 示例具有相同的结果。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  -v "$(pwd)"/target:/app2:ro,rslave \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

现在，如果你创建 `/app/foo/`，`/app2/foo/` 也存在。

## 配置 SELinux 标签

如果你使用 SELinux，可以添加 `z` 或 `Z` 选项来修改挂载到容器中的主机文件或目录的 SELinux 标签。这会影响主机机器上的文件或目录本身，并可能在 Docker 范围之外产生后果。

- `z` 选项表示绑定挂载内容在多个容器之间共享。
- `Z` 选项表示绑定挂载内容是私有的且不共享。

对这些选项使用极度谨慎。使用 `Z` 选项绑定挂载系统目录（如 `/home` 或 `/usr`）会使你的主机机器无法运行，你可能需要手动重新标记主机机器文件。

> [!IMPORTANT]
>
> 使用服务时绑定挂载，SELinux 标签（`:Z` 和 `:z`）以及 `:ro` 被忽略。详情请见 [moby/moby #32579](https://github.com/moby/moby/issues/32579)。

此示例设置 `z` 选项以指定多个容器可以共享绑定挂载的内容：

无法使用 `--mount` 标志修改 SELinux 标签。

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:z \
  nginx:latest
```

## 在 Docker Compose