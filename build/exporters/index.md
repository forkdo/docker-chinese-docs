# 导出器概述


导出器将你的构建结果保存为指定的输出类型。你使用 [`--output` CLI 选项](/reference/cli/docker/buildx/build/#output) 来指定要使用的导出器。Buildx 支持以下导出器：

- `image`：将构建结果导出为容器镜像。
- `registry`：将构建结果导出为容器镜像，并将其推送到指定的镜像仓库。
- `local`：将构建的根文件系统导出到本地目录。
- `tar`：将构建的根文件系统打包为本地 tar 包。
- `oci`：将构建结果以 [OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md) 格式导出到本地文件系统。
- `docker`：将构建结果以 [Docker 镜像规范 v1.2.0](https://github.com/moby/moby/blob/v25.0.0/image/spec/v1.2.md) 格式导出到本地文件系统。
- `cacheonly`：不导出构建输出，但运行构建并创建缓存。

## 使用导出器

要指定导出器，请使用以下命令语法：

```console
$ docker buildx build --tag <registry>/<image> \
  --output type=<TYPE> .
```

大多数常见用例不需要你显式指定要使用哪个导出器。只有在你想自定义输出，或者想将其保存到磁盘时，才需要指定导出器。`--load` 和 `--push` 选项允许 Buildx 推断要使用的导出器设置。

例如，如果你将 `--push` 选项与 `--tag` 组合使用，Buildx 会自动使用 `image` 导出器，并将导出器配置为将结果推送到指定的镜像仓库。

要充分利用 BuildKit 所提供的各种导出器的全部灵活性，你可以使用 `--output` 标志来配置导出器选项。

## 使用场景

每种导出器类型都针对不同的用例而设计。以下各节描述了一些常见场景，以及如何使用导出器生成你所需的输出。

### 加载到镜像存储

Buildx 常用于构建可以加载到镜像存储中的容器镜像。这就是 `docker` 导出器的用武之地。以下示例展示了如何使用 `docker` 导出器构建镜像，并使用 `--output` 选项将该镜像加载到本地镜像存储：

```console
$ docker buildx build \
  --output type=docker,name=<registry>/<image> .
```

如果你提供 `--tag` 和 `--load` 选项，Buildx CLI 会自动使用 `docker` 导出器并将其加载到镜像存储：

```console
$ docker buildx build --tag <registry>/<image> --load .
```

使用 `docker` 驱动构建的镜像会自动加载到本地镜像存储。

加载到镜像存储的镜像在构建完成后立即可供 `docker run` 使用，并且当你运行 `docker images` 命令时，你会在镜像列表中看到它们。

### 推送到镜像仓库

要将构建好的镜像推送到容器镜像仓库，你可以使用 `registry` 或 `image` 导出器。

当你将 `--push` 选项传递给 Buildx CLI 时，你指示 BuildKit 将构建好的镜像推送到指定的镜像仓库：

```console
$ docker buildx build --tag <registry>/<image> --push .
```

在底层，这使用了 `image` 导出器，并设置了 `push` 参数。它与使用 `--output` 选项的以下长格式命令相同：

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true .
```

你也可以使用 `registry` 导出器，它的作用相同：

```console
$ docker buildx build \
  --output type=registry,name=<registry>/<image> .
```

### 将镜像布局导出到文件

你可以使用 `oci` 或 `docker` 导出器将构建结果保存到本地文件系统上的镜像布局。这两个导出器都会生成一个包含相应镜像布局的 tar 归档文件。`dest` 参数定义了 tar 包的目标输出路径。

```console
$ docker buildx build --output type=oci,dest=./image.tar .
[+] Building 0.8s (7/7) FINISHED
 ...
 => exporting to oci image format                                                                     0.0s
 => exporting layers                                                                                  0.0s
 => exporting manifest sha256:c1ef01a0a0ef94a7064d5cbce408075730410060e253ff8525d1e5f7e27bc900        0.0s
 => exporting config sha256:eadab326c1866dd247efb52cb715ba742bd0f05b6a205439f107cf91b3abc853          0.0s
 => sending tarball                                                                                   0.0s
$ mkdir -p out && tar -C out -xf ./image.tar
$ tree out
out
├── blobs
│   └── sha256
│       ├── 9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e
│       ├── c78795f3c329dbbbfb14d0d32288dea25c3cd12f31bd0213be694332a70c7f13
│       ├── d1cf38078fa218d15715e2afcf71588ee482352d697532cf316626164699a0e2
│       ├── e84fa1df52d2abdfac52165755d5d1c7621d74eda8e12881f6b0d38a36e01775
│       └── fe9e23793a27fe30374308988283d40047628c73f91f577432a0d05ab0160de7
├── index.json
├── manifest.json
└── oci-layout
```

### 导出文件系统

如果你不想从构建结果构建镜像，而是想导出所构建的文件系统，可以使用 `local` 和 `tar` 导出器。

`local` 导出器将文件系统解包到指定位置的目录结构中。`tar` 导出器创建一个 tar 归档文件。

```console
$ docker buildx build --output type=local,dest=<path/to/output> .
```

`local` 导出器在 [多阶段构建](../building/multi-stage.md) 中很有用，因为它允许你仅导出最少量的构建制品，例如自包含的二进制文件。

### 仅缓存导出

如果你只想运行构建而不导出任何输出，可以使用 `cacheonly` 导出器。例如，当你想运行一次测试构建时，这会很有用。或者，如果你想先运行构建，并使用后续命令创建导出。`cacheonly` 导出器会创建一个构建缓存，因此任何后续构建都是即时的。

```console
$ docker buildx build --output type=cacheonly
```

如果你没有指定导出器，并且没有提供像 `--load` 这样会自动选择适当导出器的简写选项，Buildx 默认使用 `cacheonly` 导出器。除非你使用 `docker` 驱动进行构建，在这种情况下你使用的是 `docker` 导出器。

当使用 `cacheonly` 作为默认导出器时，Buildx 会记录一条警告消息：

```console
$ docker buildx build .
WARNING: No output specified with docker-container driver.
         Build result will only remain in the build cache.
         To push result image into registry use --push or
         to load image into docker use --load
```

## 多个导出器



你可以通过多次指定 `--output` 标志为任何给定的构建使用多个导出器。这需要 **Buildx 和 BuildKit** 均为 0.13.0 或更高版本。

以下示例运行一次构建，使用三个不同的导出器：

- `registry` 导出器，用于将镜像推送到镜像仓库
- `local` 导出器，用于将构建结果提取到本地文件系统
- `--load` 标志（`image` 导出器的简写），用于将结果加载到本地镜像存储

```console
$ docker buildx build \
  --output type=registry,tag=<registry>/<image> \
  --output type=local,dest=<path/to/output> \
  --load .
```

## 配置选项

本节描述导出器可用的一些配置选项。

此处描述的选项至少对两种或更多导出器类型是通用的。此外，不同的导出器类型也支持特定参数。有关适用哪些配置参数的更多信息，请参阅每种导出器的详细页面。

此处描述的通用参数包括：

- [压缩](#compression)
- [OCI 媒体类型](#oci-media-types)

### Compression

当你导出压缩输出时，可以配置要使用的具体压缩算法和级别。虽然默认值提供了开箱即用的良好体验，但你可以调整参数以优化存储与计算成本之间的权衡。更改压缩参数可以减少所需的存储空间并改善镜像下载时间，但会增加构建时间。

要选择压缩算法，可以使用 `compression` 选项。例如，要构建具有 `compression=zstd` 的 `image`：

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,compression=zstd .
```

使用 `compression-level=<value>` 选项与 `compression` 参数一起，为支持该选项的算法选择压缩级别：

- `gzip` 和 `estargz` 为 0-9
- `zstd` 为 0-22

通常，数字越大，生成的文件越小，但压缩所需时间越长。

如果你的请求压缩算法与先前的压缩算法不同，请使用 `force-compression=true` 选项强制重新压缩从先前镜像导入的层。

> [!NOTE]
>
> `gzip` 和 `estargz` 压缩方法使用 [`compress/gzip` 包](https://pkg.go.dev/compress/gzip)，而 `zstd` 使用 [`github.com/klauspost/compress/zstd` 包](https://github.com/klauspost/compress/tree/master/zstd)。

#### zstd 压缩级别

当你指定 `compression=zstd` 时，`compression-level` 参数接受从 0 到 22 的值。BuildKit 将这些值映射到四个内部压缩级别：

| compression-level | 内部级别   | 近似 zstd 级别 | 描述                       |
| ----------------- | ---------- | -------------- | -------------------------- |
| 0-2               | Fastest    | ~1             | 最快压缩，文件更大         |
| 3-6（默认）       | Default    | ~3             | 压缩与速度平衡             |
| 7-8               | Better     | ~7             | 更好的压缩，更慢           |
| 9-22              | Best       | ~11            | 最佳压缩，最慢             |

例如，设置 `compression-level=5` 和 `compression-level=6` 会产生相同的压缩输出，因为两者都映射到 "Default" 内部级别。

### OCI media types

`image`、`registry`、`oci` 和 `docker` 导出器创建容器镜像。这些导出器同时支持 Docker 媒体类型（默认）和 OCI 媒体类型。

要导出设置了 OCI 媒体类型的镜像，请使用 `oci-mediatypes` 属性。

```console
$ docker buildx build \
  --output type=image,name=<registry>/<image>,push=true,oci-mediatypes=true .
```

## 下一步

阅读关于每个导出器的内容，了解它们的工作原理以及如何使用它们：

- [镜像与镜像仓库导出器](image-registry.md)
- [OCI 与 Docker 导出器](oci-docker.md)。
- [本地与 tar 导出器](local-tar.md)

