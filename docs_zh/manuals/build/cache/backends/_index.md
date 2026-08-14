---
title: 缓存存储后端
description: |
  缓存后端让你能够在外部管理构建缓存。
  外部缓存有助于创建可共享的缓存，从而帮助
  加速内部循环和 CI 构建。
keywords: build, buildx, cache, backend, gha, azblob, s3, registry, local
aliases:
  - /build/building/cache/backends/
---

为了确保构建快速，BuildKit 会自动将构建结果缓存到其内部的缓存中。此外，BuildKit 还支持将构建缓存导出到外部位置，以便在将来的构建中导入。

在 CI/CD 构建环境中，外部缓存几乎不可或缺。这类环境通常在各次运行之间几乎没有持久化存储，但仍然需要尽可能降低镜像构建的运行时间。

默认的 `docker` 驱动支持 `inline`、`local`、`registry` 和 `gha` 缓存后端，但前提是已启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)。其他缓存后端需要你选择不同的 [driver](/manuals/build/builders/drivers/_index.md)。

> [!WARNING]
>
> 如果你在构建过程中使用了密钥或凭据，请确保通过专用的
> [`--secret` option](/reference/cli/docker/buildx/build/#secret) 来管理它们。
> 使用 `COPY` 或 `ARG` 手动管理密钥可能导致凭据泄露。

## 后端（Backends）

Buildx 支持以下缓存存储后端：

- `inline`：将构建缓存嵌入到镜像中。

  内联缓存会被推送到与主输出结果相同的位置。这仅适用于 [`image` 导出器](../../exporters/image-registry.md)。

- `registry`：将构建缓存嵌入到一个单独的镜像中，并推送到与主输出不同的专用位置。

- `local`：将构建缓存写入文件系统上的本地目录。

- `gha`：将构建缓存上传到
  [GitHub Actions 缓存](https://docs.github.com/en/rest/actions/cache)（测试版）。

- `s3`：将构建缓存上传到
  [AWS S3 存储桶](https://aws.amazon.com/s3/)（未发布）。

- `azblob`：将构建缓存上传到
  [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
  （未发布）。

## 命令语法（Command syntax）

要使用上述任意缓存后端，你首先需要在构建时通过
[`--cache-to` option](/reference/cli/docker/buildx/build/#cache-to)
指定它，以将缓存导出到你选择的存储后端。然后，使用
[`--cache-from` option](/reference/cli/docker/buildx/build/#cache-from)
将缓存从该存储后端导入到当前构建中。与始终启用的本地 BuildKit 缓存不同，所有缓存存储后端都必须显式导出，并显式导入。

使用 `registry` 后端并同时进行缓存导入与导出的 `buildx` 命令示例：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image>[,parameters...] .
```

> [!WARNING]
>
> 通常来说，每个缓存都会写入某个位置。在没有覆盖先前缓存数据的情况下，任何位置都不能被写入两次。如果你希望维护多个作用域隔离的缓存（例如每个 Git 分支一个缓存），请务必为导出的缓存使用不同的位置。

## 多缓存（Multiple caches）

BuildKit 支持多个缓存导出器，允许你将缓存推送到多个目标。你也可以从任意数量的远程缓存中导入。例如，一种常见模式是同时使用当前分支和主分支的缓存。以下示例展示了使用注册表缓存后端从多个位置导入缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:<branch> \
  --cache-from type=registry,ref=<registry>/<cache-image>:main .
```

## 配置选项（Configuration options）

本节描述生成缓存导出时可用的一些配置选项。这里描述的选项至少对两种或更多后端类型是通用的。此外，不同的后端类型也支持各自的特定参数。有关哪些配置参数适用的详细信息，请参阅每种后端类型的详细说明页面。

这里描述的通用参数包括：

- [缓存模式](#cache-mode)
- [缓存压缩](#cache-compression)
- [OCI 媒体类型](#oci-media-types)

### 缓存模式（Cache mode）

生成缓存输出时，`--cache-to` 参数接受一个 `mode` 选项，用于定义要包含在导出的缓存中的层。除 `inline` 缓存外，所有缓存后端都支持此选项。

模式可以设置为 `mode=min` 或 `mode=max` 两个选项之一。例如，使用 `mode=max` 与注册表后端构建缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,mode=max \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此选项仅在导出缓存时使用 `--cache-to` 设置。导入缓存时（`--cache-from`），相关参数会被自动检测。

在 `min` 缓存模式（默认）下，只有导出到最终镜像中的层才会被缓存；而在 `max` 缓存模式下，所有层都会被缓存，包括中间步骤的层。

虽然 `min` 缓存通常更小（可加快导入/导出速度并降低存储成本），但 `max` 缓存更可能获得更多的缓存命中。根据你的构建复杂度和位置，你应该对两种参数都进行试验，以找到最适合你的结果。

### 缓存压缩（Cache compression）

缓存压缩选项与 [导出器压缩选项](../../exporters/_index.md#compression) 相同。这由 `local` 和 `registry` 缓存后端支持。

例如，使用 `zstd` 压缩来压缩 `registry` 缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,compression=zstd \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

### OCI 媒体类型（OCI media types）

缓存 OCI 选项与 [导出器 OCI 选项](../../exporters/_index.md#oci-media-types) 相同。这些由 `local` 和 `registry` 缓存后端支持。

例如，要导出 OCI 媒体类型的缓存，请使用 `oci-mediatypes` 属性：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

此属性仅对 `--cache-to` 标志有意义。获取缓存时，BuildKit 会自动检测要使用的正确媒体类型。

默认情况下，OCI 媒体类型会为缓存镜像生成一个 image index。某些 OCI 注册表（如 Amazon ECR）不支持 image index 媒体类型：`application/vnd.oci.image.index.v1+json`。如果你将缓存镜像导出到 ECR，或任何不支持 image index 的注册表，请将 `image-manifest` 参数设置为 `true`，以便为缓存镜像生成单个 image manifest 而非 image index：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>,oci-mediatypes=true,image-manifest=true \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

> [!NOTE]
> 自 BuildKit v0.21 起，`image-manifest` 默认启用。
