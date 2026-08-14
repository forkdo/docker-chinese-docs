# Builders


builder 是一个 BuildKit 守护进程，你可以用它来运行你的构建。BuildKit 是构建引擎，它求解 Dockerfile 中的构建步骤，以生成容器镜像或其他制品。

你可以创建和管理 builder、检查它们，甚至连接到远程运行的 builder。你通过 Docker CLI 与 builder 交互。

## 默认 builder（Default builder）

Docker Engine 会自动创建一个 builder，作为你构建的默认后端。这个 builder 使用与守护进程捆绑在一起的 BuildKit 库。这个 builder 无需任何配置。

默认 builder 直接绑定到 Docker 守护进程及其
[context](/manuals/engine/manage-resources/contexts.md)。如果你更改了 Docker 上下文，你的 `default` builder 就会指向新的 Docker 上下文。

## 构建驱动（Build drivers）

Buildx 实现了 [build drivers](drivers/_index.md) 的概念，用来指代不同的 builder 配置。守护进程创建的默认 builder 使用 [`docker` 驱动](drivers/docker.md)。

Buildx 支持以下构建驱动：

- `docker`：使用与 Docker 守护进程捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专门的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

## 选中的 builder（Selected builder）

选中的 builder 指的是当你运行构建命令时默认使用的 builder。

当你运行构建，或以某种方式通过 CLI 与 builder 交互时，你可以使用可选的 `--builder` 标志，或 `BUILDX_BUILDER`
[环境变量](../building/variables.md#buildx_builder)
来按名称指定一个 builder。如果你不指定 builder，则会使用选中的 builder。

使用 `docker buildx ls` 命令查看可用的 builder 实例。builder 名称旁边的星号（`*`）表示选中的 builder。

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

### 选择不同的 builder（Select a different builder）

要在 builder 之间切换，请使用 `docker buildx use <name>` 命令。

运行此命令后，你指定的 builder 会在你调用构建时自动被选中。

### `docker build` 与 `docker buildx build` 的区别（Difference between `docker build` and `docker buildx build`）

尽管 `docker build` 是 `docker buildx build` 的别名，但这两个命令之间存在细微差别。使用 Buildx 时，构建客户端与守护进程（BuildKit）是解耦的。这意味着你可以从单个客户端使用多个 builder，甚至是远程的。

`docker build` 命令始终默认使用与 Docker Engine 捆绑在一起的默认 builder，以确保与旧版 Docker CLI 的向后兼容。另一方面，`docker buildx build` 命令会在将你的构建发送给 BuildKit 之前，检查你是否已将不同的 builder 设置为默认 builder。

要将 `docker build` 命令与非默认 builder 一起使用，你必须显式指定 builder：

- 使用 `--builder` 标志：

  ```console
  $ docker build --builder my_builder .
  ```

- 或者使用 `BUILDX_BUILDER` 环境变量：

  ```console
  $ BUILDX_BUILDER=my_builder docker build .
  ```

<!-- vale Docker.We = NO -->

一般来说，我们建议你在使用自定义 builder 时使用 `docker buildx build` 命令。这样可以确保你[选中的 builder](#selected-builder)配置被正确解读。

<!-- vale Docker.We = YES -->

## 补充信息（Additional information）

- 有关如何与 builder 交互并管理它们，请参阅 [Manage builders](./manage.md)
- 要了解不同类型的 builder，请参阅 [Build drivers](drivers/_index.md)

