---
title: 数据包过滤与防火墙
weight: 10
description: Docker 如何与数据包过滤、iptables 和防火墙协同工作
keywords: network, iptables, firewall
aliases:
- /network/iptables/
- /network/packet-filtering-firewalls/
---

在 Linux 上，Docker 会创建防火墙规则以实现网络隔离、[端口发布](./port-publishing.md)和过滤。

由于这些规则对于 Docker 桥接网络的正常运行是必需的，因此您不应修改 Docker 创建的规则。

本页介绍控制 Docker 防火墙规则的选项，这些规则用于实现端口发布以及 NAT/伪装等功能。

> [!NOTE]
> 
> Docker 为桥接网络创建防火墙规则。
> 
> 不会为 `ipvlan`、`macvlan` 或 `host` 网络创建规则。

## 防火墙后端

默认情况下，Docker Engine 使用 iptables 创建其防火墙规则，参见 [Docker 与 iptables](./firewall-iptables.md)。它也支持 nftables，参见 [Docker 与 nftables](./firewall-nftables.md)。

对于桥接网络，iptables 和 nftables 具有相同的功能。

Docker Engine 选项 `firewall-backend` 可用于选择使用 iptables 还是 nftables。请参阅 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/)。

## 路由器上的 Docker

在 Linux 上，Docker 需要在主机上启用“IP 转发”。因此，如果 `sysctl` 设置 `net.ipv4.ip_forward` 和 `net.ipv6.conf.all.forwarding` 在启动时尚未启用，Docker 会启用它们。当它这样做时，它还会配置防火墙以丢弃转发的数据包，除非它们被显式接受。

当 Docker 将默认转发策略设置为“丢弃”（drop）时，它将阻止您的 Docker 主机充当路由器。这是在启用 IP 转发时的推荐设置，除非需要路由器功能。

要阻止 Docker 将转发策略设置为“丢弃”，请在 `/etc/docker/daemon.json` 中包含 `"ip-forward-no-drop": true`，或者向 `dockerd` 命令行添加选项 `--ip-forward-no-drop`。

> [!NOTE]
>
> 使用实验性的 nftables 后端时，Docker 本身不会启用 IP 转发，也不会创建默认的“丢弃”nftables 策略。请参阅 [从 iptables 迁移到 nftables](./firewall-nftables.md#migrating-from-iptables-to-nftables)。

## 防止 Docker 操作防火墙规则

在 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/) 中将 `iptables` 或 `ip6tables` 键设置为 `false`，将阻止 Docker 创建其大部分 `iptables` 或 `nftables` 规则。但是，此选项不适合大多数用户，它可能会破坏 Docker Engine 的容器网络。

例如，如果禁用了 Docker 防火墙且没有替换规则，桥接网络中的容器将无法通过伪装访问互联网主机，但其所有端口都将对本地网络上的主机可访问。

无法完全阻止 Docker 创建防火墙规则，并且事后创建规则非常复杂，超出了这些说明的范围。

## 与 firewalld 集成

如果您在将 `iptables` 或 `ip6tables` 选项设置为 `true` 的情况下运行 Docker，并且您的系统上启用了 [firewalld](https://firewalld.org)，那么除了其通常的 iptables 或 nftables 规则外，Docker 还会创建一个名为 `docker` 的 `firewalld` 区域，其目标为 `ACCEPT`。

Docker 创建的所有桥接网络接口（例如 `docker0`）都会被插入到 `docker` 区域中。

Docker 还会创建一个名为 `docker-forwarding` 的转发策略，允许从 `ANY` 区域到 `docker` 区域的转发。

## Docker 与 ufw

[Uncomplicated Firewall](https://launchpad.net/ufw) (ufw) 是一个随 Debian 和 Ubuntu 附带的前端，它允许您管理防火墙规则。Docker 和 ufw 使用防火墙规则的方式使它们彼此不兼容。

当您使用 Docker 发布容器的端口时，进出该容器的流量在经过 ufw 防火墙设置之前就会被转移。Docker 在 `nat` 表中路由容器流量，这意味着数据包在到达 ufw 使用的 `INPUT` 和 `OUTPUT` 链之前就被转移了。数据包在防火墙规则应用之前就被路由了，从而有效地忽略了您的防火墙配置。