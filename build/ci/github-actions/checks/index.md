# 使用 GitHub Actions 验证构建配置


[Build checks](/manuals/build/checks.md) 让你能够在不实际运行构建的情况下验证 `docker build`
配置。

## Run checks with `docker/build-push-action`

要在 GitHub Actions 工作流中使用 `build-push-action` 运行构建检查，请将 `call` 输入参数设为 `check`。
设置后，如果发现构建配置存在任何检查警告，工作流将失败。

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
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Validate build configuration
        uses: docker/build-push-action@v7
        with:
          call: check

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
```

## Run checks with `docker/bake-action`

如果你使用 Bake 和 `docker/bake-action` 来运行构建，则无需在 GitHub Actions 工作流配置中指定任何
特殊输入。相反，定义一个调用 `check` 方法的 Bake target，并在你的 CI 中调用该 target。

```hcl
target "build" {
  dockerfile = "Dockerfile"
  args = {
    FOO = "bar"
  }
}
target "validate-build" {
  inherits = ["build"]
  call = "check"
}
```

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

      - name: Validate build configuration
        uses: docker/bake-action@v7
        with:
          targets: validate-build

      - name: Build
        uses: docker/bake-action@v7
        with:
          targets: build
          push: true
```

### Using the `call` input directly

你也可以设置 `call` 输入来指定构建方法，这等同于在使用 `docker buildx bake` 时传入 `--call` 标志。

例如，要在不于 Bake 文件中定义 `call` 的情况下运行检查：

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

      - name: Validate build configuration
        uses: docker/bake-action@v7
        with:
          targets: build
          call: check
```

