---
title: 替代容器运行时
description: |
  Docker Engine 默认使用 runc 作为容器运行时，但您可以通过 CLI 或配置守护进程来指定替代运行时。
keywords: engine, runtime, containerd, runtime v2, shim
aliases:
  - /engine/alternative-runtimes/
---

Docker Engine 使用 containerd 管理容器生命周期，包括创建、启动和停止容器。默认情况下，containerd 使用 runc 作为其容器运行时。

## 可以使用哪些运行时？

您可以使用任何实现 containerd [shim API](https://github.com/containerd/containerd/blob/main/core/runtime/v2/README.md) 的运行时。此类运行时附带 containerd shim，无需任何额外配置即可使用。请参阅 [使用 containerd shim](#use-containerd-shims)。

实现自身 containerd shim 的运行时示例包括：

- [Wasmtime](https://wasmtime.dev/)
- [gVisor](https://github.com/google/gvisor)
- [Kata Containers](https://katacontainers.io/)

您也可以使用设计为 runc 直接替代品的运行时。此类运行时依赖 runc containerd shim 来调用运行时二进制文件。您必须在守护进程配置中手动注册此类运行时。

[youki](https://github.com/youki-dev/youki) 是一个可以作为 runc 直接替代品运行的运行时示例。请参考 [youki 示例](#youki) 了解设置方法。

## 使用 containerd shim

containerd shim 允许您使用替代运行时，而无需更改 Docker 守护进程的配置。要使用 containerd shim，请在运行 Docker 守护进程的系统上，将 shim 二进制文件安装到 `PATH` 环境变量包含的目录中。

要将 shim 与 `docker run` 一起使用，请将运行时的完全限定名称指定为 `--runtime` 标志的值：

```console
$ docker run --runtime io.containerd.kata.v2 hello-world
```

### 在不安装到 PATH 的情况下使用 containerd shim

您可以在不将其安装到 `PATH` 的情况下使用 shim，在这种情况下，您需要在守护进程配置中注册 shim，如下所示：

```json
{
  "runtimes": {
    "foo": {
      "runtimeType": "/path/to/containerd-shim-foobar-v1"
    }
  }
}
```

要使用 shim，请指定您为其分配的名称：

```console
$ docker run --runtime foo hello-world
```

### 配置 shim

如果您需要为 containerd shim 传递额外的配置，可以在守护进程配置文件中使用 `runtimes` 选项。

1. 编辑守护进程配置文件，为您要配置的 shim 添加一个 `runtimes` 条目。

   - 在 `runtimeType` 键中指定运行时的完全限定名称
   - 在 `options` 键下添加您的运行时配置

   ```json
   {
     "runtimes": {
       "gvisor": {
         "runtimeType": "io.containerd.runsc.v1",
         "options": {
           "TypeUrl": "io.containerd.runsc.v1.options",
           "ConfigPath": "/etc/containerd/runsc.toml"
         }
       }
     }
   }
   ```

2. 重新加载守护进程的配置。

   ```console
   # systemctl reload docker
   ```

3. 使用 `docker run` 的 `--runtime` 标志使用自定义运行时。

   ```console
   $ docker run --runtime gvisor hello-world
   ```

有关 containerd shim 配置选项的更多信息，请参阅 [配置 containerd shim](/reference/cli/dockerd.md#configure-containerd-shims)。

## 示例

以下示例展示了如何设置和使用 Docker Engine 的替代容器运行时。

- [youki](#youki)
- [Wasmtime](#wasmtime)

### youki

youki 是一个用 Rust 编写的容器运行时。youki 声称比 runc 更快且内存使用更少，使其成为资源受限环境的理想选择。

youki 作为 runc 的直接替代品运行，这意味着它依赖 runc shim 来调用运行时二进制文件。当您注册充当 runc 替代品的运行时，您需要配置运行时可执行文件的路径，以及一组可选的运行时参数。有关更多信息，请参阅 [配置 runc 直接替代品](/reference/cli/dockerd.md#configure-runc-drop-in-replacements)。

要将 youki 添加为容器运行时：

1. 安装 youki 及其依赖项。

   有关说明，请参阅 [官方设置指南](https://youki-dev.github.io/youki/user/basic_setup.html)。

2. 通过编辑 Docker 守护进程配置文件（默认位于 `/etc/docker/daemon.json`）将 youki 注册为 Docker 的运行时。

   `path` 键应指定您安装 youki 的路径。

   ```console
   # cat > /etc/docker/daemon.json <<EOF
   {
     "runtimes": {
       "youki": {
         "path": "/usr/local/bin/youki"
       }
     }
   }
   EOF
   ```

3. 重新加载守护进程的配置。

   ```console
   # systemctl reload docker
   ```

现在您可以运行使用 youki 作为运行时的容器。

```console
$ docker run --rm --runtime youki hello-world
```

### Wasmtime

{{< summary-bar feature_name="Wasmtime" >}}

Wasmtime 是一个 [Bytecode Alliance](https://bytecodealliance.org/) 项目，也是一个 Wasm 运行时，可让您运行 Wasm 容器。使用 Docker 运行 Wasm 容器可提供两层安全性。您将获得容器隔离的所有好处，以及 Wasm 运行时环境提供的额外沙箱保护。

要将 Wasmtime 添加为容器运行时，请按照以下步骤操作：

1. 在守护进程配置文件中开启 [containerd 镜像存储](/manuals/engine/storage/containerd.md) 功能。

   ```json
   {
     "features": {
       "containerd-snapshotter": true
     }
   }
   ```

2. 重启 Docker 守护进程。

   ```console
   # systemctl restart docker
   ```

3. 将 Wasmtime containerd shim 安装到 `PATH` 环境变量包含的目录中。

   以下命令使用 Dockerfile 从源代码构建 Wasmtime 二进制文件，并将其导出到 `./containerd-shim-wasmtime-v1`。

   ```console
   $ docker build --output . - <<EOF
   FROM rust:latest as build
   RUN cargo install \
       --git https://github.com/containerd/runwasi.git \
       --bin containerd-shim-wasmtime-v1 \
       --root /out \
       containerd-shim-wasmtime
   FROM scratch
   COPY --from=build /out/bin /
   EOF
   ```

   将二进制文件放入 `PATH` 环境变量包含的目录中。

   ```console
   $ mv ./containerd-shim-wasmtime-v1 /usr/local/bin
   ```

现在您可以运行使用 Wasmtime 作为运行时的容器。

```console
$ docker run --rm \
 --runtime io.containerd.wasmtime.v1 \
 --platform wasi/wasm32 \
 michaelirwin244/wasm-example
```

## 相关信息

- 要了解有关容器运行时配置选项的更多信息，请参阅 [配置容器运行时](/reference/cli/dockerd.md#configure-container-runtimes)。
- 您可以配置守护进程默认使用的运行时。请参考 [配置默认容器运行时](/reference/cli/dockerd.md#configure-the-default-container-runtime)。