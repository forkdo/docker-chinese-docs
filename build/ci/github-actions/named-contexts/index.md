# 在 GitHub Actions 中使用命名上下文


你可以定义[额外的构建上下文](/reference/cli/docker/buildx/build/#build-context)，
并在 Dockerfile 中通过 `FROM name` 或 `--from=name` 访问它们。当 Dockerfile 定义了同名阶段时，
该阶段会被覆盖。

在 GitHub Actions 中，这对于复用其他构建的结果，或在你的工作流中将某个镜像固定到特定标签很有用。

## Pin image to a tag

用固定版本的镜像替换 `alpine:latest`：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://alpine:3.23
          tags: myimage:latest
```

## Use image in subsequent steps

默认情况下，[Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)
action 使用 `docker-container` 作为构建驱动，因此构建出的 Docker 镜像不会自动加载。

借助命名上下文，你可以复用已构建的镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          driver: docker

      - name: Build base image
        uses: docker/build-push-action@v7
        with:
          context: "{{defaultContext}}:base"
          load: true
          tags: my-base-image:latest

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://my-base-image:latest
          tags: myimage:latest
```

## Using with a container builder

如上一节所示，在使用命名上下文构建时我们并没有使用默认的
[`docker-container` driver](../../builders/drivers/docker-container.md)。这是因为该驱动由于隔离性
无法从 Docker 存储中加载镜像。要解决这个问题，你可以使用[本地注册表](local-registry.md)
在工作流中推送你的基础镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:3
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          # network=host driver-opt needed to push to local registry
          driver-opts: network=host

      - name: Build base image
        uses: docker/build-push-action@v7
        with:
          context: "{{defaultContext}}:base"
          tags: localhost:5000/my-base-image:latest
          push: true

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://localhost:5000/my-base-image:latest
          tags: myimage:latest
```

