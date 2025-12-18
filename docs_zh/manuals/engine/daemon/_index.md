---
description: 配置 Docker 守护进程
keywords: docker, daemon, configuration
title: Docker 守护进程配置概述
linkTitle: 守护进程
weight: 60
aliases:
  - /articles/chef/
  - /articles/configuring/
  - /articles/dsc/
  - /articles/puppet/
  - /config/thirdparty/
  - /config/thirdparty/ansible/
  - /config/thirdparty/chef/
  - /config/thirdparty/dsc/
  - /config/thirdparty/puppet/
  - /engine/admin/
  - /engine/admin/ansible/
  - /engine/admin/chef/
  - /engine/admin/configuring/
  - /engine/admin/dsc/
  - /engine/admin/puppet/
  - /engine/articles/chef/
  - /engine/articles/configuring/
  - /engine/articles/dsc/
  - /engine/articles/puppet/
  - /engine/userguide/
  - /config/daemon/
---

本页面介绍如何自定义 Docker 守护进程 `dockerd`。

> [!NOTE]
>
> 本页面适用于手动安装 Docker Engine 的用户。如果您使用的是 Docker Desktop，请参考
> [设置页面](/manuals/desktop/settings-and-maintenance/settings.md#docker-engine)。

## 配置 Docker 守护进程

有两种方式可以配置 Docker 守护进程：

- 使用 JSON 配置文件。这是首选选项，因为它将所有配置集中在一个位置。
- 在启动 `dockerd` 时使用命令行标志。

只要不同时在标志和 JSON 文件中指定相同的选项，您就可以同时使用这两种方式。如果发生这种情况，Docker 守护进程将无法启动，并打印错误消息。

### 配置文件

下表显示了 Docker 守护进程默认情况下查找配置文件的位置，具体取决于您的系统和运行守护进程的方式。

| 操作系统和配置 | 文件位置                              |
| -------------------- | ------------------------------------------ |
| Linux，常规设置 | `/etc/docker/daemon.json`                  |
| Linux，无根模式 | `~/.config/docker/daemon.json`             |
| Windows              | `C:\ProgramData\docker\config\daemon.json` |

对于无根模式，守护进程遵循 `XDG_CONFIG_HOME` 变量。如果设置了该变量，预期的文件位置是 `$XDG_CONFIG_HOME/docker/daemon.json`。

您也可以在启动时使用 `dockerd --config-file` 标志显式指定配置文件的位置。

在 [dockerd 参考文档](/reference/cli/dockerd.md#daemon-configuration-file) 中了解可用的配置选项。

### 使用标志配置

您也可以手动启动 Docker 守护进程并使用标志进行配置。这在排查问题时可能很有用。

以下是如何手动启动 Docker 守护进程的示例，使用与前面 JSON 配置相同的配置：

```console
$ dockerd --debug \
  --tls=true \
  --tlscert=/var/docker/server.pem \
  --tlskey=/var/docker/serverkey.pem \
  --host tcp://192.168.59.3:2376
```

在 [dockerd 参考文档](/reference/cli/dockerd.md) 中了解可用的配置选项，或运行：

```console
$ dockerd --help
```

## 守护进程数据目录

Docker 守护进程将所有数据持久化到单个目录中。这跟踪了与 Docker 相关的所有内容，包括容器、镜像、卷、服务定义和密钥。

默认情况下，守护进程将数据存储在：

- Linux 上：`/var/lib/docker`
- Windows 上：`C:\ProgramData\docker`

当使用 [containerd 镜像存储](/manuals/engine/storage/containerd.md)（Docker Engine 29.0 及以后版本在全新安装上的默认设置）时，镜像内容和容器快照存储在 `/var/lib/containerd` 中。其他守护进程数据（卷、配置）仍保留在 `/var/lib/docker` 中。

当使用 `overlay2` 等 [经典存储驱动](/manuals/engine/storage/drivers/_index.md)（升级安装的默认设置）时，所有数据都存储在 `/var/lib/docker` 中。

### 配置数据目录位置

您可以使用 `data-root` 配置选项配置 Docker 守护进程使用不同的存储目录。

```json
{
  "data-root": "/mnt/docker-data"
}
```

`data-root` 选项不影响使用 containerd 镜像存储时存储在 `/var/lib/containerd` 中的镜像和容器数据。要更改 containerd 快照存储位置，请使用系统 containerd 配置文件：

```toml {title="/etc/containerd/config.toml"}
version = 2
root = "/mnt/containerd-data"
```

确保为每个守护进程使用专用目录。如果两个守护进程共享同一目录（例如 NFS 共享），您将遇到难以排查的错误。

## 下一步

Docker 文档中讨论了许多特定的配置选项。您可以继续了解以下内容：

- [自动启动容器](/manuals/engine/containers/start-containers-automatically.md)
- [限制容器的资源](/manuals/engine/containers/resource_constraints.md)
- [配置存储驱动](/manuals/engine/storage/drivers/select-storage-driver.md)
- [容器安全](/manuals/engine/security/_index.md)
- [配置 Docker 守护进程使用代理](./proxy.md)