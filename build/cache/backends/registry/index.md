# 注册表缓存


`registry` 缓存存储可以看作是对 `inline` 缓存的扩展。与 `inline` 缓存不同，`registry` 缓存完全独立于镜像，因此使用起来更加灵活——`registry` 支持的缓存能完成内联缓存所能做的一切，而且更多：

- 允许将缓存与最终生成的镜像制品分离，从而你可以在不携带缓存的情况下分发最终镜像。
- 它可以高效地以 `max` 模式缓存多阶段构建，而不只是最终的阶段。
- 它可以与其他导出器配合使用以获得更高灵活性，而不只是 `image` 导出器。

这种缓存存储后端仅在启用了 [containerd 镜像存储](/manuals/desktop/features/containerd.md) 时才与默认的 `docker` 驱动配合工作。如果未启用 containerd 镜像存储，请使用其他驱动。更多信息请参阅 [Build drivers](/manuals/build/builders/drivers/_index.md)。

## 概要（Synopsis）

与更简单的 `inline` 缓存不同，`registry` 缓存支持多个配置参数：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

下表描述了你可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| Name                | Option                  | Type                    | Default | Description                                                                                                                     |
|---------------------|-------------------------|-------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| `ref`               | `cache-to`,`cache-from` | String                  |         | 要导入的缓存镜像的完整名称。                                                                                                    |
| `mode`              | `cache-to`              | `min`,`max`             | `min`   | 要导出的缓存层，参见 [cache mode][1]。                                                                                          |
| `oci-mediatypes`    | `cache-to`              | `true`,`false`          | `true`  | 在导出的清单中使用 OCI 媒体类型，参见 [OCI media types][2]。                                                                    |
| `image-manifest`    | `cache-to`              | `true`,`false`          | `true`  | 使用 OCI 媒体类型时，为缓存镜像生成 image manifest 而非 image index，参见 [OCI media types][2]。                                |
| `compression`       | `cache-to`              | `gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，参见 [cache compression][3]。                                                                                         |
| `compression-level` | `cache-to`              | `0..22`                 |         | 压缩级别，参见 [cache compression][3]。                                                                                         |
| `force-compression` | `cache-to`              | `true`,`false`          | `false` | 强制应用压缩，参见 [cache compression][3]。                                                                                     |
| `ignore-error`      | `cache-to`              | Boolean                 | `false` | 忽略由缓存导出失败引起的错误。                                                                                                  |

[1]: _index.md#cache-mode
[2]: _index.md#oci-media-types
[3]: _index.md#cache-compression

只要 `ref` 的值不与你推送镜像的目标位置相同，你可以为其选择任意有效值。你可能会选择不同的标签（例如 `foo/bar:latest` 和 `foo/bar:build-cache`）、不同的镜像名称（例如 `foo/bar` 和 `foo/bar-cache`），甚至是不同的仓库（例如 `docker.io/foo/bar` 和 `ghcr.io/foo/bar`）。由你来决定将镜像与缓存镜像分离所使用的策略。

如果 `--cache-from` 的目标不存在，缓存导入步骤会失败，但构建仍会继续。

## 延伸阅读（Further reading）

有关缓存的入门介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `registry` 缓存后端的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately)。

