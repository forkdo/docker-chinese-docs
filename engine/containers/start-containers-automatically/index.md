# 自动启动容器

Docker 提供了[重启策略](/reference/cli/docker/container/run.md#restart)，用于控制容器在退出时或 Docker 重启时是否自动启动。重启策略会按照正确的顺序启动相关联的容器。Docker 建议您使用重启策略，避免使用进程管理器来启动容器。

重启策略与 `dockerd` 命令的 `--live-restore` 标志不同。使用 `--live-restore` 可以在 Docker 升级期间保持容器运行，但网络和用户输入会中断。

## 使用重启策略

要为容器配置重启策略，请在执行 `docker run` 命令时使用 [`--restart`](/reference/cli/docker/container/run.md#restart) 标志。`--restart` 标志的值可以是以下任意一种：

| 标志                       | 描述                                                                                                                                                                                                                                                                                                                                                           |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no`                       | 不自动重启容器。（默认）                                                                                                                                                                                                                                                                                                                  |
| `on-failure[:max-retries]` | 如果容器因错误退出（表现为非零退出码），则重启容器。可选地，使用 `:max-retries` 选项限制 Docker 守护进程尝试重启容器的次数。`on-failure` 策略仅在容器因失败退出时触发重启。如果守护进程重启，容器不会被重启。 |
| `always`                   | 如果容器停止，则总是重启容器。如果容器被手动停止，则仅在 Docker 守护进程重启或容器本身被手动重启时才会重启。（参见[重启策略详情](#restart-policy-details)中的第二点）                                                                                                                |
| `unless-stopped`           | 与 `always` 类似，但当容器被停止（手动或其他方式）时，即使 Docker 守护进程重启，容器也不会被重启。                                                                                                                                                                                                                         |

以下命令启动一个 Redis 容器，并配置为始终重启，除非容器被显式停止或守护进程重启。

```console
$ docker run -d --restart unless-stopped redis
```

以下命令更改名为 `redis` 的正在运行的容器的重启策略。

```console
$ docker update --restart unless-stopped redis
```

以下命令确保所有正在运行的容器重启。

```console
$ docker update --restart unless-stopped $(docker ps -q)
```

### 重启策略详情

使用重启策略时，请注意以下几点：

- 重启策略仅在容器成功启动后生效。成功启动意味着容器至少运行了 10 秒，并且 Docker 已经开始监控它。这可以防止无法启动的容器进入重启循环。

- 如果您手动停止容器，则在 Docker 守护进程重启或容器被手动重启之前，重启策略将被忽略。这可以防止重启循环。

- 重启策略仅适用于容器。要为 Swarm 服务配置重启策略，请参见[与服务重启相关的标志](/reference/cli/docker/service/create.md)。

### 重启前台容器

当您在**前台**运行容器时，停止容器会导致附加的 CLI 也退出，无论容器的重启策略是什么。以下示例说明了这种行为。

1. 创建一个 Dockerfile，打印数字 1 到 5，然后退出。

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

3. 从镜像运行容器，指定其重启策略为 `always`。

   容器将打印数字 1..5 到 stdout，然后退出。这会导致附加的 CLI 也退出。

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

4. 运行 `docker ps` 显示容器仍在运行或重启，这得益于重启策略。但 CLI 会话已经退出，它不会在容器首次退出后继续存在。

   ```console
   $ docker ps
   CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS     NAMES
   081991b35afe   startstop   "/bin/sh -c /start.sh"   9 seconds ago   Up 4 seconds             gallant_easley
   ```

5. 您可以在重启之间使用 `docker container attach` 命令将终端重新附加到容器。下次容器退出时，终端会再次分离。

   ```console
   $ docker container attach 081991b35afe
   4
   5
   Exiting...
   $
   ```

## 使用进程管理器

如果重启策略无法满足您的需求（例如，当 Docker 外部的进程依赖于 Docker 容器时），您可以使用进程管理器，如 [systemd](https://systemd.io/) 或 [supervisor](http://supervisord.org/)。

> [!WARNING]
>
> 不要将 Docker 重启策略与主机级进程管理器结合使用，因为这会导致冲突。

要使用进程管理器，请配置它使用您通常用于手动启动容器的相同 `docker start` 或 `docker service` 命令来启动您的容器或服务。有关更多详细信息，请参阅特定进程管理器的文档。

### 在容器内使用进程管理器

进程管理器也可以在容器内运行，以检查某个进程是否正在运行，并在未运行时启动/重启它。

> [!WARNING]
>
> 这些进程管理器不感知 Docker，仅监控容器内的操作系统进程。Docker 不推荐这种方法，因为它依赖于平台，并且可能因 Linux 发行版的版本而异。
