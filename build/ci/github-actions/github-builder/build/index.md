# 使用 Docker GitHub Builder 执行构建


[`build.yml` 可复用工作流](https://github.com/docker/github-builder?tab=readme-ov-file#build-reusable-workflow)
基于 Dockerfile 构建，并封装了许多仓库手动拼接的同一批核心任务。本页介绍如何调用该工作流、
发布[多平台镜像](../../../building/multi-platform.md)，以及在无需每个仓库都重建作业结构的情况下
导出本地构建产物。

## Build and push an image

下面的工作流基于仓库的 Dockerfile 构建，在分支与标签事件上推送，并使用元数据输入生成标签：

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
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
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

当设置 `output: image` 时，`meta-images` 是必填的，因为工作流会基于该输入创建镜像名称与
[manifest 标签](../manage-tags-labels.md)。`distribute: true` 是默认值，因此多平台构建可以
分散到 GitHub 托管的原生 runner 上，而不是把整个构建强行放在一台机器上。默认的 `runner`
映射将 Linux Arm 平台发送到 `ubuntu-24.04-arm`，其他平台使用 `ubuntu-24.04`。要更改该映射，
请参阅 [runner selection](architecture.md#runner-selection)。`sign: auto` 也是默认行为，
意味着工作流会在镜像被推送时签名 [attestation manifests](../attestations.md)。

## Export local output as an artifact

同一个工作流也可以导出文件而非发布镜像。当你希望在 CI 中获得编译产物、解包后的根文件系统，
或其他本地 exporter 结果时，这会很有用：

```yaml
name: ci

on:
  pull_request:

permissions:
  contents: read

jobs:
  build:
    uses: docker/github-builder/.github/workflows/build.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: local
      artifact-upload: true
      artifact-name: build-output
      platforms: linux/amd64,linux/arm64
```

使用 `output: local` 时，工作流将文件导出到 runner 的文件系统，并在 finalize 阶段合并各平台的产物。
当设置 `artifact-upload: true` 时，合并结果会作为 GitHub artifact 上传，且 `sign: auto` 会对
上传的产物签名。本地输出会忽略 `push`，因此这种形式下没有注册表要求。

## Add cache, Dockerfile inputs, and metadata labels

你可以在同一次作业调用中调整 Dockerfile 构建。此示例设置了自定义 Dockerfile 路径、目标阶段、
GitHub Actions 缓存以及元数据标签：

```yaml
name: ci

on:
  push:
    branches:
      - "main"

permissions:
  contents: read

jobs:
  build:
    uses: docker/github-builder/.github/workflows/build.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: image
      push: true
      context: .
      file: ./docker/Dockerfile
      target: runtime
      build-args: |
        NODE_ENV=production
        VERSION=${{ github.sha }}
      cache: true
      cache-scope: myapp
      meta-images: name/app
      meta-tags: |
        type=sha
      set-meta-labels: true
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

这是一个 Dockerfile 构建，因此输入与 `docker/build-push-action` 高度对应。区别在于可复用工作流
负责 Buildx 设置、[BuildKit](../../../buildkit/_index.md) 配置、
[SLSA provenance](../../../metadata/attestations/slsa-provenance.md) 模式、
[GitHub Actions 缓存后端](../../../cache/backends/gha.md) 接线、签名以及 manifest 创建。
如果你需要更多关于元数据或平台分发的背景知识，请参阅
[Manage tags and labels](../manage-tags-labels.md) 与 [Multi-platform image](../multi-platform.md)。

