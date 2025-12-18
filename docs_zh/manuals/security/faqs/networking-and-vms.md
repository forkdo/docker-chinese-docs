---
title: 网络和虚拟机常见问题
linkTitle: 网络和虚拟机
description: Docker Desktop 网络和虚拟化安全的常见问题
keywords: docker desktop networking, virtualization, hyper-v, wsl2, network security, firewall
weight: 30
tags: [FAQ]
aliases:
- /faq/security/networking-and-vms/
---

## 如何限制容器的互联网访问？

Docker Desktop 没有内置的限制机制，但您可以在主机上使用进程级防火墙。对 `com.docker.vpnkit` 用户空间进程应用规则，以控制它可以连接的位置（DNS 白名单、数据包过滤器）以及可以使用的端口/协议。

对于企业环境，可以考虑使用 [Air-gapped containers](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md)，它提供对容器的网络访问控制。

## 可以对容器网络流量应用防火墙规则吗？

可以。Docker Desktop 使用用户空间进程（`com.docker.vpnkit`）进行网络连接，该进程会继承启动它的用户所设置的约束，如防火墙规则、VPN 设置和 HTTP 代理属性。

## 使用 Hyper-V 的 Docker Desktop for Windows 是否允许用户创建其他虚拟机？

不允许。`DockerDesktopVM` 名称在服务中是硬编码的，因此您无法使用 Docker Desktop 创建或操作其他虚拟机。

## Docker Desktop 如何在 Hyper-V 和 WSL 2 中实现网络隔离？

Docker Desktop 在 WSL 2（在 `docker-desktop` 发行版中）和 Hyper-V（在 `DockerDesktopVM` 中）中使用相同的 VM 进程。主机/VM 通信使用 `AF_VSOCK` 超管理器套接字（共享内存），而不是网络交换机或接口。所有主机网络通信都是通过 `com.docker.vpnkit.exe` 和 `com.docker.backend.exe` 进程使用标准 TCP/IP 套接字完成的。

更多信息，请参阅 [Docker Desktop 网络的工作原理](https://www.docker.com/blog/how-docker-desktop-networking-works-under-the-hood/)。