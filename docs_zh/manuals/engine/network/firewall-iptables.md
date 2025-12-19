---
title: Docker 与 iptables
weight: 10
description: Docker 如何与 iptables 协同工作
keywords: network, iptables, firewall
---

Docker 为桥接网络在主机的网络命名空间中创建 iptables 规则。对于桥接和其他网络类型，DNS 的 iptables 规则也会在容器的网络命名空间中创建。

可以使用守护进程选项 `iptables` 和 `ip6tables` 禁用 iptables 规则的创建，参见[防止 Docker 操作防火墙规则](packet-filtering-firewalls.md#prevent-docker-from-manipulating-firewall-rules)。
但是，对于大多数用户来说，不建议这样做，因为它很可能会破坏容器网络。

### Docker 和 iptables 链

为了支持桥接和覆盖网络，Docker 在 `filter` 表中创建以下自定义 `iptables` 链：

* `DOCKER-USER`
    * 用户定义规则的占位符，这些规则将在 `DOCKER-FORWARD` 和 `DOCKER` 链中的规则之前被处理。
* `DOCKER-FORWARD`
    * Docker 网络处理的第一阶段。将与已建立连接无关的数据包传递给其他 Docker 链的规则，以及接受属于已建立连接部分的数据包的规则。
* `DOCKER`, `DOCKER-BRIDGE`, `DOCKER-INTERNAL`
    * 根据运行容器的端口转发配置，决定是否应接受不属于已建立连接的数据包的规则。
* `DOCKER-CT`
    * 每个桥接的连接跟踪规则。
* `DOCKER-INGRESS`
    * 与 Swarm 网络相关的规则。

在 `FORWARD` 链中，Docker 添加无条件跳转到 `DOCKER-USER`、`DOCKER-FORWARD` 和 `DOCKER-INGRESS` 链的规则。

在 `nat` 表中，Docker 创建链 `DOCKER` 并添加规则以实现伪装和端口映射。

Docker 需要主机上启用 IP 转发才能进行其默认桥接网络配置。如果它启用了 IP 转发，它还会将 `filter` 表中 iptables `FORWARD` 链的默认策略设置为 `DROP`。

### 在 Docker 规则之前添加 iptables 策略

被这些自定义链中的规则接受或拒绝的数据包将不会被附加到 `FORWARD` 链的用户定义规则看到。因此，要添加额外的规则来过滤这些数据包，请使用 `DOCKER-USER` 链。

附加到 `FORWARD` 链的规则将在 Docker 的规则之后被处理。

### 匹配请求的原始 IP 和端口

当数据包到达 `DOCKER-USER` 链时，它们已经通过了目标网络地址转换（DNAT）过滤器。这意味着您使用的 `iptables` 标志只能匹配容器的内部 IP 地址和端口。

如果您想根据网络请求中的原始 IP 和端口来匹配流量，您必须使用
[`conntrack` iptables 扩展](https://ipset.netfilter.org/iptables-extensions.man.html#lbAO)。例如：

```console
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -I DOCKER-USER -p tcp -m conntrack --ctorigdst 198.51.100.2 --ctorigdstport 80 -j ACCEPT
```

> [!IMPORTANT]
>
> 使用 `conntrack` 扩展可能会导致性能下降。

### 允许主机接口之间的转发

如果 Docker 已将 `filter` 表中 `FORWARD` 链的默认策略设置为 `DROP`，则可以使用 `DOCKER-USER` 中的规则来允许主机接口之间的转发。例如：

```console
$ iptables -I DOCKER-USER -i src_if -o dst_if -j ACCEPT
```

### 限制外部连接到容器

默认情况下，允许所有外部源 IP 连接到已发布到 Docker 主机地址的端口。

要仅允许特定 IP 或网络访问容器，请在 `DOCKER-USER` 过滤链的顶部插入一个否定规则。例如，以下规则丢弃除 `192.0.2.2` 之外的所有 IP 地址的数据包：

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.2 -j DROP
```

您需要将 `ext_if` 更改为您主机实际的外部接口。您也可以改为允许来自源子网的连接。以下规则仅允许来自子网 `192.0.2.0/24` 的访问：

```console
$ iptables -I DOCKER-USER -i ext_if ! -s 192.0.2.0/24 -j DROP
```

最后，您可以使用 `--src-range` 指定要接受的 IP 地址范围（请记住，使用 `--src-range` 或 `--dst-range` 时也要添加 `-m iprange`）：

```console
$ iptables -I DOCKER-USER -m iprange -i ext_if ! --src-range 192.0.2.1-192.0.2.3 -j DROP
```

您可以将 `-s` 或 `--src-range` 与 `-d` 或 `--dst-range` 结合使用，以同时控制源和目标。例如，如果 Docker 主机具有地址 `2001:db8:1111::2` 和 `2001:db8:2222::2`，您可以使规则特定于 `2001:db8:1111::2`，而让 `2001:db8:2222::2` 保持开放。

您可能需要允许来自允许的外部地址范围之外的服务器的响应。例如，容器可能会向不允许访问容器服务的主机发送 DNS 或 HTTP 请求。以下规则接受属于已被其他规则接受的流的任何传入或传出数据包。它必须放置在限制来自外部地址范围访问的 `DROP` 规则之前。

```console
$ iptables -I DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT
```

有关 iptables 配置和高级用法的更多信息，请参阅 [Netfilter.org HOWTO](https://www.netfilter.org/documentation/HOWTO/NAT-HOWTO.html)。