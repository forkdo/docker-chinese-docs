---
title: 故障排除
description: 解决在构建、运行或调试 Docker Hardened Images 时遇到的常见问题，例如非 root 行为、缺少 shell 和端口访问问题。
weight: 40
tags: [故障排除]
keywords: 硬化镜像故障排除, docker 调试容器, 非 root 权限问题, 缺少 shell 错误, 无包管理器
---

以下是在迁移到或使用 Docker Hardened Images (DHIs) 时可能遇到的常见问题及推荐的解决方案。

## 通用调试

Docker Hardened Images 为安全性和运行时性能进行了优化。因此，它们通常不包含 shell 或标准调试工具。推荐的调试基于 DHIs 的容器的方法是使用 [Docker Debug](./how-to/debug.md)。

Docker Debug 允许您：

- 将临时调试容器附加到现有容器。
- 使用 shell 和熟悉的工具，如 `curl`、`ps`、`netstat` 和 `strace`。
- 根据需要在可写、临时层中安装额外工具，会话结束后该层会消失。

## 权限

DHIs 默认以非 root 用户身份运行，以增强安全性。这可能导致在访问文件或目录时出现权限问题。确保您的应用程序文件和运行时目录由预期的 UID/GID 拥有，或具有适当的权限。

要找出 DHI 以哪个用户身份运行，请查看 Docker Hub 上该镜像的仓库页面。更多信息请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

## 特权端口

默认情况下，非 root 容器无法绑定到 1024 以下的端口。这一点由容器运行时和内核强制执行（特别是在 Kubernetes 和 Docker Engine < 20.10 中）。

在容器内，配置您的应用程序监听非特权端口（1025 或更高）。例如 `docker run -p 80:8080 my-image` 将容器内的端口 8080 映射到主机的端口 80，允许您在无需 root 权限的情况下访问它。

## 无 shell

运行时 DHIs 省略了交互式 shell，如 `sh` 或 `bash`。如果您的构建或工具假设存在 shell（例如用于 `RUN` 指令），请在早期构建阶段使用该镜像的 `dev` 变体，并将最终产物复制到运行时镜像中。

要找出 DHI 是否有 shell，请查看 Docker Hub 上该镜像的仓库页面。更多信息请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

此外，当您需要对运行中的容器进行 shell 访问时，请使用 [Docker Debug](./how-to/debug.md)。

## 入口点差异

DHIs 可能定义了与 Docker Official Images (DOIs) 或其他社区镜像不同的入口点。

要找出 DHI 的 ENTRYPOINT 或 CMD，请查看 Docker Hub 上该镜像的仓库页面。更多信息请参阅 [查看镜像变体详情](./how-to/explore.md#view-image-variant-details)。

## 无包管理器

运行时 Docker Hardened Images 为了安全性和最小攻击面而被精简。因此，它们不包含 `apk` 或 `apt` 等包管理器。这意味着您无法直接在运行时镜像中安装额外软件。

如果您的构建或应用程序设置需要安装包（例如编译代码、安装运行时依赖项或添加诊断工具），请在构建阶段使用该镜像的 `dev` 变体。然后，仅将必要的产物复制到最终的运行时镜像中。