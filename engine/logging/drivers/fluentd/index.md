# Fluentd 日志驱动

`fluentd` 日志驱动将容器日志作为结构化日志数据发送到 [Fluentd](https://www.fluentd.org) 收集器。然后，用户可以使用 Fluentd 的各种[输出插件](https://www.fluentd.org/plugins)将这些日志写入各种目的地。

除了日志消息本身，`fluentd` 日志驱动还会在结构化日志消息中发送以下元数据：

| 字段               | 描述                                                                                                                              |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `container_id`     | 完整的 64 字符容器 ID。                                                                                                           |
| `container_name`   | 容器启动时的名称。如果您使用 `docker rename` 重命名容器，新名称不会反映在日志条目中。                                               |
| `source`           | `stdout` 或 `stderr`                                                                                                              |
| `log`              | 容器日志                                                                                                                          |

## 用法

可以通过多次指定 `--log-opt` 来支持一些选项：

- `fluentd-address`：指定用于连接 Fluentd 守护进程的套接字地址，例如 `fluentdhost:24224` 或 `unix:///path/to/fluentd.sock`。
- `tag`：为 Fluentd 消息指定标签。支持一些 Go 模板标记，例如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}` `docker.{{.ID}}`。

要将 `fluentd` 驱动用作默认日志驱动，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值。该文件在 Linux 主机上位于 `/etc/docker/`，在 Windows Server 上位于 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动设置为 `fluentd` 并设置 `fluentd-address` 选项。

```json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "fluentdhost:24224"
  }
}
```

重启 Docker 以使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须作为字符串提供。因此，布尔值和数值（例如 `fluentd-async` 或 `fluentd-max-retries` 的值）必须用引号 (`"`) 括起来。

要为特定容器设置日志驱动，请将 `--log-driver` 选项传递给 `docker run`：

```console
$ docker run --log-driver=fluentd ...
```

在使用此日志驱动之前，请启动 Fluentd 守护进程。日志驱动默认通过 `localhost:24224` 连接到此守护进程。使用 `fluentd-address` 选项可连接到其他地址。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
```

如果容器无法连接到 Fluentd 守护进程，除非使用了 `fluentd-async` 选项，否则容器会立即停止。

## 选项

用户可以使用 `--log-opt NAME=VALUE` 标志来指定其他 Fluentd 日志驱动选项。

### fluentd-address

默认情况下，日志驱动连接到 `localhost:24224`。提供 `fluentd-address` 选项可连接到其他地址。支持 `tcp`（默认）和 `unix` 套接字。

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=tcp://fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=unix:///path/to/fluentd.sock
```

上面的两个命令指定了相同的地址，因为 `tcp` 是默认值。

### tag

默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。请参阅[日志标签选项文档](log_tags.md)以自定义日志标签格式。

### labels, labels-regex, env, 和 env-regex

`labels` 和 `env` 选项各自接受一个逗号分隔的键列表。如果 `label` 和 `env` 键之间存在冲突，则 `env` 的值优先。这两个选项都会向日志消息的额外属性添加其他字段。

`env-regex` 和 `labels-regex` 选项分别与 `env` 和 `labels` 类似且兼容。它们的值是用于匹配与日志相关的环境变量和标签的正则表达式。它用于高级[日志标签选项](log_tags.md)。

### fluentd-async

Docker 在后台连接到 Fluentd。消息会被缓冲，直到连接建立。默认为 `false`。

### fluentd-async-reconnect-interval

启用 `fluentd-async` 时，`fluentd-async-reconnect-interval` 选项定义重新建立到 `fluentd-address` 的连接的间隔（以毫秒为单位）。如果地址解析为一个或多个 IP 地址（例如 Consul 服务地址），此选项非常有用。

### fluentd-buffer-limit

设置内存中缓冲的事件数量。记录将存储在内存中，直到达到此数量。如果缓冲区已满，记录日志的调用将失败。默认为 1048576。
(https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit)

### fluentd-retry-wait

重试之间的等待时间。默认为 1 秒。

### fluentd-max-retries

最大重试次数。默认为 `4294967295` (2\*\*32 - 1)。

### fluentd-sub-second-precision

以纳秒分辨率生成事件日志。默认为 `false`。

### fluentd-write-timeout

设置对 `fluentd` 守护进程的写入调用的超时时间。默认情况下，写入没有超时，并且会无限期地阻塞。

## 使用 Docker 管理 Fluentd 守护进程

关于 `Fluentd` 本身，请参阅[项目网页](https://www.fluentd.org)及其[文档](https://docs.fluentd.org)。

要使用此日志驱动，请在主机上启动 `fluentd` 守护进程。我们建议您使用 [Fluentd Docker 镜像](https://hub.docker.com/r/fluent/fluentd/)。如果您想在每个主机上聚合多个容器日志，然后将日志传输到另一个 Fluentd 节点以创建聚合存储，此镜像特别有用。

### 测试容器日志记录器

1.  编写一个配置文件 (`test.conf`) 来转储输入日志：

    ```text
    <source>
      @type forward
    </source>

    <match *>
      @type stdout
    </match>
    ```

2.  使用此配置文件启动 Fluentd 容器：

    ```console
    $ docker run -it -p 24224:24224 -v /path/to/conf/test.conf:/fluentd/etc/test.conf -e FLUENTD_CONF=test.conf fluent/fluentd:latest
    ```

3.  使用 `fluentd` 日志驱动启动一个或多个容器：

    ```console
    $ docker run --log-driver=fluentd your/application
    ```
