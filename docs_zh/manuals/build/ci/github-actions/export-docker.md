---
title: 使用 GitHub Actions 导出到 Docker
linkTitle: 导出到 Docker
description: 使用 GitHub Actions 将构建结果加载到镜像存储
keywords: ci, github actions, gha, buildkit, buildx, docker, export, load
---

你可能希望借助 `docker images` 让构建结果在 Docker 客户端中可用，以便在你的工作流另一步骤中使用：

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
      
      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          load: true
          tags: myimage:latest
      
      - name: Inspect
        run: |
          docker image inspect myimage:latest
```
