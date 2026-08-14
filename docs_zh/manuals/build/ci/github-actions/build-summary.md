---
title: GitHub Actions 构建摘要
linkTitle: 构建摘要
description: 通过 GitHub Actions 概览你的 Docker 构建
keywords: github actions, gha, build, summary, annotation
---

Docker 用于构建和推送镜像的 GitHub Actions 会为你的构建生成一份作业摘要，概述执行过程与所用材料：

- 显示所用 Dockerfile、构建时长以及缓存利用率的摘要
- 构建的输入项，如构建参数、标签、标注以及构建上下文
- 对于使用 [Bake](../../bake/_index.md) 的构建，显示该构建的完整 bake 定义

![A GitHub Actions build summary](../images/gha_build_summary.png)

如果你使用以下版本的 [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)
或 [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)
GitHub Actions，Docker 构建的作业摘要会自动出现：

- `docker/build-push-action@{{% param "build_push_action_version" %}}`
- `docker/bake-action@{{% param "bake_action_version" %}}`

要查看作业摘要，在作业完成后打开 GitHub 中该作业的详情页。无论构建成功还是失败，摘要都可用。
在构建失败的情况下，摘要还会显示导致构建失败的错误信息：

![Builds summary error message](../images/build_summary_error.png)

## Import build records to Docker Desktop

作业摘要包含一个用于下载本次运行的构建记录归档的链接。构建记录归档是一个 ZIP 文件，包含一次构建
（如果你使用 `docker/bake-action` 构建了多个 target，则为多次构建）的详细信息。你可以将此构建记录
归档导入 Docker Desktop，从而通过 [Docker Desktop **Builds** 视图](/manuals/desktop/use-desktop/builds.md)
获得一个强大的图形界面，用于进一步分析构建性能。

要将构建记录归档导入 Docker Desktop：

1. 下载并安装 [Docker Desktop](/get-started/get-docker.md)。

2. 从 GitHub Actions 的作业摘要中下载构建记录归档。

3. 打开 Docker Desktop 中的 **Builds** 视图。

4. 选择 **Import build** 按钮，然后浏览到你下载的 `.zip` 作业摘要归档。或者，在打开导入构建对话框后，
   你也可以将构建记录归档 ZIP 文件拖放到 Docker Desktop 窗口中。

5. 选择 **Import** 以添加构建记录。

几秒钟后，来自 GitHub Actions 运行的构建会出现在 Builds 视图的 **Completed builds** 标签页下。
要检查某次构建并查看所有输入、结果、构建步骤以及缓存利用率的详细视图，请在列表中选择该项。

## Disable job summary

要禁用作业摘要，请在构建步骤的 YAML 配置中设置 `DOCKER_BUILD_SUMMARY` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        env:
          DOCKER_BUILD_SUMMARY: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## Disable build record upload

要禁用将构建记录归档上传到 GitHub，请在构建步骤的 YAML 配置中设置
`DOCKER_BUILD_RECORD_UPLOAD` 环境变量：

```yaml {hl_lines=4}
      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

在此配置下，构建摘要仍会生成，但不再包含下载构建记录归档的链接。

## Limitations

目前构建摘要不支持以下情况：

- 托管在 GitHub Enterprise Server 上的仓库。摘要只能在托管于 GitHub.com 的仓库中查看。
