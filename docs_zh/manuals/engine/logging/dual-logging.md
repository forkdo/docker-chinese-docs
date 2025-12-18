---
description: >
  了解如何在使用第三方日志解决方案时，本地读取容器日志。
keywords: >
  docker, logging, driver, dual logging, dual logging, cache, ring-buffer,
  configuration
title: 在远程日志驱动中使用 docker logs
aliases:
  - /config/containers/logging/dual-logging/
---

## 概述

无论配置了何种日志驱动或插件，你都可以使用 `docker logs` 命令来读取容器日志。
Docker Engine 使用 [`local`](drivers/local.md) 日志驱动作为缓存，用于读取容器的最新日志。
这被称为双重日志（dual logging）。默认情况下，缓存启用了日志文件轮转，
每个容器最多限制为 5 个文件，每个文件 20 MB（压缩前）。

请参考 [配置选项](#configuration-options) 部分来自定义这些默认值，
或参考 [禁用双重日志](#disable-the-dual-logging-cache) 部分来禁用此功能。

## 前置条件

如果配置的日志驱动不支持读取日志，Docker Engine 会自动启用双重日志。

以下示例展示了在有和没有双重日志功能时运行 `docker logs` 命令的结果：

### 无双重日志功能

当容器配置了远程日志驱动（如 `splunk`），且双重日志被禁用时，
尝试本地读取容器日志会显示错误：

- 步骤 1：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      "cache-disabled": "true",
      ... (options for "splunk" logging driver)
    }
  }
  ```

- 步骤 2：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 步骤 3：读取容器日志

  ```console
  $ docker logs 7d6ac83a89a0
  Error response from daemon: configured logging driver does not support reading
  ```

### 有双重日志功能

启用双重日志缓存后，即使日志驱动不支持读取日志，也可以使用 `docker logs` 命令读取日志。
以下示例展示了一个使用 `splunk` 远程日志驱动作为默认值，并启用双重日志缓存的守护进程配置：

- 步骤 1：配置 Docker 守护进程

  ```console
  $ cat /etc/docker/daemon.json
  {
    "log-driver": "splunk",
    "log-opts": {
      ... (options for "splunk" logging driver)
    }
  }
  ```

- 步骤 2：启动容器

  ```console
  $ docker run -d busybox --name testlog top
  ```

- 步骤 3：读取容器日志

  ```console
  $ docker logs 7d6ac83a89a0
  2019-02-04T19:48:15.423Z [INFO]  core: marked as sealed
  2019-02-04T19:48:15.423Z [INFO]  core: pre-seal teardown starting
  2019-02-04T19:48:15.423Z [INFO]  core: stopping cluster listeners
  2019-02-04T19:48:15.423Z [INFO]  core: shutting down forwarding rpc listeners
  2019-02-04T19:48:15.423Z [INFO]  core: forwarding rpc listeners stopped
  2019-02-04T19:48:15.599Z [INFO]  core: rpc listeners successfully shut down
  2019-02-04T19:48:15.599Z [INFO]  core: cluster listeners successfully shut down
  ```

> [!NOTE]
>
> 对于支持读取日志的日志驱动（如 `local`、`json-file` 和 `journald` 驱动），
> 在双重日志功能可用之前或之后使用 `docker logs` 读取日志没有功能差异。
> 对于这些驱动，日志在两种情况下都可以通过 `docker logs` 读取。

### 配置选项

双重日志缓存接受与 [`local` 日志驱动](drivers/local.md) 相同的配置选项，
但需要添加 `cache-` 前缀。这些选项可以为每个容器单独指定，
也可以使用 [守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file) 为新容器设置默认值。

默认情况下，缓存启用了日志文件轮转，每个容器最多限制为 5 个文件，每个文件 20MB（压缩前）。
使用下面描述的配置选项来自定义这些默认值。

| 选项             | 默认值    | 描述                                                                                                                                                     |
| :--------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cache-disabled` | `"false"` | 禁用本地缓存。布尔值作为字符串传递（`true`、`1`、`0` 或 `false`）。                                                                                       |
| `cache-max-size` | `"20m"`   | 缓存在轮转前的最大大小。正整数加一个表示单位的修饰符（`k`、`m` 或 `g`）。                                                                                 |
| `cache-max-file` | `"5"`     | 缓存文件的最大数量。如果轮转日志时创建了过多文件，最旧的文件将被删除。正整数。                                                                            |
| `cache-compress` | `"true"`  | 启用或禁用轮转日志文件的压缩。布尔值作为字符串传递（`true`、`1`、`0` 或 `false`）。                                                                       |

## 禁用双重日志缓存

使用 `cache-disabled` 选项禁用双重日志缓存。在仅通过远程日志系统读取日志，
且无需通过 `docker logs` 进行调试的场景中，禁用缓存可以节省存储空间。

可以为单个容器禁用缓存，也可以使用 [守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file) 为新容器默认禁用。

以下示例使用守护进程配置文件，将 [`splunk`](drivers/splunk.md) 日志驱动作为默认值，并禁用缓存：

```console
$ cat /etc/docker/daemon.json
{
  "log-driver": "splunk",
  "log-opts": {
    "cache-disabled": "true",
    ... (options for "splunk" logging driver)
  }
}
```

> [!NOTE]
>
> 对于支持读取日志的日志驱动（如 `local`、`json-file` 和 `journald` 驱动），
> 不使用双重日志，禁用该选项不会产生任何效果。

## 局限性

- 如果使用远程日志驱动或插件的容器遇到网络问题，不会向本地缓存写入日志。
- 如果写入 `logdriver` 失败（文件系统已满、写入权限被移除等），缓存写入也会失败，
  并在守护进程日志中记录。日志条目不会重试写入缓存。
- 在默认配置中，由于使用了环形缓冲区（ring buffer）以防止在慢速文件写入时阻塞容器的 stdio，
  某些日志可能会从缓存中丢失。管理员必须在守护进程关闭时修复这些问题。