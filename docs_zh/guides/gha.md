---
title: GitHub Actions 与 Docker 入门
linkTitle: GitHub Actions 和 Docker
summary: |
  了解如何使用 GitHub Actions 自动构建和推送镜像。
params:
  tags: [devops]
  time: 10 minutes
---

本指南介绍如何使用 Docker 和 GitHub Actions 构建 CI 流水线。你将学会如何使用 Docker 官方的 GitHub Actions 将你的应用构建为 Docker 镜像并推送到 Docker Hub。学完本指南后，你将拥有一个简单、可用的 GitHub Actions Docker 构建配置。你可以直接使用，或根据需要进一步扩展。

## 前置条件

如果你想跟着本指南操作，请确保满足以下条件：

- 一个 Docker 账户。
- 熟悉 Dockerfile。

本指南假设你具备 Docker 基础概念，但会详细解释如何在 GitHub Actions 工作流中使用 Docker。

## 获取示例应用

本指南与具体项目无关，假设你已有一个包含 Dockerfile 的应用。

如果你需要一个示例项目来跟随学习，可以使用 [这个示例应用](https://github.com/dvdksn/rpg-name-generator.git)，它包含用于构建容器化应用的 Dockerfile。或者，你也可以使用自己的 GitHub 项目，或从模板创建新仓库。

{{% dockerfile.inline %}}

{{ $data := resources.GetRemote "https://raw.githubusercontent.com/dvdksn/rpg-name-generator/refs/heads/main/Dockerfile" }}

```dockerfile {collapse=true}
{{ $data.Content }}
```

{{% /dockerfile.inline %}}

## 配置你的 GitHub 仓库

本指南的工作流将构建的镜像推送到 Docker Hub。为此，你必须在 GitHub Actions 工作流中使用 Docker 凭据（用户名和访问令牌）进行身份验证。

有关如何创建 Docker 访问令牌的说明，请参阅
[创建和管理访问令牌](/manuals/security/access-tokens.md)。

准备好 Docker 凭据后，将凭据添加到 GitHub 仓库，以便在 GitHub Actions 中使用：

1. 打开仓库的 **Settings**。
2. 在 **Security** 下，进入 **Secrets and variables > Actions**。
3. 在 **Secrets** 下，创建一个名为 `DOCKER_PASSWORD` 的新仓库密钥，内容为你的 Docker 访问令牌。
4. 接着，在 **Variables** 下，创建一个名为 `DOCKER_USERNAME` 的仓库变量，内容为你的 Docker Hub 用户名。

## 设置 GitHub Actions 工作流

GitHub Actions 工作流定义了一系列步骤来自动化任务，例如构建和推送 Docker 镜像，响应诸如提交或拉取请求等触发器。在本指南中，工作流专注于自动化 Docker 构建和测试，确保你的容器化应用在发布前正常工作。

在仓库的 `.github/workflows/` 目录下创建一个名为 `docker-ci.yml` 的文件。从基本工作流配置开始：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
```

此配置在推送到主分支和拉取请求时运行工作流。通过包含两种触发器，你可以确保在合并拉取请求之前，镜像能够正确构建。

## 提取标签和注释的元数据

工作流的第一步，使用 `docker/metadata-action` 为你的镜像生成元数据。此操作提取 Git 仓库的信息（如分支名和提交 SHA），并生成镜像的元数据，如标签和注释。

将以下 YAML 添加到工作流文件：

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image
```

这些步骤准备了元数据，用于在构建和推送过程中为镜像打标签和添加注释。

- **Checkout** 步骤克隆 Git 仓库。
- **Extract Docker image metadata** 步骤提取 Git 元数据，并为 Docker 构建生成镜像标签和注释。

## 向注册表身份验证

在构建镜像之前，先向注册表身份验证，以确保你能将构建的镜像推送到注册表。

要向 Docker Hub 身份验证，请将以下步骤添加到工作流：

```yaml
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

此步骤使用 [在仓库设置中配置的 Docker 凭据](#configure-your-github-repository)。

## 构建并推送镜像

最后，构建最终的生产镜像并推送到注册表。以下配置构建镜像并直接推送到注册表。

```yaml
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

在此配置中：

- `push: ${{ github.event_name != 'pull_request' }}` 确保仅在事件不是拉取请求时推送镜像。这样，工作流为拉取请求构建和测试镜像，但仅在主分支提交时推送镜像。
- `tags` 和 `annotations` 使用元数据操作的输出，自动为镜像应用一致的标签和 [注释](/manuals/build/metadata/annotations.md)。

## 证明

SBOM（软件物料清单）和来源证明可提高安全性和可追溯性，确保你的镜像满足现代软件供应链要求。

只需少量额外配置，你就可以配置 `docker/build-push-action` 在构建时生成软件物料清单（SBOM）和来源证明。

要生成这些额外元数据，你需要对工作流做两处更改：

- 在构建步骤之前，添加一个使用 `docker/setup-buildx-action` 的步骤。此操作为你的 Docker 构建客户端配置额外功能，这些功能是默认客户端不支持的。
- 然后，更新 **Build and push Docker image** 步骤，启用 SBOM 和来源证明。

以下是更新后的代码片段：

```yaml
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

有关证明的更多详细信息，请参阅
[文档](/manuals/build/metadata/attestations/_index.md)。

## 结论

结合前面部分的所有步骤，以下是完整的工作流配置：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

此工作流实现了使用 GitHub Actions 构建和推送 Docker 镜像的最佳实践。此配置可直接使用，或根据项目需要扩展更多功能，例如
[多平台](/manuals/build/building/multi-platform.md)。

### 延伸阅读

- 在 [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) 部分了解高级配置和示例。
- 对于更复杂的构建设置，你可能需要考虑 [Bake](/manuals/build/bake/_index.md)。（另请参阅 [Mastering Buildx Bake 指南](/guides/bake/index.md)。）
- 了解 Docker 的托管构建服务，专为更快、多平台构建而设计，请参阅 [Docker Build Cloud](/guides/docker-build-cloud/_index.md)。