---
title: Bake 简介
linkTitle: 简介（Introduction）
weight: 10
description: 开始使用 Bake 来构建你的项目
keywords: bake, quickstart, build, project, introduction, getting started
---

Bake 是 `docker build` 命令的一层抽象，让你能够以一致的方式更轻松地为团队中的每个人管理
构建配置（CLI 标志、环境变量等）。

Bake 是内置于 Buildx CLI 的命令，因此只要你安装了 Buildx，就可以通过 `docker buildx bake`
命令使用 bake。

## 使用 Bake 构建项目

下面是一个简单的 `docker build` 命令示例：

```console
$ docker build -f Dockerfile -t myapp:latest .
```

该命令构建当前目录下的 Dockerfile，并将生成的镜像标记为 `myapp:latest`。

要使用 Bake 表达相同的构建配置：

```hcl {title=docker-bake.hcl}
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
}
```

Bake 提供了一种结构化的方式来管理你的构建配置，让你不必每次都记住 `docker build` 的所有 CLI 标志。
有了这个文件，构建镜像只需运行：

```console
$ docker buildx bake myapp
```

对于简单的构建，`docker build` 和 `docker buildx bake` 之间的区别微乎其微。然而，随着构建配置
变得复杂，Bake 提供了一种更结构化的方式来管理这种复杂性，而用 `docker build` 的 CLI 标志来管理
会非常困难。它还提供了一种在团队间共享构建配置的方式，使每个人都能以相同配置、一致的方式构建镜像。

## Bake 文件格式

你可以用 HCL 或 JSON 编写 Bake 文件。Bake 还可以读取
[Docker Compose 文件](./compose-file.md)，并将每个服务转换为一个构建目标。HCL 是表达力最强、
最灵活格式，这也是你在本文档以及使用 Bake 的项目中看到它被广泛使用的原因。

可以为目标设置的属性与 `docker build` 的 CLI 标志非常相似。例如，考虑以下 `docker build` 命令：

```console
$ docker build \
  -f Dockerfile \
  -t myapp:latest \
  --build-arg foo=bar \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  .
```

Bake 的等价写法为：

```hcl {title=docker-bake.hcl}
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  args = {
    foo = "bar"
  }
  no-cache = true
  platforms = ["linux/amd64", "linux/arm64"]
}
```

> [!TIP]
>
> 想要在 VS Code 中获得更好的 Bake 文件编辑体验？
> 查看 [Docker DX](https://marketplace.visualstudio.com/items?itemName=docker.docker) 扩展，可获得 lint、代码导航和漏洞扫描功能。

## 下一步

要了解有关使用 Bake 的更多信息，请参阅以下主题：

- 了解如何在 Bake 中定义和使用 [目标（targets）](./targets.md)
- 要查看可以为目标设置的所有属性，请参阅 [Bake 文件参考](/build/bake/reference/)。
