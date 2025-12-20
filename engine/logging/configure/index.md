# 配置日志驱动程序

Docker 提供了多种日志记录机制，帮助您获取正在运行的容器和服务的信息。这些机制被称为日志驱动程序。每个 Docker 守护进程都有一个默认的日志驱动程序，除非您将其配置为使用不同的日志驱动程序（简称日志驱动），否则每个容器都会使用该默认驱动程序。

默认情况下，Docker 使用 [`json-file` 日志驱动程序](drivers/json-file.md)，该驱动程序在内部将容器日志缓存为 JSON 格式。除了使用 Docker 自带的日志驱动程序外，您还可以实现和使用[日志驱动程序插件](plugins.md)。

> [!TIP]
>
> 使用 `local` 日志驱动程序可防止磁盘耗尽。默认情况下，不会执行日志轮转。因此，由默认的 [`json-file` 日志驱动程序](drivers/json-file.md) 存储的日志文件可能会占用大量磁盘空间，特别是对于生成大量输出的容器，这可能导致磁盘空间耗尽。
>
> Docker 保留 json-file 日志驱动程序（不带日志轮转）作为默认设置，以保持与旧版本 Docker 的向后兼容性，并适用于将 Docker 用作 Kubernetes 运行时的场景。
>
> 对于其他情况，建议使用 `local` 日志驱动程序，因为它默认执行日志轮转，并使用更高效的文件格式。请参阅下面的[配置默认日志驱动程序](#configure-the-default-logging-driver)部分，了解如何将 `local` 日志驱动程序配置为默认设置，以及 [local 文件日志驱动程序](drivers/local.md) 页面以获取有关 `local` 日志驱动程序的更多详细信息。

## 配置默认日志驱动程序

要配置 Docker 守护进程默认使用特定的日志驱动程序，请在 `daemon.json` 配置文件中将 `log-driver` 的值设置为日志驱动程序的名称。有关详细信息，请参阅 [`dockerd` 参考手册](/reference/cli/dockerd/#daemon-configuration-file) 中的“守护进程配置文件”部分。

默认日志驱动程序是 `json-file`。以下示例将默认日志驱动程序设置为 [`local` 日志驱动程序](drivers/local.md)：

```json
{
  "log-driver": "local"
}
```

如果日志驱动程序具有可配置选项，您可以在 `daemon.json` 文件中将其设置为一个 JSON 对象，键为 `log-opts`。以下示例在 `json-file` 日志驱动程序上设置了四个可配置选项：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3",
    "labels": "production_status",
    "env": "os,customer"
  }
}
```

重启 Docker 以使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。布尔值和数值（例如上面示例中的 `max-file` 值）必须用引号 (`"`) 括起来。

如果您未指定日志驱动程序，则默认为 `json-file`。要查找 Docker 守护进程的当前默认日志驱动程序，请运行 `docker info` 并搜索 `Logging Driver`。您可以在 Linux、macOS 或 Windows 上的 PowerShell 中使用以下命令：

```console
$ docker info --format '{{.LoggingDriver}}'

json-file
```

> [!NOTE]
>
> 在守护进程配置中更改默认日志驱动程序或日志驱动程序选项仅影响在配置更改后创建的容器。现有容器保留创建时使用的日志驱动程序选项。要更新容器的日志驱动程序，必须使用所需选项重新创建容器。
> 请参阅下面的[为容器配置日志驱动程序](#configure-the-logging-driver-for-a-container)部分，了解如何查找容器的日志驱动程序配置。

## 为容器配置日志驱动程序

启动容器时，您可以使用 `--log-driver` 标志将其配置为使用与 Docker 守护进程默认值不同的日志驱动程序。如果日志驱动程序具有可配置选项，您可以使用一个或多个 `--log-opt <NAME>=<VALUE>` 标志实例来设置它们。即使容器使用默认日志驱动程序，也可以使用不同的可配置选项。

以下示例启动一个使用 `none` 日志驱动程序的 Alpine 容器。

```console
$ docker run -it --log-driver none alpine ash
```

要查找正在运行容器的当前日志驱动程序（如果守护进程正在使用 `json-file` 日志驱动程序），请运行以下 `docker inspect` 命令，将容器名称或 ID 替换为 `<CONTAINER>`：

```console
$ docker inspect -f '{{.HostConfig.LogConfig.Type}}' <CONTAINER>

json-file
```

## 配置从容器到日志驱动程序的日志消息传递模式

Docker 提供了两种将消息从容器传递到日志驱动程序的模式：

- （默认）从容器到驱动程序的直接、阻塞式传递
- 非阻塞式传递，将日志消息存储在驱动程序消费的每个容器的中间缓冲区中

`non-blocking` 消息传递模式可防止应用程序因日志背压而阻塞。当 STDERR 或 STDOUT 流阻塞时，应用程序可能会以意外方式失败。

> [!WARNING]
>
> 当缓冲区满时，新消息将不会被排队。通常，丢弃消息比阻塞应用程序的日志写入过程更可取。

`mode` 日志选项控制是使用 `blocking`（默认）还是 `non-blocking` 消息传递。

`max-buffer-size` 控制在 `mode` 设置为 `non-blocking` 时用于中间消息存储的缓冲区大小。默认值为 `1m`，即 1 MB（100 万字节）。有关允许的格式字符串，请参阅 [go-units 包中的 `FromHumanSize()` 函数](https://pkg.go.dev/github.com/docker/go-units#FromHumanSize)，一些示例包括 `1KiB`（1024 字节）、`2g`（20 亿字节）。

以下示例启动一个 Alpine 容器，使用非阻塞模式记录输出，并设置 4 兆字节的缓冲区：

```console
$ docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m alpine ping 127.0.0.1
```

### 在日志驱动程序中使用环境变量或标签

某些日志驱动程序会将容器的 `--env|-e` 或 `--label` 标志的值添加到容器的日志中。此示例启动一个容器，使用 Docker 守护进程的默认日志驱动程序（在以下示例中为 `json-file`），但设置了环境变量 `os=ubuntu`。

```console
$ docker run -dit --label production_status=testing -e os=ubuntu alpine sh
```

如果日志驱动程序支持，这会在日志输出中添加额外的字段。以下输出由 `json-file` 日志驱动程序生成：

```json
"attrs":{"production_status":"testing","os":"ubuntu"}
```

## 支持的日志驱动程序

支持以下日志驱动程序。请参阅每个驱动程序的文档链接，了解其可配置选项（如果适用）。如果您正在使用[日志驱动程序插件](plugins.md)，可能会看到更多选项。

| 驱动程序                                | 描述                                                                                                 |
| :------------------------------------ | :---------------------------------------------------------------------------------------------------------- |
| `none`                                | 容器没有可用的日志，`docker logs` 不会返回任何输出。                       |
| [`local`](drivers/local.md)           | 日志以专为最小开销设计的自定义格式存储。                                           |
| [`json-file`](drivers/json-file.md)   | 日志格式化为 JSON。Docker 的默认日志驱动程序。                                      |
| [`syslog`](drivers/syslog.md)         | 将日志消息写入 `syslog` 设施。主机上必须运行 `syslog` 守护进程。  |
| [`journald`](drivers/journald.md)     | 将日志消息写入 `journald`。主机上必须运行 `journald` 守护进程。               |
| [`gelf`](drivers/gelf.md)             | 将日志消息写入 Graylog 扩展日志格式 (GELF) 端点，例如 Graylog 或 Logstash。           |
| [`fluentd`](drivers/fluentd.md)       | 将日志消息写入 `fluentd`（转发输入）。主机上必须运行 `fluentd` 守护进程。 |
| [`awslogs`](drivers/awslogs.md)       | 将日志消息写入 Amazon CloudWatch Logs。                                                              |
| [`splunk`](drivers/splunk.md)         | 使用 HTTP 事件收集器将日志消息写入 `splunk`。                                             |
| [`etwlogs`](drivers/etwlogs.md)       | 将日志消息作为 Windows 事件跟踪 (ETW) 事件写入。仅在 Windows 平台上可用。         |
| [`gcplogs`](drivers/gcplogs.md)       | 将日志消息写入 Google Cloud Platform (GCP) Logging。                                                 |

## 日志驱动程序的局限性

- 读取日志信息需要解压缩轮转的日志文件，这会导致磁盘使用量暂时增加（直到读取轮转文件中的日志条目），并在解压缩期间增加 CPU 使用率。
- 托管 Docker 数据目录的主机存储容量决定了日志文件信息的最大大小。
