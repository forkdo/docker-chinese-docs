# Rust 语言专项指南


Rust 语言专项指南将教你如何使用 Docker 创建容器化的 Rust 应用。在本指南中，你将学习如何：

- 容器化一个 Rust 应用
- 构建镜像并将新构建的镜像作为容器运行
- 设置卷（volumes）和网络
- 使用 Compose 编排容器
- 使用容器进行开发

完成 Rust 模块后，你应该能够根据本指南提供的示例和说明容器化你自己的 Rust 应用。

从构建你的第一个 Rust 镜像开始。

## Build your Rust image

### 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你也可以使用任意客户端。

### 概述

本指南将带你构建你的第一个 Rust 镜像。一个镜像包含了运行应用所需的一切——代码或二进制文件、运行时、依赖，以及任何其他所需的文件系统对象。

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想在此工作的目录，并运行以下命令来克隆仓库：

```console
$ git clone https://github.com/docker/docker-rust-hello && cd docker-rust-hello
```

### 选择基础镜像

> [!TIP]
>
> [Gordon](/ai/gordon/)，Docker 的 AI 助手，可以为你的项目生成 Docker 相关文件。让 Gordon 创建专为你的应用定制的 Dockerfile、Compose 文件以及 `.dockerignore`。

在编辑你的 Dockerfile 之前，你需要选择一个基础镜像。你可以使用 [Rust Docker 官方镜像](https://hub.docker.com/_/rust)，
或使用 [Docker Hardened Image（DHI）](https://hub.docker.com/hardened-images/catalog/dhi/rust)。

Docker Hardened Images（DHI）是由 Docker 维护的最小、安全、可投入生产的镜像。
它们有助于减少漏洞并简化合规。更多细节请参阅 [Docker Hardened Images](/dhi/)。

**使用 Docker Hardened Images**



Docker Hardened Images（DHI）公开可用，可以直接作为基础镜像使用。
要拉取 Docker Hardened Images，请先用 Docker 进行一次身份验证：

```bash
docker login dhi.io
```

使用 dhi.io 镜像仓库中的 DHI，例如：

```bash
FROM dhi.io/rust:${RUST_VERSION}-alpine3.22-dev AS build
```

以下 Dockerfile 使用 Rust DHI 作为构建基础镜像：

```dockerfile {title=Dockerfile}
# Make sure RUST_VERSION matches the Rust version
ARG RUST_VERSION=1.92
ARG APP_NAME=docker-rust-hello

################################################################################
# Create a stage for building the application.
################################################################################

FROM dhi.io/rust:${RUST_VERSION}-alpine3.22-dev AS build
ARG APP_NAME
WORKDIR /app

# Install host build dependencies.
RUN apk add --no-cache clang lld musl-dev git

# Build the application.
RUN --mount=type=bind,source=src,target=src \
    --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/var/cache/cargo \
    CARGO_HOME=/var/cache/cargo cargo build --locked --release && \
    cp ./target/release/$APP_NAME /bin/server

################################################################################
# Create a new stage for running the application that contains the minimal
# We use dhi.io/static for the final stage because it’s a minimal Docker Hardened Image runtime (basically “just # enough OS to run the binary”), which helps keep the image small and with a lower attack surface compared to a # # full Alpine/Debian runtime.
################################################################################

FROM dhi.io/static:20250419 AS final

# Copy the executable from the "build" stage.
COPY --from=build /bin/server /bin/

# Configure rocket to listen on all interfaces.
ENV ROCKET_ADDRESS=0.0.0.0

# Expose the port that the application listens on.
EXPOSE 8000

# What the container should run when it is started.
CMD ["/bin/server"]

```

**使用 Docker Official Images**



```dockerfile {title=Dockerfile}
# Pin the Rust toolchain version used in the build stage.
ARG RUST_VERSION=1.92

# Name of the compiled binary produced by Cargo (must match Cargo.toml package name).
ARG APP_NAME=docker-rust-hello

################################################################################
# Build stage (DOI Rust image)
# This stage compiles the application.
################################################################################

FROM docker.io/library/rust:${RUST_VERSION}-alpine AS build

# Re-declare args inside the stage if you want to use them here.
ARG APP_NAME

# All build steps happen inside /app.
WORKDIR /app

# Install build dependencies needed to compile Rust crates on Alpine
RUN apk add --no-cache clang lld musl-dev git

# Build the application
RUN --mount=type=bind,source=src,target=src \
    --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/var/cache/cargo \
    CARGO_HOME=/var/cache/cargo cargo build --locked --release && \
    cp ./target/release/$APP_NAME /bin/server

################################################################################
# Runtime stage (DOI Alpine image)
# This stage runs the already-compiled binary with minimal dependencies.
################################################################################

FROM docker.io/library/alpine:3.18 AS final

# Create a non-privileged user (recommended best practice)
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Drop privileges for runtime.
USER appuser

# Copy only the compiled binary from the build stage.
COPY --from=build /bin/server /bin/

# Rocket: listen on all interfaces inside the container.
ENV ROCKET_ADDRESS=0.0.0.0

# Document the port your app listens on.
EXPOSE 8000

# Start the application.
CMD ["/bin/server"]
```



缓存挂载使用单一的 `CARGO_HOME`，以便并发构建通过 Cargo 的缓存锁来协调访问。设置 `CARGO_HOME` 也会改变 Cargo 查找全局配置和凭据的位置。项目级的 `.cargo/config.toml` 文件不受影响。

要构建镜像，只有 Dockerfile 是必需的。在你喜欢的 IDE 或文本编辑器中打开 Dockerfile 查看其内容。要了解更多关于 Dockerfile 的信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md)。

### .dockerignore 文件

[`.dockerignore`](/reference/dockerfile.md#dockerignore-file) 文件指定了你不想复制到镜像中的模式和路径，以保持镜像尽可能小。在你喜欢的 IDE 或文本编辑器中打开 `.dockerignore` 文件查看其内容。

### 构建镜像

既然你已经创建了 Dockerfile，就可以构建镜像了。要构建镜像，请使用 `docker build` 命令。`docker build` 命令从 Dockerfile 和上下文（context）构建 Docker 镜像。构建的上下文是位于指定 PATH 或 URL 中的一组文件。Docker 构建过程可以访问该上下文中任意文件。

`docker build` 命令可选地接受一个 `--tag` 标志。该标签设置镜像的名称以及可选标签，格式为 `name:tag`。如果你不传标签，Docker 会使用 `latest` 作为默认标签。

构建 Docker 镜像。

```console
$ docker build --tag docker-rust-image-dhi .
```

你应该会看到类似如下的输出。

```console
[+] Building 1.4s (13/13) FINISHED                                                                                                                                 docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                                               0.0s
 => => transferring dockerfile: 1.67kB                                                                                                                                             0.0s
 => [internal] load metadata for dhi.io/static:20250419                                                                                                                            1.1s
 => [internal] load metadata for dhi.io/rust:1.92-alpine3.22-dev                                                                                                                   1.2s
 => [auth] static:pull token for dhi.io                                                                                                                                            0.0s
 => [auth] rust:pull token for dhi.io                                                                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                                                                  0.0s
 => => transferring context: 646B                                                                                                                                                  0.0s
 => [build 1/3] FROM dhi.io/rust:1.92-alpine3.22-dev@sha256:49eb72825a9e15fe48f2c4875a63c7e7f52a5b430bb52b8254b91d132aa5bf38                                                       0.0s
 => => resolve dhi.io/rust:1.92-alpine3.22-dev@sha256:49eb72825a9e15fe48f2c4875a63c7e7f52a5b430bb52b8254b91d132aa5bf38                                                             0.0s
 => [final 1/2] FROM dhi.io/static:20250419@sha256:74fc43fa240887b8159970e434244039aab0c6efaaa9cf044004cdc22aa2a34d                                                                0.0s
 => => resolve dhi.io/static:20250419@sha256:74fc43fa240887b8159970e434244039aab0c6efaaa9cf044004cdc22aa2a34d                                                                      0.0s
 => [internal] load build context                                                                                                                                                  0.0s
 => => transferring context: 117B                                                                                                                                                  0.0s
 => CACHED [build 2/3] WORKDIR /build                                                                                                                                              0.0s
 => CACHED [build 3/3] RUN --mount=type=bind,source=src,target=src     --mount=type=bind,source=Cargo.toml,target=Cargo.toml     --mount=type=bind,source=Cargo.lock,target=Cargo  0.0s
 => CACHED [final 2/2] COPY --from=build /build/target/release/docker-rust-hello /server                                                                                           0.0s
 => exporting to image                                                                                                                                                             0.1s
 => => exporting layers                                                                                                                                                            0.0s
 => => exporting manifest sha256:cc937bbdd712ef6e5445501f77e02ef8455ef64c567598786d46b7b21a4d4fa8                                                                                  0.0s
 => => exporting config sha256:077507b483af4b5e1a928e527e4bb3a4aaf0557e1eea81cd39465f564c187669                                                                                    0.0s
 => => exporting attestation manifest sha256:11b60e7608170493da1fdd88c120e2d2957f2a72a22edbc9cfbdd0dd37d21f89                                                                      0.0s
 => => exporting manifest list sha256:99a1b925a8d6ebf80e376b8a1e50cd806ec42d194479a3375e1cd9d2911b4db9                                                                             0.0s
 => => naming to docker.io/library/docker-rust-image-dhi:latest                                                                                                                    0.0s
 => => unpacking to docker.io/library/docker-rust-image-dhi:latest                                                                                                                 0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/yczk0ijw8kc5g20e8nbc8r6lj
```

### 查看本地镜像

要查看你本地机器上的镜像列表，你有两种选择。一种是使用 Docker CLI，另一种是使用 [Docker Desktop](/manuals/desktop/use-desktop/images.md)。既然你已经在终端中工作，就用 CLI 来看看如何列出镜像。

要列出镜像，运行 `docker images` 命令。

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U
```

你应该会看到至少列出一个镜像，包括你刚刚构建的 `docker-rust-image-dhi:latest`。

### 给镜像打标签

如前所述，镜像名称由以斜杠分隔的名称组件（name components）组成。名称组件可以包含小写字母、数字和分隔符。分隔符可以是句点、一个或两个下划线，或者一个或多个短横线。名称组件不能以分隔符开头或结尾。

一个镜像由清单（manifest）和一组层（layers）组成。目前你无需过多关注清单和层，只需知道“标签”指向这些产物的组合。一个镜像可以有多个标签。为你构建的镜像创建一个第二个标签，并查看它的层。

要为你构建的镜像创建一个新标签，运行以下命令。

```console
$ docker tag docker-rust-image-dhi:latest docker-rust-image-dhi:v1.0.0
```

`docker tag` 命令为镜像创建一个新标签，它不会创建一个新镜像。该标签指向同一个镜像，只是引用镜像的另一种方式。

现在，运行 `docker images` 命令查看本地镜像列表。

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U
docker-rust-image-dhi:v1.0.0   99a1b925a8d6       11.6MB         2.45MB    U
```

你可以看到有两个镜像以 `docker-rust-image-dhi` 开头。你知道它们是同一个镜像，因为如果你查看 `IMAGE ID` 列，会看到这两个镜像的值相同。

删除你刚刚创建的标签。为此，请使用 `rmi` 命令。`rmi` 命令代表 remove image（移除镜像）。

```console
$ docker rmi docker-rust-image-dhi:v1.0.0
Untagged: docker-rust-image-dhi:v1.0.0
```

注意 Docker 的响应告诉你，Docker 并没有移除镜像，只是“取消标记（untagged）”了它。你可以通过运行 `docker images` 命令来验证这一点。

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U
```

Docker 移除了标记为 `:v1.0.0` 的镜像，但 `docker-rust-image-dhi:latest` 标签在你的机器上仍然可用。

## Run your Rust image as a container

### 先决条件

你已完成 [Build your Rust image](#build-your-rust-image)，并且已经构建了镜像。

### 概述

容器是一个普通的操系统进程，只是 Docker 隔离了这个进程，使它拥有自己的文件系统、自己的网络，以及独立于主机的隔离进程树。

要在容器内运行镜像，你需要使用 `docker run` 命令。`docker run` 命令需要一个参数，即镜像的名称。

### 运行镜像

使用 `docker run` 运行你在 [Build your Rust image](#build-your-rust-image) 中构建的镜像。

```console
$ docker run docker-rust-image-dhi
```

运行此命令后，你会注意到你没有回到命令提示符。这是因为你的应用是一个服务器，它在循环中运行，等待传入请求，直到你停止容器才将控制权交还给操作系统。

打开一个新终端，然后用 `curl` 命令向服务器发起请求。

```console
$ curl http://localhost:8000
```

你应该会看到类似如下的输出。

```console
curl: (7) Failed to connect to localhost port 8000 after 2236 ms: Couldn't connect to server
```

如你所见，`curl` 命令失败了。这意味着你无法连接到 localhost 的 8000 端口。这是正常的，因为你的容器在隔离环境中运行，其中也包括网络。停止容器，并重新启动，同时将 8000 端口发布到你的本地网络。

要停止容器，按 ctrl-c。这会让你回到终端提示符。

要为你的容器发布端口，你可以在 `docker run` 命令上使用 `--publish` 标志（简写为 `-p`）。`--publish` 命令的格式为 `[主机端口]:[容器端口]`。因此，如果你想将容器内的 8000 端口暴露到容器外的 3001 端口，你需要向 `--publish` 标志传入 `3001:8000`。

你在容器中运行应用时没有指定端口，默认是 8000。如果你想让之前访问 8000 端口的请求生效，可以将主机的 3001 端口映射到容器的 8000 端口：

```console
$ docker run --publish 3001:8000 docker-rust-image-dhi
```

现在，重新运行 curl 命令。记得打开一个新终端。

```console
$ curl http://localhost:3001
```

你应该会看到类似如下的输出。

```console
Hello, Docker!
```

成功！你成功连接到了运行在容器内、监听 8000 端口的应用。切换回运行你容器的终端并停止它。

按 ctrl-c 停止容器。

### 在分离模式下运行

到目前为止一切顺利，但你的示例应用是一个 Web 服务器，你不需要一直连接到容器。Docker 可以在分离模式（detached mode）下，即在后台运行你的容器。为此，你可以使用 `--detach` 或简写为 `-d`。Docker 像之前一样启动你的容器，但这次会“分离”出容器并返回到终端提示符。

```console
$ docker run -d -p 3001:8000 docker-rust-image-dhi
3e4830e7f01304811d97dd3469d47a0c7a916a8b6c28ce0ef19c6f689a521144
```

Docker 在后台启动了你的容器，并在终端上打印了容器 ID。

再次确认你的容器是否正常运行。重新运行 curl 命令。

```console
$ curl http://localhost:3001
```

你应该会看到类似如下的输出。

```console
Hello, Docker!
```

### 列出容器

既然你在后台运行了容器，你怎么知道你的容器是否在运行，或者你的机器上还有什么其他容器在运行？要查看机器上运行的容器列表，可以运行 `docker ps`。这类似于你在 Linux 中使用 ps 命令查看进程列表。

你应该会看到类似如下的输出。

```console
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                23 seconds ago   Up 22 seconds   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   youthful_lamport
```

`docker ps` 命令提供了大量关于你运行中的容器的信息。你可以看到容器 ID、容器内运行的镜像、用于启动容器的命令、创建时间、状态、暴露的端口，以及容器的名称。

你可能想知道容器的名称从何而来。由于你在启动容器时没有为它提供名称，Docker 生成了一个随机名称。你马上会修复这个问题，但首先你需要停止容器。要停止容器，运行 `docker stop` 命令，它的作用就是停止容器。你需要传入容器的名称，也可以使用容器 ID。

```console
$ docker stop youthful_lamport
youthful_lamport
```

现在，重新运行 `docker ps` 命令查看运行中的容器列表。

```console
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### 停止、启动和命名容器

你可以启动、停止并重启 Docker 容器。当你停止一个容器时，它不会被移除，但其状态会变为 stopped（已停止），容器内的进程也会停止。当你在上一个模块运行 `docker ps` 命令时，默认输出只显示运行中的容器。当你传入 `--all` 或简写为 `-a` 时，你会看到机器上的所有容器，无论其启动还是停止状态。

```console
$ docker ps -a
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS                          PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                About a minute ago   Exited (0) 28 seconds ago                                                     youthful_lamport
60009b7eaf40   docker-rust-image-dhi   "/server"                2 minutes ago        Exited (0) About a minute ago                                                 sharp_noyce
152e1d7d9eea   docker-rust-image-dhi   "/server ."              4 minutes ago        Exited (0) 2 minutes ago                                                      magical_bhabha
```

你现在应该会看到列出了几个容器。这些是你启动并停止但尚未移除的容器。

重启你刚刚停止的容器。找到你刚刚停止的容器名称，并在下面的重启命令中替换该容器名称。

```console
$ docker restart youthful_lamport
```

现在使用 `docker ps --all` 命令再次列出所有容器。

```console
$ docker ps --all
CONTAINER ID   IMAGE                   COMMAND                  CREATED             STATUS                         PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                3 minutes ago       Up 7 seconds                   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   youthful_lamport
60009b7eaf40   docker-rust-image-dhi   "/server"                4 minutes ago       Exited (0) 3 minutes ago                                                     sharp_noyce
152e1d7d9eea   docker-rust-image-dhi   "/server ."              5 minutes ago       Exited (0) 4 minutes ago                                                     magical_bhabha
```

注意你刚刚重启的容器是以分离模式启动的。另外，观察容器的状态是“Up X seconds”（已运行 X 秒）。当你重启一个容器时，它会以最初启动时所用的相同标志或命令启动。

现在，停止并移除你的所有容器，然后看看如何修复随机命名的问题。停止你刚刚启动的容器。找到你运行中的容器名称，并在以下命令中替换为你系统上的容器名称。

```console
$ docker stop youthful_lamport
youthful_lamport
```

既然你已经停止了所有容器，就移除它们。当你移除一个容器时，它不再运行，也不再处于停止状态，而是容器内的进程已被停止，并且容器的元数据已被移除。

要移除一个容器，请使用 `docker rm` 命令并传入容器名称。你可以在一条命令中传入多个容器名称。同样，请将以下命令中的容器名称替换为你系统上的容器名称。

```console
$ docker rm youthful_lamport friendly_montalcini tender_bose
youthful_lamport
sharp_noyce
magical_bhabha
```

再次运行 `docker ps --all` 命令，查看 Docker 已移除了所有容器。

现在，是时候解决随机命名的问题了。标准做法是给你的容器命名，原因很简单——这样更容易识别容器中运行的是什么，以及它与哪个应用或服务相关联。

要命名一个容器，请向 `docker run` 命令传入 `--name` 标志。

```console
$ docker run -d -p 3001:8000 --name docker-rust-container docker-rust-image-dhi
1aa5d46418a68705c81782a58456a4ccdb56a309cb5e6bd399478d01eaa5cdda
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                         NAMES
219b2e3c7c38   docker-rust-image-dhi   "/server"                6 seconds ago   Up 5 seconds   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   docker-rust-container
```

现在你可以根据名称识别你的容器了。

## Develop your Rust application

### 先决条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 你已完成 Docker Desktop [学习中心](/manuals/desktop/use-desktop/_index.md) 中的演练，以了解 Docker 概念。
- 你有一个 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但你也可以使用任意客户端。

### 概述

在本节中，你将学习如何在 Docker 中使用卷（volumes）和网络（networking）。你还将使用 Docker 构建镜像，并使用 Docker Compose 让一切变得简单得多。

首先，你将了解在容器中运行数据库，以及如何使用卷和网络来持久化你的数据并让你的应用与数据库通信。然后，你会把一切都整合到一个 Compose 文件中，让你用一条命令搭建并运行本地开发环境。

### 在容器中运行数据库

与其下载 PostgreSQL、安装、配置然后作为服务运行 PostgreSQL 数据库，你可以使用 PostgreSQL 的 Docker 官方镜像，并在容器中运行它。

在容器中运行 PostgreSQL 之前，先创建一个由 Docker 管理的卷来存储你的持久化数据和配置。请使用 Docker 提供的命名卷（named volumes）功能，而不是使用绑定挂载（bind mounts）。

运行以下命令创建你的卷。

```console
$ docker volume create db-data
```

现在创建一个网络，让你的应用和数据库用来相互通信。该网络称为用户自定义桥接网络（user-defined bridge network），它提供了一个不错的 DNS 查找服务，你在创建连接字符串时可以使用它。

```console
$ docker network create postgresnet
```

现在你可以在容器中运行 PostgreSQL，并附加到你之前创建的卷和网络。Docker 从 Hub 拉取镜像并在本地为你运行。
在以下命令中，选项 `--mount` 用于携带卷启动容器。更多信息请参阅 [Docker volumes](/manuals/engine/storage/volumes.md)。

```console
$ docker run --rm -d --mount \
  "type=volume,src=db-data,target=/var/lib/postgresql" \
  -p 5432:5432 \
  --network postgresnet \
  --name db \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=example \
  postgres:18
```

现在，确保你运行的 PostgreSQL 数据库正在运行，并且你可以连接到它。连接到容器内运行的 PostgreSQL 数据库。

```console
$ docker exec -it db psql -U postgres
```

你应该会看到类似如下的输出。

```console
psql (15.3 (Debian 15.3-1.pgdg110+1))
Type "help" for help.

postgres=#
```

在之前的命令中，你通过将 `psql` 命令传给 `db` 容器来登录 PostgreSQL 数据库。按 ctrl-d 退出 PostgreSQL 交互式终端。

### 获取并运行示例应用

对于示例应用，你将使用来自 [Awesome Compose](https://github.com/docker/awesome-compose/tree/master/react-rust-postgres) 的 react-rust-postgres 应用后端的一个变体。

1. 使用以下命令克隆示例应用仓库。

   ```console
   $ git clone https://github.com/docker/docker-rust-postgres
   ```

2. 在克隆的仓库目录中，创建一个 `Dockerfile`。该应用包含一个 `migrations` 目录（除了 `src` 之外）用于初始化数据库，因此 Dockerfile 在构建阶段包含了该目录的绑定挂载。

   ```dockerfile {hl_lines="28"}
   # syntax=docker/dockerfile:1

   # Comments are provided throughout this file to help you get started.
   # If you need more help, visit the Dockerfile reference guide at
   # https://docs.docker.com/reference/dockerfile/

   ################################################################################
   # Create a stage for building the application.

   ARG RUST_VERSION=1.70.0
   ARG APP_NAME=react-rust-postgres
   FROM rust:${RUST_VERSION}-slim-bullseye AS build
   ARG APP_NAME
   WORKDIR /app

   # Build the application.
   # Leverage a cache mount to /var/cache/cargo for downloaded dependencies
   # and a cache mount to /app/target/ for compiled dependencies which will
   # speed up subsequent builds.
   # Leverage a bind mount to the src directory to avoid having to copy the
   # source code into the container. Once built, copy the executable to an
   # output directory before the cache mounted /app/target is unmounted.
   RUN --mount=type=bind,source=src,target=src \
       --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
       --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
       --mount=type=cache,target=/app/target/ \
       --mount=type=cache,target=/var/cache/cargo \
       --mount=type=bind,source=migrations,target=migrations \
       <<EOF
   set -e
   CARGO_HOME=/var/cache/cargo cargo build --locked --release
   cp ./target/release/$APP_NAME /bin/server
   EOF

   ################################################################################
   # Create a new stage for running the application that contains the minimal
   # runtime dependencies for the application. This often uses a different base
   # image from the build stage where the necessary files are copied from the build
   # stage.
   #
   # The example below uses the debian bullseye image as the foundation for    running the app.
   # By specifying the "bullseye-slim" tag, it will also use whatever happens to    be the
   # most recent version of that tag when you build your Dockerfile. If
   # reproducibility is important, consider using a digest
   # (e.g.,    debian@sha256:ac707220fbd7b67fc19b112cee8170b41a9e97f703f588b2cdbbcdcecdd8af57).
   FROM debian:bullseye-slim AS final

   # Create a non-privileged user that the app will run under.
   # See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/   #user
   ARG UID=10001
   RUN adduser \
       --disabled-password \
       --gecos "" \
       --home "/nonexistent" \
       --shell "/sbin/nologin" \
       --no-create-home \
       --uid "${UID}" \
       appuser
   USER appuser

   # Copy the executable from the "build" stage.
   COPY --from=build /bin/server /bin/

   # Expose the port that the application listens on.
   EXPOSE 8000

   # What the container should run when it is started.
   CMD ["/bin/server"]
   ```

3. 在克隆的仓库目录中，运行 `docker build` 来构建镜像。

   ```console
   $ docker build -t rust-backend-image .
   ```

4. 运行 `docker run` 并带上以下选项，使镜像作为容器在与数据库相同的网络上运行。

   ```console
   $ docker run \
     --rm -d \
     --network postgresnet \
     --name docker-develop-rust-container \
     -p 3001:8000 \
     -e PG_DBNAME=example \
     -e PG_HOST=db \
     -e PG_USER=postgres \
     -e PG_PASSWORD=mysecretpassword \
     -e ADDRESS=0.0.0.0:8000 \
     -e RUST_LOG=debug \
     rust-backend-image
   ```

5. 用 curl 访问应用，验证它连接到了数据库。

   ```console
   $ curl http://localhost:3001/users
   ```

   你应该会收到类似如下的响应。

   ```json
   [{ "id": 1, "login": "root" }]
   ```

### 使用 Compose 进行本地开发

在克隆的仓库目录中，创建一个 `compose.yaml` 文件。使用 Compose，你无需输入所有要传给 `docker run` 命令的参数——你可以在文件中声明它们。

你需要在 `compose.yaml` 文件中更新以下项目：

- 取消注释所有的数据库指令。
- 在 server 服务下添加环境变量。

以下是更新后的 `compose.yaml` 文件。

```yaml {hl_lines=["17-23","30-55"]}
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker compose reference guide at
# https://docs.docker.com/reference/compose-file/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8000:8000
    environment:
      - PG_DBNAME=example
      - PG_HOST=db
      - PG_USER=postgres
      - PG_PASSWORD=mysecretpassword
      - ADDRESS=0.0.0.0:8000
      - RUST_LOG=debug
    # The commented out section below is an example of how to define a PostgreSQL
    # database that your application can use. `depends_on` tells Docker Compose to
    # start the database before your application. The `db-data` volume persists the
    # database data between container restarts. The `db-password` secret is used
    # to set the database password. You must create `db/password.txt` and add
    # a password of your choosing to it before running `docker compose up`.
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

注意该文件没有为这两个服务指定网络。当你使用 Compose 时，它会自动创建一个网络并将服务连接到该网络。更多信息请参阅 [Networking in Compose](/manuals/compose/how-tos/networking.md)。

在使用 Compose 运行应用之前，请注意此 Compose 文件指定了一个 `password.txt` 文件来保存数据库密码。你必须创建此文件，因为它未包含在源仓库中。

在克隆的仓库目录中，创建一个名为 `db` 的新目录，并在该目录中创建一个名为 `password.txt` 的文件，其中包含数据库的密码。用你喜欢的 IDE 或文本编辑器，将以下内容添加到 `password.txt` 文件。

```text
mysecretpassword
```

如果你有任何其他容器从前面的章节仍在运行，现在请[停止](#stop-start-and-name-containers)它们。

现在，运行以下 `docker compose up` 命令来启动你的应用。

```console
$ docker compose up --build
```

该命令传入了 `--build` 标志，因此 Docker 会编译你的镜像，然后启动容器。

现在测试你的 API 端点。打开一个新终端，然后用 curl 命令向服务器发起请求：

```console
$ curl http://localhost:8000/users
```

你应该会收到以下响应：

```json
[{ "id": 1, "login": "root" }]
```

### 小结

在本节中，你了解了如何设置 Compose 文件，用一条命令运行你的 Rust 应用和数据库。

相关信息：

- [Docker volumes](/manuals/engine/storage/volumes.md)
- [Compose 概览](/manuals/compose/_index.md)

