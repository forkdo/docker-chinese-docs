---
title: 导出二进制文件
weight: 50
description: 使用 Docker 构建创建并导出可执行二进制文件
keywords: build, buildkit, buildx, guide, tutorial, build arguments, arg
aliases:
  - /build/guide/export/
---

你知道可以用 Docker 将你的应用程序构建为独立二进制文件吗？有时，你不想将应用程序打包并分发为 Docker
镜像。用 Docker 构建你的应用程序，并使用导出器（exporter）将输出保存到磁盘。

`docker build` 的默认输出格式是容器镜像。该镜像会自动加载到你的本地镜像存储，你可以从镜像运行容器，
或将其推送到仓库。在底层，这使用了名为 `docker` 导出器的默认导出器。

要将构建结果导出为文件，你可以使用 `--output` 标志（简称 `-o`）。`--output` 标志让你更改构建的输出格式。

## 从构建中导出二进制文件（Export binaries from a build）

如果你为 `docker build --output` 标志指定一个文件路径，Docker 会在构建结束时将构建容器的内容导出到
主机文件系统上的指定位置。这使用了 `local` [导出器](/manuals/build/exporters/local-tar.md)。

这样做的妙处在于，你可以利用 Docker 强大的隔离和构建特性来创建独立二进制文件。这对于 Go、Rust 以及
其他可以编译为单个二进制的语言非常适用。

以下示例创建一个打印 "Hello, World!" 的简单 Rust 程序，并将二进制文件导出到主机文件系统。

1. 为此示例创建一个新目录，并进入该目录：

   ```console
   $ mkdir hello-world-bin
   $ cd hello-world-bin
   ```

2. 创建包含以下内容的 Dockerfile：

   ```Dockerfile
   # syntax=docker/dockerfile:1
   FROM rust:alpine AS build
   WORKDIR /src
   COPY <<EOT hello.rs
   fn main() {
       println!("Hello World!");
   }
   EOT
   RUN rustc -o /bin/hello hello.rs
   
   FROM scratch
   COPY --from=build /bin/hello /
   ENTRYPOINT ["/hello"]
   ```

   > [!TIP]
   > `COPY <<EOT` 语法是 [here-document](/reference/dockerfile.md#here-documents)（嵌入文档）。
   > 它让你在 Dockerfile 中编写多行字符串。这里用它来在 Dockerfile 中内联创建一个简单的 Rust 程序。

   此 Dockerfile 使用多阶段构建，在第一阶段编译程序，然后将二进制文件复制到第二阶段的 scratch 镜像。
   最终镜像是一个仅包含二进制文件的最小镜像。对于不需要完整操作系统即可运行的程序，使用 `scratch`
   镜像创建最小构建制品是一种常见做法。

3. 构建 Dockerfile 并将二进制文件导出到当前工作目录：

   ```console
   $ docker build --output=. .
   ```

   此命令构建 Dockerfile 并将二进制文件导出到当前工作目录。二进制文件名为 `hello`，创建在当前工作目录中。

## 导出多平台构建（Exporting multi-platform builds）

你使用 `local` 导出器结合 [多平台构建](/manuals/build/building/multi-platform.md) 导出二进制文件。这让你
可以一次性编译多个二进制文件，只要编译器支持目标平台，这些二进制文件就可以在任何架构的任何机器上运行。

继续 [从构建中导出二进制文件](#export-binaries-from-a-build) 一节中的 Dockerfile 示例：

```dockerfile
# syntax=docker/dockerfile:1
FROM rust:alpine AS build
WORKDIR /src
COPY <<EOT hello.rs
fn main() {
    println!("Hello World!");
}
EOT
RUN rustc -o /bin/hello hello.rs

FROM scratch
COPY --from=build /bin/hello /
ENTRYPOINT ["/hello"]
```

你可以使用 `docker build` 命令的 `--platform` 标志为此 Rust 程序构建多个平台。结合 `--output` 标志，构建
会将每个目标的二进制文件导出到指定目录。

例如，要为 `linux/amd64` 和 `linux/arm64` 构建程序：

```console
$ docker build --platform=linux/amd64,linux/arm64 --output=out .
$ tree out/
out/
├── linux_amd64
│   └── hello
└── linux_arm64
    └── hello

3 directories, 2 files
```

## 更多信息（Additional information）

除了 `local` 导出器外，还有其他可用的导出器。要了解有关可用导出器及其使用方法的更多信息，请参阅
[导出器](/manuals/build/exporters/_index.md) 文档。
