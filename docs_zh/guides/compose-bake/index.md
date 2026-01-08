---
title: 使用 Bake 构建 Compose 项目
description: 学习如何使用 Docker Buildx Bake 构建 Docker Compose 项目
summary: '本指南演示如何使用 Bake 为 Docker Compose 项目构建生产级镜像。

  '
tags:
- devops
params:
  time: 20 分钟
---

本指南探讨如何使用 Bake 为包含多个服务的 Docker Compose 项目构建镜像。

[Docker Buildx Bake](/manuals/build/bake/_index.md) 是一个构建编排工具，它支持声明式配置构建过程，类似于 Docker Compose 定义运行时堆栈的方式。对于使用 Docker Compose 启动本地开发服务的项目，Bake 提供了一种方法，可以通过生产就绪的构建配置无缝扩展项目。

## 前提条件

本指南假设您熟悉以下内容：

- Docker Compose
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 概述

本指南将使用 [dvdksn/example-voting-app](https://github.com/dvdksn/example-voting-app) 仓库作为示例，这是一个使用 Docker Compose 的单体仓库（monorepo），可以通过 Bake 进行扩展。

```console
$ git clone https://github.com/dvdksn/example-voting-app.git
$ cd example-voting-app
```

该仓库使用 Docker Compose 在 `compose.yaml` 文件中定义运行应用程序的运行时配置。此应用包含以下服务：

| 服务      | 描述                                                                 |
| --------- | -------------------------------------------------------------------- |
| `vote`    | 一个 Python 前端 Web 应用，允许您在两个选项之间进行投票。            |
| `result`  | 一个 Node.js Web 应用，实时显示投票结果。                            |
| `worker`  | 一个 .NET 工作器，用于消费投票并将其存储在数据库中。                 |
| `db`      | 一个由 Docker 卷支持的 Postgres 数据库。                             |
| `redis`   | 一个收集新投票的 Redis 实例。                                        |
| `seed`    | 一个实用程序容器，用于向数据库植入模拟数据。                         |

`vote`、`result` 和 `worker` 服务均由此仓库中的代码构建而来，而 `db` 和 `redis` 则使用来自 Docker Hub 的现有 Postgres 和 Redis 镜像。`seed` 服务是一个实用程序，它向前端服务调用请求以填充数据库，用于测试目的。

## 使用 Compose 构建

当您启动 Docker Compose 项目时，任何定义了 `build` 属性的服务都会在服务启动前自动构建。以下是示例仓库中 `vote` 服务的构建配置：

```yaml {title="compose.yaml"}
services:
  vote:
    build:
      context: ./vote # 构建上下文
      target: dev # Dockerfile 阶段
```

`vote`、`result` 和 `worker` 服务都指定了构建配置。运行 `docker compose up` 将触发这些服务的构建。

您知道吗，您也可以仅使用 Compose 来构建服务镜像？`docker compose build` 命令允许您使用 Compose 文件中指定的构建配置来调用构建。例如，要使用此配置构建 `vote` 服务，请运行：

```console
$ docker compose build vote
```

省略服务名称以一次性构建所有服务：

```console
$ docker compose build
```

`docker compose build` 命令在您只需要构建镜像而无需运行服务时非常有用。

Compose 文件格式支持多种属性来定义您的构建配置。例如，要指定镜像的标签名称，请在服务上设置 `image` 属性。

```yaml
services:
  vote:
    image: username/vote
    build:
      context: ./vote
      target: dev
    #...

  result:
    image: username/result
    build:
      context: ./result
    #...

  worker:
    image: username/worker
    build:
      context: ./worker
    #...
```

运行 `docker compose build` 会创建三个服务镜像，其完全限定的镜像名称可以推送到 Docker Hub。

`build` 属性支持[广泛的](/reference/compose-file/build.md)选项来配置构建。然而，构建生产级镜像通常与本地开发中使用的镜像不同。为了避免在 Compose 文件中充斥着可能不适用于本地构建的构建配置，可以考虑通过使用 Bake 来分离生产构建和本地构建。这种方法分离了关注点：使用 Compose 进行本地开发，使用 Bake 进行生产就绪的构建，同时仍然重用服务定义和基本的构建配置。

## 使用 Bake 构建

与 Compose 类似，Bake 从配置文件解析项目的构建定义。Bake 支持 HashiCorp Configuration Language (HCL)、JSON 和 Docker Compose YAML 格式。当您使用多个文件时，Bake 会查找所有适用的配置文件并将其合并为一个统一的构建配置。Compose 文件中定义的构建选项会被 Bake 文件中指定的选项扩展，或者在某些情况下被覆盖。

以下部分探讨如何使用 Bake 扩展 Compose 文件中定义的构建选项以用于生产。

### 查看构建配置

Bake 会自动从服务的 `build` 属性创建构建配置。使用 Bake 的 `--print` 标志查看给定 Compose 文件的构建配置。此标志会计算构建配置并以 JSON 格式输出构建定义。

```console
$ docker buildx bake --print
```

JSON 格式的输出显示了将要执行的组（group）以及该组的所有目标（target）。组是构建的集合，目标代表单个构建。

```json
{
  "group": {
    "default": {
      "targets": [
        "vote",
        "result",
        "worker",
        "seed"
      ]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
    },
    "seed": {
      "context": "seed-data",
      "dockerfile": "Dockerfile",
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "target": "dev",
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
    }
  }
}
```

如您所见，Bake 创建了一个包含四个目标的 `default` 组：

- `seed`
- `vote`
- `result`
- `worker`

此组是根据您的 Compose 文件自动创建的；它包含所有具有构建配置的服务。要使用 Bake 构建此服务组，请运行：

```console
$ docker buildx bake
```

### 自定义构建组

首先重新定义 Bake 执行的默认构建组。当前的默认组包含一个 `seed` 目标——一个仅用于向数据库植入模拟数据的 Compose 服务。由于此目标不生成生产镜像，因此无需包含在构建组中。

要自定义 Bake 使用的构建配置，请在仓库根目录下，与您的 `compose.yaml` 文件并排，创建一个名为 `docker-bake.hcl` 的新文件。

```console
$ touch docker-bake.hcl
```

打开 Bake 文件并添加以下配置：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["vote", "result", "worker"]
}
```

保存文件并再次打印您的 Bake 定义。

```console
$ docker buildx bake --print
```

JSON 输出显示 `default` 组仅包含您关心的目标。

```json
{
  "group": {
    "default": {
      "targets": ["vote", "result", "worker"]
    }
  },
  "target": {
    "result": {
      "context": "result",
      "dockerfile": "Dockerfile",
      "tags": ["username/result"]
    },
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "dev"
    },
    "worker": {
      "context": "worker",
      "dockerfile": "Dockerfile",
      "tags": ["username/worker"]
    }
  }
}
```

在这里，每个目标的构建配置（上下文、标签等）都从 `compose.yaml` 文件中获取。组则由 `docker-bake.hcl` 文件定义。

### 自定义目标

Compose 文件目前将 `dev` 阶段定义为 `vote` 服务的构建目标。这对于在本地开发中运行的镜像是合适的，因为 `dev` 阶段包含了额外的开发依赖项和配置。然而，对于生产镜像，您会希望改为以 `final` 镜像为目标。

要修改 `vote` 服务使用的目标阶段，请将以下配置添加到 Bake 文件中：

```hcl
target "vote" {
  target = "final"
}
```

这会覆盖 Compose 文件中指定的 `target` 属性，并使用不同的值。Compose 文件中的其他构建选项（标签、上下文）保持不变。您可以通过使用 `docker buildx bake --print vote` 检查 `vote` 目标的构建配置来验证：

```json
{
  "group": {
    "default": {
      "targets": ["vote"]
    }
  },
  "target": {
    "vote": {
      "context": "vote",
      "dockerfile": "Dockerfile",
      "tags": ["username/vote"],
      "target": "final"
    }
  }
}
```

### 其他构建功能

生产级构建通常具有与开发构建不同的特征。以下是您可能希望为生产镜像添加的一些功能示例。

多平台
: 对于本地开发，您只需要为本地平台构建镜像，因为这些镜像只会在您的机器上运行。但对于要推送到注册表的镜像，通常建议为多个平台（尤其是 arm64 和 amd64）进行构建。

证明（Attestations）
: [证明](/manuals/build/metadata/attestations/_index.md)是附加到镜像的清单，描述了镜像的创建方式及其包含的组件。向镜像附加证明有助于确保您的镜像遵循软件供应链最佳实践。

注解（Annotations）
: [注解](/manuals/build/metadata/annotations.md)为镜像提供描述性元数据。使用注解记录任意信息并将其附加到镜像，这有助于使用者和工具了解镜像的来源、内容以及如何使用。

> [!TIP]
> 为什么不直接在 Compose 文件中定义这些额外的构建选项呢？
>
> Compose 文件格式中的 `build` 属性并不支持所有构建功能。此外，某些功能（如多平台构建）可能会大大增加构建服务所需的时间。对于本地开发，最好保持构建步骤简单快速，将花哨的功能留给发布构建。

要将这些属性添加到您使用 Bake 构建的镜像中，请按如下方式更新 Bake 文件：

```hcl
group "default" {
  targets = ["vote", "result", "worker"]
}

target "_common" {
  annotations = ["org.opencontainers.image.authors=username"]
  platforms = ["linux/amd64", "linux/arm64"]
  attest = [
    "type=provenance,mode=max",
    "type=sbom"
  ]
}

target "vote" {
  inherits = ["_common"]
  target = "final"
}

target "result" {
  inherits = ["_common"]
}

target "worker" {
  inherits = ["_common"]
}
```

这定义了一个新的 `_common` 目标，它定义了可重用的构建配置，用于向镜像添加多平台支持、注解和证明。可重用的目标由构建目标继承。

通过这些更改，使用 Bake 构建项目会为 `linux/amd64` 和 `linux/arm64` 架构生成三组多平台镜像。每个镜像都带有作者注解，以及 SBOM 和来源证明记录。

## 结论

本指南中演示的模式为在使用 Docker Compose 的项目中管理生产就绪的 Docker 镜像提供了一种有用的方法。使用 Bake 让您可以访问 Buildx 和 BuildKit 的所有强大功能，并且还有助于以合理的方式分离您的开发和构建配置。

### 延伸阅读

有关如何使用 Bake 的更多信息，请查看以下资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [使用 Compose 文件进行 Bake 构建](/manuals/build/bake/compose-file.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [使用 Docker Buildx Bake 掌握多平台构建、测试等](/guides/bake/index.md)
- [Bake GitHub Action](https://github.com/docker/bake-action)