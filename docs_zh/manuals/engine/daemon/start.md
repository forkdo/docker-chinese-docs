---
title: 启动守护进程
weight: 10
description: 手动启动 Docker 守护进程
keywords: docker, 守护进程, 配置, 故障排除
aliases:
  - /config/daemon/start/
---

本页面展示了如何启动 Docker 守护进程，包括手动启动或使用操作系统工具启动。

## 使用操作系统工具启动守护进程

在典型安装中，Docker 守护进程由系统工具启动，而不是由用户手动启动。这使得机器重启时可以自动启动 Docker。

启动 Docker 的命令取决于您的操作系统。请查看 [安装 Docker](/manuals/engine/install/_index.md) 下的正确页面。

### 使用 systemd 启动

在某些操作系统上（如 Ubuntu 和 Debian），Docker 守护进程服务会自动启动。如需手动启动，请使用以下命令：

```console
$ sudo systemctl start docker
```

如果您希望 Docker 在系统启动时自动运行，请参阅
[配置 Docker 在启动时自动运行](/manuals/engine/install/linux-postinstall.md#configure-docker-to-start-on-boot-with-systemd)。

## 手动启动守护进程

如果您不想使用系统工具管理 Docker 守护进程，或者只是想测试一下，可以使用 `dockerd` 命令手动运行它。根据您的操作系统配置，您可能需要使用 `sudo`。

以这种方式启动 Docker 时，它会在前台运行，并将日志直接发送到您的终端。

```console
$ dockerd

INFO[0000] +job init_networkdriver()
INFO[0000] +job serveapi(unix:///var/run/docker.sock)
INFO[0000] Listening for HTTP on unix (/var/run/docker.sock)
```

当您手动启动 Docker 后，要停止它，只需在终端中按 `Ctrl+C` 即可。