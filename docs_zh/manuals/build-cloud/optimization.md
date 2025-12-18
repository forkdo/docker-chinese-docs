---
title: 优化云端构建
linkTitle: 优化
weight: 40
description: 远程构建与本地构建不同。以下是如何优化远程构建器的方法。
keywords: build, cloud build, optimize, remote, local, cloud
aliases:
  - /build/cloud/optimization/
---

Docker Build Cloud 在远程运行您的构建，而不是在您调用构建的机器上运行。这意味着客户端和构建器之间的文件传输通过网络进行。

通过网络传输文件的延迟更高，带宽更低，相比本地传输。Docker Build Cloud 具有多种功能来缓解这一问题：

- 它使用附加存储卷来存储构建缓存，这使得读写缓存非常快速。
- 将构建结果加载回客户端时，仅拉取与之前构建相比发生变化的层。

尽管有这些优化，对于大型项目或网络连接较慢的情况，远程构建仍可能导致上下文传输缓慢和镜像加载缓慢。以下是一些优化构建以提高传输效率的方法：

- [Dockerignore 文件](#dockerignore-文件)
- [精简基础镜像](#精简基础镜像)
- [多阶段构建](#多阶段构建)
- [在构建中获取远程文件](#在构建中获取远程文件)
- [多线程工具](#多线程工具)

有关优化构建的更多信息，请参阅
[构建最佳实践](/manuals/build/building/best-practices.md)。

### Dockerignore 文件

使用 [`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)，
您可以明确指定哪些本地文件不包含在构建上下文中。您在忽略文件中指定的 glob 模式匹配的文件不会传输到远程构建器。

您可能想要添加到 `.dockerignore` 文件中的一些示例包括：

- `.git` — 跳过在构建上下文中发送版本控制历史。注意这意味着您无法在构建步骤中运行 Git 命令，例如 `git rev-parse`。
- 包含构建产物的目录，例如二进制文件。这些是在本地开发期间创建的构建产物。
- 包管理器的供应商目录，例如 `node_modules`。

通常，您的 `.dockerignore` 文件的内容应与您的 `.gitignore` 类似。

### 精简基础镜像

为 Dockerfile 中的 `FROM` 指令选择较小的镜像可以帮助减少最终镜像的大小。[Alpine 镜像](https://hub.docker.com/_/alpine) 是一个很好的最小 Docker 镜像示例，它提供了您期望从 Linux 容器获得的所有操作系统实用程序。

还有特殊的 [`scratch` 镜像](https://hub.docker.com/_/scratch)，
它完全不包含任何内容。例如，对于创建静态链接二进制文件的镜像很有用。

### 多阶段构建

[多阶段构建](/build/building/multi-stage/) 可以让您的构建运行得更快，
因为阶段可以并行运行。它还可以使您的最终结果更小。
编写 Dockerfile 时，最终运行时阶段应使用尽可能小的基础镜像，
并且只包含您的程序运行所需的资源。

还可以使用 Dockerfile `COPY --from` 指令
[从其他镜像或阶段复制资源](/build/building/multi-stage/#name-your-build-stages)。
这种技术可以减少最终阶段的层数和层的大小。

### 在构建中获取远程文件

在可能的情况下，您应该在构建期间从远程位置获取文件，
而不是将文件打包到构建上下文中。直接在 Docker Build Cloud 服务器上下载文件更好，
因为它可能比通过构建上下文传输文件更快。

您可以使用
[Dockerfile `ADD` 指令](/reference/dockerfile/#add)，
或在 `RUN` 指令中使用 `wget` 和 `rsync` 等工具在构建期间获取远程文件。

### 多线程工具

您在构建指令中使用的某些工具默认可能不会利用多个核心。一个这样的例子是 `make`，
除非您指定 `make --jobs=<n>` 选项，否则默认使用单线程。对于涉及此类工具的构建步骤，
请尝试检查是否可以通过并行化来优化执行。