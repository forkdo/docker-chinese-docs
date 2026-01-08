---
title: Compose 构建规范
description: 了解 Compose 构建规范
keywords: compose, compose 规范, compose 文件参考, compose 构建规范
aliases: 
 - /compose/compose-file/build/
weight: 130
---

{{% include "compose/build.md" %}}

在前一种情况下，整个路径被用作 Docker 上下文来执行 Docker 构建，在目录根目录查找标准的 `Dockerfile`。路径可以是绝对路径或相对路径。如果是相对路径，它会从包含 Compose 文件的目录解析。如果是绝对路径，该路径会阻止 Compose 文件的可移植性，因此 Compose 会显示警告。

在后一种情况下，可以指定构建参数，包括替代的 `Dockerfile` 位置。路径可以是绝对路径或相对路径。如果是相对路径，它会从包含 Compose 文件的目录解析。如果是绝对路径，该路径会阻止 Compose 文件的可移植性，因此 Compose 会显示警告。

## 使用 `build` 和 `image`

当 Compose 面对服务的 `build` 子部分和 `image` 属性时，它遵循 [`pull_policy`](services.md#pull_policy) 属性定义的规则。

如果服务定义中缺少 `pull_policy`，Compose 会首先尝试拉取镜像，然后如果在注册表或平台缓存中找不到镜像，则从源代码构建。

## 发布构建的镜像

支持 `build` 的 Compose 提供了一个将构建的镜像推送到注册表的选项。这样做时，它不会尝试推送没有 `image` 属性的服务镜像。Compose 会警告你缺少 `image` 属性，这会阻止镜像被推送。

## 示例说明

以下示例通过一个具体的示例应用程序说明了 Compose 构建规范的概念。该示例是非规范性的。

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp

  backend:
    image: example/database
    build:
      context: backend
      dockerfile: ../backend.Dockerfile

  custom:
    build: ~/custom
```

当用于从源代码构建服务镜像时，Compose 文件创建三个 Docker 镜像：

* `example/webapp`：使用 Compose 文件夹中的 `webapp` 子目录作为 Docker 构建上下文构建 Docker 镜像。如果该文件夹中缺少 `Dockerfile`，则返回错误。
* `example/database`：使用 Compose 文件夹中的 `backend` 子目录构建 Docker 镜像。`backend.Dockerfile` 文件用于定义构建步骤，该文件在上下文路径中搜索，这意味着 `..` 解析为 Compose 文件夹，因此 `backend.Dockerfile` 是一个同级文件。
* 使用用户 `$HOME` 中的 `custom` 目录作为 Docker 上下文构建 Docker 镜像。Compose 显示关于用于构建镜像的非便携式路径的警告。

在推送时，`example/webapp` 和 `example/database` Docker 镜像都被推送到默认注册表。`custom` 服务镜像被跳过，因为没有设置 `image` 属性，Compose 显示关于此缺失属性的警告。

## 属性

`build` 子部分定义了 Compose 用于从源代码构建 Docker 镜像的配置选项。
`build` 可以指定为包含构建上下文路径的字符串，也可以指定为详细结构：

使用字符串语法，只能配置构建上下文，可以是：
- Compose 文件夹的相对路径。此路径必须是目录，且必须包含 `Dockerfile`

  ```yml
  services:
    webapp:
      build: ./dir
  ```

- Git 仓库 URL。Git URL 在其片段部分接受上下文配置，由冒号 (`:`) 分隔。
第一部分表示 Git 检出的引用，可以是分支、标签或远程引用。
第二部分表示仓库中用作构建上下文的子目录。

  ```yml
  services:
    webapp:
      build: https://github.com/mycompany/example.git#branch_or_tag:subdirectory
  ```

或者 `build` 可以是一个对象，其字段定义如下：

### `additional_contexts`

{{< summary-bar feature_name="构建附加上下文" >}}

`additional_contexts` 定义了镜像构建器在构建镜像时应使用的命名上下文列表。

`additional_contexts` 可以是映射或列表：

```yml
build:
  context: .
  additional_contexts:
    - resources=/path/to/resources
    - app=docker-image://my-app:latest
    - source=https://github.com/myuser/project.git
```

```yml
build:
  context: .
  additional_contexts:
    resources: /path/to/resources
    app: docker-image://my-app:latest
    source: https://github.com/myuser/project.git
```

当用作列表时，语法遵循 `NAME=VALUE` 格式，其中 `VALUE` 是字符串。除此之外的验证是镜像构建器的责任（并且是构建器特定的）。Compose 至少支持绝对和相对路径到目录以及 Git 仓库 URL，就像 [context](#context) 一样。其他上下文类型必须以前缀 `type://` 为前缀以避免歧义。

如果镜像构建器不支持附加上下文，Compose 会警告你，并可能列出未使用的上下文。

有关 [`docker buildx build --build-context`](https://github.com/docker/buildx/blob/master/docs/reference/buildx_build.md#-additional-build-contexts---build-context) 的示例用法，请参阅参考文档。

`additional_contexts` 也可以引用由另一个服务构建的镜像。
这允许服务镜像使用另一个服务镜像作为基础镜像进行构建，并在服务镜像之间共享层。

```yaml
services:
 base:
  build:
    context: .
    dockerfile_inline: |
      FROM alpine
      RUN ...
 my-service:
  build:
    context: .
    dockerfile_inline: |
      FROM base # 为服务 base 构建的镜像
      RUN ...
    additional_contexts:
      base: service:base
```

### `args`

`args` 定义构建参数，即 Dockerfile `ARG` 值。

使用以下 Dockerfile 作为示例：

```Dockerfile
ARG GIT_COMMIT
RUN echo "Based on commit: $GIT_COMMIT"
```

`args` 可以在 Compose 文件的 `build` 键下设置以定义 `GIT_COMMIT`。`args` 可以设置为映射或列表：

```yml
build:
  context: .
  args:
    GIT_COMMIT: cdc3b19
```

```yml
build:
  context: .
  args:
    - GIT_COMMIT=cdc3b19
```

在指定构建参数时可以省略值，在这种情况下，其在构建时的值必须通过用户交互获得，否则在构建 Docker 镜像时不会设置构建参数。

```yml
args:
  - GIT_COMMIT
```

### `cache_from`

`cache_from` 定义了镜像构建器应用于缓存解析的源列表。

缓存位置语法遵循全局格式 `[NAME|type=TYPE[,KEY=VALUE]]`。简单的 `NAME` 实际上是 `type=registry,ref=NAME` 的快捷表示法。

Compose 构建实现可能支持自定义类型，Compose 规范定义了必须支持的规范类型：

- `registry` 从由键 `ref` 设置的 OCI 镜像中检索构建缓存

```yml
build:
  context: .
  cache_from:
    - alpine:latest
    - type=local,src=path/to/cache
    - type=gha
```

不支持的缓存被忽略，不会阻止你构建镜像。

### `cache_to`

`cache_to` 定义了用于与未来构建共享构建缓存的导出位置列表。

```yml
build:
  context: .
  cache_to:
   - user/app:cache
   - type=local,dest=path/to/cache
```

缓存目标使用 [`cache_from`](#cache_from) 定义的相同 `type=TYPE[,KEY=VALUE]` 语法定义。

不支持的缓存被忽略，不会阻止你构建镜像。

### `context`

`context` 定义包含 Dockerfile 的目录路径或 Git 仓库的 URL。

当提供的值是相对路径时，它被解释为相对于项目目录。
Compose 会警告你关于用于定义构建上下文的绝对路径，因为这些路径会阻止 Compose 文件的可移植性。

```yml
build:
  context: ./dir
```

```yml
services:
  webapp:
    build: https://github.com/mycompany/webapp.git
```

如果未显式设置，`context` 默认为项目目录 (`.`)。

### `dockerfile`

`dockerfile` 设置替代的 Dockerfile。相对路径从构建上下文解析。
Compose 会警告你关于用于定义 Dockerfile 的绝对路径，因为它会阻止 Compose 文件的可移植性。

设置时，不允许 `dockerfile_inline` 属性，Compose
拒绝任何同时设置两者的 Compose 文件。

```yml
build:
  context: .
  dockerfile: webapp.Dockerfile
```

### `dockerfile_inline`

{{< summary-bar feature_name="构建内联 Dockerfile" >}}

`dockerfile_inline` 将 Dockerfile 内容定义为 Compose 文件中的内联字符串。设置时，`dockerfile`
属性不允许，Compose 拒绝任何同时设置两者的 Compose 文件。

建议使用 YAML 多行字符串语法来定义 Dockerfile 内容：

```yml
build:
  context: .
  dockerfile_inline: |
    FROM baseimage
    RUN some command
```

### `entitlements`

{{< summary-bar feature_name="构建特权" >}}

`entitlements` 定义了构建期间允许的额外特权。

 ```yaml
 entitlements:
   - network.host
   - security.insecure
 ```

### `extra_hosts`

`extra_hosts` 在构建时添加主机名映射。使用与 [`extra_hosts`](services.md#extra_hosts) 相同的语法。

```yml
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"
```
IPv6 地址可以用方括号括起来，例如：

```yml
extra_hosts:
  - "myhostv6=[::1]"
```

分隔符 `=` 是首选的，但 `:` 也可以使用。在 Docker Compose 版本 [2.24.1](https://github.com/docker/compose/releases/tag/v2.24.1) 中引入。例如：

```yml
extra_hosts:
  - "somehost:162.242.195.82"
  - "myhostv6:::1"
```

Compose 在容器的网络配置中创建匹配的条目，其中包含 IP 地址和主机名，这意味着对于 Linux，`/etc/hosts` 将获得额外的行：

```text
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### `isolation`

`isolation` 指定构建容器的隔离技术。与 [isolation](services.md#isolation) 一样，支持的值是平台特定的。

### `labels`

`labels` 向结果镜像添加元数据。`labels` 可以设置为数组或映射。

建议使用反向 DNS 表示法来防止你的标签与其他软件冲突。

```yml
build:
  context: .
  labels:
    com.example.description: "Accounting webapp"
    com.example.department: "Finance"
    com.example.label-with-empty-value: ""
```

```yml
build:
  context: .
  labels:
    - "com.example.description=Accounting webapp"
    - "com.example.department=Finance"
    - "com.example.label-with-empty-value"
```

### `network`

为构建期间的 `RUN` 指令设置容器连接的网络。

```yaml
build:
  context: .
  network: host
```  

```yaml
build:
  context: .
  network: custom_network_1
```

使用 `none` 在构建期间禁用网络：

```yaml
build:
  context: .
  network: none
```

### `no_cache`

`no_cache` 禁用镜像构建器缓存，并强制从源代码完全重建所有镜像层。这只适用于 Dockerfile 中声明的层，引用的镜像可以在注册表上的标签更新时从本地镜像存储中检索（参见 [pull](#pull)）。

### `platforms`

`platforms` 定义了目标 [平台](services.md#platform) 列表。

```yml
build:
  context: "."
  platforms:
    - "linux/amd64"
    - "linux/arm64"
```

当省略 `platforms` 属性时，Compose 将服务的平台包含在默认构建目标平台列表中。

当定义了 `platforms` 属性时，Compose 包含服务的平台，否则用户将无法运行他们构建的镜像。

Compose 在以下情况下报告错误：
- 当列表包含多个平台但实现无法存储多平台镜像时。
- 当列表包含不支持的平台时。

  ```yml
  build:
    context: "."
    platforms:
      - "linux/amd64"
      - "unsupported/unsupported"
  ```
- 当列表非空且不包含服务的平台时。

  ```yml
  services:
    frontend:
      platform: "linux/amd64"
      build:
        context: "."
        platforms:
          - "linux/arm64"
  ```

### `privileged`

{{< summary-bar feature_name="构建特权" >}}

`privileged` 配置服务镜像以提升的权限构建。支持和实际影响是平台特定的。

```yml
build:
  context: .
  privileged: true
```

### `provenance`

{{< summary-bar feature_name="Compose 来源" >}} 

`provenance` 配置构建器向发布的镜像添加 [来源证明](https://slsa.dev/provenance/v0.2#schema)。 

值可以是布尔值以启用/禁用来源证明，也可以是 key=value 字符串以设置来源配置。你可以通过设置 `mode` 参数来使用此功能选择包含在来源证明中的详细程度。

```yaml
build:
  context: .
  provenance: true
```

```yaml
build:
  context: .
  provenance: mode=max
```

### `pull`

`pull` 要求镜像构建器拉取引用的镜像（Dockerfile 指令中的 `FROM`），即使这些镜像已经存在于本地镜像存储中。

### `sbom`

{{< summary-bar feature_name="Compose sbom" >}}

`sbom` 配置构建器向发布的镜像添加 [来源证明](https://slsa.dev/provenance/v0.2#schema)。 
值可以是布尔值以启用/禁用 sbom 证明，也可以是 key=value 字符串以设置 SBOM 生成器配置。这让你选择替代的 SBOM 生成器镜像（参见 https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md）

```yaml
build:
  context: .
  sbom: true
```

```yaml
build:
  context: .
  sbom: generator=docker/scout-sbom-indexer:latest # 使用替代的 SBOM 生成器
```

### `secrets`

`secrets` 基于每个服务构建授予对由 [secrets](services.md#secrets) 定义的敏感数据的访问权限。支持两种不同的语法变体：简短语法和长语法。

如果机密未在此 Compose 文件的 [`secrets`](secrets.md) 部分中定义，Compose 会报告错误。

#### 简短语法

简短语法变体仅指定机密名称。这授予容器对机密的访问权限，并将其作为只读挂载到容器内的 `/run/secrets/<secret_name>`。源名称和目标挂载点都设置为机密名称。

以下示例使用简短语法授予 `frontend` 服务构建对 `server-certificate` 机密的访问权限。`server-certificate` 的值设置为文件 `./server.cert` 的内容。

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### 长语法

长语法在机密如何在服务的容器内创建方面提供了更多的粒度。

- `source`：机密在平台上的名称。
- `target`：在 Dockerfile 中声明的机密 ID。如果未指定，默认为 `source`。
- `uid` 和 `gid`：服务任务容器中 `/run/secrets/` 内文件的数字 uid 或 gid。默认值为 `USER`。
- `mode`：服务任务容器中 `/run/secrets/` 内挂载文件的 [权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法。
  默认值为可读权限（模式 `0444`）。
  如果设置了可写位，则必须忽略。如果设置了可执行位，则可能被设置。

以下示例将 `server-certificate` 机密文件的名称设置为容器内的 `server.crt`，将模式设置为 `0440`（组可读）并将用户和组设置为 `103`。`server-certificate` 机密的值由平台通过查找提供，其生命周期不由 Compose 直接管理。

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - source: server-certificate
          target: cert # Dockerfile 中的机密 ID
          uid: "103"
          gid: "103"
          mode: 0440
secrets:
  server-certificate:
    external: true
```

```dockerfile
# Dockerfile
FROM nginx
RUN --mount=type=secret,id=cert,required=true,target=/root/cert ...
```

服务构建可能被授予访问多个机密的权限。长语法和短语法可以在同一个 Compose 文件中使用。在顶级 `secrets` 中定义机密不应意味着授予任何服务构建对其的访问权限。
这种授权必须在服务规范中明确说明，作为 [secrets](services.md#secrets) 服务元素。

### `ssh`

`ssh` 定义镜像构建器在构建镜像期间应使用的 SSH 身份验证（例如，克隆私有仓库）。

`ssh` 属性语法可以是：
* `default`：让构建器连接到 SSH 代理。
* `ID=path`：ID 和相关路径的键值定义。它可以是 [PEM](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail) 文件，也可以是 ssh-agent 套接字的路径。

```yaml
build:
  context: .
  ssh:
    - default   # 挂载默认 SSH 代理
```
或
```yaml
build:
  context: .
  ssh: ["default"]   # 挂载默认 SSH 代理
```

使用自定义 ID `myproject` 和本地 SSH 密钥路径：
```yaml
build:
  context: .
  ssh:
    - myproject=~/.ssh/myproject.pem
```

然后镜像构建器可以依赖于此在构建期间挂载 SSH 密钥。

例如，[SSH 挂载](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md#run---mounttypessh) 可用于挂载由 ID 设置的 SSH 密钥并访问安全资源：

```console
RUN --mount=type=ssh,id=myproject git clone ...
```

### `shm_size`

`shm_size` 设置为构建 Docker 镜像分配的共享内存（Linux 上的 `/dev/shm` 分区）大小。指定为表示字节数的整数值或表示 [字节值](extension.md#specifying-byte-values) 的字符串。

```yml
build:
  context: .
  shm_size: '2gb'
```

```yaml
build:
  context: .
  shm_size: 10000000
```

### `tags`

`tags` 定义了必须与构建镜像关联的标签映射列表。此列表是 [服务部分中定义的 `image` 属性](services.md#image) 的补充

```yml
tags:
  - "myimage:mytag"
  - "registry/username/myrepos:my-other-tag"
```

### `target`

`target` 定义了在多阶段 `Dockerfile` 内部定义的构建阶段。

```yml
build:
  context: .
  target: prod
```

### `ulimits`

{{< summary-bar feature_name="构建 ulimits" >}}

`ulimits` 覆盖容器的默认 `ulimits`。它被指定为单个限制的整数值或软/硬限制的映射。

```yml
services:
  frontend:
    build:
      context: .
      ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000
```