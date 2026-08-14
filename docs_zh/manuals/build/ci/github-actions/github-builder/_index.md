---
title: Docker GitHub Builder
linkTitle: GitHub Builder
description: 使用 Docker 维护的可复用 GitHub Actions 工作流，通过 BuildKit 构建镜像与本地产物。
keywords: ci, github actions, gha, buildkit, buildx, bake, reusable workflows
params:
  sidebar:
    badge:
      color: green
      text: New
---

Docker GitHub Builder 是 [`docker/github-builder` 仓库](https://github.com/docker/github-builder) 中一组
[可复用工作流](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)，
用于通过 [BuildKit](../../../buildkit/_index.md) 构建容器镜像与本地产物。
本节说明这些工作流解决了什么问题、它们与在每个仓库中自行拼接多个 GitHub Actions 有何不同，
以及何时应使用 [`build.yml`](build.md) 或 [`bake.yml`](bake.md)。

如果你用 `docker/login-action`、`docker/setup-buildx-action`、`docker/metadata-action`
以及 `docker/build-push-action` 或 `docker/bake-action` 来组合一个构建作业，
那么你的仓库将掌控构建运行方式的每一个细节。这种方式可行，但也意味着每个仓库都必须自行维护
runner 选择、[缓存配置](../cache.md)、[来源证明（Provenance）设置](../attestations.md)、
签名行为以及[多平台 manifest 处理](../multi-platform.md)。
Docker GitHub Builder 将这些实现细节移入 Docker 维护的可复用工作流中，
因此你的工作流只需决定何时构建以及传入哪些输入。

这种差异在作业定义中最为直观。传统工作流会逐一写出每个 action 步骤：

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@{{% param "setup_qemu_action_version" %}}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        
      - name: Docker meta
        uses: docker/metadata-action@{{% param "metadata_action_version" %}}
        id: meta
        with:
          images: name/app

      - name: Build and push
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha
```

使用 Docker GitHub Builder 后，同样的构建只是一个可复用工作流调用：

```yaml
jobs:
  build:
    uses: docker/github-builder/.github/workflows/build.yml@{{% param "github_builder_version" %}}
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: image
      push: ${{ github.event_name != 'pull_request' }}
      meta-images: name/app
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

这种模式为你提供一条由 Docker 组织维护的构建流水线，它使用固定版本的
[BuildKit](../../../buildkit/_index.md) 环境，在有帮助时跨 runner 分发
[多平台构建](../../../building/multi-platform.md)，并生成已签名的
[SLSA provenance](../../../metadata/attestations/slsa-provenance.md)，
其中记录了源提交与构建者身份。

这种权衡是刻意为之。你保留对构建何时运行以及使用哪些输入的控制权，
但构建实现本身位于 Docker 维护的工作流中，而非各仓库的作业步骤里。

当你的仓库基于 Dockerfile 构建、且熟悉的 `build-push-action` 输入能清晰地映射到你的工作流时，
使用 [`build.yml`](build.md)。当你的仓库已用 [Bake 定义](../../../bake/_index.md) 描述构建，
或希望将 Bake targets、overrides 和变量保持为单一事实来源时，使用 [`bake.yml`](bake.md)。

两个工作流都支持镜像输出、本地输出、导出缓存到
[GitHub Actions 缓存后端](../../../cache/backends/gha.md)、
[SBOM 生成](../../../metadata/attestations/sbom.md)以及签名。Bake 工作流额外增加了
Bake 定义校验，并且每次工作流调用只构建一个 target。

{{% sectionlinks %}}
