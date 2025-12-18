---
description: Docker Desktop for Windows 常见问题解答
keywords: desktop, windows, faqs
title: Docker Desktop for Windows 常见问题解答
linkTitle: Windows
tags: [FAQ]
weight: 30
---

### 我可以在 Docker Desktop 旁边使用 VirtualBox 吗？

可以，如果你的机器上启用了 [Windows Hypervisor Platform](https://docs.microsoft.com/en-us/virtualization/api/) 功能，就可以同时运行 VirtualBox 和 Docker Desktop。

### 为什么需要 Windows 10 或 Windows 11？

Docker Desktop 使用 Windows 的 Hyper-V 功能。虽然较旧的 Windows 版本也支持 Hyper-V，但它们的 Hyper-V 实现缺少 Docker Desktop 正常工作所需的关键功能。

### 我可以在 Windows Server 上运行 Docker Desktop 吗？

不可以，Docker Desktop 不支持在 Windows Server 上运行。

### Windows 上的符号链接如何工作？

Docker Desktop 支持两种类型的符号链接：Windows 原生符号链接和在容器内创建的符号链接。

Windows 原生符号链接在容器中显示为符号链接，而在容器内创建的符号链接则表示为 [mfsymlinks](https://wiki.samba.org/index.php/UNIX_Extensions#Minshall.2BFrench_symlinks)。这些是带有特殊元数据的常规 Windows 文件。因此，在容器内创建的符号链接在容器内显示为符号链接，但在主机上不会。

### 与 Kubernetes 和 WSL 2 的文件共享

Docker Desktop 将 Windows 主机文件系统挂载在运行 Kubernetes 的容器内的 `/run/desktop` 下。
有关如何配置 Kubernetes 持久卷以表示主机目录的示例，请参阅 [Stack Overflow 帖子](https://stackoverflow.com/questions/67746843/clear-persistent-volume-from-a-kubernetes-cluster-running-on-docker-desktop/69273405#69273)。

### 如何添加自定义 CA 证书？

你可以在 Docker 守护进程中添加受信任的证书颁发机构（CA），用于验证注册表服务器证书，以及客户端证书，用于向注册表进行身份验证。

Docker Desktop 支持所有受信任的证书颁发机构（CA）（根 CA 或中间 CA）。Docker 识别存储在“受信任的根证书颁发机构”或“中间证书颁发机构”下的证书。

Docker Desktop 基于 Windows 证书存储创建所有用户信任的 CA 的证书包，并将其附加到 Moby 受信任证书中。因此，如果企业 SSL 证书在主机上被用户信任，它也会被 Docker Desktop 信任。

要了解如何为注册表安装 CA 根证书的更多信息，请参阅 Docker Engine 主题中的 [使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。

### 如何添加客户端证书？

你可以在 `~/.docker/certs.d/<MyRegistry><Port>/client.cert` 和 `~/.docker/certs.d/<MyRegistry><Port>/client.key` 中添加客户端证书。你不需要使用 `git` 命令推送你的证书。

当 Docker Desktop 应用启动时，它会将 Windows 系统上的 `~/.docker/certs.d` 文件夹复制到 Moby（在 Hyper-V 上运行的 Docker Desktop 虚拟机）的 `/etc/docker/certs.d` 目录中。

在对密钥链或 `~/.docker/certs.d` 目录进行任何更改后，你需要重启 Docker Desktop 才能使更改生效。

注册表不能列为不安全注册表（参见 [Docker 守护进程](/manuals/desktop/settings-and-maintenance/settings.md#docker-engine)）。Docker Desktop 会忽略列在不安全注册表中的证书，并且不会发送客户端证书。尝试从注册表拉取的 `docker run` 等命令会在命令行以及注册表上产生错误消息。

要了解如何设置客户端 TLS 证书进行验证的更多信息，请参阅 Docker Engine 主题中的 [使用证书验证仓库客户端](/manuals/engine/security/certificates.md)。