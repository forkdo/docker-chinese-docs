---
description: 了解如何在 Docker Engine 中使用本地日志记录驱动程序
keywords: local, docker, logging, driver, file
title: 本地文件日志记录驱动程序
aliases:
  - /engine/reference/logging/local/
  - /engine/admin/logging/local/
  - /config/containers/logging/local/
---

`local` 日志记录驱动程序捕获容器的 stdout/stderr 输出，并将其写入针对性能和磁盘使用进行优化的内部存储中。

默认情况下，`local` 驱动程序为每个容器保留 100MB 的日志消息，并使用自动压缩来减小磁盘上的占用空间。100MB 的默认值是基于每个文件 20MB 的默认大小以及此类文件的默认数量 5（以考虑日志轮转）。

> [!WARNING]
>
> `local` 日志记录驱动程序使用基于文件的存储。这些文件设计为仅由 Docker 守护进程访问。使用外部工具与这些文件进行交互可能会干扰 Docker 的日志记录系统并导致意外行为，应避免这样做。

## 用法

要将 `local` 驱动程序用作默认日志记录驱动程序，请在 `daemon.json` 文件中将 `log-driver` 和 `log-opt` 键设置为适当的值。该文件在 Linux 主机上位于 `/etc/docker/`，在 Windows Server 上位于 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动程序设置为 `local` 并设置 `max-size` 选项。

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m"
  }
}
```

重新启动 Docker 以使更改对新创建的容器生效。现有容器不会自动使用新的日志记录配置。

您可以使用 `--log-driver` 标志为特定容器设置日志记录驱动程序，用于 `docker container create` 或 `docker run`：

```console
$ docker run \
      --log-driver local --log-opt max-size=10m \
      alpine echo hello world
```

请注意，`local` 是 bash 保留关键字，因此在脚本中可能需要将其引用起来。

### 选项

`local` 日志记录驱动程序支持以下日志记录选项：

| Option     | Description                                                                                                                                                   | Example value              |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------- |
| `max-size` | 日志在轮转前的最大大小。一个正整数加上表示度量单位的修饰符（`k`、`m` 或 `g`）。默认为 20m。      | `--log-opt max-size=10m`   |
| `max-file` | 可以存在的日志文件的最大数量。如果轮转日志产生过多文件，则会删除最旧的文件。一个正整数。默认为 5。 | `--log-opt max-file=3`     |
| `compress` | 切换轮转日志文件的压缩。默认启用。                                                                                                  | `--log-opt compress=false` |

### 示例

此示例启动一个 `alpine` 容器，该容器最多可以有 3 个日志文件，每个文件不超过 10 兆字节。

```console
$ docker run -it --log-driver local --log-opt max-size=10m --log-opt max-file=3 alpine ash
```