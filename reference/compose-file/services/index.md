# 在 Docker Compose 中定义服务



服务是应用程序中计算资源的抽象定义，可以独立于其他组件进行扩展或替换。服务由平台根据复制要求和部署约束运行的一组容器支持。由于服务由容器支持，因此它们由 Docker 镜像和一组运行时参数定义。服务中的所有容器都使用这些参数以相同的方式创建。

Compose 文件必须声明一个 `services` 顶级元素作为映射，其键是服务名称的字符串表示，其值是服务定义。服务定义包含应用于每个服务容器的配置。

每个服务还可以包含一个 `build` 部分，该部分定义如何为服务创建 Docker 镜像。Compose 支持使用此服务定义构建 Docker 镜像。如果未使用，`build` 部分将被忽略，Compose 文件仍被视为有效。构建支持是 Compose 规范的一个可选方面，在 [Compose 构建规范](build.md) 文档中有详细描述。

每个服务都定义了运行其容器的运行时约束和要求。`deploy` 部分将这些约束分组，并让平台调整部署策略以最好地匹配容器的需求与可用资源。部署支持是 Compose 规范的一个可选方面，在 [Compose 部署规范](deploy.md) 文档中有详细描述。如果未实现，`deploy` 部分将被忽略，Compose 文件仍被视为有效。

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

`backend` 服务从位于 `backend` 目录中的 Dockerfile 构建镜像，该镜像设置在 `builder` 阶段构建。

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





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2200">2.20.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



当定义 `attach` 并设置为 `false` 时，Compose 不会收集服务日志，直到您显式请求它。

默认服务配置是 `attach: true`。

### `build`

`build` 指定从源代码创建容器镜像的构建配置，如 [Compose 构建规范](build.md) 中所定义。

### `blkio_config`

`blkio_config` 定义了一组配置选项，用于设置服务的块 I/O 限制。

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
取值范围为 10 到 1000 的整数值，默认值为 500。

#### `weight_device`

按设备微调带宽分配。列表中的每个项目必须有两个键：

- `path`: 定义受影响设备的符号路径。
- `weight`: 10 到 1000 之间的整数值。

### `cpu_count`

`cpu_count` 定义服务容器可用的 CPU 数量。

### `cpu_percent`

`cpu_percent` 定义可用 CPU 的可用百分比。

### `cpu_shares`

`cpu_shares` 定义为一个整数值，表示服务容器相对于其他容器的相对 CPU 权重。

### `cpu_period`

`cpu_period` 配置 CPU CFS（完全公平调度器）周期，当平台基于 Linux 内核时。

### `cpu_quota`

`cpu_quota` 配置 CPU CFS（完全公平调度器）配额，当平台基于 Linux 内核时。

### `cpu_rt_runtime`

`cpu_rt_runtime` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒作为单位的整数值，也可以是 [持续时间](extension.md#specifying-durations)。

```yml
 cpu_rt_runtime: '400ms'
 cpu_rt_runtime: '95000'
```

### `cpu_rt_period`

`cpu_rt_period` 为支持实时调度器的平台配置 CPU 分配参数。它可以是使用微秒作为单位的整数值，也可以是 [持续时间](extension.md#specifying-durations)。

```yml
 cpu_rt_period: '1400us'
 cpu_rt_period: '11000'
```

### `cpus`

`cpus` 定义要分配给服务容器的（可能是虚拟的）CPU 数量。这是一个小数。
`0.000` 表示无限制。

设置时，`cpus` 必须与 [部署规范](deploy.md#cpus) 中的 `cpus` 属性一致。

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





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2150">2.15.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



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

如果值为 `null`，则使用镜像中的默认命令。

如果值为 `[]`（空列表）或 `''`（空字符串），则镜像声明的默认命令将被忽略，或者换句话说，被覆盖为空。

> [!NOTE]
>
> 与 Dockerfile 中的 `CMD` 指令不同，`command` 字段不会自动在镜像定义的 [`SHELL`](/reference/dockerfile.md#shell-form) 指令的上下文中运行。如果您的 `command` 依赖于特定于 shell 的功能，例如环境变量扩展，则需要在 shell 中显式运行它。例如：
>
> ```yaml
> command: /bin/sh -c 'echo "hello $$HOSTNAME"'
> ```

该值也可以是一个列表，类似于 [Dockerfile](/reference/dockerfile.md#exec-form) 使用的 [exec 形式语法](/reference/dockerfile.md#exec-form)。

### `configs`

`configs` 让服务调整其行为，而无需重建 Docker 镜像。服务只有在通过 `configs` 属性显式授权时才能访问配置。支持两种不同的语法变体。

如果 `config` 在平台上不存在或未在 Compose 文件的 [`configs` 顶级元素](configs.md) 中定义，Compose 会报告错误。

为 configs 定义了两种语法：短语法和长语法。

您可以授予服务对多个配置的访问权限，并且可以混合使用长语法和短语法。

#### 短语法

短语法变体仅指定配置名称。这授予容器对配置的访问权限，并将其作为文件挂载到服务容器的文件系统中。容器内的挂载点位置在 Linux 容器中默认为 `/<config_name>`，在 Windows 容器中默认为 `C:\<config-name>`。

以下示例使用短语法授予 `redis` 服务对 `my_config` 和 `my_other_config` 配置的访问权限。`my_config` 的值设置为文件 `./my_config.txt` 的内容，`my_other_config` 定义为外部资源，这意味着它已在平台上定义。如果外部配置不存在，则部署失败。

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

长语法在如何在服务的任务容器中创建配置方面提供了更精细的控制。

- `source`: 平台上存在的配置名称。
- `target`: 要挂载到服务任务容器中的文件路径和名称。如果未指定，则默认为 `/<source>`。
- `uid` 和 `gid`: 挂载的配置文件在服务任务容器中拥有的数字 uid 或 gid。
- `mode`: 挂载在服务任务容器中的文件的 [权限](https://wintelguy.com/permissions-calc.pl)，以八进制表示法表示。默认值为世界可读 (`0444`)。可写位必须被忽略。可执行位可以设置。

以下示例将 `my_config` 的名称在容器内设置为 `redis_config`，将模式设置为 `0440`（组可读），并将用户和组设置为 `103`。`redis` 服务无权访问 `my_other_config` 配置。

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



使用 `depends_on` 属性，您可以控制服务的启动和关闭顺序。如果服务之间紧密耦合，且启动顺序会影响应用程序的功能，这一属性将非常有用。

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

长形式语法支持配置短形式无法表达的附加字段。

- `restart`: 当设置为 `true` 时，Compose 在更新依赖服务后重新启动此服务。这适用于由 Compose 操作控制的显式重新启动，不包括容器运行时在容器死亡后的自动重新启动。在 Docker Compose 版本 [2.17.0](/manuals/compose/releases/release-notes.md#2170) 中引入。
- `condition`: 设置依赖项被视为满足的条件
  - `service_started`: 等同于前面描述的短语法。
  - `service_healthy`: 指定依赖项在启动依赖服务之前需要是“健康的”（由 [`healthcheck`](#healthcheck) 指示）。
  - `service_completed_successfully`: 指定依赖项在启动依赖服务之前需要成功完成运行。
- `required`: 当设置为 `false` 时，如果依赖服务未启动或不可用，Compose 仅发出警告。如果未定义，`required` 的默认值为 `true`。在 Docker Compose 版本 [2.20.0](/manuals/compose/releases/release-notes.md#2200) 中引入。

服务依赖项会导致以下行为：

- Compose 按依赖顺序创建服务。在以下示例中，`db` 和 `redis` 在 `web` 之前创建。
- Compose 等待标记为 `service_healthy` 的依赖项的健康检查通过。在以下示例中，`db` 在 `web` 创建之前需要是“健康的”。
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

`deploy` 指定服务的部署和生命周期的配置，如 [Compose 部署规范](deploy.md) 中所定义。

### `develop`





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2220">2.22.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



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

`domainname` 声明用于服务容器的自定义域名。它必须是有效的 RFC 1123 主机名。

### `driver_opts`





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2271">2.27.1</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



`driver_opts` 指定一个选项列表作为键值对传递给驱动程序。这些选项是驱动程序相关的。

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

如果 `entrypoint` 非 null，Compose 会忽略镜像中的任何默认命令，例如 Dockerfile 中的 `CMD` 指令。

另请参阅 [`command`](#command) 以设置或覆盖入口点进程要执行的默认命令。

在其短形式中，值可以定义为字符串：
```yml
entrypoint: /code/entrypoint.sh
```

或者，该值也可以是一个列表，类似于 [Dockerfile](https://docs.docker.com/reference/dockerfile/#cmd)：

```yml
entrypoint:
  - php
  - -d
  - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
  - -d
  - memory_limit=-1
  - vendor/bin/phpunit
```

如果值为 `null`，则使用镜像中的默认入口点。

如果值为 `[]`（空列表）或 `''`（空字符串），则镜像声明的默认入口点将被忽略，或者换句话说，被覆盖为空。

### `env_file`



`env_file` 属性用于指定一个或多个包含要传递给容器的环境变量的文件。

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





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2271">2.24.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



`required` 属性默认为 `true`。当 `required` 设置为 `false` 且 `.env` 文件缺失时，Compose 会静默忽略该条目。

```yml
env_file:
  - path: ./default.env
    required: true # default
  - path: ./override.env
    required: false
```

#### `format`





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2300">2.30.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



`format` 属性允许您为 `env_file` 使用替代文件格式。如果未设置，`env_file` 将根据 [`Env_file` 格式](#env_file-format) 中概述的 Compose 规则进行解析。

`raw` 格式允许您使用带有 key=value 项的 `env_file`，但 Compose 不会尝试解析值进行插值。这使您可以按原样传递值，包括引号和 `$` 符号。

```yml
env_file:
  - path: ./default.env
    format: raw
```

#### `Env_file` 格式

`.env` 文件中的每一行必须是 `VAR[=[VAL]]` 格式。适用以下语法规则：

- 以 `#` 开头的行被视为注释并被忽略。
- 空行被忽略。
- 无引号和双引号 (`"`) 的值应用 [插值](interpolation.md)。
- 每行代表一个键值对。值可以选择性地加引号。
- 分隔键和值的分隔符可以是 `=` 或 `:`。
- 值前后的空格被忽略。
  - `VAR=VAL` -> `VAL`
  - `VAR="VAL"` -> `VAL`
  - `VAR='VAL'` -> `VAL`
  - `VAR: VAL` -> `VAL`
  - `VAR = VAL  ` -> `VAL` <!-- markdownlint-disable-line no-space-in-code -->
- 无引号值的内联注释前面必须有空格。
  - `VAR=VAL # comment` -> `VAL`
  - `VAR=VAL# not a comment` -> `VAL# not a comment`
- 引号值的内联注释必须跟在闭引号之后。
  - `VAR="VAL # not a comment"` -> `VAL # not a comment`
  - `VAR="VAL" # comment` -> `VAL`
- 单引号 (`'`) 值按字面意思使用。
  - `VAR='$OTHER'` -> `$OTHER`
  - `VAR='${OTHER}'` -> `${OTHER}`
- 引号可以用 `\` 转义。
  - `VAR='Let\'s go!'` -> `Let's go!`
  - `VAR="{\"hello\": \"json\"}"` -> `{"hello": "json"}`
- 常见的 shell 转义序列，包括 `\n`、`\r`、`\t` 和 `\\`，在双引号值中受支持。
  - `VAR="some\tvalue"` -> `some  value`
  - `VAR='some\tvalue'` -> `some\tvalue`
  - `VAR=some\tvalue` -> `some\tvalue`

`VAL` 可以省略，在这种情况下变量值为空字符串。
`=VAL` 可以省略，在这种情况下变量未设置。

```bash
# Set Rails/Rack environment
RACK_ENV=development
VAR="quoted"
```

### `environment`



`environment` 属性定义了在容器中设置的环境变量。`environment` 可以使用数组或映射。
任何布尔值：true、false、yes、no，都应该用引号括起来，以确保它们不会被 YAML 解析器转换为 True 或 False。

环境变量可以通过单个键（没有值或等号）声明。在这种情况下，Compose 依赖您来解析值。如果值未解析，则变量未设置，并从服务容器环境中移除。

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

`expose` 定义 Compose 从容器暴露的（传入）端口或端口范围。这些端口必须对链接的服务可访问，并且不应发布到主机机器。只能指定内部容器端口。

语法是 `<portnum>/[<proto>]` 或 `<startport-endport>/[<proto>]` 表示端口范围。如果未显式设置，则使用 `tcp` 协议。

```yml
expose:
  - "3000"
  - "8000"
  - "8080-8085/tcp"
```

> [!NOTE]
>
> 如果镜像的 Dockerfile 已经暴露了端口，即使您的 Compose 文件中未设置 `expose`，它对网络上的其他容器也是可见的。

### `extends`

`extends` 允许您在不同文件甚至完全不同的项目之间共享通用配置。使用 `extends`，您可以在一个地方定义一组通用的服务选项，并从任何地方引用它。您可以引用另一个 Compose 文件并选择您也想在自己的应用程序中使用的服务，并能够覆盖一些属性以满足自己的需求。

您可以在任何服务上使用 `extends` 以及其他配置键。`extends` 值必须是一个映射，定义为必需的 `service` 和可选的 `file` 键。

```yaml
extends:
  file: common.yml
  service: webapp
```

- `service`: 定义作为基础引用的服务名称，例如 `web` 或 `database`。
- `file`: 定义该服务的 Compose 配置文件的位置。

#### 限制

当使用 `extends` 引用服务时，它可以声明对其他资源的依赖。这些依赖可以通过 `volumes`、`networks`、`configs`、`secrets`、`links`、`volumes_from` 或 `depends_on` 等属性显式定义。或者，依赖项可以在命名空间声明（如 `ipc`、`pid` 或 `network_mode`）中使用 `service:{name}` 语法引用另一个服务。

Compose 不会自动将这些引用的资源导入扩展模型。您有责任确保所有必需的资源都在依赖于扩展的模型中显式声明。

不支持使用 `extends` 的循环引用，Compose 在检测到时会返回错误。

#### 查找引用的服务

`file` 值可以是：

- 不存在。
  这表示引用同一 Compose 文件中的另一个服务。
- 文件路径，可以是：
  - 相对路径。此路径被视为相对于主 Compose 文件的位置。
  - 绝对路径。

由 `service` 表示的服务必须存在于标识的引用 Compose 文件中。
如果出现以下情况，Compose 会返回错误：

- 找不到由 `service` 表示的服务。
- 找不到由 `file` 表示的 Compose 文件。

#### 合并服务定义

两个服务定义，当前 Compose 文件中的主定义和由 `extends` 指定的引用定义，按以下方式合并：

- 映射：主服务定义映射中的键覆盖引用服务定义映射中的键。未被覆盖的键按原样包含。
- 序列：项目组合在一起形成一个新的序列。元素的顺序被保留，引用的项目在前，主项目在后。
- 标量：主服务定义中的键优先于引用中的键。

##### 映射

以下键应视为映射：`annotations`、`build.args`、`build.labels`、`build.extra_hosts`、`deploy.labels`、`deploy.update_config`、`deploy.rollback_config`、`deploy.restart_policy`、`deploy.resources.limits`、`environment`、`healthcheck`、`labels`、`logging.options`、`sysctls`、`storage_opt`、`extra_hosts`、`ulimits`。

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

`blkio_config.device_read_bps`、`blkio_config.device_read_iops`、`blkio_config.device_write_bps`、`blkio_config.device_write_iops`、`devices` 和 `volumes` 下的项目也被视为映射，其中键是容器内的目标路径。

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

如果引用的服务定义包含 `extends` 映射，则其下的项目将简单地复制到新的合并定义中。然后再次启动合并过程，直到没有 `extends` 键剩余。

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

以下键应视为序列：`cap_add`、`cap_drop`、`configs`、`deploy.placement.constraints`、`deploy.placement.preferences`、`deploy.reservations.generic_resources`、`device_cgroup_rules`、`expose`、`external_links`、`ports`、`secrets`、`security_opt`。
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

如果使用列表语法，以下键也应视为序列：`dns`、`dns_search`、`env_file`、`tmpfs`。与前面提到的序列字段不同，合并产生的重复项不会被删除。

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

短语法在列表中使用纯字符串。值必须以 `HOSTNAME=IP` 的形式为主机设置主机名和 IP 地址。

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

首选分隔符 `=`，但也可以使用 `:`。在 Docker Compose 版本 [2.24.1](/manuals/compose/releases/release-notes.md#2241) 中引入。例如：

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





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="/compose/releases/release-notes/#2300">2.30.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



`gpus` 指定要分配给容器使用的 GPU 设备。这等同于具有隐式 `gpu` 功能的 [设备请求](deploy.md#devices)。

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

`group_add` 指定容器内用户必须是其成员的其他组（按名称或编号）。

此功能有用的示例是当多个容器（以不同用户身份运行）需要读取或写入共享卷上的同一文件时。该文件可以由所有容器共享的组拥有，并在 `group_add` 中指定。

```yml
services:
  myservice:
    image: alpine
    group_add:
      - mail
```

在创建的容器内运行 `id` 必须显示该用户属于 `mail` 组，如果未声明 `group_add`，则不会是这种情况。

### `healthcheck`



`healthcheck` 属性声明了一个用于确定服务容器是否“健康”的检查。其工作方式与服务的 Docker 镜像在 Dockerfile 中设置的 `HEALTHCHECK` 指令相同，并且具有相同的默认值。您的 Compose 文件可以覆盖 Dockerfile 中设置的值。

有关 `HEALTHCHECK` 的更多信息，请参阅 [Dockerfile 参考](/reference/dockerfile.md#healthcheck)。

```yml
healthcheck:
  test: ["
