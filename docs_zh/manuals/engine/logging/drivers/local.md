---
description: 了解如何在 Docker Engine 中使用本地日志驱动
keywords: local, docker, logging, driver, file
title: 本地文件日志驱动
aliases:
  - /engine/reference/logging/local/
  - /engine/admin/logging/local/
  - /config/containers/logging/local/
---

`local` 日志驱动会捕获容器的 stdout/stderr 输出，并将它们写入经过优化的内部存储，以提高性能和磁盘使用效率。

默认情况下，`local` 驱动为每个容器保留 100MB 的日志消息，并使用自动压缩来减少磁盘占用。这个 100MB 的默认值基于每个文件 20MB 的默认大小和默认 5 个文件数量（考虑日志轮转）。

> [!WARNING]
>
> `local` 日志驱动使用基于文件的存储。这些文件设计为仅由 Docker 守护进程访问。使用外部工具与这些文件交互可能会干扰 Docker 的日志系统，导致意外行为，应避免这样做。

## 使用方法

要将 `local` 驱动设置为默认日志驱动，请在 `daemon.json` 文件中设置 `log-driver` 和 `log-opt` 键为适当的值。该文件位于 Linux 主机上的 `/etc/docker/` 或 Windows Server 上的 `C:\ProgramData\docker\config\daemon.json`。有关使用 `daemon.json` 配置 Docker 的更多信息，请参阅 [daemon.json](/reference/cli/dockerd.md#daemon-configuration-file)。

以下示例将日志驱动设置为 `local` 并设置 `max-size` 选项。

```json
{
  "log-driver": "local",
  "log-opts": {
    "max-size": "10m"
  }
}
```

重启 Docker 以使更改对新创建的容器生效。现有容器不会自动使用新的日志配置。

您可以通过在 `docker container create` 或 `docker run` 中使用 `--log-driver` 标志为特定容器设置日志驱动：

```console
$ docker run \
      --log-driver local --log-opt max-size=10m \
      alpine echo hello world
```

注意 `local` 是 bash 保留关键字，因此在脚本中可能需要用引号括起来。

### 选项

`local` 日志驱动支持以下日志选项：

| 选项       | 描述                                                                                                                                                   | 示例值                     |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------- |
| `max-size` | 日志轮转前的最大大小。正整数加上表示单位的修饰符（`k`、`m` 或 `g`）。默认为 20m。                                                                       | `--log-opt max-size=10m`   |
| `max-file` | 可存在的最大日志文件数。如果轮转日志创建了过多文件，最旧的文件将被删除。正整数。默认为 5。                                                              | `--log-opt max-file=3`     |
| `compress` | 切换轮转日志文件的压缩。默认启用。                                                                                                                  | `--log-opt compress=false` |

### 示例

此示例启动一个 `alpine` 容器，该容器最多可以有 3 个日志文件，每个不超过 10 兆字节。

```console
$ docker run -it --log-driver local --log-opt max-size=10m --log-opt max-file=3 alpine ash
```