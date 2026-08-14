---
title: 使用 GitHub Actions 在推送前进行测试
linkTitle: 推送前测试
description: 这里介绍了如何在将镜像推送到注册表之前对其进行验证
keywords: ci, github actions, gha, buildkit, buildx, test
---

在某些情况下，你可能希望在推送镜像之前先验证其是否按预期工作。下面的工作流通过多个步骤来实现这一点：

1. 构建并将镜像导出到 Docker
2. 测试你的镜像
3. 进行多平台构建并推送镜像

```yaml
name: ci

on:
  push:

env:
  TEST_TAG: user/app:test
  LATEST_TAG: user/app:latest

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@{{% param "setup_qemu_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Build and export to Docker
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          load: true
          tags: ${{ env.TEST_TAG }}

      - name: Test
        run: |
          docker run --rm ${{ env.TEST_TAG }}

      - name: Build and push
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ env.LATEST_TAG }}
```

> [!NOTE]
>
> 此工作流中 `linux/amd64` 镜像只构建一次。镜像会被构建一次，后续步骤会复用第一个
> `Build and push` 步骤的内部缓存。第二个 `Build and push` 步骤只构建 `linux/arm64`。
