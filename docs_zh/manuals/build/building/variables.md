---
title: 构建变量
linkTitle: 变量
weight: 20
description: 使用构建参数和环境变量配置构建
keywords: build, args, variables, parameters, env, environment variables, config
aliases:
- /build/buildkit/color-output-controls/
- /build/building/env-vars/
- /build/guide/build-args/
---

在 Docker Build 中，构建参数（`ARG`）和环境变量（`ENV`）都是将信息传递给构建过程的
手段。你可以用它们对构建进行参数化，从而实现更灵活、可配置的构建。

> [!WARNING]
>
> 构建参数和环境变量不适合用来向构建传递密钥，因为它们会在最终镜像中暴露。相反，请使用
> secret 挂载或 SSH 挂载，它们能安全地将密钥暴露给构建过程。
>
> 详见 [构建密钥](./secrets.md)。

## 异同点（Similarities and differences）

构建参数和环境变量很相似。它们都在 Dockerfile 中声明，并可以使用 `docker build`
命令的标志进行设置。两者都可用于对构建进行参数化。但它们各自服务于不同的目的。

### 构建参数（Build arguments）

构建参数是 Dockerfile 本身的变量。用它们来参数化 Dockerfile 指令的值。例如，你可能
会使用一个构建参数来指定要安装的依赖版本。

构建参数除非在指令中实际使用，否则对构建没有影响。它们无法在被镜像实例化的容器中
访问或存在，除非显式地从 Dockerfile 传入镜像文件系统或配置。它们可能持久化在镜像
元数据（如来源证明 attestations）和镜像历史中，这就是它们不适合保存密钥的原因。

它们使 Dockerfile 更灵活，也更易于维护。

有关如何使用构建参数的示例，参见 [`ARG` 用法示例](#arg-usage-example)。

### 环境变量（Environment variables）

环境变量会被传递进构建执行环境，并持久化在被镜像实例化的容器中。

环境变量主要用于：

- 配置构建的执行环境
- 为容器设置默认环境变量

环境变量（若已设置）可以直接影响构建的执行，以及应用程序的行为或配置。

你无法在构建时覆盖或设置环境变量。环境变量的值必须在 Dockerfile 中声明。你可以
将环境变量与构建参数结合，以允许在构建时配置环境变量。

有关如何使用环境变量配置构建的示例，参见 [`ENV` 用法示例](#env-usage-example)。

## `ARG` 用法示例（`ARG` usage example）

构建参数通常用于指定所用组件（如镜像变体或软件包版本）的版本。

将版本指定为构建参数，让你可以使用不同版本进行构建，而无需手动更新 Dockerfile。
这也让 Dockerfile 更易于维护，因为它允许你在文件顶部声明版本。

构建参数也可以是在多处复用某个值的一种方式。例如，如果你在构建中使用了多个 `alpine`
变体，可以确保各处使用的是相同版本的 `alpine`：

- `golang:1.22-alpine${ALPINE_VERSION}`
- `python:3.12-alpine${ALPINE_VERSION}`
- `nginx:1-alpine${ALPINE_VERSION}`

以下示例使用构建参数定义了 `node` 和 `alpine` 的版本。

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION="{{% param example_node_version %}}"
ARG ALPINE_VERSION="{{% param example_alpine_version %}}"

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS base
WORKDIR /src

FROM base AS build
COPY package*.json ./
RUN npm ci
RUN npm run build

FROM base AS production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /src/dist/ .
CMD ["node", "app.js"]
```

在此例中，构建参数具有默认值。调用构建时指定它们的值是可选的。要覆盖默认值，
需使用 `--build-arg` CLI 标志：

```console
$ docker build --build-arg NODE_VERSION=current .
```

有关如何使用构建参数的更多信息，请参阅：

- [`ARG` Dockerfile 参考](/reference/dockerfile.md#arg)
- [`docker build --build-arg` 参考](/reference/cli/docker/buildx/build/#build-arg)

## `ENV` 用法示例（`ENV` usage example）

使用 `ENV` 声明环境变量，会使该变量对构建阶段中所有后续指令可用。以下示例展示了
在使用 `npm` 安装 JavaScript 依赖之前，将 `NODE_ENV` 设置为 `production` 的例子。
设置该变量会使 `npm` 省略仅本地开发所需的软件包。

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
WORKDIR /app
COPY package*.json ./
ENV NODE_ENV=production
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

环境变量默认在构建时不可配置。如果你想在构建时更改 `ENV` 的值，可以将环境变量与
构建参数结合：

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
WORKDIR /app
COPY package*.json ./
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

使用此 Dockerfile，你可以用 `--build-arg` 覆盖 `NODE_ENV` 的默认值：

```console
$ docker build --build-arg NODE_ENV=development .
```

注意，由于你设置的环境变量会持久化在容器中，使用它们可能导致应用程序运行时出现
非预期的副作用。

有关如何在构建中使用环境变量的更多信息，请参阅：

- [`ENV` Dockerfile 参考](/reference/dockerfile.md#env)

## 作用域（Scoping）

在 Dockerfile 全局作用域中声明的构建参数不会自动继承到构建阶段中。它们只能在
全局作用域中访问。

```dockerfile
# syntax=docker/dockerfile:1

# 以下构建参数在全局作用域中声明：
ARG NAME="joe"

FROM alpine
# 以下指令无法访问 $NAME 构建参数
# 因为该参数是在全局作用域中定义的，而非针对此阶段。
RUN echo "hello ${NAME}!"
```

此例中的 `echo` 命令求值结果为 `hello !`，因为 `NAME` 构建参数的值超出了作用域。
要将全局构建参数继承到某个阶段，必须消费它们：

```dockerfile
# syntax=docker/dockerfile:1

# 在全局作用域中声明构建参数
ARG NAME="joe"

FROM alpine
# 在构建阶段消费该构建参数
ARG NAME
RUN echo $NAME
```

一旦构建参数在某个阶段被声明或消费，它就会自动被子阶段继承。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# 在构建阶段中声明构建参数
ARG NAME="joe"

# 基于 "base" 创建一个新阶段
FROM base AS build
# NAME 构建参数在此处可用
# 因为它在父阶段中声明
RUN echo "hello $NAME!"
```

下图进一步说明了在多阶段构建中构建参数和环境变量的继承机制。

{{< figure src="../../images/build-variables.svg" class="invertible" >}}

## 预定义构建参数（Pre-defined build arguments）

本节描述默认情况下所有构建都可用的预定义构建参数。

### 多平台构建参数（Multi-platform build arguments）

多平台构建参数描述构建和目标平台的构建与目标平台。

构建平台是构建器（BuildKit 守护进程）所在主机的操作系统、架构和平台变体。

- `BUILDPLATFORM`
- `BUILDOS`
- `BUILDARCH`
- `BUILDVARIANT`

目标平台参数持有为构建指定的目标平台的相同值，使用 `docker build` 命令的
`--platform` 标志指定。

- `TARGETPLATFORM`
- `TARGETOS`
- `TARGETARCH`
- `TARGETVARIANT`

这些参数对于在多平台构建中进行交叉编译很有用。它们在 Dockerfile 的全局作用域中
可用，但不会自动被子构建阶段继承。要在阶段内部使用它们，必须声明它们：

```dockerfile
# syntax=docker/dockerfile:1

# 预定义构建参数在全局作用域中可用
FROM --platform=$BUILDPLATFORM golang
# 要将它们继承到阶段，使用 ARG 声明
ARG TARGETOS
RUN GOOS=$TARGETOS go build -o ./exe .
```

有关多平台构建参数的更多信息，请参阅
[多平台参数](/reference/dockerfile.md#automatic-platform-args-in-the-global-scope)

### 代理参数（Proxy arguments）

代理构建参数让你为构建指定要使用的代理。你无需在 Dockerfile 中声明或引用这些参数。
使用 `--build-arg` 指定一个代理就足以让构建使用该代理。

代理参数默认会自动从构建缓存和 `docker history` 的输出中排除。如果你确实在
Dockerfile 中引用了这些参数，代理配置就会进入构建缓存。

构建器支持以下代理构建参数。这些变量不区分大小写。

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `FTP_PROXY`
- `NO_PROXY`
- `ALL_PROXY`

要为你的构建配置代理：

```console
$ docker build --build-arg HTTP_PROXY=https://my-proxy.example.com .
```

有关代理构建参数的更多信息，请参阅
[代理参数](/reference/dockerfile.md#predefined-args)。

## 构建工具配置变量（Build tool configuration variables）

以下环境变量用于启用、禁用或改变 Buildx 和 BuildKit 的行为。注意，这些变量并非用于
配置构建容器；它们在构建内部不可用，且与 `ENV` 指令无关。它们用于配置 Buildx 客户端
或 BuildKit 守护进程。

| 变量                                                                        | 类型              | 描述                                                      |
|-----------------------------------------------------------------------------|-------------------|------------------------------------------------------------------|
| [BUILDKIT_COLORS](#buildkit_colors)                                         | String            | 配置终端输出的文字颜色。                                        |
| [BUILDKIT_HOST](#buildkit_host)                                             | String            | 指定用于远程构建器的主机。                                      |
| [BUILDKIT_PROGRESS](#buildkit_progress)                                     | String            | 配置进度输出的类型。                                            |
| [BUILDKIT_TTY_LOG_LINES](#buildkit_tty_log_lines)                           | String            | 日志行数（针对 TTY 模式下的活动步骤）。                          |
| [BUILDX_BAKE_FILE](#buildx_bake_file)                                       | String            | 指定 `docker buildx bake` 的构建定义文件。                      |
| [BUILDX_BAKE_FILE_SEPARATOR](#buildx_bake_file_separator)                   | String            | 指定 `BUILDX_BAKE_FILE` 的文件路径分隔符。                     |
| [BUILDX_BAKE_GIT_AUTH_HEADER](#buildx_bake_git_auth_header)                 | String            | 远程 Bake 文件的 HTTP 认证方案。                               |
| [BUILDX_BAKE_GIT_AUTH_TOKEN](#buildx_bake_git_auth_token)                   | String            | 远程 Bake 文件的 HTTP 认证令牌。                               |
| [BUILDX_BAKE_GIT_SSH](#buildx_bake_git_ssh)                                 | String            | 远程 Bake 文件的 SSH 认证。                                   |
| [BUILDX_BUILDER](#buildx_builder)                                           | String            | 指定要使用的构建器实例。                                        |
| [BUILDX_CONFIG](#buildx_config)                                             | String            | 指定配置、状态和日志的位置。                                    |
| [BUILDX_CPU_PROFILE](#buildx_cpu_profile)                                   | String            | 在指定位置生成 `pprof` CPU profile。                          |
| [BUILDX_EXPERIMENTAL](#buildx_experimental)                                 | Boolean           | 开启实验性特性。                                              |
| [BUILDX_GIT_CHECK_DIRTY](#buildx_git_check_dirty)                           | Boolean           | 启用脏 Git 检出检测。                                         |
| [BUILDX_GIT_INFO](#buildx_git_info)                                         | Boolean           | 移除来源证明中的 Git 信息。                                    |
| [BUILDX_GIT_LABELS](#buildx_git_labels)                                     | String \| Boolean | 向镜像添加 Git 来源标签。                                      |
| [BUILDX_MEM_PROFILE](#buildx_mem_profile)                                   | String            | 在指定位置生成 `pprof` 内存 profile。                          |
| [BUILDX_METADATA_PROVENANCE](#buildx_metadata_provenance)                   | String \| Boolean | 自定义包含在元数据文件中的来源信息。                            |
| [BUILDX_METADATA_WARNINGS](#buildx_metadata_warnings)                       | String            | 在元数据文件中包含构建警告。                                    |
| [BUILDX_NO_DEFAULT_ATTESTATIONS](#buildx_no_default_attestations)           | Boolean           | 关闭默认来源证明。                                            |
| [BUILDX_NO_DEFAULT_OCI_ARTIFACT](#buildx_no_default_oci_artifact)           | Boolean           | 默认关闭证明的 OCI artifact 存储。                              |
| [BUILDX_NO_DEFAULT_LOAD](#buildx_no_default_load)                           | Boolean           | 默认关闭向镜像存储加载镜像。                                    |
| [EXPERIMENTAL_BUILDKIT_SOURCE_POLICY](#experimental_buildkit_source_policy) | String            | 指定 BuildKit 源策略文件。                                     |

BuildKit 还支持一些额外的配置参数。请参阅
[BuildKit 内置构建参数](/reference/dockerfile.md#buildkit-built-in-build-args)。

你可以用不同方式表达环境变量的布尔值。例如，`true`、`1` 和 `T` 都求值为真。求值是
使用 Go 标准库中的 `strconv.ParseBool` 函数完成的。详见
[参考文档](https://pkg.go.dev/strconv#ParseBool)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### BUILDKIT_COLORS

更改终端输出的颜色。将 `BUILDKIT_COLORS` 设置为以下格式的 CSV 字符串：

```console
$ export BUILDKIT_COLORS="run=123,20,245:error=yellow:cancel=blue:warning=white"
```

颜色值可以是任意有效的 RGB 十六进制码，或
[BuildKit 预定义颜色](https://github.com/moby/buildkit/blob/master/util/progress/progressui/colors.go)
之一。

按照 [no-color.org](https://no-color.org/) 的建议，将 `NO_COLOR` 设置为任何值都会关闭
彩色输出。

### BUILDKIT_HOST

{{< summary-bar feature_name="Buildkit host" >}}

你使用 `BUILDKIT_HOST` 来指定用作远程构建器的 BuildKit 守护进程地址。这与将地址作为
位置参数传递给 `docker buildx create` 相同。

用法：

```console
$ export BUILDKIT_HOST=tcp://localhost:1234
$ docker buildx create --name=remote --driver=remote
```

如果你同时指定了 `BUILDKIT_HOST` 环境变量和位置参数，则参数优先。

### BUILDKIT_PROGRESS

设置 BuildKit 进度输出的类型。有效值为：

- `auto`（默认）：在交互式终端中自动使用 `tty`，否则使用 `plain`
- `plain`：以简单文本格式顺序显示构建步骤
- `tty`：带有格式化进度条和构建步骤的交互式输出
- `quiet`：抑制进度输出，仅显示错误和最终镜像 ID
- `none`：无进度输出，仅显示错误
- `rawjson`：以原始 JSON 输出构建进度（便于其他工具解析）

用法：

```console
$ export BUILDKIT_PROGRESS=plain
```

### BUILDKIT_TTY_LOG_LINES

你可以通过设置 `BUILDKIT_TTY_LOG_LINES` 为一个数字（默认为 `6`）来更改 TTY 模式下
活动步骤可见的日志行数。

```console
$ export BUILDKIT_TTY_LOG_LINES=8
```

### EXPERIMENTAL_BUILDKIT_SOURCE_POLICY

让你指定一个
[BuildKit 源策略](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#reproducing-the-pinned-dependencies)
文件，用于创建具有固定依赖的可复现构建。

```console
$ export EXPERIMENTAL_BUILDKIT_SOURCE_POLICY=./policy.json
```

示例：

```json
{
  "rules": [
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "docker-image://docker.io/library/alpine:latest"
      },
      "updates": {
        "identifier": "docker-image://docker.io/library/alpine:latest@sha256:4edbd2beb5f78b1014028f4fbb99f3237d9561100b6881aabbf5acce2c4f9454"
      }
    },
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "https://raw.githubusercontent.com/moby/buildkit/v0.10.1/README.md"
      },
      "updates": {
        "attrs": {"http.checksum": "sha256:6e4b94fc270e708e1068be28bd3551dc6917a4fc5a61293d51bb36e6b75c4b53"}
      }
    },
    {
      "action": "DENY",
      "selector": {
        "identifier": "docker-image://docker.io/library/golang*"
      }
    }
  ]
}
```

### BUILDX_BAKE_FILE

{{< summary-bar feature_name="Buildx bake file" >}}

指定 `docker buildx bake` 的一个或多个构建定义文件。

此环境变量提供了 `-f` / `--file` 命令行标志的替代方案。

多个文件可通过系统路径分隔符分隔（Linux/macOS 上为 `:`，Windows 上为 `;`）：

```console
export BUILDX_BAKE_FILE=file1.hcl:file2.hcl
```

或使用由 [BUILDX_BAKE_FILE_SEPARATOR](#buildx_bake_file_separator) 变量定义的自定义分隔符：

```console
export BUILDX_BAKE_FILE_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

如果 `BUILDX_BAKE_FILE` 和 `-f` 标志都设置了，则只使用通过 `-f` 提供的文件。

如果列出的文件不存在或无效，bake 会返回错误。

### BUILDX_BAKE_FILE_SEPARATOR

{{< summary-bar feature_name="Buildx bake file separator" >}}

控制 `BUILDX_BAKE_FILE` 环境变量中文件路径之间使用的分隔符。

如果你的文件路径包含默认分隔符字符，或者你想跨不同平台统一分隔符，这会很有用。

```console
export BUILDX_BAKE_PATH_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

### BUILDX_BAKE_GIT_AUTH_HEADER

{{< summary-bar feature_name="Buildx bake Git auth token" >}}

在使用私有 Git 仓库中的远程 Bake 定义时，设置 HTTP 认证方案。这等效于
[`GIT_AUTH_HEADER` 密钥](./secrets#http-authentication-scheme)，但在加载远程 Bake 文件时
便于 Bake 的起飞前认证。支持的值为 `bearer`（默认）和 `basic`。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_HEADER=basic
```

### BUILDX_BAKE_GIT_AUTH_TOKEN

{{< summary-bar feature_name="Buildx bake Git auth token" >}}

在使用私有 Git 仓库中的远程 Bake 定义时，设置 HTTP 认证令牌。这等效于
[`GIT_AUTH_TOKEN` 密钥](./secrets#git-authentication-for-remote-contexts)，但在加载远程 Bake 文件时
便于 Bake 的起飞前认证。

用法：

```console
$ export BUILDX_BAKE_GIT_AUTH_TOKEN=$(cat git-token.txt)
```

### BUILDX_BAKE_GIT_SSH

{{< summary-bar feature_name="Buildx bake Git SSH" >}}

让你指定要转发给 Bake 的 SSH agent 套接字文件路径列表，用于在使用私有仓库中的远程 Bake 定义时
向 Git 服务器认证。这类似于构建的 SSH 挂载，但在解析构建定义时便于 Bake 的起飞前认证。

通常无需设置此环境变量，因为 Bake 默认会使用 `SSH_AUTH_SOCK` agent 套接字。只有在你想使用一个
不同文件路径的套接字时才需要指定此变量。此变量可以接受使用逗号分隔字符串的多个路径。

用法：

```console
$ export BUILDX_BAKE_GIT_SSH=/run/foo/listener.sock,~/.creds/ssh.sock
```

### BUILDX_BUILDER

覆盖已配置的构建器实例。与 `docker buildx --builder` CLI 标志相同。

用法：

```console
$ export BUILDX_BUILDER=my-builder
```

### BUILDX_CONFIG

你可以使用 `BUILDX_CONFIG` 指定用于构建配置、状态和日志的目录。该目录的查找顺序如下：

- `$BUILDX_CONFIG`
- `$DOCKER_CONFIG/buildx`
- `~/.docker/buildx`（默认）

用法：

```console
$ export BUILDX_CONFIG=/usr/local/etc
```

### BUILDX_CPU_PROFILE

{{< summary-bar feature_name="Buildx CPU profile" >}}

如果指定，Buildx 会在指定位置生成一个 `pprof` CPU profile。

> [!NOTE]
> 此属性仅当你开发 Buildx 时才有用。该 profiling 数据与构建性能分析无关。

用法：

```console
$ export BUILDX_CPU_PROFILE=buildx_cpu.prof
```

### BUILDX_EXPERIMENTAL

启用实验性构建特性。

用法：

```console
$ export BUILDX_EXPERIMENTAL=1
```

### BUILDX_GIT_CHECK_DIRTY

{{< summary-bar feature_name="Buildx Git check dirty" >}}

当设置为 true 时，检查
[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 中源码控制信息的脏状态。

用法：

```console
$ export BUILDX_GIT_CHECK_DIRTY=1
```

### BUILDX_GIT_INFO

{{< summary-bar feature_name="Buildx Git info" >}}

当设置为 false 时，从
[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 中移除源码控制信息。

用法：

```console
$ export BUILDX_GIT_INFO=0
```

### BUILDX_GIT_LABELS

{{< summary-bar feature_name="Buildx Git labels" >}}

根据你构建的镜像的 Git 信息添加来源标签。这些标签为：

- `com.docker.image.source.entrypoint`：Dockerfile 相对于项目根目录的位置
- `org.opencontainers.image.revision`：Git 提交修订
- `org.opencontainers.image.source`：仓库的 SSH 或 HTTPS 地址

示例：

```json
  "Labels": {
    "com.docker.image.source.entrypoint": "Dockerfile",
    "org.opencontainers.image.revision": "5734329c6af43c2ae295010778cd308866b95d9b",
    "org.opencontainers.image.source": "git@github.com:foo/bar.git"
  }
```

用法：

- 设置 `BUILDX_GIT_LABELS=1` 以包含 `entrypoint` 和 `revision` 标签。
- 设置 `BUILDX_GIT_LABELS=full` 以包含所有标签。

如果仓库处于脏状态，`revision` 会获得一个 `-dirty` 后缀。

### BUILDX_MEM_PROFILE

{{< summary-bar feature_name="Buildx mem profile" >}}

如果指定，Buildx 会在指定位置生成一个 `pprof` 内存 profile。

> [!NOTE]
> 此属性仅当你开发 Buildx 时才有用。该 profiling 数据与构建性能分析无关。

用法：

```console
$ export BUILDX_MEM_PROFILE=buildx_mem.prof
```

### BUILDX_METADATA_PROVENANCE

{{< summary-bar feature_name="Buildx metadata provenance" >}}

默认情况下，Buildx 通过 [`--metadata-file` flag](/reference/cli/docker/buildx/build/#metadata-file)
在元数据文件中包含最少的来源信息。此环境变量允许你自定义元数据文件中包含的来源信息：
* `min` 设置最少来源（默认）。
* `max` 设置完整来源。
* `disabled`、`false` 或 `0` 不设置任何来源。

### BUILDX_METADATA_WARNINGS

{{< summary-bar feature_name="Buildx metadata warnings" >}}

默认情况下，Buildx 不会通过
[`--metadata-file` flag](/reference/cli/docker/buildx/build/#metadata-file) 在元数据文件中包含构建警告。
你可以将此环境变量设置为 `1` 或 `true` 来包含它们。

### BUILDX_NO_DEFAULT_ATTESTATIONS

{{< summary-bar feature_name="Buildx no default" >}}

默认情况下，BuildKit v0.11 及更高版本会向你构建的镜像添加
[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。设置 `BUILDX_NO_DEFAULT_ATTESTATIONS=1`
以禁用默认来源证明。

用法：

```console
$ export BUILDX_NO_DEFAULT_ATTESTATIONS=1
```

### BUILDX_NO_DEFAULT_OCI_ARTIFACT

{{< summary-bar feature_name="Buildx no default OCI artifact" >}}

从 BuildKit v0.32.0 开始，当启用 OCI 媒体类型时，BuildKit 将证明存储为 OCI artifact。
设置 `BUILDX_NO_DEFAULT_OCI_ARTIFACT=1` 使 Buildx 在构建使用支持证明的导出器且你未显式设置
`oci-artifact` 导出器属性时，设置 `oci-artifact=false`。

用法：

```console
$ export BUILDX_NO_DEFAULT_OCI_ARTIFACT=1
```

### BUILDX_NO_DEFAULT_LOAD

当你使用 `docker` 驱动构建镜像时，镜像会在构建结束时自动加载到镜像存储。设置
`BUILDX_NO_DEFAULT_LOAD` 以禁用镜像到本地容器存储的自动加载。

用法：

```console
$ export BUILDX_NO_DEFAULT_LOAD=1
```

<!-- vale Docker.HeadingSentenceCase = YES -->