---
title: 使用 Docker Build Cloud
linkTitle: 用法
weight: 20
description: 使用 Buildx CLI 客户端调用云构建
keywords: build, cloud build, usage, cli, buildx, client
aliases:
- /build/cloud/usage/
---

要使用 Docker Build Cloud 进行构建，请调用构建命令并使用 `--builder` 标志指定构建器的名称。

```console
$ docker buildx build --builder cloud-<ORG>-<BUILDER_NAME> --tag <IMAGE> .
```

## 默认使用

如果您希望使用 Docker Build Cloud 而无需每次都指定 `--builder` 标志，可以将其设置为默认构建器。

{{< tabs group="ui" >}}
{{< tab name="CLI" >}}

运行以下命令：

```console
$ docker buildx use cloud-<ORG>-<BUILDER_NAME> --global
```

{{< /tab >}}
{{< tab name="Docker Desktop" >}}

1. 打开 Docker Desktop 设置并导航至 **Builders** 选项卡。
2. 在 **Available builders** 下找到云构建器。
3. 打开下拉菜单并选择 **Use**。

   ![使用 Docker Desktop GUI 选择云构建器作为默认构建器](/build/images/set-default-builder-gui.webp)

{{< /tab >}}
{{< /tabs >}}

使用 `docker buildx use` 更改默认构建器仅会更改 `docker buildx build` 命令的默认构建器。`docker build` 命令仍然使用 `default` 构建器，除非您显式指定 `--builder` 标志。

如果您使用 `make` 等构建脚本，其中使用了 `docker build` 命令，我们建议将您的构建命令更新为 `docker buildx build`。或者，您可以设置 [`BUILDX_BUILDER` 环境变量](/manuals/build/building/variables.md#buildx_builder) 来指定 `docker build` 应使用的构建器。

## 与 Docker Compose 一起使用

要使用 `docker compose build` 通过 Docker Build Cloud 进行构建，首先将云构建器设置为您选择的构建器，然后运行构建。

> [!NOTE]
>
> 确保您使用的是受支持的 Docker Compose 版本，请参阅[先决条件](setup.md#prerequisites)。

```console
$ docker buildx use cloud-<ORG>-<BUILDER_NAME>
$ docker compose build
```

除了 `docker buildx use`，您还可以使用 `docker compose build --builder` 标志或 [`BUILDX_BUILDER` 环境变量](/manuals/build/building/variables.md#buildx_builder) 来选择云构建器。

## 加载构建结果

使用 `--tag` 进行构建会在构建完成后自动将构建结果加载到本地镜像存储中。要在没有标签的情况下构建并加载结果，必须传递 `--load` 标志。

不支持为多平台镜像加载构建结果。构建多平台镜像时，请使用 `docker buildx build --push` 标志将输出推送到注册表。

```console
$ docker buildx build --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64 \
  --tag <IMAGE> \
  --push .
```

如果您想使用标签进行构建，但又不想将结果加载到本地镜像存储中，可以将构建结果仅导出到构建缓存：

```console
$ docker buildx build --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64 \
  --tag <IMAGE> \
  --output type=cacheonly .
```

## 多平台构建

要运行多平台构建，必须使用 `--platform` 标志指定所有要为其构建的平台。

```console
$ docker buildx build --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64 \
  --tag <IMAGE> \
  --push .
```

如果您未指定平台，云构建器会自动为与您本地环境匹配的架构进行构建。

要了解有关为多个平台构建的更多信息，请参阅[多平台构建](/build/building/multi-platform/)。

## Docker Desktop 中的云构建

Docker Desktop 的[构建视图](/desktop/use-desktop/builds/)与 Docker Build Cloud 开箱即用。此视图不仅可以显示您自己的构建信息，还可以显示团队成员使用同一构建器发起的构建信息。

使用共享构建器的团队可以访问以下信息：

- 正在进行和已完成的构建
- 构建配置、统计信息、依赖项和结果
- 构建源（Dockerfile）
- 构建日志和错误

这使您和您的团队可以协作进行故障排除和提高构建速度，而无需来回发送构建日志和基准测试结果。

## 在 Docker Build Cloud 中使用密钥

要在 Docker Build Cloud 中使用构建密钥（例如身份验证凭据或令牌），请为 `docker buildx` 命令使用 `--secret` 和 `--ssh` CLI 标志。流量是加密的，密钥永远不会存储在构建缓存中。

> [!WARNING]
>
> 如果您错误地使用构建参数来传递凭据、身份验证令牌或其他密钥，您应该重构您的构建，改用[密钥挂载](/reference/cli/docker/buildx/build.md#secret)来传递密钥。
> 构建参数存储在缓存中，其值会通过证明（attestations）暴露。
> 密钥挂载不会泄漏到构建之外，也永远不会包含在证明中。

更多信息，请参阅：

- [`docker buildx build --secret`](/reference/cli/docker/buildx/build/#secret)
- [`docker buildx build --ssh`](/reference/cli/docker/buildx/build/#ssh)

## 管理构建缓存

您无需手动管理 Docker Build Cloud 缓存。
系统会通过[垃圾回收](/build/cache/garbage-collection/)为您管理。

如果您达到存储限制，旧缓存会自动删除。
您可以使用 [`docker buildx du` 命令](/reference/cli/docker/buildx/du/) 检查当前的缓存状态。

要手动清除构建器的缓存，请使用 [`docker buildx prune` 命令](/reference/cli/docker/buildx/prune/)。这与修剪任何其他构建器的缓存类似。

> [!WARNING]
>
> 修剪云构建器的缓存也会删除其他使用同一构建器的团队成员的缓存。

## 取消将 Docker Build Cloud 设置为默认构建器

如果您已将云构建器设置为默认构建器，并希望恢复为默认的 `docker` 构建器，请运行以下命令：

```console
$ docker context use default
```

这不会从您的系统中删除构建器。
它只会更改自动选择用于运行构建的构建器。

## 内部网络上的注册表

Docker Build Cloud 可以与内部网络上的[私有注册表](/manuals/build-cloud/builder-settings.md#private-resource-access)或注册表镜像一起使用。