---
title: 故障排除
description: 解决在构建、运行或调试 Docker 强化镜像时遇到的常见问题，例如非 root 行为、缺少 Shell 以及端口访问问题。
weight: 40
tags: [故障排除]
keywords: troubleshoot hardened image, docker debug container, non-root permission issue, missing shell error, no package manager
---

以下是在迁移到 Docker 强化镜像 (DHI) 或使用过程中可能遇到的常见问题及其推荐的解决方案。

## 常规调试

Docker 强化镜像针对安全性和运行时性能进行了优化。因此，它们通常不包含 Shell 或标准调试工具。在基于 DHI 构建的容器上进行故障排除的推荐方法是使用 [Docker Debug](./how-to/debug.md)。

Docker Debug 允许您：

- 将临时调试容器附加到现有的容器上。
- 使用 Shell 以及 `curl`、`ps`、`netstat` 和 `strace` 等熟悉的工具。
- 在可写入的临时层中按需安装其他工具，该层会在会话结束后消失。

## 权限

出于增强安全性的考虑，DHI 默认以非 root 用户身份运行。这可能导致在访问文件或目录时出现权限问题。请确保您的应用程序文件和运行时目录由预期的 UID/GID 拥有，或者具有适当的权限。

要了解 DHI 以哪个用户身份运行，请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

## 特权端口

非 root 容器默认无法绑定 1024 以下的端口。这由容器运行时和内核强制执行（尤其是在 Kubernetes 和 Docker Engine < 20.10 中）。

在容器内部，将您的应用程序配置为监听非特权端口（1025 或更高）。例如，`docker run -p 80:8080 my-image` 将容器内的 8080 端口映射到主机的 80 端口，允许您无需 root 权限即可访问它。

## 无 Shell

运行时 DHI 省略了 `sh` 或 `bash` 等交互式 Shell。如果您的构建或工具假设存在 Shell（例如，用于 `RUN` 指令），请在早期的构建阶段使用镜像的 `dev` 变体，并将最终构建产物复制到运行时镜像中。

要了解 DHI 是否包含 Shell，请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

此外，当您需要对正在运行的容器进行 Shell 访问时，请使用 [Docker Debug](./how-to/debug.md)。

## 入口点差异

DHI 定义的入口点可能与 Docker 官方镜像 (DOI) 或其他社区镜像不同。

要了解 DHI 的 ENTRYPOINT 或 CMD，请查看 Docker Hub 上该镜像的仓库页面。有关更多信息，请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

## 无包管理器

运行时 Docker 强化镜像为了安全性和最小攻击面进行了精简。因此，它们不包含 `apk` 或 `apt` 等包管理器。这意味着您无法直接在运行时镜像中安装额外的软件。

如果您的构建或应用程序设置需要安装软件包（例如，编译代码、安装运行时依赖项或添加诊断工具），请在构建阶段使用镜像的 `dev` 变体。然后，仅将必要的构建产物复制到最终的运行时镜像中。