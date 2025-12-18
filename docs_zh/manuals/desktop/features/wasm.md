---
title: Wasm workloads 
weight: 90
description: 如何使用 Docker Desktop 运行 Wasm 工作负载
keywords: Docker, WebAssembly, wasm, containerd, engine
toc_max: 3
aliases: 
- /desktop/wasm/
params:
  sidebar:
    badge:
      color: blue
      text: Beta
---

{{< summary-bar feature_name="Wasm workloads" >}}

> [!IMPORTANT]
>
> Wasm 工作负载将在未来的 Docker Desktop 版本中被弃用并移除。它不再被积极维护。

WebAssembly (Wasm) 是 Linux 和 Windows 容器的快速、轻量替代方案。借助 Docker Desktop，您现在可以并行运行 Wasm 工作负载和传统容器。

本文档提供有关在 Docker 中与 Linux 容器并行运行 Wasm 应用程序的能力的信息。

> [!TIP]
>
> 在 [Docker Wasm 技术预览博客文章](https://www.docker.com/blog/docker-wasm-technical-preview/) 中了解有关 Wasm 用例和权衡的更多信息。

## 开启 Wasm 工作负载

Wasm 工作负载需要开启 [containerd 镜像存储](containerd.md) 功能。如果您尚未使用 containerd 镜像存储，则预存在的镜像和容器将无法访问。

1. 在 Docker Desktop 中导航到 **Settings**。
2. 在 **General** 选项卡中，勾选 **Use containerd for pulling and storing images**。
3. 转到 **Features in development**，勾选 **Enable Wasm** 选项。
4. 选择 **Apply** 保存设置。
5. 在确认对话框中，选择 **Install** 以安装 Wasm 运行时。

Docker Desktop 将下载并安装以下运行时：
- `io.containerd.slight.v1`
- `io.containerd.spin.v2`
- `io.containerd.wasmedge.v1`
- `io.containerd.wasmtime.v1`
- `io.containerd.lunatic.v1`
- `io.containerd.wws.v1`
- `io.containerd.wasmer.v1`

## 使用示例

### 使用 `docker run` 运行 Wasm 应用程序

以下 `docker run` 命令在您的系统上启动一个 Wasm 容器：

```console
$ docker run \
  --runtime=io.containerd.wasmedge.v1 \
  --platform=wasi/wasm \
  secondstate/rust-example-hello
```

运行此命令后，您可以访问 [http://localhost:8080/](http://localhost:8080/) 查看此示例模块的 "Hello world" 输出。

如果您收到错误消息，请参阅 [故障排除部分](#troubleshooting) 获取帮助。

注意此命令中使用的 `--runtime` 和 `--platform` 标志：

- `--runtime=io.containerd.wasmedge.v1`：通知 Docker 引擎您要使用 Wasm containerd shim 而不是标准 Linux 容器运行时
- `--platform=wasi/wasm`：指定您要使用的镜像的架构。通过利用 Wasm 架构，您不需要为不同的机器架构构建单独的镜像。Wasm 运行时负责将 Wasm 二进制文件转换为机器指令的最后一步。

### 使用 Docker Compose 运行 Wasm 应用程序

可以使用以下 Docker Compose 文件运行相同的应用程序：

```yaml
services:
  app:
    image: secondstate/rust-example-hello
    platform: wasi/wasm
    runtime: io.containerd.wasmedge.v1
```

使用正常的 Docker Compose 命令启动应用程序：

   ```console
   $ docker compose up
   ```

### 使用 Wasm 运行多服务应用程序

网络工作方式与 Linux 容器相同，为您提供将 Wasm 应用程序与其他容器化工作负载（如数据库）结合在同一应用程序堆栈中的灵活性。

在以下示例中，Wasm 应用程序利用运行在容器中的 MariaDB 数据库。

1. 克隆仓库。

   ```console
   $ git clone https://github.com/second-state/microservice-rust-mysql.git
   Cloning into 'microservice-rust-mysql'...
   remote: Enumerating objects: 75, done.
   remote: Counting objects: 100% (75/75), done.
   remote: Compressing objects: 100% (42/42), done.
   remote: Total 75 (delta 29), reused 48 (delta 14), pack-reused 0
   Receiving objects: 100% (75/75), 19.09 KiB | 1.74 MiB/s, done.
   Resolving deltas: 100% (29/29), done.
   ```

2. 导航到克隆的项目并使用 Docker Compose 启动项目。

   ```console
   $ cd microservice-rust-mysql
   $ docker compose up
   [+] Running 0/1
   ⠿ server Warning                                                                                                  0.4s
   [+] Building 4.8s (13/15)
   ...
   microservice-rust-mysql-db-1      | 2022-10-19 19:54:45 0 [Note] mariadbd: ready for connections.
   microservice-rust-mysql-db-1      | Version: '10.9.3-MariaDB-1:10.9.3+maria~ubu2204'  socket: '/run/mysqld/mysqld.sock'  port: 3306  mariadb.org binary distribution
   ```

   如果您从另一个终端窗口运行 `docker image ls`，您可以看到镜像存储中的 Wasm 镜像。

   ```console
   $ docker image ls
   REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
   server       latest    2c798ddecfa1   2 minutes ago   3MB
   ```

   检查镜像显示镜像具有 `wasi/wasm` 平台，这是操作系统和架构的组合：

   ```console
   $ docker image inspect server | grep -A 3 "Architecture"
           "Architecture": "wasm",
           "Os": "wasi",
           "Size": 3001146,
           "VirtualSize": 3001146,
   ```

3. 在浏览器中打开 URL `http://localhost:8090` 并创建一些示例订单。所有这些都与 Wasm 服务器交互。

4. 完成后，通过在启动应用程序的终端中按 `Ctrl+C` 来关闭所有服务。

### 构建和推送 Wasm 模块

1. 创建一个构建您的 Wasm 应用程序的 Dockerfile。

   如何执行此操作因您使用的编程语言而异。

2. 在 `Dockerfile` 的单独阶段中，提取模块并将其设置为 `ENTRYPOINT`。

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM scratch
   COPY --from=build /build/hello_world.wasm /hello_world.wasm
   ENTRYPOINT [ "/hello_world.wasm" ]
   ```

3. 构建并推送指定 `wasi/wasm` 架构的镜像。Buildx 使这变得容易，只需一个命令即可完成。

   ```console
   $ docker buildx build --platform wasi/wasm -t username/hello-world .
   ...
   => exporting to image                                                                             0.0s
   => => exporting layers                                                                            0.0s
   => => exporting manifest sha256:2ca02b5be86607511da8dc688234a5a00ab4d58294ab9f6beaba48ab3ba8de56  0.0s
   => => exporting config sha256:a45b465c3b6760a1a9fd2eda9112bc7e3169c9722bf9e77cf8c20b37295f954b    0.0s
   => => naming to docker.io/username/hello-world:latest                                            0.0s
   => => unpacking to docker.io/username/hello-world:latest                                         0.0s
   $ docker push username/hello-world
   ```

## 故障排除

本节包含如何解决常见问题的说明。

### Unknown runtime specified

如果您尝试在没有 [containerd 镜像存储](./containerd.md) 的情况下运行 Wasm 容器，将显示类似以下的错误：

```text
docker: Error response from daemon: Unknown runtime specified io.containerd.wasmedge.v1.
```

在 Docker Desktop 设置中 [开启 containerd 功能](./containerd.md#enable-the-containerd-image-store) 并重试。

### Failed to start shim: failed to resolve runtime path

如果您使用的是不支持运行 Wasm 工作负载的旧版 Docker Desktop，您将看到类似以下的错误消息：

```text
docker: Error response from daemon: failed to start shim: failed to resolve runtime path: runtime "io.containerd.wasmedge.v1" binary not installed "containerd-shim-wasmedge-v1": file does not exist: unknown.
```

更新您的 Docker Desktop 到最新版本并重试。

## 已知问题

- Docker Compose 在被中断时可能无法干净退出。作为解决方法，通过发送 SIGKILL 信号来清理 `docker-compose` 进程（`killall -9 docker-compose`）。
- 推送至 Docker Hub 可能会给出错误，提示 `server message: insufficient_scope: authorization failed`，即使已通过 Docker Desktop 登录。作为解决方法，在 CLI 中运行 `docker login`