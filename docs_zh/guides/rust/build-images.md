---
title: 构建您的 Rust 镜像
linkTitle: 构建镜像
weight: 5
keywords: rust, build, images, dockerfile
description: 了解如何构建您的第一个 Rust Docker 镜像
aliases:
- /language/rust/build-images/
- /guides/language/rust/build-images/
---

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您拥有 [git 客户端](https://git-scm.com/downloads)。本节中的示例使用基于命令行的 git 客户端，但您可以使用任何客户端。

## 概述

本指南将引导您完成构建您的第一个 Rust 镜像。镜像包含运行应用程序所需的一切——代码或二进制文件、运行时、依赖项以及所需的任何其他文件系统对象。

## 获取示例应用程序

克隆示例应用程序以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/docker/docker-rust-hello && cd docker-rust-hello
```

## 为 Rust 创建 Dockerfile

现在您有了一个应用程序，可以使用 `docker init` 为其创建 Dockerfile。在 `docker-rust-hello` 目录中，运行 `docker init` 命令。`docker init` 提供了一些默认配置，但您需要回答一些关于您的应用程序的问题。参考以下示例来回答 `docker init` 的提示，并对您的提示使用相同的答案。

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Rust
? What version of Rust do you want to use? 1.70.0
? What port does your server listen on? 8000
```

现在，您的 `docker-rust-hello` 目录中应该有以下新文件：

- Dockerfile
- .dockerignore
- compose.yaml
- README.Docker.md

对于构建镜像，只有 Dockerfile 是必需的。在您喜欢的 IDE 或文本编辑器中打开 Dockerfile，查看其内容。要了解更多关于 Dockerfile 的信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md)。

## .dockerignore 文件

当您运行 `docker init` 时，它还会创建一个 [`.dockerignore`](/reference/dockerfile.md#dockerignore-file) 文件。使用 `.dockerignore` 文件指定您不希望复制到镜像中的模式和路径，以尽可能保持镜像最小。在您喜欢的 IDE 或文本编辑器中打开 `.dockerignore` 文件，查看其中已有的内容。

## 构建镜像

现在您已经创建了 Dockerfile，可以构建镜像了。为此，请使用 `docker build` 命令。`docker build` 命令根据 Dockerfile 和上下文构建 Docker 镜像。构建的上下文是位于指定路径或 URL 中的一组文件。Docker 构建过程可以访问此上下文中的任何文件。

构建命令可选择性地接受 `--tag` 标志。该标签设置镜像的名称以及可选的标签，格式为 `name:tag`。如果您不传递标签，Docker 将使用 "latest" 作为其默认标签。

构建 Docker 镜像。

```console
$ docker build --tag docker-rust-image .
```

您应该会看到类似以下的输出。

```console
[+] Building 62.6s (14/14) FINISHED
 => [internal] load .dockerignore                                                                                                    0.1s
 => => transferring context: 2B                                                                                                      0.0s
 => [internal] load build definition from Dockerfile                                                                                 0.1s
 => => transferring dockerfile: 2.70kB                                                                                               0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                           2.3s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14      0.0s
 => [internal] load metadata for docker.io/library/debian:bullseye-slim                                                              1.9s
 => [internal] load metadata for docker.io/library/rust:1.70.0-slim-bullseye                                                         1.7s
 => [build 1/3] FROM docker.io/library/rust:1.70.0-slim-bullseye@sha256:585eeddab1ec712dade54381e115f676bba239b1c79198832ddda397c1f  0.0s
 => [internal] load build context                                                                                                    0.0s
 => => transferring context: 35.29kB                                                                                                 0.0s
 => [final 1/3] FROM docker.io/library/debian:bullseye-slim@sha256:7606bef5684b393434f06a50a3d1a09808fee5a0240d37da5d181b1b121e7637  0.0s
 => CACHED [build 2/3] WORKDIR /app                                                                                                  0.0s
 => [build 3/3] RUN --mount=type=bind,source=src,target=src     --mount=type=bind,source=Cargo.toml,target=Cargo.toml     --mount=  57.7s
 => CACHED [final 2/3] RUN adduser     --disabled-password     --gecos ""     --home "/nonexistent"     --shell "/sbin/nologin"      0.0s
 => CACHED [final 3/3] COPY --from=build /bin/server /bin/                                                                           0.0s
 => exporting to image                                                                                                               0.0s
 => => exporting layers                                                                                                              0.0s
 => => writing image sha256:f1aa4a9f58d2ecf73b0c2b7f28a6646d9849b32c3921e42adc3ab75e12a3de14                                         0.0s
 => => naming to docker.io/library/docker-rust-image
```

## 查看本地镜像

要查看本地机器上的镜像列表，您有两个选择。一个是使用 Docker CLI，另一个是使用 [Docker Desktop](/manuals/desktop/use-desktop/images.md)。由于您已经在终端中工作，我们来看一下如何使用 CLI 列出镜像。

要列出镜像，请运行 `docker images` 命令。

```console
$ docker images
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-rust-image         latest            8cae92a8fbd6   3 minutes ago   123MB
```

您应该会看到至少列出一个镜像，包括您刚刚构建的 `docker-rust-image:latest`。

## 标记镜像

如前所述，镜像名称由斜杠分隔的名称组件组成。名称组件可以包含小写字母、数字和分隔符。分隔符可以包括句点、一个或两个下划线，或一个或多个破折号。名称组件不能以分隔符开头或结尾。

镜像由清单和层列表组成。此时不必太担心清单和层，除了“标签”指向这些工件的组合。您可以为一个镜像设置多个标签。为您构建的镜像创建第二个标签，并查看其层。

要为您构建的镜像创建新标签，请运行以下命令。

```console
$ docker tag docker-rust-image:latest docker-rust-image:v1.0.0
```

`docker tag` 命令为镜像创建新标签。它不会创建新镜像。该标签指向同一个镜像，只是引用镜像的另一种方式。

现在，运行 `docker images` 命令查看本地镜像列表。

```console
$ docker images
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-rust-image         latest            8cae92a8fbd6   4 minutes ago   123MB
docker-rust-image         v1.0.0            8cae92a8fbd6   4 minutes ago   123MB
rust                      latest            be5d294735c6   4 minutes ago   113MB
```

您可以看到两个以 `docker-rust-image` 开头的镜像。您知道它们是同一个镜像，因为如果您查看 `IMAGE ID` 列，您会看到两个镜像的值是相同的。

删除您刚刚创建的标签。为此，请使用 `rmi` 命令。`rmi` 命令代表移除镜像 (remove image)。

```console
$ docker rmi docker-rust-image:v1.0.0
Untagged: docker-rust-image:v1.0.0
```

请注意，Docker 的响应告诉您 Docker 没有删除镜像，只是“取消标记”了它。您可以通过运行 `docker images` 命令来检查这一点。

```console
$ docker images
REPOSITORY               TAG               IMAGE ID       CREATED         SIZE
docker-rust-image        latest            8cae92a8fbd6   6 minutes ago   123MB
rust                     latest            be5d294735c6   6 minutes ago   113MB
```

Docker 移除了标记为 `:v1.0.0` 的镜像，但 `docker-rust-image:latest` 标签在您的机器上仍然可用。

## 总结

本节展示了如何使用 `docker init` 为 Rust 应用程序创建 Dockerfile 和 .dockerignore 文件。然后向您展示了如何构建镜像。最后，还展示了如何标记镜像和列出所有镜像。

相关信息：

- [Dockerfile 参考](/reference/dockerfile.md)
- [.dockerignore 文件](/reference/dockerfile.md#dockerignore-file)
- [docker init CLI 参考](/reference/cli/docker/init.md)
- [docker build CLI 参考](/reference/cli/docker/buildx/build.md)

## 下一步

在下一节中，了解如何将镜像作为容器运行。