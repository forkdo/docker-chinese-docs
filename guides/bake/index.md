# 精通 Docker Buildx Bake 的多平台构建、测试等功能


本指南演示如何使用 Docker Buildx Bake 简化并自动化构建镜像、测试和生成构建产物的流程。通过在声明式的 `docker-bake.hcl` 文件中定义构建配置，你可以摆脱手写脚本，为复杂的构建、测试和产物生成启用高效的工作流。

## 预备知识

本指南假定你已熟悉：

- Docker
- [Buildx](/manuals/build/concepts/overview.md#buildx)
- [BuildKit](/manuals/build/concepts/overview.md#buildkit)
- [多阶段构建](/manuals/build/building/multi-stage.md)
- [多平台构建](/manuals/build/building/multi-platform.md)

## 前提条件

- 你的机器上已安装较新版本的 Docker。
- 你已安装 Git 以便克隆仓库。
- 你正在使用 [containerd](/manuals/desktop/features/containerd.md) 镜像存储。

## 简介

本指南使用一个示例项目来演示 Docker Buildx Bake 如何精简你的构建与测试工作流。该仓库同时包含一个 Dockerfile 和一个 `docker-bake.hcl` 文件，为你提供一套开箱可用的环境来试用 Bake 命令。

首先克隆示例仓库：

```bash
git clone https://github.com/dvdksn/bakeme.git
cd bakeme
```

Bake 文件 `docker-bake.hcl` 以声明式语法定义构建 target，并使用 target 和 group，使你能够高效地管理复杂构建。

以下是该 Bake 文件的初始内容：

```hcl
target "default" {
  target = "image"
  tags = [
    "bakeme:latest",
  ]
  attest = [
    "type=provenance,mode=max",
    "type=sbom",
  ]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

`target` 关键字为 Bake 定义一个构建 target。`default` target 定义了当命令行上未指定具体 target 时要构建的目标。以下是 `default` target 各选项的简要说明：

- `target`：Dockerfile 中的目标构建阶段。
- `tags`：分配给镜像的标签。
- `attest`：附加到镜像上的[证明](/manuals/build/metadata/attestations/_index.md)。

  > [!TIP]
  > 这些证明提供诸如构建来源 (provenance) 等元数据（用于追踪镜像构建的来源），以及 SBOM（软件物料清单），后者对安全审计与合规非常有用。

- `platforms`：要构建的平台变体。

要执行此构建，请在仓库根目录运行以下命令：

```console
$ docker buildx bake
```

有了 Bake，你无需再记忆冗长难背的命令行咒语，用结构化的配置文件取代手写、易出错的脚本，从而简化构建配置的管理。

作为对比，不使用 Bake 时该构建命令会是这样：

```console
$ docker buildx build \
  --target=image \
  --tag=bakeme:latest \
  --provenance=true \
  --sbom=true \
  --platform=linux/amd64,linux/arm64,linux/riscv64 \
  .
```

## 测试与代码检查

Bake 不仅用于定义构建配置和执行构建。你还可以用 Bake 运行测试，这实际上是把 BuildKit 当作任务运行器使用。在容器中运行测试非常适合确保结果可复现。本节展示如何添加两类测试：

- 使用 `go test` 进行单元测试。
- 使用 `golangci-lint` 对代码风格问题进行检查。

按照测试驱动开发 (TDD) 的方式，先向 Bake 文件中添加一个新的 `test` target：

```hcl
target "test" {
  target = "test"
  output = ["type=cacheonly"]
}
```

> [!TIP]
> 使用 `type=cacheonly` 可确保构建输出实际上被丢弃；各层会保存到 BuildKit 的缓存中，但 Buildx 不会尝试将结果加载到 Docker Engine 的镜像存储中。
>
> 对于测试运行，你无需导出构建输出 —— 只有测试的执行才重要。

要执行这个 Bake target，运行 `docker buildx bake test`。此时你会收到一个错误，提示 Dockerfile 中不存在 `test` 阶段。

```console
$ docker buildx bake test
[+] Building 1.2s (6/6) FINISHED
 => [internal] load local bake definitions
...
ERROR: failed to solve: target stage "test" could not be found
```

为满足该 target，添加对应的 Dockerfile 目标阶段。这里的 `test` 阶段与构建阶段基于同一个 base 阶段。

```dockerfile
FROM base AS test
RUN --mount=target=. \
    --mount=type=cache,target=/go/pkg/mod \
    go test .
```

> [!TIP]
> [`--mount=type=cache` 指令](/manuals/build/cache/optimize.md#use-cache-mounts)会在多次构建之间缓存 Go 模块，避免重复下载依赖，从而提升构建性能。这个共享缓存确保 build、test 及其他阶段都能使用相同的依赖集。

现在，用 Bake 运行 `test` target 就会执行该项目的单元测试。如果你想验证它是否生效，可以随意修改 `main_test.go` 让测试失败。

接下来，为启用代码检查，向 Bake 文件添加另一个名为 `lint` 的 target：

```hcl
target "lint" {
  target = "lint"
  output = ["type=cacheonly"]
}
```

然后在 Dockerfile 中添加对应的构建阶段。该阶段将使用 Docker Hub 上官方的 `golangci-lint` 镜像。

> [!TIP]
> 由于该阶段依赖于执行一个外部依赖，通常最好将你想使用的版本定义为构建参数。这样便可以把依赖版本集中放在 Dockerfile 开头，方便日后管理版本升级。

```dockerfile {hl_lines=[2,"6-8"]}
ARG GO_VERSION="1.23"
ARG GOLANGCI_LINT_VERSION="1.61"

#...

FROM golangci/golangci-lint:v${GOLANGCI_LINT_VERSION}-alpine AS lint
RUN --mount=target=.,rw \
    golangci-lint run
```

最后，为了同时运行两项测试，你可以使用 Bake 文件中的 `groups` 结构。一个 group 可以指定多个 target，通过一次调用一起运行。

```hcl
group "validate" {
  targets = ["test", "lint"]
}
```

现在，同时运行两项测试就这么简单：

```console
$ docker buildx bake validate
```

## 构建变体

有时你需要构建同一程序的多个版本。下面的示例使用 Bake 并借助[矩阵](/manuals/build/bake/matrices.md)分别构建程序的 "release" 和 "debug" 变体。使用矩阵可以让你以不同配置并行执行构建，既节省时间又保证一致性。

矩阵会把单次构建展开为多次构建，每次代表矩阵参数的一种唯一组合。这意味着你可以让 Bake 并行构建程序的生产版本和开发版本，而只需极少的配置改动。

本指南的示例项目已配置为使用一个构建期选项，用于按条件启用调试日志和追踪能力。

- 如果你用 `go build -tags="debug"` 编译程序，就会启用额外的日志与追踪能力（开发模式）。
- 如果构建时不带 `debug` 标签，程序会使用默认日志器编译（生产模式）。

更新 Bake 文件，添加一个定义待构建变量组合的 matrix 属性：

```diff {title="docker-bake.hcl"}
 target "default" {
+  matrix = {
+    mode = ["release", "debug"]
+  }
+  name = "image-${mode}"
   target = "image"
```

`matrix` 属性定义了要构建的变体（"release" 和 "debug"）。`name` 属性定义了矩阵如何展开为多个不同的构建 target。在本例中，matrix 属性把该构建展开为两条工作流：`image-release` 和 `image-debug`，各自使用不同的配置参数。

接下来，定义一个名为 `BUILD_TAGS` 的构建参数，其取值来自矩阵变量。

```diff {title="docker-bake.hcl"}
   target = "image"
+  args = {
+    BUILD_TAGS = mode
+  }
   tags = [
```

你还需要修改这些构建的镜像标签分配方式。按照当前写法，两条矩阵路径会生成相同的镜像标签名并相互覆盖。更新 `tags` 属性，使用条件运算符根据矩阵变量值来设置标签。

```diff {title="docker-bake.hcl"}
   tags = [
-    "bakeme:latest",
+    mode == "release" ? "bakeme:latest" : "bakeme:dev"
   ]
```

- 如果 `mode` 为 `release`，标签名为 `bakeme:latest`
- 如果 `mode` 为 `debug`，标签名为 `bakeme:dev`

最后，更新 Dockerfile，在编译阶段消费 `BUILD_TAGS` 参数。当 `-tags="${BUILD_TAGS}"` 选项求值为 `-tags="debug"` 时，编译器会使用 [`debug.go`](https://github.com/dvdksn/bakeme/blob/75c8a41e613829293c4bd3fc3b4f0c573f458f42/debug.go#L1) 文件中的 `configureLogging` 函数。

```diff {title=Dockerfile}
 # build compiles the program
 FROM base AS build
-ARG TARGETOS TARGETARCH
+ARG TARGETOS TARGETARCH BUILD_TAGS
 ENV GOOS=$TARGETOS
 ENV GOARCH=$TARGETARCH
 RUN --mount=target=. \
        --mount=type=cache,target=/go/pkg/mod \
-       go build -o "/usr/bin/bakeme" .
+       go build -tags="${BUILD_TAGS}" -o "/usr/bin/bakeme" .
```

就这些。做出这些改动后，你的 `docker buildx bake` 命令现在会构建两个多平台镜像变体。你可以使用 `docker buildx bake --print` 命令查看 Bake 生成的规范化构建配置。运行该命令会显示 Bake 将执行一个 `default` group，其中包含两个使用不同构建参数和镜像标签的 target。

```json {collapse=true}
{
  "group": {
    "default": {
      "targets": ["image-release", "image-debug"]
    }
  },
  "target": {
    "image-debug": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "debug"
      },
      "tags": ["bakeme:dev"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    },
    "image-release": {
      "attest": ["type=provenance,mode=max", "type=sbom"],
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "BUILD_TAGS": "release"
      },
      "tags": ["bakeme:latest"],
      "target": "image",
      "platforms": ["linux/amd64", "linux/arm64", "linux/riscv64"]
    }
  }
}
```

把所有平台变体也算进去，这意味着该构建配置总共会生成 6 个不同的镜像。

```console
$ docker buildx bake
$ docker image ls --tree

IMAGE                   ID             DISK USAGE   CONTENT SIZE   USED
bakeme:dev              f7cb5c08beac       49.3MB         28.9MB
├─ linux/riscv64        0eae8ba0367a       9.18MB         9.18MB
├─ linux/arm64          56561051c49a         30MB         9.89MB
└─ linux/amd64          e8ca65079c1f        9.8MB          9.8MB

bakeme:latest           20065d2c4d22       44.4MB         25.9MB
├─ linux/riscv64        7cc82872695f       8.21MB         8.21MB
├─ linux/arm64          e42220c2b7a3       27.1MB         8.93MB
└─ linux/amd64          af5b2dd64fde       8.78MB         8.78MB
```

## 导出构建产物

导出诸如二进制文件之类的构建产物，在部署到没有 Docker 或 Kubernetes 的环境时会很有用。例如，当你的程序本就打算在用户的本地机器上运行时。

> [!TIP]
> 本节讨论的技巧不仅适用于二进制文件等构建输出，也适用于任何类型的产物，例如测试报告。

对于 Go、Rust 这类编译产出的二进制文件通常可移植的编程语言，创建仅用于导出二进制文件的备选构建 target 非常简单。你只需在 Dockerfile 中添加一个空阶段，其中除了你想导出的二进制文件外什么都不放。

首先，我们来添加一种快捷方式，为你的本地平台构建二进制文件，并导出到本地文件系统的 `./build/local`。

在 `docker-bake.hcl` 文件中创建一个新的 `bin` target。在该阶段中，把 `output` 属性设置为一个本地文件系统路径。Buildx 会自动检测到输出看起来像一个文件路径，并使用[本地导出器](/manuals/build/exporters/local-tar.md)将结果导出到指定路径。

```hcl
target "bin" {
  target = "bin"
  output = ["build/bin"]
  platforms = ["local"]
}
```

注意该阶段指定了 `local` 平台。默认情况下，如果未指定 `platforms`，构建会以 BuildKit 主机的操作系统和架构为目标。如果你使用 Docker Desktop，这通常意味着即便你的本机是 macOS 或 Windows，构建目标也会是 `linux/amd64` 或 `linux/arm64`，因为 Docker 运行在一个 Linux 虚拟机中。使用 `local` 平台可强制目标平台与你的本地环境一致。

接下来，向 Dockerfile 添加 `bin` 阶段，从 build 阶段复制编译好的二进制文件。

```dockerfile
FROM scratch AS bin
COPY --from=build "/usr/bin/bakeme" /
```

现在你可以用 `docker buildx bake bin` 导出本地平台版本的二进制文件。例如在 macOS 上，该构建 target 会生成 [Mach-O 格式](https://en.wikipedia.org/wiki/Mach-O)的可执行文件 —— 这是 macOS 的标准可执行格式。

```console
$ docker buildx bake bin
$ file ./build/bin/bakeme
./build/bin/bakeme: Mach-O 64-bit executable arm64
```

接下来，我们添加一个 target 来构建该程序的所有平台变体。为此，你可以[继承](/manuals/build/bake/inheritance.md)刚刚创建的 `bin` target，并通过添加所需平台来扩展它。

```hcl
target "bin-cross" {
  inherits = ["bin"]
  platforms = [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64",
  ]
}
```

现在，构建 `bin-cross` target 会为所有平台生成二进制文件。系统会为每个变体自动创建子目录。

```console
$ docker buildx bake bin-cross
$ tree build/
build/
└── bin
    ├── bakeme
    ├── linux_amd64
    │   └── bakeme
    ├── linux_arm64
    │   └── bakeme
    └── linux_riscv64
        └── bakeme

5 directories, 4 files
```

若想同时生成 "release" 和 "debug" 变体，你可以像处理 default target 那样使用矩阵。使用矩阵时，你还需要根据矩阵值区分输出目录，否则每次矩阵运行都会把二进制文件写到同一位置。

```hcl
target "bin-all" {
  inherits = ["bin-cross"]
  matrix = {
    mode = ["release", "debug"]
  }
  name = "bin-${mode}"
  args = {
    BUILD_TAGS = mode
  }
  output = ["build/bin/${mode}"]
}
```

```console
$ rm -r ./build/
$ docker buildx bake bin-all
$ tree build/
build/
└── bin
    ├── debug
    │   ├── linux_amd64
    │   │   └── bakeme
    │   ├── linux_arm64
    │   │   └── bakeme
    │   └── linux_riscv64
    │       └── bakeme
    └── release
        ├── linux_amd64
        │   └── bakeme
        ├── linux_arm64
        │   └── bakeme
        └── linux_riscv64
            └── bakeme

10 directories, 6 files
```

## 结论

Docker Buildx Bake 精简了复杂的构建工作流，使高效的多平台构建、测试和产物导出成为可能。将 Buildx Bake 集成到项目中，你可以简化 Docker 构建、让构建配置具备可移植性，并驾驭复杂的配置。

尝试不同的配置，并扩展你的 Bake 文件以契合项目需求。你可以考虑把 Bake 集成到 CI/CD 流水线中，实现构建、测试和产物部署的自动化。Buildx Bake 的灵活性与强大能力可以显著改善你的开发与部署流程。

### 延伸阅读

有关如何使用 Bake 的更多信息，请查看以下资源：

- [Bake 文档](/manuals/build/bake/_index.md)
- [矩阵 target](/manuals/build/bake/matrices.md)
- [Bake 文件参考](/manuals/build/bake/reference.md)
- [Bake GitHub Action](https://github.com/docker/bake-action)

