# 使用 Docker GitHub Builder 执行 Bake


[`bake.yml` 可复用工作流](https://github.com/docker/github-builder?tab=readme-ov-file#bake-reusable-workflow)
基于 [Bake 定义](../../../bake/_index.md) 而非一组 Dockerfile 输入进行构建。
本页介绍如何针对某个 target 调用该工作流、如何传入 Bake overrides 和变量，
以及当 Bake 文件已是构建的单一事实来源时，如何导出本地输出。

## Build and push a Bake target

下面的工作流从 `docker-bake.hcl` 构建 `image` target，
并使用从[元数据输入](../manage-tags-labels.md)生成的标签来发布结果：

```yaml
name: ci

on:
  push:
    branches:
      - "main"
    tags:
      - "v*"
  pull_request:

permissions:
  contents: read

jobs:
  bake:
    uses: docker/github-builder/.github/workflows/bake.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: image
      push: ${{ github.event_name != 'pull_request' }}
      target: image
      meta-images: name/app
      meta-tags: |
        type=ref,event=branch
        type=ref,event=pr
        type=semver,pattern={{version}}
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

Bake 工作流每次工作流调用只构建一个 target。组（groups）和多 target 构建不受支持，
因为 [SLSA provenance](../attestations.md)、digest 处理以及 manifest 创建都限定在单个 target 范围内。

工作流会在构建开始前校验定义，并从你在 `files` 中传入的文件解析 target。
runner 选择与 Build 工作流使用相同的 `runner` 输入。在默认映射不足时，
设置一个 GitHub 托管的 Linux runner 标签或平台映射。详见
[runner selection](architecture.md#runner-selection)。

## Override target values and variables

由于工作流将构建委托给 Bake，你可以继续使用 `set` 和 `vars` 进行 target 级别的覆盖：

```yaml
name: ci

on:
  push:
    branches:
      - "main"

permissions:
  contents: read

jobs:
  bake:
    uses: docker/github-builder/.github/workflows/bake.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: image
      push: true
      target: image
      vars: |
        IMAGE_TAG=${{ github.sha }}
      set: |
        *.args.BUILD_RUN_ID=${{ github.run_id }}
        *.platform=linux/amd64,linux/arm64
      cache: true
      cache-scope: image
      meta-images: name/app
      meta-tags: |
        type=sha
      set-meta-annotations: true
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

这种形式适合已经使用 Bake groups、target 继承以及变量展开的仓库。可复用工作流会负责
Buildx 设置、[GitHub Actions 缓存导出](../../../cache/backends/gha.md)、
[Provenance 默认值](../../../metadata/attestations/slsa-provenance.md)、
签名行为以及最终的多平台 manifest。元数据标签和注解可以合并进 Bake 定义中，
无需在你的工作流中额外添加独立的元数据步骤。

## Export local output from Bake

如果 target 应导出文件而非发布镜像，将工作流输出切换为 `local` 并上传产物：

```yaml
name: ci

on:
  pull_request:

permissions:
  contents: read

jobs:
  bake:
    uses: docker/github-builder/.github/workflows/bake.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: local
      target: binaries
      artifact-upload: true
      artifact-name: bake-output
```

使用 `output: local` 时，工作流会将匹配的本地输出覆盖项注入 Bake 运行，
并在各平台构建完成后合并已上传的产物。如果你需要一个保留在普通作业中的手动 Bake 模式，
请参阅 [Multi-platform image](../multi-platform.md)。如果你的构建不需要
Bake 定义，请改用 [build.yml](build.md)。

