---
title: 使用 GitHub Actions 管理标签和标记
linkTitle: 标签和标记
description: 使用 GitHub Actions 自动为镜像分配标签和标记
keywords: ci, github actions, gha, buildkit, buildx, tags, labels
---

如果你想要"自动"管理标记，并按照 [OCI 镜像格式规范](https://github.com/opencontainers/image-spec/blob/master/annotations.md)
来管理标签，可以在一个专门的设置步骤中完成。下面的工作流
将使用 [Docker Metadata Action](https://github.com/docker/metadata-action)
根据 GitHub Actions 事件和 Git 元数据来处理标签和标记：

```yaml
name: ci

on:
  schedule:
    - cron: "0 10 * * *"
  push:
    branches:
      - "**"
    tags:
      - "v*.*.*"
  pull_request:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Docker meta
        id: meta
        uses: docker/metadata-action@{{% param "metadata_action_version" %}}
        with:
          # list of Docker images to use as base name for tags
          images: |
            name/app
            ghcr.io/username/app
          # generate Docker tags based on the following events/attributes
          tags: |
            type=schedule
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=semver,pattern={{major}}
            type=sha

      - name: Login to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GHCR
        if: github.event_name != 'pull_request'
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          registry: ghcr.io
          username: ${{ github.repository_owner }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@{{% param "setup_qemu_action_version" %}}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Build and push
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```
