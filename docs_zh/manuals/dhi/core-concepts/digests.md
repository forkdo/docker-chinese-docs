---
title: 镜像摘要
description: 了解 Docker Hardened Images 如何通过签名元数据、来源信息和最小攻击面来保障软件供应链每个阶段的安全。
keywords: docker image digest, pull image by digest, immutable container image, secure container reference, multi-platform manifest
---

## 什么是 Docker 镜像摘要？

Docker 镜像摘要是一个唯一的、基于加密算法的标识符（SHA-256 哈希值），用于表示 Docker 镜像的内容。与可以重复使用或更改的标签不同，摘要是不可变的，能够确保每次拉取的都是完全相同的镜像。这保证了在不同环境和部署之间的一致性。

例如，`nginx:latest` 镜像的摘要可能如下所示：

```text
sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

此摘要唯一标识了 `nginx:latest` 镜像的特定版本，确保镜像内容的任何更改都会生成不同的摘要。

## 为什么镜像摘要很重要？

使用镜像摘要而不是标签具有多个优势：

- **不可变性**：一旦镜像构建完成并生成其摘要，与该摘要关联的内容就无法更改。这意味着如果你使用摘要拉取镜像，你可以确信你获取的是最初构建的完全相同的镜像。

- **安全性**：摘要通过确保镜像内容未被篡改来防止供应链攻击。即使镜像内容发生微小变化，也会导致完全不同的摘要。

- **一致性**：使用摘要确保在不同环境中使用相同的镜像，减少开发、预发布和生产环境之间出现差异的风险。

## Docker Hardened Image 摘要

通过使用镜像摘要引用 DHI（Docker Hardened Images），你可以确保应用程序始终使用完全相同的、安全的镜像版本，从而增强安全性和合规性。

## 查看镜像摘要

### 使用 Docker CLI

要查看 Docker 镜像的摘要，可以使用以下命令。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ docker buildx imagetools inspect <image-name>:<tag>
```

### 使用 Docker Hub UI

1. 访问 [Docker Hub](https://hub.docker.com/) 并登录。
2. 导航到你的组织命名空间并打开镜像的 DHI 仓库。
3. 选择 **Tags** 标签页查看镜像变体。
4. 列表中的每个标签都包含一个 **Digest** 字段，显示镜像的 SHA-256 值。

## 按摘要拉取镜像

按摘要拉取镜像可确保你拉取的是由指定摘要标识的确切镜像版本。

要使用摘要拉取 Docker 镜像，请使用以下命令。将 `<image-name>` 替换为镜像名称，将 `<digest>` 替换为镜像摘要。

```console
$ docker pull <image-name>@sha256:<digest>
```

例如，要使用摘要 `94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a` 拉取 `docs/dhi-python:3.13` 镜像，你需要运行：

```console
$ docker pull docs/dhi-python@sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

## 多平台镜像和清单

Docker Hardened Images 以多平台镜像的形式发布，这意味着单个镜像标签（如 `docs/dhi-python:3.13`）可以支持多种操作系统和 CPU 架构，例如 `linux/amd64`、`linux/arm64` 等。

多平台标签不是指向单个镜像，而是指向一个清单列表（也称为索引），这是一个更高级别的对象，引用多个镜像摘要，每个支持的平台对应一个。

当你使用 `docker buildx imagetools inspect` 检查多平台镜像时，你会看到类似以下内容：

```text
Name:      docs/dhi-python:3.13
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:6e05...d231

Manifests:
  Name:        docs/dhi-python:3.13@sha256:94a0...ea1a
  Platform:    linux/amd64
  ...

  Name:        docs/dhi-python:3.13@sha256:7f1d...bc43
  Platform:    linux/arm64
  ...
```

- 清单列表摘要（`sha256:6e05...d231`）标识整体的多平台镜像。
- 每个特定平台的镜像都有自己的摘要（例如，`linux/amd64` 对应 `sha256:94a0...ea1a`）。

### 为什么这很重要

- **可复现性**：如果你在不同架构上构建或运行容器，仅使用标签会自动解析为你平台对应的镜像摘要。
- **验证**：你可以拉取并验证你平台特定镜像的摘要，以确保你使用的是确切的镜像版本，而不仅仅是清单列表。
- **策略执行**：当使用 Docker Scout 强制执行基于摘要的策略时，每个平台变体都会使用其摘要单独评估。