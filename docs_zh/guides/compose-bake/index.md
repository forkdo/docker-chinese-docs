---
title: 使用 Bake 构建 Compose 项目
description: 了解如何使用 Docker Buildx Bake 构建 Docker Compose 项目的镜像
summary: |
  本指南演示了如何使用 Bake 为 Docker Compose 项目构建生产级镜像。
languages: []
tags: [devops]
params:
  time: 20 分钟
---

本指南探讨了如何使用 Bake 为包含多个服务的 Docker Compose 项目构建镜像。

[Docker Buildx Bake](/manuals/build/bake/_index.md) 是一个构建编排工具，支持以声明式方式配置构建，就像 Docker Compose 为运行时栈定义配置一样。对于使用 Docker Compose 定义本地开发服务的项目，Bake 提供了一种无缝扩展项目的方式，添加生产就绪的构建配置。

## 前置条件

本指南假设您熟悉：

- Docker Compose
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 项目概览

本指南将使用
[dvdksn/example-voting-app](https://github.com/dvdksn/example-voting-app)
仓库作为示例，展示一个使用 Docker Compose 的单体仓库（monorepo）如何通过 Bake 扩展。

```console
$ git clone https://github.com/dvdksn/example-voting-app.git
$ cd example-voting-app
```

该仓库使用 Docker Compose 在 `compose.yaml` 文件中定义应用程序的运行时配置。该应用包含以下服务：

| 服务   | 描述                                                                 |
| ------ | -------------------------------------------------------------------- |
| `vote` | 一个 Python 前端 Web 应用，允许您在两个选项之间投票。                 |
| `result` | 一个 Node.js Web 应用，实时显示投票结果。                            |
| `worker` | 一个 .NET 工作者，消费投票并将其存储到数据库中。                      |
| `db`   | 一个由 Docker 卷支持的 Postgres 数据库。                              |
| `redis` | 一个收集新投票的 Redis 实例。                                        |
| `seed` | 一个工具容器，用于调用前端服务以填充数据库（用于测试）。               |

`vote`、`result` 和 `worker` 服务从仓库中的代码构建，而 `db` 和 `redis` 使用来自 Docker Hub 的预构建 Postgres 和 Redis 镜像。`seed` 服务是一个实用工具，通过调用前端服务生成模拟数据填充数据库，用于测试目的。

## 使用 Compose 构建

当您启动 Docker Compose 项目时，任何定义了 `build` 属性的服务都会在启动前自动构建。以下是示例仓库中 `vote` 服务的构建配置：

```yaml {title="compose.yaml"}
services:
  vote:
    build:
      context: ./vote # 构建上下文
      target: dev # Dockerfile 阶段
```

`vote`、`result` 和 `worker` 服务都指定了构建配置。运行 `docker compose up` 将触发这些服务的构建。

您知道也可以仅使用 Compose 来构建服务镜像吗？`docker compose build` 命令允许您使用 Compose 文件中指定的构建配置调用构建。例如，使用此配置构建 `vote` 服务：

```console
$ docker compose build vote
```

省略服务名称可一次性构建所有服务：

```console
$ docker compose build
```

`docker compose build` 命令在您只需要构建镜像而不需要运行服务时很有用。

Compose 文件格式支持许多属性来定义构建配置。例如，要指定镜像的标签名称，在服务上设置 `image` 属性：

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

运行 `docker compose build` 将创建三个服务镜像，带有完全限定的镜像名称，您可以将它们推送到 Docker Hub。

`build` 属性支持[广泛的选项](/reference/compose-file/build.md)来配置构建。然而，构建生产级镜像通常与本地开发中使用的镜像不同。为避免在 Compose 文件中混入可能不适合本地构建的构建配置，考虑使用 Bake 来构建发布镜像，将生产构建与本地构建分离。这种方法分离了关注点：使用 Compose 进行本地开发，使用 Bake 进行生产就绪的构建，同时仍然重用服务定义和基本构建配置。

## 使用 Bake 构建

与 Compose 类似，Bake 从配置文件解析项目的构建定义。Bake 支持 HashiCorp 配置语言 (HCL)、JSON 和 Docker Compose YAML 格式。当您使用 Bake 与多个文件时，它会找到并合并所有适用的配置文件到一个统一的构建配置中。Compose 文件中定义的构建选项会被 Bake 文件中指定的选项扩展，或在某些情况下被覆盖。

以下部分探讨了如何使用 Bake 扩展 Compose 文件中为生产环境定义的构建选项。

### 查看构建配置

Bake 自动从服务的 `build` 属性创建构建配置。使用 Bake 的 `--print` 标志查看给定 Compose 文件的构建配置。此标志评估构建配置并以 JSON 格式输出构建定义。

```console
$ docker buildx bake --print
```

JSON 格式的输出显示将执行的组，以及该组的所有目标。组是构建的集合，目标代表单个构建。

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

如您所见，Bake 从 Compose 文件自动创建了一个 `default` 组，包含四个目标：

- `seed`
- `vote`
- `result`
- `worker`

此组从您的 Compose 文件创建；它包含所有包含构建配置的服务。要使用 Bake 构建此组服务，运行：

```console
$ docker buildx bake
```

### 自定义构建组

首先重新定义 Bake 执行的默认构建组。当前的默认组包含一个 `seed` 目标——一个仅用于填充数据库模拟数据的 Compose 服务。由于此目标不生成生产镜像，因此不需要将其包含在构建组中。

要自定义 Bake 使用的构建配置，在仓库根目录创建一个新文件，与您的 `compose.yaml` 文件放在一起，命名为 `docker-bake.hcl`。

```console
$ touch docker-bake.hcl
```

打开 Bake 文件并添加以下配置：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["vote", "result", "worker"]
}
```

保存文件并再次打印您的 Bake 定义：

```console
$ docker buildx bake --print
```

JSON 输出显示 `default` 组仅包含您关心的目标：

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

这里，每个目标的构建配置（上下文、标签等）从 `compose.yaml` 文件中获取。组由 `docker-bake.hcl` 文件定义。

### 自定义目标

Compose 文件当前将 `vote` 服务的构建目标定义为 `dev` 阶段。这对于您在本地开发中运行的镜像来说是合适的，因为 `dev` 阶段包含额外的开发依赖和配置。但对于生产镜像，您希望使用 `final` 镜像作为目标。

要修改 `vote` 服务使用的构建目标，在 Bake 文件中添加以下配置：

```hcl
target "vote" {
  target = "final"
}
```

这在使用 Bake 运行构建时会覆盖 Compose 文件中指定的 `target` 属性，使用不同的值。Compose 文件中的其他构建选项（标签、上下文）保持不变。您可以通过检查 `vote` 目标的构建配置来验证：`docker buildx bake --print vote`：

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

### 额外的构建功能

生产级构建通常与开发构建具有不同的特性。以下是您可能想为生产镜像添加的一些功能示例。

多平台
: 对于本地开发，您只需要为本地平台构建镜像，因为这些镜像只是在您的机器上运行。但对于推送到注册表的镜像，通常最好为多个平台构建，特别是 arm64 和 amd64。

证明 (Attestations)
: [证明](/manuals/build/metadata/attestations/_index.md) 是附加到镜像的清单，描述镜像的创建方式和包含的组件。为您的镜像附加证明有助于确保镜像遵循软件供应链最佳实践。

注释 (Annotations)
: [注释](/manuals/build/metadata/annotations.md) 为镜像提供描述性元数据。使用注释记录任意信息并将其附加到镜像，有助于消费者和工具了解镜像的来源、内容和使用方法。

> [!TIP]
> 为什么不直接在 Compose 文件中定义这些额外的构建选项？
>
> Compose 文件格式中的 `build` 属性不支持所有构建功能。此外，某些功能（如多平台构建）可能会显著增加构建服务所需的时间。对于本地开发，最好保持构建步骤简单快速，将高级功能留给发布构建。

要将这些属性添加到您使用 Bake 构建的镜像中，请更新 Bake 文件如下：

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

这定义了一个新的 `_common` 目标，为镜像定义了可重用的构建配置，添加多平台支持、注释和证明。可重用的目标被构建目标继承。

通过这些更改，使用 Bake 构建项目将为 `linux/amd64` 和 `linux/arm64` 架构生成三组多平台镜像。每个镜像都装饰有作者注释，以及 SBOM 和来源证明记录。

## 结论

本指南演示的模式为使用 Docker Compose 的项目管理生产就绪 Docker 镜像提供了一种有用的方法。使用 Bake 让您可以访问 Buildx 和 BuildKit 的所有强大功能，还有助于以合理的方式分离开发和构建配置。

### 进一步阅读

有关如何使用 Bake 的更多信息，请查看这些资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [从 Compose 文件使用 Bake 构建](/manuals/build/bake/compose-file.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [使用 Docker Buildx Bake 掌握多平台构建、测试等](/guides/bake/index.md)
- [Bake GitHub Action](https://github.com/docker/bake-action)