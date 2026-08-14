# 使用 GitHub Actions 管理缓存


本页包含将缓存存储后端与 GitHub Actions 结合使用的示例。

> [!NOTE]
>
> 有关缓存存储后端的更多细节，请参阅 [Cache storage backends](../../cache/backends/_index.md)。

## Inline cache

在大多数情况下，你会希望使用 [inline cache exporter](../../cache/backends/inline.md)。
但请注意，`inline` 缓存导出器仅支持 `min` 缓存模式。要使用 `max` 缓存模式，需要使用 registry 缓存
导出器配合 `cache-to` 选项分别推送镜像与缓存，如 [registry cache example](#registry-cache) 所示。

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:latest
          cache-to: type=inline
```

## Registry cache

你可以使用 [registry cache exporter](../../cache/backends/registry.md)
从注册表上的缓存 manifest 或（特殊）镜像配置导入/导出缓存。

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

## GitHub cache

### Cache backend API



[GitHub Actions cache exporter](../../cache/backends/gha.md)
后端使用 [GitHub Cache service API](https://github.com/tonistiigi/go-actions-cache)
来获取和上传缓存 blob。这就是为什么你只应在 GitHub Action 工作流中使用此缓存后端，因为 `url`
（`$ACTIONS_RESULTS_URL`）和 `token`（`$ACTIONS_RUNTIME_TOKEN`）属性仅在 workflow 上下文中才会被填充。

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

> [!IMPORTANT]
>
> 自 2025 年 4 月 15 日起，[仅支持 GitHub Cache service API v2。](https://gh.io/gha-cache-sunset) 旧的 v1 API 已经停用。
>
> 如果你在构建过程中遇到以下错误：
>
> ```console
> ERROR: failed to solve: This legacy service is shutting down, effective April 15, 2025. Migrate to the new service ASAP. For more information: https://gh.io/gha-cache-sunset
> ```
>
> 你可能正在使用只支持旧版 GitHub Cache service API v1 的过时工具。根据你的使用场景，以下是你需要升级到的最低版本：
> * Docker Buildx >= v0.21.0
> * BuildKit >= v0.20.0
> * Docker Compose >= v2.33.1
> * Docker Engine >= v28.0.0（如果你使用启用了 containerd 镜像存储的 Docker 驱动进行构建）
>
> 如果你在 GitHub 托管的 runner 上使用 `docker/build-push-action` 或 `docker/bake-action`
> action，Docker Buildx 和 BuildKit 已经是最新版本；但在自托管 runner 上，你可能需要自行更新它们。
> 或者，你可以使用 `docker/setup-buildx-action` action 来安装最新版本的 Docker Buildx：
>
> ```yaml
> - name: Set up Docker Buildx
>   uses: docker/setup-buildx-action@v4
>   with:
>    version: latest
> ```
>
> 如果你使用 Docker Compose 进行构建，可以使用 `docker/setup-compose-action` action：
>
> ```yaml
> - name: Set up Docker Compose
>   uses: docker/setup-compose-action@v2
>   with:
>    version: latest
> ```
>
> 如果你使用启用了 containerd 镜像存储的 Docker Engine 进行构建，可以使用 `docker/setup-docker-action` action：
>
> ```yaml
> -
>   name: Set up Docker
>   uses: docker/setup-docker-action@v5
>   with:
>     version: latest
>     daemon-config: |
>       {
>         "features": {
>           "containerd-snapshotter": true
>         }
>       }
> ```

### Cache mounts

默认情况下，BuildKit 不会在 GitHub Actions 缓存中保留 cache mounts。要将 cache mounts 放入
GitHub Actions 缓存并在多次构建之间复用，可以使用
[`reproducible-containers/buildkit-cache-dance`](https://github.com/reproducible-containers/buildkit-cache-dance)
提供的变通方案。

这个 GitHub Action 会创建临时容器，提取 cache mount 数据并将其注入到你的 Docker 构建步骤中。

下面的示例展示了如何在一个 Go 项目中使用这个变通方案。

`build/package/Dockerfile` 中的示例 Dockerfile

```Dockerfile
FROM golang:1.21.1-alpine as base-build

WORKDIR /build

RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,source=go.mod,target=go.mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    go mod download

RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=bind,target=. \
    go build -o /bin/app ./src
...
```

示例 CI action

```yaml
name: ci

on:
  push:

jobs:
  build:
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

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: user/app
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Go Build Cache for Docker
        uses: actions/cache@v5
        with:
          path: go-build-cache
          key: ${{ runner.os }}-go-build-cache-${{ hashFiles('**/go.sum') }}

      - name: Inject go-build-cache
        uses: reproducible-containers/buildkit-cache-dance@4b2444fec0c0fb9dbf175a96c094720a692ef810 # v2.1.4
        with:
          cache-source: go-build-cache

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          cache-from: type=gha
          cache-to: type=gha,mode=max
          file: build/package/Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64
```

有关此变通方案的更多信息，请参阅
[GitHub 仓库](https://github.com/reproducible-containers/buildkit-cache-dance)。

### Local cache

> [!WARNING]
>
> 目前，旧的缓存条目不会被删除，因此缓存大小 [持续增长](https://github.com/docker/build-push-action/issues/252)。
> 下面的示例使用 `Move cache` 步骤作为变通方案（详见 [`moby/buildkit#1896`](https://github.com/moby/buildkit/issues/1896)）。

你也可以使用 [actions/cache](https://github.com/actions/cache) 与
[local cache exporter](../../cache/backends/local.md)，
借助 [GitHub cache](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
来实现：

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

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Cache Docker layers
        uses: actions/cache@v5
        with:
          path: ${{ runner.temp }}/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=local,src=${{ runner.temp }}/.buildx-cache
          cache-to: type=local,dest=${{ runner.temp }}/.buildx-cache-new,mode=max

      - # Temp fix
        # https://github.com/docker/build-push-action/issues/252
        # https://github.com/moby/buildkit/issues/1896
        name: Move cache
        run: |
          rm -rf ${{ runner.temp }}/.buildx-cache
          mv ${{ runner.temp }}/.buildx-cache-new ${{ runner.temp }}/.buildx-cache
```

