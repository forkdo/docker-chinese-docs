---
title: 调试 Docker Hardened Image 容器
linkTitle: 调试容器
weight: 60
keywords: debug, hardened images, DHI, troubleshooting, ephemeral container, docker debug, non-root containers, hardened container image, debug secure container
description: 了解如何使用 Docker Debug 在本地或生产环境中对 Docker Hardened Images (DHI) 进行故障排除。
---

Docker Hardened Images (DHI) 优先考虑极简主义和安全性，这意味着它们有意省略了许多常见的调试工具（如 shell 或包管理器）。这使得直接进行故障排除变得困难且可能带来风险。为了解决这个问题，你可以使用 [Docker
Debug](../../../reference/cli/docker/debug.md)，这是一个安全的工作流程，可以临时将一个临时的调试容器附加到正在运行的服务或镜像上，而无需修改原始镜像。

本指南展示了如何在开发过程中在本地调试 Docker Hardened Images。你也可以使用 `--host` 选项远程调试容器。

以下示例使用镜像 `python:3.13`，但相同的步骤适用于任何镜像。

## 步骤 1：从 Hardened Image 运行一个容器

从一个基于 DHI 的容器开始，模拟一个问题：

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

这个容器不包含 shell 或像 `ps`、`top` 或 `cat` 这样的工具。

如果你尝试：

```console
$ docker exec -it myapp sh
```

你会看到：

```console
exec: "sh": executable file not found in $PATH
```

## 步骤 2：使用 Docker Debug 检查容器

使用 `docker debug` 命令将一个临时的、工具丰富的调试容器附加到正在运行的实例上。

```console
$ docker debug myapp
```

从这里，你可以检查正在运行的进程、网络状态或挂载的文件。

例如，要检查正在运行的进程：

```console
$ ps aux
```

使用以下命令退出调试会话：

```console
$ exit
```

## 下一步

Docker Debug 可帮助你对加固容器进行故障排除，而不会损害原始镜像的完整性。因为调试容器是临时且独立的，所以它避免了将安全风险引入生产环境。

如果你遇到与权限、端口、缺少 shell 或包管理器相关的问题，请参阅 [对 Docker Hardened Images 进行故障排除](../troubleshoot.md) 以获取推荐的解决方案和解决方法。