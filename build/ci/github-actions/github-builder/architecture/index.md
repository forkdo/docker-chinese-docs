# Docker GitHub Builder 架构


Docker GitHub Builder 将仓库编排与构建实现分离。调用方仓库决定构建何时运行、授予哪些
权限与密钥，以及传入哪些输入。位于 [`docker/github-builder` 仓库](https://github.com/docker/github-builder)
中的可复用工作流则拥有构建实现本身。这种拆分让仓库工作流保持精简，同时将 BuildKit、缓存、
provenance、SBOM 生成、签名以及多平台组装集中到由 Docker 维护的单一路径中。

![GitHub Builder overview](./images/architecture-overview.png)

## Core architecture

调用方工作流会调用 [`build.yml`](build.md) 或 [`bake.yml`](bake.md)。
[`build.yml`](build.md) 是面向 Dockerfile 构建的入口点。
[`bake.yml`](bake.md) 是面向 Bake 构建的入口点，其中 Bake 定义仍是 target 与 overrides 的
单一事实来源。在两种情况下，调用方仍然掌握仓库策略，包括触发器、分支条件、权限、密钥、
target 选择、元数据输入，以及镜像输出与本地输出之间的选择。

在可复用工作流内部，第一阶段准备构建。它会校验传入的输入、解析 runner 配置，并将多平台
请求展开为每个平台一个作业。执行模型最容易理解为一个矩阵：`linux/amd64` 运行在 `ubuntu-24.04`
上，`linux/arm64` 运行在 `ubuntu-24.04-arm` 上。每个平台作业独立构建，随后工作流将结果
finalize 为一份面向调用方的输出契约。

```yaml
requested platforms:
  linux/amd64,linux/arm64

conceptual platform jobs:
  linux/amd64 -> ubuntu-24.04
  linux/arm64 -> ubuntu-24.04-arm
```

### Runner selection

`runner` 输入接受单个 GitHub 托管的 Linux runner 标签，或以换行分隔的平台映射。

默认值是使用 GitHub 托管 Ubuntu runner 的平台映射：

```yaml
runner: |
  default=ubuntu-24.04
  linux/arm=ubuntu-24.04-arm
  linux/arm64=ubuntu-24.04-arm
```

在平台作业中，runner 标签解析为单个值：

```yaml
runner: ubuntu-24.04
```

映射必须定义一个 `default` runner。其他键是平台前缀，最具体匹配的前缀优先。例如，`linux/arm`
可匹配 `linux/arm/v7` 等变体，而 `linux/arm64` 是另一个独立前缀：

在下面的示例中，`linux` 匹配那些不匹配更长前缀的 Linux 平台。`default` 键仍然是必需的，
因为它是在没有平台前缀匹配时的回退。

```yaml
runner: |
  default=ubuntu-24.04
  linux=ubuntu-24.04
  linux/arm=ubuntu-24.04-arm
  linux/arm64=ubuntu-24.04-arm
```

可复用工作流要求使用 GitHub 托管的 Linux runner。为兼容起见，旧的 `auto`、`amd64` 和 `arm64`
值仍被接受，但会发出弃用警告。请改用显式的 runner 标签或平台映射。

## Execution path

![GitHub Builder execution flow](./images/execution-flow.png)

执行路径刻意保持精简。调用方仓库调用可复用工作流。可复用工作流准备构建、运行各平台作业，
并 finalize 结果。对于镜像输出，finalization 生成注册表镜像与多平台 manifest。对于本地输出，
finalization 合并各平台文件，并可将合并结果作为 GitHub artifact 上传。调用方无需重建 Buildx、
BuildKit、缓存或 manifest 组装是如何连接在一起的。

## The two reusable entrypoints

[`build.yml`](build.md) 更适合构建已经以面向 Dockerfile 的工作流来表达的场景。它与 `context`、
`file`、`target`、`build-args`、`labels`、`annotations` 和 `platforms` 等概念天然契合。
这是最接近 `docker/build-push-action` 的入口点，区别仅在于工作流实现被集中化了。

[`bake.yml`](bake.md) 更适合仓库已使用 Bake 作为构建定义的场景。它保留了 Bake 模型，
包括 target 解析、`files`、`set` 和 `vars`，同时仍将执行路由到相同的 Docker 维护构建路径。
一个重要的架构细节是：Bake 工作流以每次工作流调用一个 target 为中心，这将 provenance、digest
处理以及最终 manifest 组装一次限定在一个构建单元范围内。

## Output model

可复用工作流暴露一组稳定的面向调用方的输出，以便下游作业能够在不理解内部作业图的情况下消费结果。
实际上，主要的值包括 `digest`、`meta-json`、`artifact-name`、`output-type` 和 `signed`。
这份契约很重要，因为它让晋升（promotion）、发布或后续自动化与 runner 选择及逐平台组装的机制
解耦。

## Examples

### Dockerfile-oriented image build

下面的示例展示了由 [`build.yml`](build.md) 驱动的多平台镜像构建的形态。

```yaml
name: ci

on:
  push:
    branches:
      - "main"
    tags:
      - "v*"
  pull_request:

permissions:
  contents: read

jobs:
  build:
    uses: docker/github-builder/.github/workflows/build.yml@v1
    permissions:
      contents: read
      id-token: write
    with:
      output: image
      push: ${{ github.event_name != 'pull_request' }}
      platforms: linux/amd64,linux/arm64
      meta-images: name/app
      meta-tags: |
        type=ref,event=branch
        type=ref,event=pr
        type=semver,pattern={{version}}
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

这次调用很精简，因为可复用工作流承接了繁重的工作。仓库决定构建何时运行以及它想要哪些输入，
而共享实现则负责 Buildx 设置、BuildKit 配置、平台扇出、元数据生成、provenance、SBOM 生成、
签名以及最终 manifest 创建。

### Bake-oriented local output

下面的示例展示了导出本地输出并上传合并后产物的 Bake 调用的形态。

```yaml
name: ci

on:
  pull_request:

permissions:
  contents: read

jobs:
  bake:
    uses: docker/github-builder/.github/workflows/bake.yml@v1
    permissions:
      contents: read
      id-token: write
    with:
      output: local
      target: binaries
      artifact-upload: true
      artifact-name: bake-output
```

这种形式在仓库已将构建定义保留在 Bake 中、并希望保持该单一事实来源时很有用。工作流将本地
输出行为注入 Bake 运行，在需要时逐平台执行 target，并将结果合并为一份面向调用方的产物。

## Why this architecture works

### Performance

性能优势来自原生平台扇出、共享的 BuildKit 配置以及集中化的缓存处理。多平台工作可以分散到
匹配的 GitHub 托管 runner 上，而不是让每种架构都经过同一台构建机器。这减轻了模拟（emulation）
压力，缩短了跨平台构建的关键路径，并为每个调用方仓库提供相同的优化构建基线。

### Security

安全模型来自将构建实现放在 Docker 维护的可复用工作流中，而非各调用方仓库里临时的作业步骤。
调用方仍然控制权限与密钥，但构建逻辑本身集中审查并纳入版本管理。该项目还将 provenance、SBOM
生成和签名视为一等公民，从而强化了仓库编排与产物生产之间的信任边界。

### Isolation and reliability

可靠性来自关注点分离。调用方仓库编排构建。可复用工作流执行构建。这减少了 CI 漂移，移除了
仓库中重复的胶水代码，并使结果更容易推理——因为调用方看到的是一份稳定的契约，而非一个庞大的
自定义作业定义。

