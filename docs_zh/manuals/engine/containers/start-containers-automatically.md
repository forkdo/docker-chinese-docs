---
description: 如何自动启动容器
keywords: 容器, 重启, 策略, 自动化, 管理
title: 自动启动容器
weight: 10
aliases:
  - /engine/articles/host_integration/
  - /engine/admin/host_integration/
  - /engine/admin/start-containers-automatically/
  - /config/containers/start-containers-automatically/
---

Docker 提供了 [重启策略](/reference/cli/docker/container/run.md#restart)
来控制容器在退出时或 Docker 重启时是否自动启动。重启策略会按正确顺序启动链接的容器。Docker 建议您使用重启策略，避免使用进程管理器来启动容器。

重启策略与 `dockerd` 命令的 `--live-restore` 标志不同。使用 `--live-restore` 可以在 Docker 升级期间保持容器运行，尽管网络和用户输入会被中断。

## 使用重启策略

要为容器配置重启策略，在使用 `docker run` 命令时使用 [`--restart`](/reference/cli/docker/container/run.md#restart) 标志。`--restart` 标志的值可以是以下任意一种：

| 标志                       | 描述                                                                                                                                                                                                                                                                                                                                                           |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no`                       | 不自动重启容器。（默认）                                                                                                                                                                                                                                                                                                                  |
| `on-failure[:max-retries]` | 如果容器因错误退出（表现为非零退出码），则重启容器。可选地，使用 `:max-retries` 选项限制 Docker 守护进程尝试重启容器的次数。`on-failure` 策略仅在容器以失败退出时提示重启。如果守护进程重启，它不会重启容器。                                                                                                                                                                                                 |
| `always`                   | 如果容器停止，则始终重启容器。如果它被手动停止，只有当 Docker 守护进程重启或容器本身被手动重启时才会重启。（参见 [重启策略详情](#restart-policy-details) 中列出的第二个要点）                                                                                                                                                                                                                                                |
| `unless-stopped`           | 类似于 `always`，除非容器被停止（手动或其他方式），否则即使 Docker 守护进程重启也不会重启容器。                                                                                                                                                                                                                         |

以下命令启动一个 Redis 容器并配置为始终重启，除非容器被显式停止或守护进程重启。

```console
$ docker run -d --restart unless-stopped redis
```

以下命令更改已运行容器 `redis` 的重启策略。

```console
$ docker update --restart unless-stopped redis
```

以下命令确保所有运行中的容器重启。

```console
$ docker update --restart unless-stopped $(docker ps -q)
```

### 重启策略详情

使用重启策略时请记住以下几点：

- 重启策略仅在容器成功启动后生效。在这种情况下，成功启动意味着容器至少运行了 10 秒，且 Docker 已开始监控它。这可以防止从未启动的容器进入重启循环。

- 如果您手动停止容器，重启策略将被忽略，直到 Docker 守护进程重启或容器被手动重启。这可以防止重启循环。

- 重启策略仅适用于容器。要为 Swarm 服务配置重启策略，请参阅
  [与服务重启相关的标志](/reference/cli/docker/service/create.md)。

### 重启前台容器

当您在前台运行容器时，停止容器会导致附加的 CLI 退出，无论容器的重启策略如何。以下示例说明了这种行为。

1. 创建一个 Dockerfile，打印数字 1 到 5 然后退出。

   ```dockerfile
   FROM busybox:latest
   COPY --chmod=755 <<"EOF" /start.sh
   echo "Starting..."
   for i in $(seq 1 5); do
     echo "$i"
     sleep 1
   done
   echo "Exiting..."
   exit 1
   EOF
   ENTRYPOINT /start.sh
   ```

2. 从 Dockerfile 构建镜像。

   ```console
   $ docker build -t startstop .
   ```

3. 从镜像运行容器，指定 `always` 作为其重启策略。

   容器将数字 1..5 打印到标准输出，然后退出。这导致附加的 CLI 也退出。

   ```console
   $ docker run --restart always startstop
   Starting...
   1
   2
   3
   4
   5
   Exiting...
   $
   ```

4. 运行 `docker ps` 显示容器仍在运行或重启，这要归功于重启策略。但是 CLI 会话已经退出。它没有在容器首次退出后继续运行。

   ```console
   $ docker ps
   CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS     NAMES
   081991b35afe   startstop   "/bin/sh -c /start.sh"   9 seconds ago   Up 4 seconds             gallant_easley
   ```

5. 您可以使用 `docker container attach` 命令在重启之间重新附加终端到容器。下次容器退出时，它再次被分离。

   ```console
   $ docker container attach 081991b35afe
   4
   5
   Exiting...
   $
   ```

## 使用进程管理器

如果重启策略不满足您的需求，例如当 Docker 外部的进程依赖于 Docker 容器时，您可以改用进程管理器，如
[systemd](https://systemd.io/) 或
[supervisor](http://supervisord.org/)。

> [!WARNING]
>
> 不要将 Docker 重启策略与主机级进程管理器结合使用，因为这会产生冲突。

要使用进程管理器，配置它使用与您手动启动容器时相同的 `docker start` 或 `docker service` 命令来启动您的容器或服务。有关详细信息，请查阅特定进程管理器的文档。

### 在容器内使用进程管理器

进程管理器也可以在容器内运行，检查进程是否正在运行，如果没有，则启动/重启它。

> [!WARNING]
>
> 这些管理器并不了解 Docker，仅监控容器内的操作系统进程。Docker 不推荐这种方法，因为它是平台相关的，可能在给定 Linux 发行版的不同版本之间有所不同。