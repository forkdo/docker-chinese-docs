---
title: 网络概述
linkTitle: 网络
weight: 30
description: 从容器的角度了解网络的工作原理
keywords: 网络, 容器, 独立, IP 地址, DNS 解析
aliases:
- /articles/networking/
- /config/containers/container-networking/
- /engine/tutorials/networkingcontainers/
- /engine/userguide/networking/
- /engine/userguide/networking/configure-dns/
- /engine/userguide/networking/default_network/binding/
- /engine/userguide/networking/default_network/configure-dns/
- /engine/userguide/networking/default_network/container-communication/
- /engine/userguide/networking/dockernetworks/
- /network/
---

容器网络指的是容器相互连接和通信，以及与非 Docker 网络服务通信的能力。

容器默认启用网络，并且可以进行出站连接。容器对其所连接的网络类型或其网络对等体是否也是 Docker 容器一无所知。容器只看到一个具有 IP 地址、网关、路由表、DNS 服务和其他网络详细信息的网络接口。

本文档从容器的角度描述网络，以及容器网络相关的概念。

Linux 上的 Docker Engine 首次启动时，它有一个内置的单个网络，称为“默认桥接”网络。当你运行容器时未使用 `--network` 选项，它将连接到默认桥接网络。

连接到默认桥接网络的容器可以访问 Docker 主机外部的网络服务。它们使用“伪装”技术，这意味着如果 Docker 主机有 Internet 访问权限，容器无需额外配置即可访问 Internet。

例如，要在默认桥接网络上运行一个容器并让它 ping 一个 Internet 主机：

```console
$ docker run --rm -ti busybox ping -c1 docker.com
PING docker.com (23.185.0.4): 56 data bytes
64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms

--- docker.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 6.564/6.564/6.564 ms
```

## 用户定义的网络

默认配置下，连接到默认桥接网络的容器可以使用容器 IP 地址相互访问，但无法通过名称相互引用。

将应该完全访问彼此的容器组分离，但限制对其他组容器的访问可能很有用。

你可以创建自定义的用户定义网络，并将容器组连接到同一网络。一旦连接到用户定义的网络，容器可以使用容器 IP 地址或容器名称相互通信。

以下示例使用 `bridge` 网络驱动程序创建一个网络，并在该网络中运行一个容器：

```console
$ docker network create -d bridge my-net
$ docker run --network=my-net -it busybox
```

### 驱动程序

Docker Engine 有许多网络驱动程序，以及默认的“桥接”驱动程序。在 Linux 上，以下内置网络驱动程序可用：

| 驱动程序                          | 描述                                                         |
|:--------------------------------|:-------------------------------------------------------------|
| [bridge](./drivers/bridge.md)   | 默认网络驱动程序。                                           |
| [host](./drivers/host.md)       | 移除容器和 Docker 主机之间的网络隔离。                       |
| [none](./drivers/none.md)       | 完全隔离容器与主机和其他容器。                               |
| [overlay](./drivers/overlay.md) | Swarm 覆盖网络将多个 Docker 守护进程连接在一起。             |
| [ipvlan](./drivers/ipvlan.md)   | 将容器连接到外部 VLAN。                                      |
| [macvlan](./drivers/macvlan.md) | 容器在主机网络上显示为设备。                                 |

更多信息可以在特定的网络驱动程序页面中找到，包括它们的配置选项和功能详细信息。

原生 Windows 容器有不同的驱动程序集，参见 [Windows 容器网络驱动程序](https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/network-drivers-topologies)。

### 连接到多个网络

将容器连接到网络可以类比为将网线连接到物理主机。就像主机可以连接到多个以太网网络一样，容器也可以连接到多个 Docker 网络。

例如，前端容器可以连接到具有外部访问权限的桥接网络，以及一个 [`--internal`](/reference/cli/docker/network/create/#internal) 网络，与运行不需要外部网络访问的后端服务的容器通信。

容器也可以连接到不同类型的网络。例如，一个 `ipvlan` 网络提供 Internet 访问，一个 `bridge` 网络用于访问本地服务。

容器也可以共享网络栈，参见 [容器网络](#container-networks)。

发送数据包时，如果目标是直接连接网络中的地址，数据包将被发送到该网络。否则，数据包将被发送到默认网关，路由到其目的地。在上面的例子中，`ipvlan` 网络的网关必须是默认网关。

默认网关由 Docker 选择，当容器的网络连接改变时可能会改变。要在创建容器或连接新网络时让 Docker 选择特定的默认网关，请设置网关优先级。参见 `docker run` 和 `docker network connect` 命令的 `gw-priority` 选项。

默认的 `gw-priority` 是 `0`，具有最高优先级的网络的网关是默认网关。因此，当网络应该始终是默认网关时，只需将其 `gw-priority` 设置为 `1` 即可。

```console
$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr
```

## 发布的端口

当你使用 `docker create` 或 `docker run` 创建或运行容器时，桥接网络上所有容器的端口都可以从 Docker 主机和连接到同一网络的其他容器访问。从主机外部或其他桥接网络中的容器（默认配置下）无法访问这些端口。

使用 `--publish` 或 `-p` 标志使端口在主机外部和连接到其他桥接网络的容器中可用。

有关端口映射的更多信息，包括如何禁用它并使用直接路由到容器，参见 [端口发布](./port-publishing.md)。

## IP 地址和主机名

创建网络时，默认启用 IPv4 地址分配，可以使用 `--ipv4=false` 禁用。可以使用 `--ipv6` 启用 IPv6 地址分配。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

默认情况下，容器连接到的每个 Docker 网络都会为其分配一个 IP 地址。容器从网络的 IP 子网中获取 IP 地址。Docker 守护进程为容器执行动态子网和 IP 地址分配。每个网络也有默认的子网掩码和网关。

你可以将正在运行的容器连接到多个网络，要么在创建容器时多次传递 `--network` 标志，要么对已运行的容器使用 `docker network connect` 命令。在这两种情况下，你都可以使用 `--ip` 或 `--ip6` 标志指定容器在特定网络上的 IP 地址。

同样，容器的主机名默认为 Docker 中的容器 ID。你可以使用 `--hostname` 覆盖主机名。当使用 `docker network connect` 连接到现有网络时，你可以使用 `--alias` 标志为容器在该网络上指定额外的网络别名。

### 子网分配

Docker 网络可以使用显式配置的子网或从默认池自动分配的子网。

#### 显式子网配置

你可以在创建网络时指定确切的子网：

```console
$ docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet
```

#### 自动子网分配

当未提供 `--subnet` 选项时，Docker 从预定义的“默认地址池”中自动选择子网。这些池可以在 `/etc/docker/daemon.json` 中配置。Docker 的内置默认值等同于：

```json
{
  "default-address-pools": [
    {"base":"172.17.0.0/16","size":16},
    {"base":"172.18.0.0/16","size":16},
    {"base":"172.19.0.0/16","size":16},
    {"base":"172.20.0.0/14","size":16},
    {"base":"172.24.0.0/14","size":16},
    {"base":"172.28.0.0/14","size":16},
    {"base":"192.168.0.0/16","size":20}
  ]
}
```

- `base`: 可以分配的子网。
- `size`: 用于每个分配子网的前缀长度。

当需要 IPv6 子网且 `default-address-pools` 中没有 IPv6 地址时，Docker 从唯一本地地址 (ULA) 前缀分配子网。要使用特定的 IPv6 子网，请将它们添加到你的 `default-address-pools` 中。更多信息参见 [动态 IPv6 子网分配](../daemon/ipv6.md#dynamic-ipv6-subnet-allocation)。

Docker 尝试避免使用主机上已使用的地址前缀。但是，在某些网络环境中，你可能需要自定义 `default-address-pools` 以防止路由冲突。

默认池使用大型子网，这限制了你可以创建的网络数量。你可以将基础子网划分为更小的池以支持更多网络。

例如，此配置允许 Docker 从 `172.17.0.0/16` 创建 256 个网络。Docker 将分配子网 `172.17.0.0/24`、`172.17.1.0/24` 等，直到 `172.17.255.0/24`：

```json
{
  "default-address-pools": [
    {"base": "172.17.0.0/16", "size": 24}
  ]
}
```

你也可以通过在 `--subnet` 选项中使用未指定的地址，从默认池请求具有特定前缀长度的子网：

```console
$ docker network create --ipv6 --subnet ::/56 --subnet 0.0.0.0/24 mynet
6686a6746b17228f5052528113ddad0e6d68e2e3905d648e336b33409f2d3b64
$ docker network inspect mynet -f '{{json .IPAM.Config}}' | jq .
[
  {
    "Subnet": "172.19.0.0/24",
    "Gateway": "172.19.0.1"
  },
  {
    "Subnet": "fdd3:6f80:972c::/56",
    "Gateway": "fdd3:6f80:972c::1"
  }
]
```

> [!NOTE]
>
> 在 Docker 29.0.0 中引入了对 `--subnet` 中未指定地址的支持。如果 Docker 降级到较旧版本，以这种方式创建的网络将无法使用。它们可以被删除并重新创建，或者如果守护进程恢复到 29.0.0 或更高版本，它们将再次正常工作。

## DNS 服务

默认情况下，容器使用与主机相同的 DNS 服务器，但你可以使用 `--dns` 覆盖此设置。

默认情况下，容器继承在 `/etc/resolv.conf` 配置文件中定义的 DNS 设置。连接到默认 `bridge` 网络的容器接收此文件的副本。连接到 [自定义网络](drivers/bridge.md#use-user-defined-bridge-networks) 的容器使用 Docker 的嵌入式 DNS 服务器。嵌入式 DNS 服务器将外部 DNS 查找转发到主机上配置的 DNS 服务器。

你可以使用 `docker run` 或 `docker create` 命令的标志为每个容器配置 DNS 解析，这些标志用于启动容器。下表描述了与 DNS 配置相关的可用 `docker run` 标志。

| 标志           | 描述                                                                                                                                                                                                                                           |
| -------------- |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--dns`        | DNS 服务器的 IP 地址。要指定多个 DNS 服务器，请使用多个 `--dns` 标志。DNS 请求将从容器的网络命名空间转发，因此，例如，`--dns=127.0.0.1` 指的是容器自己的环回地址。                                                                               |
| `--dns-search` | 搜索非完全限定主机名的 DNS 搜索域。要指定多个 DNS 搜索前缀，请使用多个 `--dns-search` 标志。                                                                                                                                                   |
| `--dns-opt`    | 表示 DNS 选项及其值的键值对。参见操作系统 `resolv.conf` 文档中的有效选项。                                                                                                                                                                     |
| `--hostname`   | 容器用于自身的主机名。如果未指定，默认为主机的容器 ID。                                                                                                                                                                                        |

### 自定义主机

你的容器在 `/etc/hosts` 中会有行定义容器自身的主机名，以及 `localhost` 和其他一些常见内容。主机机器上 `/etc/hosts` 中定义的自定义主机不会被容器继承。要将额外的主机传递到容器中，请参见 `docker run` 参考文档中的 [将条目添加到容器 hosts 文件](/reference/cli/docker/container/run.md#add-host)。

## 容器网络

除了用户定义的网络外，你还可以直接将容器连接到另一个容器的网络栈，使用 `--network container:<name|id>` 标志格式。

使用 `container:` 网络模式的容器不支持以下标志：

- `--add-host`
- `--hostname`
- `--dns`
- `--dns-search`
- `--dns-option`
- `--mac-address`
- `--publish`
- `--publish-all`
- `--expose`

以下示例运行一个 Redis 容器，Redis 绑定到 127.0.0.1，然后运行 `redis-cli` 命令并通过 127.0.0.1 连接到 Redis 服务器。

```console
$ docker run -d --name redis redis --bind 127.0.0.1
$ docker run --rm -it --network container:redis redis redis-cli -h 127.0.0.1
```