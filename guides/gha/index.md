# 使用 Docker 的 GitHub Actions 入门

本指南介绍如何使用 Docker 和 GitHub Actions 构建 CI 流水线。您将学习如何使用 Docker 官方 GitHub Actions 将应用程序构建为 Docker 镜像并推送到 Docker Hub。在本指南结束时，您将拥有一个简单且功能完整的 GitHub Actions 配置，可用于 Docker 构建。您可以直接使用该配置，也可以根据需要进一步扩展。

## 先决条件

如果您想跟随本指南操作，请确保您具备以下条件：

- 一个 Docker 账户。
- 熟悉 Dockerfile。

本指南假定您对 Docker 概念有基本的了解，但会提供在 GitHub Actions 工作流中使用 Docker 的说明。

## 获取示例应用

本指南与项目无关，假定您有一个包含 Dockerfile 的应用程序。

如果您需要一个示例项目来跟随操作，可以使用[这个示例应用程序](https://github.com/dvdksn/rpg-name-generator.git)，它包含一个用于构建应用程序容器化版本的 Dockerfile。或者，您也可以使用自己的 GitHub 项目或从模板创建一个新仓库。





```dockerfile {collapse=true}
#syntax=docker/dockerfile:1

# builder installs dependencies and builds the node app
FROM node:lts-alpine AS builder
WORKDIR /src
RUN --mount=src=package.json,target=package.json \
    --mount=src=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN --mount=type=cache,target=/root/.npm \
    npm run build

# release creates the runtime image
FROM node:lts-alpine AS release
WORKDIR /app
COPY --from=builder /src/build .
EXPOSE 3000
CMD ["node", "."]

```



## 配置您的 GitHub 仓库

本指南中的工作流会将您构建的镜像推送到 Docker Hub。为此，您必须在 GitHub Actions 工作流中使用 Docker 凭据（用户名和访问令牌）进行身份验证。

有关如何创建 Docker 访问令牌的说明，请参阅[创建和管理访问令牌](/manuals/security/access-tokens.md)。

准备好 Docker 凭据后，将这些凭据添加到您的 GitHub 仓库中，以便在 GitHub Actions 中使用：

1. 打开您仓库的 **Settings**（设置）。
2. 在 **Security**（安全性）下，转到 **Secrets and variables > Actions**（机密和变量 > Actions）。
3. 在 **Secrets**（机密）下，创建一个名为 `DOCKER_PASSWORD` 的新仓库机密，其中包含您的 Docker 访问令牌。
4. 接下来，在 **Variables**（变量）下，创建一个名为 `DOCKER_USERNAME` 的仓库变量，其中包含您的 Docker Hub 用户名。

## 设置您的 GitHub Actions 工作流

GitHub Actions 工作流定义了一系列步骤，用于自动执行任务，例如在提交或拉取请求等触发器响应时构建和推送 Docker 镜像。在本指南中，工作流侧重于自动化 Docker 构建和测试，确保您的容器化应用程序在发布之前能够正常工作。

在仓库的 `.github/workflows/` 目录中创建一个名为 `docker-ci.yml` 的文件。从基本的工作流配置开始：

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
```

此配置会在推送到 main 分支和拉取请求时运行工作流。通过包含这两个触发器，您可以确保镜像在合并之前为拉取请求正确构建。

## 为标签和注解提取元数据

对于工作流中的第一步，请使用 `docker/metadata-action` 为您的镜像生成元数据。此操作会提取有关 Git 仓库的信息，例如分支名称和提交 SHA，并生成镜像元数据，例如标签和注解。

将以下 YAML 添加到您的工作流文件中：

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

这些步骤会在构建和推送过程中为镜像准备用于标记和注解的元数据。

- **Checkout** 步骤会克隆 Git 仓库。
- **Extract Docker image metadata** 步骤会提取 Git 元数据，并为 Docker 构建生成镜像标签和注解。

## 向您的注册表进行身份验证

在构建镜像之前，向您的注册表进行身份验证，以确保您可以将构建的镜像推送到注册表。

要与 Docker Hub 进行身份验证，请将以下步骤添加到您的工作流中：

```yaml
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

此步骤使用[在仓库设置中配置的 Docker 凭据](#configure-your-github-repository)。

## 构建并推送镜像

最后，构建最终的生产镜像并将其推送到您的注册表。以下配置会构建镜像并将其直接推送到注册表。

```yaml
      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

在此配置中：

- `push: ${{ github.event_name != 'pull_request' }}` 确保仅在事件不是拉取请求时才推送镜像。这样，工作流会为拉取请求构建和测试镜像，但仅为推送到 main 分支的提交推送镜像。
- `tags` 和 `annotations` 使用元数据操作的输出，自动为镜像应用一致的标签和[注解](/manuals/build/metadata/annotations.md)。

## 证明

SBOM（软件物料清单）和来源证明可以提高安全性和可追溯性，确保您的镜像符合现代软件供应链的要求。

只需进行少量额外配置，您就可以配置 `docker/build-push-action` 在构建时为镜像生成软件物料清单 (SBOM) 和来源证明。

要生成此额外元数据，您需要对工作流进行两项更改：

- 在构建步骤之前，添加一个使用 `docker/setup-buildx-action` 的步骤。此操作会使用默认客户端不支持的其他功能来配置您的 Docker 构建客户端。
- 然后，更新 **Build and push Docker image** 步骤，以同时启用 SBOM 和来源证明。

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

有关证明的更多详细信息，请参阅[文档](/manuals/build/metadata/attestations/_index.md)。

## 结论

通过前面部分概述的所有步骤，以下是完整的工作流配置：

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

此工作流实现了使用 GitHub Actions 构建和推送 Docker 镜像的最佳实践。此配置可以直接使用，也可以根据项目的需求扩展其他功能，例如[多平台](/manuals/build/building/multi-platform.md)。

### 延伸阅读

- 在 [Docker Build GitHub Actions](/manuals/build/ci/github-actions/_index.md) 部分了解有关高级配置和示例的更多信息。
- 对于更复杂的构建设置，您可能需要考虑 [Bake](/manuals/build/bake/_index.md)。（另请参阅[精通 Buildx Bake 指南](/guides/bake/index.md)。）
- 了解 Docker 托管的构建服务，旨在实现更快、多平台的构建，请参阅 [Docker Build Cloud](/guides/docker-build-cloud/_index.md)。
