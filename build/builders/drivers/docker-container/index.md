# Docker 容器驱动


Docker 容器驱动允许在一个专用的 Docker 容器中创建受管理且可自定义的 BuildKit 环境。

与默认 Docker 驱动相比，使用 Docker 容器驱动有几个优势。例如：

- 指定要使用的自定义 BuildKit 版本。
- 构建多架构镜像，参见 [QEMU](#qemu)
- 用于[缓存导入和导出](/manuals/build/cache/backends/_index.md)的高级选项

## 概要（Synopsis）

运行以下命令来创建一个名为 `container`、使用 Docker 容器驱动的新 builder：

```console
$ docker buildx create \
  --name container \
  --driver=docker-container \
  --driver-opt=[key=value,...]
container
```

下表描述了你可以传递给 `--driver-opt` 的可用驱动专属选项：

| Parameter        | Type    | Default          | Description                                                                                                            |
| ---------------- | ------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `image`          | String  |                  | 设置容器要使用的 BuildKit 镜像。                                                                                      |
| `memory`         | String  |                  | 设置容器可以使用的内存量。                                                                                             |
| `memory-swap`    | String  |                  | 设置容器的内存交换（swap）限制。                                                                                      |
| `cpu-quota`      | String  |                  | 对容器施加 CPU CFS 配额。                                                                                             |
| `cpu-period`     | String  |                  | 设置容器的 CPU CFS 调度周期。                                                                                         |
| `cpu-shares`     | String  |                  | 配置容器的 CPU 份额（相对权重）。                                                                                     |
| `cpuset-cpus`    | String  |                  | 限制容器可以使用的 CPU 核心集合。                                                                                     |
| `cpuset-mems`    | String  |                  | 限制容器可以使用的 CPU 内存节点集合。                                                                                 |
| `default-load`   | Boolean | `false`          | 自动将镜像加载到 Docker Engine 镜像存储。                                                                             |
| `network`        | String  |                  | 设置容器的网络模式。                                                                                                   |
| `cgroup-parent`  | String  | `/docker/buildx` | 如果 Docker 使用 "cgroupfs" 驱动，设置容器的 cgroup 父级。                                                            |
| `restart-policy` | String  | `unless-stopped` | 设置容器的 [restart policy](/manuals/engine/containers/start-containers-automatically.md#use-a-restart-policy)。       |
| `env.<key>`      | String  |                  | 在容器中设置环境变量 `key` 为指定的 `value`。                                                                         |
| `provenance-add-gha`   | Boolean |    `true`       | 自动将 GitHub Actions 上下文写入 builder 用于溯源（provenance）。                                                      |

在配置容器的资源限制之前，请先阅读[为容器配置运行时资源约束](/engine/containers/resource_constraints/)。

## 用法（Usage）

当你运行构建时，Buildx 会拉取指定的 `image`（默认是
[`moby/buildkit`](https://hub.docker.com/r/moby/buildkit)）。
当容器启动后，Buildx 将提交给该构建的构建提交到容器化的构建服务器。

```console
$ docker buildx build -t <image> --builder=container .
WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 1.9s done
#1 creating container buildx_buildkit_container0
#1 creating container buildx_buildkit_container0 0.5s done
#1 DONE 2.4s
...
```

## 缓存持久化（Cache persistence）

`docker-container` 驱动支持缓存持久化，因为它将所有 BuildKit 状态及相关的缓存存储到一个专用的 Docker 卷中。

要持久化 `docker-container` 驱动的缓存，即使在使用 `docker buildx rm` 和 `docker buildx create` 重新创建驱动之后，你也可以使用 `--keep-state` 标志销毁该 builder：

例如，创建一个名为 `container` 的 builder，然后在持久化状态的同时移除它：

```console
# setup a builder
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT              STATUS   BUILDKIT PLATFORMS
container *     docker-container
  container0    desktop-linux                running  v0.10.5  linux/amd64
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# remove the builder while persisting state
$ docker buildx rm --keep-state container
$ docker volume ls
DRIVER    VOLUME NAME
local     buildx_buildkit_container0_state

# the newly created driver with the same name will have all the state of the previous one!
$ docker buildx create --name=container --driver=docker-container --use --bootstrap
container
```

## QEMU

`docker-container` 驱动支持使用 [QEMU](https://www.qemu.org/)（用户模式）来构建非原生平台。使用 `--platform` 标志指定要构建的架构。

例如，要为 `amd64` 和 `arm64` 构建一个 Linux 镜像：

```console
$ docker buildx build \
  --builder=container \
  --platform=linux/amd64,linux/arm64 \
  -t <registry>/<image> \
  --push .
```

> [!NOTE]
>
> 使用 QEMU 进行仿真可能比原生构建慢得多，尤其是对于编译和压缩或解压缩这类计算密集型任务。

## 自定义网络（Custom network）

你可以自定义 builder 容器使用的网络。如果你需要为构建使用特定网络，这会很有用。

例如，让我们[创建一个网络](/reference/cli/docker/network/create/) 名为 `foonet`：

```console
$ docker network create foonet
```

现在创建一个将使用该网络的 [`docker-container` builder](/reference/cli/docker/buildx/create/)：

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=foonet"
```

启动并[检查 `mybuilder`](/reference/cli/docker/buildx/inspect/)：

```console
$ docker buildx inspect --bootstrap
```

[检查 builder 容器](/reference/cli/docker/inspect/) 并查看正在使用的网络：

```console
$ docker inspect buildx_buildkit_mybuilder0 --format={{.NetworkSettings.Networks}}
map[foonet:0xc00018c0c0]
```

## 延伸阅读（Further reading）

有关 Docker 容器驱动的更多信息，请参阅
[buildx 参考](/reference/cli/docker/buildx/create/#driver)。

