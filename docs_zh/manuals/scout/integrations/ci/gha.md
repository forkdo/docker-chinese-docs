---
description: 如何将 Docker Scout 与 GitHub Actions 集成
keywords: 供应链, 安全, ci, 持续集成, github actions
title: 将 Docker Scout 与 GitHub Actions 集成
linkTitle: GitHub Actions
---

以下示例展示了如何使用 GitHub Actions 设置 Docker Scout 工作流。当触发拉取请求时，该操作会构建镜像，并使用 Docker Scout 将新版本与生产环境中运行的镜像版本进行比较。

此工作流使用 [docker/scout-action](https://github.com/docker/scout-action) GitHub Action 来运行 `docker scout compare` 命令，以可视化拉取请求中的镜像与生产环境中运行的镜像之间的差异。

## 前置条件

- 此示例假设您已拥有一个现有的镜像仓库（在 Docker Hub 或其他注册表中），并且已启用 Docker Scout。
- 此示例使用了 [环境](../environment/_index.md)，通过名为 `production` 的环境中的同一镜像的不同版本来比较拉取请求中构建的镜像。

## 步骤

首先，设置 GitHub Action 工作流以构建镜像。这里与 Docker Scout 无关，但您需要构建一个镜像来进行比较。

将以下内容添加到 GitHub Actions YAML 文件中：

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
  # 您注册表的主机名
  REGISTRY: docker.io
  # 镜像仓库，不含主机名和标签
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      # 向容器注册表进行身份验证
      - name: Authenticate to registry ${{ env.REGISTRY }}
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}
      
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v3

      # 为 Docker 提取元数据（标签、标签）
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          labels: |
            org.opencontainers.image.revision=${{ env.SHA }}
          tags: |
            type=edge,branch=$repo.default_branch
            type=semver,pattern=v{{version}}
            type=sha,prefix=,suffix=,format=short

      # 使用 Buildx 构建并推送 Docker 镜像
      # (不推送 PR，而是加载)
      - name: Build and push Docker image
        id: build-and-push
        uses: docker/build-push-action@v6
        with:
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

这将创建工作流步骤以：

1. 设置 Docker buildx。
2. 向注册表进行身份验证。
3. 从 Git 引用和 GitHub 事件中提取元数据。
4. 构建并推送 Docker 镜像到注册表。

> [!NOTE]
>
> 此 CI 工作流对您的镜像运行本地分析和评估。要在本地评估镜像，您必须确保镜像已加载到运行器的本地镜像存储中。
>
> 如果您将镜像推送到注册表，或构建无法加载到运行器本地镜像存储的镜像（例如多平台镜像或带有 SBOM 或来源证明的镜像），则此比较将无法工作。

完成此设置后，您可以添加以下步骤来运行镜像比较：

```yaml
      # 如果您的注册表是 Docker Hub 并且您之前已进行身份验证，可以跳过此步骤
      - name: Authenticate to Docker
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # 将拉取请求中构建的镜像与生产环境中的镜像进行比较
      - name: Docker Scout
        id: docker-scout
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          ignore-unchanged: true
          only-severities: critical,high
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

比较命令会分析镜像并评估策略合规性，然后将结果与 `production` 环境中对应的镜像进行交叉引用。此示例仅包含严重和高严重性的漏洞，并排除两个镜像中都存在的漏洞，仅显示变化部分。

GitHub Action 默认在拉取请求评论中输出比较结果。

![显示 Docker Scout 在 GitHub Action 中输出结果的截图](../../images/gha-output.webp)

展开 **Policies** 部分以查看两个镜像之间策略合规性的差异。请注意，虽然此示例中的新镜像尚未完全合规，但输出显示新镜像的状态相比基线有所改善。

![GHA 策略评估输出](../../images/gha-policy-eval.webp)