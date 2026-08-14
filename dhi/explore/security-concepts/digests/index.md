# Image digests


## 什么是 Docker 镜像摘要？（What are Docker image digests?）

Docker 镜像摘要（digest）是一个唯一的、密码学标识符（SHA-256 哈希值），代表某个 Docker 镜像的内容。与可以重复或更改的标签（tag）不同，摘要是不可变的，并且确保每次拉取的都是完全相同的镜像。这保证了在不同环境和部署之间的一致性。

例如，`nginx:latest` 镜像的摘要可能看起来像这样：

```text
sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

该摘要唯一标识了 `nginx:latest` 镜像的特定版本，确保镜像内容的任何改动都会导致一个不同的摘要。

## 为什么镜像摘要很重要？（Why are image digests important?）

使用镜像摘要而非标签具有如下优势：

- 不可变性：镜像一旦构建并生成了摘要，与该摘要绑定的内容就不能再改变。这意味着，如果你使用摘要来拉取镜像，你可以确信取回的就是最初构建的那同一个镜像。
- 安全性：摘要有助于防止供应链攻击，因为它确保镜像内容未被篡改。即便镜像内容有一个微小的改动，也会产生一个完全不同的摘要。
- 一致性：使用摘要可确保在不同环境中使用同一个镜像，降低开发、预发和生产环境之间出现差异的风险。

## Docker Hardened Image 摘要

通过使用镜像摘要来引用 DHI，你可以确保应用程序始终使用完全相同的那个安全镜像版本，从而增强安全性与合规性。

## 查看镜像摘要

### 使用 Docker CLI

要查看 Docker 镜像的镜像摘要，你可以使用以下命令。请将 `<image-name>:<tag>` 替换为镜像名称和标签。

```console
$ docker buildx imagetools inspect <image-name>:<tag>
```

### 使用 Docker Hub UI

1. 前往 [Docker Hub](https://hub.docker.com/) 并登录。
2. 导航到你所在组织的命名空间，打开已镜像的 DHI 仓库。
3. 选择 **Tags** 选项卡以查看镜像变体。
4. 列表中的每个标签都包含一个 **Digest** 字段，用于显示该镜像的 SHA-256 值。

## 按摘要拉取镜像

按摘要拉取镜像可以确保你拉取的是由指定摘要所标识的那个精确镜像版本。

要按摘要拉取 Docker 镜像，使用以下命令。请将 `<image-name>` 替换为镜像名称、`<digest>` 替换为镜像摘要。

```console
$ docker pull <image-name>@sha256:<digest>
```

例如，要按摘要 `94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a` 拉取 `docs/dhi-python:3.13` 镜像，你可以运行：

```console
$ docker pull docs/dhi-python@sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

## 多平台镜像与清单（Multi-platform images and manifests）

Docker Hardened Images 以多平台镜像的形式发布，这意味着一个镜像标签（如 `docs/dhi-python:3.13`）可以支持多种操作系统和 CPU 架构，例如 `linux/amd64`、`linux/arm64` 等。

多平台标签指向的不是单个镜像，而是一个清单列表（manifest list，也称为 index/索引），它是一个更高层级的对象，引用了多个镜像摘要，每个受支持的平台各对应一个。

当你使用 `docker buildx imagetools inspect` 检查一个多平台镜像时，你会看到类似如下内容：

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

- 清单列表摘要（`sha256:6e05...d231`）标识了整个多平台镜像。
- 每个平台特定的镜像都有自己的摘要（例如，`linux/amd64` 对应 `sha256:94a0...ea1a`）。

### 为什么这很重要（Why this matters）

- 可复现性：如果你在不同的架构上构建或运行容器，仅使用标签就会解析为适合你平台的相应镜像摘要。
- 可验证性：你可以拉取并验证适用于你平台的特定镜像摘要，以确保使用的是精确的镜像版本，而不仅仅是清单列表。
- 策略强制执行：当使用 Docker Scout 强制实施基于摘要的策略时，每个平台变体都会通过其摘要被单独评估。

