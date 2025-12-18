---
title: 替代容器运行时
description: |
  Docker Engine 使用 runc 作为默认容器运行时，但你可以通过 CLI 或配置
  守护进程来指定替代运行时
keywords: engine, runtime, containerd, runtime v2, shim
aliases:
  - /engine/alternative-runtimes/
---

Docker Engine 使用 containerd 来管理容器生命周期，包括创建、启动和停止容器。
默认情况下，containerd 使用 runc 作为其容器运行时。

## 可以使用哪些运行时？

你可以使用任何实现了 containerd 
[shim API](https://github.com/containerd/containerd/blob/main/core/runtime/v2/README.md) 的运行时。
此类运行时自带 containerd shim，你可以直接使用而无需额外配置。
请参阅 [使用 containerd shim](#use-containerd-shims)。

实现了自定义 containerd shim 的运行时示例包括：

- [Wasmtime](https://wasmtime.dev/)
- [gVisor](https://github.com/google/gvisor)
- [Kata Containers](https://katacontainers.io/)

你也可以使用设计为 runc 直接替换的运行时。此类
运行时依赖 runc containerd shim 来调用运行时二进制文件。
你必须在守护进程配置中手动注册此类运行时。

[youki](https://github.com/youki-dev/youki)
就是一个可以作为 runc 直接替换的运行时示例。
请参考 [youki 示例](#youki) 了解设置说明。

## 使用 containerd shim

containerd shim 让你可以使用替代运行时，而无需更改 Docker 守护进程的配置。要使用 containerd shim，请将 shim 二进制文件安装到 Docker 守护进程所在系统的 `PATH` 中。

要在 `docker run` 中使用 shim，请在 `--runtime` 标志中指定运行时的完全限定名称：

```console
$ docker run --runtime io.containerd.kata.v2 hello-world
```

### 不安装到 PATH 时使用 containerd shim

你可以在不将 shim 安装到 PATH 的情况下使用它，此时需要在守护进程配置中注册 shim，如下所示：

```json
{
  "runtimes": {
    "foo": {
      "runtimeType": "/path/to/containerd-shim-foobar-v1"
    }
  }
}
```

要使用该 shim，请指定你为其分配的名称：

```console
$ docker run --runtime foo hello-world
```

### 配置 shim

如果你需要为 containerd shim 传递额外的配置，可以使用守护进程配置文件中的 `runtimes` 选项。

1. 编辑守护进程配置文件，添加你要配置的 shim 的 `runtimes` 条目。

   - 在 `runtimeType` 键中指定运行时的完全限定名称
   - 在 `options` 键下添加你的运行时配置

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

3. 使用 `--runtime` 标志为 `docker run` 使用自定义运行时。

   ```console
   $ docker run --runtime gvisor hello-world
   ```

有关 containerd shim 配置选项的更多信息，请参阅
[配置 containerd shim](/reference/cli/dockerd.md#configure-containerd-shims)。

## 示例

以下示例展示了如何在 Docker Engine 中设置和使用替代容器运行时。

- [youki](#youki)
- [Wasmtime](#wasmtime)

### youki

youki 是一个用 Rust 编写的容器运行时。
youki 声称比 runc 更快且使用更少的内存，
使其成为资源受限环境的良好选择。

youki 作为 runc 的直接替换运行，意味着它依赖 runc shim 来调用运行时二进制文件。当你注册充当 runc 替换的运行时时，你配置运行时可执行文件的路径，以及可选的运行时参数集。更多信息请参阅
[配置 runc 直接替换](/reference/cli/dockerd.md#configure-runc-drop-in-replacements)。

要添加 youki 作为容器运行时：

1. 安装 youki 及其依赖项。

   有关说明，请参考
   [官方设置指南](https://youki-dev.github.io/youki/user/basic_setup.html)。

2. 通过编辑 Docker 守护进程配置文件，将 youki 注册为 Docker 的运行时，默认位置为 `/etc/docker/daemon.json`。

   `path` 键应指定你安装 youki 的路径。

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

现在你可以运行使用 youki 作为运行时的容器。

```console
$ docker run --rm --runtime youki hello-world
```

### Wasmtime

{{< summary-bar feature_name="Wasmtime" >}}

Wasmtime 是一个
[Bytecode Alliance](https://bytecodealliance.org/)
项目，是一个让你运行 Wasm 容器的 Wasm 运行时。
使用 Docker 运行 Wasm 容器提供两层安全性。
你将获得容器隔离的所有好处，
以及 Wasm 运行时环境提供的额外沙箱保护。

要添加 Wasmtime 作为容器运行时，请按以下步骤操作：

1. 在守护进程配置文件中启用 [containerd 镜像存储](/manuals/engine/storage/containerd.md) 功能。

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

3. 在 `PATH` 上安装 Wasmtime containerd shim。

   以下 Dockerfile 命令从源代码构建 Wasmtime 二进制文件并将其导出到 `./containerd-shim-wasmtime-v1`。

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

   将二进制文件移动到 `PATH` 中的目录。

   ```console
   $ mv ./containerd-shim-wasmtime-v1 /usr/local/bin
   ```

现在你可以运行使用 Wasmtime 作为运行时的容器。

```console
$ docker run --rm \
 --runtime io.containerd.wasmtime.v1 \
 --platform wasi/wasm32 \
 michaelirwin244/wasm-example
```

## 相关信息

- 要了解有关容器运行时配置选项的更多信息，请参阅 [配置容器运行时](/reference/cli/dockerd.md#configure-container-runtimes)。
- 你可以配置守护进程应使用的默认容器运行时。请参阅 [配置默认容器运行时](/reference/cli/dockerd.md#configure-the-default-container-runtime)。