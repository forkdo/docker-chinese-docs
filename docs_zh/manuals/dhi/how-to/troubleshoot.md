---
title: 故障排除
description: 解决构建、运行或调试 Docker 安全加固镜像时的常见问题，例如非 root 行为、缺少 shell 和端口访问。
weight: 100
tags: [Troubleshooting]
keywords: troubleshoot hardened image, docker debug container, non-root permission issue, missing shell error, no package manager, debug, hardened images, DHI, troubleshooting, ephemeral container, docker debug, non-root containers, hardened container image, debug secure container
aliases:
  - /dhi/how-to/debug/
  - /dhi/troubleshoot/
---

本页介绍在迁移到或使用 Docker 安全加固镜像（DHI）时可能遇到的调试技术和常见问题。

## 常规调试

Docker 安全加固镜像优先考虑最小化和安全性，这意味着它们有意省略了许多常见的调试工具（如 shell 或包管理器）。这使得在没有引入风险的情况下直接进行故障排除变得困难。为了解决这个问题，您可以使用 [Docker Debug](/reference/cli/docker/debug/)，这是一种安全工作流，可在不修改原始镜像的情况下，将临时调试容器附加到正在运行的服务或镜像。

本节介绍如何在开发期间在本地调试 Docker 安全加固镜像。借助 Docker Debug，您还可以使用 `--host` 选项远程调试容器。

### 使用 Docker Debug

#### 步骤 1：从加固镜像运行容器

从一个模拟问题的基于 DHI 的容器开始：

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

该容器不包含 shell 或 `ps`、`top`、`cat` 等工具。

如果您尝试：

```console
$ docker exec -it myapp sh
```

您将看到：

```console
exec: "sh": executable file not found in $PATH
```

#### 步骤 2：使用 Docker Debug 检查容器

使用 `docker debug` 命令将临时的、工具丰富的调试容器附加到正在运行的实例。

```console
$ docker debug myapp
```

在此处，您可以检查正在运行的进程、网络状态或已挂载的文件。

例如，要检查正在运行的进程：

```console
$ ps aux
```

完成后输入 `exit` 离开容器。

### 替代调试方法

除了使用 Docker Debug，您还可以使用以下方法来调试 DHI 容器。

#### 使用 -dev 变体

Docker 安全加固镜像提供 `-dev` 变体，其中包含 shell 和用于安装调试工具的包管理器。只需将镜像标签替换为 `-dev`：

```console
$ docker run -it --rm dhi.io/python:3.13-dev sh
```

完成后输入 `exit` 离开容器。请注意，使用 `-dev` 变体会增加攻击面，不建议将其作为生产环境的运行时。

#### 使用镜像挂载挂载调试工具

您可以使用镜像挂载功能将调试工具挂载到容器中，而无需修改基础镜像。

##### 步骤 1：从加固镜像运行容器

从一个模拟问题的基于 DHI 的容器开始：

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

##### 步骤 2：将调试工具挂载到容器中

运行一个新容器，将工具丰富的镜像（如 `busybox`）挂载到正在运行容器的命名空间中：

```console
$ docker run --rm -it --pid container:myapp \
  --mount type=image,source=busybox,destination=/dbg,ro \
  dhi.io/python:3.13 /dbg/bin/sh
```

这会将 BusyBox 镜像挂载到 `/dbg`，使您可以访问其工具，同时保持原始容器镜像不变。由于加固的 Python 镜像不包含标准实用程序，您需要使用挂载工具的完整路径：

```console
$ /dbg/bin/ls /
$ /dbg/bin/ps aux
$ /dbg/bin/cat /etc/os-release
```

完成后输入 `exit` 离开容器。

## 常见问题

以下是使用 Docker 安全加固镜像时可能遇到的具体问题以及建议的解决方案。

### 权限

DHI 默认以非 root 用户运行，以增强安全性。这可能导致访问文件或目录时出现权限问题。请确保您的应用程序文件和运行时目录由预期的 UID/GID 拥有，或具有适当的权限。

要了解 DHI 以哪个用户运行，请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅[查看镜像变体详细信息](../tools/hub.md#image-variant-details-page)。

### 特权端口

非 root 容器默认无法绑定到 1024 以下的端口。这由容器运行时和内核（尤其是在 Kubernetes 和 Docker Engine < 20.10 中）强制执行。

在容器内部，将您的应用程序配置为侦听非特权端口（1025 或更高）。例如 `docker run -p 80:8080 my-image` 将容器中的端口 8080 映射到主机上的端口 80，使您无需 root 权限即可访问它。

### 无 shell

运行时 DHI 省略了 `sh` 或 `bash` 等交互式 shell。如果您的构建或工具假设存在 shell（例如用于 `RUN` 指令），请在较早的构建阶段使用镜像的 `dev` 变体，并将最终制品复制到运行时镜像中。

要了解 DHI 具有哪些 shell（如果有），请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅[查看镜像变体详细信息](../tools/hub.md#image-variant-details-page)。

此外，当您需要访问正在运行的容器的 shell 时，请使用 Docker Debug。有关更多详细信息，请参阅[常规调试](#general-debugging)。

### 入口点差异

与 Docker 官方镜像（DOI）或其他社区镜像相比，DHI 可能定义了不同的入口点。

要了解 DHI 的 ENTRYPOINT 或 CMD，请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅[查看镜像变体详细信息](../tools/hub.md#image-variant-details-page)。

### 无包管理器

运行时 Docker 安全加固镜像为了安全性和最小的攻击面而进行了精简。因此，它们不包含 `apk` 或 `apt` 等包管理器。这意味着您无法直接在运行时镜像中安装额外的软件。

如果您的构建或应用程序设置需要安装软件包（例如，编译代码、安装运行时依赖项或添加诊断工具），请在构建阶段使用镜像的 `dev` 变体。然后，仅将必要的制品复制到最终的运行时镜像中。
