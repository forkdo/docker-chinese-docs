---
title: 在 CI 中评估策略合规性
description: |
  配置你的持续集成流水线，当镜像的策略评估结果比基线更差时
  使流水线失败
keywords: scout, supply chain, policy, ci
---

将策略评估添加到你的持续集成流水线中，有助于检测和防止代码变更导致策略合规性比基线更差的情况。

在 CI 环境中推荐的策略评估策略包括评估本地镜像，并将结果与基线进行比较。如果本地镜像的策略合规性比指定基线更差，CI 运行将以错误失败。如果策略合规性更好或未改变，CI 运行成功。

这种比较是相对的，意味着它只关注你的 CI 镜像是否比基线更好或更差。它不是通过或失败所有策略的绝对检查。通过测量相对于你定义的基线，你可以快速查看变更是否对策略合规性产生积极或消极影响。

## 工作原理

当你在 CI 中进行策略评估时，你会在 CI 流水线中构建的镜像上运行本地策略评估。要运行本地评估，你评估的镜像必须存在于 CI 工作流运行的镜像存储中。构建或拉取镜像，然后运行评估。

要运行策略评估，并在本地镜像的合规性比比较基线更差时触发失败，你需要指定用作基线的镜像版本。你可以硬编码特定的镜像引用，但更好的解决方案是使用[环境](../integrations/environment/_index.md)自动从环境中推断镜像版本。以下示例使用环境与 `production` 环境中的镜像进行比较。

## 示例

以下示例展示了如何在 CI 中运行策略评估，使用 [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout) 对 CI 中构建的镜像执行 `compare` 命令。compare 命令有一个 `to-env` 输入，将对名为 `production` 的环境进行比较。`exit-on` 输入设置为 `policy`，意味着仅当策略合规性恶化时比较才会失败。

此示例不假设你使用 Docker Hub 作为容器注册表。因此，此工作流使用 `docker/login-action` 两次：

- 一次用于向你的容器注册表进行身份验证。
- 再次用于向 Docker 进行身份验证，以拉取 `production` 镜像的分析结果。

如果你使用 Docker Hub 作为容器注册表，你只需要进行一次身份验证。

> [!NOTE]
>
> 由于 Docker Engine 的限制，不支持将多平台镜像或带有证明的镜像加载到镜像存储中。
>
> 为了使策略评估正常工作，你必须将镜像加载到运行器的本地镜像存储中。确保你构建的是没有证明的单平台镜像，并且正在加载构建结果。否则，策略评估将失败。

还要注意作业的 `pull-requests: write` 权限。Docker Scout GitHub Action 默认会添加带有评估结果的拉取请求评论，这需要此权限。有关详细信息，请参阅
[Pull Request Comments](https://github.com/docker/scout-action#pull-request-comments)。

```yaml
name: Docker

on:
  push:
    tags: ["*"]
    branches:
      - "main"
  pull_request:
    branches: ["**"]

env:
  REGISTRY: docker.io
  IMAGE_NAME: <IMAGE_NAME>
  DOCKER_ORG: <ORG>

jobs:
  build:
    permissions:
      pull-requests: write

    runs-on: ubuntu-latest
    steps:
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}
      
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build image
        id: build-and-push
        uses: docker/build-push-action@v4
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}

      - name: Authenticate with Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Compare
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          platform: "linux/amd64"
          ignore-unchanged: true
          only-severities: critical,high
          organization: ${{ env.DOCKER_ORG }}
          exit-on: policy
```

以下截图展示了当策略评估检查失败时，GitHub PR 评论的样子，因为 PR 镜像中的策略比基线更差。

![Policy evaluation comment in GitHub PR](../images/scout-policy-eval-ci.webp)

此示例演示了如何使用 GitHub Actions 在 CI 中运行策略评估。Docker Scout 还支持其他 CI 平台。有关更多信息，请参阅 [Docker Scout CI
integrations](../integrations/_index.md#continuous-integration)。