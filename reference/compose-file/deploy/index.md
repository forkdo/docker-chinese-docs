# Compose 部署规范



Deploy 是 Compose Specification 的一个可选部分。它提供了一组部署规范，用于管理容器在不同环境中的行为。

## 属性

### `endpoint_mode`

`endpoint_mode` 指定外部客户端连接到服务时所使用的服务发现方法。Compose 部署规范定义了两个标准值：

* `endpoint_mode: vip`: 为服务分配一个虚拟 IP (VIP)，作为客户端在网络上访问服务的前端。平台在客户端和运行服务的节点之间路由请求，客户端无需知晓有多少节点参与服务，也无需知晓它们的 IP 地址或端口。

* `endpoint_mode: dnsrr`: 平台为服务设置 DNS 条目，使得对服务名称的 DNS 查询返回一个 IP 地址列表（DNS 轮询），客户端直接连接到其中一个地址。

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "8080:80"
    deploy:
      mode: replicated
      replicas: 2
      endpoint_mode: vip
```

### `labels`

`labels` 为服务指定元数据。这些标签仅设置在服务上，而不会设置在服务的任何容器上。这假设平台拥有某种原生的“服务”概念，可以与 Compose 应用模型相匹配。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      labels:
        com.example.description: "此标签将出现在 web 服务上"
```

### `mode`

`mode` 定义用于运行服务或作业的复制模型。选项包括：

- `global`: 确保每个物理节点上恰好有一个任务持续运行，直到停止。
- `replicated`: 在节点间持续运行指定数量的任务，直到停止（默认）。
- `replicated-job`: 执行定义数量的任务，直到达到完成状态（以代码 0 退出）。
   - 任务总数由 `replicas` 决定。
   - 可以使用 `max-concurrent` 选项限制并发（仅限 CLI）。
- `global-job`: 每个物理节点执行一个任务，并达到完成状态（以代码 0 退出）。
   - 在添加新节点时自动运行。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: global

  batch-job:
    image: example/processor
    deploy:
      mode: replicated-job
      replicas: 5

  maintenance:
    image: example/updater
    deploy:
      mode: global-job
```

> [!NOTE] 
> - 作业模式（`replicated-job` 和 `global-job`）专为完成并以代码 0 退出的任务设计。
> - 已完成的任务会一直保留，直到被显式移除。
> - 用于控制并发的选项（如 `max-concurrent`）仅通过 CLI 支持，在 Compose 中不可用。

有关作业选项和行为的更多详细信息，请参阅 [Docker CLI 文档](/reference/cli/docker/service/create.md#running-as-a-job)

### `placement`

`placement` 指定约束和偏好，供平台选择运行服务容器的物理节点。

#### `constraints`

`constraints` 定义平台节点必须满足的必要属性，才能运行服务容器。更多示例，请参阅 [CLI 参考文档](/reference/cli/docker/service/create.md#constraint)。

```yml
deploy:
  placement:
    constraints:
      - node.labels.disktype==ssd
```

#### `preferences`

`preferences` 定义一种策略（目前唯一支持的策略是 `spread`），用于将任务均匀分布到数据中心节点标签的各个值上。更多示例，请参阅 [CLI 参考文档](/reference/cli/docker/service/create.md#placement-pref)。

```yml
deploy:
  placement:
    preferences:
      - spread: node.labels.zone
```

### `replicas`

如果服务是 `replicated`（默认值），`replicas` 指定在任何给定时间应运行的容器数量。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      mode: replicated
      replicas: 6
```

### `resources`

`resources` 为容器在平台上运行配置物理资源约束。这些约束可以配置为：

- `limits`: 平台必须阻止容器分配更多资源。
- `reservations`: 平台必须保证容器至少可以分配配置的资源量。

```yml
services:
  frontend:
    image: example/webapp
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 50M
          pids: 1
        reservations:
          cpus: '0.25'
          memory: 20M
```

#### `cpus`

`cpus` 配置容器可用 CPU 资源的限制或预留，以核心数表示。

#### `memory`

`memory` 配置容器可分配内存量的限制或预留，设置为表示[字节值](extension.md#specifying-byte-values)的字符串。

#### `pids`

`pids` 调整容器的 PIDs 限制，设置为整数。

#### `devices`

`devices` 配置容器可使用设备的预留。它包含一个预留列表，每个预留设置为一个对象，包含以下参数：`capabilities`、`driver`、`count`、`device_ids` 和 `options`。

设备使用能力列表进行预留，因此 `capabilities` 是唯一必需的字段。设备必须满足所有请求的能力才能成功预留。

##### `capabilities`

`capabilities` 设置为一个字符串列表，表示通用能力和驱动程序特定的能力。目前识别以下通用能力：

- `gpu`: 图形加速器
- `tpu`: AI 加速器

为避免名称冲突，驱动程序特定的能力必须以驱动程序名称为前缀。例如，预留一个支持 NVIDIA CUDA 的加速器可能如下所示：

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
```

##### `driver`

可以使用 `driver` 字段请求预留设备的不同驱动程序。该值指定为字符串。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["nvidia-compute"]
          driver: nvidia
```

##### `count`

如果 `count` 设置为 `all` 或未指定，Compose 会预留所有满足请求能力的设备。否则，Compose 会预留至少指定数量的设备。该值指定为整数。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["tpu"]
          count: 2
```

`count` 和 `device_ids` 字段是互斥的。如果同时指定两者，Compose 会返回错误。

##### `device_ids`

如果设置了 `device_ids`，Compose 会预留具有指定 ID 的设备，前提是它们满足请求的能力。该值指定为字符串列表。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          device_ids: ["GPU-f123d1c9-26bb-df9b-1c23-4a731f61d8c7"]
```

`count` 和 `device_ids` 字段是互斥的。如果同时指定两者，Compose 会返回错误。

##### `options`

可以使用 `options` 以键值对的形式设置驱动程序特定的选项。

```yml
deploy:
  resources:
    reservations:
      devices:
        - capabilities: ["gpu"]
          driver: gpuvendor
          options:
            virtualization: false
```

### `restart_policy`

`restart_policy` 配置容器退出时是否以及如何重新启动。如果未设置 `restart_policy`，Compose 会考虑服务配置中设置的 `restart` 字段。

- `condition`. 设置为：
  - `none`，无论退出状态如何，容器都不会自动重新启动。
  - `on-failure`，如果容器因错误（表现为非零退出代码）而退出，则重新启动容器。
  - `any`（默认），无论退出状态如何，容器都会重新启动。
- `delay`: 两次重启尝试之间的等待时间，指定为[持续时间](extension.md#specifying-durations)。默认为 0，表示可以立即进行重启尝试。
- `max_attempts`: 在放弃之前允许的最大失败重启尝试次数。（默认值：无限次重试。）仅当容器在 `window` 定义的时间内未能成功重启时，失败尝试才会计入 `max_attempts`。例如，如果 `max_attempts` 设置为 `2`，并且容器在第一次尝试中未能在窗口内重启，Compose 将继续重试，直到发生两次此类失败尝试，即使这意味着尝试超过两次。
- `window`: 重启后等待以确定是否成功的时间量，指定为[持续时间](extension.md#specifying-durations)（默认值：在重启后立即评估结果）。

```yml
deploy:
  restart_policy:
    condition: on-failure
    delay: 5s
    max_attempts: 3
    window: 120s
```

### `rollback_config`

`rollback_config` 配置在更新失败时应如何回滚服务。

- `parallelism`: 一次回滚的容器数量。如果设置为 0，则所有容器同时回滚。
- `delay`: 每组容器回滚之间等待的时间（默认 0s）。
- `failure_action`: 回滚失败时的操作。`continue` 或 `pause` 之一（默认 `pause`）。
- `monitor`: 每次任务更新后监控失败的持续时间 `(ns|us|ms|s|m|h)`（默认 0s）。
- `max_failure_ratio`: 回滚期间可容忍的失败率（默认 0）。
- `order`: 回滚期间的操作顺序。`stop-first`（在启动新任务之前停止旧任务）或 `start-first`（首先启动新任务，运行中的任务会短暂重叠）之一（默认 `stop-first`）。

### `update_config`

`update_config` 配置应如何更新服务。对于配置滚动更新非常有用。

- `parallelism`: 一次更新的容器数量。
- `delay`: 更新一组容器之间等待的时间。
- `failure_action`: 更新失败时的操作。`continue`、`rollback` 或 `pause` 之一（默认：`pause`）。
- `monitor`: 每次任务更新后监控失败的持续时间 `(ns|us|ms|s|m|h)`（默认 0s）。
- `max_failure_ratio`: 更新期间可容忍的失败率。
- `order`: 更新期间的操作顺序。`stop-first`（在启动新任务之前停止旧任务）或 `start-first`（首先启动新任务，运行中的任务会短暂重叠）之一（默认 `stop-first`）。

```yml
deploy:
  update_config:
    parallelism: 2
    delay: 10s
    order: stop-first
```
