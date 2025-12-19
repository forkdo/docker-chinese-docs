---
title: 启动守护进程
weight: 10
description: 手动启动 Docker 守护进程
keywords: docker, daemon, configuration, troubleshooting
aliases:
  - /config/daemon/start/
---

本页介绍如何手动或使用操作系统实用程序启动守护进程。

## 使用操作系统实用程序启动守护进程

在典型安装中，Docker 守护进程由系统实用程序启动，而不是由用户手动启动。这样可以更轻松地在机器重启时自动启动 Docker。

启动 Docker 的命令取决于您的操作系统。请查看 [安装 Docker](/manuals/engine/install/_index.md) 下的相应页面。

### 使用 systemd 启动

在某些操作系统（如 Ubuntu 和 Debian）上，Docker 守护进程服务会自动启动。使用以下命令手动启动它：

```console
$ sudo systemctl start docker
```

如果您希望 Docker 在启动时自动运行，请参阅 [配置 Docker 在启动时运行](/manuals/engine/install/linux-postinstall.md#configure-docker-to-start-on-boot-with-systemd)。

## 手动启动守护进程

如果您不想使用系统实用程序来管理 Docker 守护进程，或者只是想进行测试，可以使用 `dockerd` 命令手动运行它。根据您的操作系统配置，您可能需要使用 `sudo`。

以这种方式启动 Docker 时，它会在前台运行，并将其日志直接发送到您的终端。

```console
$ dockerd

INFO[0000] +job init_networkdriver()
INFO[0000] +job serveapi(unix:///var/run/docker.sock)
INFO[0000] Listening for HTTP on unix (/var/run/docker.sock)
```

要停止手动启动的 Docker，请在终端中按 `Ctrl+C`。