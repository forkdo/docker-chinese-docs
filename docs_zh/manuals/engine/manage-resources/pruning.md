---
description: 使用 prune 命令移除未使用的资源以释放磁盘空间
keywords: 清理, prune, images, volumes, containers, networks, disk, administration, 垃圾回收
title: 清理未使用的 Docker 对象
aliases:
- /engine/admin/pruning/
- /config/pruning/
---

Docker 采用保守的方法来清理未使用的对象（通常称为“垃圾回收”），例如镜像、容器、卷和网络。除非您明确要求 Docker 这样做，否则这些对象通常不会被移除。这可能导致 Docker 占用额外的磁盘空间。针对每种类型的对象，Docker 都提供了一个 `prune` 命令。此外，您可以使用 `docker system prune` 一次清理多种类型的对象。本主题将展示如何使用这些 `prune` 命令。

## 清理镜像

`docker image prune` 命令允许您清理未使用的镜像。默认情况下，`docker image prune` 仅清理 _悬空（dangling）_ 镜像。悬空镜像是指未被标记且未被任何容器引用的镜像。要移除悬空镜像：

```console
$ docker image prune

WARNING! This will remove all dangling images.
Are you sure you want to continue? [y/N] y
```

要移除所有未被现有容器使用的镜像，请使用 `-a` 标志：

```console
$ docker image prune -a

WARNING! This will remove all images without at least one container associated to them.
Are you sure you want to continue? [y/N] y
```

默认情况下，系统会提示您继续。要绕过提示，请使用 `-f` 或 `--force` 标志。

您可以使用 `--filter` 标志配合过滤表达式来限制清理的镜像范围。例如，仅考虑创建时间超过 24 小时的镜像：

```console
$ docker image prune -a --filter "until=24h"
```

其他过滤表达式也可用。请参阅 [`docker image prune` 参考](/reference/cli/docker/image/prune.md) 获取更多示例。

## 清理容器

当您停止一个容器时，除非您在启动时使用了 `--rm` 标志，否则它不会被自动移除。要查看 Docker 主机上的所有容器（包括已停止的容器），请使用 `docker ps -a`。您可能会惊讶于存在的容器数量，尤其是在开发系统上！已停止容器的可写层仍然占用磁盘空间。要清理这些空间，您可以使用 `docker container prune` 命令。

```console
$ docker container prune

WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
```

默认情况下，系统会提示您继续。要绕过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有已停止的容器都会被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除停止时间超过 24 小时的容器：

```console
$ docker container prune --filter "until=24h"
```

其他过滤表达式也可用。请参阅 [`docker container prune` 参考](/reference/cli/docker/container/prune.md) 获取更多示例。

## 清理卷

卷可以被一个或多个容器使用，并在 Docker 主机上占用空间。卷永远不会被自动移除，因为这样做可能会破坏数据。

```console
$ docker volume prune

WARNING! This will remove all volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，系统会提示您继续。要绕过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的卷都会被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除未标记 `keep` 标签的卷：

```console
$ docker volume prune --filter "label!=keep"
```

其他过滤表达式也可用。请参阅 [`docker volume prune` 参考](/reference/cli/docker/volume/prune.md) 获取更多示例。

## 清理网络

Docker 网络不会占用太多磁盘空间，但它们确实会创建 `iptables` 规则、桥接网络设备和路由表条目。要清理这些东西，您可以使用 `docker network prune` 来清理未被任何容器使用的网络。

```console
$ docker network prune

WARNING! This will remove all networks not used by at least one container.
Are you sure you want to continue? [y/N] y
```

默认情况下，系统会提示您继续。要绕过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的网络都会被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令仅移除创建时间超过 24 小时的网络：

```console
$ docker network prune --filter "until=24h"
```

其他过滤表达式也可用。请参阅 [`docker network prune` 参考](/reference/cli/docker/network/prune.md) 获取更多示例。

## 清理所有内容

`docker system prune` 命令是一个快捷方式，用于清理镜像、容器和网络。默认情况下，卷不会被清理，您必须指定 `--volumes` 标志才能让 `docker system prune` 清理卷。

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache

Are you sure you want to continue? [y/N] y
```

要同时清理卷，请添加 `--volumes` 标志：

```console
$ docker system prune --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all volumes not used by at least one container
        - all dangling images
        - all build cache

Are you sure you want to continue? [y/N] y
```

默认情况下，系统会提示您继续。要绕过提示，请使用 `-f` 或 `--force` 标志。

默认情况下，所有未使用的容器、网络和镜像都会被移除。您可以使用 `--filter` 标志来限制范围。例如，以下命令移除创建时间超过 24 小时的项目：

```console
$ docker system prune --filter "until=24h"
```

其他过滤表达式也可用。请参阅 [`docker system prune` 参考](/reference/cli/docker/system/prune.md) 获取更多示例。