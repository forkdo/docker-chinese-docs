# 将 docker logs 与远程日志记录驱动程序结合使用

## 概述

无论配置的日志记录驱动程序或插件如何，您都可以使用 `docker logs` 命令来读取容器日志。Docker 引擎使用 [`local`](drivers/local.md) 日志记录驱动程序作为读取容器最新日志的缓存。这称为**双重日志记录 (dual logging)**。默认情况下，缓存启用日志文件轮转，并且每个容器限制为最多 5 个文件，每个文件最大 20 MB（压缩前）。

请参阅[配置选项](#configuration-options)部分以自定义这些默认值，或参阅[禁用双重日志记录](#disable-the-dual-logging-cache)部分以禁用此功能。

## 先决条件

如果配置的日志记录驱动程序不支持读取日志，Docker 引擎会自动启用双重日志记录。

以下示例展示了在有和没有双重日志记录功能的情况下运行 `docker logs` 命令的结果：

### 没有双重日志记录功能

当容器配置为使用远程日志记录驱动程序（如 `splunk`）且双重日志记录被禁用时，尝试在本地读取容器日志会显示错误：

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

### 具有双重日志记录功能

启用双重日志记录缓存后，即使日志记录驱动程序不支持读取日志，也可以使用 `docker logs` 命令读取日志。以下示例显示了使用 `splunk` 远程日志记录驱动程序作为默认值并启用双重日志记录缓存的守护进程配置：

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
> 对于支持读取日志的日志记录驱动程序，例如 `local`、`json-file` 和 `journald` 驱动程序，在双重日志记录功能可用之前或之后，功能上没有差异。对于这些驱动程序，在两种情况下都可以使用 `docker logs` 读取日志。

### 配置选项

双重日志记录缓存接受与 [`local` 日志记录驱动程序](drivers/local.md)相同的配置选项，但带有 `cache-` 前缀。这些选项可以按容器指定，也可以使用[守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file)为新容器设置默认值。

默认情况下，缓存启用日志文件轮转，并且每个容器限制为最多 5 个文件，每个文件最大 20 MB（压缩前）。使用下面描述的配置选项来自定义这些默认值。

| 选项               | 默认值      | 描述                                                                                                                               |
| :----------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| `cache-disabled`   | `"false"`   | 禁用本地缓存。作为字符串传递的布尔值 (`true`, `1`, `0`, 或 `false`)。                                                              |
| `cache-max-size`   | `"20m"`     | 缓存在轮转之前的最大大小。一个正整数加上表示度量单位的修饰符 (`k`, `m`, 或 `g`)。                                                 |
| `cache-max-file`   | `"5"`       | 可以存在的缓存文件的最大数量。如果轮转日志产生过多文件，将删除最旧的文件。一个正整数。                                             |
| `cache-compress`   | `"true"`    | 启用或禁用轮转日志文件的压缩。作为字符串传递的布尔值 (`true`, `1`, `0`, 或 `false`)。                                              |

## 禁用双重日志记录缓存

使用 `cache-disabled` 选项可以禁用双重日志记录缓存。在日志仅通过远程日志系统读取且不需要通过 `docker logs` 读取日志进行调试的情况下，禁用缓存有助于节省存储空间。

可以为单个容器禁用缓存，或者在使用[守护进程配置文件](/reference/cli/dockerd/#daemon-configuration-file)时为新容器默认禁用缓存。

以下示例使用守护进程配置文件将 [`splunk`](drivers/splunk.md) 日志记录驱动程序作为默认值，并禁用缓存：

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
> 对于支持读取日志的日志记录驱动程序，例如 `local`、`json-file` 和 `journald` 驱动程序，不使用双重日志记录，禁用该选项没有效果。

## 限制

- 如果使用将日志发送到远程的日志记录驱动程序或插件的容器遇到网络问题，则不会发生对本地缓存的 `write` 操作。
- 如果由于任何原因（文件系统已满、写入权限被移除）导致对 `logdriver` 的写入失败，缓存写入也会失败，并记录在守护进程日志中。不会重试对缓存的日志条目写入。
- 在默认配置下，可能会丢失一些缓存中的日志，因为使用了环形缓冲区来防止在文件写入缓慢时阻塞容器的 stdio。管理员必须在守护进程关闭时修复这些问题。
