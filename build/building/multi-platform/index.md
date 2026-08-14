# 多平台构建


多平台构建是指一次构建调用面向多个不同的操作系统或 CPU 架构组合。构建镜像时，这让你能创建可在
多个平台上运行的单个镜像，例如 `linux/amd64`、`linux/arm64` 和 `windows/amd64`。

## 为什么要进行多平台构建？（Why multi-platform builds?）

Docker 通过将应用程序及其依赖打包到容器中，解决了「在我机器上能跑」的问题。这让在同一应用程序在不同
环境（如开发、测试和生产）中运行变得容易。

但容器化本身只解决了部分问题。容器共享主机内核，这意味着容器内运行的代码必须与主机的架构兼容。这就是
你无法在 arm64 主机上运行 `linux/amd64` 容器（除非使用模拟），也无法在 Linux 主机上运行 Windows 容器的
原因。

多平台构建通过将同一应用程序的多个变体打包到单个镜像中来解决此问题。这让你能够在不同类型的硬件上运行
相同的镜像，例如运行 x86-64 的开发机器或云中基于 ARM 的 Amazon EC2 实例，而无需模拟。

### 单平台镜像与多平台镜像的区别（Difference between single-platform and multi-platform images）

多平台镜像的结构与单平台镜像不同。单平台镜像包含指向单一配置和单一层集合的单个清单。多平台镜像包含
清单列表（manifest list），指向多个清单，每个清单指向不同的配置和层集合。

![多平台镜像结构](/build/images/single-vs-multiplatform-image.svg)

当你将多平台镜像推送到仓库时，仓库会存储清单列表和所有单独的清单。当你拉取镜像时，仓库返回清单列表，
Docker 会根据主机的架构自动选择正确的变体。例如，如果你在基于 ARM 的 Raspberry Pi 上运行多平台镜像，
Docker 会选择 `linux/arm64` 变体。如果你在 x86-64 笔记本上运行同一镜像，Docker 会选择 `linux/amd64`
变体（如果你使用的是 Linux 容器）。

## 先决条件（Prerequisites）

多平台镜像需要支持清单列表的镜像存储。Docker Desktop 和 Docker Engine 29.0+ 默认使用
[containerd 镜像存储](/manuals/desktop/features/containerd.md)，它开箱即用地支持多平台镜像。如果你使用的是
这些版本之一，则无需额外设置。

如果你使用的是较旧的 Docker Engine 版本，或从仍使用经典存储驱动的旧版本升级而来，你有两个选择：

- 使用 [守护进程配置文件](/manuals/engine/storage/containerd.md) 启用 containerd 镜像存储。
- 使用 `docker-container` 驱动创建自定义构建器（见下一节）。

### 自定义构建器（Custom builder）

作为使用 containerd 镜像存储的替代方案，你可以创建一个使用 `docker-container` 驱动的自定义构建器。该驱动
支持多平台构建，但结果镜像不会被加载到你的 Docker Engine 镜像存储中。你可以用 `docker build --push` 直接
将它们推送到容器仓库。

```console
$ docker buildx create \
  --name container-builder \
  --driver docker-container \
  --bootstrap --use
```

> [!NOTE]
> 使用 `docker-container` 驱动的构建不会自动加载到你的 Docker Engine 镜像存储。有关更多信息，请参阅
> [构建驱动](/manuals/build/builders/drivers/_index.md)。

如果你使用的是独立的 Docker Engine，并且需要使用模拟来构建多平台镜像，官方 BuildKit 发布版捆绑了 QEMU
用户态模拟器，因此在大多数情况下你无需手动安装 QEMU。如果模拟失败（例如使用未附带捆绑模拟器的第三方
BuildKit 包），请参阅 [手动安装 QEMU](#install-qemu-manually)。

## 构建多平台镜像（Build multi-platform images）

触发构建时，使用 `--platform` 标志定义构建输出的目标平台，例如 `linux/amd64` 和 `linux/arm64`：

```console
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

## 策略（Strategies）

根据你的用例，你可以使用三种不同的策略构建多平台镜像：

1. 使用 [QEMU](#qemu) 模拟
2. 使用具有 [多个原生节点](#multiple-native-nodes) 的构建器
3. 使用多阶段构建进行 [交叉编译](#cross-compilation)

### QEMU

如果你的构建器已支持模拟，使用 QEMU 在模拟下构建多平台镜像是入门最容易的方式。使用模拟无需更改你的
Dockerfile，BuildKit 会自动检测可用于模拟的架构。

> [!NOTE]
>
> 使用 QEMU 的模拟可能比原生构建慢得多，尤其是对于编译、压缩或解压等计算密集型任务。
>
> 如果可能，请改用 [多个原生节点](#multiple-native-nodes) 或 [交叉编译](#cross-compilation)。

Docker Desktop 默认支持在模拟下运行和构建多平台镜像。无需配置，因为构建器使用 Docker Desktop VM 中捆绑的
QEMU。

#### 手动安装 QEMU（Install QEMU manually）

如果 BuildKit 捆绑的 QEMU 模拟器不适用于你的构建（例如使用未携带它们的第三方 BuildKit 包），你可以安装
QEMU 并在主机操作系统上注册可执行文件类型。安装 QEMU 的先决条件是：

- Linux 内核版本 4.8 或更高
- `binfmt-support` 版本 2.1.7 或更高
- QEMU 二进制文件必须是静态编译的，并使用 `fix_binary` 标志注册

使用 [`tonistiigi/binfmt`](https://github.com/tonistiigi/binfmt) 镜像，通过单条命令安装 QEMU 并在主机上
注册可执行文件类型：

```console
$ docker run --privileged --rm tonistiigi/binfmt --install all
```

这会安装 QEMU 二进制文件并用 [`binfmt_misc`](https://en.wikipedia.org/wiki/Binfmt_misc) 注册它们，使 QEMU
能够执行非原生的文件格式进行模拟。

一旦 QEMU 安装完成且可执行文件类型在主机操作系统上注册，它们在容器内就是透明的。你可以通过检查
`/proc/sys/fs/binfmt_misc/qemu-*` 中的标志是否包含 `F` 来验证注册。

### 多个原生节点（Multiple native nodes）

使用多个原生节点能更好地支持 QEMU 无法处理的更复杂情况，并提供更好的性能。

你可以使用 `--append` 标志向构建器添加额外的节点。

以下命令从名为 `node-amd64` 和 `node-arm64` 的 Docker 上下文创建一个多节点构建器。此示例假设你已经添加了
那些上下文。

```console
$ docker buildx create --use --name mybuild node-amd64
mybuild
$ docker buildx create --append --name mybuild node-arm64
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

虽然这种方法相比模拟有优势，但管理多节点构建器会带来搭建和管理构建器集群的一些开销。或者，你可以使用
Docker Build Cloud，这是一项在 Docker 基础设施上提供托管多节点构建器的服务。使用 Docker Build Cloud，你
可以获得原生的多平台 ARM 和 X86 构建器，而无需维护它们的负担。使用云构建器还提供额外的好处，例如共享
构建缓存。

注册 Docker Build Cloud 后，将构建器添加到你的本地环境并开始构建。

```console
$ docker buildx create --driver cloud <ORG>/<BUILDER_NAME>
cloud-<ORG>-<BUILDER_NAME>
$ docker build \
  --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag <IMAGE_NAME> \
  --push .
```

有关更多信息，请参阅 [Docker Build Cloud](/manuals/build-cloud/_index.md)。

### 交叉编译（Cross-compilation）

根据你的项目，如果你使用的编程语言对交叉编译有良好的支持，你可以利用多阶段构建，从构建器的原生架构为
目标平台构建二进制文件。特殊构建参数（如 `BUILDPLATFORM` 和 `TARGETPLATFORM`）会自动在你的 Dockerfile 中
可用。

在以下示例中，`FROM` 指令固定到构建器的原生平台（使用 `--platform=$BUILDPLATFORM` 选项）以防止模拟被
触发。然后在 `RUN` 指令中插入预定义的 `$BUILDPLATFORM` 和 `$TARGETPLATFORM` 构建参数。此处，这些值只是用
`echo` 打印到 stdout，但这说明了如何将它们传递给编译器进行交叉编译。

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
FROM alpine
COPY --from=build /log /log
```

## 示例（Examples）

以下是一些多平台构建的示例：

- [使用模拟的简单多平台构建](#simple-multi-platform-build-using-emulation)
- [使用 Docker Build Cloud 的多平台 Neovim 构建](#multi-platform-neovim-build-using-docker-build-cloud)
- [交叉编译 Go 应用程序](#cross-compiling-a-go-application)

### 使用模拟的简单多平台构建（Simple multi-platform build using emulation）

此示例演示了如何使用 QEMU 模拟构建简单的多平台镜像。该镜像包含一个打印容器架构的单个文件。

先决条件：

- Docker Desktop，或已安装 [QEMU](#install-qemu-manually) 的 Docker Engine

步骤：

1. 创建一个空目录并进入该目录：

   ```console
   $ mkdir multi-platform
   $ cd multi-platform
   ```

2. 创建一个打印容器架构的简单 Dockerfile：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM alpine
   RUN uname -m > /arch
   ```

3. 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t multi-platform .
   ```

4. 运行镜像并打印架构：

   ```console
   $ docker run --rm multi-platform cat /arch
   ```

   - 如果你在 x86-64 机器上运行，你应该看到 `x86_64`。
   - 如果你在 ARM 机器上运行，你应该看到 `aarch64`。

### 使用 Docker Build Cloud 的多平台 Neovim 构建（Multi-platform Neovim build using Docker Build Cloud）

此示例演示了如何使用 Docker Build Cloud 运行多平台构建，以编译并导出
[Neovim](https://github.com/neovim/neovim) 的 `linux/amd64` 和 `linux/arm64` 平台二进制文件。

Docker Build Cloud 提供托管的原生多节点构建器，支持无需模拟的原生多平台构建，使编译等 CPU 密集型任务快得多。

先决条件：

- 你已 [注册 Docker Build Cloud 并创建了构建器](/manuals/build-cloud/setup.md)

步骤：

1. 创建一个空目录并进入该目录：

   ```console
   $ mkdir docker-build-neovim
   $ cd docker-build-neovim
   ```

2. 创建一个构建 Neovim 的 Dockerfile。

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM debian:bookworm AS build
   WORKDIR /work
   RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
       --mount=type=cache,target=/var/lib/apt,sharing=locked \
       apt-get update && apt-get install -y \
       build-essential \
       cmake \
       curl \
       gettext \
       ninja-build \
       unzip
   ADD https://github.com/neovim/neovim.git#stable .
   RUN make CMAKE_BUILD_TYPE=RelWithDebInfo

   FROM scratch
   COPY --from=build /work/build/bin/nvim /
   ```

3. 使用 Docker Build Cloud 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build \
      --builder <cloud-builder> \
      --platform linux/amd64,linux/arm64 \
      --output ./bin .
   ```

   此命令使用云构建器构建镜像，并将二进制文件导出到 `bin` 目录。

4. 验证二进制文件已为两个平台构建。你应该看到 `linux/amd64` 和 `linux/arm64` 的 `nvim` 二进制文件。

   ```console
   $ tree ./bin
   ./bin
   ├── linux_amd64
   │   └── nvim
   └── linux_arm64
       └── nvim

   3 directories, 2 files
   ```

### 交叉编译 Go 应用程序（Cross-compiling a Go application）

此示例演示了如何使用多阶段构建为多个平台交叉编译 Go 应用程序。该应用程序是一个监听 8080 端口并返回容器
架构的简单 HTTP 服务器。此示例使用 Go，但相同原则适用于其他支持交叉编译的编程语言。

Docker 构建的交叉编译通过利用一系列预定义（在 BuildKit 中）的构建参数来工作，这些参数为你提供有关构建器和
构建目标平台的信息。你可以使用这些预定义参数将平台信息传递给编译器。

在 Go 中，你可以使用 `GOOS` 和 `GOARCH` 环境变量指定要构建的目标平台。

先决条件：

- Docker Desktop 或 Docker Engine

步骤：

1. 创建一个空目录并进入该目录：

   ```console
   $ mkdir go-server
   $ cd go-server
   ```

2. 创建一个构建 Go 应用程序的基础 Dockerfile：

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:alpine AS build
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN go build -o server .

   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   此 Dockerfile 还不能通过交叉编译构建多平台。如果你尝试用 `docker build` 构建此 Dockerfile，构建器会尝
   试使用模拟为指定平台构建镜像。

3. 要添加交叉编译支持，更新 Dockerfile 以使用预定义的 `BUILDPLATFORM`、`TARGETOS` 和 `TARGETARCH` 构建
   参数。
   - 使用 `--platform=$BUILDPLATFORM` 选项将 `golang` 镜像固定到构建器的平台。
   - 为 Go 编译阶段添加 `ARG` 指令，使 `TARGETOS` 和 `TARGETARCH` 构建参数可供该阶段的命令使用。
   - 将 `GOOS` 和 `GOARCH` 环境变量设置为 `TARGETOS` 和 `TARGETARCH` 的值。Go 编译器使用这些变量进行交叉
     编译。

   **Updated Dockerfile**



   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM --platform=$BUILDPLATFORM golang:alpine AS build
   ARG TARGETOS
   ARG TARGETARCH
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .

   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   **Old Dockerfile**



   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:alpine AS build
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN go build -o server .

   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   **Diff**



   ```diff
   # syntax=docker/dockerfile:1
   -FROM golang:alpine AS build
   +FROM --platform=$BUILDPLATFORM golang:alpine AS build
   +ARG TARGETOS
   +ARG TARGETARCH
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   -RUN go build -o server .
   +RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .

   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   

4. 为 `linux/amd64` 和 `linux/arm64` 构建镜像：

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t go-server .
   ```

此示例展示了如何使用 Docker 构建为多个平台交叉编译 Go 应用程序。如何进行交叉编译的具体步骤可能因你使用的
编程语言而异。请查阅你所用编程语言的文档，了解有关为不同平台交叉编译的更多信息。

> [!TIP]
> 你可能还想考虑查看 [xx - Dockerfile 交叉编译助手](https://github.com/tonistiigi/xx)。`xx` 是一个包含
> 实用脚本的 Docker 镜像，让使用 Docker 构建进行交叉编译更容易。

