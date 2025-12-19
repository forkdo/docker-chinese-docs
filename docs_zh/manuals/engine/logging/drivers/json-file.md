---
description: 了解如何在 Docker Engine 中使用 json-file 日志驱动
keywords: json-file, docker, logging, driver
title: JSON File 日志驱动
aliases:
  - /engine/reference/logging/json-file/
  - /engine/admin/logging/json-file/
  - /config/containers/logging/json-file/
---

默认情况下，Docker 会捕获所有容器的标准输出（和标准错误），并使用 JSON 格式将它们写入文件。JSON 格式使用其来源（`stdout` 或 `stderr`）和时间戳注释每一行。每个日志文件仅包含关于一个容器的信息。

```json
{
  "log": "Log line is here\n",
  "stream": "stdout",
  "time": "2019-01-01T11:11:11.111111111Z"
}
```

> [!WARNING]
>
> `json-file` 日志驱动使用基于文件的存储。这些文件设计为仅供 Docker 守护进程独占访问。使用外部工具与这些文件交互可能会干扰 Docker 的日志系统并导致意外行为，应予以避免。

## 用法

要将 `json-file` 驱动用作默认日志驱动，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opts` 键设置为适当的值。该文件在 Linux 主机上位于 `/etc/docker/`，在 Windows Server 上位于 `C:\ProgramData\docker\config\`。如果该文件不存在，请先创建它。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动设置为 `json-file`，并设置 `max-size` 和 `max-file` 选项以启用自动日志轮转。

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

> [!NOTE]
>
> `daemon.json` 配置文件中的 `log-opts` 配置选项必须作为字符串提供。因此，布尔值和数值（例如上面示例中 `max-file` 的值）必须用引号（`"`）括起来。

重新启动 Docker，以使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

您可以使用 `--log-driver` 标志结合 `docker container create` 或 `docker run` 来为特定容器设置日志驱动：

```console
$ docker run \
      --log-driver json-file --log-opt max-size=10m \
      alpine echo hello world
```

### 选项

`json-file` 日志驱动支持以下日志选项：

| 选项             | 描述                                                                                                                                                  | 示例值                                             |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `max-size`     | 日志在轮转前的最大大小。一个正整数加上表示计量单位的修饰符（`k`、`m` 或 `g`）。默认为 -1（无限制）。                                                      | `--log-opt max-size=10m`                           |
| `max-file`     | 可以存在的日志文件的最大数量。如果轮转日志产生过多文件，则会删除最旧的文件。**仅在同时设置了 `max-size` 时有效。**一个正整数。默认为 1。                      | `--log-opt max-file=3`                             |
| `labels`       | 在启动 Docker 守护进程时应用。此守护进程接受的以逗号分隔的日志相关标签列表。用于高级[日志标签选项](log_tags.md)。                                           | `--log-opt labels=production_status,geo`           |
| `labels-regex` | 与 `labels` 类似且兼容。用于匹配日志相关标签的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                            | `--log-opt labels-regex=^(production_status\|geo)` |
| `env`          | 在启动 Docker 守护进程时应用。此守护进程接受的以逗号分隔的日志相关环境变量列表。用于高级[日志标签选项](log_tags.md)。                                        | `--log-opt env=os,customer`                        |
| `env-regex`    | 与 `env` 类似且兼容。用于匹配日志相关环境变量的正则表达式。用于高级[日志标签选项](log_tags.md)。                                                           | `--log-opt env-regex=^(os\|customer)`              |
| `compress`     | 切换轮转日志的压缩。默认为 `disabled`。                                                                                                                  | `--log-opt compress=true`                          |

### 示例

此示例启动一个 `alpine` 容器，该容器最多可以有 3 个日志文件，每个文件最大为 10 兆字节。

```console
$ docker run -it --log-opt max-size=10m --log-opt max-file=3 alpine ash
```