---
title: 配置你的 GitHub Actions 构建器
linkTitle: BuildKit 配置
description: 在 CI 中配合 GitHub Actions 配置 BuildKit 实例
keywords: ci, github actions, gha, buildkit, buildx
---

本页包含在使用我们的 [Setup Buildx Action](https://github.com/docker/setup-buildx-action) 时
配置 BuildKit 实例的说明。

## Version pinning

默认情况下，该 action 会尝试使用 GitHub Runner（构建客户端）上可用的最新版本
[Buildx](https://github.com/docker/buildx) 以及 [BuildKit](https://github.com/moby/buildkit)
（构建服务端）的最新发布版本。

要固定到特定版本的 Buildx，请使用 `version` 输入。例如，固定到 Buildx v0.10.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
  with:
    version: v0.10.0
```

要固定到特定版本的 BuildKit，请在 `driver-opts` 输入中使用 `image` 选项。例如，固定到 BuildKit v0.11.0：

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
  with:
    driver-opts: image=moby/buildkit:v0.11.0
```

## BuildKit container logs

要在使用 `docker-container` 驱动时显示 BuildKit 容器日志，你必须
[启用步骤调试日志](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging#enabling-step-debug-logging)，
或在 [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action 中
设置 `--debug` buildkitd 标志：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          buildkitd-flags: --debug
      
      - name: Build
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
```

日志会在作业结束时显示：

![BuildKit container logs](images/buildkit-container-logs.png)

## BuildKit Daemon configuration

如果你使用的是 [`docker-container` driver](/manuals/build/builders/drivers/docker-container.md)
（默认），可以通过 `config` 或 `buildkitd-config-inline` 输入为构建器提供一份
[BuildKit 配置](../../buildkit/toml-configuration.md)：

### Registry mirror

你可以使用 `buildkitd-config-inline` 输入，直接在工作流中以内联块的形式配置 registry mirror：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          buildkitd-config-inline: |
            [registry."docker.io"]
              mirrors = ["mirror.gcr.io"]
```

有关使用 registry mirror 的更多信息，请参阅 [Registry mirror](../../buildkit/configure.md#registry-mirror)。

### Max parallelism

你可以限制 BuildKit solver 的并行度，这对于低性能机器尤为有用。

你可以像前面的示例一样使用 `buildkitd-config-inline` 输入，或者如果你愿意，也可以使用
仓库中的专用 BuildKit 配置文件，配合 `config` 输入：

```toml
# .github/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          config: .github/buildkitd.toml
```

## Append additional nodes to the builder

Buildx 支持在多个机器上运行构建。这对于在原生节点上为 QEMU 无法处理的更复杂场景
构建[多平台镜像](../../building/multi-platform.md)很有用。在原生节点上构建通常具有更好的性能，
并允许你将构建分布到多台机器上。

你可以使用 `append` 选项向正在创建的构建器追加节点。它以 YAML 字符串文档的形式接收输入，
以消除与 GitHub Actions 内在相关的限制：你只能在输入字段中使用字符串：

| Name              | Type   | Description                                                                                                                                                                                                   |
| ----------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | String | [节点名称](/reference/cli/docker/buildx/create/#node)。若为空，则为所属构建器的名称加索引号后缀。如果你想在工作流的底层步骤中修改/移除某个节点，设置它会很有用。 |
| `endpoint`        | String | 要添加到构建器的节点的 [Docker context 或 endpoint](/reference/cli/docker/buildx/create/#description)                                                                                        |
| `driver-opts`     | List   | 额外的 [driver 特定选项](/reference/cli/docker/buildx/create/#driver-opt) 列表                                                                                                              |
| `buildkitd-flags` | String | buildkitd 守护进程的 [Flags](/reference/cli/docker/buildx/create/#buildkitd-flags)                                                                                                   |
| `platforms`       | String | 节点的固定 [platforms](/reference/cli/docker/buildx/create/#platform)。若不为空，取值优先于检测到的取值。                                                                                         |

下面是一个使用 [`remote` driver](/manuals/build/builders/drivers/remote.md)
和 [TLS authentication](#tls-authentication) 的远程节点示例：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          driver: remote
          endpoint: tcp://oneprovider:1234
          append: |
            - endpoint: tcp://graviton2:1234
              platforms: linux/arm64
            - endpoint: tcp://linuxone:1234
              platforms: linux/s390x
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.ONEPROVIDER_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.ONEPROVIDER_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.ONEPROVIDER_KEY }}
          BUILDER_NODE_1_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_1_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_1_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
          BUILDER_NODE_2_AUTH_TLS_CACERT: ${{ secrets.LINUXONE_CA }}
          BUILDER_NODE_2_AUTH_TLS_CERT: ${{ secrets.LINUXONE_CERT }}
          BUILDER_NODE_2_AUTH_TLS_KEY: ${{ secrets.LINUXONE_KEY }}
```

## Authentication for remote builders

下面的示例展示了如何处理远程构建器的身份验证，使用 SSH 或 TLS。

### SSH authentication

要使用 [`docker-container` driver](/manuals/build/builders/drivers/docker-container.md)
连接到 SSH endpoint，你必须在 GitHub Runner 上配置好 SSH 私钥与配置：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: graviton2
          private-key: ${{ secrets.SSH_PRIVATE_KEY }}
          private-key-name: aws_graviton2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          endpoint: ssh://me@graviton2
```

### TLS authentication

你也可以使用 remote 驱动[设置一个远程 BuildKit 实例](/manuals/build/builders/drivers/remote.md#example-remote-buildkit-in-docker-container)。
为了便于在工作流中集成，你可以使用环境变量，通过 BuildKit 客户端证书为 `tcp://` 设置身份验证：

- `BUILDER_NODE_<idx>_AUTH_TLS_CACERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_CERT`
- `BUILDER_NODE_<idx>_AUTH_TLS_KEY`

`<idx>` 占位符是节点在节点列表中的位置。

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          driver: remote
          endpoint: tcp://graviton2:1234
        env:
          BUILDER_NODE_0_AUTH_TLS_CACERT: ${{ secrets.GRAVITON2_CA }}
          BUILDER_NODE_0_AUTH_TLS_CERT: ${{ secrets.GRAVITON2_CERT }}
          BUILDER_NODE_0_AUTH_TLS_KEY: ${{ secrets.GRAVITON2_KEY }}
```

## Standalone mode

如果 GitHub Runner 上没有安装 Docker CLI，则会直接调用 Buildx 二进制文件，而不是作为 Docker CLI 插件来调用。
如果你希望在自托管 runner 中使用 `kubernetes` 驱动，这会很有用：

```yaml
name: ci

on:
  push:

jobs:
  buildx:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@{{% param "checkout_action_version" %}}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        with:
          driver: kubernetes
      
      - name: Build
        run: |
          buildx build .
```

## Isolated builders

下面的示例展示了如何为不同的作业选择不同的构建器。

一个可能有用的场景是：你正在使用一个 monorepo，并希望将不同的包指向特定的构建器。例如，
某些包构建时可能特别耗费资源，需要更多算力，或者它们需要配备特定能力或硬件的构建器。

有关远程构建器的更多信息，请参阅 [`remote` driver](/manuals/build/builders/drivers/remote.md)
以及 [append builder nodes example](#append-additional-nodes-to-the-builder)。

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up builder1
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        id: builder1
      
      - name: Set up builder2
        uses: docker/setup-buildx-action@{{% param "setup_buildx_action_version" %}}
        id: builder2
      
      - name: Build against builder1
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          builder: ${{ steps.builder1.outputs.name }}
          target: mytarget1
      
      - name: Build against builder2
        uses: docker/build-push-action@{{% param "build_push_action_version" %}}
        with:
          builder: ${{ steps.builder2.outputs.name }}
          target: mytarget2
```
