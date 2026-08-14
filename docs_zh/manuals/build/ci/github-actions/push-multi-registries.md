---
title: 使用 GitHub Actions 推送到多个注册表
linkTitle: 推送到多个注册表
description: 使用 GitHub Actions 推送到多个注册表
keywords: ci, github actions, gha, buildkit, buildx, registry
---

下面的工作流会连接到 Docker Hub 与 GitHub Container Registry，并将镜像推送到这两个注册表：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@{{% param "login_action_version" %}}
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Login to GitHub Container Registry
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
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            user/app:latest
            user/app:1.0.0
            ghcr.io/user/app:latest
            ghcr.io/user/app:1.0.0
```
