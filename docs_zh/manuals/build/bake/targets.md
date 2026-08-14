---
title: Bake 目标（Targets）
linkTitle: 目标（Targets）
weight: 20
description: 了解如何定义和使用 Bake 中的目标
keywords: bake, target, targets, buildx, docker, buildkit, default
---

Bake 文件中的目标代表一次构建调用。它持有你通常会使用标志传递给 `docker build` 命令的所有信息。

```hcl {title=docker-bake.hcl}
target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要使用 Bake 构建目标，将目标的名称传递给 `bake` 命令。

```console
$ docker buildx bake webapp
```

你可以通过向 `bake` 命令传递多个目标名称来一次构建多个目标。

```console
$ docker buildx bake webapp api tests
```

## 默认目标

如果你在运行 `docker buildx bake` 时没有指定目标，Bake 将构建名为 `default` 的目标。

```hcl {title=docker-bake.hcl}
target "default" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

要构建此目标，不带任何参数地运行 `docker buildx bake`：

```console
$ docker buildx bake
```

## 目标属性

你可以为目标设置的属性与 `docker build` 的 CLI 标志非常相似，只是多了几个 Bake 特有的属性。

`dockerfile` 属性指定目标的 Dockerfile 路径。如果你还设置了 `context`，则 `dockerfile` 路径相对于
该上下文解析。

```hcl {title=docker-bake.hcl}
target "default" {
  context = "app"
  # resolves to app/src/www/Dockerfile
  dockerfile = "src/www/Dockerfile"
}
```

有关可以为目标设置的所有属性，请参阅 [Bake 参考](/build/bake/reference#target)。

## 目标分组

你可以使用 `group` 块将目标分组在一起。当你想一次构建多个目标时这很有用。

```hcl {title=docker-bake.hcl}
group "all" {
  targets = ["webapp", "api", "tests"]
}

target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}

target "api" {
  dockerfile = "api.Dockerfile"
  tags = ["docker.io/username/api:latest"]
  context = "https://github.com/username/api"
}

target "tests" {
  dockerfile = "tests.Dockerfile"
  contexts = {
    webapp = "target:webapp"
    api = "target:api"
  }
  output = ["type=local,dest=build/tests"]
  context = "."
}
```

要构建组中的所有目标，将组的名称传递给 `bake` 命令。

```console
$ docker buildx bake all
```

## 目标和组的模式匹配

Bake 在指定目标或分组目标时支持 shell 风格的通配符模式。这让你可以更轻松地构建多个目标，而无需
逐一显式列出。

支持的模式：

- `*` 匹配任意字符序列
- `?` 匹配任意单个字符
- `[abc]` 匹配方括号内的任意字符

> [!NOTE]
>
> 始终将通配符模式用引号包裹。如果不加引号，你的 shell 会将通配符展开以匹配当前目录中的文件，从而导致错误。

示例：

```console
# Match all targets starting with 'foo-'
$ docker buildx bake "foo-*"

# Match all targets
$ docker buildx bake "*"

# Matches: foo-baz, foo-caz, foo-daz, etc.
$ docker buildx bake "foo-?az"

# Matches: foo-bar, boo-bar
$ docker buildx bake "[fb]oo-bar"

# Matches: mtx-a-b-d, mtx-a-b-e, mtx-a-b-f
$ docker buildx bake "mtx-a-b-*"
```

你也可以组合多个模式：

```console
$ docker buildx bake "foo*" "tests"
```

## 其他资源

参阅以下页面以了解更多关于 Bake 功能的信息：

- 了解如何在 Bake 中使用 [变量](./variables.md)，使你的构建配置更加灵活。
- 了解如何使用矩阵通过 [矩阵（Matrices）](./matrices.md) 以不同配置构建多个镜像。
- 前往 [Bake 文件参考](/build/bake/reference/) 了解你可以在 Bake 文件中设置的所有属性及其语法。
