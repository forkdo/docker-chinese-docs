---
title: IPvlan 网络驱动
description: 有关使用 IPvlan 让容器在网络中显示为物理机器的所有信息
keywords: network, ipvlan, l2, l3, standalone
aliases:
- /network/ipvlan/
- /network/drivers/ipvlan/
---

IPvlan 驱动让用户完全控制 IPv4 和 IPv6 地址分配。VLAN 驱动在此基础上更进一步，让操作员完全控制第 2 层 VLAN 标记，甚至包括对底层网络集成感兴趣的用户的 IPvlan L3 路由。对于抽象物理约束的覆盖（overlay）部署，请参阅 [多主机覆盖](overlay.md) 驱动。

IPvlan 是对久经考验的网络虚拟化技术的一种新尝试。Linux 的实现极其轻量级，因为它们不是使用传统的 Linux 网桥进行隔离，而是关联到一个 Linux 以太网接口或子接口，以强制执行网络之间的隔离并连接到物理网络。

IPvlan 提供了许多独特的功能，并且各种模式为未来的创新提供了充足的空间。这些方法的两个高级优势是：绕过 Linux 网桥带来的积极性能影响，以及拥有更少活动部件的简单性。移除传统上位于 Docker 主机网卡和容器接口之间的网桥，留下了一个由容器接口组成的简单设置，这些接口直接连接到 Docker 主机接口。对于面向外部的服务来说，这种结果很容易访问，因为在这些场景中不需要端口映射。

## 选项

下表描述了使用 `ipvlan` 驱动创建网络时，可以传递给 `--opt` 的驱动特定选项。

| Option        | Default  | Description                                                           |
| ------------- | -------- | --------------------------------------------------------------------- |
| `ipvlan_mode` | `l2`     | 设置 IPvlan 操作模式。可以是：`l2`、`l3`、`l3s` 之一      |
| `ipvlan_flag` | `bridge` | 设置 IPvlan 模式标志。可以是：`bridge`、`private`、`vepa` 之一 |
| `parent`      |          | 指定要使用的父接口。                                |

## 示例

### 先决条件

- 本页上的所有示例都是单主机示例。
- 所有示例都可以在运行 Docker 的单台主机上执行。任何使用子接口（如 `eth0.10`）的示例都可以替换为 `eth0` 或 Docker 主机上的任何其他有效的父接口。带有 `.` 的子接口是动态创建的。`-o parent` 接口也可以完全省略，驱动将创建一个 `dummy` 接口，以便执行示例时本地主机能够连接。
- 内核要求：
  - IPvlan Linux 内核 v4.2+（支持更早的内核但存在错误）。要检查当前内核版本，请使用 `uname -r`。

### IPvlan L2 模式示例用法

IPvlan `L2` 模式拓扑的示例如下图所示。驱动通过 `-d driver_name` 选项指定。本例中为 `-d ipvlan`。

![简单的 IPvlan L2 模式示例](images/ipvlan_l2_simple.png)

下一个示例中的父接口 `-o parent=eth0` 配置如下：

```console
$ ip addr show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

使用主机接口的网络作为 `docker network create` 中的 `--subnet`。容器将通过 `-o parent=` 选项附加到与主机接口相同的网络。

创建 IPvlan 网络并运行一个连接到该网络的容器：

```console
# IPvlan  (-o ipvlan_mode= 如果未指定，默认为 L2 模式)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 db_net

# 在 db_net 网络上启动一个容器
$ docker run --net=db_net -it --rm alpine /bin/sh

# 注意：容器无法 ping 底层主机接口，因为 Linux 为了额外的隔离而有意过滤了这些 ping。
```

IPvlan 的默认模式是 `l2`。如果 `-o ipvlan_mode=` 未指定，则使用默认模式。同样，如果 `--gateway` 为空，则将网络上的第一个可用地址设置为网关。例如，如果在网络创建时提供的子网是 `--subnet=192.168.1.0/24`，那么容器收到的网关将是 `192.168.1.1`。

为了帮助理解此模式如何与其他主机交互，下图显示了两个 Docker 主机之间的相同第 2 层网段，该网段适用于 IPvlan L2 模式。

![多个 IPvlan 主机](images/macvlan-bridge-ipvlan-l2.webp?w=700)

以下命令将创建与之前创建的网络 `db_net` 完全相同的网络，使用驱动的默认值 `--gateway=192.168.1.1` 和 `-o ipvlan_mode=l2`。

```console
# IPvlan  (-o ipvlan_mode= 如果未指定，默认为 L2 模式)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    -o parent=eth0 db_net_ipv

# 以守护进程模式启动一个具有显式名称的容器
$ docker run --net=db_net_ipv --name=ipv1 -itd alpine /bin/sh

# 启动第二个容器并使用容器名称 ping，以查看 docker 包含的名称解析功能
$ docker run --net=db_net_ipv --name=ipv2 -it --rm alpine /bin/sh
$ ping -c 4 ipv1

# 注意：容器无法 ping 底层主机接口，因为 Linux 为了额外的隔离而有意过滤了这些 ping。
```

驱动还支持 `--internal` 标志，该标志将完全隔离网络上的容器与该网络外部的任何通信。由于网络隔离与网络的父接口紧密耦合，因此在 `docker network create` 中省略 `-o parent=` 选项的结果与使用 `--internal` 选项完全相同。如果未指定父接口或使用了 `--internal` 标志，驱动将为用户创建一个 netlink 类型的 `dummy` 父接口并用作父接口，从而有效地完全隔离网络。

以下两个 `docker network create` 示例会产生相同的网络，您可以将容器附加到这些网络：

```console
# 空的 '-o parent=' 创建一个隔离的网络
$ docker network create -d ipvlan \
    --subnet=192.168.10.0/24 isolated1

# 显式的 '--internal' 标志效果相同：
$ docker network create -d ipvlan \
    --subnet=192.168.11.0/24 --internal isolated2

# 甚至 '--subnet=' 也可以留空，将分配默认的
# IPAM 子网 172.18.0.0/16
$ docker network create -d ipvlan isolated3

$ docker run --net=isolated1 --name=cid1 -it --rm alpine /bin/sh
$ docker run --net=isolated2 --name=cid2 -it --rm alpine /bin/sh
$ docker run --net=isolated3 --name=cid3 -it --rm alpine /bin/sh

# 要连接到任何容器，请使用 `docker exec` 并启动 shell
$ docker exec -it cid1 /bin/sh
$ docker exec -it cid2 /bin/sh
$ docker exec -it cid3 /bin/sh
```

### IPvlan 802.1Q 中继 L2 模式示例用法

在架构上，IPvlan L2 模式中继在网关和 L2 路径隔离方面与 Macvlan 相同。存在一些细微差别，这些差别可能对 ToR（架顶式）交换机中的 CAM 表压力、每个端口一个 MAC 以及主机父网卡上的 MAC 耗尽等是有利的。802.1Q 中继场景看起来是相同的。两种模式都遵守标记标准，并与物理网络无缝集成，用于底层集成和硬件供应商插件集成。

同一 VLAN 上的主机通常位于同一子网中，并且几乎总是根据其安全策略分组在一起。在大多数情况下，多层应用程序被分层到不同的子网中，因为每个进程的安全配置文件需要某种形式的隔离。例如，将信用卡处理托管在与前端 Web 服务器相同的虚拟网络上将是一个法规遵从性问题，并且规避了长期以来的深度防御分层架构的最佳实践。VLAN 或使用覆盖驱动程序时的等效 VNI（虚拟网络标识符）是隔离租户流量的第一步。

![深入探讨 Docker VLAN](images/vlans-deeper-look.webp)

带有 VLAN 标记的 Linux 子接口可以已经存在，也可以在调用 `docker network create` 时创建。`docker network rm` 将删除子接口。像 `eth0` 这样的父接口不会被删除，只删除 netlink 父索引 > 0 的子接口。

为了让驱动添加/删除 VLAN 子接口，格式需要是 `interface_name.vlan_tag`。可以使用其他子接口命名作为指定的父接口，但链接不会在调用 `docker network rm` 时自动删除。

使用现有的父 VLAN 子接口或让 Docker 管理它们的选项使用户能够完全管理 Linux 接口和网络，或者让 Docker 创建和删除 VLAN 父子接口（netlink `ip link`），而无需用户费心。

例如：使用 `eth0.10` 表示 `eth0` 的子接口，标记为 VLAN id `10`。等效的 `ip link` 命令将是 `ip link add link eth0 name eth0.10 type vlan id 10`。

该示例创建了 VLAN 标记的网络，然后启动两个容器以测试容器之间的连接性。不同的 VLAN 无法相互 ping 通，除非有路由器在两个网络之间进行路由。默认命名空间根据 IPvlan 设计是不可达的，以便将容器命名空间与底层主机隔离。

#### VLAN ID 20

在第一个由 Docker 主机标记和隔离的网络中，`eth0.20` 是使用 `-o parent=eth0.20` 指定的标记为 VLAN id `20` 的父接口。可以使用其他命名格式，但需要使用 `ip link` 或 Linux 配置文件手动添加和删除链接。只要 `-o parent` 存在，任何符合 Linux netlink 的内容都可以使用。

```console
# 现在像往常一样添加网络和主机，附加到已标记的主（子）接口
$ docker network create -d ipvlan \
    --subnet=192.168.20.0/24 \
    --gateway=192.168.20.1 \
    -o parent=eth0.20 ipvlan20

# 在两个单独的终端中，启动一个 Docker 容器，容器现在可以相互 ping 通。
$ docker run --net=ipvlan20 -it --name ivlan_test1 --rm alpine /bin/sh
$ docker run --net=ipvlan20 -it --name ivlan_test2 --rm alpine /bin/sh
```

#### VLAN ID 30

在第二个由 Docker 主机标记和隔离的网络中，`eth0.30` 是使用 `-o parent=eth0.30` 指定的标记为 VLAN id `30` 的父接口。`ipvlan_mode=` 默认为 l2 模式 `ipvlan_mode=l2`。也可以显式设置，结果相同，如下一个示例所示。

```console
# 现在像往常一样添加网络和主机，附加到已标记的主（子）接口。
$ docker network create -d ipvlan \
    --subnet=192.168.30.0/24 \
    --gateway=192.168.30.1 \
    -o parent=eth0.30 \
    -o ipvlan_mode=l2 ipvlan30

# 在两个单独的终端中，启动一个 Docker 容器，容器现在可以相互 ping 通。
$ docker run --net=ipvlan30 -it --name ivlan_test3 --rm alpine /bin/sh
$ docker run --net=ipvlan30 -it --name ivlan_test4 --rm alpine /bin/sh
```

网关在容器内部设置为默认网关。该网关通常是网络上的外部路由器。

```console
$$ ip route
  default via 192.168.30.1 dev eth0
  192.168.30.0/24 dev eth0  src 192.168.30.2
```

示例：多子网 IPvlan L2 模式，在同一子网上启动两个容器并相互 ping 通。为了使 `192.168.114.0/24` 能够到达 `192.168.116.0/24`，在 L2 模式下需要一个外部路由器。L3 模式可以在共享相同 `-o parent=` 的子网之间进行路由。

网络路由器上的辅助地址很常见，因为当地址空间耗尽时，会在 L3 VLAN 接口上添加另一个辅助地址，通常称为“交换虚拟接口”（SVI）。

```console
$ docker network create -d ipvlan \
    --subnet=192.168.114.0/24 --subnet=192.168.116.0/24 \
    --gateway=192.168.114.254 --gateway=192.168.116.254 \
    -o parent=eth0.114 \
    -o ipvlan_mode=l2 ipvlan114

$ docker run --net=ipvlan114 --ip=192.168.114.10 -it --rm alpine /bin/sh
$ docker run --net=ipvlan114 --ip=192.168.114.11 -it --rm alpine /bin/sh
```

一个关键的收获是，操作员能够将他们的物理网络映射到虚拟网络中，以便将容器集成到他们的环境中，而无需进行操作上的大修。NetOps 将一个 802.1Q 中继放入 Docker 主机。该虚拟链接将是网络创建时传入的 `-o parent=`。对于未标记（非 VLAN）的链接，就像 `-o parent=eth0` 一样简单，或者对于带有 VLAN ID 的 802.1Q 中继，每个网络都映射到网络中相应的 VLAN/子网。

例如，NetOps 提供 VLAN ID 和通过以太网链接传递到 Docker 主机服务器的 VLAN 的关联子网。这些值在配置 Docker 网络时插入到 `docker network create` 命令中。这些是持久性配置，每次 Docker 引擎启动时都会应用，从而无需管理通常复杂的配置文件。网络接口也可以通过预先创建来手动管理，Docker 网络将永远不会修改它们，并将它们用作父接口。从 NetOps 到 Docker 网络命令的示例映射如下：

- VLAN: 10, Subnet: 172.16.80.0/24, Gateway: 172.16.80.1
  - `--subnet=172.16.80.0/24 --gateway=172.16.80.1 -o parent=eth0.10`
- VLAN: 20, IP subnet: 172.16.50.0/22, Gateway: 172.16.50.1
  - `--subnet=172.16.50.0/22 --gateway=172.16.50.1 -o parent=eth0.20`
- VLAN: 30, Subnet: 10.1.100.0/16, Gateway: 10.1.100.1
  - `--subnet=10.1.100.0/16 --gateway=10.1.100.1 -o parent=eth0.30`

### IPvlan L3 模式示例

IPvlan 需要将路由分发到每个端点。驱动仅构建 IPvlan L3 模式端口并将容器附加到该接口。在整个集群中分发路由超出了这个单主机范围驱动的初始实现。在 L3 模式下，Docker 主机非常类似于在容器中启动新网络的路由器。它们位于上游网络不知道的网络上，除非进行路由分发。对于那些好奇 IPvlan L3 如何适应容器网络的人，请参见以下示例。

![Docker IPvlan L2 模式](images/ipvlan-l3.webp?w=500)

IPvlan L3 模式丢弃所有广播和多播流量。仅此原因就使 IPvlan L3 模式成为那些寻求大规模和可预测网络集成的用户的首选。它是可预测的，因此将带来更高的正常运行时间，因为不涉及桥接。桥接环路一直是导致重大停机的原因，根据故障域的大小，可能很难确定故障点。这是由于 BPDUs（网桥端口数据单元）的级联性质，它们在整个广播域（VLAN）中泛洪以查找并阻止拓扑环路。消除桥接域，或者至少将它们隔离到一对 ToR（架顶式交换机）中，将减少难以排除故障的桥接不稳定性。IPvlan L2 模式非常适合仅中继到一对 ToR 的隔离 VLAN，这些 ToR 可以提供无环路的无阻塞结构。下一步是通过 IPvlan L3 模式在边缘进行路由，这将故障域缩小到仅本地主机。

- L3 模式需要位于与默认命名空间不同的子网中，因为它需要在默认命名空间中有一个指向 IPvlan 父接口的 netlink 路由。
- 本例中使用的父接口是 `eth0`，它位于子网 `192.168.1.0/24` 中。请注意，`docker network` 与 `eth0` 不在同一子网中。
- 与 IPvlan l2 模式不同，只要它们共享相同的父接口 `-o parent=`，不同的子网/网络可以相互 ping 通。

```console
$$ ip a show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:39:45:2e brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

- 传统的网关对于 L3 模式 IPvlan 接口来说意义不大，因为不允许广播流量。因此，容器的默认网关指向容器的 `eth0` 设备。有关详细信息，请参阅 L3 容器内部的 `ip route` 或 `ip -6 route` 的 CLI 输出。

模式 `-o ipvlan_mode=l3` 必须显式指定，因为默认的 IPvlan 模式是 `l2`。

以下示例未指定父接口。网络驱动将为用户创建一个 dummy 类型的链接，而不是拒绝网络创建并将容器仅隔离为彼此通信。

```console
# 创建 IPvlan L3 网络
$ docker network create -d ipvlan \
    --subnet=192.168.214.0/24 \
    --subnet=10.1.214.0/24 \
    -o ipvlan_mode=l3 ipnet210

# 测试 192.168.214.0/24 连接性
$ docker run --net=ipnet210 --ip=192.168.214.10 -itd alpine /bin/sh
$ docker run --net=ipnet210 --ip=10.1.214.10 -itd alpine /bin/sh

# 测试从 10.1.214.0/24 到 192.168.214.0/24 的 L3 连接性
$ docker run --net=ipnet210 --ip=192.168.214.9 -it --rm alpine ping -c 2 10.1.214.10

# 测试从 192.168.214.0/24 到 10.1.214.0/24 的 L3 连接性
$ docker run --net=ipnet210 --ip=10.1.214.9 -it --rm alpine ping -c 2 192.168.214.10

```

> [!NOTE]
>
> 请注意，网络创建中没有 `--gateway=` 选项。如果指定了该字段，在 `l3` 模式下将被忽略。查看容器内部的容器路由表：
>
> ```console
> # 在 L3 模式容器内部
> $$ ip route
>  default dev eth0
>   192.168.214.0/24 dev eth0  src 192.168.214.10
> ```

为了从远程 Docker 主机 ping 容器，或者容器能够 ping 远程主机，远程主机或中间的物理网络需要有一条指向容器 Docker 主机 eth 接口的主机 IP 地址的路由。

### 双栈 IPv4 IPv6 IPvlan L2 模式

- Libnetwork 不仅让您完全控制 IPv4 地址分配，还让您完全控制 IPv6 地址分配，并在两个地址族之间实现功能对等。

- 下一个示例将从仅 IPv6 开始。在同一个 VLAN `139` 上启动两个容器并相互 ping 通。由于未指定 IPv4 子网，默认的 IPAM 将分配一个默认的 IPv4 子网。除非上游网络在 VLAN `139` 上显式路由，否则该子网是隔离的。

```console
# 创建一个 v6 网络
$ docker network create -d ipvlan \
    --ipv6 --subnet=2001:db8:abc2::/64 --gateway=2001:db8:abc2::22 \
    -o parent=eth0.139 v6ipvlan139

# 在网络上启动一个容器
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh
```

查看容器 eth0 接口和 v6 路由表：

```console
# 在 IPv6 容器内部
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.2/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc2::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc2::22 dev eth0  metric 1024
```

启动第二个容器并 ping 第一个容器的 v6 地址。

```console
# 测试 IPv6 上的 L2 连接性
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh

# 在第二个 IPv6 容器内部
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::2/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ping6 2001:db8:abc2::1
PING 2001:db8:abc2::1 (2001:db8:abc2::1): 56 data bytes
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=0 ttl=64 time=0.044 ms
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=1 ttl=64 time=0.058 ms

2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.044/0.051/0.058/0.000 ms
```

下一个示例将设置一个双栈 IPv4/IPv6 网络，VLAN ID 示例为 `140`。

接下来创建一个包含两个 IPv4 子网和一个 IPv6 子网的网络，所有子网都有显式网关：

```console
$ docker network create -d ipvlan \
    --subnet=192.168.140.0/24 --subnet=192.168.142.0/24 \
    --gateway=192.168.140.1 --gateway=192.168.142.1 \
    --subnet=2001:db8:abc9::/64 --gateway=2001:db8:abc9::22 \
    -o parent=eth0.140 \
    -o ipvlan_mode=l2 ipvlan140
```

启动一个容器并查看 eth0 以及 v4 和 v6 路由表：

```console
$ docker run --net=ipvlan140 --ip6=2001:db8:abc2::51 -it --rm alpine /bin/sh

$ ip a show eth0
78: eth0@if77: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.140.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc9::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip route
default via 192.168.140.1 dev eth0
192.168.140.0/24 dev eth0  proto kernel  scope link  src 192.168.140.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc9::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc9::22 dev eth0  metric 1024
```

启动第二个容器，指定特定的 `--ip4` 地址，并使用 IPv4 数据包 ping 第一个主机：

```console
$ docker run --net=ipvlan140 --ip=192.168.140.10 -it --rm alpine /bin/sh
```

> [!NOTE]
>
> 在 IPvlan `L2` 模式下，同一父接口上的不同子网无法相互 ping 通。这需要一个路由器使用辅助子网代理 ARP 请求。然而，只要它们共享相同的 `-o parent` 父链接，IPvlan `L3` 将在不同的子网之间路由单播流量。

### 双栈 IPv4 IPv6 IPvlan L3 模式

示例：IPvlan L3 模式双栈 IPv4/IPv6，多子网带 802.1Q VLAN 标签:118

与所有示例一样，不一定必须使用标记的 VLAN 接口。子接口可以与 `eth0`、`eth1`、`bond0` 或主机上除 `lo` 回环之外的任何其他有效接口互换。

您将看到的主要区别是，L3 模式不创建带有下一跳的默认路由，而是将默认路由指向 `dev eth`，因为根据设计，ARP/广播/多播都被 Linux 过滤。由于父接口本质上充当路由器，因此父接口 IP 和子网需要与容器网络不同。这与网桥和 L2 模式相反，后者需要位于同一子网（广播域）中才能转发广播和多播数据包。

```console
# 创建一个 IPv6+IPv4 双栈 IPvlan L3 网络
# v4 和 v6 的网关都设置为一个设备，例如 'default dev eth0'
$ docker network create -d ipvlan \
    --subnet=192.168.110.0/24 \
    --subnet=192.168.112.0/24 \
    --subnet=2001:db8:abc6::/64 \
    -o parent=eth0 \
    -o ipvlan_mode=l3 ipnet110


# 在网络上启动几个容器 (ipnet110)
# 在单独的终端中并检查连接性
$ docker run --net=ipnet110 -it --rm alpine /bin/sh
# 启动第二个容器，指定 v6 地址
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::10 -it --rm alpine /bin/sh
# 启动第三个容器，指定 IPv4 地址
$ docker run --net=ipnet110 --ip=192.168.112.30 -it --rm alpine /bin/sh
# 启动第四个容器，同时指定 IPv4 和 IPv6 地址
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::50 --ip=192.168.112.50 -it --rm alpine /bin/sh
```

接口和路由表输出如下：

```console
$$ ip a show eth0
63: eth0@if59: <BROADCAST,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.112.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc6::10/64 scope link nodad
       valid_lft forever preferred_lft forever

# 注意默认路由是 eth 设备，因为 ARP 被过滤。
$$ ip route
  default dev eth0  scope link
  192.168.112.0/24 dev eth0  proto kernel  scope link  src 192.168.112.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc6::/64 dev eth0  proto kernel  metric 256
default dev eth0  metric 1024
```

> [!NOTE]
>
> 当您删除一个指定了 v6 地址的容器，然后使用相同的 v6 地址启动一个新容器时，指定 `--ip6=` 地址时可能存在一个错误，它会抛出以下错误，好像地址没有正确释放到 v6 求中。它将无法卸载容器并保持死亡状态。

```console
docker: Error response from daemon: Address already in use.
```

### 手动创建 802.1Q 链接

#### VLAN ID 40

如果用户不希望驱动创建 VLAN 子接口，则需要在运行 `docker network create` 之前存在该子接口。如果您的子接口命名不是 `interface.vlan_id`，只要接口存在且已启动，它就会在 `-o parent=` 选项中再次得到尊重。

手动创建的链接可以命名为任何名称，只要它们在网络创建时存在即可。无论名称如何，手动创建的链接在使用 `docker network rm` 删除网络时都不会被删除。

```console
# 创建一个绑定到 dot1q vlan 40 的新子接口
$ ip link add link eth0 name eth0.40 type vlan id 40

# 启用新的子接口
$ ip link set eth0.40 up

# 现在像往常一样添加网络和主机，附加到已标记的主（子）接口
$ docker network create -d ipvlan \
    --subnet=192.168.40.0/24 \
    --gateway=192.168.40.1 \
    -o parent=eth0.40 ipvlan40

# 在两个单独的终端中，启动一个 Docker 容器，容器现在可以相互 ping 通。
$ docker run --net=ipvlan40 -it --name ivlan