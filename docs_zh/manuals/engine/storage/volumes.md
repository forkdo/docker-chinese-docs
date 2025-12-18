---
description:
  学习如何创建、管理和使用卷，替代绑定挂载，以持久化 Docker 生成和使用的数据。
title: 卷（Volumes）
weight: 10
keywords:
  docker compose volumes, docker volumes, docker compose volume, docker volume mount, docker mount volume, docker volume create, docker volume location
aliases:
  - /userguide/dockervolumes/
  - /engine/tutorials/dockervolumes/
  - /engine/userguide/dockervolumes/
  - /engine/admin/volumes/volumes/
  - /storage/volumes/
  - /engine/admin/volumes/backing-up/
---

卷是容器的持久化数据存储，由 Docker 创建和管理。你可以使用 `docker volume create` 命令显式创建卷，或者 Docker 可以在容器或服务创建期间自动创建卷。

当你创建一个卷时，它会被存储在 Docker 主机上的某个目录中。当你将卷挂载到容器中时，就是将这个目录挂载到容器中。这与绑定挂载的工作方式类似，不同之处在于卷由 Docker 管理，并且与主机核心功能隔离。

## 何时使用卷

卷是持久化 Docker 容器生成和使用数据的首选机制。虽然 [绑定挂载](bind-mounts.md) 依赖于主机的目录结构和操作系统，但卷完全由 Docker 管理。卷适用于以下使用场景：

- 卷比绑定挂载更容易备份或迁移。
- 你可以使用 Docker CLI 命令或 Docker API 管理卷。
- 卷在 Linux 和 Windows 容器上都能工作。
- 卷可以更安全地在多个容器之间共享。
- 新卷可以通过容器或构建预先填充内容。
- 当你的应用需要高性能 I/O 时。

如果你需要从主机访问文件，卷不是好的选择，因为卷完全由 Docker 管理。如果你需要从容器和主机都访问文件或目录，请使用 [绑定挂载](bind-mounts.md)。

卷通常是比直接向容器写入数据更好的选择，因为卷不会增加使用它的容器的大小。使用卷也更快；写入容器的可写层需要 [存储驱动](/manuals/engine/storage/drivers/_index.md) 来管理文件系统。存储驱动提供联合文件系统，使用 Linux 内核。这种额外的抽象会降低性能，与直接写入主机文件系统的卷相比性能较差。

如果你的容器生成非持久化的状态数据，请考虑使用 [tmpfs 挂载](tmpfs.md) 以避免将数据永久存储在任何地方，并通过避免写入容器的可写层来提高容器的性能。

卷使用 `rprivate`（递归私有）绑定传播，卷的绑定传播不可配置。

## 卷的生命周期

卷的内容存在于特定容器的生命周期之外。当容器被销毁时，可写层也随其一起被销毁。使用卷可确保即使使用它的容器被移除，数据也能持久化。

给定的卷可以同时挂载到多个容器中。当没有运行中的容器使用卷时，卷仍然对 Docker 可用，不会被自动删除。你可以使用 `docker volume prune` 删除未使用的卷。

## 将卷挂载到现有数据上

如果你将一个_非空卷_挂载到容器中的某个目录，而该目录中已存在文件或目录，则预先存在的文件会被挂载遮蔽。这类似于如果你将文件保存到 Linux 主机的 `/mnt`，然后将 U 盘挂载到 `/mnt`。U 盘的内容会遮蔽 `/mnt` 的内容，直到 U 盘被卸载。

对于容器，没有直接的方法卸载挂载以再次显示被遮蔽的文件。你最好的选择是重新创建容器而不使用挂载。

如果你将一个_空卷_挂载到容器中的某个目录，而该目录中已存在文件或目录，这些文件或目录默认会被传播（复制）到卷中。类似地，如果你启动一个容器并指定一个尚不存在的卷，会为你创建一个空卷。这是预先填充另一个容器所需数据的好方法。

要防止 Docker 将容器的预先存在的文件复制到空卷中，请使用 `volume-nocopy` 选项，参见 [Options for --mount](#options-for---mount)。

## 命名卷和匿名卷

卷可以是命名的或匿名的。匿名卷被赋予一个随机名称，该名称在给定的 Docker 主机内保证唯一。与命名卷一样，匿名卷即使在你删除使用它们的容器后也会持久化，除非你在创建容器时使用 `--rm` 标志，这种情况下与容器关联的匿名卷会被销毁。参见 [Remove anonymous volumes](volumes.md#remove-anonymous-volumes)。

如果你连续创建多个使用匿名卷的容器，每个容器都会创建自己的卷。匿名卷不会自动在容器之间重用或共享。要在两个或多个容器之间共享匿名卷，你必须使用随机卷 ID 挂载匿名卷。

## 语法

要使用 `docker run` 命令挂载卷，你可以使用 `--mount` 或 `--volume` 标志。

```console
$ docker run --mount type=volume,src=<volume-name>,dst=<mount-path>
$ docker run --volume <volume-name>:<mount-path>
```

通常，`--mount` 更受推荐。主要区别是 `--mount` 标志更明确，并支持所有可用选项。

如果你想执行以下操作，必须使用 `--mount`：

- 指定 [卷驱动选项](#use-a-volume-driver)
- 挂载 [卷子目录](#mount-a-volume-subdirectory)
- 将卷挂载到 Swarm 服务中

### Options for --mount

`--mount` 标志由多个键值对组成，用逗号分隔，每个键值对由 `<key>=<value>` 元组组成。键的顺序不重要。

```console
$ docker run --mount type=volume[,src=<volume-name>],dst=<mount-path>[,<key>=<value>...]
```

`--mount type=volume` 的有效选项包括：

| 选项                         | 描述                                                                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source`, `src`                | 挂载的源。对于命名卷，这是卷的名称。对于匿名卷，此字段被省略。                                                                                                                                                                       |
| `destination`, `dst`, `target` | 文件或目录在容器中挂载的路径。                                                                                                                                                                                                       |
| `volume-subpath`               | 卷内要挂载到容器中的子目录路径。子目录必须在卷挂载到容器之前存在于卷中。参见 [Mount a volume subdirectory](#mount-a-volume-subdirectory)。                                                                                           |
| `readonly`, `ro`               | 如果存在，会导致卷被[以只读方式挂载到容器中](#use-a-read-only-volume)。                                                                                                                                                                                         |
| `volume-nocopy`                | 如果存在，当卷为空时，目标位置的数据不会被复制到卷中。默认情况下，如果卷为空，目标位置的内容会被复制到挂载的卷中。                                                                                                              |
| `volume-opt`                   | 可以指定多次，接受由选项名称和其值组成的键值对。                                                                                                                            |

```console {title="示例"}
$ docker run --mount type=volume,src=myvolume,dst=/data,ro,volume-subpath=/foo
```

### Options for --volume

`--volume` 或 `-v` 标志由三个字段组成，用冒号字符 (`:`) 分隔。字段必须按正确顺序排列。

```console
$ docker run -v [<volume-name>:]<mount-path>[:opts]
```

在命名卷的情况下，第一个字段是卷的名称，在给定的主机上是唯一的。对于匿名卷，第一个字段被省略。第二个字段是文件或目录在容器中挂载的路径。

第三个字段是可选的，是逗号分隔的选项列表。`--volume` 与数据卷的有效选项包括：

| 选项           | 描述                                                                                                                                                                        |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `readonly`, `ro` | 如果存在，会导致卷被[以只读方式挂载到容器中](#use-a-read-only-volume)。                                                                            |
| `volume-nocopy`  | 如果存在，当卷为空时，目标位置的数据不会被复制到卷中。默认情况下，如果卷为空，目标位置的内容会被复制到挂载的卷中。 |

```console {title="示例"}
$ docker run -v myvolume:/data:ro
```

## 创建和管理卷

与绑定挂载不同，你可以在任何容器范围之外创建和管理卷。

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

## 使用卷启动容器

如果你使用尚不存在的卷启动容器，Docker 会为你创建该卷。以下示例将卷 `myvol2` 挂载到容器中的 `/app/`。

以下 `-v` 和 `--mount` 示例产生相同的结果。除非你在运行第一个示例后删除 `devtest` 容器和 `myvol2` 卷，否则你不能同时运行它们。

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

使用 `docker inspect devtest` 验证 Docker 创建了卷并正确挂载。查找 `Mounts` 部分：

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

这显示挂载是卷，显示正确的源和目标，以及挂载是读写模式。

停止容器并删除卷。注意卷删除是单独的步骤。

```console
$ docker container stop devtest

$ docker container rm devtest

$ docker volume rm myvol2
```

## 在 Docker Compose 中使用卷

以下示例显示了一个带有卷的单个 Docker Compose 服务：

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - myapp:/home/node/app
volumes:
  myapp:
```

首次运行 `docker compose up` 时会创建一个卷。当你后续运行该命令时，Docker 会重用同一个卷。

你可以在 Compose 之外直接使用 `docker volume create` 创建卷，然后在 `compose.yaml` 中引用它，如下所示：

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

有关在 Compose 中使用卷的更多信息，请参考 Compose 规范中的 [Volumes](/reference/compose-file/volumes.md) 部分。

### 使用卷启动服务

当你启动服务并定义卷时，每个服务容器使用自己的本地卷。如果你使用 `local` 卷驱动，没有容器可以共享这些数据。但是，某些卷驱动确实支持共享存储。

以下示例启动一个带有四个副本的 `nginx` 服务，每个副本使用一个名为 `myvol2` 的本地卷。

```console
$ docker service create -d \
  --replicas=4 \
  --name devtest-service \
  --mount source=myvol2,target=/app \
  nginx:latest
```

使用 `docker service ps devtest-service` 验证服务正在运行：

```console
$ docker service ps devtest-service

ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
4d7oz1j85wwn        devtest-service.1   nginx:latest        moby                Running             Running 14 seconds ago
```

你可以删除服务以停止运行的任务：

```console
$ docker service rm devtest-service
```

删除服务不会删除服务创建的任何卷。卷删除是单独的步骤。

### 使用容器填充卷

如果你启动一个创建新卷的容器，并且容器在要挂载的目录（如 `/app/`）中有文件或目录，Docker 会将目录的内容复制到卷中。然后容器挂载并使用该卷，其他使用该卷的容器也可以访问预先填充的内容。

为了演示这一点，以下示例启动一个 `nginx` 容器，并将新卷 `nginx-vol` 填充为容器的 `/usr/share/nginx/html` 目录的内容。这是 Nginx 存储其默认 HTML 内容的位置。

`--mount` 和 `-v` 示例具有相同的结果。

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

运行上述任一示例后，运行以下命令以清理容器和卷。注意卷删除是单独的步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 使用只读卷

对于某些开发应用，容器需要写入绑定挂载，以便更改传播回 Docker 主机。在其他时候，容器只需要对数据的读取访问权限。多个容器可以挂载同一个卷。你可以同时将单个卷作为 `read-write` 挂载到某些容器，作为 `read-only` 挂载到其他容器。

以下示例更改了前面的示例。它将目录作为只读卷挂载，通过在容器内的挂载点后添加 `ro` 到（默认为空）选项列表中。当存在多个选项时，你可以用逗号分隔它们。

`--mount` 和 `-v` 示例具有相同的结果。

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

使用 `docker inspect nginxtest` 验证 Docker 正确创建了只读挂载。查找 `Mounts` 部分：

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

停止并删除容器，然后删除卷。卷删除是单独的步骤。

```console
$ docker container stop nginxtest

$ docker container rm nginxtest

$ docker volume rm nginx-vol
```

## 挂载卷子目录

当你将卷挂载到容器时，你可以使用 `--mount` 标志的 `volume-subpath` 参数指定要使用的卷的子目录。你指定的子目录必须在将卷挂载到容器之前存在于卷中；如果不存在，挂载会失败。

指定 `volume-subpath` 对于你只想与容器共享卷的特定部分时很有用。例如，假设你有多个容器在运行，你想将每个容器的日志存储在共享卷中。你可以在共享卷中为每个容器创建子目录，并将子目录挂载到容器中。

以下示例创建一个 `logs` 卷，并在卷中初始化子目录 `app1` 和 `app2`。然后启动两个容器，并将 `logs` 卷的子目录之一挂载到每个容器中。此示例假设容器中的进程将其日志写入 `/var/log/app1` 和 `/var/log/app2`。

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

通过这种设置，容器将它们的日志写入 `logs` 卷的独立子目录中。容器无法访问其他容器的日志。

## 在机器之间共享数据

在构建容错应用时，你可能需要配置同一服务的多个副本以访问相同的文件。

![shared storage](images/volumes-shared-storage.webp)

在开发应用时有几种方法可以实现这一点。一种是在应用逻辑中添加逻辑，将文件存储在云对象存储系统（如 Amazon S3）中。另一种是创建带有驱动支持将文件写入外部存储系统（如 NFS 或 Amazon S3）的卷。

卷驱动让你能够将底层存储系统与应用逻辑抽象开来。例如，如果你的服务使用带有 NFS 驱动的卷，你可以更新服务以使用不同的驱动。例如，要将数据存储在云端，而无需更改应用逻辑。

## 使用卷驱动

当你使用 `docker volume create` 创建卷时，或者当你启动使用尚未创建的卷的容器时，