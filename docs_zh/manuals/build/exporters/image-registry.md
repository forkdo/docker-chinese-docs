---
title: 镜像与镜像仓库导出器
description: |
  镜像和镜像仓库导出器创建一个可以加载到本地镜像存储或推送到镜像仓库的镜像
keywords: build, buildx, buildkit, exporter, image, registry
aliases:
  - /build/building/exporters/image-registry/
---

`image` 导出器将构建结果输出为容器镜像格式。`registry` 导出器与之完全相同，但它通过自动设置 `push=true` 来推送结果。

## 概要（Synopsis）

使用 `image` 和 `registry` 导出器构建容器镜像：

```console
$ docker buildx build --output type=image[,parameters] .
$ docker buildx build --output type=registry[,parameters] .
```

下表描述了你可以为 `type=image` 传递给 `--output` 的可用参数：

| 参数                   | 类型                                   | 默认值  | 描述                                                                                                                                                                       |
| ---------------------- | -------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                 | String                                 |         | 镜像名称。要指定多个名称，请使用逗号分隔的列表。                                                                                                                           |
| `push`                 | `true`,`false`                         | `false` | 创建镜像后进行推送。                                                                                                                                                       |
| `push-by-digest`       | `true`,`false`                         | `false` | 不带名称推送镜像。                                                                                                                                                         |
| `registry.insecure`    | `true`,`false`                         | `false` | 允许推送到不安全的镜像仓库。                                                                                                                                               |
| `dangling-name-prefix` | `<value>`                              |         | 使用 `prefix@<digest>` 命名镜像，用于匿名镜像                                                                                                                              |
| `name-canonical`       | `true`,`false`                         |         | 添加额外的规范名称 `name@<digest>`                                                                                                                                         |
| `compression`          | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip`  | 压缩类型，请参阅 [压缩][1]                                                                                                                                                |
| `compression-level`    | `0..22`                                |         | 压缩级别，请参阅 [压缩][1]                                                                                                                                                |
| `force-compression`    | `true`,`false`                         | `false` | 强制应用压缩，请参阅 [压缩][1]                                                                                                                                            |
| `rewrite-timestamp`    | `true`,`false`                         | `false` | 将文件时间戳重写为 `SOURCE_DATE_EPOCH` 值。有关如何指定 `SOURCE_DATE_EPOCH` 值，请参阅 [构建可复现性][4]。                                                                |
| `oci-mediatypes`       | `true`,`false`                         | `false` | 在导出器清单中使用 OCI 媒体类型，请参阅 [OCI 媒体类型][2]                                                                                                                 |
| `oci-artifact`         | `true`,`false`                         | `false` | 证明被格式化为 OCI 制品，请参阅 [OCI 媒体类型][2]                                                                                                                          |
| `unpack`               | `true`,`false`                         | `false` | 创建后解包镜像（与 containerd 配合使用）                                                                                                                                  |
| `store`                | `true`,`false`                         | `true`  | 将结果镜像存储到 worker 的（例如 containerd）镜像存储中，并确保镜像在内容存储中具有所有 blob。如果 worker 没有镜像存储（例如使用 OCI worker 时），则忽略此参数。            |
| `annotation.<key>`     | String                                 |         | 使用相应的 `key` 和 `value` 将注解附加到构建的镜像上，请参阅 [注解][3]                                                                                                    |

[1]: _index.md#compression
[2]: _index.md#oci-media-types
[3]: #annotations
[4]: https://github.com/moby/buildkit/blob/master/docs/build-repro.md
[5]: /manuals/build/metadata/attestations/_index.md#attestations-as-oci-artifacts

`name` 参数是 `--output` 值内部的 CSV 值。要指定多个镜像名称，请引用完整的 `name` 字段：

```console
$ docker buildx build \
    --output 'type=image,"name=registry.example.com/myapp:1.0,registry.example.com/myapp:latest",push=true' .
```

如果要改用 CLI 标志分配多个名称，请重复使用 [`--tag` 标志](/reference/cli/docker/buildx/build/#tag)。

## Annotations

这些导出器支持使用 `annotation` 参数（后跟使用点表示法的注解名称）添加 OCI 注解。以下示例设置了 `org.opencontainers.image.title` 注解：

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

有关注解的更多信息，请参阅 [BuildKit 文档](https://github.com/moby/buildkit/blob/master/docs/annotations.md)。

## 延伸阅读

有关 `image` 或 `registry` 导出器的更多信息，请参阅 [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#imageregistry)。
