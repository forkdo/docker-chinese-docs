---
title: 在 Bake 中使用额外的上下文
linkTitle: 上下文（Contexts）
weight: 80
description: |
  当你想要固定镜像版本，或引用其他目标的输出时，额外的上下文非常有用
keywords: build, buildx, bake, buildkit, hcl
aliases:
  - /build/customize/bake/build-contexts/
  - /build/bake/build-contexts/
---

除了定义构建上下文的主 `context` 键之外，每个目标还可以使用键为 `contexts` 的映射来定义
额外的命名上下文。这些值映射到 [build 命令](/reference/cli/docker/buildx/build/#build-context) 中的
`--build-context` 标志。

在 Dockerfile 内部，这些上下文可用于 `FROM` 指令或 `--from` 标志。

支持的上下文值包括：

- 本地文件系统目录
- 容器镜像
- Git URL
- HTTP URL
- Bake 文件中另一个目标的名称

## 固定 alpine 镜像

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello world"
```

```hcl {title=docker-bake.hcl}
target "app" {
  contexts = {
    alpine = "docker-image://alpine:3.13"
  }
}
```

## 使用辅助源目录

```dockerfile {title=Dockerfile}
FROM golang
COPY --from=src . .
```

```hcl {title=docker-bake.hcl}
# Running `docker buildx bake app` will result in `src` not pointing
# to some previous build stage but to the client filesystem, not part of the context.
target "app" {
  contexts = {
    src = "../path/to/source"
  }
}
```

## 使用目标作为构建上下文

要将一个目标的构建结果用作另一个目标的构建上下文，请使用 `target:` 前缀指定目标名称。

```dockerfile {title=baseapp.Dockerfile}
FROM scratch
```

```dockerfile {title=Dockerfile}
# syntax=docker/dockerfile:1
FROM baseapp
RUN echo "Hello world"
```

```hcl {title=docker-bake.hcl}
target "base" {
  dockerfile = "baseapp.Dockerfile"
}

target "app" {
  contexts = {
    baseapp = "target:base"
  }
}
```

在大多数情况下，你应该只使用带有多个目标的单个多阶段 Dockerfile 来实现类似的行为。仅当你有
多个无法轻易合并为一个的 Dockerfile 时，才推荐使用这种情况。
