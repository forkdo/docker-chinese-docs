# 本地缓存


`local` 缓存存储是一种简单的缓存选项，它使用
[OCI 镜像布局](https://github.com/opencontainers/image-spec/blob/main/image-layout.md)
作为底层目录结构，将你的缓存作为文件存储在文件系统的某个目录中。本地缓存是一个不错的选择，适用于你只是进行测试，或者希望灵活地自行管理共享存储解决方案的情况。

## 概要（Synopsis）

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir[,parameters...] \
  --cache-from type=local,src=path/to/local/dir .
```

下表描述了你可以传递给 `--cache-to` 和 `--cache-from` 的可用 CSV 参数。

| Name                | Option       | Type                    | Default | Description                                                                                                                     |
|---------------------|--------------|-------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------|
| `src`               | `cache-from` | String                  |         | 从中导入缓存的本地目录路径。                                                                                                    |
| `digest`            | `cache-from` | String                  |         | 要导入的清单摘要，参见 [cache versioning][4]。                                                                                  |
| `dest`              | `cache-to`   | String                  |         | 缓存导出到的本地目录路径。                                                                                                      |
| `mode`              | `cache-to`   | `min`,`max`             | `min`   | 要导出的缓存层，参见 [cache mode][1]。                                                                                          |
| `oci-mediatypes`    | `cache-to`   | `true`,`false`          | `true`  | 在导出的清单中使用 OCI 媒体类型，参见 [OCI media types][2]。                                                                    |
| `image-manifest`    | `cache-to`   | `true`,`false`          | `true`  | 使用 OCI 媒体类型时，为缓存镜像生成 image manifest 而非 image index，参见 [OCI media types][2]。                                |
| `compression`       | `cache-to`   | `gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，参见 [cache compression][3]。                                                                                         |
| `compression-level` | `cache-to`   | `0..22`                 |         | 压缩级别，参见 [cache compression][3]。                                                                                        |
| `force-compression` | `cache-to`   | `true`,`false`          | `false` | 强制应用压缩，参见 [cache compression][3]。                                                                                     |
| `ignore-error`      | `cache-to`   | Boolean                 | `false` | 忽略由缓存导出失败引起的错误。                                                                                                  |

[1]: _index.md#cache-mode
[2]: _index.md#oci-media-types
[3]: _index.md#cache-compression
[4]: #cache-versioning

如果 `src` 缓存不存在，缓存导入步骤会失败，但构建仍会继续。

## 缓存版本控制（Cache versioning）

<!-- FIXME: update once https://github.com/moby/buildkit/pull/3111 is released -->

本节描述本地文件系统上缓存的版本控制工作原理，以及如何使用 `digest` 参数来使用旧版本的缓存。

如果你手动查看缓存目录，可以看到生成的 OCI 镜像布局：

```console
$ ls cache
blobs  index.json  ingest
$ cat cache/index.json | jq
{
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.index.v1+json",
      "digest": "sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707",
      "size": 1560,
      "annotations": {
        "org.opencontainers.image.ref.name": "latest"
      }
    }
  ]
}
```

与其他缓存类型一样，本地缓存会在导出时通过替换 `index.json` 文件的内容而被替换。不过，先前的缓存仍会保留在 `blobs` 目录中。这些旧缓存可通过 digest 寻址，并会无限期保留。因此，本地缓存的大小会持续增长（更多信息请参阅 [`moby/buildkit#1896`](https://github.com/moby/buildkit/issues/1896)）。

使用 `--cache-from` 导入缓存时，你可以指定 `digest` 参数来强制加载旧版本的缓存，例如：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=local,dest=path/to/local/dir \
  --cache-from type=local,ref=path/to/local/dir,digest=sha256:6982c70595cb91769f61cd1e064cf5f41d5357387bab6b18c0164c5f98c1f707 .
```

## 延伸阅读（Further reading）

有关缓存的入门介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `local` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#local-directory-1)。

