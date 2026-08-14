---
title: 创建并构建 Docker Hardened Image
linktitle: 创建并构建镜像
description: 了解如何编写 DHI 定义文件，并使用声明式 YAML 模式构建您自己的 Docker Hardened Image。
keywords: hardened images, DHI, build, yaml, security, sbom, provenance, declarative, catalog, definition file
weight: 26
---

Docker Hardened Images (DHI) 由声明式 YAML 定义文件构建，而非传统的 Dockerfile。单个 YAML 文件精确描述镜像中包含的内容：软件包、用户、环境变量、入口点以及元数据。DHI 构建系统会生成仅包含所需软件包的签名镜像，并附带软件物料清单 (SBOM) 和 SLSA Build Level 3 溯源信息。

本页讲解如何编写 DHI 定义文件、在本地构建镜像，以及使用诸如构建阶段、第三方仓库、文件路径和开发变体等高级模式。

> [!IMPORTANT]
>
> DHI 构建系统从 `dhi.io` 拉取基础镜像和构建工具，因此在构建定义文件之前，必须先向该注册表进行身份验证。登录时请使用您的 Docker ID 凭据（即用于 Docker Hub 的相同用户名和密码）。
>
> 运行 `docker login dhi.io` 进行身份验证。

## DHI 构建与 Dockerfile 的区别

Dockerfile 是一系列命令式指令：`RUN`、`COPY`、`FROM`。DHI 定义文件则是一个声明式规范。您描述镜像的期望状态，由构建系统去推算如何生成它。

每个 DHI 定义都以语法指令开头，该指令告诉 BuildKit 使用哪个 DHI 构建前端。前端是解析和处理 YAML 定义（而非默认 Dockerfile 解析器）的组件：

```yaml
# syntax=dhi.io/build:2-alpine3.23
```

前端版本对应于基础发行版：

| 发行版            | 语法指令                                  |
|-------------------|-------------------------------------------|
| Alpine 3.22       | `# syntax=dhi.io/build:2-alpine3.22`      |
| Alpine 3.23       | `# syntax=dhi.io/build:2-alpine3.23`      |
| Alpine 3.24       | `# syntax=dhi.io/build:2-alpine3.24`      |
| Debian 12 (Bookworm)| `# syntax=dhi.io/build:2-debian12`       |
| Debian 13 (Trixie)| `# syntax=dhi.io/build:2-debian13`        |

DHI 构建系统读取 YAML，从指定的仓库解析软件包，组装文件系统，创建用户账户，设置元数据，并生成签名 OCI 镜像。

## 探索目录作为参考

[DHI 目录仓库](https://github.com/docker-hardened-images/catalog) 基于 Apache 2.0 开源，包含每一个官方镜像定义。研究现有定义是学习不同类型镜像 YAML 模式的最佳方式。

该目录遵循以下目录结构：

```text
catalog/
├── image/
│   ├── alpine-base/
│   │   ├── alpine-3.23/
│   │   │   ├── 3.23.yaml            # 运行时变体
│   │   │   └── 3.23-dev.yaml        # 开发变体
│   │   ├── guides.md
│   │   ├── info.yaml
│   │   ├── logo.svg
│   │   └── overview.md
│   ├── nginx/
│   │   ├── alpine-3.22/
│   │   ├── alpine-3.23/
│   │   │   ├── mainline.yaml
│   │   │   ├── mainline-dev.yaml
│   │   │   ├── stable.yaml
│   │   │   └── stable-dev.yaml
│   │   ├── debian-12/
│   │   ├── debian-13/
│   │   ├── bin/
│   │   ├── guides.md
│   │   ├── info.yaml
│   │   ├── logo.svg
│   │   └── overview.md
│   └── redis/
│       ├── debian-13/
│       │   ├── 8.0.yaml              # 运行时
│       │   ├── 8.0-dev.yaml          # 开发
│       │   ├── 8.0-compat.yaml       # 兼容运行时
│       │   └── 8.0-compat-dev.yaml   # 兼容开发
│       ├── guides.md
│       ├── info.yaml
│       ├── logo.svg
│       └── overview.md
├── chart/
└── package/
```

每个镜像按发行版组织其变体。镜像支持多种变体类型：

- `runtime` 变体是最小化的，通常以非 root 用户运行。
- `dev` 变体添加 shell、包管理器和开发工具。
- 兼容性变体添加了常见的 shell 实用程序，例如 `bash`、`coreutils`、`grep` 和 `sed`，以便与现有工作流配合使用。兼容性镜像在 `runtime` 或 `dev` 变体之外使用 `flavor: compat` 字段。
- 兼容性开发变体将兼容性软件包与开发工具组合在一起。

部分镜像还支持其他风格，例如 `sfw`（软件框架）变体。有关每个镜像可用变体的完整列表，请参阅目录。

## 试一试：构建目录镜像

在编写自己的定义之前，先尝试直接从 GitHub 构建现有的目录镜像：

```console
$ docker buildx build \
    https://raw.githubusercontent.com/docker-hardened-images/catalog/refs/heads/main/image/alpine-base/alpine-3.23/3.23.yaml \
    --sbom=generator=dhi.io/scout-sbom-indexer:1 \
    --provenance=1 \
    --tag my-alpine-base:3.23 \
    --load
```

这将直接从 GitHub 下载定义文件并在本地构建。构建完成后，验证镜像：

```console
$ docker images my-alpine-base
```

要修改镜像，请克隆目录并在本地编辑 YAML 文件：

```console
$ git clone https://github.com/docker-hardened-images/catalog.git
$ cd catalog
```

## YAML 模式参考

以下各节描述 DHI 定义文件中可用的字段。

### 必填字段

每个定义都必须包含以下顶层字段：

| 字段          | 描述                                                       |
|---------------|-----------------------------------------------------------|
| `name`        | 镜像的可读名称。                                          |
| `image`       | 完整的注册表路径，例如 `dhi.io/my-image`。                |
| `variant`     | 镜像变体类型：`runtime` 或 `dev`。                        |
| `tags`        | 镜像标签列表。                                            |
| `platforms`   | 目标架构，例如 `linux/amd64` 和 `linux/arm64`。           |
| `contents`    | 要安装的软件包仓库和软件包。                              |

### 镜像元数据

这些字段为镜像添加元数据：

| 字段          | 描述                                                       |
|---------------|-----------------------------------------------------------|
| `os-release`  | 定义镜像内部的 `/etc/os-release` 内容。                   |
| `annotations` | OCI 镜像注解，例如描述和许可证。                          |
| `dates`       | 发布日期和生命周期结束日期。                              |
| `vars`        | 用于模板化的构建时变量。                                  |
| `flavor`      | 镜像风格修饰符，例如用于兼容性镜像的 `compat`。           |

### 容器配置

这些字段控制容器的运行方式：

| 字段          | 描述                                                       |
|---------------|-----------------------------------------------------------|
| `accounts`    | 用户、组和 `run-as` 用户。                                |
| `environment` | 环境变量。                                                |
| `entrypoint`  | 容器入口点命令。                                          |
| `cmd`         | 默认命令参数。                                            |
| `work-dir`    | 容器内的工作目录。                                        |
| `volumes`     | 卷挂载点。                                                |
| `ports`       | 暴露的网络端口。                                          |
| `paths`       | 要创建的目录、文件和符号链接。                            |

### 高级字段

这些字段支持更复杂的构建模式：

| 字段                 | 描述                                                  |
|----------------------|-------------------------------------------------------|
| `contents.builds`    | 带有 shell 流水线的构建阶段。                         |
| `contents.keyring`   | 第三方软件包仓库的签名密钥。                          |
| `contents.artifacts` | 要包含的预构建 OCI 制品。                             |
| `contents.mappings`  | 用于提高 SBOM 准确性的包 URL (purl) 映射。            |
| `contents.files`     | 从 Git URL 获取并带有校验和的源文件。                 |

## 创建最小化镜像

从最简单的可行定义开始：一个带有非 root 用户的 Alpine 基础镜像。

为您的项目创建一个目录，并添加一个名为 `base.yaml` 的文件：

```yaml
# syntax=dhi.io/build:2-alpine3.23

name: My Base Image
image: my-registry/my-base
variant: runtime
tags:
  - "1.0.0"
  - "1.0"
platforms:
  - linux/amd64
  - linux/arm64

contents:
  repositories:
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/main
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/community
  packages:
    - alpine-baselayout-data
    - busybox
    - ca-certificates-bundle

accounts:
  run-as: nonroot
  users:
    - name: nonroot
      uid: 65532
      gid: 65532
  groups:
    - name: nonroot
      gid: 65532
      members:
        - nonroot

os-release:
  name: Docker Hardened Images (Alpine)
  id: alpine
  version-id: "3.23"
  pretty-name: My Hardened Image
  home-url: https://docker.com/products/hardened-images/
  bug-report-url: https://docker.com/support/

environment:
  SSL_CERT_FILE: /etc/ssl/certs/ca-certificates.crt

annotations:
  org.opencontainers.image.description: A minimal Alpine base image

cmd:
  - /bin/sh
```

在此定义中：

- `contents.repositories` 使用完整的 URL 指向 Alpine 软件包镜像。
- `contents.packages` 列出确切的 Alpine 软件包名称。
- `accounts` 块创建一个 `nonroot` 用户（UID 65532），并将其设置为容器的默认用户。
- `os-release` 块定义了 `/etc/os-release` 中出现的内容。请始终将 `bug-report-url` 与 `home-url` 一起包含。
- `annotations` 块添加了在注册表和 Docker Scout 报告中可见的 OCI 元数据。

构建镜像：

```console
$ docker buildx build . -f base.yaml \
    --sbom=generator=dhi.io/scout-sbom-indexer:1 \
    --provenance=1 \
    --tag my-base:latest \
    --load
```
> [!NOTE]
>
> 规范文件中的 `tags` 字段定义镜像元数据（嵌入在镜像清单中的变体和版本标签）。CLI 上的 `--tag` 标志设置用于推送或加载镜像的 OCI 镜像引用。二者用途不同——规范文件标签描述的是*镜像是什么*，而 CLI 标签决定*镜像存储在哪里*。

## 使用 Debian 基础与第三方仓库

对于需要 Debian 软件包或第三方 APT 仓库的应用程序，请使用 Debian 语法指令。以下示例从官方 Redis APT 仓库构建 Redis 镜像。

创建一个名为 `redis.yaml` 的文件：

```yaml
# syntax=dhi.io/build:2-debian13

name: Redis 8.0.x
image: my-registry/my-redis
variant: runtime
tags:
  - "8.0"
  - "8.0.5"
platforms:
  - linux/amd64
  - linux/arm64

contents:
  repositories:
    - deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb trixie main
  keyring:
    - https://packages.redis.io/gpg
  packages:
    - '!libelogind0'
    - '!mawk'
    - '!original-awk'
    - base-files
    - libpcre2-8-0
    - libssl3t64
    - libstdc++6
    - libsystemd0
    - redis=6:8.0.5-1rl1~trixie1
    - redis-server=6:8.0.5-1rl1~trixie1
    - redis-tools=6:8.0.5-1rl1~trixie1
    - tini
  mappings:
    redis: pkg:deb/redis/redis@6:8.0.5-1rl1~trixie1?os_name=debian&os_version=13
    redis-server: pkg:deb/redis/redis-server@6:8.0.5-1rl1~trixie1?os_name=debian&os_version=13
    redis-tools: pkg:deb/redis/redis-tools@6:8.0.5-1rl1~trixie1?os_name=debian&os_version=13

accounts:
  run-as: nonroot
  users:
    - name: nonroot
      uid: 65532
      gid: 65532
  groups:
    - name: nonroot
      gid: 65532
      members:
        - nonroot

os-release:
  name: Docker Hardened Images (Debian)
  id: debian
  version-id: "13"
  version-codename: trixie
  pretty-name: Docker Hardened Images/Debian GNU/Linux 13 (trixie)
  home-url: https://docker.com/products/hardened-images/
  bug-report-url: https://docker.com/support/

work-dir: /data

environment:
  REDIS_VERSION: 8.0.5

annotations:
  org.opencontainers.image.description: A minimal Redis image
  org.opencontainers.image.licenses: AGPL-3.0-only

entrypoint:
  - /usr/bin/tini
  - --

cmd:
  - redis-server
  - /etc/redis/redis.conf
  - --include
  - /etc/redis/conf.d/*.conf
```

此示例引入了几种模式：

- **第三方仓库**：`repositories` 字段使用 Debian 的 `deb [signed-by=...] URL suite component` 格式表示 APT 源。
- **密钥环**：`keyring` 字段下载用于验证来自第三方仓库软件包的 GPG 密钥。
- **软件包排除**：在软件包名称前加 `!` 可显式排除它。这可防止安装不需要的依赖项。在此例中，`!libelogind0`、`!mawk` 和 `!original-awk` 被排除。
- **Debian 版本固定**：使用完整的 epoch 格式 `redis-server=6:8.0.5-1rl1~trixie1` 来固定确切的软件包版本。
- **SBOM 映射**：`mappings` 字段提供包 URL (purl) 元数据，以便 Docker Scout 能在 SBOM 中准确识别软件。
- **Init 进程**：`entrypoint` 使用 `tini` 作为轻量级 init 进程（PID 1），以处理信号转发和僵尸进程回收。
- **配置包含**：`cmd` 使用 `--include /etc/redis/conf.d/*.conf`，以便 `paths` 节中创建的配置文件在启动时加载。

## 创建路径

使用 `paths` 字段在镜像内部创建目录、带有内联内容的文件和符号链接。以下示例扩展了 Redis 定义，添加了运行所需的路径：

```yaml
paths:
  - type: directory
    path: /var/lib/redis
    uid: 65532
    gid: 65532
    mode: "0755"
  - type: directory
    path: /var/log/redis
    uid: 65532
    gid: 65532
    mode: "0755"
  - type: directory
    path: /run/redis/
    uid: 65532
    gid: 65532
    mode: "0755"
  - type: directory
    path: /data
    uid: 65532
    gid: 65532
    mode: "0755"
  - type: file
    path: /etc/redis/conf.d/docker.conf
    content: |
      daemonize no
      bind 0.0.0.0 -::1
      logfile ""
    uid: 0
    gid: 0
    mode: "0555"
  - type: symlink
    path: /usr/bin/redis-sentinel
    uid: 0
    gid: 0
    source: /usr/bin/redis-check-rdb
```

有三种路径类型可用：

| 类型        | 必填字段                              | 描述                          |
|-------------|---------------------------------------|-------------------------------|
| `directory` | `path`、`uid`、`gid`、`mode`          | 创建一个空目录。              |
| `file`      | `path`、`content`、`uid`、`gid`、`mode` | 创建带有内联内容的文件。      |
| `symlink`   | `path`、`source`、`uid`、`gid`        | 创建符号链接。                |

`mode` 字段使用八进制权限位的字符串表示形式，例如 `"0755"` 表示所有者可读写执行，或 `"0555"` 表示所有人均可读执行。请注意，`file` 类型支持使用 YAML 多行字符串的内联 `content`。

## 添加构建阶段

对于需要在构建期间运行 shell 命令（例如配置文件、创建符号链接或调整权限）的镜像，请使用 `contents.builds` 字段。每个构建阶段都有自己的软件包、命名步骤流水线和输出映射。

以下示例在构建期间配置 Nginx，使其在特权端口之外的非特权端口上运行并禁用服务器令牌：

```yaml
# syntax=dhi.io/build:2-alpine3.23

name: Nginx mainline
image: my-registry/my-nginx
variant: runtime
tags:
  - "1.29"
platforms:
  - linux/amd64
  - linux/arm64

contents:
  repositories:
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/main
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/community
    - http://nginx.org/packages/mainline/alpine/v3.23/main
  keyring:
    - https://nginx.org/keys/nginx_signing.rsa.pub
  packages:
    - alpine-baselayout-data
    - busybox
    - musl-utils
    - nginx=1.29.5-r1
  builds:
    - name: nginx
      contents:
        repositories:
          - https://dl-cdn.alpinelinux.org/alpine/v3.23/main
          - https://dl-cdn.alpinelinux.org/alpine/v3.23/community
          - http://nginx.org/packages/mainline/alpine/v3.23/main
        keyring:
          - https://nginx.org/keys/nginx_signing.rsa.pub
        packages:
          - alpine-baselayout-data
          - bash
          - musl-utils
          - nginx=1.29.5-r1
      pipeline:
        - name: install
          runs: |
            set -eux -o pipefail

            ln -sf /dev/stdout /var/log/nginx/access.log
            ln -sf /dev/stderr /var/log/nginx/error.log

            sed -i "s,listen       80;,listen       8080;," /etc/nginx/conf.d/default.conf
            sed -i "/user  nginx;/d" /etc/nginx/nginx.conf
            sed -i "s,pid        /run/nginx.pid;,pid        /var/run/nginx.pid;," /etc/nginx/nginx.conf
            sed -i '/^http {$/a\    server_tokens off;' /etc/nginx/nginx.conf

            chown -R 65532:65532 /var/cache/nginx
            chmod -R g+w /var/cache/nginx
            chown -R 65532:65532 /etc/nginx
            chmod -R g+w /etc/nginx
            chown -R 65532:65532 /run
            chown -R 65532:65532 /run/lock
            chown -R 65532:65532 /var/run
            chown -R 65532:65532 /var/log/nginx
      outputs:
        - source: /
          target: /
          uid: 0
          gid: 0
          diff: true

accounts:
  run-as: nginx
  users:
    - name: nginx
      uid: 65532
      gid: 65532
  groups:
    - name: nginx
      gid: 65532
      members:
        - nginx
    - name: www-data
      gid: 82

os-release:
  name: Docker Hardened Images (Alpine)
  id: alpine
  version-id: "3.23"
  pretty-name: Docker Hardened Images/Alpine Linux v3.23
  home-url: https://docker.com/products/hardened-images/
  bug-report-url: https://docker.com/support/

environment:
  NGINX_VERSION: 1.29.5-r1

annotations:
  org.opencontainers.image.description: A minimal Nginx image
  org.opencontainers.image.licenses: BSD-2-Clause

entrypoint:
  - nginx

cmd:
  - -g
  - daemon off;

ports:
  - 8080/tcp
```

此定义中的关键模式：

| 元素         | 描述                                                                  |
|--------------|-----------------------------------------------------------------------|
| `contents`   | 每个构建阶段都有自己的 `contents` 节。包含仅构建期间需要的软件包，例如 `bash`。 |
| `pipeline`   | 包含运行 shell 命令的命名步骤。脚本始终以 `set -eux -o pipefail` 开头。 |
| `outputs`    | 将结果从构建阶段复制到最终镜像。设置 `diff: true` 仅复制发生变化的文件，保持镜像最小化。 |
| `accounts`   | Nginx 使用专用的 `nginx` 用户（UID 65532）而非 `nonroot`。同时创建 `www-data` 组（GID 82）以兼容 Web 服务器。 |
| `musl-utils` | 在 Alpine 版 Nginx 镜像的主软件包和构建软件包中都需要。              |

## 使用 OCI 制品作为软件包来源

您可以不从 Alpine 或 Debian 仓库安装软件包，而是从 DHI 软件包制品拉取预构建的二进制文件。目录正是以此方式构建 Python 和 Node.js 等镜像——运行时被单独编译并发布为 OCI 制品，然后在镜像定义中按摘要引用。

在 `contents` 下添加 `artifacts` 字段：

```yaml
contents:
  repositories:
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/main
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/community
  packages:
    - alpine-baselayout-data
    - bzip2
    - ca-certificates-bundle
    - expat
    - gdbm
    - libffi
    - mpdecimal
    - musl
    - ncurses
    - openssl
    - readline
    - sqlite-libs
    - tzdata
    - zlib
  artifacts:
    - name: dhi.io/pkg-python:3.13.12-alpine3.23@sha256:052b3b915055006a27c42470eed5c65d7ee92d2c3de47ecaedcc6bbd36077b95
      includes:
        - opt/**
      uid: 0
      gid: 0
```

| 字段        | 描述                                                                  |
|-------------|-----------------------------------------------------------------------|
| `name`      | 带有摘要固定的完整 OCI 引用。始终使用 `@sha256:` 以保证可重现性。      |
| `includes`  | 从制品提取文件的 Glob 模式。路径从文件系统根解析；`opt/**` 包含 `/opt` 路径下的所有内容。 |
| `excludes`  | 要跳过的文件的 Glob 模式。用于移除头文件、文档或不再使用的二进制文件。 |
| `uid`、`gid`| 提取文件的所有权。                                                    |

可用的 DHI 软件包位于目录仓库的 [`package/`](https://github.com/docker-hardened-images/catalog/tree/main/package) 目录中。

## 创建开发变体

镜像的 dev 变体添加了 shell、包管理器和开发工具。这对于调试以及作为多阶段工作流中的构建阶段非常有用。

要创建 dev 变体，请更改 `variant` 字段并启用 root 访问：

```yaml
# syntax=dhi.io/build:2-alpine3.23

name: Alpine 3.23 Base (dev)
image: my-registry/my-base
variant: dev
tags:
  - "1.0-dev"
platforms:
  - linux/amd64
  - linux/arm64

contents:
  repositories:
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/main
    - https://dl-cdn.alpinelinux.org/alpine/v3.23/community
  packages:
    - alpine-baselayout-data
    - apk-tools
    - busybox
    - ca-certificates-bundle

accounts:
  root: true
  run-as: root
  users:
    - name: nonroot
      uid: 65532
      gid: 65532
  groups:
    - name: nonroot
      gid: 65532
      members:
        - nonroot

os-release:
  name: Docker Hardened Images (Alpine)
  id: alpine
  version-id: "3.23"
  pretty-name: Docker Hardened Images/Alpine Linux v3.23
  home-url: https://docker.com/products/hardened-images/
  bug-report-url: https://docker.com/support/

environment:
  SSL_CERT_FILE: /etc/ssl/certs/ca-certificates.crt

annotations:
  org.opencontainers.image.description: A minimal Alpine base image

cmd:
  - /bin/sh
```

与运行时变体的关键区别：

- `variant: dev` 而非 `variant: runtime`。
- `accounts.root: true` 启用 root 账户。
- `run-as: root` 将 root 设为默认用户。
- `apk-tools` 被添加到软件包中，赋予镜像包管理器。
- 仍然定义了 `nonroot` 用户，以便应用程序在运行时切换到无特权用户。

对于基于 Debian 的 dev 变体，请添加 `apt` 而非 `apk-tools`，并包含 `DEBIAN_FRONTEND: noninteractive` 环境变量。

## 创建兼容性变体

兼容性变体包含常见的 shell 实用程序，以便与期望标准 Linux 用户空间的脚本和自动化工具配合使用。兼容性镜像使用 `flavor` 字段：

```yaml
variant: runtime
flavor: compat
```

兼容性变体在应用程序软件包之外添加了 `bash`、`coreutils`、`findutils`、`grep`、`hostname`、`openssl`、`procps` 和 `sed` 等软件包。兼容性开发变体将兼容性软件包与开发工具组合在一起：

```yaml
variant: dev
flavor: compat
```

有关兼容性模式的完整示例，请参阅目录中的 Redis 兼容性镜像。

## 设置端口和卷

使用 `ports` 字段声明容器暴露的端口。当容器以非 root 用户运行时，请始终使用非特权端口（高于 1024）。

```yaml
ports:
  - 8080/tcp
```

使用 `volumes` 字段声明卷挂载点：

```yaml
volumes:
  - /data
```

## 设置注解

OCI 注解为镜像添加机器可读的元数据。使用 `annotations` 字段：

```yaml
annotations:
  org.opencontainers.image.description: A minimal hardened application image
  org.opencontainers.image.licenses: Apache-2.0
```

这些注解会出现在 Docker Scout 报告和容器注册表界面中。

## 构建与验证

### 构建镜像

构建单平台镜像用于本地测试：

```console
$ docker buildx build . -f my-image.yaml \
    --sbom=generator=dhi.io/scout-sbom-indexer:1 \
    --provenance=1 \
    --tag my-image:latest \
    --load
```

### 检查 SBOM

查看生成的软件物料清单：

```console
$ docker scout sbom my-image:latest
```

### 扫描漏洞

针对已知 CVE 数据库检查镜像：

```console
$ docker scout cves my-image:latest
```

### 与未加固镜像比较

针对等效的未加固镜像衡量安全改进：

```console
$ docker scout compare my-image:latest \
    --to <non-hardened-equivalent>:<tag> \
    --platform linux/amd64
```

将 `<non-hardened-equivalent>` 替换为您要比较的 Docker 官方镜像或社区镜像。

### 使用 Docker Debug 检查

验证 os-release 和入口点配置：

```console
$ docker debug my-image:latest
```

输出显示从您的 `os-release` 配置中检测到的发行版名称，并运行入口点 lint 检查。

## 推送到注册表

为镜像打标签并推送到您的容器注册表：

```console
$ docker tag my-image:latest <your-namespace>/my-image:latest
```

```console
$ docker push <your-namespace>/my-image:latest
```

将 `<your-namespace>` 替换为您的 Docker Hub 用户名或组织命名空间。

## 为目录做贡献

Docker Hardened Images 是一个开源项目。您可以通过向 [catalog 仓库](https://github.com/docker-hardened-images/catalog) 提交拉取请求来贡献新的镜像定义或改进现有定义。

要贡献新镜像：

1. Fork 目录仓库。
2. 在 `image/` 下按照命名约定创建目录：`image/<image-name>/<distribution>/`。
3. 添加您的 YAML 定义文件（每个变体一个）。
4. 添加包含显示名称、描述和分类的 `info.yaml`。
5. 添加描述镜像的 `overview.md`。
6. 添加用于镜像图标的 `logo.svg`。
7. 添加带有使用文档的 `guides.md`。
8. 针对 `main` 分支打开拉取请求。

有关更多详细信息，请阅读目录仓库中的 [贡献指南](https://github.com/docker-hardened-images/catalog/blob/main/CONTRIBUTING.md)。
