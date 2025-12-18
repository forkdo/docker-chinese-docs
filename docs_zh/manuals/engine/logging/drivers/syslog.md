---
description: 了解如何在 Docker Engine 中使用 syslog 日志驱动
keywords: syslog, docker, 日志, 驱动
title: Syslog 日志驱动
aliases:
  - /engine/reference/logging/syslog/
  - /engine/admin/logging/syslog/
  - /config/containers/logging/syslog/
---

`syslog` 日志驱动将日志路由到 `syslog` 服务器。`syslog` 协议使用原始字符串作为日志消息，支持有限的元数据。syslog 消息必须以特定方式格式化才能有效。从有效的消息中，接收器可以提取以下信息：

- 优先级（Priority）：日志级别，如 `debug`、`warning`、`error`、`info`。
- 时间戳（Timestamp）：事件发生的时间。
- 主机名（Hostname）：事件发生的主机。
- 设施（Facility）：记录消息的子系统，如 `mail` 或 `kernel`。
- 进程名和进程 ID（PID）：生成日志的进程的名称和 ID。

格式在 [RFC 5424](https://tools.ietf.org/html/rfc5424) 中定义，Docker 的 syslog 驱动按以下方式实现 [ABNF 参考](https://tools.ietf.org/html/rfc5424#section-6)：

```text
                TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID
                    +          +             +           |        +
                    |          |             |           |        |
                    |          |             |           |        |
       +------------+          +----+        |           +----+   +---------+
       v                            v        v                v             v
2017-04-01T17:41:05.616647+08:00 a.vm {taskid:aa,version:} 1787791 {taskid:aa,version:}
```

## 使用方法

要将 `syslog` 驱动设为默认日志驱动，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值。该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动设为 `syslog` 并设置 `syslog-address` 选项。`syslog-address` 选项支持 UDP 和 TCP；此示例使用 UDP。

```json
{
  "log-driver": "syslog",
  "log-opts": {
    "syslog-address": "udp://1.2.3.4:1111"
  }
}
```

重启 Docker 以使更改生效。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。数字和布尔值（如 `syslog-tls-skip-verify` 的值）因此必须用引号（`"`）括起来。

您可以通过对 `docker container create` 或 `docker run` 使用 `--log-driver` 标志为特定容器设置日志驱动：

```console
$ docker run \
      --log-driver syslog --log-opt syslog-address=udp://1.2.3.4:1111 \
      alpine echo hello world
```

## 选项

以下日志选项受 `syslog` 日志驱动支持。它们可以作为 `daemon.json` 中的默认值设置，方法是将它们作为键值对添加到 `log-opts` JSON 数组中。它们也可以通过在启动容器时为每个选项添加 `--log-opt <key>=<value>` 标志在给定容器上设置。

| 选项                   | 描述                                                                                                                                                                                                                                                                                                      | 示例值                                                                                            |
| :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| `syslog-address`       | 外部 `syslog` 服务器的地址。URI 说明符可以是 `[tcp\|udp\|tcp+tls]://host:port`、`unix://path` 或 `unixgram://path`。如果传输协议是 `tcp`、`udp` 或 `tcp+tls`，默认端口为 `514`。                                                                                                                           | `--log-opt syslog-address=tcp+tls://192.168.1.3:514`, `--log-opt syslog-address=unix:///tmp/syslog.sock` |
| `syslog-facility`      | 要使用的 `syslog` 设施。可以是任何有效 `syslog` 设施的数字或名称。参阅 [syslog 文档](https://tools.ietf.org/html/rfc5424#section-6.2.1)。                                                                                                                                                                    | `--log-opt syslog-facility=daemon`                                                                |
| `syslog-tls-ca-cert`   | CA 签名的信任证书的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                                                      | `--log-opt syslog-tls-ca-cert=/etc/ca-certificates/custom/ca.pem`                                 |
| `syslog-tls-cert`      | TLS 证书文件的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                                                           | `--log-opt syslog-tls-cert=/etc/ca-certificates/custom/cert.pem`                                  |
| `syslog-tls-key`       | TLS 密钥文件的绝对路径。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                                                                           | `--log-opt syslog-tls-key=/etc/ca-certificates/custom/key.pem`                                    |
| `syslog-tls-skip-verify` | 如果设置为 `true`，连接到 `syslog` 守护进程时跳过 TLS 验证。默认为 `false`。如果地址协议不是 `tcp+tls`，则忽略此选项。                                                                                                                                                                                        | `--log-opt syslog-tls-skip-verify=true`                                                           |
| `tag`                  | 附加到 `syslog` 消息中 `APP-NAME` 的字符串。默认情况下，Docker 使用容器 ID 的前 12 个字符标记日志消息。请参阅 [日志标签选项文档](log_tags.md)以自定义日志标签格式。                                                                                                                                          | `--log-opt tag=mailer`                                                                            |
| `syslog-format`        | 要使用的 `syslog` 消息格式。如果不指定，Docker 使用本地 Unix syslog 格式，不指定主机名。指定 `rfc3164` 以使用 RFC-3164 兼容格式，`rfc5424` 以使用 RFC-5424 兼容格式，或 `rfc5424micro` 以使用 RFC-5424 兼容格式并具有微秒时间戳分辨率。                                                                          | `--log-opt syslog-format=rfc5424micro`                                                            |
| `labels`               | 启动 Docker 守护进程时应用。以逗号分隔的列表，列出此守护进程接受的日志相关标签。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                                         | `--log-opt labels=production_status,geo`                                                          |
| `labels-regex`         | 启动 Docker 守护进程时应用。与 `labels` 类似且兼容。用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                                   | `--log-opt labels-regex=^(production_status\|geo)`                                                |
| `env`                  | 启动 Docker 守护进程时应用。以逗号分隔的列表，列出此守护进程接受的日志相关环境变量。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                                      | `--log-opt env=os,customer`                                                                       |
| `env-regex`            | 启动 Docker 守护进程时应用。与 `env` 类似且兼容。用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                                   | `--log-opt env-regex=^(os\|customer)`                                                             |
