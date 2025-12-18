---
title: Docker 与 nftables
weight: 10
description: Docker 如何与 nftables 协同工作
keywords: 网络, nftables, 防火墙
---

> [!WARNING]
>
> Docker 29.0.0 中引入的 nftables 支持目前处于实验阶段，配置选项、行为和实现可能在未来的版本中发生变化。
> 覆盖网络（overlay networks）的规则尚未从 iptables 迁移。因此，当 Docker 守护进程以 Swarm 模式运行时，无法启用 nftables。

要使用 nftables 而非 iptables，可在 Docker Engine 命令行中使用选项 `--firewall-backend=nftables`，或在配置文件中添加 `"firewall-backend": "nftables"`。您可能还需要修改主机上的 IP 转发配置，并将 iptables `DOCKER-USER` 链中的规则迁移到 nftables，参见[从 iptables 迁移到 nftables](#migrating-from-iptables-to-nftables)。

对于桥接网络，Docker 在主机的网络命名空间中创建 nftables 规则。对于桥接网络和其他网络类型，Docker 也会在容器的网络命名空间中创建 DNS 相关的 nftables 规则。

可以使用守护进程选项 `iptables` 和 `ip6tables` 禁用 nftables 规则的创建。_这些选项同时适用于 iptables 和 nftables。_ 参见 [防止 Docker 操控防火墙规则](packet-filtering-firewalls.md#prevent-docker-from-manipulating-firewall-rules)。不过，对于大多数用户，不建议这样做，因为它很可能破坏容器网络。

## Docker 的 nftables 表

对于桥接网络，Docker 创建两个表：`ip docker-bridges` 和 `ip6 docker-bridges`。

每个表包含多个[基础链](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Adding_base_chains)，并为每个桥接网络添加更多链。Moby 项目有一些[内部文档](https://github.com/moby/moby/blob/master/integration/network/bridge/nftablesdoc/index.md)描述其 nftables 及其如何依赖于网络和容器配置。但这些表及其规则在 Docker Engine 不同版本之间可能会发生变化。

> [!NOTE]
>
> 请勿直接修改 Docker 的表，因为这些修改很可能会丢失，Docker 期望完全拥有其表。

> [!NOTE]
>
> 由于 iptables 有一组固定的链，等同于 nftables 的基础链，所有规则都包含在这些链中。`DOCKER-USER` 链用于在 Docker 规则之前插入到 `filter` 表的 `FORWARD` 链中的规则。
> 在 Docker 的 nftables 实现中，没有 `DOCKER-USER` 链。相反，您可以在单独的表中添加规则，这些表的基础链具有与 Docker 基础链相同的类型和钩子点。如有必要，可以使用[基础链优先级](https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains#Base_chain_priority)来告诉 nftables 调用链的顺序。Docker 对其每个基础链使用众所周知的[优先级值](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook)。

## 从 iptables 迁移到 nftables

如果 Docker 守护进程之前使用 iptables 防火墙后端运行，重启时使用 nftables 后端，Docker 将删除其大部分 iptables 链和规则，并改为创建 nftables 规则。

如果未启用 IP 转发，Docker 在创建需要它的桥接网络时会报告错误。由于默认桥接网络的存在，如果 IPv4 转发被禁用，错误将在守护进程启动期间报告。参见 [IP 转发](#ip-forwarding)。

如果您在 `DOCKER-USER` 链中有规则，请参见 [迁移 `DOCKER-USER`](#migrating-docker-user)。

如果 `FORWARD` 策略被 Docker 使用 iptables 设置为 `DROP`，或作为主机防火墙配置的一部分，您可能需要手动更新 iptables 的 `FORWARD` 策略。参见 [iptables 中的 FORWARD 策略](#forward-policy-in-iptables)。

### IP 转发

Docker 主机上的 IP 转发启用了 Docker 的功能，包括端口发布、桥接网络之间的通信以及从主机外部到桥接网络中容器的直接路由。

使用 iptables 运行时，根据网络和守护进程配置，Docker 可能在主机上启用 IPv4 和 IPv6 转发。

启用 nftables 防火墙后端后，Docker 不会自行启用 IP 转发。如果需要转发但尚未启用，它将报告错误。要禁用 Docker 对 IP 转发的检查，让它在确定转发被禁用时仍能启动并创建网络，可使用守护进程选项 `--ip-forward=false`，或在配置文件中添加 `"ip-forward": false`。

> [!WARNING]
>
> 启用 IP 转发时，请确保有防火墙规则阻止非 Docker 接口之间的不必要转发。

> [!NOTE]
>
> 如果您停止 Docker 以迁移到 nftables，Docker 可能已经在您的系统上启用了 IP 转发。重启后，如果其他服务未重新启用转发，Docker 将无法启动。

如果 Docker 在具有单个网络接口且无其他软件运行的虚拟机中，可能没有不必要转发需要阻止。但在具有多个网络接口的物理主机上，除非主机充当路由器，否则这些接口之间的转发可能需要使用 nftables 规则阻止。

要在主机上启用 IP 转发，请设置以下 sysctl：

- `net.ipv4.ip_forward=1`
- `net.ipv6.conf.all.forwarding=1`

如果您的主机使用 `systemd`，您可能可以使用 `systemd-sysctl`。例如，通过编辑 `/etc/sysctl.d/99-sysctl.conf`。

如果主机运行 `firewalld`，您可能可以使用它来阻止不必要转发。Docker 的桥接网络位于名为 `docker` 的 firewalld 区域中，它创建了一个名为 `docker-forwarding` 的转发策略，接受从 `ANY` 区域到 `docker` 区域的转发。

例如，要使用 nftables 阻止接口 `eth0` 和 `eth1` 之间的转发，您可以使用：

```console
table inet no-ext-forwarding {
	chain no-ext-forwarding {
		type filter hook forward priority filter; policy accept;
		iifname "eth0" oifname "eth1" drop
		iifname "eth1" oifname "eth0" drop
	}
}
```

### iptables 中的 FORWARD 策略

iptables 链的 `FORWARD` 策略为 `DROP` 时，即使包已被 Docker 的 nftables 规则接受，它仍会被 iptables 链处理，因此会被丢弃。

除非移除 `DROP` 策略或在 iptables 的 `FORWARD` 链中添加额外规则以接受 Docker 相关流量，否则某些功能（包括端口发布）将无法工作。

当 Docker 使用 iptables 且在主机上启用 IP 转发时，它将 iptables `FORWARD` 链的默认策略设置为 `DROP`。因此，如果您停止 Docker 以迁移到 nftables，它可能已设置了 `DROP` 策略，您需要移除它。无论如何，重启后它会被移除。

要继续使用依赖于链策略为 `DROP` 的 `DOCKER-USER` 规则，您必须为 Docker 相关流量添加显式的 `ACCEPT` 规则。

要检查当前的 iptables `FORWARD` 策略，请使用：

```console
$ iptables -L FORWARD
Chain FORWARD (policy DROP)
target     prot opt source               destination
$ ip6tables -L FORWARD
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
```

要将 IPv4 和 IPv6 的 iptables 策略设置为 `ACCEPT`：

```console
$ iptables -P FORWARD ACCEPT
$ ip6tables -P FORWARD ACCEPT
```

### 迁移 `DOCKER-USER`

使用防火墙后端 "iptables" 时，添加到 iptables `DOCKER-USER` 的规则在 Docker 的 filter 表 `FORWARD` 链规则之前处理。

使用 nftables 启动守护进程后，Docker 不会移除从 `FORWARD` 链到 `DOCKER-USER` 的跳转。因此，`DOCKER-USER` 中创建的规则将继续运行，直到跳转被移除或主机重启。

使用 nftables 启动时，守护进程不会添加跳转。因此，除非存在现有跳转，否则 `DOCKER-USER` 中的规则将被忽略。

#### 迁移 ACCEPT 规则

`DOCKER-USER` 链中的某些规则将继续工作。例如，如果包被丢弃，它将在 Docker 的 nftables 规则之前或之后被丢弃。但其他规则，特别是用于覆盖 Docker `DROP` 规则的 `ACCEPT` 规则，将无法工作。

在 nftables 中，"accept" 规则不是最终的。它终止其基础链的处理，但被接受的包仍会被其他基础链处理，这些链可能丢弃它。

要覆盖 Docker 的 `drop` 规则，您必须使用防火墙标记。选择主机上未使用的标记，并使用 Docker Engine 选项 `--bridge-accept-fwmark`。

例如，`--bridge-accept-fwmark=1` 告诉守护进程接受任何 `fwmark` 值为 `1` 的包。可选地，您可以提供掩码以匹配标记中的特定位，如 `--bridge-accept-fwmark=0x1/0x3`。

然后，不是在 `DOCKER-USER` 中接受包，而是添加您选择的防火墙标记，Docker 将不会丢弃它。

防火墙标记必须在 Docker 规则运行之前添加。因此，如果标记在类型为 `filter`、钩子为 `forward` 的链中添加，它必须具有优先级 `filter - 1` 或更低。

#### 使用 nftables 表替换 `DOCKER-USER`

由于 nftables 没有预定义的链，要替换 `DOCKER-USER` 链，您可以创建自己的表并添加链和规则。

`DOCKER-USER` 链的类型为 `filter`，钩子为 `forward`，因此它只能在 filter forward 链中有规则。您表中的基础链可以有任何 `type` 或 `hook`。如果您的规则需要在 Docker 规则之前运行，请给基础链分配比 Docker 链更低的 `priority` 数字。或者，使用更高的优先级确保它们在 Docker 规则之后运行。

Docker 的基础链使用 [优先级值](https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks#Priority_within_hook) 中定义的优先级值。

#### 示例：限制到容器的外部连接

默认情况下，任何远程主机都可以连接到发布到 Docker 主机外部地址的端口。

要仅允许特定 IP 或网络访问容器，创建一个带有基础链的表，该链包含丢弃规则。例如，以下表丢弃来自除 `192.0.2.2` 之外的所有 IP 地址的包：

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" ip saddr != 192.0.2.2 counter drop
	}
}
```

您需要将 `ext_if` 更改为您的主机外部接口名称。

您也可以接受来自特定源子网的连接。以下表仅接受来自子网 `192.0.2.0/24` 的访问：

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" ip saddr != 192.0.2.0/24 counter drop
	}
}
```

如果您在主机上运行其他使用 IP 转发并需要被不同外部主机访问的服务，您将需要更具体的过滤器。例如，匹配 Docker 用户定义桥接网络所属的桥接设备的默认前缀 `br-`：

```console
table ip my-table {
	chain my-filter-forward {
		type filter hook forward priority filter; policy accept;
		iifname "ext_if" oifname "br-*" ip saddr != 192.0.2.0/24 counter drop
	}
}
```

有关 nftables 配置和高级使用的更多信息，请参考 [nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)。