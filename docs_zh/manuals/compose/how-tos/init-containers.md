<!-- FILE: manuals/compose/how-tos/init-containers.md -->

---
title: 在 Compose 中使用 Init 容器
linkTitle: 使用 Init 容器
weight: 120
description: 使用 pre_start 初始化容器，在 Docker Compose 中某个服务启动前运行初始化任务。
keywords: docker compose init containers, pre_start, docker compose migrations, volume permissions, docker compose lifecycle
params:
  sidebar:
    badge:
      color: green
      text: New
---

{{< summary-bar feature_name="Compose pre_start" >}}

Init 容器（init containers）是在服务主容器启动之前运行的短期容器。它们按顺序执行，每个容器都会运行直至完成，下一个才会开始。如果任何步骤以非零代码退出，该服务将不会启动。

可将它们用于必须在应用启动前完成的初始化工作：运行数据库迁移、修复卷权限、生成动态配置，或执行任何有序的先决条件序列。

Compose 将 init 容器建模为 [`pre_start`](/reference/compose-file/services.md#pre_start) 生命周期钩子。与 [`post_start`](/reference/compose-file/services.md#post_start) 和 [`pre_stop`](/reference/compose-file/services.md#pre_stop) 在正在运行的服务容器内执行命令不同，每个 `pre_start` 步骤都运行在它自己独立的临时容器中——该容器在服务容器创建之后、启动之前创建。

## 何时不应使用 Init 容器

对于静态文件和密钥，请改用原生的 [`configs`](/reference/compose-file/configs.md) 和 [`secrets`](/reference/compose-file/secrets.md) 顶级元素。Compose 会将它们以可配置的目标路径、模式、UID 和 GID 直接挂载到容器中。无需 init 容器。

对于拥有自身生命周期的后台任务——如定时备份、退出后清理、周期性维护——init 容器并非合适的工具。这些任务独立于服务启动运行，而不是在其之前运行。

## `pre_start` 容器如何运行

服务 `pre_start` 列表中的每一步：

- 运行在它自己独立的临时容器中，该容器在服务容器创建之后、启动之前创建。
- 默认继承服务的镜像。设置 `image` 可覆盖。
- 加入与服务相同的网络，因此可访问 [`depends_on`](/reference/compose-file/services.md#depends_on) 中声明的服务。
- 共享服务的卷挂载，因此写入共享卷的文件对服务立即可见。
- 必须退出 `0`，后续步骤以及服务本身才能启动。非零退出会中止该服务及其依赖项的启动。

如果某 `pre_start` 步骤之前已成功执行、其定义未变更，或在 `restart` 策略下服务容器重启，则在后续 `docker compose up` 运行中将跳过该步骤。当定义发生变更、上一次运行失败，或使用 `--force-recreate` 重新创建服务时，它会重新运行。

## 示例

### 在应用启动前运行数据库迁移

在以下示例中，`app` 等待 `db` 变为健康状态，然后在一个复用应用镜像的临时容器中运行 `./manage.py migrate`。只有当迁移退出 `0` 后，服务容器才会启动。

```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
    pre_start:
      - command: ["./manage.py", "migrate"]

  db:
    image: postgres:18
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      retries: 5
      start_period: 30s
      timeout: 10s
```

如果迁移失败，`app` 不会启动，失败信息会在 `docker compose up` 的输出中报告。

### 在非根服务启动前修复卷所有权

命名卷以 root 所有权创建。当服务以非根用户运行时，你可以使用 `pre_start` 步骤在挂载卷之前调整所有权。

```yaml
services:
  app:
    image: myapp:latest
    user: "1000:1000"
    volumes:
      - data:/data
    pre_start:
      - image: busybox
        user: root
        command: sh -c 'chown -R 1000:1000 /data'

volumes:
  data:
```

`pre_start` 步骤使用了不同的镜像（`busybox`）并以 `root` 身份运行，即使服务本身以用户 `1000` 运行。

### 链接多个初始化步骤

`pre_start` 步骤按声明的顺序运行。只有当前一步退出 `0` 后，下一步才会启动。在以下示例中，应用会先等待迁移完成，再等待种子数据加载，然后才启动。

```yaml
services:
  app:
    image: myapp:latest
    depends_on:
      db:
        condition: service_healthy
    pre_start:
      - command: ["./manage.py", "migrate"]
      - command: ["./manage.py", "loaddata", "fixtures.json"]

  db:
    image: postgres:18
```

每一步都运行在它自己独立的临时容器中。如果第二步失败，第一步不会被回滚，但 `app` 不会启动。

### 替代一次性服务（one-shot service）模式

在 `pre_start` 出现之前，表达「在 Y 启动前运行 X」的常见做法是将初始化工作建模为一个带有 `restart: "no"` 的服务，并让主服务通过 `condition: service_completed_successfully` 依赖它：

```yaml
services:
  migrate:
    image: myapp:latest
    command: ["./manage.py", "migrate"]
    restart: "no"

  app:
    image: myapp:latest
    depends_on:
      migrate:
        condition: service_completed_successfully
```

使用 `pre_start` 表达的等价写法：

```yaml
services:
  app:
    image: myapp:latest
    pre_start:
      - command: ["./manage.py", "migrate"]
```

`pre_start` 更可取，因为：

- 初始化工作被建模为服务的从属步骤，而不是一个立即退出的对等（peer）服务。
- 已完成的步骤不会作为已退出的服务出现在 `docker compose ps` 中。
- 链接多个初始化步骤不需要在一次性服务之间建立复杂的 `depends_on` 依赖关系网。
- 临时容器默认继承服务的镜像，因此无需重复声明 `image:`。

当初始化工作是被多个服务共享的关注点，或者它需要独立于任何单一服务被寻址时，一次性服务模式仍有其用武之地。

## 限制

- `pre_start` 针对服务整体运行一次，而不是每个副本运行一次（`per_replica: false`）。按副本执行（`per_replica: true`）尚不支持。
- 跨副本共享的卷挂载（命名卷、绑定挂载）可以从 `pre_start` 步骤访问。诸如 `tmpfs` 或匿名卷之类按实例的挂载，无法通过单次共享运行来寻址。
- 当你扩容服务时，`pre_start` 不会重新触发。一个步骤仅在定义变更、先前失败或使用 `--force-recreate` 时才会再次运行。

## 参考与附加信息

- [`pre_start`](/reference/compose-file/services.md#pre_start)
- [`post_start`](/reference/compose-file/services.md#post_start)
- [`pre_stop`](/reference/compose-file/services.md#pre_stop)
- [`depends_on`](/reference/compose-file/services.md#depends_on)
- [使用生命周期钩子](/manuals/compose/how-tos/lifecycle.md)
- [控制启动顺序](/manuals/compose/how-tos/startup-order.md)
