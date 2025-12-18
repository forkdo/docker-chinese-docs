---
title: 数据包过滤和防火墙
weight: 10
description: Docker 如何与数据包过滤、iptables 和防火墙协同工作
keywords: 网络, iptables, 防火墙
aliases:
- /network/iptables/
- /network/packet-filtering-firewalls/
---

在 Linux 上，Docker 会创建防火墙规则来实现网络隔离、[端口发布](./port-publishing.md) 和过滤。

由于这些规则对于 Docker 桥接网络的正确运行是必需的，因此不应修改 Docker 创建的规则。

本文档描述了控制 Docker 防火墙规则的选项，以实现端口发布、NAT/伪装等功能。

> [!NOTE]
> 
> Docker 为桥接网络创建防火墙规则。
> 
> 对于 `ipvlan`、`macvlan` 或 `host` 网络不会创建规则。

## 防火墙后端

默认情况下，Docker Engine 使用 iptables 创建其防火墙规则，参见 [Docker 与 iptables](./firewall-iptables.md)。它也支持 nftables，参见 [Docker 与 nftables](./firewall-nftables.md)。

对于桥接网络，iptables 和 nftables 具有相同的功能。

Docker Engine 选项 `firewall-backend` 可用于选择使用 iptables 还是 nftables。参见
[守护进程配置](https://docs.docker.com/reference/cli/dockerd/)。

## Docker 在路由器上

在 Linux 上，Docker 需要在主机上启用“IP 转发”。因此，当它启动时，如果 `sysctl` 设置 `net.ipv4.ip_forward` 和 `net.ipv6.conf.all.forwarding` 尚未启用，它会启用这些设置。当它这样做时，它还会配置防火墙以丢弃转发的数据包，除非它们被明确接受。

当 Docker 将默认转发策略设置为“丢弃”时，它会阻止您的 Docker 主机充当路由器。当启用 IP 转发时，这是推荐的设置，除非需要路由器功能。

要阻止 Docker 将转发策略设置为“丢弃”，请在 `/etc/docker/daemon.json` 中包含 `"ip-forward-no-drop": true`，或在 `dockerd` 命令行中添加选项 `--ip-forward-no-drop`。

> [!NOTE]
>
> 使用实验性的 nftables 后端时，Docker 不会自行启用 IP 转发，也不会创建默认的“丢弃”nftables 策略。参见
> [从 iptables 迁移到 nftables](./firewall-nftables.md#migrating-from-iptables-to-nftables)。

## 防止 Docker 操纵防火墙规则

在 [守护进程配置](https://docs.docker.com/reference/cli/dockerd/) 中将 `iptables` 或 `ip6tables` 键设置为 `false`，将阻止 Docker 创建其大部分 `iptables` 或 `nftables` 规则。但是，此选项不适用于大多数用户，它可能会破坏 Docker Engine 的容器网络。

例如，在禁用 Docker 的防火墙并且没有替代规则的情况下，桥接网络中的容器将无法通过伪装访问互联网主机，但它们的所有端口都将对本地网络上的主机开放。

完全阻止 Docker 创建防火墙规则是不可能的，事后创建规则非常复杂，超出了这些说明的范围。

## 与 firewalld 集成

如果在系统上启用了 [firewalld](https://firewalld.org)，并且 Docker 的 `iptables` 或 `ip6tables` 选项设置为 `true`，除了其常规的 iptables 或 nftables 规则外，Docker 还会创建一个名为 `docker`、目标为 `ACCEPT` 的 `firewalld` 区域。

Docker 创建的所有桥接网络接口（例如 `docker0`）都会插入到 `docker` 区域中。

Docker 还创建了一个名为 `docker-forwarding` 的转发策略，允许从 `ANY` 区域到 `docker` 区域的转发。

## Docker 与 ufw

[简化防火墙](https://launchpad.net/ufw)
(ufw) 是 Debian 和 Ubuntu 自带的防火墙前端，它允许您管理防火墙规则。Docker 和 ufw 以相互不兼容的方式使用防火墙规则。

当您使用 Docker 发布容器端口时，到该容器的流量在通过 ufw 防火墙设置之前就会被重定向。Docker 在 `nat` 表中路由容器流量，这意味着数据包在到达 ufw 使用的 `INPUT` 和 `OUTPUT` 链之前就被重定向了。数据包在防火墙规则应用之前就被路由，实际上忽略了您的防火墙配置。