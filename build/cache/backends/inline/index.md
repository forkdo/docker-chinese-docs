# 内联缓存


`inline` 缓存存储后端是获取外部缓存最简单的方式，如果你已经在构建并推送镜像，那么它很容易上手使用。

内联缓存的缺点在于，它不像其他驱动那样能很好地扩展到多阶段构建。它也无法将输出制品与缓存输出分离。这意味着，如果你使用了特别复杂的构建流程，或者不将镜像直接导出到注册表，那么你可能需要考虑使用 [registry](./registry.md) 缓存。

## 概要（Synopsis）

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline \
  --cache-from type=registry,ref=<registry>/<image> .
```

`inline` 缓存不支持额外的参数。

要使用 `inline` 存储导出缓存，请将 `type=inline` 传递给 `--cache-to` 选项：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline .
```

或者，你也可以不通过 `--cache-to` 标志，而是设置构建参数 `BUILDKIT_INLINE_CACHE=1` 来导出内联缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --build-arg BUILDKIT_INLINE_CACHE=1 .
```

要在将来的构建中导入生成的缓存，请将 `type=registry` 传递给 `--cache-from`，这让你能够从指定注册表中的 Docker 镜像内提取缓存：

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-from type=registry,ref=<registry>/<image> .
```

## 延伸阅读（Further reading）

有关缓存的入门介绍，请参阅 [Docker 构建缓存](../_index.md)。

有关 `inline` 缓存后端的更多信息，请参阅
[BuildKit README](https://github.com/moby/buildkit#inline-push-image-and-cache-together)。

