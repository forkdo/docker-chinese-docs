---
---
linkTitle: Services
title: Define services in Docker Compose
description: Explore all the attributes the services top-level element can have.
weight: 20
keywords: "compose, compose specification, services, compose file reference"
aliases:
  - /compose/compose-file/05-services/---
linkTitle: 服务
title: 在 Docker Compose 中定义服务
description: 探索服务顶层元素可以拥有的所有属性。
weight: 20---
{{% include "compose/services.md" %}}

Compose 文件必须声明一个 `services` 顶层元素，其键是服务名称的字符串表示，其值是服务定义。服务定义包含应用于每个服务容器的配置。

每个服务还可以包含一个 `build` 部分，该部分定义如何为服务创建 Docker 镜像。Compose 支持使用此服务定义构建 Docker 镜像。如果未使用，则 `build` 部分将被忽略，并且 Compose 文件仍然被视为有效。构建支持是 Compose 规范的一个可选方面，在 [Compose 构建规范](build.md) 文档中有详细描述。

每个服务都定义了运行其容器的运行时约束和需求。`deploy` 部分将这些约束分组，并允许平台调整部署策略，以最佳地匹配容器需求与可用资源。部署支持是 Compose 规范的一个可选方面，在 [Compose 部署规范](deploy.md) 文档中有详细描述。如果未实现，`deploy` 部分将被忽略，并且 Compose 文件仍然被视为有效。

## 示例

### 简单示例

以下示例演示了如何使用 Docker Compose 定义两个简单服务，设置它们的镜像，映射端口，并配置基本的环境变量。

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"

  db:
    image: postgres:18
    environment:
      POSTGRES_USER: example
      POSTGRES_DB: exampledb
```

### 高级示例

在以下示例中，`proxy` 服务使用 Nginx 镜像，将本地 Nginx 配置文件挂载到容器中，暴露端口 `80` 并依赖于 `backend` 服务。

`backend` 服务从位于 `backend` 目录中的 Dockerfile 构建镜像，该镜像设置为在 `builder` 阶段构建。

```yaml
services:
  proxy:
    image: nginx
    volumes:
      - type: bind
        source: ./proxy/nginx.conf
        target: /etc/nginx/conf.d/default.conf
        read_only: true
    ports:
      - 80:80
    depends_on:
      - backend

  backend:
    build:
      context: backend
      target: builder
```

有关更多示例 Compose 文件，请探索 [Awesome Compose 示例](https://github.com/docker/awesome-compose)。

## 属性

<!-- vale off(Docker.HeadingSentenceCase.yml) -->

### `annotations`

`annotations` 为容器定义注解。`annotations` 可以使用数组或映射。

```yml
annotations:
  com.example.foo: bar
```

```yml
annotations:
  - com.example.foo=bar
```

### `attach`

{{< summary-bar feature_name="Compose attach" >}}

当定义 `attach` 并设置为 `false` 时，Compose 不会收集服务日志，直到您显式请求它这样做。

默认服务配置是 `attach: true`。

### `build`

`build` 指定从源代码创建容器镜像的构建配置，如 [Compose 构建规范](build.md) 中所定义。

### `blkio_config`

`blkio_config` 定义了一组配置选项，用于为服务设置块 I/O 限制。

```yml
services:
  foo:
    image: busybox
    blkio_config:
       weight: 300
       weight_device:
         - path: /dev/sda
           weight: 400
       device_read_bps:
         - path: /dev/sdb
           rate: '12mb'
       device_read_iops:
         - path: /dev/sdb
           rate: 120
       device_write_bps:
         - path: /dev/sdb
           rate: '1024k'
       device_write_iops:
         - path: /dev/sdb
           rate: 30
```

#### `device_read_bps`, `device_write_bps`

为给定设备的读/写操作设置每秒字节数的限制。
列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `rate`: 可以是表示字节数的整数值，也可以是表示字节值的字符串。

#### `device_read_iops`, `device_write_iops`

为给定设备的读/写操作设置每秒操作数的限制。
列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `rate`: 表示允许的每秒操作数的整数值。

#### `weight`

修改分配给服务的带宽相对于其他服务的比例。
取值范围为 10 到 1000 的整数值，其中 500 是默认值。

#### `weight_device`

按设备微调带宽分配。列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `weight`: 10 到 1000 之间的整数值。

### `cpu_count`

`cpu_count` 定义服务容器可用的 CPU 数量。

### `cpu_percent`

`cpu_percent` 定义可用 CPU 的可用百分比。

### `cpu_shares`

`cpu_shares` 定义为整数值，表示服务容器相对于其他容器的相对 CPU 权重。

### `cpu_period`

`cpu_period` 配置 CPU CFS（完全公平调度器）周期，当平台基于 Linux 内核时。

### `cpu_quota`

`cpu_quota` 配置 CPU CFS（完全公平调度器）配额，当平台基于 Linux 内核时。

### `cpu_rt_runtime`

`cpu_rt_runtime` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒作为单位的整数值，也可以是[持续时间](extension.md#specifying-durations)。

```yml
 cpu_rt_runtime: '400ms'
 cpu_rt_runtime: '95000'
```

### `cpu_rt_period`

`cpu_rt_period` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒作为单位的整数值，也可以是[持续时间](extension.md#specifying-durations)。

```yml
 cpu_rt_period: '1400us'
 cpu_rt_period: '11000'
```

### `cpus`

`cpus` 定义要分配给服务容器的（可能是虚拟的）CPU 数量。这是一个小数。
`0.000` 表示没有限制。

设置时，`cpus` 必须与 [部署规范](deploy.md#cpus) 中的 `cpus` 属性保持一致。

### `cpuset`

`cpuset` 定义允许执行的显式 CPU。可以是范围 `0-3` 或列表 `0,1`。

### `cap_add`

`cap_add` 指定额外的容器 [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) 作为字符串。

```yaml
cap_add:
  - ALL
```

### `cap_drop`

`cap_drop` 指定要删除的容器 [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) 作为字符串。

```yaml
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

### `cgroup`

{{< summary-bar feature_name="Compose cgroup" >}}

`cgroup` 指定要加入的 cgroup 命名空间。如果未设置，则由容器运行时决定选择哪个 cgroup 命名空间（如果支持）。

- `host`: 在容器运行时 cgroup 命名空间中运行容器。
- `private`: 在其自己的私有 cgroup 命名空间中运行容器。

### `cgroup_parent`

`cgroup_parent` 为容器指定一个可选的父 [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html)。

```yaml
cgroup_parent: m-executor-abcd
```

### `command`

`command` 覆盖容器镜像声明的默认命令，例如 Dockerfile 的 `CMD`。

```yaml
command: bundle exec thin -p 3000
```

如果值为 `null`，则使用镜像的默认命令。

如果值为 `[]`（空列表）或 `''`（空字符串），则镜像声明的默认命令将被忽略，或者换句话说，被覆盖为空。

> [!NOTE]
>
> 与 Dockerfile 中的 `CMD` 指令不同，`command` 字段不会自动在镜像定义的 [`SHELL`](/reference/dockerfile.md#shell-form) 指令上下文中运行。如果您的 `command` 依赖于特定于 shell 的功能，例如环境变量扩展，您需要显式地在 shell 中运行它。例如：
>
> ```yaml
> command: /bin/sh -c 'echo "hello $$HOSTNAME"'
> ```

该值也可以是一个列表，类似于 [Dockerfile](/reference/dockerfile.md#exec-form) 使用的 [exec-form 语法](/reference/dockerfile.md#exec-form)。

### `configs`

`configs` 让服务调整其行为，而无需重建 Docker 镜像。服务只有在通过 `configs` 属性显式授权时才能访问配置。支持两种不同的语法变体。

如果 `config` 在平台上不存在或未在 Compose 文件的 [`configs` 顶层元素](configs.md) 中定义，Compose 会报告错误。

为 configs 定义了两种语法：短语法和长语法。

您可以授予服务访问多个配置的权限，并且可以混合使用长语法和短语法。

#### 短语法

短语法变体仅指定配置名称。这授予容器访问配置的权限，并将其作为文件挂载到服务容器的文件系统中。容器内的挂载点位置在 Linux 容器中默认为 `/<config_name>`，在 Windows 容器中为 `C:\<config-name>`。

以下示例使用短语法授予 `redis` 服务访问 `my_config` 和 `my_other_config` 配置的权限。`my_config` 的值设置为文件 `./my_config.txt` 的内容，`my_other_config` 定义为外部资源，这意味着它已在平台上定义。如果外部配置不存在，则部署失败。

```yml
services:
  redis:
    image: redis:latest
    configs:
      - my_config
      - my_other_config
configs:
  my_config:
    file: ./my_config.txt
  my_other_config:
    external: true
```

#### 长语法

长语法在如何在服务的任务容器中创建配置方面提供了更细粒度的控制。

- `source`: 平台上存在的配置名称。
- `target`: 要挂载到服务任务容器中的文件路径和名称。如果未指定，则默认为 `/<source>`。
- `uid` 和 `gid`: 拥有服务任务容器内挂载配置文件的数字 uid 或 gid。
- `mode`: 挂载在服务任务容器中的文件的[权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法表示。默认值为世界可读 (`0444`)。可写位必须被忽略。可执行位可以设置。

以下示例将 `my_config` 的名称在容器内设置为 `redis_config`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`redis` 服务没有访问 `my_other_config` 配置的权限。

```yml
services:
  redis:
    image: redis:latest
    configs:
      - source: my_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440
configs:
  my_config:
    external: true
  my_other_config:
    external: true
```

### `container_name`

`container_name` 是一个字符串，用于指定自定义容器名称，而不是默认生成的名称。

```yml
container_name: my-web-container
```

如果 Compose 文件指定了 `container_name`，Compose 不会将服务扩展到一个容器以上。尝试这样做会导致错误。

`container_name` 遵循 `[a-zA-Z0-9][a-zA-Z0-9_.-]+` 的正则表达式格式。

### `credential_spec`

`credential_spec` 为托管服务帐户配置凭据规范。

如果您的服务使用 Windows 容器，您可以对 `credential_spec` 使用 `file:` 和 `registry:` 协议。Compose 还支持用于自定义用例的附加协议。

`credential_spec` 必须是 `file://<filename>` 或 `registry://<value-name>` 格式。

```yml
credential_spec:
  file: my-credential-spec.json
```

使用 `registry:` 时，凭据规范从守护程序主机上的 Windows 注册表中读取。具有给定名称的注册表值必须位于：

```bash
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\Containers\CredentialSpecs
```

以下示例从注册表中名为 `my-credential-spec` 的值加载凭据规范：

```yml
credential_spec:
  registry: my-credential-spec
```

#### gMSA 配置示例

为服务配置 gMSA 凭据规范时，您只需使用 `config` 指定一个凭据规范，如下例所示：

```yml
services:
  myservice:
    image: myimage:latest
    credential_spec:
      config: my_credential_spec

configs:
  my_credentials_spec:
    file: ./my-credential-spec.json
```

### `depends_on`

{{% include "compose/services-depends-on.md" %}}

#### 短语法

短语法变体仅指定依赖项的服务名称。
服务依赖项会导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 按依赖顺序删除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前删除。

简单示例：

```yml
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres:18
```

Compose 保证在启动依赖服务之前，依赖服务已经启动。
Compose 等待依赖服务“就绪”后再启动依赖服务。

#### 长语法

长表单语法支持配置短表单中无法表达的附加字段。

- `restart`: 当设置为 `true` 时，Compose 在更新依赖服务后重新启动此服务。这适用于由 Compose 操作控制的显式重新启动，不包括容器在死亡后由容器运行时自动重新启动。在 Docker Compose 版本 [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0) 中引入。

- `condition`: 设置依赖项被视为满足的条件
  - `service_started`: 等同于前面描述的短语法。
  - `service_healthy`: 指定依赖项在启动依赖服务之前需要是“健康的”（由 [`healthcheck`](#healthcheck) 指示）。
  - `service_completed_successfully`: 指定依赖项在启动依赖服务之前需要成功完成运行。
- `required`: 当设置为 `false` 时，如果依赖服务未启动或不可用，Compose 仅发出警告。如果未定义，`required` 的默认值为 `true`。在 Docker Compose 版本 [2.20.0](https://github.com/docker/compose/releases/tag/v2.20.0) 中引入。

服务依赖项会导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 等待标记为 `service_healthy` 的依赖项的健康检查通过。在以下示例中，`db` 需要在 `web` 创建之前是“健康的”。

- Compose 按依赖顺序删除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前删除。

```yml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres:18
```

Compose 保证在启动依赖服务之前，依赖服务已经启动。
Compose 保证在启动依赖服务之前，标记为 `service_healthy` 的依赖服务是“健康的”。

### `deploy`

`deploy` 指定服务的部署和生命周期配置，如 [Compose 部署规范](deploy.md) 中所定义。

### `develop`

{{< summary-bar feature_name="Compose develop" >}}

`develop` 指定用于保持容器与源代码同步的开发配置，如 [开发部分](develop.md) 中所定义。

### `device_cgroup_rules`

`device_cgroup_rules` 为此容器定义设备 cgroup 规则列表。
格式与 Linux 内核在 [控制组设备白名单控制器](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/devices.html) 中指定的格式相同。

```yml
device_cgroup_rules:
  - 'c 1:3 mr'
  - 'a 7:* rmw'
```

### `devices`

`devices` 为创建的容器定义设备映射列表，形式为 `HOST_PATH:CONTAINER_PATH[:CGROUP_PERMISSIONS]`。

```yml
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
  - "/dev/sda:/dev/xvda:rwm"
```

`devices` 也可以依赖 [CDI](https://github.com/cncf-tags/container-device-interface) 语法，让容器运行时选择设备：

```yml
devices:
  - "vendor1.com/device=gpu"
```

### `dns`

`dns` 定义要在容器网络接口配置上设置的自定义 DNS 服务器。它可以是单个值或列表。

```yml
dns: 8.8.8.8
```

```yml
dns:
  - 8.8.8.8
  - 9.9.9.9
```

### `dns_opt`

`dns_opt` 列出要传递给容器 DNS 解析器（Linux 上的 `/etc/resolv.conf` 文件）的自定义 DNS 选项。

```yml
dns_opt:
  - use-vc
  - no-tld-query
```

### `dns_search`

`dns_search` 定义要在容器网络接口配置上设置的自定义 DNS 搜索域。它可以是单个值或列表。

```yml
dns_search: example.com
```

```yml
dns_search:
  - dc1.example.com
  - dc2.example.com
```

### `domainname`

`domainname` 声明服务容器要使用的自定义域名。它必须是有效的 RFC 1123 主机名。

### `driver_opts`

{{< summary-bar feature_name="Compose driver opts" >}}

`driver_opts` 指定一个键值对选项列表以传递给驱动程序。这些选项是特定于驱动程序的。

```yml
services:
  app:
    networks:
      app_net:
        driver_opts:
          com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

有关更多信息，请参阅 [网络驱动程序文档](/manuals/engine/network/_index.md)。

### `entrypoint`

`entrypoint` 声明服务容器的默认入口点。这会覆盖服务 Dockerfile 中的 `ENTRYPOINT` 指令。

如果 `entrypoint` 非 null，Compose 会忽略镜像的任何默认命令，例如 Dockerfile 中的 `CMD` 指令。

另请参阅 [`command`](#command) 以设置或覆盖入口点进程要执行的默认命令。

在其短形式中，值可以定义为字符串：
```yml
entrypoint: /code/entrypoint.sh
```

或者，该值也可以是一个列表，类似于 [Dockerfile](https://docs.docker.com/reference/dockerfile/#cmd) 的方式：

```yml
entrypoint:
  - php
  - -d
  - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
  - -d
  - memory_limit=-1
  - vendor/bin/phpunit
```

如果值为 `null`，则使用镜像的默认入口点。

如果值为 `[]`（空列表）或 `''`（空字符串），则镜像声明的默认入口点将被忽略，或者换句话说，被覆盖为空。

### `env_file`

{{% include "compose/services-env-file.md" %}}

```yml
env_file: .env
```

相对路径从 Compose 文件的父文件夹解析。由于绝对路径会阻止 Compose 文件的可移植性，当使用此类路径设置 `env_file` 时，Compose 会发出警告。

在 [`environment`](#environment) 部分声明的环境变量会覆盖这些值。即使这些值为空或未定义，也是如此。

`env_file` 也可以是一个列表。列表中的文件从上到下处理。对于在两个环境文件中指定的相同变量，列表中最后一个文件中的值有效。

```yml
env_file:
  - ./a.env
  - ./b.env
```

列表元素也可以声明为映射，这样可以设置附加属性。

#### `required`

{{< summary-bar feature_name="Compose required" >}}

`required` 属性默认为 `true`。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。

```yml
env_file:
  - path: ./default.env
    required: true # default
  - path: ./override.env
    required: false
```

#### `format`

{{< summary-bar feature_name="Compose format" >}}

`format` 属性允许您为 `env_file` 使用替代文件格式。如果未设置，`env_file` 将根据 [`Env_file` 格式](#env_file-format) 中概述的 Compose 规则进行解析。

`raw` 格式允许您使用带有键=值项的 `env_file`，但 Compose 不会尝试解析值以进行插值。这允许您按原样传递值，包括引号和 `$` 符号。

```yml
env_file:
  - path: ./default.env
    format: raw
```

#### `Env_file` 格式

`.env` 文件中的每一行都必须是 `VAR[=[VAL]]` 格式。适用以下语法规则：

- 以 `#` 开头的行被视为注释并被忽略。
- 空行被忽略。
- 未加引号和双引号 (`"`) 的值会应用[插值](interpolation.md)。
- 每行代表一个键值对。值可以选择性地加引号。
- 分隔键和值的分隔符可以是 `=` 或 `:`。
- 值前后的空格将被忽略。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
  - `VAR: VAL` -> `VAL`
  - `VAR = VAL  ` -> `VAL` <!-- markdownlint-disable-line no-space-in-code -->
- 未加引号值的内联注释前面必须有一个空格。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 加引号值的内联注释必须跟在闭引号后面。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号 (`'`) 值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 双引号值中支持常见的 shell 转义序列，包括 `\n`, `\r`, `\t` 和 `\\`。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`

`VAL` 可以省略，在这种情况下，变量值为空字符串。
`=VAL` 可以省略，在这种情况下，变量未设置。

```bash
# Set Rails/Rack environment
RACK_ENV=development
VAR="quoted"
```

### `environment`

{{% include "compose/services-environment.md" %}}

环境变量可以通过单个键（没有值的等号）声明。在这种情况下，Compose 依赖您来解析值。如果值未解析，变量将被取消设置并从服务容器环境中移除。

映射语法：

```yml
environment:
  RACK_ENV: development
  SHOW: "true"
  USER_INPUT:
```

数组语法：

```yml
environment:
  - RACK_ENV=development
  - SHOW=true
  - USER_INPUT
```

当服务同时设置了 `env_file` 和 `environment` 时，`environment` 设置的值具有优先权。

### `expose`

`expose` 定义 Compose 从容器暴露的（传入）端口或端口范围。这些端口必须可供链接的服务访问，并且不应发布到主机机器。只能指定内部容器端口。

语法是 `<portnum>/[<proto>]` 或 `<startport-endport>/[<proto>]` 表示端口范围。如果未显式设置，则使用 `tcp` 协议。

```yml
expose:
  - "3000"
  - "8000"
  - "8080-8085/tcp"
```

> [!NOTE]
>
> 如果镜像的 Dockerfile 已经暴露了端口，即使您的 Compose 文件中没有设置 `expose`，它对网络上的其他容器也是可见的。

### `extends`

`extends` 允许您在不同文件甚至完全不同的项目之间共享公共配置。使用 `extends`，您可以在一个地方定义一组通用的服务选项，并从任何地方引用它。您可以引用另一个 Compose 文件并选择您也想在自己的应用程序中使用的服务，并能够覆盖一些属性以满足自己的需求。

您可以在任何服务上使用 `extends` 以及其他配置键。`extends` 值必须是一个映射，定义为必需的 `service` 和可选的 `file` 键。

```yaml
extends:
  file: common.yml
  service: webapp
```

- `service`: 定义作为基础引用的服务名称，例如 `web` 或 `database`。
- `file`: 定义该服务的 Compose 配置文件的位置。

#### 限制

当使用 `extends` 引用服务时，它可以声明对其他资源的依赖关系。这些依赖关系可以通过 `volumes`、`networks`、`configs`、`secrets`、`links`、`volumes_from` 或 `depends_on` 等属性显式定义。或者，依赖关系可以在命名空间声明（如 `ipc`、`pid` 或 `network_mode`）中使用 `service:{name}` 语法引用另一个服务。

Compose 不会自动将这些引用的资源导入扩展模型。您有责任确保所有必需的资源都在依赖扩展的模型中显式声明。

不支持使用 `extends` 进行循环引用，Compose 在检测到时会返回错误。

#### 查找引用的服务

`file` 值可以是：

- 不存在。
  这表示正在引用同一 Compose 文件中的另一个服务。
- 文件路径，可以是：
  - 相对路径。此路径被视为相对于主 Compose 文件的位置。
  - 绝对路径。

由 `service` 表示的服务必须存在于标识的引用 Compose 文件中。
如果出现以下情况，Compose 会返回错误：

- 找不到由 `service` 表示的服务。
- 找不到由 `file` 表示的 Compose 文件。

#### 合并服务定义

两个服务定义，主定义在当前 Compose 文件中，引用的定义由 `extends` 指定，按以下方式合并：

- 映射：主服务定义映射中的键会覆盖引用服务定义映射中的键。未被覆盖的键按原样包含。
- 序列：项目组合在一起形成一个新的序列。元素的顺序被保留，引用的项目在前，主项目在后。
- 标量：主服务定义中的键优先于引用定义中的键。

##### 映射

以下键应视为映射：`annotations`, `build.args`, `build.labels`, `build.extra_hosts`, `deploy.labels`, `deploy.update_config`, `deploy.rollback_config`, `deploy.restart_policy`, `deploy.resources.limits`, `environment`, `healthcheck`, `labels`, `logging.options`, `sysctls`, `storage_opt`, `extra_hosts`, `ulimits`。

适用于 `healthcheck` 的一个例外是，主映射不能指定 `disable: true`，除非引用的映射也指定 `disable: true`。在这种情况下，Compose 会返回错误。
例如，以下输入：

```yaml
services:
  common:
    image: busybox
    environment:
      TZ: utc
      PORT: 80
  cli:
    extends:
      service: common
    environment:
      PORT: 8080
```

为 `cli` 服务生成以下配置。如果使用数组语法，也会产生相同的输出。

```yaml
environment:
  PORT: 8080
  TZ: utc
image: busybox
```

`blkio_config.device_read_bps`, `blkio_config.device_read_iops`, `blkio_config.device_write_bps`, `blkio_config.device_write_iops`, `devices` 和 `volumes` 下的项目也被视为映射，其中键是容器内的目标路径。

例如，以下输入：

```yaml
services:
  common:
    image: busybox
    volumes:
      - common-volume:/var/lib/backup/data:rw
  cli:
    extends:
      service: common
    volumes:
      - cli-volume:/var/lib/backup/data:ro
```

为 `cli` 服务生成以下配置。请注意，挂载路径现在指向新的卷名称，并且应用了 `ro` 标志。

```yaml
image: busybox
volumes:
- cli-volume:/var/lib/backup/data:ro
```

如果引用的服务定义包含 `extends` 映射，则其下的项目将简单地复制到新的合并定义中。然后再次启动合并过程，直到没有剩余的 `extends` 键。

例如，以下输入：

```yaml
services:
  base:
    image: busybox
    user: root
  common:
    image: busybox
    extends:
      service: base
  cli:
    extends:
      service: common
```

为 `cli` 服务生成以下配置。在这里，`cli` 服务从 `common` 服务获取 `user` 键，而 `common` 服务又从 `base` 服务获取此键。

```yaml
image: busybox
user: root
```

##### 序列

以下键应视为序列：`cap_add`, `cap_drop`, `configs`, `deploy.placement.constraints`, `deploy.placement.preferences`, `deploy.reservations.generic_resources`, `device_cgroup_rules`, `expose`, `external_links`, `ports`, `secrets`, `security_opt`。
合并产生的任何重复项都会被删除，因此序列只包含唯一的元素。

例如，以下输入：

```yaml
services:
  common:
    image: busybox
    security_opt:
      - label=role:ROLE
  cli:
    extends:
      service: common
    security_opt:
      - label=user:USER
```

为 `cli` 服务生成以下配置。

```yaml
image: busybox
security_opt:
- label=role:ROLE
- label=user:USER
```

如果使用列表语法，以下键也应视为序列：`dns`, `dns_search`, `env_file`, `tmpfs`。与前面提到的序列字段不同，合并产生的重复项不会被删除。

##### 标量

服务定义中任何其他允许的键都应视为标量。

### `external_links`

`external_links` 将服务容器链接到 Compose 应用程序外部管理的服务。
`external_links` 定义要使用平台查找机制检索的现有服务的名称。
可以指定形式为 `SERVICE:ALIAS` 的别名。

```yml
external_links:
  - redis
  - database:mysql
  - database:postgresql
```

### `extra_hosts`

`extra_hosts` 将主机名映射添加到容器网络接口配置（Linux 上的 `/etc/hosts`）。

#### 短语法

短语法在列表中使用纯字符串。值必须以 `HOSTNAME=IP` 的形式为附加主机设置主机名和 IP 地址。

```yml
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"
```

IPv6 地址可以括在方括号中，例如：

```yml
extra_hosts:
  - "myhostv6=[::1]"
```

分隔符 `=` 是首选，但 `:` 也可以使用。在 Docker Compose 版本 [2.24.1](https://github.com/docker/compose/releases/tag/v2.24.1) 中引入。例如：

```yml
extra_hosts:
  - "somehost:162.242.195.82"
  - "myhostv6:::1"
```

#### 长语法

或者，`extra_hosts` 可以设置为主机名和 IP 之间的映射

```yml
extra_hosts:
  somehost: "162.242.195.82"
  otherhost: "50.31.209.229"
  myhostv6: "::1"
```

Compose 在容器的网络配置中创建一个匹配的条目，其中包含 IP 地址和主机名，这意味着对于 Linux，`/etc/hosts` 会获得额外的行：

```console
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### `gpus`

{{< summary-bar feature_name="Compose gpus" >}}

`gpus` 指定要分配给容器使用的 GPU 设备。这等同于具有隐式 `gpu` 功能的[设备请求](deploy.md#devices)。

```yaml
services:
  model:
    gpus:
      - driver: 3dfx
        count: 2
```

`gpus` 也可以设置为字符串 `all`，以将所有可用的 GPU 设备分配给容器。

```yaml
services:
  model:
    gpus: all
```

### `group_add`

`group_add` 指定容器内用户必须是其成员的附加组（按名称或编号）。

这在多个容器（以不同用户身份运行）需要读取或写入共享卷上的同一文件时非常有用。该文件可以由所有容器共享的组拥有，并在 `group_add` 中指定。

```yml
services:
  myservice:
    image: alpine
    group_add:
      - mail
```

在创建的容器内运行 `id` 必须显示用户属于 `mail` 组，如果未声明 `group_add`，则情况不会如此。

### `healthcheck`

{{% include "compose/services-healthcheck.md" %}}

有关 `HEALTHCHECK` 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md#healthcheck)。

```yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 1m30s
  timeout: 10s
  retries: 3
  start_period: 40s
  start_interval: 5s
```

`interval`, `timeout`, `start_period`, 和 `start_interval` 是[指定为持续时间](extension.md#specifying-durations)。在 Docker Compose 版本 [2.20.2](https://github.com/docker/compose/releases/tag/v2.20.2) 中引入。

`test` 定义 Compose 为检查容器健康状况而运行的命令。它可以是字符串或列表。如果是列表，第一项必须是 `NONE`、`CMD` 或 `CMD-SHELL`。
如果是字符串，则等同于指定 `CMD-SHELL` 后跟该字符串。

```yml
# Hit the local web app
test: ["CMD", "curl", "-f", "http://localhost"]
```

使用 `CMD-SHELL` 以字符串形式运行配置的命令，使用容器的默认 shell（Linux 上为 `/bin/sh`）。以下两种形式是等效的：

```yml
test: ["CMD-SHELL", "curl -f http://localhost || exit 1"]
```

```yml
test: curl -f https://localhost || exit 1
```

`NONE` 禁用健康检查，主要用于禁用服务 Docker 镜像设置的 Healthcheck Dockerfile 指令集。或者，可以通过设置 `disable: true` 来禁用镜像设置的健康检查：

```yml
healthcheck:
  disable: true
```

### `hostname`

`hostname` 声明服务容器要使用的自定义主机名。它必须是有效的 RFC 1123 主机名。

### `image`

`image` 指定要从中启动容器的镜像。`image` 必须遵循 Open Container Specification [可寻址镜像格式](https://github.com/opencontainers/org/blob/master/docs/docs/introduction/digests.md)，即 `[<registry>/][<project>/]<image>[:<tag>|@<digest>]`。

```yml
    image: redis
    image: redis:5
    image: redis@sha256:0ed5d5928d4737458944eb604cc8509e245c3e19d02ad83935398bc4b991aac7
    image: library/redis
    image: docker.io/library/redis
    image: my_private.registry:5000/redis
```

如果镜像在平台上不存在，Compose 会根据 `pull_policy` 尝试拉取它。如果您也使用 [Compose 构建规范](build.md)，则有其他选项可以控制拉取与从源代码构建镜像的优先级，但拉取镜像是默认行为。

只要声明了 `build` 部分，就可以从 Compose 文件中省略 `image`。如果您不使用 Compose 构建规范，并且 Compose 文件中缺少 `image`，Compose 将无法工作。

### `init`

`init` 在容器内运行一个 init 进程（PID 1），该进程转发信号并回收进程。
将此选项设置为 `true` 可为服务启用此功能。

```yml
services:
  web:
    image: alpine:latest
    init: true
```

使用的 init 二进制文件是特定于平台的。

### `ipc`

`ipc` 配置服务容器设置的 IPC 隔离模式。

- `shareable`: 给予容器其自己的私有 IPC 命名空间，并有可能与其他容器共享。
- `service:{name}`: 使容器加入另一个容器的（`shareable`）IPC 命名空间。

```yml
    ipc: "shareable"
    ipc: "service:[service name]"
```

### `isolation`

`isolation` 指定容器的隔离技术。支持的值是特定于平台的。

### `labels`

`labels` 向容器添加元数据。您可以使用数组或映射。

建议使用反向 DNS 表示法，以防止您的标签与其他软件使用的标签冲突。

```yml
labels:
  com.example.description: "Accounting webapp"
  com.example.department: "Finance"
  com.example.label-with-empty-value: ""
```

```yml
labels:
  - "com.example.description=Accounting webapp"
  - "com.example.department=Finance"
  - "com.example.label-with-empty-value"
```

Compose 使用规范标签创建容器：

- `com.docker.compose.project` 设置在 Compose 创建的所有资源上，值为用户项目名称
- `com.docker.compose.service` 设置在服务容器上，值为 Compose 文件中定义的服务名称

`com.docker.compose` 标签前缀是保留的。在 Compose 文件中指定此前缀的标签会导致运行时错误。

### `label_file`

{{< summary-bar feature_name="Compose label file" >}}

`label_file` 属性允许您从外部文件或文件列表加载服务的标签。这提供了一种管理多个标签的便捷方式，而不会使 Compose 文件变得混乱。

该文件使用键值格式，类似于 `env_file`。您可以将多个文件指定为一个列表。使用多个文件时，它们按在列表中出现的顺序处理。如果在多个文件中定义了相同的标签，则列表中最后一个文件中的值会覆盖前面的值。

```yaml
services:
  one:
    label_file: ./app.labels

  two:
    label_file:
      - ./app.labels
      - ./additional.labels
```

如果标签在 `label_file` 和 `labels` 属性中都定义了，则 [labels](#labels) 中的值具有优先权。

### `links`

`links` 定义到另一个服务中容器的网络链接。可以同时指定服务名称和链接别名 (`SERVICE:ALIAS`)，或者仅指定服务名称。

```yml
web:
  links:
    - db
    - db:database
    - redis
```

链接服务的容器可通过与别名相同的主机名访问，如果未指定别名，则通过服务名称访问。

链接不是启用服务通信所必需的。当未设置特定的网络配置时，任何服务都可以在 `default` 网络上通过该服务的名称访问任何其他服务。如果服务指定了它们连接的网络，`links` 不会覆盖网络配置。未连接到共享网络的服务无法相互通信。Compose 不会就配置不匹配发出警告。

链接还以与 [`depends_on`](#depends_on) 相同的方式表达服务之间的隐式依赖关系，因此它们决定了服务启动的顺序。

### `logging`

`logging` 定义服务的日志记录配置。

```yml
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

`driver` 名称指定服务容器的日志记录驱动程序。默认值和可用值是特定于平台的。特定于驱动程序的选项可以使用 `options` 作为键值对来设置。

### `mac_address`

> 在 Docker Compose 版本 2.24.0 及更高版本中可用。

`mac_address` 为服务容器设置 Mac 地址。

> [!NOTE]
> 容器运行时可能会拒绝此值，例如 Docker Engine >= v25.0。在这种情况下，您应该使用 [networks.mac_address](#mac_address) 代替。

### `mem_limit`

`mem_limit` 配置容器可以分配的内存量限制，设置为表示[字节值](extension.md#specifying-byte-values)的字符串。

设置时，`mem_limit` 必须与 [部署规范](deploy.md#memory) 中的 `limits.memory` 属性保持一致。

### `mem_reservation`

`mem_reservation` 配置容器可以分配的内存量预留，设置为表示[字节值](extension.md#specifying-byte-values)的字符串。

设置时，`mem_reservation` 必须与 [部署规范](deploy.md#memory) 中的 `reservations.memory` 属性保持一致。

### `mem_swappiness`

`mem_swappiness` 定义为百分比，值在 0 到 100 之间，表示主机内核将匿名内存页交换出去的程度。

- `0`: 关闭匿名页面交换。
- `100`: 将所有匿名页面设置为可交换。

默认值是特定于平台的。

### `memswap_limit`

`memswap_limit` 定义容器允许交换到磁盘的内存量。这是一个修饰符属性，仅在同时设置了 [`memory`](deploy.md#memory) 时才有意义。使用交换允许容器在用尽所有可用内存时将多余的内存需求写入磁盘。经常将内存交换到磁盘的应用程序会受到性能损失。

- 如果 `memswap_limit` 设置为正整数，则 `memory` 和 `memswap_limit` 都必须设置。`memswap_limit` 表示可以使用的内存和交换的总量，`memory` 控制非交换内存的使用量。因此，如果 `memory`="300m" 且 `memswap_limit`="1g"，容器可以使用 300m 内存和 700m (1g - 300m) 交换空间。
- 如果 `memswap_limit` 设置为 0，则该设置被忽略，该值被视为未设置。
- 如果 `memswap_limit` 设置为与 `memory` 相同的值，并且 `memory` 设置为正整数，则容器无法访问交换空间。
- 如果 `memswap_limit` 未设置，但 `memory` 已设置，并且主机容器配置了交换内存，则容器可以使用与 `memory` 设置一样多的交换空间。例如，如果 `memory`="300m" 且 `memswap_limit` 未设置，容器总共可以使用 600m 内存和交换空间。
- 如果 `memswap_limit` 显式设置为 -1，则容器允许使用无限交换空间，最多可达主机系统上可用的量。

### `models`

{{< summary-bar feature_name="Compose models" >}}

`models` 定义服务在运行时应使用的 AI 模型。每个引用的模型必须在 [`models` 顶层元素](models.md) 下定义。

```yaml
services:
  short_syntax:
    image: app
    models:
      - my_model
  long_syntax:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL
        model_var: MODEL
```

当服务链接到模型时，Docker Compose 会注入环境变量以将连接详细信息和模型标识符传递给容器。这允许应用程序在运行时动态定位和通信模型，而无需硬编码值。

#### 长语法

长语法让您更好地控制环境变量名称。

- `endpoint_var` 设置保存模型运行程序 URL 的环境变量的名称。
- `model_var` 设置保存模型标识符的环境变量的名称。

如果省略其中任何一个，Compose 会根据模型键自动生成环境变量名称，使用以下规则：

 - 将模型键转换为大写
 - 将任何 '-' 字符替换为 '_'
 - 为端点变量附加 `_URL`

### `network_mode`

`network_mode` 设置服务容器的网络模式。

- `none`: 关闭所有容器网络。
- `host`: 给予容器对主机网络接口的原始访问权限。
- `service:{name}`: 通过引用其服务名称，使容器可以访问指定的容器。
- `container:{name}`: 通过引用其容器 ID，使容器可以访问指定的容器。

有关容器网络的更多信息，请参阅 [Docker Engine 文档](/manuals/engine/network/_index.md#container-networks)。

```yml
    network_mode: "host"
    network_mode: "none"
    network_mode: "service:[service name]"
```

设置时，不允许使用 [`networks`](#networks) 属性，Compose 会拒绝任何包含这两个属性的 Compose 文件。

### `networks`

{{% include "compose/services-networks.md" %}}

```yml
services:
  some-service:
    networks:
      - some-network
      - other-network
```
有关 `networks` 顶层元素的更多信息，请参阅 [网络](networks.md)。

#### 隐式默认网络

如果 `networks` 在 Compose 文件中为空或不存在，Compose 会考虑服务连接到 `default` 网络的隐式定义：

```yml
services:
  some-service:
    image: foo
```
此示例实际上等同于：

```yml
services:
  some-service:
    image: foo
    networks:
      default: {}
```

如果您希望服务不连接到任何网络，您必须设置 [`network_mode: none`](#network_mode)。

#### `aliases`

`aliases` 声明服务在网络上替代主机名。同一网络上的其他容器可以使用服务名称或别名来连接到服务的容器之一。

由于 `aliases` 是网络范围的，同一服务在不同网络上可以有不同的别名。

> [!NOTE]
> 网络范围的别名可以由多个容器甚至多个服务共享。
> 如果是这样，则无法保证名称解析到哪个容器。

```yml
services:
  some-service:
    networks:
      some-network:
        aliases:
          - alias1
          - alias3
      other-network:
        aliases:
          - alias2
```

在以下示例中，服务 `frontend` 能够在 `back-tier` 网络上通过主机名 `backend` 或 `database` 访问 `backend` 服务。服务 `monitoring` 能够在 `admin` 网络上通过 `backend` 或 `mysql` 访问相同的 `backend` 服务。

```yml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

  monitoring:
    image: example/monitoring
    networks:
      - admin

  backend:
    image: example/backend
    networks:
      back-tier:
        aliases:
          - database
      admin:
        aliases:
          - mysql

networks:
  front-tier: {}
  back-tier: {}
  admin: {}
```

#### `interface_name`

{{< summary-bar feature_name="Compose interface-name" >}}

`interface_name` 允许您指定用于将服务连接到给定网络的网络接口的名称。这确保了跨服务和网络的一致和可预测的接口命名。

```yaml
services:
  backend:
    image: alpine
    command: ip link show
    networks:
      back-tier:
        interface_name: eth0
```

运行示例 Compose 应用程序会显示：

```console
backend-1  | 11: eth0@if64: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
```

#### `ipv4_address`, `ipv6_address`

指定加入网络时服务容器的静态 IP 地址。

[顶层网络部分](networks.md) 中相应的网络配置必须具有 `ipam` 属性，其中包含覆盖每个静态地址的子网配置。

```yml
services:
  frontend:
    image: example/webapp
    networks:
      front-tier:
        ipv4_address: 172.16.238.10
        ipv6_address: 2001:3984:3989::10

networks:
  front-tier:
    ipam:
      driver: default
      config:
        - subnet: "172.16.238.0/24"
        - subnet: "2001:3984:3989::/64"
```

#### `link_local_ips`

`link_local_ips` 指定链路本地 IP 列表。链路本地 IP 是属于众所周知的子网的特殊 IP，纯粹由操作员管理，通常取决于部署它们的架构。

示例：

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net:
        link_local_ips:
          - 57.123.22.11
          - 57.123.22.13
networks:
  app_net:
    driver: bridge
```

#### `mac_address`

{{< summary-bar feature_name="Compose mac address" >}}

`mac_address` 设置服务容器连接到此特定网络时使用的 Mac 地址。

#### `driver_opts`

`driver_opts` 指定一个键值对选项列表以传递给驱动程序。这些选项是特定于驱动程序的。有关更多信息，请查阅驱动程序的文档。

```yml
services:
  app:
    networks:
      app_net:
        driver_opts:
          foo: "bar"
          baz: 1
```

#### `gw_priority`

{{< summary-bar feature_name="Compose gw priority" >}}

具有最高 `gw_priority` 的网络被选为服务容器的默认网关。
如果未指定，默认值为 0。

在以下示例中，`app_net_2` 将被选为默认网关。

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
      app_net_2:
        gw_priority: 1
      app_net_3:
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

#### `priority`

`priority` 指示 Compose 将服务容器连接到其网络的顺序。如果未指定，默认值为 0。

如果容器运行时在服务级别接受 `mac_address` 属性，则它将应用于具有最高 `priority` 的网络。在其他情况下，请使用属性 `networks.mac_address`。

`priority` 不影响哪个网络被选为默认网关。请改用 [`gw_priority`](#gw_priority) 属性。

`priority` 不控制网络连接添加到容器的顺序，它不能用于确定容器中的设备名称（`eth0` 等）。

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
        priority: 1000
      app_net_2:

      app_net_3:
        priority: 100
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

### `oom_kill_disable`

如果设置了 `oom_kill_disable`，Compose 会配置平台，使其在内存不足的情况下不会杀死容器。

### `oom_score_adj`

`oom_score_adj` 调整容器在内存不足时被平台杀死的优先级。值必须在 -1000,1000 范围内。

### `pid`

`pid` 设置 Compose 创建的容器的 PID 模式。
支持的值是特定于平台的。

### `pids_limit`

`pids_limit` 调整容器的 PIDs 限制。设置为 -1 表示无限制 PIDs。

```yml
pids_limit: 10
```

设置时，`pids_limit` 必须与 [部署规范](deploy.md#pids) 中的 `pids` 属性保持一致。

### `platform`

`platform` 定义服务容器运行的目标平台。它使用 `os[/arch[/variant]]` 语法。

`os`、`arch` 和 `variant` 的值必须符合 [OCI 镜像规范](https://github.com/opencontainers/image-spec/blob/v1.0.2/image-index.md) 使用的约定。

Compose 使用此属性来确定要拉取哪个版本的镜像和/或在哪个平台上执行服务的构建。

```yml
platform: darwin
platform: windows/amd64
platform: linux/arm64/v8
```

### `ports`

{{% include "compose/services-ports.md" %}}

> [!NOTE]
>
> 端口映射不得与 `network_mode: host` 一起使用。这样做会导致运行时错误，因为 `network_mode: host` 已经将容器端口直接暴露给主机网络，因此不需要端口映射。

#### 短语法

短语法是一个冒号分隔的字符串，用于设置主机 IP、主机端口和容器端口，形式为：

`[HOST:]CONTAINER[/PROTOCOL]` 其中：

- `HOST` 是 `[IP:](port | range)`（可选）。如果未设置，则绑定到所有网络接口 (`0.0.0.0`)。
- `CONTAINER` 是 `port | range`。
- `PROTOCOL` 将端口限制为指定协议，`tcp` 或 `udp`（可选）。默认为 `tcp`。

端口可以是单个值或范围。`HOST` 和 `CONTAINER` 必须使用等效的范围。

您可以同时指定两个端口 (`HOST:CONTAINER`)，或者仅指定容器端口。在后一种情况下，容器运行时会自动分配主机的任何未分配端口。

`HOST:CONTAINER` 应始终指定为（带引号的）字符串，以避免与 [YAML base-60 浮点数](https://yaml.org/type/float.html) 冲突。

IPv6 地址可以括在方括号中。

示例：

```yml
ports:
  - "3000"
  - "3000-3005"
  - "8000:8000"
  - "9090-9091:8080-8081"
  - "49100:22"
  - "8000-9000:80"
  - "127.0.0.1:8001:8001"
  - "127.0.0.1:5000-5010:5000-5010"
  - "::1:6000:6000"
  - "[::1]:6001:6001"
  - "6060:6060/udp"
```

> [!NOTE]
>
> 如果容器引擎不支持主机 IP 映射，Compose 会拒绝 Compose 文件并忽略指定的主机 IP。

#### 长语法

长表单语法允许您配置短表单中无法表达的附加字段。

- `target`: 容器端口。
- `published`: 公开暴露的端口。定义为字符串，可以使用语法 `start-end` 设置为范围。这意味着实际端口在指定范围内分配一个剩余的可用端口。
- `host_ip`: 主机 IP 映射。如果未设置，则绑定到所有网络接口 (`0.0.0.0`)。
- `protocol`: 端口协议 (`tcp` 或 `udp`)。默认为 `tcp`。
- `app_protocol`: 此端口使用的应用程序协议（TCP/IP 第 4 层 / OSI 第 7 层）。这是可选的，可用作提示，以便 Compose 为其理解的协议提供更丰富的行为。在 Docker Compose 版本 [2.26.0](https://github.com/docker/compose/releases/tag/v2.26.0) 中引入。
- `mode`: 指定在 Swarm 设置中发布端口的方式。如果设置为 `host`，则在 Swarm 中的每个节点上发布端口。如果设置为 `ingress`，则允许在 Swarm 中的节点之间进行负载均衡。默认为 `ingress`。
- `name`: 端口的可读名称，用于记录其在服务中的使用情况。

```yml
ports:
  - name: web
    target: 80
    host_ip: 127.0.0.1
    published: "8080"
    protocol: tcp
    app_protocol: http
    mode: host

  - name: web-secured
    target: 443
    host_ip: 127.0.0.1
    published: "8083-9000"
    protocol: tcp
    app_protocol: https
    mode: host
```

### `post_start`

{{< summary-bar feature_name="Compose post start" >}}

`post_start` 定义容器启动后要运行的一系列生命周期钩子。命令运行的确切时间无法保证。

- `command`: 指定容器启动后要运行的命令。此属性是必需的，您可以选择使用 shell 形式或 exec 形式。
- `user`: 运行命令的用户。如果未设置，命令将以与主服务命令相同的用户运行。
- `privileged`: 允许 `post_start` 命令以特权访问运行。
- `working_dir`: 运行命令的工作目录。如果未设置，则在与主服务命令相同的工作目录中运行。
- `environment`: 专门为 `post_start` 命令设置环境变量。虽然命令继承为服务主命令定义的环境变量，但此部分允许您添加新变量或覆盖现有变量。

```yaml
services:
  test:
    post_start:
      - command: ./do_something_on_startup.sh
        user: root
        privileged: true
        environment:
          - FOO=BAR
```

有关更多信息，请参阅 [使用生命周期钩子](/manuals/compose/how-tos/lifecycle.md)。

### `pre_stop`

{{< summary-bar feature_name="Compose pre stop" >}}

`pre_stop` 定义容器停止前要运行的一系列生命周期钩子。如果容器自行停止或突然终止，这些钩子不会运行。

配置等同于 [post_start](#post_start)。

### `privileged`

`privileged` 配置服务容器以提升的权限运行。支持和实际影响是特定于平台的。

### `profiles`

`profiles` 定义服务要启用的命名配置文件列表。如果未分配，服务将始终启动，但如果已分配，则仅在配置文件激活时启动。

如果存在，`profiles` 遵循 `[a-zA-Z0-9][a-zA-Z0-9_.-]+` 的正则表达式格式。

```yaml
services:
  frontend:
    image: frontend
    profiles: ["frontend"]

  phpmyadmin:
    image: phpmyadmin
    depends_on:
      - db
    profiles:
      - debug
```

### `provider`

{{< summary-bar feature_name="Compose provider services" >}}

`provider` 可用于定义 Compose 不会直接管理的服务。Compose 将服务生命周期委托给专用或第三方组件。

```yaml
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar
  app:
    image: myapp
    depends_on:
       - database
```

当 Compose 运行应用程序时，`awesomecloud` 二进制文件用于管理 `database` 服务设置。
依赖服务 `app` 接收到以服务名称为前缀的附加环境变量，以便它可以访问资源。

为了说明，假设 `awesomecloud` 执行产生了变量 `URL` 和 `API_KEY`，则 `app` 服务在环境变量 `DATABASE_URL` 和 `DATABASE_API_KEY` 下运行。

当 Compose 停止应用程序时，`awesomecloud` 二进制文件用于管理 `database` 服务的拆除。

Compose 用于将服务生命周期委托给外部二进制文件的机制在 [Compose 可扩展性文档](https://github.com/docker/compose/tree/main/docs/extension.md) 中有描述。

有关使用 `provider` 属性的更多信息，请参阅 [使用提供程序服务](/manuals/compose/how-tos/provider-services.md)。

#### `type`

`type` 属性是必需的。它定义了 Compose 用于管理设置和拆除生命周期事件的外部组件。

#### `options`

`options` 特定于所选的提供程序，并且不受 compose 规范的验证。

### `pull_policy`

`pull_policy` 定义 Compose 在开始拉取镜像时做出的决定。可能的值是：

- `always`: Compose 始终从注册表拉取镜像。
- `never`: Compose 不从注册表拉取镜像，而是依赖平台缓存的镜像。如果没有缓存的镜像，则报告失败。
- `missing`: 仅当镜像在平台缓存中不可用时，Compose 才会拉取镜像。如果您不使用 [Compose 构建规范](build.md)，这是默认选项。`if_not_present` 被视为此值的别名，以实现向后兼容。即使使用 `missing` 拉取策略，也会始终拉取 `latest` 标签。
- `build`: Compose 构建镜像。如果镜像已存在，Compose 会重新构建它。
- `daily`: 如果上次拉取发生在 24 小时前，Compose 会检查注册表是否有镜像更新。
- `weekly`: 如果上次拉取发生在 7 天前，Compose 会检查注册表是否有镜像更新。
- `every_<duration>`: 如果上次拉取发生在 `<duration>` 之前，Compose 会检查注册表是否有镜像更新。持续时间可以用周 (`w`)、天 (`d`)、小时 (`h`)、分钟 (`m`)、秒 (`s`) 或这些的组合来表示。

```yaml
services:
  test:
    image: nginx
    pull_policy: every_12h
```

### `read_only`

`read_only` 配置服务容器以只读文件系统创建。

### `restart`

`restart` 定义平台在容器终止时应用的策略。

- `no`: 默认重启策略。在任何情况下都不会重新启动容器。
- `always`: 该策略始终重新启动容器，直到其被移除。
- `on-failure[:max-retries]`: 如果退出代码指示错误，该策略会重新启动容器。可选地，限制 Docker 守护程序尝试的重启重试次数。
- `unless-stopped`: 该策略无论退出代码如何都会重新启动容器，但在服务停止或移除时停止重新启动。

```yml
    restart: "no"
    restart: always
    restart: on-failure
    restart: on-failure:3
    restart: unless-stopped
```

您可以在 Docker 运行参考页的[重启策略 (--restart)](/reference/cli/docker/container/run.md#restart) 部分找到有关重启策略的更详细信息。

### `runtime`

`runtime` 指定用于服务容器的运行时。

例如，`runtime` 可以是 [OCI 运行时规范](https://github.com/opencontainers/runtime-spec/blob/master/implementations.md) 的实现名称，例如 "runc"。

```yml
web:
  image: busybox:latest
  command: true
  runtime: runc
```

默认为 `runc`。要使用不同的运行时，请参阅 [替代运行时](/manuals/engine/daemon/alternative-runtimes.md)。

### `scale`

`scale` 指定要为此服务部署的默认容器数量。当两者都设置时，`scale` 必须与 [部署规范](deploy.md#replicas) 中的 `replicas` 属性保持一致。

### `secrets`

{{% include "compose/services-secrets.md" %}}

支持两种不同的语法变体；短语法和长语法。长语法和短语法可用于同一 Compose 文件中的 secrets。

如果机密在平台上不存在或未在 Compose 文件的 [`secrets` 顶层部分](secrets.md) 中定义，Compose 会报告错误。

在顶层 `secrets` 中定义机密并不意味着授予任何服务对其的访问权限。此类授权必须在服务规范中作为 [secrets](secrets.md) 服务元素显式授予。

#### 短语法

短语法变体仅指定机密名称。这授予容器访问机密的权限，并将其作为只读挂载到容器内的 `/run/secrets/<secret_name>`。源名称和目标挂载点都设置为机密名称。

以下示例使用短语法授予 `frontend` 服务访问 `server-certificate` 机密的权限。`server-certificate` 的值设置为文件 `./server.cert` 的内容。

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### 长语法

长语法在如何在服务的容器中创建机密方面提供了更细粒度的控制。

- `source`: 平台上存在的机密名称。
- `target`: 要挂载到服务任务容器中的 `/run/secrets/` 中的文件名称，或者如果需要备用位置，则为文件的绝对路径。如果未指定，则默认为 `source`。
- `uid` 和 `gid`: 拥有服务任务容器内 `/run/secrets/` 中文件的数字 uid 或 gid。
- `mode`: 挂载在服务任务容器内 `/run/secrets/` 中的文件的[权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法表示。默认值为世界可读权限 (模式 `0444`)。如果设置了可写位，则必须忽略。可执行位可以设置。

请注意，当机密的源是 [`file`](secrets.md) 时，Docker Compose 中未实现对 `uid`、`gid` 和 `mode` 属性的支持。这是因为底层使用的绑定挂载不允许 uid 重新映射。

以下示例将 `server-certificate` 机密文件的名称在容器内设置为 `server.cert`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`server-certificate` 的值设置为文件 `./server.cert` 的内容。

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - source: server-certificate
        target: server.cert
        uid: "103"
        gid: "103"
        mode: 0o440
secrets:
  server-certificate:
    file: ./server.cert
```

### `security_opt`

`security_opt` 覆盖每个容器的默认标记方案。

```yml
security_opt:
  - label=user:USER
  - label=role:ROLE
```

有关您可以覆盖的其他默认标记方案，请参阅 [安全配置](/reference/cli/docker/container/run.md#security-opt)。

### `shm_size`

`shm_size` 配置服务容器允许的共享内存大小（Linux 上的 `/dev/shm` 分区）。它被指定为[字节值](extension.md#specifying-byte-values)。

### `stdin_open`

`stdin_open` 配置服务容器以分配 stdin 运行。这与使用 `-i` 标志运行容器相同。有关更多信息，请参阅 [保持 stdin 打开](/reference/cli/docker/container/run.md#interactive)。

支持的值是 `true` 或 `false`。

### `stop_grace_period`

`stop_grace_period` 指定当容器不处理 SIGTERM（或使用 [`stop_signal`](#stop_signal) 指定的任何停止信号）时，Compose 在尝试停止容器之前必须等待多长时间，然后再发送 SIGKILL。它被指定为[持续时间](extension.md#specifying-durations)。

```yml
    stop_grace_period: 1s
    stop_grace_period: 1m30s
```

默认值是 10 秒，容器在发送 SIGKILL 之前退出。

### `stop_signal`

`stop_signal` 定义 Compose 用于停止服务容器的信号。如果未设置，容器将由 Compose 通过发送 `SIGTERM` 停止。

```yml
stop_signal: SIGUSR1
```

### `storage_opt`

`storage_opt` 定义服务的存储驱动程序选项。

```yml
storage_opt:
  size: '1G'
```

### `sysctls`

`sysctls` 定义要在容器中设置的内核参数。`sysctls` 可以使用数组或映射。

```yml
sysctls:
  net.core.somaxconn: 1024
  net.ipv4.tcp_syncookies: 0
```

```yml
sysctls:
  - net.core.somaxconn=1024
  - net.ipv4.tcp_syncookies=0
```

您只能使用内核中命名空间化的 sysctl。Docker 不支持在也修改主机系统的容器内更改 sysctl。有关支持的 sysctl 的概述，请参阅[在运行时配置命名空间内核参数 (sysctls)](/reference/cli/docker/container/run.md#sysctl)。

### `tmpfs`

`tmpfs` 在容器内挂载一个临时文件系统。它可以是单个值或列表。

```yml
tmpfs:
 - <path>
 - <path>:<options>
```

- `path`: 容器内将挂载 tmpfs 的路径。
- `options`: tmpfs 挂载的选项逗号分隔列表。

可用选项：

- `mode`: 设置文件系统权限。
- `uid`: 设置拥有挂载 tmpfs 的用户 ID。
- `gid`: 设置拥有挂载 tmpfs 的组 ID。

```yml
services:
  app:
    tmpfs:
      - /data:mode=755,uid=1009,gid=1009
      - /run
```

### `tty`

`tty` 配置服务容器以 TTY 运行。这与使用 `-t` 或 `--tty` 标志运行容器相同。有关更多信息，请参阅[分配伪 TTY](/reference/cli/docker/container/run.md#tty)。

支持的值是 `true` 或 `false`。

### `ulimits`

`ulimits` 覆盖容器的默认 `ulimits`。它被指定为整数表示单个限制，或映射表示软/硬限制。

```yml
ulimits:
  nproc: 65535
  nofile:
    soft: 20000
    hard: 40000
```

### `use_api_socket`

当设置了 `use_api_socket` 时，容器能够通过 API 套接字与底层容器引擎交互。您的凭据被挂载在容器内，因此容器充当与容器引擎相关的命令的纯委托。通常，容器运行的命令可以 `pull` 和 `push` 到您的注册表。

### `user`

`user` 覆盖用于运行容器进程的用户。默认值由镜像设置，例如 Dockerfile `USER`。如果未设置，则为 `root`。

### `userns_mode`

`userns_mode` 为服务设置用户命名空间。支持的值是特定于平台的，并且可能取决于平台配置。

```yml
userns_mode: "host"
```

### `uts`

{{< summary-bar feature_name="Compose uts" >}}

`uts` 配置为服务容器设置的 UTS 命名空间模式。如果未指定，则由运行时决定分配 UTS 命名空间（如果支持）。可用值为：

- `'host'`: 导致容器使用与主机相同的 UTS 命名空间。

```yml
    uts: "host"
```

### `volumes`

{{% include "compose/services-volumes.md" %}}

以下示例显示了一个命名卷 (`db-data`) 被 `backend` 服务使用，以及为单个服务定义的绑定挂载。

```yml
services:
  backend:
    image: example/backend
    volumes:
      - type: volume
        source: db-data
        target: /data
        volume:
          nocopy: true
          subpath: sub
      - type: bind
        source: /var/run/postgres/postgres.sock
        target: /var/run/postgres/postgres.sock

volumes:
  db-data:
```

有关 `volumes` 顶层元素的更多信息，请参阅 [卷](volumes.md)。

#### 短语法

短语法使用单个冒号分隔值的字符串来指定卷挂载 (`VOLUME:CONTAINER_PATH`)，或访问模式 (`VOLUME:CONTAINER_PATH:ACCESS_MODE`)。

- `VOLUME`: 可以是托管容器的平台上的主机路径（绑定挂载）或卷名称。
- `CONTAINER_PATH`: 卷在容器中挂载的路径。
- `ACCESS_MODE`: 逗号分隔的选项列表 `,`：
  - `rw`: 读写访问。如果未指定任何内容，这是默认值。
  - `ro`: 只读访问。
  - `z`: SELinux 选项，表示绑定挂载的主机内容在多个容器之间共享。
  - `Z`: SELinux 选项，表示绑定挂载的主机内容是私有的，并且不与其他容器共享。

> [!NOTE]
>
> SELinux 重新标记绑定挂载选项在没有 SELinux 的平台上被忽略。

> [!NOTE]
> 相对主机路径仅由部署到本地容器运行时的 Compose 支持。这是因为相对路径是从 Compose 文件的父目录解析的，这只适用于本地情况。当 Compose 部署到非本地平台时，它会拒绝使用相对主机路径的 Compose 文件并报错。为避免与命名卷产生歧义，相对路径应始终以 `.` 或 `..` 开头。

> [!NOTE]
>
> 对于绑定挂载，短语法会在主机上的源路径不存在时创建一个目录。这是为了与 `docker-compose` 旧版向后兼容。
> 可以通过使用长语法并将 `create_host_path` 设置为 `false` 来防止这种情况。

#### 长语法

长表单语法允许您配置短表单中无法表达的附加字段。

- `type`: 挂载类型。可以是 `volume`、`bind`、`tmpfs`、`image`、`npipe` 或 `cluster`。
- `source`: 挂载的源，对于绑定挂载是主机上的路径，对于镜像挂载是 Docker 镜像引用，或者是[顶层 `volumes` 键](volumes.md) 中定义的卷名称。不适用于 tmpfs 挂载。
- `target`: 卷在容器中挂载的路径。
- `read_only`: 将卷设置为只读的标志。
- `bind`: 用于配置附加绑定选项：
  - `propagation`: 用于绑定的传播模式。
  - `create_host_path`: 如果源路径上没有任何内容，则在主机上创建目录。默认为 `true`。
  - `selinux`: SELinux 重新标记选项 `z`（共享）或 `Z`（私有）。
- `volume`: 配置附加卷选项：
  - `nocopy`: 在创建卷时禁止从容器复制数据的标志。
  - `subpath`: 卷内要挂载而不是卷根的路径。
- `tmpfs`: 配置附加 tmpfs 选项：
  - `size`: tmpfs 挂载的大小（以字节为单位，可以是数字或字节单位）。
  - `mode`: tmpfs 挂载的文件模式，作为 Unix 权限位的八进制数。在 Docker Compose 版本 [2.14.0](https://github.com/docker/compose/releases/tag/v2.14.0) 中引入。
- `image`: 配置附加镜像选项：
  - `subpath`: 要挂载的源镜像内的路径，而不是镜像根目录。在 [Docker Compose 版本 2.35.0](https://github.com/docker/compose/releases/tag/v2.35.0) 中可用。
- `consistency`: 挂载的一致性要求。可用值是特定于平台的。

> [!TIP]
>
> 处理大型存储库或单体存储库，或者处理不再随代码库扩展的虚拟文件系统？
> Compose 现在利用[同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 并自动为绑定挂载创建文件共享。
> 确保您使用付费订阅登录 Docker，并在 Docker Desktop 的设置中启用了**访问实验性功能**和**使用 Compose 管理同步文件共享**。

### `volumes_from`

`volumes_from` 挂载来自另一个服务或容器的所有卷。您可以选择指定只读访问 `ro` 或读写 `rw`。如果未指定访问级别，则使用读写访问。

您还可以使用 `container:` 前缀挂载来自不受 Compose 管理的容器的卷。

```yaml
volumes_from:
  - service_name
  - service_name:ro
  - container:container_name
  - container:container_name:rw
```

### `working_dir`

`working_dir` 覆盖容器的工作目录，该目录由镜像指定，例如 Dockerfile 的 `WORKDIR`。