---
description: 了解 Docker Desktop 如何处理网络、防火墙、文件访问、代理和端点可见性。
keywords: docker desktop, networking, architecture, firewall, proxies, crowdstrike, vpn
title: Docker Desktop 的网络功能
linkTitle: 网络
weight: 30
--- 

本文档解释了 Docker Desktop 如何在容器、虚拟机（VM）和主机之间路由网络流量和文件 I/O，以及这种行为如何被防火墙和终端保护工具识别。

## 概述

Docker Desktop 在轻量级 Linux 虚拟机（VM）内运行 Docker 引擎。根据您的系统配置和操作系统，Docker Desktop 使用不同的后端组件在 Docker VM 和主机之间路由网络和文件操作。

### 后端组件及其职责

后端组件充当：

- 网络代理：在主机和 Linux VM 之间转换流量。
   - 在 Windows 和 Mac 上，由 `com.docker.backend` 进程处理。
   - 在 Linux 上，由 `qemu` 进程执行此功能。
- 文件服务器：处理容器对主机文件系统的文件访问。
   - 使用 gRPC FUSE 时，后端执行文件共享。
   - 使用 `virtiofs`、`osxfs` 或 `krun` 时，文件访问由这些各自的守护进程处理，而非后端进程。
- 控制平面：管理 Docker API 调用、端口转发和代理配置。

下表更详细地总结了典型的设置：

| 平台        | 设置                                | 网络处理组件    | 文件共享处理组件                | 说明                                                     |
| --------------- | ------------------------------------ | ------------------------ | -------------------------------------- | --------------------------------------------------------- |
| Windows         | Hyper-V                              | `com.docker.backend.exe` | `com.docker.backend.exe`               | 最简单的设置，EDR/防火墙工具完全可见                         |
| Windows (WSL 2) | WSL 2                                | `com.docker.backend.exe` | WSL 2 内核（主机不可见） | 仅在需要 WSL 2 集成时推荐使用                             |
| Mac             | 虚拟化框架 + gRPC FUSE | `com.docker.backend`     | `com.docker.backend`                   | 推荐用于性能和可见性                                        |
| Mac             | 虚拟化框架 + `virtiofs`| `com.docker.backend`     | Apple 的虚拟化框架       | 性能更高，但主机无法看到文件访问                           |
| Mac             | 虚拟化框架 + `osxfs`   | `com.docker.backend`     | `osxfs`                                | 传统设置，不推荐使用                                        |
| Mac             | DockerVMM + `virtiofs`               | `com.docker.backend`     | `krun`                                 | 当前处于 Beta 阶段                                        |
| Linux           | 原生 Linux VM                      | `qemu`                   | `virtiofsd`                            | Linux 上没有 `com.docker.backend` 进程                    |


## 容器如何连接到互联网

Docker Desktop 中的每个 Linux 容器都在 Docker 管理的小型虚拟网络内运行，每个容器都连接到 Docker 管理的网络并获得自己的内部 IP 地址。您可以使用 `docker network ls`、`docker network create` 和 `docker network inspect` 查看和管理这些网络。它们由 [`daemon.json`](/manuals/engine/daemon/_index.md) 管理。

当容器发起网络请求时，例如使用 `apt-get update` 或 `docker pull`：

- 容器的 `eth0` 接口连接到 VM 内的虚拟网桥（`docker0`）。
- 容器的出站流量通过网络地址转换（NAT）使用虚拟适配器（通常具有类似 `192.168.65.3` 的内部 IP）传输。
- 流量通过共享内存通道传输到主机系统，而不是通过传统的虚拟网络接口。这种方法确保了可靠的通信，并避免了与主机级网络适配器或防火墙配置的冲突。
- 在主机上，Docker Desktop 的后端进程接收流量并使用与其他应用程序相同的网络 API 创建标准 TCP/IP 连接。

所有出站容器网络流量都来自 `com.docker.backend` 进程。防火墙、VPN 和安全工具（如 Crowdstrike）看到的流量来自此进程——而不是来自 VM 或未知源，因此防火墙和终端安全软件可以直接对 `com.docker.backend` 应用规则。

## 暴露端口的工作原理

当您使用 `-p` 或 `--publish` 标志发布容器端口时，Docker Desktop 使该容器端口可从主机系统或本地网络访问。

例如，使用 `docker run -p 80:80 nginx`：

- Docker Desktop 的后端进程在指定的主机端口（本例中为端口 `80`）上监听。
- 当应用程序（如 Web 浏览器）连接到该端口时，Docker Desktop 通过共享内存通道将连接转发到运行容器的 Linux VM。
- 在 VM 内，连接被路由到容器的内部 IP 地址和端口，例如 `172.17.0.2:80`。
- 容器通过相同路径响应，因此您可以像访问任何其他本地服务一样从主机访问它。

默认情况下，`docker run -p` 监听所有网络接口（`0.0.0.0`），但您可以将其限制为特定地址，例如 `127.0.0.1`（`localhost`）或特定网络适配器。此行为可以通过 [Docker Desktop 的网络设置](/manuals/desktop/settings-and-maintenance/settings.md#network) 修改为默认绑定到 `localhost`。

主机防火墙可以通过过滤 `com.docker.backend` 来允许或拒绝入站连接。

## 在 Docker Desktop 中使用代理

Docker Desktop 可以使用系统的默认代理设置或您使用 [Docker Desktop 的代理设置](/manuals/desktop/settings-and-maintenance/settings.md#proxies) 配置的自定义设置。所有代理流量都通过 `com.docker.backend.exe` 传输。

启用代理时：

- 后端进程通过内部代理 `http.docker.internal:3128` 转发网络请求，例如 `docker pull`。
- 内部代理然后直接连接到互联网或通过您的上游代理连接，具体取决于您的配置，并在必要时添加身份验证。
- Docker Desktop 然后通过代理下载请求的镜像或数据。

注意：
- 代理遵循系统或手动代理配置。
- 在 Windows 上，支持 Basic、NTLM 和 Kerberos 身份验证。
- 对于 Mac，不支持原生 NTLM/Kerberos。作为变通方案，在 `localhost` 上运行本地代理。
- 使用 Docker API 直接的 CLI 插件和其他工具必须使用 `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY` 环境变量单独配置。

## 防火墙和端点可见性

要限制 VM 或容器网络，请对 `com.docker.backend.exe`（Windows）、`com.docker.backend`（Mac）或 `qemu`（Linux）应用规则，因为所有 VM 网络都通过这些进程传输。

使用 Windows Defender 防火墙或企业端点防火墙进行控制。这使得在主机级别进行流量检查和限制，而无需修改 Docker 引擎。

Crowdstrike 和类似工具可以观察通过后端进程传输的所有流量和文件访问。

| 操作 | 主机 EDR 可见？ | 原因 | 
|---------|----------------------|---------| 
| 容器读取主机文件 | 是 | 由 `com.docker.backend` 处理访问 | 
| 容器写入主机文件 | 是 | 同一进程执行写入 | 
| 容器访问其自己的文件系统层 | 否 | 仅存在于 VM 内部 |