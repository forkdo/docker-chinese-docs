---
description: 了解如何在 Docker Engine 中使用 Graylog Extended Format 日志驱动
keywords: graylog, gelf, 日志, 驱动
title: Graylog Extended Format 日志驱动
aliases:
  - /engine/reference/logging/gelf/
  - /engine/admin/logging/gelf/
  - /config/containers/logging/gelf/
---

`gelf` 日志驱动是一种便捷的格式，被多种工具支持，例如 [Graylog](https://www.graylog.org/)、[Logstash](https://www.elastic.co/products/logstash) 和 [Fluentd](https://www.fluentd.org)。许多工具使用这种格式。

在 GELF 中，每条日志消息都是一个字典，包含以下字段：

- 版本
- 主机（最初发送消息的主机）
- 时间戳
- 消息的简短和详细版本
- 任何自定义字段

## 使用方法

要将 `gelf` 驱动设置为默认日志驱动，请在 `daemon.json` 文件中设置 `log-driver` 和 `log-opt` 键为适当的值。该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动设置为 `gelf`，并设置 `gelf-address` 选项。

```json
{
  "log-driver": "gelf",
  "log-opts": {
    "gelf-address": "udp://1.2.3.4:12201"
  }
}
```

重启 Docker 以使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须提供为字符串。布尔值和数值（例如 `gelf-tcp-max-reconnect` 的值）因此必须用引号 (`"`) 括起来。

您可以通过在使用 `docker container create` 或 `docker run` 时设置 `--log-driver` 标志，为特定容器设置日志驱动：

```console
$ docker run \
      --log-driver gelf --log-opt gelf-address=udp://1.2.3.4:12201 \
      alpine echo hello world
```

### GELF 选项

`gelf` 日志驱动支持以下选项：

| 选项                     | 是否必需 | 描述                                                                                                                                                                                                                                                                         | 示例值                                      |
| :------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `gelf-address`             | 必需 | GELF 服务器的地址。`tcp` 和 `udp` 是唯一支持的 URI 标识符，您必须指定端口。                                                                                                                                                                 | `--log-opt gelf-address=udp://192.168.0.42:12201`  |
| `gelf-compression-type`    | 可选 | `UDP Only` GELF 驱动用于压缩每条日志消息的压缩类型。允许的值为 `gzip`、`zlib` 和 `none`。默认值为 `gzip`。请注意，启用压缩会导致过度的 CPU 使用，因此强烈建议将其设置为 `none`。            | `--log-opt gelf-compression-type=gzip`             |
| `gelf-compression-level`   | 可选 | `UDP Only` 当 `gzip` 或 `zlib` 为 `gelf-compression-type` 时的压缩级别。范围为 `-1` 到 `9`（最佳压缩）的整数。默认值为 1（最快速度）。较高级别在较低速度下提供更多的压缩。`-1` 或 `0` 禁用压缩。 | `--log-opt gelf-compression-level=2`               |
| `gelf-tcp-max-reconnect`   | 可选 | `TCP Only` 连接断开时的最大重连尝试次数。正整数。默认值为 3。                                                                                                                                                            | `--log-opt gelf-tcp-max-reconnect=3`               |
| `gelf-tcp-reconnect-delay` | 可选 | `TCP Only` 重连尝试之间的秒数。正整数。默认值为 1。                                                                                                                                                                     | `--log-opt gelf-tcp-reconnect-delay=1`             |
| `tag`                      | 可选 | 附加到 `gelf` 消息中 `APP-NAME` 的字符串。默认情况下，Docker 使用容器 ID 的前 12 个字符来标记日志消息。有关自定义日志标签格式的详细信息，请参阅 [日志标签选项文档](log_tags.md)。                             | `--log-opt tag=mailer`                             |
| `labels`                   | 可选 | 在启动 Docker 守护进程时应用。此守护进程接受的与日志相关的标签的逗号分隔列表。在 `extra` 字段中添加额外的键，前缀为下划线 (`_`)。用于高级 [日志标签选项](log_tags.md)。                                        | `--log-opt labels=production_status,geo`           |
| `labels-regex`             | 可选 | 与 `labels` 类似且兼容。用于匹配与日志相关的标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                    | `--log-opt labels-regex=^(production_status\|geo)` |
| `env`                      | 可选 | 在启动 Docker 守护进程时应用。此守护进程接受的与日志相关的环境变量的逗号分隔列表。在 `extra` 字段中添加额外的键，前缀为下划线 (`_`)。用于高级 [日志标签选项](log_tags.md)。                         | `--log-opt env=os,customer`                        |
| `env-regex`                | 可选 | 与 `env` 类似且兼容。用于匹配与日志相关的环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                        | `--log-opt env-regex=^(os\|customer)`              |

> [!NOTE]
>
> `gelf` 驱动不支持 TCP 连接的 TLS。发送到 TLS 保护的输入的消息可能会静默失败。

### 示例

此示例将容器配置为使用在 `192.168.0.42` 的 `12201` 端口上运行的 GELF 服务器。

```console
$ docker run -dit \
    --log-driver=gelf \
    --log-opt gelf-address=udp://192.168.0.42:12201 \
    alpine sh
```