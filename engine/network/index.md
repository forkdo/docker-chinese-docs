# 网络概述

容器网络是指容器之间以及容器与非 Docker 网络服务进行连接和通信的能力。

容器默认启用网络功能，并且可以发起出站连接。容器不知道其连接的网络类型，也不知道其网络对等方是否也是 Docker 容器。容器仅能看到一个具有 IP 地址、网关、路由表、DNS 服务和其他网络详细信息的网络接口。

本文从容器的角度描述网络以及容器网络相关的概念。

当 Linux 上的 Docker Engine 首次启动时，它有一个名为 "default bridge" 的内置网络。当您在不使用 `--network` 选项的情况下运行容器时，它会连接到默认桥接网络。

连接到默认桥接网络的容器可以访问 Docker 主机外部的网络服务。它们使用 "伪装"（masquerading）技术，这意味着，如果 Docker 主机可以访问互联网，则容器无需额外配置即可访问互联网。

例如，在默认桥接网络上运行一个容器，并让它 ping 一个互联网主机：

```console
$ docker run --rm -ti busybox ping -c1 docker.com
PING docker.com (23.185.0.4): 56 data bytes
64 bytes from 23.185.0.4: seq=0 ttl=62 time=6.564 ms

--- docker.com ping statistics ---
1 packets transmitted, 1 packets received, 0% packet loss
round-trip min/avg/max = 6.564/6.564/6.564 ms
```

## 用户定义的网络

在默认配置下，连接到默认桥接网络的容器可以使用容器 IP 地址无限制地访问彼此。它们无法通过名称相互引用。

将应该完全互访但又需要限制访问其他组容器的容器组进行分离是很有用的。

您可以创建自定义的用户定义网络，并将容器组连接到同一网络。一旦连接到用户定义网络，容器就可以使用容器 IP 地址或容器名称进行通信。

以下示例使用 `bridge` 网络驱动程序创建一个网络，并在该网络中运行一个容器：

```console
$ docker network create -d bridge my-net
$ docker run --network=my-net -it busybox
```

### 驱动程序

Docker Engine 除了默认的 "bridge" 外，还有许多网络驱动程序。在 Linux 上，以下内置网络驱动程序可用：

| 驱动程序                          | 描述                                                         |
|:--------------------------------|:--------------------------------------------------------------------|
| [bridge](./drivers/bridge.md)   | 默认网络驱动程序。                                         |
| [host](./drivers/host.md)       | 移除容器与 Docker 主机之间的网络隔离。 |
| [none](./drivers/none.md)       | 完全将容器与主机和其他容器隔离。  |
| [overlay](./drivers/overlay.md) | Swarm 覆盖网络将多个 Docker 守护进程连接在一起。    |
| [ipvlan](./drivers/ipvlan.md)   | 将容器连接到外部 VLAN。                               |
| [macvlan](./drivers/macvlan.md) | 容器作为设备出现在主机的网络上。                 |

更多信息可以在特定的网络驱动程序页面中找到，包括其配置选项和功能详情。

原生 Windows 容器有一组不同的驱动程序，请参阅 [Windows 容器网络驱动程序](https://learn.microsoft.com/en-us/virtualization/windowscontainers/container-networking/network-drivers-topologies)。

### 连接到多个网络

将容器连接到网络可以比作将以太网电缆连接到物理主机。正如主机可以连接到多个以太网网络一样，容器也可以连接到多个 Docker 网络。

例如，一个前端容器可能连接到一个具有外部访问权限的桥接网络，以及一个
[`--internal`](/reference/cli/docker/network/create/#internal) 网络，用于与不需要外部网络访问的后端服务容器进行通信。

容器也可以连接到不同类型的网络。例如，一个 `ipvlan` 网络用于提供互联网访问，而一个 `bridge` 网络用于访问本地服务。

容器也可以共享网络堆栈，请参阅 [容器网络](#container-networks)。

发送数据包时，如果目的地是直接连接网络中的地址，则数据包会发送到该网络。否则，数据包会发送到默认网关以路由到其目的地。在上面的示例中，`ipvlan` 网络的网关必须是默认网关。

默认网关由 Docker 选择，并且可能在容器的网络连接发生变化时改变。
要在创建容器或连接新网络时让 Docker 选择特定的默认网关，请设置网关优先级。请参阅 [`docker run`](/reference/cli/docker/container/run.md) 和
[`docker network connect`](/reference/cli/docker/network/connect.md) 命令的 `gw-priority` 选项。

默认的 `gw-priority` 为 `0`，具有最高优先级的网络中的网关是默认网关。因此，当一个网络应该始终是默认网关时，只需将其 `gw-priority` 设置为 `1` 即可。

```console
$ docker run --network name=gwnet,gw-priority=1 --network anet1 --name myctr myimage
$ docker network connect anet2 myctr
```

## 发布的端口

当您使用 `docker create` 或 `docker run` 创建或运行容器时，桥接网络上容器的所有端口都可以从 Docker 主机和连接到同一网络的其他容器访问。端口无法从主机外部访问，或者在默认配置下，无法从其他网络中的容器访问。

使用 `--publish` 或 `-p` 标志使端口在主机外部可用，并可供其他桥接网络中的容器使用。

有关端口映射的更多信息，包括如何禁用它并使用直接路由到容器，请参阅
[端口发布](./port-publishing.md)。

## IP 地址和主机名

创建网络时，默认启用 IPv4 地址分配，可以使用 `--ipv4=false` 禁用。可以使用 `--ipv6` 启用 IPv6 地址分配。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

默认情况下，容器会为其连接的每个 Docker 网络获取一个 IP 地址。
容器从网络的 IP 子网接收一个 IP 地址。
Docker 守护进程为容器执行动态子网划分和 IP 地址分配。每个网络还具有默认的子网掩码和网关。

您可以将正在运行的容器连接到多个网络，可以在创建容器时多次传递 `--network` 标志，或者使用 `docker network connect` 命令连接已运行的容器。
在这两种情况下，您都可以使用 `--ip` 或 `--ip6` 标志来指定容器在该特定网络上的 IP 地址。

同样，容器的主机名在 Docker 中默认为容器的 ID。您可以使用 `--hostname` 覆盖主机名。
使用 `docker network connect` 连接到现有网络时，可以使用 `--alias` 标志为容器在该网络上指定额外的网络别名。

### 子网分配

Docker 网络可以使用显式配置的子网，也可以使用从默认池自动分配的子网。

#### 显式子网配置

您可以在创建网络时指定确切的子网：

```console
$ docker network create --ipv6 --subnet 192.0.2.0/24 --subnet 2001:db8::/64 mynet
```

#### 自动子网分配

当未提供 `--subnet` 选项时，Docker 会自动从预定义的 "默认地址池" 中选择一个子网。
这些池可以在 `/etc/docker/daemon.json` 中配置。Docker 的内置默认值等同于：

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

- `base`: 可以从中分配的子网。
- `size`: 用于每个分配的子网的前缀长度。

当需要 IPv6 子网且 `default-address-pools` 中没有 IPv6 地址时，Docker 会从唯一本地地址 (ULA) 前缀分配子网。要改用特定的 IPv6 子网，请将它们添加到您的
`default-address-pools` 中。有关更多信息，请参阅 [动态 IPv6 子网分配](../daemon/ipv6.md#dynamic-ipv6-subnet-allocation)。

Docker 会尝试避免使用主机上已在使用的地址前缀。但是，在某些网络环境中，您可能需要自定义
`default-address-pools` 以防止路由冲突。

默认池使用大型子网，这限制了您可以创建的网络数量。您可以将基础子网划分为更小的池以支持更多网络。

例如，此配置允许 Docker 从 `172.17.0.0/16` 创建 256 个网络。
Docker 将分配子网 `172.17.0.0/24`、`172.17.1.0/24`，依此类推，直到 `172.17.255.0/24`：

```json
{
  "default-address-pools": [
    {"base": "172.17.0.0/16", "size": 24}
  ]
}
```

您还可以通过在 `--subnet` 选项中使用未指定的地址来从默认池请求具有特定前缀长度的子网：

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
> 对 `--subnet` 中未指定地址的支持是在 Docker 29.0.0 中引入的。
> 如果将 Docker 降级到旧版本，以这种方式创建的网络将变得不可用。
> 它们可以被删除并重新创建，或者如果守护进程恢复到 29.0.0 或更高版本，它们将再次发挥作用。

## DNS 服务

容器默认使用与主机相同的 DNS 服务器，但您可以使用 `--dns` 覆盖此设置。

默认情况下，容器继承 `/etc/resolv.conf` 配置文件中定义的 DNS 设置。
连接到默认 `bridge` 网络的容器会接收此文件的副本。
连接到
[自定义网络](drivers/bridge.md#use-user-defined-bridge-networks) 的容器使用 Docker 的嵌入式 DNS 服务器。
嵌入式 DNS 服务器将外部 DNS 查找转发到主机上配置的 DNS 服务器。

您可以使用用于启动容器的 `docker run` 或 `docker create` 命令的标志，在每个容器的基础上配置 DNS 解析。
下表描述了与 DNS 配置相关的可用 `docker run` 标志。

| 标志           | 描述                                                                                                                                                                                                                                           |
| -------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--dns`        | DNS 服务器的 IP 地址。要指定多个 DNS 服务器，请使用多个 `--dns` 标志。DNS 请求将从容器的网络命名空间转发，因此，例如 `--dns=127.0.0.1` 指的是容器自己的环回地址。 |
| `--dns-search` | 用于搜索非完全限定主机名的 DNS 搜索域。要指定多个 DNS 搜索前缀，请使用多个 `--dns-search` 标志。                                                                                                              |
| `--dns-opt`    | 表示 DNS 选项及其值的键值对。有关有效选项，请参阅操作系统的 `resolv.conf` 文档。                                                                                                              |
| `--hostname`   | 容器自身使用的主机名。如果未指定，则默认为容器的 ID。                                                                                                                                                            |

### 自定义主机

您的容器在 `/etc/hosts` 中会有定义容器自身主机名以及 `localhost` 和一些其他常见内容的行。主机上 `/etc/hosts` 中定义的自定义主机不会被容器继承。
要将额外的主机传递到容器中，请参阅 `docker run` 参考文档中的 [向容器 hosts 文件添加条目](/reference/cli/docker/container/run.md#add-host)。

## 容器网络

除了用户定义的网络，您还可以使用 `--network container:<name|id>` 标志格式将容器直接附加到另一个容器的网络堆栈。

对于使用 `container:` 网络模式的容器，不支持以下标志：

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

- [Docker 与 iptables](/engine/network/firewall-iptables/)

- [Docker 与 nftables](/engine/network/firewall-nftables/)

- [数据包过滤与防火墙](/engine/network/packet-filtering-firewalls/)

- [端口发布与映射](/engine/network/port-publishing/)

- [网络驱动](/engine/network/drivers/)

- [在 Docker 中使用 CA 证书](/engine/network/ca-certs/)

- [旧版容器链接](/engine/network/links/)

