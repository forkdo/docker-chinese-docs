---
description: 了解如何在 Docker Engine 中使用 Amazon CloudWatch Logs 日志驱动
keywords: AWS, Amazon, CloudWatch, 日志, 驱动
title: Amazon CloudWatch Logs 日志驱动
aliases:
- /engine/reference/logging/awslogs/
- /engine/admin/logging/awslogs/
- /config/containers/logging/awslogs/
---

`awslogs` 日志驱动将容器日志发送到 [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring)。
日志条目可以通过 [AWS 管理控制台](https://console.aws.amazon.com/cloudwatch/home#logs:) 或 [AWS SDK 和命令行工具](https://docs.aws.amazon.com/cli/latest/reference/logs/index.html) 检索。

## 使用方法

要将 `awslogs` 驱动设为默认日志驱动，请在 `daemon.json` 文件中设置 `log-driver` 和 `log-opt` 键为适当的值。该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。
以下示例将日志驱动设为 `awslogs` 并设置 `awslogs-region` 选项。

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "us-east-1"
  }
}
```

重启 Docker 以使更改生效。

您也可以在运行容器时使用 `--log-driver` 选项为特定容器设置日志驱动：

```console
$ docker run --log-driver=awslogs ...
```

如果您使用 Docker Compose，请使用以下声明示例设置 `awslogs`：

```yaml
myservice:
  logging:
    driver: awslogs
    options:
      awslogs-region: us-east-1
```

## Amazon CloudWatch Logs 选项

您可以在 `daemon.json` 中添加日志选项以设置 Docker 范围的默认值，或者在启动容器时使用 `--log-opt NAME=VALUE` 标志指定 Amazon CloudWatch Logs 日志驱动选项。

### awslogs-region

`awslogs` 日志驱动将您的 Docker 日志发送到特定区域。使用 `awslogs-region` 日志选项或 `AWS_REGION` 环境变量设置区域。默认情况下，如果您的 Docker 守护进程在 EC2 实例上运行且未设置区域，驱动将使用实例的区域。

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 ...
```

### awslogs-endpoint

默认情况下，Docker 使用 `awslogs-region` 日志选项或检测到的区域来构建远程 CloudWatch Logs API 端点。
使用 `awslogs-endpoint` 日志选项可以使用提供的端点覆盖默认端点。

> [!NOTE]
>
> `awslogs-region` 日志选项或检测到的区域控制用于签名的区域。如果您使用 `awslogs-endpoint` 指定的端点使用不同的区域，可能会遇到签名错误。

### awslogs-group

您必须为 `awslogs` 日志驱动指定一个 [日志组](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)。
您可以使用 `awslogs-group` 日志选项指定日志组：

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=myLogGroup ...
```

### awslogs-stream

要配置使用哪个 [日志流](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)，
您可以指定 `awslogs-stream` 日志选项。如果未指定，容器 ID 将用作日志流。

> [!NOTE]
>
> 给定日志组内的日志流一次只能由一个容器使用。同时为多个容器使用相同的日志流可能会导致日志性能降低。

### awslogs-create-group

默认情况下，如果日志组不存在，日志驱动将返回错误。但是，您可以将 `awslogs-create-group` 设置为 `true` 以按需自动创建日志组。
`awslogs-create-group` 选项默认为 `false`。

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-create-group=true \
    ...
```

> [!NOTE]
>
> 在尝试使用 `awslogs-create-group` 之前，您的 AWS IAM 策略必须包含 `logs:CreateLogGroup` 权限。

### awslogs-create-stream

默认情况下，日志驱动会创建用于容器日志持久化的 AWS CloudWatch Logs 流。

将 `awslogs-create-stream` 设置为 `false` 以禁用日志流创建。禁用后，Docker 守护进程假设日志流已存在。一个适用的用例是日志流创建由另一个进程处理，避免冗余的 AWS CloudWatch Logs API 调用。

如果 `awslogs-create-stream` 设置为 `false` 且日志流不存在，日志持久化到 CloudWatch 会在容器运行时失败，导致守护进程日志中出现 `Failed to put log events` 错误消息。

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-stream=myLogStream \
    --log-opt awslogs-create-stream=false \
    ...
```

### awslogs-datetime-format

`awslogs-datetime-format` 选项使用 [Python `strftime` 格式](https://strftime.org) 定义多行起始模式。
日志消息由匹配该模式的行和任何不匹配该模式的后续行组成。因此，匹配的行是日志消息之间的分隔符。

使用此格式的一个用例是解析堆栈转储等输出，否则这些输出可能会记录在多个条目中。正确的模式允许将其捕获在单个条目中。

如果同时配置了 `awslogs-datetime-format` 和 `awslogs-multiline-pattern`，此选项始终优先。

> [!NOTE]
>
> 多行日志执行所有日志消息的正则表达式解析和匹配，这可能对日志性能产生负面影响。

考虑以下日志流，其中新日志消息以时间戳开头：

```console
[May 01, 2017 19:00:01] A message was logged
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words
[May 01, 2017 19:01:32] Another message was logged
```

该格式可以用 `strftime` 表达式 `[%b %d, %Y %H:%M:%S]` 表示，`awslogs-datetime-format` 值可以设置为该表达式：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-datetime-format='\[%b %d, %Y %H:%M:%S\]' \
    ...
```

这将日志解析为以下 CloudWatch 日志事件：

```console
# 第一个事件
[May 01, 2017 19:00:01] A message was logged

# 第二个事件
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words

# 第三个事件
[May 01, 2017 19:01:32] Another message was logged
```

支持以下 `strftime` 代码：

| 代码 | 含义                                                          | 示例  |
| :--- | :--------------------------------------------------------------- | :------- |
| `%a` | 星期几的缩写名称。                                        | Mon      |
| `%A` | 星期几的全名。                                               | Monday   |
| `%w` | 星期几作为十进制数，0 为星期日，6 为星期六。 | 0        |
| `%d` | 月份中的日期作为零填充的十进制数。                | 08       |
| `%b` | 月份的缩写名称。                                          | Feb      |
| `%B` | 月份的全名。                                                 | February |
| `%m` | 月份作为零填充的十进制数。                           | 02       |
| `%Y` | 带世纪的年份作为十进制数。                           | 2008     |
| `%y` | 不带世纪的年份作为零填充的十进制数。            | 08       |
| `%H` | 小时（24 小时制）作为零填充的十进制数。            | 19       |
| `%I` | 小时（12 小时制）作为零填充的十进制数。            | 07       |
| `%p` | AM 或 PM。                                                        | AM       |
| `%M` | 分钟作为零填充的十进制数。                          | 57       |
| `%S` | 秒作为零填充的十进制数。                          | 04       |
| `%L` | 毫秒作为零填充的十进制数。                    | .123     |
| `%f` | 微秒作为零填充的十进制数。                    | 000345   |
| `%z` | UTC 偏移量，格式为 +HHMM 或 -HHMM。                           | +1300    |
| `%Z` | 时区名称。                                                  | PST      |
| `%j` | 年份中的日期作为零填充的十进制数。                 | 363      |

### awslogs-multiline-pattern

`awslogs-multiline-pattern` 选项使用正则表达式定义多行起始模式。
日志消息由匹配该模式的行和任何不匹配该模式的后续行组成。因此，匹配的行是日志消息之间的分隔符。

如果也配置了 `awslogs-datetime-format`，此选项将被忽略。

> [!NOTE]
>
> 多行日志执行所有日志消息的正则表达式解析和匹配，这可能对日志性能产生负面影响。

考虑以下日志流，其中每条日志消息应以模式 `INFO` 开头：

```console
INFO A message was logged
INFO Another multi-line message was logged
     Some random message
INFO Another message was logged
```

您可以使用正则表达式 `^INFO`：

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-multiline-pattern='^INFO' \
    ...
```

这将日志解析为以下 CloudWatch 日志事件：

```console
# 第一个事件
INFO A message was logged

# 第二个事件
INFO Another multi-line message was logged
     Some random message

# 第三个事件
INFO Another message was logged
```

### tag

指定 `tag` 作为 `awslogs-stream` 选项的替代。`tag` 解释 Go 模板标记，如 `{{.ID}}`、`{{.FullID}}` 或 `{{.Name}}` `docker.{{.ID}}`。有关支持的模板替换的详细信息，请参阅 [tag 选项文档](log_tags.md)。

当同时指定 `awslogs-stream` 和 `tag` 时，`awslogs-stream` 提供的值会覆盖 `tag` 指定的模板。

如果未指定，容器 ID 将用作日志流。

> [!NOTE]
>
> CloudWatch 日志 API 不支持日志名称中的 `:`。这在使用 `{{ .ImageName }}` 作为标签时可能会导致一些问题，因为 Docker 镜像的格式为 `IMAGE:TAG`，例如 `alpine:latest`。
> 可以使用模板标记获取正确的格式。要获取镜像名称和容器 ID 的前 12 个字符，您可以使用：
>
> ```bash
> --log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}'
> ```
>
> 输出类似于：`alpine_latest-bf0072049c76`

### awslogs-force-flush-interval-seconds

`awslogs` 驱动定期将日志刷新到 CloudWatch。

`awslogs-force-flush-interval-seconds` 选项更改日志刷新间隔秒数。

默认为 5 秒。

### awslogs-max-buffered-events

`awslogs` 驱动缓冲日志。

`awslogs-max-buffered-events` 选项更改日志缓冲区大小。

默认为 4K。

## 凭据

您必须向 Docker 守护进程提供 AWS 凭据才能使用 `awslogs` 日志驱动。您可以通过 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 环境变量、默认 AWS 共享凭据文件（root 用户的 `~/.aws/credentials`）或如果您在 Amazon EC2 实例上运行 Docker 守护进程，则使用 Amazon EC2 实例配置文件提供这些凭据。

凭据必须附加允许 `logs:CreateLogStream` 和 `logs:PutLogEvents` 操作的策略，如以下示例所示。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```