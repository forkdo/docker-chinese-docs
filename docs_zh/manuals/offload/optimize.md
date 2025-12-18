---
title: 优化 Docker Offload 使用
linktitle: 优化使用
weight: 40
description: 了解如何优化 Docker Offload 的使用。
keywords: cloud, optimize, performance, offload
---

Docker Offload 在远程而非您执行命令的本地机器上构建和运行容器。这意味着文件必须通过网络从您的本地系统传输到云端。

网络传输相比本地传输会引入更高的延迟和更低的带宽。

即使有优化措施，大型项目或较慢的网络连接仍可能导致较长的传输时间。以下是几种优化 Docker Offload 使用的方法：

- [使用 `.dockerignore` 文件](#dockerignore-files)
- [选择精简的基础镜像](#slim-base-images)
- [使用多阶段构建](#multi-stage-builds)
- [在构建过程中获取远程文件](#fetch-remote-files-in-build)
- [利用多线程工具](#multi-threaded-tools)

有关 Dockerfile 的一般建议，请参阅 [构建最佳实践](/manuals/build/building/best-practices.md)。

## dockerignore 文件

[`.dockerignore` 文件](/manuals/build/concepts/context.md#dockerignore-files)
允许您指定哪些本地文件不应包含在构建上下文中。这些模式排除的文件不会在构建期间上传到 Docker Offload。

通常需要忽略的项目包括：

- `.git` – 避免传输您的版本历史记录。（注意：您将无法在构建中运行 `git` 命令。）
- 构建产物或本地生成的二进制文件。
- 依赖文件夹，如 `node_modules`（如果这些在构建过程中会重新恢复）。

一般而言，您的 `.dockerignore` 应该与您的 `.gitignore` 类似。

## 精简基础镜像

在 `FROM` 指令中使用较小的基础镜像可以减少最终镜像的大小并提高构建性能。[`alpine`](https://hub.docker.com/_/alpine) 镜像就是一个很好的最小化基础镜像示例。

对于完全静态的二进制文件，您可以使用 [`scratch`](https://hub.docker.com/_/scratch)，这是一个空的基础镜像。

## 多阶段构建

[多阶段构建](/build/building/multi-stage/) 允许您在 Dockerfile 中分离构建时和运行时环境。这不仅可以减少最终镜像的大小，还能在构建过程中实现并行执行各个阶段。

使用 `COPY --from` 从早期阶段或外部镜像复制文件。这种方法有助于最小化不必要的层并减少最终镜像的大小。

## 在构建中获取远程文件

在可能的情况下，在构建过程中从互联网下载大文件，而不是将它们打包在本地上下文中。这可以避免从您的客户端到 Docker Offload 的网络传输。

您可以使用以下方法实现：

- Dockerfile 的 [`ADD` 指令](/reference/dockerfile/#add)
- `RUN` 命令，如 `wget`、`curl` 或 `rsync`

### 多线程工具

某些构建工具（如 `make`）默认是单线程的。如果工具支持，请将其配置为并行运行。例如，使用 `make --jobs=4` 同时运行四个作业。

充分利用云端的可用 CPU 资源可以显著改善构建时间。