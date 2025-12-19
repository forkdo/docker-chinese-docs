---
title: 优化云端构建
linkTitle: 优化
weight: 40
description: &desc 远程构建与本地构建有所不同。本文介绍如何针对远程构建器进行优化。
keywords: build, cloud build, optimize, remote, local, cloud
aliases:
  - /build/cloud/optimization/
params:
  - name: description
    value: *desc
---

Docker Build Cloud 在远程运行构建，而不是在调用构建的机器上执行。这意味着客户端与构建器之间的文件传输通过网络进行。

相比本地传输，网络传输的延迟更高且带宽更低。Docker Build Cloud 提供了多种功能来缓解这个问题：

- 使用附加存储卷作为构建缓存，使缓存的读写速度非常快。
- 将构建结果加载回客户端时，仅拉取与之前构建相比发生变化的层。

尽管有这些优化，对于大型项目或网络连接较慢的情况，远程构建仍可能导致上下文传输和镜像加载缓慢。以下是一些优化构建以提高传输效率的方法：

- [Dockerignore 文件](#dockerignore-files)
- [精简基础镜像](#slim-base-images)
- [多阶段构建](#multi-stage-builds)
- [在构建中获取远程文件](#fetch-remote-files-in-build)
- [多线程工具](#multi-threaded-tools)

有关如何优化构建的更多信息，请参阅
[构建最佳实践](/manuals/build/building/best-practices.md)。

### Dockerignore 文件

使用 [`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)，
可以明确指定哪些本地文件不需要包含在构建上下文中。在忽略文件中指定的 glob 模式匹配的文件不会被传输到远程构建器。

你可能希望添加到 `.dockerignore` 文件的一些示例包括：

- `.git` — 跳过在构建上下文中发送版本控制历史。请注意，这意味着你无法在构建步骤中运行 Git 命令，例如 `git rev-parse`。
- 包含构建产物的目录，例如二进制文件。开发过程中本地创建的构建产物。
- 包管理器的供应商目录，例如 `node_modules`。

通常，`.dockerignore` 文件的内容应与 `.gitignore` 文件中的内容类似。

### 精简基础镜像

在 Dockerfile 的 `FROM` 指令中选择较小的镜像，有助于减小最终镜像的大小。[Alpine 镜像](https://hub.docker.com/_/alpine)
是一个很好的最小化 Docker 镜像示例，它提供了你期望从 Linux 容器中获得的所有操作系统工具。

还有特殊的 [`scratch` 镜像](https://hub.docker.com/_/scratch)，它完全不包含任何内容。例如，对于创建静态链接的二进制文件镜像非常有用。

### 多阶段构建

[多阶段构建](/build/building/multi-stage/) 可以加快构建速度，因为阶段可以并行运行。它还可以使最终结果更小。
以这样的方式编写 Dockerfile，使最终的运行时阶段使用尽可能小的基础镜像，仅包含程序运行所需的资源。

还可以使用 Dockerfile 的 `COPY --from` 指令
[从其他镜像或阶段复制资源](/build/building/multi-stage/#name-your-build-stages)。
这种技术可以减少最终阶段的层数以及这些层的大小。

### 在构建中获取远程文件

如果可能，你应该在构建过程中从远程位置获取文件，而不是将文件捆绑到构建上下文中。直接在 Docker Build Cloud 服务器上下载文件更好，因为这可能比通过构建上下文传输文件更快。

你可以在构建过程中使用
[Dockerfile `ADD` 指令](/reference/dockerfile/#add) 获取远程文件，
或在 `RUN` 指令中使用 `wget` 和 `rsync` 等工具获取。

### 多线程工具

你在构建指令中使用的一些工具默认可能不会利用多个核心。一个这样的例子是 `make`，它默认使用单个线程，除非你指定 `make --jobs=<n>` 选项。对于涉及此类工具的构建步骤，尝试检查是否可以通过并行化来优化执行。