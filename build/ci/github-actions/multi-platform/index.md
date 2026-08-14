# 使用 GitHub Actions 构建多平台镜像


你可以使用 `platforms` 选项构建[多平台镜像](../../building/multi-platform.md)，如以下示例所示：

> [!NOTE]
>
> - 有关可用平台的列表，请参阅 [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)
>   action。
> - 如果你需要支持更多平台，可以使用 [Docker Setup QEMU](https://github.com/docker/setup-qemu-action)
>   action 配合 QEMU。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: user/app:latest
```

## Build and load multi-platform images

GitHub Actions runner 的默认 Docker 配置支持构建多平台镜像并将其推送到注册表。但是，它不支持在
构建后将多平台镜像加载到 runner 的本地镜像存储。要在本地加载多平台镜像，你需要为 Docker Engine
启用 containerd 镜像存储选项。

无法直接配置 GitHub Actions runner 中的默认 Docker 配置，但你可以使用 `docker/setup-docker-action`
来为某个作业自定义 Docker Engine 和 CLI 设置。

下面的示例工作流启用了 containerd 镜像存储，构建一个多平台镜像，并将结果加载到 GitHub runner 的
本地镜像存储。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker
        uses: docker/setup-docker-action@v5
        with:
          daemon-config: |
            {
              "debug": true,
              "features": {
                "containerd-snapshotter": true
              }
            }

      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          platforms: linux/amd64,linux/arm64
          load: true
          tags: user/app:latest
```

## Distribute build across multiple runners

在同一台 runner 上构建多个平台会显著延长构建时间，尤其是在处理复杂 Dockerfile 或大量目标平台时。
如果你希望在不自行维护自定义矩阵与合并作业的情况下，将平台构建分散到多个 runner 上，请使用
[Docker GitHub Builder](github-builder/_index.md)。这些可复用工作流会计算逐平台矩阵，在每个平台
各自的 runner 上运行，并为你创建最终的 manifest。

下面的工作流使用 [`build.yml` 可复用工作流](github-builder/build.md)
来分发一个多平台 Dockerfile 构建：

```yaml
name: ci

on:
  push:

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
      push: true
      platforms: linux/amd64,linux/arm64
      meta-images: user/app
      meta-tags: |
        type=ref,event=branch
        type=ref,event=pr
        type=semver,pattern={{version}}
        type=semver,pattern={{major}}.{{minor}}
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

使用默认开启的 `distribute: true`，工作流会将构建拆分为每个 runner 一个平台，并在其 finalize 阶段
组装最终的多平台镜像。默认的 `runner` 映射将 Linux Arm 平台发送到 `ubuntu-24.04-arm`，其他平台使用
`ubuntu-24.04`。要自定义该映射，请参阅
[runner selection](github-builder/architecture.md#runner-selection)。如果你需要直接控制 Docker 构建
输入，请参阅 [Build with Docker GitHub Builder build.yml](github-builder/build.md)。

### With Bake

当你的构建定义在 Bake 文件中时，可以使用 [`bake.yml` 可复用工作流](github-builder/bake.md) 实现
相同模式。该工作流从 Bake 定义中读取目标平台，分发逐平台构建，并在无需单独的准备或合并作业的情况下
发布最终 manifest。

```hcl
variable "DEFAULT_TAG" {
  default = "app:local"
}

// Special target: https://github.com/docker/metadata-action#bake-definition
target "docker-metadata-action" {
  tags = ["${DEFAULT_TAG}"]
}

// Default target if none specified
group "default" {
  targets = ["image-local"]
}

target "image" {
  inherits = ["docker-metadata-action"]
}

target "image-local" {
  inherits = ["image"]
  output = ["type=docker"]
}

target "image-all" {
  inherits = ["image"]
  platforms = [
    "linux/amd64",
    "linux/arm/v6",
    "linux/arm/v7",
    "linux/arm64"
  ]
}
```

```yaml
name: ci

on:
  push:

permissions:
  contents: read

jobs:
  bake:
    uses: docker/github-builder/.github/workflows/bake.yml@v1
    permissions:
      contents: read
      id-token: write
    with:
      output: image
      push: true
      target: image-all
      meta-images: user/app
      meta-tags: |
        type=ref,event=branch
        type=sha
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

