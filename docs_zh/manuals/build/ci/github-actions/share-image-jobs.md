---
title: 在 GitHub Actions 的多个作业间共享构建的镜像
linkTitle: 在作业间共享镜像
description: 在不推送到注册表的情况下在 runner 之间共享镜像
keywords: ci, github actions, gha, buildkit, buildx
---

由于每个作业都在各自独立的 runner 中隔离运行，除使用
[自托管 runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
或 [Docker Build Cloud](/build-cloud) 外，你无法在作业之间使用已构建的镜像。
不过，你可以借助工作流中的 [actions/upload-artifact](https://github.com/actions/upload-artifact)
和 [actions/download-artifact](https://github.com/actions/download-artifact)
这两个 action [在作业之间传递数据](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow)：

> [!NOTE]
>
> 该工作流仅支持单平台镜像，因为 Docker exporter 不支持 manifest 列表。
> 对于多平台镜像，请将镜像推送到注册表。如果后续作业在推送前重新构建镜像，
> 请配置[共享缓存后端](cache.md)以复用先前的构建结果。另请参阅
> [Multi-platform image with GitHub Actions](multi-platform.md)。

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}

      - name: Build and export
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          tags: myimage:latest
          outputs: type=docker,dest=${{ runner.temp }}/myimage.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}/myimage.tar

  use:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}

      - name: Load image
        run: |
          docker load --input ${{ runner.temp }}/myimage.tar
          docker image ls -a
```
