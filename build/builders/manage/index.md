# 管理 builders


你可以使用 `docker buildx` 命令，或[使用 Docker Desktop](#manage-builders-with-docker-desktop) 来创建、检查和管builder。

## 创建新的 builder（Create a new builder）

默认 builder 使用 [`docker` 驱动](drivers/docker.md)。
你不能手动创建新的 `docker` builder，但你可以创建使用其他驱动的 builder，例如
[`docker-container` 驱动](drivers/docker-container.md)，
它会在容器中运行 BuildKit 守护进程。

使用
[`docker buildx create`](/reference/cli/docker/buildx/create/)
命令来创建 builder。

```console
$ docker buildx create --name=<builder-name>
```

如果省略 `--driver` 标志，Buildx 默认使用 `docker-container` 驱动。有关可用驱动的更多信息，请参阅 [Build drivers](drivers/_index.md)。

## 列出可用的 builders（List available builders）

使用 `docker buildx ls` 查看系统上可用的 builder 实例，以及它们所使用的驱动。

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

builder 名称旁边的星号（`*`）表示
[选中的 builder](_index.md#selected-builder)。

## 检查一个 builder（Inspect a builder）

要通过 CLI 检查一个 builder，请使用 `docker buildx inspect <name>`。
你只能检查处于活动状态的 builder。你可以向命令添加 `--bootstrap` 标志来启动该 builder。

```console
$ docker buildx inspect --bootstrap my_builder
[+] Building 1.7s (1/1) FINISHED                                                                  
 => [internal] booting buildkit                                                              1.7s
 => => pulling image moby/buildkit:buildx-stable-1                                           1.3s
 => => creating container buildx_buildkit_my_builder0                                        0.4s
Name:          my_builder
Driver:        docker-container
Last Activity: 2023-06-21 18:28:37 +0000 UTC

Nodes:
Name:      my_builder0
Endpoint:  unix:///var/run/docker.sock
Status:    running
Buildkit:  v0.11.6
Platforms: linux/arm64, linux/amd64, linux/amd64/v2, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/mips64le, linux/mips64, linux/arm/v7, linux/arm/v6
```

如果你想查看某个 builder 使用了多少磁盘空间，请使用 `docker buildx du` 命令。默认情况下，该命令会显示所有可用 builder 的总磁盘用量。要查看特定 builder 的用量，请使用 `--builder` 标志。

```console
$ docker buildx du --builder my_builder
ID                                        RECLAIMABLE SIZE        LAST ACCESSED
olkri5gq6zsh8q2819i69aq6l                 true        797.2MB     37 seconds ago
6km4kasxgsywxkm6cxybdumbb*                true        438.5MB     36 seconds ago
qh3wwwda7gx2s5u4hsk0kp4w7                 true        213.8MB     37 seconds ago
54qq1egqem8max3lxq6180cj8                 true        200.2MB     37 seconds ago
ndlp969ku0950bmrw9muolw0c*                true        116.7MB     37 seconds ago
u52rcsnfd1brwc0chwsesb3io*                true        116.7MB     37 seconds ago
rzoeay0s4nmss8ub59z6lwj7d                 true        46.25MB     4 minutes ago
itk1iibhmv7awmidiwbef633q                 true        33.33MB     37 seconds ago
4p78yqnbmgt6xhcxqitdieeln                 true        19.46MB     4 minutes ago
dgkjvv4ay0szmr9bl7ynla7fy*                true        19.24MB     36 seconds ago
tuep198kmcw299qc9e4d1a8q2                 true        8.663MB     4 minutes ago
n1wzhauk9rpmt6ib1es7dktvj                 true        20.7kB      4 minutes ago
0a2xfhinvndki99y69157udlm                 true        16.56kB     37 seconds ago
gf0z1ypz54npfererqfeyhinn                 true        16.38kB     37 seconds ago
nz505f12cnsu739dw2pw0q78c                 true        8.192kB     37 seconds ago
hwpcyq5hdfvioltmkxu7fzwhb*                true        8.192kB     37 seconds ago
acekq89snc7j6im1rjdizvsg1*                true        8.192kB     37 seconds ago
Reclaimable:  2.01GB
Total:        2.01GB
```

## 移除一个 builder（Remove a builder）

使用
[`docker buildx remove`](/reference/cli/docker/buildx/create/)
命令来移除一个 builder。

```console
$ docker buildx rm <builder-name>
```

如果你移除了当前选中的 builder，则会自动选中默认的 `docker` builder。
你不能移除默认 builder。

该 builder 的本地构建缓存也会被移除。

### 移除远程 builders（Removing remote builders）

移除远程 builder 不会影响远程构建缓存。
它也不会停止远程的 BuildKit 守护进程。
它只会移除你与该 builder 的连接。

## 使用 Docker Desktop 管理 builders（Manage builders with Docker Desktop）

如果你已开启
[Docker Desktop 构建视图](/manuals/desktop/use-desktop/builds.md)，
你可以在 [Docker Desktop 设置](/manuals/desktop/settings-and-maintenance/settings.md#builders) 中检查 builder。

