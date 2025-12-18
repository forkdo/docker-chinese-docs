---
description:
  Docker Scout 可以与运行时环境集成，为您提供软件供应链的实时洞察。
keywords: 供应链, 安全, 流, 环境, 工作负载, 部署
title: 将 Docker Scout 与环境集成
---

您可以将 Docker Scout 与运行时环境集成，从而获得运行中工作负载的洞察。这为您提供已部署制品的安全状态实时视图。

Docker Scout 允许您定义多个环境，并将镜像分配到不同环境。这为您提供软件供应链的完整概览，并允许您查看和比较环境之间的差异，例如暂存环境和生产环境。

如何定义和命名您的环境由您决定。您可以使用对您有意义的模式，匹配您应用程序的发布方式。

## 分配到环境

每个环境包含对若干镜像的引用。这些引用代表在该特定环境中当前运行的容器。

例如，假设您在生产环境中运行 `myorg/webapp:3.1`，您可以将该标签分配给您的 `production` 环境。您可能在暂存环境中运行同一镜像的不同版本，此时您可以将该版本的镜像分配给 `staging` 环境。

要将环境添加到 Docker Scout，您可以：

- 使用 `docker scout env <environment> <image>` CLI 命令手动记录镜像到环境
- 启用运行时集成以自动检测环境中的镜像

Docker Scout 支持以下运行时集成：

- [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout#record-an-image-deployed-to-an-environment)
- [CLI 客户端](./cli.md)
- [Sysdig 集成](./sysdig.md)

> [!NOTE]
>
> 仅组织所有者可以创建新环境并设置集成。
> 此外，仅当镜像[已被分析](/manuals/scout/explore/analysis.md)（无论是手动还是通过[注册表集成](/manuals/scout/integrations/_index.md#container-registries)）时，Docker Scout 才会将镜像分配到环境。

## 列出环境

要查看组织中所有可用环境，您可以使用 `docker scout env` 命令。

```console
$ docker scout env
```

默认情况下，此命令打印您个人 Docker 组织的所有环境。要列出您所属的另一个组织的环境，请使用 `--org` 标志。

```console
$ docker scout env --org <org>
```

您可以使用 `docker scout config` 命令更改默认组织。这会更改所有 `docker scout` 命令（不仅仅是 `env`）的默认组织。

```console
$ docker scout config organization <org>
```

## 环境间比较

将镜像分配到环境允许您在环境之间进行比较。这对于 GitHub Pull Request 等场景很有用，可以将 PR 代码构建的镜像与暂存或生产环境中的对应镜像进行比较。

您也可以使用 [`docker scout compare`](/reference/cli/docker/scout/compare.md) CLI 命令的 `--to-env` 标志与流进行比较：

```console
$ docker scout compare --to-env production myorg/webapp:latest
```

## 查看环境的镜像

要查看环境的镜像：

1. 转到 Docker Scout 仪表板中的 [Images 页面](https://scout.docker.com/)。
2. 打开 **Environments** 下拉菜单。
3. 选择您要查看的环境。

列表显示已分配给所选环境的所有镜像。如果您在环境中部署了同一镜像的多个版本，所有版本都会出现在列表中。

或者，您可以使用 `docker scout env` 命令从终端查看镜像。

```console
$ docker scout env production
docker/scout-demo-service:main@sha256:ef08dca54c4f371e7ea090914f503982e890ec81d22fd29aa3b012351a44e1bc
```

### 镜像标签不匹配

当您在 **Images** 选项卡中选择环境后，列表中的标签代表用于部署镜像的标签。标签是可变的，意味着您可以更改标签引用的镜像摘要。如果 Docker Scout 检测到标签引用过时的摘要，镜像名称旁边会显示警告图标。