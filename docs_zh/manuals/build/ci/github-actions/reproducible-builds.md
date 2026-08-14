---
title: 在 GitHub Actions 中构建可复现的镜像
linkTitle: 可复现构建
description: 如何在 GitHub Actions 中使用 SOURCE_EPOCH 环境变量创建可复现构建
keywords: build, buildx, github actions, ci, gha, reproducible builds, SOURCE_DATE_EPOCH
---

`SOURCE_DATE_EPOCH` 是一个[标准化的环境变量][source_date_epoch]，
用于指示构建工具产生可复现的输出。为构建设置该环境变量后，
镜像索引、配置以及文件元数据中的时间戳都会反映为指定的 Unix 时间。

[source_date_epoch]: https://reproducible-builds.org/docs/source-date-epoch/

要在 GitHub Actions 中设置该环境变量，
可使用构建步骤内置的 `env` 属性。

## Unix epoch timestamps

下面的示例将 `SOURCE_DATE_EPOCH` 变量设置为 0，即 Unix epoch 时间。

{{< tabs group="action" >}}
{{< tab name="`docker/build-push-action`" >}}

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
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: 0
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

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
        uses: docker/bake-action@{{% param "bake_action_version" %}}
        env:
          SOURCE_DATE_EPOCH: 0
```

{{< /tab >}}
{{< /tabs >}}

## Git commit timestamps

下面的示例将 `SOURCE_DATE_EPOCH` 设置为 Git 提交时间戳。

{{< tabs group="action" >}}
{{< tab name="`docker/build-push-action`" >}}

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

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          tags: user/app:latest
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

{{< /tab >}}
{{< tab name="`docker/bake-action`" >}}

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

      - name: Get Git commit timestamps
        run: echo "TIMESTAMP=$(git log -1 --pretty=%ct)" >> $GITHUB_ENV

      - name: Build
        uses: docker/bake-action@{{% param "bake_action_version" %}}
        env:
          SOURCE_DATE_EPOCH: ${{ env.TIMESTAMP }}
```

{{< /tab >}}
{{< /tabs >}}

## Additional information

有关 BuildKit 中 `SOURCE_DATE_EPOCH` 支持的更多信息，
请参阅 [BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch)。
