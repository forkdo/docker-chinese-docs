# 优化构建中的缓存使用


在使用 Docker 构建时，如果某条指令及其所依赖的文件自上次构建以来没有变化，那么该层就会从构建缓存中复用。从缓存复用层可以加快构建过程，因为 Docker 不必重新构建该层。

以下是一些你可以用来优化构建缓存并加速构建过程的技术：

- [合理安排层顺序](#order-your-layers)：将 Dockerfile 中的命令按合理顺序排列，有助于避免不必要的缓存失效。
- [保持构建上下文精简](#keep-the-context-small)：上下文是发送给 builder 以处理构建指令的文件和目录集合。尽可能保持上下文精简，可以减少需要发送给 builder 的数据量，并降低缓存失效的可能性。
- [使用绑定挂载](#use-bind-mounts)：绑定挂载让你可以将主机上的文件或目录挂载到构建容器中。使用绑定挂载有助于避免在镜像中产生不必要的层，从而拖慢构建过程。
- [使用缓存挂载](#use-cache-mounts)：缓存挂载让你可以指定在构建期间使用的持久化包缓存。持久化缓存有助于加速构建步骤，尤其是涉及使用包管理器安装包的步骤。拥有持久化的包缓存意味着即使你重新构建某一层，也只需下载新增或变更的包。
- [使用外部缓存](#use-an-external-cache)：外部缓存让你可以将构建缓存存储在远程位置。外部缓存镜像可以在多次构建之间、跨不同环境共享。

## 合理安排层顺序（Order your layers）

将 Dockerfile 中的命令按逻辑顺序排列是一个很好的起点。因为某个变更会导致后续步骤重新构建，所以尽量让开销大的步骤出现在 Dockerfile 的靠前位置。经常变化的步骤应出现在 Dockerfile 的靠后位置，以避免触发尚未变化层的重建。

考虑以下示例。一个从当前目录中的源文件运行 JavaScript 构建的 Dockerfile 片段：

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # Copy over all files in the current directory
RUN npm install   # Install dependencies
RUN npm build     # Run build
```

这个 Dockerfile 相当低效。即使依赖自上次以来没有变化，每次构建 Docker 镜像时，更新任何文件都会导致重新安装所有依赖。

取而代之的是，可以将 `COPY` 命令拆成两步。首先，复制包管理文件（在本例中为 `package.json` 和 `yarn.lock`）。然后，安装依赖。最后，复制经常变更的源代码。

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .    # Copy package management files
RUN npm install                  # Install dependencies
COPY . .                         # Copy over project files
RUN npm build                    # Run build
```

通过在 Dockerfile 的较早层中安装依赖，当项目文件发生变化时就无需重建那些层了。

## 保持上下文精简（Keep the context small）

确保构建上下文不包含不必要文件的最简单方法，是在构建上下文的根目录创建一个 `.dockerignore` 文件。`.dockerignore` 文件的工作方式类似于 `.gitignore` 文件，让你可以从构建上下文中排除文件和目录。

下面是一个排除 `node_modules` 目录以及所有以 `tmp` 开头的文件和目录的 `.dockerignore` 文件示例：

```plaintext {title=".dockerignore"}
node_modules
tmp*
```

`.dockerignore` 文件中指定的忽略规则适用于整个构建上下文，包括子目录。这意味着它是一种相当粗粒度的机制，但它是排除你确定不需要放在构建上下文中的文件和目录（如临时文件、日志文件和构建产物）的好方法。

## 使用绑定挂载（Use bind mounts）

你可能熟悉在使用 `docker run` 或 Docker Compose 运行容器时的绑定挂载。绑定挂载让你可以将主机上的文件或目录挂载到容器中。

```bash
# bind mount using the -v flag
docker run -v $(pwd):/path/in/container image-name
# bind mount using the --mount flag
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

要在构建中使用绑定挂载，你可以在 Dockerfile 中使用 `RUN` 指令的 `--mount` 标志：

```dockerfile
FROM golang:latest
WORKDIR /build
RUN --mount=type=bind,target=. go build -o /app/hello
```

在此示例中，在当前目录被挂载到构建容器中的 `/build` 之前，`go build` 命令会先执行。构建输出被写入 `/app/hello`，它位于挂载点之外。这一区别很重要：构建输出必须写入绑定挂载目标之外，因为该挂载默认是只读的。在 `RUN` 指令执行期间，源代码在构建容器中可用。当指令执行完毕，挂载的文件不会被持久化到最终镜像或构建缓存中。只有 `go build` 命令的输出会保留下来。

Dockerfile 中的 `COPY` 和 `ADD` 指令让你可以将文件从构建上下文复制到构建容器中。使用绑定挂载有利于构建缓存优化，因为你不会向缓存添加不必要的层。如果你的构建上下文偏大，且它仅用于生成制品，那么你最好使用绑定挂载临时挂载生成该制品所需的源代码到构建中。如果你使用 `COPY` 将文件添加到构建容器，BuildKit 会将所有这些文件都包含在缓存中，即使这些文件并未用在最终镜像中。

在使用构建中的绑定挂载时，有几点需要注意：

- 绑定挂载默认是只读的。如果你需要写入挂载的目录，需要指定 `rw` 选项。但是，即使使用 `rw` 选项，这些更改也不会持久化到最终镜像或构建缓存中。文件写入在 `RUN` 指令执行期间有效，并在指令完成后被丢弃。
- 挂载的文件不会被持久化到最终镜像中。只有 `RUN` 指令的输出会持久化到最终镜像。如果你需要将构建上下文中的文件包含到最终镜像中，你需要使用 `COPY` 或 `ADD` 指令。
- 如果目标目录不为空，目标目录的内容会被挂载的文件隐藏。原始内容会在 `RUN` 指令完成后恢复。

  **Example**



例如，给定一个仅包含 `Dockerfile` 的构建上下文：

```plaintext
.
└── Dockerfile
```

以及一个将当前目录挂载到构建容器中的 Dockerfile：

```dockerfile
FROM alpine:latest
WORKDIR /work
RUN touch foo.txt
RUN --mount=type=bind,target=. ls
RUN ls
```

第一个带有绑定挂载的 `ls` 命令显示挂载目录的内容。第二个 `ls` 列出原始构建上下文的内容。

```plaintext {title="Build log"}
#8 [stage-0 3/5] RUN touch foo.txt
#8 DONE 0.1s

#9 [stage-0 4/5] RUN --mount=target=. ls -1
#9 0.040 Dockerfile
#9 DONE 0.0s

#10 [stage-0 5/5] RUN ls -1
#10 0.046 foo.txt
#10 DONE 0.1s
```




## 使用缓存挂载（Use cache mounts）

Docker 中的常规缓存层对应于指令及其所依赖文件的精确匹配。如果指令及其所依赖文件自该层构建以来发生了变化，该层就会失效，构建过程必须重新构建该层。

缓存挂载是一种指定在构建期间使用的持久化缓存位置的方式。缓存在各次构建之间是累积的，因此你可以多次读写缓存。这种持久化缓存意味着即使你需要重新构建某一层，也只需下载新增或变更的包。任何未变化的包都会从缓存挂载中复用。

要在构建中使用缓存挂载，你可以在 Dockerfile 中使用 `RUN` 指令的 `--mount` 标志：

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

在此示例中，`npm install` 命令使用 `/root/.npm` 目录（npm 缓存的默认位置）的缓存挂载。缓存挂载在各次构建之间持久化，因此即使你最终重建了该层，也只需下载新增或变更的包。对缓存的任何更改都会在各次构建之间持久化，并且该缓存在多次构建之间共享。

如何指定缓存挂载取决于你使用的构建工具。如果你不确定如何指定缓存挂载，请参阅你所使用构建工具的文档。以下是一些示例：

**Go**



```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/hello
```

**Apt**



```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc
```

**Python**



```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Ruby**



```dockerfile
RUN --mount=type=cache,target=/root/.gem \
    bundle install
```

**Rust**



```dockerfile
RUN --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/var/cache/cargo \
    CARGO_HOME=/var/cache/cargo cargo build
```

缓存挂载使用单一 `CARGO_HOME`，因此并发构建通过 Cargo 的缓存锁来协调访问。设置 `CARGO_HOME` 也会改变 Cargo 查找全局配置和凭据的位置。项目级别的 `.cargo/config.toml` 文件不受影响。

**.NET**



```dockerfile
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore
```

**PHP**

  

```dockerfile
RUN --mount=type=cache,target=/tmp/cache \
    composer install
```



阅读你所使用构建工具的文档非常重要，以确保你使用了正确的缓存挂载选项。包管理器对如何使用缓存有不同的要求，使用错误的选项可能导致意外行为。例如，Apt 需要对其数据拥有独占访问权，因此缓存使用 `sharing=locked` 选项，以确保使用同一缓存挂载的并行构建彼此等待，而不会同时访问相同的缓存文件。

## 使用外部缓存（Use an external cache）

构建的默认缓存存储是当前所用 builder（BuildKit 实例）的内部存储。每个 builder 使用自己的缓存存储。当你在不同 builder 之间切换时，缓存不会在它们之间共享。使用外部缓存让你可以定义一个远程位置来推送和拉取缓存数据。

外部缓存对 CI/CD 流水线尤其有用，因为其中的 builder 往往是临时的，且构建时间宝贵。在多次构建之间复用缓存可以大幅加快构建过程并降低成本。你甚至可以在本地开发环境中利用相同的缓存。

要使用外部缓存，你需要通过 `docker buildx build` 命令指定 `--cache-to` 和 `--cache-from` 选项。

- `--cache-to` 将构建缓存导出到指定位置。
- `--cache-from` 指定构建要使用的远程缓存。

以下示例展示了如何使用 `docker/build-push-action` 设置 GitHub Actions 工作流，并将构建缓存层推送到 OCI 注册表镜像：

```yaml {title=".github/workflows/ci.yml"}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

此设置告诉 BuildKit 在 `user/app:buildcache` 镜像中查找缓存。构建完成后，新的构建缓存会被推送到同一个镜像，覆盖旧的缓存。

这个缓存也可以在本地使用。要在本地构建中拉取缓存，你可以使用 `docker buildx build` 命令的 `--cache-from` 选项：

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## 总结（Summary）

优化构建中的缓存使用可以显著加快构建过程。保持构建上下文精简、使用绑定挂载、缓存挂载和外部缓存，都是你可以用来充分利用构建缓存并加速构建过程的技术。

有关本指南中所讨论概念的更多信息，请参阅：

- [.dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-files)
- [缓存失效](/manuals/build/cache/invalidation.md)
- [缓存挂载](/reference/dockerfile.md#run---mounttypecache)
- [缓存后端类型](/manuals/build/cache/backends/_index.md)
- [构建最佳实践](/manuals/build/building/best-practices.md)

