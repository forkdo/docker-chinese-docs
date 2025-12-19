---
description:
  了解如何创建、管理和使用卷（volumes）而非绑定挂载（bind mounts）来持久化 Docker 生成和使用的数据。
title: 卷（Volumes）
weight: 10
keywords:
  docker compose volumes, docker volumes, docker compose volume, docker volume
  mount, docker mount volume, docker volume create, docker volume location
aliases:
  - /userguide/dockervolumes/
  - /engine/tutorials/dockervolumes/
  - /engine/userguide/dockervolumes/
  - /engine/admin/volumes/volumes/
  - /storage/volumes/
  - /engine/admin/volumes/backing-up/
---

卷是由 Docker 创建和管理的容器持久化数据存储机制。你可以使用 `docker volume create` 命令显式创建卷，也可以在创建容器或服务时由 Docker 自动创建。

创建卷时，它会被存储在 Docker 宿主机上的某个目录中。当将卷挂载到容器中时，该目录会被挂载到容器内部。这与绑定挂载的工作方式类似，但卷由 Docker 管理，并与宿主机的核心功能隔离。

## 何时使用卷

卷是持久化 Docker 容器生成和使用数据的推荐机制。虽然[绑定挂载](bind-mounts.md)依赖于宿主机的目录结构和操作系统，但卷完全由 Docker 管理。卷适用于以下场景：

- 卷比绑定挂载更容易备份或迁移。
- 可以使用 Docker CLI 命令或 Docker API 管理卷。
- 卷在 Linux 和 Windows 容器上均可使用。
- 卷可以更安全地在多个容器之间共享。
- 新卷的内容可以由容器或构建过程预填充。
- 当应用程序需要高性能 I/O 时。

如果需要从宿主机访问文件，则卷不是最佳选择，因为卷完全由 Docker 管理。如果需要同时从容器和宿主机访问文件或目录，请使用[绑定挂载](bind-mounts.md)。

与使用容器可写层直接写入数据相比，卷通常是更好的选择，因为卷不会增加使用它的容器的大小。使用卷也更快；写入容器的可写层需要[存储驱动](/manuals/engine/storage/drivers/_index.md)来管理文件系统。存储驱动通过 Linux 内核提供联合文件系统，这种额外的抽象会降低性能，而卷直接写入宿主机的文件系统，性能更高。

如果容器生成非持久化状态数据，请考虑使用[tmpfs 挂载](tmpfs.md)，以避免永久存储数据，并通过避免写入容器的可写层来提高容器性能。

卷使用 `rprivate`（递归私有）绑定传播方式，且卷的绑定传播不可配置。

## 卷的生命周期

卷的内容存在于容器的生命周期之外。当容器被销毁时，其可写层也会被销毁。使用卷可以确保即使使用它的容器被移除，数据仍然持久化。

一个卷可以同时挂载到多个容器中。当没有正在运行的容器使用某个卷时，该卷仍对 Docker 可用，且不会自动删除。你可以使用 `docker volume prune` 删除未使用的卷。

## 将卷挂载到已有数据上

如果将一个**非空卷**挂载到容器中已存在文件或目录的目录中，原有的文件会被挂载内容遮蔽。这类似于在 Linux 宿主机上将文件保存到 `/mnt`，然后将 USB 驱动器挂载到 `/mnt` —— 在卸载 USB 驱动器之前，`/mnt` 的内容会被 USB 驱动器的内容遮蔽。

在容器中，没有直接的方法可以移除挂载以重新显示被遮蔽的文件。最佳方案是重新创建不包含该挂载的容器。

如果将一个**空卷**挂载到容器中已存在文件或目录的目录中，这些文件或目录默认会被传播（复制）到卷中。类似地，如果启动容器时指定了一个尚不存在的卷，Docker 会为你创建一个空卷。这是预填充其他容器所需数据的好方法。

要防止 Docker 将容器的已有文件复制到空卷中，请使用 `volume-nocopy` 选项，参见 [--mount 选项](#options-for---mount)。

## 命名卷与匿名卷

卷可以是命名的或匿名的。匿名卷会被分配一个在特定 Docker 宿主机上保证唯一的随机名称。与命名卷一样，即使删除了使用它们的容器，匿名卷也会持续存在，除非在创建容器时使用了 `--rm` 标志，此时与该容器关联的匿名卷会被销毁。参见[删除匿名卷](volumes.md#remove-anonymous-volumes)。

如果连续创建多个使用匿名卷的容器，每个容器都会创建自己的卷。匿名卷不会在容器之间自动重用或共享。要在两个或多个容器之间共享匿名卷，必须使用随机卷 ID 挂载该匿名卷。

## 语法

要在 `docker run` 命令中挂载卷，可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=volume,src=<volume-name>,dst=<mount-path>
$ docker run --volume <volume-name>:<mount-path>
```

通常推荐使用 `--mount`。主要区别在于 `--mount` 更明确，且支持所有可用选项。

在以下情况下必须使用 `--mount`：

- 指定[卷驱动选项](#use-a-volume-driver)
- 挂载[卷子目录](#mount-a-volume-subdirectory)
- 将卷挂载到 Swarm 服务

### --mount 选项

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对采用 `<key>=<value>` 的形式。键的顺序不重要。

```console
$ docker run --mount type=volume[,src=<volume-name>],dst=<mount-path>[,<key>=<value>...]
```

`--mount type=volume` 的有效选项包括：

| 选项 | 描述 |
| --- | --- |
| `source`, `src` | 挂载源。对于命名卷，这是卷的名称；对于匿名卷，此字段省略。 |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。 |
| `volume-subpath` | 要挂载到容器中的卷内子目录路径。该子目录必须在卷挂载到容器之前存在于卷中。参见[挂载卷子目录](#mount-a-volume-subdirectory)。 |
| `readonly`, `ro` | 如果存在，卷将以[只读方式挂载到容器中](#use-a-read-only-volume)。 |
| `volume-nocopy` | 如果存在，当卷为空时，目标位置的数据不会被复制到卷中。默认情况下，如果目标位置有内容且卷为空，内容会被复制到挂载的卷中。 |
| `volume-opt` | 可多次指定，采用键值对形式，包含选项名称及其值。 |

```console {title="示例"}
$ docker run --mount type=volume,src=myvolume,dst=/data,ro,volume-subpath=/foo
```

### --volume 选项

`--volume` 或 `-v` 标志由三个字段组成，用冒号（`:`）分隔。字段必须按正确顺序排列。

```console
$ docker run -v [<volume-name>:]<mount-path>[:opts]
```

对于命名卷，第一个字段是卷的名称，在特定宿主机上唯一。对于匿名卷，第一个字段省略。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是一个逗号分隔的选项列表。使用数据卷时 `--volume` 的有效选项包括：

| 选项 | 描述 |
| --- | --- |
| `readonly`, `ro` | 如果存在，卷将以[只读方式挂载到容器中](#use-a-read-only-volume)。 |
| `volume-nocopy` | 如果存在，当卷为空时，目标位置的数据不会被复制到卷中。默认情况下，如果目标位置有内容且卷为空，内容会被复制到挂载的卷中。 |

```console {title="示例"}
$ docker run -v myvolume:/data:ro
```

## 创建和管理卷

与绑定挂载不同，你可以在任何容器之外创建和管理卷。

创建卷：

```console
$ docker volume create my-vol
```

列出卷：

```console
$ docker volume ls

local               my-vol
```

检查卷：

```console
$ docker volume inspect my-vol
[
    {
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/my-vol/_data",
        "Name": "my-vol",
        "Options": {},
        "Scope": "local"
    }
]
```

删除卷：

```console
$ docker volume rm my-vol
```

## 启动带卷的容器

如果启动容器时使用的卷尚不存在，Docker 会为你创建该卷。以下示例将卷 `myvol2` 挂载到容器的 `/app/` 目录。

以下 `-v` 和 `--mount` 示例会产生相同结果。除非在运行第一个示例后删除 `devtest` 容器和 `myvol2` 卷，否则不能同时运行这两个示例。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name devtest \
  --mount source=myvol2,target=/app \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name devtest \
  -v myvol2:/app \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect devtest` 验证 Docker 是否正确创建了卷并挂载。查看 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "volume",
        "Name": "myvol2",
        "Source": "/var/lib/docker/volumes/myvol2/_data",
        "Destination": "/app",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    }
],
```

这表明挂载是一个卷，显示了正确的源和目标，且挂载为读写模式。

停止容器并删除卷。注意：删除卷是一个独立步骤。

```console
$ docker container stop devtest

$ docker container rm devtest

$ docker volume rm myvol2
```

## 在 Docker Compose 中使用卷

以下示例展示了一个带有卷的 Docker Compose 服务：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
```

首次运行 `docker compose up` 时会创建一个卷。后续运行该命令时，Docker 会重用同一个卷。

你可以使用 `docker volume create` 在 Compose 之外直接创建卷，然后在 `compose.yaml` 中引用它：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
    external: true
```

有关在 Compose 中使用卷的更多信息，请参阅 Compose 规范中的[卷（Volumes）](/reference/compose-file/volumes.md)部分。

### 启动带卷的服务

启动服务并定义卷时，每个服务容器都会使用自己的本地卷。如果使用 `local` 卷驱动，任何容器都无法共享这些数据。但某些卷驱动确实支持共享存储。

以下示例启动一个包含四个副本的 `nginx` 服务，每个副本都使用名为 `myvol2` 的本地卷。

```console
$ docker service create -d \
  --replicas=4 \
  --name devtest-service \
  --mount source=myvol2,target=/app \
  nginx:latest
```

使用 `docker service ps devtest-service` 验证服务是否正在运行：

```console
$ docker service ps devtest-service

ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
4d7oz1j85wwn        devtest-service.1   nginx:latest        moby                Running             Running 14 seconds ago
```

你可以删除服务以停止正在运行的任务：

```console
$ docker service rm devtest-service
```

删除服务不会删除服务创建的卷。删除卷是一个独立步骤。

### 使用容器填充卷

如果启动一个创建新卷的容器，且该容器在要挂载的目录（如 `/app/`）中有文件或目录，Docker 会将该目录的内容复制到卷中。然后容器会挂载并使用该卷，其他使用该卷的容器也可以访问预填充的内容。

为演示这一点，以下示例启动一个 `nginx` 容器，并将容器 `/usr/share/nginx/html` 目录的内容填充到新卷 `nginx-vol` 中。这是 Nginx 存储默认 HTML 内容的位置。

`--mount` 和 `-v` 示例的最终结果相同。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  -v nginx-vol:/usr/share/nginx/html \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

运行上述任一示例后，运行以下命令清理容器和卷。注意：删除卷是一个独立步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 使用只读卷

对于某些开发应用程序，容器需要写入绑定挂载，以便将更改传播回 Docker 宿主机。而在其他情况下，容器只需要读取数据的权限。多个容器可以挂载同一个卷。你可以同时将单个卷以 `read-write` 模式挂载给某些容器，以 `read-only` 模式挂载给其他容器。

以下示例修改了前面的示例，通过添加 `ro` 到挂载点后的选项列表（默认为空），将目录挂载为只读卷。如果存在多个选项，可以用逗号分隔。

`--mount` 和 `-v` 示例的结果相同。

{{< tabs >}}
{{< tab name="`--mount`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  --mount source=nginx-vol,destination=/usr/share/nginx/html,readonly \
  nginx:latest
```

{{< /tab >}}
{{< tab name="`-v`" >}}

```console
$ docker run -d \
  --name=nginxtest \
  -v nginx-vol:/usr/share/nginx/html:ro \
  nginx:latest
```

{{< /tab >}}
{{< /tabs >}}

使用 `docker inspect nginxtest` 验证 Docker 是否正确创建了只读挂载。查看 `Mounts` 部分：

```json
"Mounts": [
    {
        "Type": "volume",
        "Name": "nginx-vol",
        "Source": "/var/lib/docker/volumes/nginx-vol/_data",
        "Destination": "/usr/share/nginx/html",
        "Driver": "local",
        "Mode": "",
        "RW": false,
        "Propagation": ""
    }
],
```

停止并删除容器，然后删除卷。删除卷是一个独立步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 挂载卷子目录

将卷挂载到容器时，可以使用 `--mount` 标志的 `volume-subpath` 参数指定使用卷的子目录。指定的子目录必须在尝试挂载到容器之前存在于卷中；如果不存在，挂载会失败。

指定 `volume-subpath` 很有用，如果你只想与容器共享卷的特定部分。例如，你有多个正在运行的容器，并希望将每个容器的日志存储在共享卷中。你可以在共享卷中为每个容器创建子目录，并将子目录挂载到容器。

以下示例创建一个 `logs` 卷，并在卷中初始化 `app1` 和 `app2` 子目录。然后启动两个容器，并将 `logs` 卷的一个子目录挂载到每个容器。此示例假设容器中的进程将其日志写入 `/var/log/app1` 和 `/var/log/app2`。

```console
$ docker volume create logs
$ docker run --rm \
  --mount src=logs,dst=/logs \
  alpine mkdir -p /logs/app1 /logs/app2
$ docker run -d \
  --name=app1 \
  --mount src=logs,dst=/var/log/app1,volume-subpath=app1 \
  app1:latest
$ docker run -d \
  --name=app2 \
  --mount src=logs,dst=/var/log/app2,volume-subpath=app2 \
  app2:latest
```

通过此设置，容器将其日志写入 `logs` 卷的单独子目录中。容器无法访问其他容器的日志。

## 在机器之间共享数据

构建容错应用程序时，可能需要配置同一服务的多个副本，使其能够访问相同的文件。

![共享存储](images/volumes-shared-storage.webp)

在开发应用程序时有几种方法可以实现这一点。一种是在应用程序中添加逻辑，将文件存储在云对象存储系统（如 Amazon S3）上。另一种是使用支持将文件写入外部存储系统（如 NFS 或 Amazon S3）的驱动创建卷。

卷驱动让你可以将底层存储系统与应用程序逻辑解耦。例如，如果你的服务使用带有 NFS 驱动的卷，你可以更新服务以使用不同的驱动（例如将数据存储在云中），而无需更改应用程序逻辑。

## 使用卷驱动

使用 `docker volume create` 创建卷，或启动使用尚未创建的卷的容器时，可以指定卷驱动。以下示例使用 `rclone/docker-volume-rclone` 卷驱动，首先在创建独立卷时，然后在启动创建新卷的容器时。

> [!NOTE]
>
> 如果你的卷驱动接受逗号分隔的列表作为选项，你必须从外部 CSV 解析器中转义该值。要转义 `volume-opt`，请用双引号（`"`）包围它，并用单引号（`'`）包围整个挂载参数。
>
> 例如，`local` 驱动接受挂载选项作为 `o` 参数中的逗号分隔列表。此示例展示了正确转义列表的方法。
>
> ```console
> $ docker service create \
>  --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>,volume-driver=local,volume-opt=type=nfs,volume-opt=device=<nfs-server>:<nfs-path>,"volume-opt=o=addr=<nfs-address>,vers=4,soft,timeo=180,bg,tcp,rw"'
>  --name myservice \
>  <IMAGE>
> ```

### 初始设置

以下示例假设你有两个节点，第一个节点是 Docker 宿主机，可以通过 SSH 连接到第二个节点。

在 Docker 宿主机上安装 `rclone/docker-volume-rclone` 插件：

```console
$ docker plugin install --grant-all-permissions rclone/docker-volume-rclone --aliases rclone
```

### 使用卷驱动创建卷

此示例将主机 `1.2.3.4` 上的 `/remote` 目录挂载到名为 `rclonevolume` 的卷中。每个卷驱动可能有零个或多个可配置选项，你可以使用 `-o` 标志指定每个选项。

```console
$ docker volume create \
  -d rclone \
  --name rclonevolume \
  -o type=sftp \
  -o path=remote \
  -o sftp-host=1.2.3.4 \
  -o sftp-user=user \
  -o "sftp-password=$(cat file_containing_password_for_remote_host)"
```

现在可以将此卷挂载到容器中。

### 启动使用卷驱动创建卷的容器

> [!NOTE]
>
> 如果卷驱动要求你传递任何选项，必须使用 `--mount` 标志挂载卷，而不能使用 `-v`。

```console
$ docker run -d \
  --name rclone-container \
  --mount type=volume,volume-driver=rclone,src=rclonevolume,target=/app,volume-opt=type=sftp,volume-opt=path=remote, volume-opt=sftp-host=1.2.3.4,volume-opt=sftp-user=user,volume-opt=-o "sftp-password=$(cat file_containing_password_for_remote_host)" \
  nginx:latest
```

### 创建创建 NFS 卷的服务

以下示例展示了如何在创建服务时创建 NFS 卷。它使用 `10.0.0.10` 作为 NFS 服务器，`/var/docker-nfs` 作为 NFS 服务器上的导出目录。注意指定的卷驱动是 `local`。

#### NFSv3

```console
$ docker service create -d \
  --name nfs-service \
  --mount 'type=volume,source=nfsvolume,target=/app,volume-driver=local,volume-opt=type=nfs,volume-opt=device=:/var/docker-nfs,volume-opt=o=addr=10.0.0.10' \
  nginx:latest
```

#### NFSv4

```console
$ docker service create -d \
    --name nfs-service \
    --mount 'type=volume,source=nfsvolume,target=/app,volume-driver=local,volume-opt=type=nfs,volume-opt=device=:/var/docker-nfs,"volume-opt=o=addr=10.0.0.10,rw,nfsvers=4,async"' \
    nginx:latest
```

### 创建 CIFS/Samba 卷

你可以在 Docker 中直接挂载 Samba 共享，而无需在宿主机上配置挂载点。

```console
$ docker volume create \
	--driver local \
	--opt type=cifs \
	--opt device=//uxxxxx.your-server.de/backup \
	--opt o=addr=uxxxxx.your-server.de,username=uxxxxxxx,password=*****,file_mode=0777,dir_mode=0777 \
	--name cifs-volume
```

如果指定主机名而非 IP，则 `addr` 选项是必需的。这允许 Docker 执行主机名查找。

### 块存储设备

你可以将块存储设备（如外部驱动器或驱动器分区）挂载到容器。以下示例展示了如何创建和使用文件作为块存储设备，以及如何将块设备挂载为容器卷。

> [!IMPORTANT]
>
> 以下过程仅作为示例。此处展示的解决方案不推荐作为通用实践。除非你确信自己在做什么，否则不要尝试此方法。

#### 块设备挂载的工作原理

在底层，使用 `local` 存储驱动的 `--mount` 标志会调用 Linux 的 `mount` 系统调用，并将你传递的选项原样转发。Docker 不会在 Linux 内核支持的本地挂载功能之上实现任何额外功能。

如果你熟悉 [Linux `mount` 命令](https://man7.org/linux/man-pages/man8/mount.8.html)，可以将 `--mount` 选项视为以下方式转发到 `mount` 命令：

```console
$ mount -t <mount.volume-opt.type> <mount.volume-opt.device> <mount.dst> -o <mount.volume-opts.o>
```

为更清楚地说明这一点，考虑以下 `mount` 命令示例。此命令将 `/dev/loop5` 设备挂载到系统上的 `/external-drive` 路径。

```console
$ mount -t ext4 /dev/loop5 /external-drive
```

以下 `docker run` 命令从运行容器的角度来看实现了类似的结果。使用此 `--mount` 选项运行容器，会以与执行前述 `mount` 命令相同的方式设置挂载。

```console
$ docker run \
  --mount='type=volume,dst=/external-drive,volume-driver=local,volume-opt=device=/dev/loop5,volume-opt=type=ext4'
```

你不能直接在容器内运行 `mount` 命令，因为容器无法访问 `/dev/loop5` 设备。这就是 `docker run` 命令使用 `--mount` 选项的原因。

#### 示例：在容器中挂载块设备

以下步骤创建一个 `ext4` 文件系统并将其挂载到容器中。你的系统对文件系统的支持取决于所使用的 Linux 内核版本。

1. 创建一个文件并为其分配一些空间：

   ```console
   $ fallocate -l 1G disk.raw
   ```

2. 在 `disk.raw` 文件上构建文件系统：

   ```console
   $ mkfs.ext4 disk.raw
   ```

3. 创建 loop 设备：

   ```console
   $ losetup -f --show disk.raw
   /dev/loop5
   ```

   > [!NOTE]
   >
   > `losetup` 创建一个临时 loop 设备，系统重启后或手动使用 `losetup -d` 删除后会被移除。

4. 运行一个将 loop 设备挂载为卷的容器：

   ```console
   $ docker run -it --rm \
     --mount='type=volume,dst=/external-drive,volume-driver=local,volume-opt=device=/dev/loop5,volume-opt=type=ext4' \
     ubuntu bash
   ```

   容器启动时，路径 `/external-drive` 会将宿主机的 `disk.raw` 文件作为块设备挂载。

5. 完成后，当设备从容器卸载时，分离 loop 设备以从宿主机系统移除设备：

   ```console
   $ losetup -d /dev/loop5
   ```

## 备份、恢复或迁移数据卷

卷对备份、恢复和迁移很有用。使用 `--volumes-from` 标志创建一个挂载该卷的新容器。

### 备份卷

例如，创建一个名为 `dbstore` 的新容器：

```console
$ docker run -v /dbdata --name dbstore ubuntu /bin/bash
```

在下一个命令中：

- 启动一个新容器并挂载 `dbstore` 容器的卷
- 将本地宿主机目录挂载为 `/backup`
- 传递一个命令，将 `dbdata` 卷的内容打包到 `/backup` 目录中的 `backup.tar` 文件。

```console
$ docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
```

命令完成且容器停止时，会创建 `dbdata` 卷的备份。

### 从备份恢复卷

使用刚创建的备份，可以将其恢复到同一容器，或恢复到在其他地方创建的另一容器。

例如，创建一个名为 `dbstore2` 的新容器：

```console
$ docker run -v /dbdata --name dbstore2 ubuntu /bin/bash
```

然后，在新容器的数据卷中解压备份文件：

```console
$ docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"
```

你可以使用这些技术，结合你喜欢的工具，自动化备份、迁移和恢复测试。

## 删除卷

Docker 数据卷在删除容器后仍会持续存在。需要考虑两种类型的卷：

- 命名卷有来自容器外部的特定源，例如 `awesome:/bar`。
- 匿名卷没有特定源。因此，删除容器时，可以指示 Docker Engine 守护进程删除它们。

### 删除匿名卷

要自动删除匿名卷，请使用 `--rm` 选项。例如，此命令创建一个匿名 `/foo` 卷。删除容器时，Docker Engine 会删除 `/foo` 卷，但不会删除 `awesome` 卷。

```console
$ docker run --rm -v /foo -v awesome:/bar busybox top
```

> [!NOTE]
>
> 如果另一个容器使用 `--volumes-from` 绑定卷，卷定义会被**复制**，且第一个容器删除后匿名卷仍会保留。

### 删除所有卷

要删除所有未使用的卷并释放空间：

```console
$ docker volume prune
```

## 下一步

- 了解[绑定挂载](bind-mounts.md)。
- 了解[tmpfs 挂载](tmpfs.md)。
- 了解[存储驱动](/engine/storage/drivers/)。
- 了解[第三方卷驱动插件](/engine/extend/legacy_plugins/)。