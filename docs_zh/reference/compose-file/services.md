---
linkTitle: Services
title: 在 Docker Compose 中定义服务
description: 探索 services 顶级元素可以包含的所有属性。
keywords: compose, compose specification, services, compose file reference
aliases:
 - /compose/compose-file/05-services/
weight: 20
---

{{% include "compose/services.md" %}}

一个 Compose 文件必须声明一个 `services` 顶级元素，它是一个映射，其键是服务名称的字符串表示，值是服务定义。每个服务定义包含应用于每个服务容器的配置。

每个服务也可以包含一个 `build` 部分，它定义了如何为服务创建 Docker 镜像。
Compose 支持使用此服务定义构建 Docker 镜像。如果不使用，`build` 部分将被忽略，Compose 文件仍然被认为是有效的。构建支持是 Compose 规范的可选部分，在 [Compose Build 规范](build.md) 文档中有详细描述。

每个服务定义了运行其容器所需的运行时约束和要求。`deploy` 部分将这些约束分组，让平台能够调整部署策略，以最好地匹配容器的需求与可用资源。部署支持是 Compose 规范的可选部分，在 [Compose Deploy 规范](deploy.md) 文档中有详细描述。如果不实现，`deploy` 部分将被忽略，Compose 文件仍然被认为是有效的。

## 示例

### 简单示例

以下示例演示了如何定义两个简单服务，设置它们的镜像，映射端口，并使用 Docker Compose 配置基本的环境变量。

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

在以下示例中，`proxy` 服务使用 Nginx 镜像，将本地 Nginx 配置文件挂载到容器中，暴露端口 `80`，并依赖于 `backend` 服务。

`backend` 服务从位于 `backend` 目录中的 Dockerfile 构建镜像，该 Dockerfile 设置为在 `builder` 阶段构建。

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

`annotations` 为容器定义注释。`annotations` 可以使用数组或映射。

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

当 `attach` 被定义并设置为 `false` 时，Compose 不会收集服务日志，直到你显式请求它。

默认服务配置是 `attach: true`。

### `build`

`build` 指定从源创建容器镜像的构建配置，如 [Compose Build 规范](build.md) 中所定义。

### `blkio_config`

`blkio_config` 定义一组配置选项，用于为服务设置块 I/O 限制。

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

为给定设备上的读/写操作设置每秒字节数的限制。列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `rate`: 要么是表示字节数的整数值，要么是表示字节值的字符串。

#### `device_read_iops`, `device_write_iops`

为给定设备上的读/写操作设置每秒操作数的限制。列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `rate`: 表示每秒允许操作数的整数值。

#### `weight`

修改服务相对于其他服务的可用带宽比例。取 10 到 1000 之间的整数值，500 为默认值。

#### `weight_device`

通过设备微调带宽分配。列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `weight`: 10 到 1000 之间的整数值。

### `cpu_count`

`cpu_count` 定义服务容器可用的 CPU 数量。

### `cpu_percent`

`cpu_percent` 定义服务容器可用的 CPU 百分比。

### `cpu_shares`

`cpu_shares` 以整数值定义服务容器相对于其他容器的 CPU 权重。

### `cpu_period`

`cpu_period` 在基于 Linux 内核的平台上配置 CPU CFS（完全公平调度器）周期。

### `cpu_quota`

`cpu_quota` 在基于 Linux 内核的平台上配置 CPU CFS（完全公平调度器）配额。

### `cpu_rt_runtime`

`cpu_rt_runtime` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒为单位的整数值，或 [duration](extension.md#specifying-durations)。

```yml
 cpu_rt_runtime: '400ms'
 cpu_rt_runtime: '95000'
```

### `cpu_rt_period`

`cpu_rt_period` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒为单位的整数值，或 [duration](extension.md#specifying-durations)。

```yml
 cpu_rt_period: '1400us'
 cpu_rt_period: '11000'
```

### `cpus`

`cpus` 定义分配给服务容器的（可能是虚拟的）CPU 数量。这是一个分数。`0.000` 表示无限制。

当设置时，`cpus` 必须与 [Deploy 规范](deploy.md#cpus) 中的 `cpus` 属性一致。

### `cpuset`

`cpuset` 定义允许执行的明确 CPU。可以是范围 `0-3` 或列表 `0,1`

### `cap_add`

`cap_add` 以字符串形式指定额外的容器 [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)。

```yaml
cap_add:
  - ALL
```

### `cap_drop`

`cap_drop` 以字符串形式指定容器要丢弃的 [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)。

```yaml
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

### `cgroup`

{{< summary-bar feature_name="Compose cgroup" >}}

`cgroup` 指定要加入的 cgroup 命名空间。当未设置时，由容器运行时决定使用哪个 cgroup 命名空间（如果支持）。

- `host`: 在容器运行时 cgroup 命名空间中运行容器。
- `private`: 在其自己的私有 cgroup 命名空间中运行容器。

### `cgroup_parent`

`cgroup_parent` 指定容器的可选父 [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html)。

```yaml
cgroup_parent: m-executor-abcd
```

### `command`

`command` 覆盖容器镜像声明的默认命令，例如 Dockerfile 的 `CMD`。

```yaml
command: bundle exec thin -p 3000
```

如果值为 `null`，则使用镜像的默认命令。

如果值为 `[]`（空列表）或 `''`（空字符串），则忽略镜像声明的默认命令，或者换句话说，将其覆盖为空。

> [!NOTE]
>
> 与 Dockerfile 中的 `CMD` 指令不同，`command` 字段不会自动在镜像中定义的 [`SHELL`](/reference/dockerfile.md#shell-form) 指令上下文中运行。如果你的 `command` 依赖于 shell 特定的功能（如环境变量扩展），你需要显式地在 shell 中运行它。例如：
>
> ```yaml
> command: /bin/sh -c 'echo "hello $$HOSTNAME"'
> ```

值也可以是列表，类似于 [exec-form 语法](/reference/dockerfile.md#exec-form) 在 [Dockerfile](/reference/dockerfile.md#exec-form) 中使用。

### `configs`

`configs` 让服务能够适应其行为，而无需重建 Docker 镜像。服务只能在通过 `configs` 属性显式授予时访问 configs。支持两种不同的语法变体。

如果 `config` 在平台上不存在或未在 Compose 文件的 [`configs` 顶级元素](configs.md) 中定义，Compose 会报告错误。

有两种语法定义 configs：简短语法和长语法。

你可以授予服务访问多个 configs 的权限，并且可以混合使用长语法和短语法。

#### 短语法

短语法变体只指定 config 名称。这授予容器访问 config 的权限，并将其作为文件挂载到服务容器的文件系统中。挂载点在容器中的位置默认为 Linux 容器中的 `/<config_name>` 和 Windows 容器中的 `C:\<config-name>`。

以下示例使用短语法授予 `redis` 服务访问 `my_config` 和 `my_other_config` configs 的权限。`my_config` 的值设置为 `./my_config.txt` 文件的内容，`my_other_config` 定义为外部资源，这意味着它已经在平台上定义。如果外部 config 不存在，部署将失败。

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

长语法在服务的任务容器内如何创建 config 方面提供了更多的粒度。

- `source`: config 在平台上的名称。
- `target`: 在服务的任务容器中挂载文件的路径和名称。如果未指定，默认为 `/<source>`。
- `uid` 和 `gid`: 在服务的任务容器中拥有挂载 config 文件的数字 uid 或 gid。
- `mode`: 在服务的任务容器中挂载文件的 [权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示。默认值为可全局读取（`0444`）。可写位必须被忽略。可执行位可以被设置。

以下示例在容器内将 `my_config` 的名称设置为 `redis_config`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`redis` 服务无法访问 `my_other_config` config。

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

`container_name` 是指定自定义容器名称的字符串，而不是默认生成的名称。

```yml
container_name: my-web-container
```

如果 Compose 文件指定了 `container_name`，Compose 不会将服务扩展到一个以上的容器。尝试这样做会导致错误。

`container_name` 遵循正则表达式格式 `[a-zA-Z0-9][a-zA-Z0-9_.-]+`

### `credential_spec`

`credential_spec` 为托管服务账户配置凭据规范。

如果你有使用 Windows 容器的服务，可以使用 `file:` 和 `registry:` 协议用于 `credential_spec`。Compose 还支持额外的协议以满足自定义用例。

`credential_spec` 必须采用 `file://<filename>` 或 `registry://<value-name>` 格式。

```yml
credential_spec:
  file: my-credential-spec.json
```

使用 `registry:` 时，凭据规范从守护进程主机上的 Windows 注册表中读取。具有给定名称的注册表值必须位于：

```bash
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\Containers\CredentialSpecs
```

以下示例从注册表中名为 `my-credential-spec` 的值加载凭据规范：

```yml
credential_spec:
  registry: my-credential-spec
```

#### 示例 gMSA 配置

为服务配置 gMSA 凭据规范时，你只需要使用 `config` 指定凭据规范，如以下示例所示：

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

短语法变体只指定依赖项的服务名称。服务依赖导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 按依赖顺序移除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前移除。

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

Compose 保证依赖服务在启动依赖服务之前已启动。Compose 在启动依赖服务之前等待依赖服务“就绪”。

#### 长语法

长格式语法允许配置在短格式中无法表达的附加字段。

- `restart`: 当设置为 `true` 时，Compose 在更新依赖服务后重启此服务。这适用于由 Compose 操作控制的显式重启，不包括容器运行时在容器死亡后自动重启。在 Docker Compose 版本 [2.17.0](/manuals/compose/releases/release-notes.md#2170) 中引入。

- `condition`: 设置依赖满足的条件
  - `service_started`: 等同于前面描述的短语法
  - `service_healthy`: 指定依赖在启动依赖服务之前预期为“健康”（由 [`healthcheck`](#healthcheck) 指示）
  - `service_completed_successfully`: 指定依赖在启动依赖服务之前预期成功完成。
- `required`: 当设置为 `false` 时，Compose 只在依赖服务未启动或不可用时发出警告。如果未定义，默认值为 `true`。在 Docker Compose 版本 [2.20.0](/manuals/compose/releases/release-notes.md#2200) 中引入。

服务依赖导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。

- Compose 等待依赖的健康检查通过，这些依赖标记为 `service_healthy`。在以下示例中，`db` 预期在 `web` 创建之前为“健康”。

- Compose 按依赖顺序移除服务。在以下示例中，`web` 在 `db` 和 `redis` 之前移除。

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

Compose 保证依赖服务在启动依赖服务之前已启动。Compose 保证标记为 `service_healthy` 的依赖服务在启动依赖服务之前为“健康”。

### `deploy`

`deploy` 指定服务部署和生命周期的配置，如 [Compose Deploy 规范](deploy.md) 中所定义。

### `develop`

{{< summary-bar feature_name="Compose develop" >}}

`develop` 指定与源保持同步的容器开发配置，如 [Development Section](develop.md) 中所定义。

### `device_cgroup_rules`

`device_cgroup_rules` 定义此容器的设备 cgroup 规则列表。格式与 Linux 内核在 [Control Groups Device Whitelist Controller](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/devices.html) 中指定的格式相同。

```yml
device_cgroup_rules:
  - 'c 1:3 mr'
  - 'a 7:* rmw'
```

### `devices`

`devices` 定义以 `HOST_PATH:CONTAINER_PATH[:CGROUP_PERMISSIONS]` 格式创建的容器的设备映射列表。

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
  - 9.