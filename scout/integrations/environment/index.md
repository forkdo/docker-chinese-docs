# 将 Docker Scout 与环境集成

您可以将 Docker Scout 与您的运行时环境集成，并获取正在运行的工作负载的洞察信息。这为您提供了已部署工件安全状态的实时视图。

Docker Scout 允许您定义多个环境，并将镜像分配到不同的环境。这为您提供了软件供应链的完整概览，并让您可以查看和比较环境之间的差异，例如 staging 和 production。

如何定义和命名您的环境取决于您自己。您可以使用对您有意义且与您交付应用程序方式相匹配的模式。

## 分配到环境

每个环境都包含对多个镜像的引用。这些引用代表了在该特定环境中当前运行的容器。

例如，假设您在生产环境中运行 `myorg/webapp:3.1`，您可以将该标签分配给您的 `production` 环境。您可能在 staging 环境中运行同一镜像的不同版本，在这种情况下，您可以将该版本的镜像分配给 `staging` 环境。

要将环境添加到 Docker Scout，您可以：

- 使用 `docker scout env <environment> <image>` CLI 命令手动记录镜像到环境。
- 启用运行时集成以自动检测您环境中的镜像。

Docker Scout 支持以下运行时集成：

- [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout#record-an-image-deployed-to-an-environment)
- [CLI 客户端](./cli.md)
- [Sysdig 集成](./sysdig.md)

> [!NOTE]
>
> 只有组织所有者才能创建新环境和设置集成。
> 此外，Docker Scout 仅在镜像[已被分析](/manuals/scout/explore/analysis.md)的情况下（无论是手动分析还是通过[镜像仓库集成](/manuals/scout/integrations/_index.md#container-registries)分析），才会将镜像分配给环境。

## 列出环境

要查看组织的所有可用环境，您可以使用 `docker scout env` 命令。

```console
$ docker scout env
```

默认情况下，这会打印您个人 Docker 组织的所有环境。要列出您所属的另一个组织的环境，请使用 `--org` 标志。

```console
$ docker scout env --org <org>
```

您可以使用 `docker scout config` 命令来更改默认组织。这会更改所有 `docker scout` 命令的默认组织，而不仅仅是 `env` 命令。

```console
$ docker scout config organization <org>
```

## 环境间比较

将镜像分配到环境可以让您在环境内部和环境之间进行比较。这对于 GitHub 拉取请求等场景非常有用，可以比较从 PR 中的代码构建的镜像与 staging 或 production 中的相应镜像。

您还可以使用 `--to-env` 标志与流进行比较，通过 [`docker scout compare`](/reference/cli/docker/scout/compare.md) CLI 命令：

```console
$ docker scout compare --to-env production myorg/webapp:latest
```

## 查看环境的镜像

要查看环境的镜像：

1. 转到 Docker Scout 仪表板中的 [Images 页面](https://scout.docker.com/)。
2. 打开 **Environments** 下拉菜单。
3. 选择您要查看的环境。

该列表会显示已分配到所选环境的所有镜像。如果您在某个环境中部署了同一镜像的多个版本，则该镜像的所有版本都会出现在列表中。

或者，您可以使用 `docker scout env` 命令从终端查看镜像。

```console
$ docker scout env production
docker/scout-demo-service:main@sha256:ef08dca54c4f371e7ea090914f503982e890ec81d22fd29aa3b012351a44e1bc
```

### 不匹配的镜像标签

当您在 **Images** 选项卡上选择一个环境时，列表中的标签代表用于部署镜像的标签。标签是可变的，这意味着您可以更改标签引用的镜像摘要。如果 Docker Scout 检测到某个标签引用了过时的摘要，则会在镜像名称旁边显示一个警告图标。

- [将 Docker Scout 与 Sysdig 集成](https://docs.docker.com/scout/integrations/environment/sysdig/)

- [通过 CLI 进行通用环境集成](https://docs.docker.com/scout/integrations/environment/cli/)

