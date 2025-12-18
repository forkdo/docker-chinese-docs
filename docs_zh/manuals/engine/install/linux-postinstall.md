---
description: 查找 Linux 用户推荐的 Docker Engine 安装后步骤，包括如何以非 root 用户身份运行 Docker 等。
keywords: 无需 sudo 运行 docker、docker 以 root 身份运行、docker 安装后配置、docker 安装后步骤、docker 以非 root 身份运行、非 root 用户运行 docker、如何在 linux 中运行 docker、如何在 linux 中运行 docker、如何在 linux 中启动 docker、在 linux 上运行 docker
title: Docker Engine 的 Linux 安装后步骤
linkTitle: 安装后步骤
weight: 90
aliases:
- /engine/installation/linux/docker-ee/linux-postinstall/
- /engine/installation/linux/linux-postinstall/
- /install/linux/linux-postinstall/
---

这些可选的安装后步骤描述了如何配置您的 Linux 主机以更好地与 Docker 配合使用。

## 将 Docker 作为非 root 用户管理

Docker 守护进程绑定到 Unix 套接字，而不是 TCP 端口。默认情况下，Unix 套接字归 `root` 用户所有，其他用户只能使用 `sudo` 访问它。Docker 守护进程始终以 `root` 用户身份运行。

如果您不想在 `docker` 命令前加 `sudo`，请创建一个名为 `docker` 的 Unix 组并添加用户。当 Docker 守护进程启动时，它会创建一个可由 `docker` 组成员访问的 Unix 套接字。在某些 Linux 发行版中，使用包管理器安装 Docker Engine 时，系统会自动创建此组。在这种情况下，您无需手动创建该组。

<!-- prettier-ignore -->
> [!WARNING]
>
> `docker` 组向用户授予 root 级权限。有关这如何影响您系统安全的详细信息，请参阅
> [Docker 守护进程攻击面](../security/_index.md#docker-daemon-attack-surface)。

> [!NOTE]
>
> 要以非 root 用户身份运行 Docker，请参阅
> [以非 root 用户身份运行 Docker 守护进程（Rootless 模式）](../security/rootless.md)。

要创建 `docker` 组并添加您的用户：

1. 创建 `docker` 组。

   ```console
   $ sudo groupadd docker
   ```

2. 将您的用户添加到 `docker` 组。

   ```console
   $ sudo usermod -aG docker $USER
   ```

3. 注销并重新登录，以便重新评估您的组成员身份。

   > 如果您在虚拟机中运行 Linux，可能需要重启虚拟机才能使更改生效。

   您也可以运行以下命令来激活组的更改：

   ```console
   $ newgrp docker
   ```

4. 验证您是否可以不使用 `sudo` 运行 `docker` 命令。

   ```console
   $ docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行它。当容器运行时，它会打印一条消息然后退出。

   如果您最初在将用户添加到 `docker` 组之前使用 `sudo` 运行 Docker CLI 命令，可能会看到以下错误：

   ```text
   WARNING: Error loading config file: /home/user/.docker/config.json -
   stat /home/user/.docker/config.json: permission denied
   ```

   此错误表示 `~/.docker/` 目录的权限设置不正确，这是由于之前使用 `sudo` 命令导致的。

   要解决此问题，可以删除 `~/.docker/` 目录（它会自动重新创建，但任何自定义设置都会丢失），或者使用以下命令更改其所有者和权限：

   ```console
   $ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
   $ sudo chmod g+rwx "$HOME/.docker" -R
   ```

## 配置 Docker 在启动时使用 systemd 自动启动

许多现代 Linux 发行版使用 [systemd](https://systemd.io/) 来管理哪些服务在系统启动时启动。在 Debian 和 Ubuntu 上，Docker 服务默认在启动时启动。要在其他使用 systemd 的 Linux 发行版上自动启动 Docker 和 containerd，请运行以下命令：

```console
$ sudo systemctl enable docker.service
$ sudo systemctl enable containerd.service
```

要停止此行为，请改用 `disable`。

```console
$ sudo systemctl disable docker.service
$ sudo systemctl disable containerd.service
```

您可以使用 systemd 单元文件在启动时配置 Docker 服务，例如添加 HTTP 代理、为 Docker 运行时文件设置不同的目录或分区，或其他自定义设置。例如，请参阅 [配置守护进程使用代理](/manuals/engine/daemon/proxy.md#systemd-unit-file)。

## 配置默认日志驱动

Docker 提供 [日志驱动](/manuals/engine/logging/_index.md) 来从主机上运行的所有容器收集和查看日志数据。默认日志驱动 `json-file` 将日志数据写入主机文件系统上的 JSON 格式文件。随着时间的推移，这些日志文件会扩大，可能导致磁盘资源耗尽。

为避免日志数据过度使用磁盘的问题，请考虑以下选项之一：

- 配置 `json-file` 日志驱动以启用
  [日志轮转](/manuals/engine/logging/drivers/json-file.md)。
- 使用 [替代日志驱动](/manuals/engine/logging/configure.md#configure-the-default-logging-driver)，例如默认执行日志轮转的 ["local" 日志驱动](/manuals/engine/logging/drivers/local.md)。
- 使用将日志发送到远程日志聚合器的日志驱动。

## 下一步

- 查看 [Docker 工作坊](/get-started/workshop/_index.md) 以学习如何构建镜像并将其作为容器化应用程序运行。