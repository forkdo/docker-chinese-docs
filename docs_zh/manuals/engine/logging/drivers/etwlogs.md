---
description: 学习如何在 Docker Engine 中使用 ETW（Event Tracing for Windows）日志驱动程序
keywords: ETW, docker, logging, driver
title: ETW 日志驱动程序
aliases:
- /engine/admin/logging/etwlogs/
- /config/containers/logging/etwlogs/
---

Event Tracing for Windows (ETW) 日志驱动程序将容器日志作为 ETW 事件转发。
ETW 是 Windows 中的事件跟踪（Event Tracing），是 Windows 中用于跟踪应用程序的通用框架。
每个 ETW 事件都包含一个消息，其中包含日志及其上下文信息。
客户端可以创建 ETW 监听器来监听这些事件。

此日志驱动程序在 Windows 中注册的 ETW 提供程序具有以下 GUID 标识符：
`{a3693192-9ed6-46d2-a981-f8226c8363bd}`。
客户端创建一个 ETW 监听器，并注册以监听来自日志驱动程序提供程序的事件。
提供程序和监听器的创建顺序无关紧要。
客户端可以在提供程序向系统注册之前，就创建其 ETW 监听器并开始监听来自提供程序的事件。

## 使用方法

以下是如何使用 Windows 大多数安装中包含的 `logman` 实用程序监听这些事件的示例：

1. `logman start -ets DockerContainerLogs -p "{a3693192-9ed6-46d2-a981-f8226c8363bd}" 0x0 -o trace.etl`
2. 使用 `etwlogs` 驱动程序运行容器，通过在 Docker run 命令中添加 `--log-driver=etwlogs`，并生成日志消息。
3. `logman stop -ets DockerContainerLogs`
4. 这将生成一个包含事件的 etl 文件。将此文件转换为人类可读形式的一种方法是运行：`tracerpt -y trace.etl`。

每个 ETW 事件都包含一个格式如下的结构化消息字符串：

```text
container_name: %s, image_name: %s, container_id: %s, image_id: %s, source: [stdout | stderr], log: %s
```

消息中每个项目的详细信息如下：

| Field            | Description                                    |
| ---------------- | ---------------------------------------------- |
| `container_name` | 容器启动时的名称。                             |
| `image_name`     | 容器镜像的名称。                               |
| `container_id`   | 完整的 64 字符容器 ID。                        |
| `image_id`       | 容器镜像的完整 ID。                            |
| `source`         | `stdout` 或 `stderr`。                         |
| `log`            | 容器日志消息。                                 |

以下是一个事件消息示例（输出格式已为可读性调整）：

```yaml
container_name: backstabbing_spence,
image_name: windowsservercore,
container_id: f14bb55aa862d7596b03a33251c1be7dbbec8056bbdead1da8ec5ecebbe29731,
image_id: sha256:2f9e19bd998d3565b4f345ac9aaf6e3fc555406239a4fb1b1ba879673713824b,
source: stdout,
log: Hello world!
```

客户端可以解析此消息字符串以获取日志消息及其上下文信息。
时间戳也可在 ETW 事件中获得。

> [!NOTE]
>
> 此 ETW 提供程序仅发出消息字符串，而不是特殊结构化的 ETW 事件。
> 因此，您无需向系统注册清单文件即可读取和解释其 ETW 事件。