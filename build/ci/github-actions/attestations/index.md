# 使用 GitHub Actions 添加 SBOM 与 provenance 证明


软件物料清单（SBOM）与 provenance
[证明（attestations）](../../metadata/attestations/_index.md) 会为你的镜像添加有关其内容以及
构建方式的元数据。

`docker/build-push-action` 的 4 及更高版本支持证明。

## Default provenance

`docker/build-push-action` GitHub Action 会自动向你的镜像添加 provenance 证明，条件如下：

- 如果 GitHub 仓库为公开仓库，则自动向镜像添加 `mode=max` 的 provenance 证明。
- 如果 GitHub 仓库为私有仓库，则自动向镜像添加 `mode=min` 的 provenance 证明。
- 如果你使用的是 [`docker` 导出器](../../exporters/oci-docker.md)，或者你使用 `load: true` 将构建结果
  加载到 runner，则不会向镜像添加任何证明。这些输出格式不支持证明。

> [!WARNING]
>
> 如果你使用 `docker/build-push-action` 为公开 GitHub 仓库中的代码构建镜像，默认附加到镜像上的
> provenance 证明会包含构建参数的值。如果你误用构建参数向构建传递密钥（例如用户凭据或认证令牌），
> 这些密钥就会暴露在 provenance 证明中。请重构你的构建，改用
> [secret 挂载](/reference/cli/docker/buildx/build/#secret) 来传递这些密钥。同时记得轮换你可能已经
> 暴露的任何密钥。

## Max-level provenance

建议你在构建镜像时使用最高级别的 provenance 证明。私有仓库默认只添加 min 级别的 provenance，但你可以
通过在 `docker/build-push-action` GitHub Action 上将 `provenance` 输入设为 `mode=max` 来手动覆盖
provenance 级别。

请注意，为镜像添加证明意味着你必须直接将镜像推送到注册表，而不是将镜像加载到 runner 的本地镜像存储。
这是因为本地镜像存储不支持加载带有证明的镜像。

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

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

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push image
        uses: docker/build-push-action@v7
        with:
          push: true
          provenance: mode=max
          tags: ${{ steps.meta.outputs.tags }}
```

## SBOM

SBOM 证明不会自动添加到镜像。要添加 SBOM 证明，请将 `docker/build-push-action` 的 `sbom` 输入设为 true。

请注意，为镜像添加证明意味着你必须直接将镜像推送到注册表，而不是将镜像加载到 runner 的本地镜像存储。
这是因为本地镜像存储不支持加载带有证明的镜像。

```yaml
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

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

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build and push image
        uses: docker/build-push-action@v7
        with:
          sbom: true
          push: true
          tags: ${{ steps.meta.outputs.tags }}
```

