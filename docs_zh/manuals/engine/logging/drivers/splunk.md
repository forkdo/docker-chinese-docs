---
description: 了解如何在 Docker Engine 中使用 Splunk 日志驱动
keywords: splunk, docker, logging, driver
title: Splunk 日志驱动
aliases:
  - /engine/reference/logging/splunk/
  - /engine/admin/logging/splunk/
  - /config/containers/logging/splunk/
---

`splunk` 日志驱动将容器日志发送到 Splunk Enterprise 和 Splunk Cloud 中的
[HTTP Event Collector](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/)。

## 用法

你可以将 Docker 日志配置为默认使用 `splunk` 驱动，或在每个容器上单独配置。

要将 `splunk` 驱动设为默认日志驱动，需在 `daemon.json` 配置文件中设置 `log-driver` 和 `log-opts` 为适当的值，然后重启 Docker。例如：

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

`daemon.json` 文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅
[daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须以字符串形式提供。布尔值和数值（如 `splunk-gzip` 或 `splunk-gzip-level` 的值）因此必须用引号（`"`）括起来。

要为特定容器使用 `splunk` 驱动，请在 `docker run` 命令中使用 `--log-driver` 和 `log-opt` 命令行标志：

```console
$ docker run --log-driver=splunk --log-opt splunk-token=VALUE --log-opt splunk-url=VALUE ...
```

## Splunk 选项

以下属性允许你配置 Splunk 日志驱动。

- 要在 Docker 环境中配置 `splunk` 驱动，请在 `daemon.json` 中使用键 `"log-opts": {"NAME": "VALUE", ...}`。
- 要为单个容器配置 `splunk` 驱动，请在 `docker run` 中使用标志 `--log-opt NAME=VALUE ...`。

| 选项                      | 是否必需 | 描述                                                                                                                                                                                                                                                                                                                                |
| :-------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `splunk-token`              | 必需 | Splunk HTTP Event Collector 令牌。                                                                                                                                                                                                                                                                                                         |
| `splunk-url`                | 必需 | 指向你的 Splunk Enterprise、自助式 Splunk Cloud 实例或 Splunk Cloud 托管集群的路径（包括 HTTP Event Collector 使用的端口和协议），格式如下之一：`https://your_splunk_instance:8088`、`https://input-prd-p-XXXXXXX.cloud.splunk.com:8088` 或 `https://http-inputs-XXXXXXXX.splunkcloud.com`。 |
| `splunk-source`             | 可选 | 事件源。                                                                                                                                                                                                                                                                                                                              |
| `splunk-sourcetype`         | 可选 | 事件源类型。                                                                                                                                                                                                                                                                                                                         |
| `splunk-index`              | 可选 | 事件索引。                                                                                                                                                                                                                                                                                                                               |
| `splunk-capath`             | 可选 | 根证书路径。                                                                                                                                                                                                                                                                                                                  |
| `splunk-caname`             | 可选 | 用于验证服务器证书的名称；默认使用 `splunk-url` 的主机名。                                                                                                                                                                                                                                        |
| `splunk-insecureskipverify` | 可选 | 忽略服务器证书验证。                                                                                                                                                                                                                                                                                                      |
| `splunk-format`             | 可选 | 消息格式。可以是 `inline`、`json` 或 `raw`。默认为 `inline`。                                                                                                                                                                                                                                                                    |
| `splunk-verify-connection`  | 可选 | 启动时验证 Docker 是否可以连接到 Splunk 服务器。默认为 true。                                                                                                                                                                                                                                                               |
| `splunk-gzip`               | 可选 | 启用/禁用 gzip 压缩以向 Splunk Enterprise 或 Splunk Cloud 实例发送事件。默认为 false。                                                                                                                                                                                                                           |
| `splunk-gzip-level`         | 可选 | 设置 gzip 压缩级别。有效值为 -1（默认）、0（无压缩）、1（最佳速度）... 9（最佳压缩）。默认为 [DefaultCompression](https://golang.org/pkg/compress/gzip/#DefaultCompression)。                                                                                                                    |
| `tag`                       | 可选 | 指定消息标签，可解释某些标记。默认值为 `{{.ID}}`（容器 ID 的 12 个字符）。请参考 [日志标签选项文档](log_tags.md) 以自定义日志标签格式。                                                                                                                                                                                         |
| `labels`                    | 可选 | 以逗号分隔的标签键列表，如果为容器指定了这些标签，则应将其包含在消息中。                                                                                                                                                                                                                  |
| `labels-regex`              | 可选 | 与 `labels` 类似且兼容。用于匹配日志相关标签的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                                           |
| `env`                       | 可选 | 以逗号分隔的环境变量键列表，如果为容器指定了这些变量，则应将其包含在消息中。                                                                                                                                                                                                |
| `env-regex`                 | 可选 | 与 `env` 类似且兼容。用于匹配日志相关环境变量的正则表达式。用于高级 [日志标签选项](log_tags.md)。                                                                                                                                                                               |

如果 `label` 和 `env` 键之间发生冲突，`env` 的值优先。这两个选项都会为日志消息的属性添加额外字段。

以下是为 Splunk Enterprise 实例指定的日志选项示例。该实例安装在与 Docker 守护进程相同的机器上本地运行。

使用 HTTPS 方案指定根证书和通用名称的路径。这用于验证。`SplunkServerDefaultCert` 由 Splunk 证书自动生成。

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

Splunk Cloud 上托管的 Splunk 实例的 `splunk-url` 格式类似于 `https://http-inputs-XXXXXXXX.splunkcloud.com`，不包含端口说明符。

### 消息格式

有三种日志驱动消息格式：`inline`（默认）、`json` 和 `raw`。

{{< tabs >}}
{{< tab name="Inline" >}}

默认格式是 `inline`，其中每条日志消息作为字符串嵌入。例如：

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

要将消息格式化为 `json` 对象，请设置 `--log-opt splunk-format=json`。驱动会尝试将每一行解析为 JSON 对象并作为嵌入对象发送。如果无法解析消息，则以 `inline` 格式发送。例如：

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

Splunk 日志驱动允许你通过为 Docker 守护进程设置环境变量来配置一些高级选项。

| 环境变量名称                        | 默认值 | 描述                                                                                                                              |
| :----------------------------------------------- | :------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_FREQUENCY`  | `5s`          | 等待更多消息进行批处理的时间。                                                                                             |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_BATCH_SIZE` | `1000`        | 在一次批处理中发送的消息数量。                                                          |
| `SPLUNK_LOGGING_DRIVER_BUFFER_MAX`               | `10 * 1000`   | 缓冲区中可重试的最大消息数。                                                                               |
| `SPLUNK_LOGGING_DRIVER_CHANNEL_SIZE`             | `4 * 1000`    | 用于发送消息到后台日志记录器工作进程（负责批处理消息）的通道中可挂起消息的最大数量。 |