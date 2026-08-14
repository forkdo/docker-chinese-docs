# 使用 GitHub Actions 添加镜像注解


注解允许你为 OCI 镜像组件（如 manifests、indexes 和 descriptors）指定任意元数据。

要在使用 GitHub Actions 构建镜像时添加注解，可使用 [metadata-action] 自动创建符合 OCI 规范的注解。
metadata action 会创建一个 `annotations` 输出，你可以在 [build-push-action] 和 [bake-action] 中
引用它。

[metadata-action]: https://github.com/docker/metadata-action#overwrite-labels-and-annotations
[build-push-action]: https://github.com/docker/build-push-action/
[bake-action]: https://github.com/docker/bake-action/

**build-push-action**



```yaml {hl_lines=32}
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

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

**bake-action**



```yaml {hl_lines=37}
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

      - name: Build
        uses: docker/bake-action@v7
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file-tags }}
            cwd://${{ steps.meta.outputs.bake-file-annotations }}
          push: true
```



## Configure annotation level

默认情况下，注解会放置在镜像 manifests 上。要配置
[annotation level](../../metadata/annotations.md#specify-annotation-level)，请在
`metadata-action` 步骤上设置 `DOCKER_METADATA_ANNOTATIONS_LEVELS` 环境变量，其值为一个逗号分隔的
列表，包含你想要注解的所有层级。例如，将 `DOCKER_METADATA_ANNOTATIONS_LEVELS` 设为 `index`
会在镜像 index 上生成注解，而不是在 manifests 上。

下面的示例会在镜像 index 和 manifests 上都创建注解。

```yaml {hl_lines=28}
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
        env:
          DOCKER_METADATA_ANNOTATIONS_LEVELS: manifest,index

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

> [!NOTE]
>
> 构建必须生成你想要注解的组件。例如，要注解镜像 index，构建必须生成 index。如果构建
> 只生成了 manifest，而你指定了 `index` 或 `index-descriptor`，构建将会失败。

