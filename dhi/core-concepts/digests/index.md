# 镜像摘要

## 什么是 Docker 镜像摘要？

Docker 镜像摘要（Image digest）是一种唯一的、加密的标识符（SHA-256 哈希值），用于表示 Docker 镜像的内容。与可以重复使用或更改的标签（tag）不同，摘要具有不可变性，确保每次拉取的都是完全相同的镜像。这保证了不同环境和部署之间的一致性。

例如，`nginx:latest` 镜像的摘要可能如下所示：

```text
sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

该摘要唯一标识了 `nginx:latest` 镜像的特定版本，确保镜像内容的任何更改都会产生不同的摘要。

## 为什么镜像摘要很重要？

使用镜像摘要代替标签具有以下优势：

- **不可变性**：一旦镜像被构建并生成其摘要，与该摘要关联的内容就无法更改。这意味着，如果您使用摘要拉取镜像，可以确信您检索到的正是最初构建的完全相同的镜像。
- **安全性**：摘要有助于防止供应链攻击，因为它确保了镜像内容未被篡改。即使镜像内容发生微小更改，也会导致完全不同的摘要。
- **一致性**：使用摘要可确保在不同环境中使用相同的镜像，从而降低开发、预生产和生产环境之间出现差异的风险。

## Docker Hardened Image 摘要

通过使用镜像摘要来引用 DHIs，您可以确保您的应用程序始终使用完全相同的安全镜像版本，从而增强安全性和合规性。

## 查看镜像摘要

### 使用 Docker CLI

要查看 Docker 镜像的镜像摘要，您可以使用以下命令。将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ docker buildx imagetools inspect <image-name>:<tag>
```

### 使用 Docker Hub UI

1.  前往 [Docker Hub](https://hub.docker.com/) 并登录。
2.  导航到您组织的命名空间并打开镜像的 DHI 仓库。
3.  选择 **Tags** 标签页以查看镜像变体。
4.  列表中的每个标签都包含一个 **Digest** 字段，显示镜像的 SHA-256 值。

## 通过摘要拉取镜像

通过摘要拉取镜像可确保您拉取的是由指定摘要标识的精确镜像版本。

要使用摘要拉取 Docker 镜像，请使用以下命令。将 `<image-name>` 替换为镜像名称，将 `<digest>` 替换为镜像摘要。

```console
$ docker pull <image-name>@sha256:<digest>
```

例如，要使用摘要 `94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a` 拉取 `docs/dhi-python:3.13` 镜像，您可以运行：

```console
$ docker pull docs/dhi-python@sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

## 多平台镜像和清单

Docker Hardened Images 作为多平台镜像发布，这意味着单个镜像标签（如 `docs/dhi-python:3.13`）可以支持多种操作系统和 CPU 架构，例如 `linux/amd64`、`linux/arm64` 等。

多平台标签不是指向单个镜像，而是指向一个清单列表（也称为索引），这是一个更高级别的对象，引用多个镜像摘要，每个支持的平台对应一个。

当您使用 `docker buildx imagetools inspect` 检查多平台镜像时，您会看到类似以下内容：

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

-   清单列表摘要 (`sha256:6e05...d231`) 标识了整个多平台镜像。
-   每个特定平台的镜像都有自己的摘要（例如，`linux/amd64` 的 `sha256:94a0...ea1a`）。

### 为什么这很重要

-   **可重现性**：如果您在不同架构上构建或运行容器，仅使用标签将解析为您平台的相应镜像摘要。
-   **验证**：您可以拉取并验证您平台的特定镜像摘要，以确保您使用的是精确的镜像版本，而不仅仅是清单列表。
-   **策略执行**：当使用 Docker Scout 强制执行基于摘要的策略时，每个平台变体都会使用其摘要进行单独评估。
