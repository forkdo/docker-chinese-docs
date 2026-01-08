---
title: 优化云端构建
linkTitle: 优化
weight: 40
description: 远程构建与本地构建不同。本文介绍如何针对远程构建器进行优化。
keywords: build, cloud build, optimize, remote, local, cloud
aliases:
- /build/cloud/optimization/
---

Docker Build Cloud 在远程运行你的构建，而不是在你调用构建的机器上。
这意味着客户端和构建器之间的文件传输是通过网络进行的。

通过网络传输文件比本地传输具有更高的延迟和更低的带宽。
Docker Build Cloud 具有以下几个特性来缓解此问题：

- 它使用附加的存储卷作为构建缓存，这使得缓存读写非常快。
- 将构建结果加载回客户端时，只会拉取与之前构建相比发生变更的层。

尽管有这些优化，对于大型项目或网络连接较慢的情况，远程构建仍然可能导致上下文传输和镜像加载缓慢。
以下是一些你可以用来优化构建以提高传输效率的方法：

- [Dockerignore 文件](#dockerignore-files)
- [精简基础镜像](#slim-base-images)
- [多阶段构建](#multi-stage-builds)
- [在构建中获取远程文件](#fetch-remote-files-in-build)
- [多线程工具](#multi-threaded-tools)

有关如何优化构建的更多信息，请参阅
[构建最佳实践](/manuals/build/building/best-practices.md)。

### Dockerignore 文件

通过使用 [`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)，
你可以明确指定哪些本地文件不希望包含在构建上下文中。
被你在忽略文件中指定的 glob 模式匹配到的文件不会被传输到远程构建器。

一些你可能想要添加到 `.dockerignore` 文件中的示例如下：

- `.git` — 跳过在构建上下文中发送版本控制历史。请注意，
  这意味着你将无法在构建步骤中运行 Git 命令，例如 `git rev-parse`。
- 包含构建产物（如二进制文件）的目录。这些是在开发过程中本地创建的构建产物。
- 包管理器的 vendor 目录，例如 `node_modules`。

通常，`.dockerignore` 文件的内容应与你的 `.gitignore` 文件内容类似。

### 精简基础镜像

在 Dockerfile 中为你的 `FROM` 指令选择更小的镜像，可以帮助减少最终镜像的大小。
[Alpine 镜像](https://hub.docker.com/_/alpine) 是一个最小化 Docker 镜像的典型例子，它提供了你对 Linux 容器所期望的所有 OS 工具。

此外还有特殊的 [`scratch` 镜像](https://hub.docker.com/_/scratch)，
它完全不包含任何内容。例如，它可用于创建静态链接二进制文件的镜像。

### 多阶段构建

[多阶段构建](/build/building/multi-stage/) 可以让你的构建运行得更快，
因为各个阶段可以并行运行。它也可以使你的最终结果更小。
编写 Dockerfile 时，应确保最终的运行时阶段使用尽可能小的基础镜像，并且仅包含程序运行所需的资源。

你也可以使用 Dockerfile 的 `COPY --from` 指令，
[从其他镜像或阶段复制资源](/build/building/multi-stage/#name-your-build-stages)。
这种技术可以减少最终阶段的层数以及这些层的大小。

### 在构建中获取远程文件

在可能的情况下，你应该在构建过程中从远程位置获取文件，而不是将文件打包到构建上下文中。
直接在 Docker Build Cloud 服务器上下载文件会更好，因为这可能比通过构建上下文传输文件更快。

你可以在构建期间使用 [Dockerfile 的 `ADD` 指令](/reference/dockerfile/#add)
来获取远程文件，或者在 `RUN` 指令中使用 `wget` 和 `rsync` 等工具来获取。

### 多线程工具

你在构建指令中使用的一些工具默认可能不会利用多核。
`make` 就是一个典型的例子，它默认使用单线程，除非你指定 `make --jobs=<n>` 选项。
对于涉及此类工具的构建步骤，请尝试检查是否可以通过并行化来优化执行。