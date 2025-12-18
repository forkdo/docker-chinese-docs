---
title: IPvlan 网络驱动
description:
  关于使用 IPvlan 的全部内容，让你的容器在网络中看起来像物理机器
keywords: network, ipvlan, l2, l3, standalone
aliases:
  - /network/ipvlan/
  - /network/drivers/ipvlan/
---

IPvlan 驱动为用户提供了对 IPv4 和 IPv6 地址的完全控制。VLAN 驱动在此基础上更进一步，为运营商提供了对第 2 层 VLAN 标记的完全控制，甚至为对底层网络集成感兴趣的用户提供了 IPvlan L3 路由。对于需要抽象物理约束的覆盖部署，请参阅 [多主机覆盖](overlay.md) 驱动。

IPvlan 是一种新的网络虚拟化技术，它在传统方法的基础上进行了创新。Linux 实现非常轻量级，因为它们不使用传统的 Linux 网桥进行隔离，而是与 Linux 以太网接口或子接口关联，以强制网络之间的隔离并连接到物理网络。

IPvlan 提供了许多独特的功能，并为各种模式的进一步创新留下了充足的空间。这些方法的两个主要优势是：绕过 Linux 网桥带来的积极性能影响，以及减少活动部件的简单性。移除传统上位于 Docker 主机 NIC 和容器接口之间的网桥，留下了一个简单的设置，由容器接口直接连接到 Docker 主机接口。这使得外部面向服务的访问变得简单，因为这些场景中不需要端口映射。

## 选项

下表描述了在使用 `ipvlan` 驱动创建网络时，可以传递给 `--opt` 的驱动特定选项。

| 选项        | 默认值  | 描述                                                           |
| ------------- | -------- | --------------------------------------------------------------------- |
| `ipvlan_mode` | `l2`     | 设置 IPvlan 操作模式。可以是：`l2`、`l3`、`l3s`      |
| `ipvlan_flag` | `bridge` | 设置 IPvlan 模式标志。可以是：`bridge`、`private`、`vepa` |
| `parent`      |          | 指定要使用的父接口。                                |

## 示例

### 前置条件

- 本页上的所有示例都是单主机的。
- 所有示例都可以在运行 Docker 的单个主机上执行。使用子接口（如 `eth0.10`）的任何示例都可以替换为 `eth0` 或 Docker 主机上的任何其他有效父接口。带 `.` 的子接口会动态创建。`-o parent` 接口也可以完全省略在 `docker network create` 中，驱动将创建一个 `dummy` 接口，使本地主机连接能够执行示例。
- 内核要求：
  - IPvlan Linux 内核 v4.2+（对早期内核的支持存在但有 bug）。要检查当前内核版本，请使用 `uname -r`

### IPvlan L2 模式示例用法

下图显示了 IPvlan `L2` 模式拓扑的一个示例。驱动通过 `-d driver_name` 选项指定。在本例中为 `-d ipvlan`。

![简单 IPvlan L2 模式示例](images/ipvlan_l2_simple.png)

下一个示例中的父接口 `-o parent=eth0` 配置如下：

```console
$ ip addr show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

使用主机接口的网络作为 `docker network create` 中的 `--subnet`。容器将连接到与主机接口相同的网络，该网络通过 `-o parent=` 选项设置。

创建 IPvlan 网络并运行连接到它的容器：

```console
# IPvlan  (-o ipvlan_mode= 如果未指定则默认为 L2 模式)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 db_net

# 在 db_net 网络上启动一个容器
$ docker run --net=db_net -it --rm alpine /bin/sh

# 注意：容器无法 ping 通底层主机接口，因为它们被 Linux 故意过滤以提供额外的隔离。
```

IPvlan 的默认模式是 `l2`。如果未指定 `-o ipvlan_mode=`，将使用默认模式。同样，如果 `--gateway` 为空，网关将设置为网络上的第一个可用地址。例如，如果在 network create 中提供的子网是 `--subnet=192.168.1.0/24`，那么容器接收的网关是 `192.168.1.1`。

为了帮助理解这种模式如何与其他主机交互，下图显示了两个 Docker 主机之间的相同第 2 层段，这适用于 IPvlan L2 模式。

![多个 IPvlan 主机](images/macvlan-bridge-ipvlan-l2.webp?w=700)

以下将创建与之前创建的网络 `db_net` 完全相同的网络，使用驱动默认值 `--gateway=192.168.1.1` 和 `-o ipvlan_mode=l2`。

```console
# IPvlan  (-o ipvlan_mode= 如果未指定则默认为 L2 模式)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    -o parent=eth0 db_net_ipv

# 以显式名称在守护进程模式下启动一个容器
$ docker run --net=db_net_ipv --name=ipv1 -itd alpine /bin/sh

# 启动第二个容器并使用容器名称 ping 以查看 Docker 包含的名称解析功能
$ docker run --net=db_net_ipv --name=ipv2 -it --rm alpine /bin/sh
$ ping -c 4 ipv1

# 注意：容器无法 ping 通底层主机接口，因为它们被 Linux 故意过滤以提供额外的隔离。
```

驱动还支持 `--internal` 标志，这将完全隔离网络上的容器，使其无法与该网络外部的任何通信进行通信。由于网络隔离与网络的父接口紧密耦合，因此在 `docker network create` 中省略 `-o parent=` 选项的结果与 `--internal` 选项完全相同。如果未指定父接口或使用 `--internal` 标志，将为用户创建一个 netlink 类型 `dummy` 父接口并用作父接口，从而完全隔离网络。

以下两个 `docker network create` 示例创建了相同的网络，你可以将容器连接到这些网络：

```console
# 空的 '-o parent=' 创建一个隔离的网络
$ docker network create -d ipvlan \
    --subnet=192.168.10.0/24 isolated1

# 显式的 '--internal' 标志是相同的：
$ docker network create -d ipvlan \
    --subnet=192.168.11.0/24 --internal isolated2

# 甚至可以省略 '--subnet='，将分配默认的 IPAM 子网 172.18.0.0/16
$ docker network create -d ipvlan isolated3

$ docker run --net=isolated1 --name=cid1 -it --rm alpine /bin/sh
$ docker run --net=isolated2 --name=cid2 -it --rm alpine /bin/sh
$ docker run --net=isolated3 --name=cid3 -it --rm alpine /bin/sh

# 要附加到任何网络，请使用 `docker exec` 并启动一个 shell
$ docker exec -it cid1 /bin/sh
$ docker exec -it cid2 /bin/sh
$ docker exec -it cid3 /bin/sh
```

### IPvlan 802.1Q 中继 L2 模式示例用法

在架构上，IPvlan L2 模式中继与 Macvlan 在网关和 L2 路径隔离方面是相同的。有一些细微差别可能对 ToR 交换机的 CAM 表压力、主机父 NIC 上的 MAC 耗尽等场景有利。802.1Q 中继场景看起来是一样的。两种模式都遵循标记标准，并与物理网络无缝集成，用于底层集成和硬件供应商插件集成。

同一 VLAN 上的主机通常在同一子网上，并且几乎总是基于其安全策略分组在一起。在大多数场景中，多层应用程序根据每个进程的安全配置文件分层到不同的子网，因为需要某种形式的隔离。例如，在与前端 Web 服务器相同的虚拟网络上托管你的信用卡处理将是一个监管合规问题，同时还绕过了长期存在的纵深防御架构最佳实践。VLAN 或等效的 VNI（虚拟网络标识符）在使用覆盖驱动时，是隔离租户流量的第一步。

![Docker VLAN 深入解析](images/vlans-deeper-look.webp)

Linux 子接口用 VLAN 标记，要么已经存在，要么在调用 `docker network create` 时创建。`docker network rm` 将删除 VLAN 子接口。父接口如 `eth0` 不会被删除，只有 netlink 父索引 > 0 的子接口会被删除。

为了让驱动添加/删除 VLAN 子接口，格式需要是 `interface_name.vlan_tag`。其他子接口命名可以用作指定的父接口，但当你调用 `docker network rm` 时，链接不会自动删除。

驱动管理 VLAN 父子接口或让用户完全管理它们的选项，使用户能够完全管理 Linux 接口和网络，或者让 Docker 创建和删除 VLAN 父子接口（netlink `ip link`），无需用户费力。

例如：使用 `eth0.10` 表示 `eth0` 的子接口，用 VLAN id `10` 标记。等效的 `ip link` 命令将是 `ip link add link eth0 name eth0.10 type vlan id 10`。

示例创建 VLAN 标记的网络，然后启动两个容器测试容器之间的连通性。不同的 VLAN 无法相互 ping 通，除非有路由器在两个网络之间路由。根据 IPvlan 设计，默认命名空间无法访问，以隔离容器命名空间与底层主机。

#### VLAN ID 20

在第一个网络中，Docker 主机用 `eth0.20` 标记和隔离，`eth0.20` 是父接口，用 VLAN id `20` 标记，通过 `-o parent=eth0.20` 指定。可以使用其他命名格式，但链接需要手动使用 `ip link` 或 Linux 配置文件添加和删除。只要 `-o parent` 存在，任何符合 Linux netlink 标准的内容都可以使用。

```console
# 现在添加网络和主机，通过附加到标记的主（子）接口来正常工作
$ docker network create -d ipvlan \
    --subnet=192.168.20.0/24 \
    --gateway=192.168.20.1 \
    -o parent=eth0.20 ipvlan20

# 在两个独立的终端中，启动一个 Docker 容器，容器现在可以相互 ping 通。
$ docker run --net=ipvlan20 -it --name ivlan_test1 --rm alpine /bin/sh
$ docker run --net=ipvlan20 -it --name ivlan_test2 --rm alpine /bin/sh
```

#### VLAN ID 30

在第二个网络中，Docker 主机用 `eth0.30` 标记和隔离，`eth0.30` 是父接口，用 VLAN id `30` 标记，通过 `-o parent=eth0.30` 指定。`ipvlan_mode=` 默认为 l2 模式 `ipvlan_mode=l2`。也可以显式设置，结果相同，如下一个示例所示。

```console
# 现在添加网络和主机，通过附加到标记的主（子）接口来正常工作。
$ docker network create -d ipvlan \
    --subnet=192.168.30.0/24 \
    --gateway=192.168.30.1 \
    -o parent=eth0.30 \
    -o ipvlan_mode=l2 ipvlan30

# 在两个独立的终端中，启动一个 Docker 容器，容器现在可以相互 ping 通。
$ docker run --net=ipvlan30 -it --name ivlan_test3 --rm alpine /bin/sh
$ docker run --net=ipvlan30 -it --name ivlan_test4 --rm alpine /bin/sh
```

网关在容器内部设置为默认网关。该网关通常是网络上的外部路由器。

```console
$$ ip route
  default via 192.168.30.1 dev eth0
  192.168.30.0/24 dev eth0  src 192.168.30.2
```

示例：多子网 IPvlan L2 模式启动两个容器在同一子网上并相互 ping 通。为了让 `192.168.114.0/24` 到达 `192.168.116.0/24`，在 L2 模式下需要外部路由器。L3 模式可以在共享公共 `-o parent=` 的子网之间路由。

网络路由器上的辅助地址在地址空间耗尽时很常见，以在 L3 VLAN 接口上添加另一个辅助地址，通常称为“交换虚拟接口”（SVI）。

```console
$ docker network create -d ipvlan \
    --subnet=192.168.114.0/24 --subnet=192.168.116.0/24 \
    --gateway=192.168.114.254 --gateway=192.168.116.254 \
    -o parent=eth0.114 \
    -o ipvlan_mode=l2 ipvlan114

$ docker run --net=ipvlan114 --ip=192.168.114.10 -it --rm alpine /bin/sh
$ docker run --net=ipvlan114 --ip=192.168.114.11 -it --rm alpine /bin/sh
```

一个关键要点是，运营商有能力将他们的物理网络映射到他们的虚拟网络中，以便将容器集成到他们的环境中，无需进行任何操作上的大修。NetOps 将 802.1Q 中继线连接到 Docker 主机。该虚拟链路将作为网络创建时传入的 `-o parent=`。对于未标记（非 VLAN）链路，就像 `-o parent=eth0` 一样简单，或者对于 802.1Q 中继线与 VLAN ID，每个网络都映射到从网络传递到 Docker 主机服务器的以太网链路上的相应 VLAN/子网。

一个示例是，NetOps 提供 VLAN ID 和关联的子网，用于传递到 Docker 主机服务器的以太网链路上的 VLAN。这些值被插入到 `docker network create` 命令中，用于配置 Docker 网络。这些是持久性配置，每次 Docker 引擎启动时都会应用，这消除了管理复杂配置文件的需要。网络接口也可以通过手动预创建来管理，Docker 网络将永远不会修改它们，并将它们用作父接口。NetOps 到 Docker 网络命令的映射示例如下：

- VLAN: 10, 子网: 172.16.80.0/24, 网关: 172.16.80.1
  - `--subnet=172.16.80.0/24 --gateway=172.16.80.1 -o parent=eth0.10`
- VLAN: 20, IP 子网: 172.16.50.0/22, 网关: 172.16.50.1
  - `--subnet=172.16.50.0/22 --gateway=172.16.50.1 -o parent=eth0.20`
- VLAN: 30, 子网: 10.1.100.0/16, 网关: 10.1.100.1
  - `--subnet=10.1.100.0/16 --gateway=10.1.100.1 -o parent=eth0.30`

### IPvlan L3 模式示例

IPvlan 将需要将路由分发到每个端点。驱动仅构建 IPvlan L3 模式端口并将容器连接到接口。在整个集群中分发路由超出了这个单主机范围驱动的初始实现。在 L3 模式下，Docker 主机非常类似于启动容器中新网络的路由器。它们位于上游网络不知道的网络上，除非分发路由。对于那些好奇 IPvlan L3 如何适应容器网络的人，请参阅以下示例。

![Docker IPvlan L2 模式](images/ipvlan-l3.webp?w=500)

IPvlan L3 模式丢弃所有广播和多播流量。仅此原因就使 IPvlan L3 模式成为那些寻求大规模和可预测网络集成的人的绝佳候选者。它是可预测的，反过来将导致更大的正常运行时间，因为没有涉及桥接。桥接环路一直是高调中断的原因，这些中断可能难以定位，具体取决于故障域的大小。这是由于 BPDU（桥接端口数据单元