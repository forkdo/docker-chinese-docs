# 使用 Bake 构建 Compose 项目


本指南探讨如何使用 Bake 为包含多个服务的 Docker Compose 项目构建镜像。

[Docker Buildx Bake](/manuals/build/bake/_index.md) 是一个构建编排工具，它让你可以用声明式配置来定义构建过程，就像 Docker Compose 用于定义运行时栈那样。对于使用 Docker Compose 在本地开发中启动服务的项目，Bake 提供了一种无缝扩展项目、加入生产级构建配置的方式。

## 前提条件

本指南假定你已熟悉：

- Docker Compose
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 项目概览

本指南将使用 [dvdksn/example-voting-app](https://github.com/dvdksn/example-voting-app) 仓库作为示例，展示一个使用 Docker Compose 的 monorepo 如何通过 Bake 进行扩展。

```console
$ git clone https://github.com/dvdksn/example-voting-app.git
$ cd example-voting-app
```

该仓库在 `compose.yaml` 文件中使用 Docker Compose 定义运行应用所需的运行时配置。该应用由以下服务组成：

| 服务     | 描述                                                       |
| -------- | ---------------------------------------------------------- |
| `vote`   | 一个用 Python 编写的前端 Web 应用，可让你在两个选项之间投票。 |
| `result` | 一个 Node.js Web 应用，实时展示投票结果。                    |
| `worker` | 一个 .NET worker，消费投票数据并将其存入数据库。             |
| `db`     | 一个由 Docker 卷支撑的 Postgres 数据库。                     |
| `redis`  | 一个用于收集新投票的 Redis 实例。                            |
| `seed`   | 一个工具容器，用模拟数据填充数据库。                         |

`vote`、`result` 和 `worker` 服务由该仓库中的代码构建，而 `db` 和 `redis` 则使用 Docker Hub 上已有的 Postgres 和 Redis 镜像。`seed` 服务是一个工具，它向前端服务发起请求以填充数据库，用于测试目的。

## 使用 Compose 构建

当你启动一个 Docker Compose 项目时，任何定义了 `build` 属性的服务都会在启动前自动构建。以下是示例仓库中 `vote` 服务的构建配置：

```yaml {title="compose.yaml"}
services:
  vote:
    build:
      context: ./vote # Build context
      target: dev # Dockerfile stage
```

`vote`、`result` 和 `worker` 服务都指定了构建配置。运行 `docker compose up` 会触发这些服务的构建。

你知道吗？你也可以仅使用 Compose 来构建服务镜像。`docker compose build` 命令允许你按 Compose 文件中指定的构建配置发起构建。例如，要使用该配置构建 `vote` 服务，运行：

```console
$ docker compose build vote
```

省略服务名可一次构建所有服务：

```console
$ docker compose build
```

当你只需要构建镜像而不运行服务时，`docker compose build` 命令非常有用。

Compose 文件格式支持多种属性来定义构建配置。例如，要为镜像指定标签名，可在服务上设置 `image` 属性。

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

运行 `docker compose build` 会创建三个带有完整限定镜像名的服务镜像，你可以将它们推送到 Docker Hub。

`build` 属性支持[广泛的选项](/reference/compose-file/build.md)来配置构建。然而，构建生产级镜像往往与本地开发所用镜像有所不同。为避免在 Compose 文件中塞入本地构建并不需要的构建配置，可以考虑使用 Bake 来构建发布镜像，从而将生产构建与本地构建分离。这种方式实现了关注点分离：用 Compose 进行本地开发，用 Bake 进行生产级构建，同时仍然复用服务定义和基础构建配置。

## 使用 Bake 构建

与 Compose 类似，Bake 也从配置文件中解析项目的构建定义。Bake 支持 HashiCorp 配置语言 (HCL)、JSON 以及 Docker Compose YAML 格式。当你在 Bake 中使用多个文件时，它会查找并将所有适用的配置文件合并为一份统一的构建配置。Compose 文件中定义的构建选项会被 Bake 文件中指定的选项扩展，某些情况下则会被覆盖。

以下部分将探讨如何使用 Bake 扩展 Compose 文件中定义的构建选项，以适配生产环境。

### 查看构建配置

Bake 会根据服务的 `build` 属性自动创建构建配置。使用 Bake 的 `--print` 标志可以查看给定 Compose 文件的构建配置。该标志会对构建配置求值，并以 JSON 格式输出构建定义。

```console
$ docker buildx bake --print
```

JSON 格式的输出会显示将要执行的 group，以及该 group 中的所有 target。group 是一组构建的集合，而 target 代表单次构建。

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

如你所见，Bake 创建了一个包含四个 target 的 `default` group：

- `seed`
- `vote`
- `result`
- `worker`

该 group 是根据你的 Compose 文件自动创建的；它包含了所有含构建配置的服务。要使用 Bake 构建这一组服务，运行：

```console
$ docker buildx bake
```

### 自定义构建 group

首先重新定义 Bake 执行的默认构建 group。当前的默认 group 包含一个 `seed` target —— 这是一个仅用于向数据库填充模拟数据的 Compose 服务。由于该 target 不产出生产镜像，因此无需包含在构建 group 中。

要自定义 Bake 使用的构建配置，在仓库根目录下（与 `compose.yaml` 文件并列）创建一个名为 `docker-bake.hcl` 的新文件。

```console
$ touch docker-bake.hcl
```

打开该 Bake 文件并添加以下配置：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["vote", "result", "worker"]
}
```

保存文件，然后再次打印你的 Bake 定义。

```console
$ docker buildx bake --print
```

JSON 输出显示 `default` group 现在只包含你关心的 target。

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

在这里，每个 target 的构建配置（context、tags 等）都取自 `compose.yaml` 文件，而 group 则由 `docker-bake.hcl` 文件定义。

### 自定义 target

目前 Compose 文件将 `dev` 阶段定义为 `vote` 服务的构建目标。对于你在本地开发中运行的镜像来说这很合适，因为 `dev` 阶段包含了额外的开发依赖和配置。然而对于生产镜像，你会希望改为以 `final` 镜像为目标。

要修改 `vote` 服务所使用的目标阶段，将以下配置添加到 Bake 文件中：

```hcl
target "vote" {
  target = "final"
}
```

当你使用 Bake 运行构建时，这会用另一个值覆盖 Compose 文件中指定的 `target` 属性。Compose 文件中的其他构建选项（tag、context）保持不变。你可以用 `docker buildx bake --print vote` 检查 `vote` target 的构建配置来验证：

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

### 其他构建特性

生产级构建通常与开发构建具有不同的特点。以下是你可能希望为生产镜像添加的一些内容示例。

多平台
: 在本地开发中，你只需为本机平台构建镜像，因为这些镜像只会在你的机器上运行。但对于要推送到镜像仓库的镜像，通常最好为多个平台构建，尤其是 arm64 和 amd64。

证明 (Attestations)
: [证明](/manuals/build/metadata/attestations/_index.md)是附加到镜像上的清单，描述该镜像是如何创建的以及包含哪些组件。为镜像附加证明有助于确保你的镜像遵循软件供应链最佳实践。

注解 (Annotations)
: [注解](/manuals/build/metadata/annotations.md)为镜像提供描述性元数据。使用注解可以记录任意信息并附加到镜像上，帮助使用者和工具了解镜像的来源、内容以及使用方式。

> [!TIP]
> 为什么不直接在 Compose 文件中定义这些额外的构建选项呢？
>
> Compose 文件格式中的 `build` 属性并不支持所有构建特性。此外，某些特性（例如多平台构建）会大幅增加构建服务所需的时间。对于本地开发，最好让构建步骤保持简单快速，把那些花哨的功能留给发布构建。

要将这些属性添加到你用 Bake 构建的镜像中，按如下方式更新 Bake 文件：

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

这里定义了一个新的 `_common` target，它定义了可复用的构建配置，用于为镜像添加多平台支持、注解和证明。各个构建 target 继承这个可复用的 target。

做出这些改动后，用 Bake 构建该项目会为 `linux/amd64` 和 `linux/arm64` 架构生成三组多平台镜像。每个镜像都带有作者注解，以及 SBOM 和来源 (provenance) 证明记录。

## 结论

本指南展示的模式为在使用 Docker Compose 的项目中管理生产级 Docker 镜像提供了一种实用方法。使用 Bake 让你能够使用 Buildx 和 BuildKit 的全部强大功能，同时以合理的方式将开发配置与构建配置分离开来。

### 延伸阅读

有关如何使用 Bake 的更多信息，请查看以下资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [从 Compose 文件使用 Bake 构建](/manuals/build/bake/compose-file.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [精通 Docker Buildx Bake 的多平台构建、测试等功能](/guides/bake/)
- [Bake GitHub Action](https://github.com/docker/bake-action)

