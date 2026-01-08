---
---
title: Packet filtering and firewalls
weight: 10
description: "How Docker works with packet filtering, iptables, and firewalls"
aliases:
  - /network/iptables/
  - /network/packet-filtering-firewalls/
keywords: "network, iptables, firewall"---
title: 数据包过滤和防火墙
weight: 10
description: "Docker 如何处理数据包过滤、iptables 和防火墙"---
在 Linux 系统上，Docker 会创建防火墙规则来实现网络隔离、[端口发布](./port-publishing.md) 和过滤功能。

由于这些规则对于 Docker 桥接网络的正常运行至关重要，因此不应修改 Docker 创建的规则。

本页面介绍了控制 Docker 防火墙规则的选项，这些规则用于实现端口发布和 NAT/伪装等功能。

> [!NOTE]
> 
> Docker 仅为桥接网络创建防火墙规则。
> 
> 对于 `ipvlan`、`macvlan` 或 `host` 网络模式，不会创建任何规则。

## 防火墙后端

默认情况下，Docker 引擎使用 iptables 创建防火墙规则，
参见 [Docker 与 iptables](./firewall-iptables.md)。它也支持 nftables，
参见 [Docker 与 nftables](./firewall-nftables.md)。

对于桥接网络，iptables 和 nftables 具有相同的功能。

Docker 引擎选项 `firewall-backend` 可用于选择使用 iptables 还是 nftables。
参见 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/)。

## 在路由器上使用 Docker

在 Linux 系统上，Docker 需要在主机上启用 "IP 转发" 功能。因此，当 Docker 启动时，
如果尚未启用，它会自动启用 `sysctl` 设置 `net.ipv4.ip_forward` 和 
`net.ipv6.conf.all.forwarding`。当它执行此操作时，还会配置防火墙以丢弃转发的数据包，
除非这些数据包被明确允许。

当 Docker 将默认转发策略设置为 "drop" 时，它将阻止您的 Docker 主机充当路由器。
这是在启用 IP 转发时的推荐设置，除非确实需要路由器功能。

要阻止 Docker 将转发策略设置为 "drop"，请在 `/etc/docker/daemon.json` 中包含
`"ip-forward-no-drop": true`，或者在 `dockerd` 命令行中添加选项 `--ip-forward-no-drop`。

> [!NOTE]
>
> 使用实验性的 nftables 后端时，Docker 本身不会启用 IP 转发，
> 也不会创建默认的 "drop" nftables 策略。参见
> [从 iptables 迁移到 nftables](./firewall-nftables.md#migrating-from-iptables-to-nftables)。

## 阻止 Docker 操作防火墙规则

在 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/) 中将 `iptables` 
或 `ip6tables` 键设置为 `false`，可以阻止 Docker 创建其大部分的 `iptables` 
或 `nftables` 规则。但是，此选项对大多数用户来说并不合适，
因为它很可能会破坏 Docker 引擎的容器网络功能。

例如，在禁用 Docker 防火墙且没有替代规则的情况下，桥接网络中的容器将无法通过伪装访问互联网主机，
但其所有端口都将对本地网络上的主机开放访问。

无法完全阻止 Docker 创建防火墙规则，而在事后创建规则则非常复杂，超出了本指南的范围。

## 与 firewalld 的集成

如果您在运行 Docker 时将 `iptables` 或 `ip6tables` 选项设置为 `true`，
并且系统上启用了 [firewalld](https://firewalld.org)，除了其通常的 iptables 
或 nftables 规则外，Docker 还会创建一个名为 `docker` 的 `firewalld` 区域，
目标设置为 `ACCEPT`。

Docker 创建的所有桥接网络接口（例如 `docker0`）都会被插入到 `docker` 区域中。

Docker 还会创建一个名为 `docker-forwarding` 的转发策略，
允许从 `ANY` 区域转发到 `docker` 区域。

## Docker 与 ufw

[Uncomplicated Firewall](https://launchpad.net/ufw)
(ufw) 是 Debian 和 Ubuntu 系统自带的前端工具，
用于管理防火墙规则。Docker 和 ufw 使用防火墙规则的方式使它们彼此不兼容。

当您使用 Docker 发布容器的端口时，进出该容器的流量会在经过 ufw 防火墙设置之前被重定向。
Docker 在 `nat` 表中路由容器流量，这意味着数据包会在到达 ufw 使用的 `INPUT` 和 `OUTPUT` 
链之前被重定向。数据包在防火墙规则应用之前就被路由了，
从而有效地忽略了您的防火墙配置。