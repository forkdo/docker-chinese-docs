---
description: 了解如何在 Docker Engine 中使用 Splunk 日志记录驱动程序
keywords: splunk, docker, logging, driver
title: Splunk 日志记录驱动程序
aliases:
- /engine/reference/logging/splunk/
- /engine/admin/logging/splunk/
- /config/containers/logging/splunk/
---

`splunk` 日志记录驱动程序将容器日志发送到 Splunk Enterprise 和 Splunk Cloud 中的
[HTTP 事件收集器](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/)。

## 用法

您可以将 Docker 日志记录配置为默认使用 `splunk` 驱动程序，或者针对每个容器单独配置。

要将 `splunk` 驱动程序用作默认日志记录驱动程序，请在 `daemon.json` 配置文件中将 `log-driver` 和 `log-opts` 键设置为适当的值，然后重新启动 Docker。例如：

```json
{
  "log-driver": "splunk",
  "log-opts": {
    "splunk-token": "",
    "splunk-url": "",
    ...
  }
}
```

`daemon.json` 文件在 Linux 主机上位于 `/etc/docker/`，在 Windows Server 上位于 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅
[daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须作为字符串提供。因此，布尔值和数值（例如 `splunk-gzip` 或 `splunk-gzip-level` 的值）必须用引号 (`"`) 括起来。

要将 `splunk` 驱动程序用于特定容器，请在 `docker run` 命令中使用命令行标志 `--log-driver` 和 `--log-opt`：

```console
$ docker run --log-driver=splunk --log-opt splunk-token=VALUE --log-opt splunk-url=VALUE ...
```

## Splunk 选项

以下属性让您配置 Splunk 日志记录驱动程序。

- 要在 Docker 环境中配置 `splunk` 驱动程序，请编辑 `daemon.json`，使用键 `"log-opts": {"NAME": "VALUE", ...}`。
- 要为单个容器配置 `splunk` 驱动程序，请在 `docker run` 中使用标志 `--log-opt NAME=VALUE ...`。

| 选项                        | 是否必需 | 描述                                                                                                                                                                                                                                                                                                                                 |
| :-------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `splunk-token`              | 是       | Splunk HTTP 事件收集器令牌。                                                                                                                                                                                                                                                                                                         |
| `splunk-url`                | 是       | 您的 Splunk Enterprise、自助式 Splunk Cloud 实例或 Splunk Cloud 托管集群的路径（包括 HTTP 事件收集器使用的端口和方案），格式如下：`https://your_splunk_instance:8088`、`https://input-prd-p-XXXXXXX.cloud.splunk.com:8088` 或 `https://http-inputs-XXXXXXXX.splunkcloud.com`。 |
| `splunk-source`             | 否       | 事件来源。                                                                                                                                                                                                                                                                                                                           |
| `splunk-sourcetype`         | 否       | 事件来源类型。                                                                                                                                                                                                                                                                                                                       |
| `splunk-index`              | 否       | 事件索引。                                                                                                                                                                                                                                                                                                                           |
| `splunk-capath`             | 否       | 根证书路径。                                                                                                                                                                                                                                                                                                                         |
| `splunk-caname`             | 否       | 用于验证服务器证书的名称；默认使用 `splunk-url` 的主机名。                                                                                                                                                                                                                                                                            |
| `splunk-insecureskipverify` | 否       | 忽略服务器证书验证。                                                                                                                                                                                                                                                                                                                 |
| `splunk-format`             | 否       | 消息格式。可以是 `inline`、`json` 或 `raw`。默认为 `inline`。                                                                                                                                                                                                                                                                         |
| `splunk-verify-connection`  | 否       | 在启动时验证 Docker 是否可以连接到 Splunk 服务器。默认为 true。                                                                                                                                                                                                                                                                       |
| `splunk-gzip`               | 否       | 启用/禁用 gzip 压缩以向 Splunk Enterprise 或 Splunk Cloud 实例发送事件。默认为 false。                                                                                                                                                                                                                                                |
| `splunk-gzip-level`         | 否       | 设置 gzip 的压缩级别。有效值为 -1（默认）、0（无压缩）、1（最佳速度）... 9（最佳压缩）。默认为 [DefaultCompression](https://golang.org/pkg/compress/gzip/#DefaultCompression)。                                                                                                                               |
| `tag`                       | 否       | 为消息指定标签，该标签会解释一些标记。默认值为 `{{.ID}}`（容器 ID 的 12 个字符）。请参阅 [log tag 选项文档](log_tags.md) 以自定义日志标签格式。                                                                                                                         |
| `labels`                    | 否       | 逗号分隔的标签键列表，如果为容器指定了这些标签，则应将其包含在消息中。                                                                                                                                                                                                                                                               |
| `labels-regex`              | 否       | 与 `labels` 类似且兼容。用于匹配日志相关标签的正则表达式。用于高级 [log tag 选项](log_tags.md)。                                                                                                                                                                                                                                    |
| `env`                       | 否       | 逗号分隔的环境变量键列表，如果为容器指定了这些变量，则应将其包含在消息中。                                                                                                                                                                                                                                                           |
| `env-regex`                 | 否       | 与 `env` 类似且兼容。用于匹配日志相关环境变量的正则表达式。用于高级 [log tag 选项](log_tags.md)。                                                                                                                                                                                                                                  |

如果 `label` 和 `env` 键之间存在冲突，则 `env` 的值优先。这两个选项都会向日志消息的属性添加额外的字段。

以下是为 Splunk Enterprise 实例指定的日志记录选项示例。该实例本地安装在运行 Docker 守护程序的同一台机器上。

使用 HTTPS 方案指定了根证书和通用名称 (Common Name) 的路径。这用于验证。`SplunkServerDefaultCert` 是由 Splunk 证书自动生成的。

```console
$ docker run \
    --log-driver=splunk \
    --log-opt splunk-token=176FCEBF-4CF5-4EDF-91BC-703796522D20 \
    --log-opt splunk-url=https://splunkhost:8088 \
    --log-opt splunk-capath=/path/to/cert/cacert.pem \
    --log-opt splunk-caname=SplunkServerDefaultCert \
    --log-opt tag="{{.Name}}/{{.FullID}}" \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

托管在 Splunk Cloud 上的 Splunk 实例的 `splunk-url` 格式为 `https://http-inputs-XXXXXXXX.splunkcloud.com`，不包含端口说明符。

### 消息格式

日志记录驱动程序有三种消息传递格式：`inline`（默认）、`json` 和 `raw`。

{{< tabs >}}
{{< tab name="Inline" >}}

默认格式是 `inline`，其中每条日志消息都作为字符串嵌入。例如：

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "{\"foo\": \"bar\"}"
}
```

{{< /tab >}}
{{< tab name="JSON" >}}

要将消息格式化为 `json` 对象，请设置 `--log-opt splunk-format=json`。驱动程序会尝试将每一行解析为 JSON 对象，并将其作为嵌入对象发送。如果无法解析消息，则以 `inline` 格式发送。例如：

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": {
    "foo": "bar"
  }
}
```

{{< /tab >}}
{{< tab name="Raw" >}}

要将消息格式化为 `raw`，请设置 `--log-opt splunk-format=raw`。属性（环境变量和标签）和标签会作为前缀添加到消息中。例如：

```console
MyImage/MyContainer env1=val1 label1=label1 my message
MyImage/MyContainer env1=val1 label1=label1 {"foo": "bar"}
```

{{< /tab >}}
{{< /tabs >}}

## 高级选项

Splunk 日志记录驱动程序允许您通过为 Docker 守护程序设置环境变量来配置一些高级选项。

| 环境变量名称                                     | 默认值      | 描述                                                                                                                               |
| :----------------------------------------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_FREQUENCY`  | `5s`        | 等待更多消息进行批处理的时间。                                                                                                     |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_BATCH_SIZE` | `1000`      | 在一批发送之前应累积的消息数量。                                                                                                   |
| `SPLUNK_LOGGING_DRIVER_BUFFER_MAX`               | `10 * 1000` | 用于重试的缓冲区中保留的最大消息数。                                                                                               |
| `SPLUNK_LOGGING_DRIVER_CHANNEL_SIZE`             | `4 * 1000`  | 可以在用于向后台日志记录器工作进程发送消息的通道中等待处理的最大消息数，这些消息会在工作进程中进行批处理。 |