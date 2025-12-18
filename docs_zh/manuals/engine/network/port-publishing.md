---
title: 端口发布与映射
weight: 10
description: 访问容器端口
keywords: 网络, iptables, 防火墙
---

默认情况下，对于 IPv4 和 IPv6，Docker 守护进程会阻止对未发布端口的访问。发布的容器端口会被映射到主机 IP 地址。为实现这一点，它使用防火墙规则执行网络地址转换（NAT）、端口地址转换（PAT）和伪装（masquerading）。

例如，`docker run -p 8080:80 [...]` 在 Docker 主机上任意地址的 8080 端口与容器的 80 端口之间创建映射。来自容器的出站连接将进行伪装，使用 Docker 主机的 IP 地址。

## 发布端口

当你使用 `docker create` 或 `docker run` 创建或运行容器时，桥接网络上的所有容器端口都可从 Docker 主机和其他连接到同一网络的容器访问。但默认配置下，这些端口无法从主机外部访问，也无法从其他网络中的容器访问。

使用 `--publish` 或 `-p` 标志可使端口在主机外部以及连接到其他桥接网络的容器中可用。

这会在主机中创建一条防火墙规则，将容器端口映射到 Docker 主机的端口，从而暴露给外部世界。以下是一些示例：

| 标志值                      | 说明                                                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | 将 Docker 主机的 8080 端口映射到容器的 TCP 80 端口。                                                                                   |
| `-p 192.168.1.100:8080:80`      | 将 Docker 主机 IP `192.168.1.100` 的 8080 端口映射到容器的 TCP 80 端口。                                                                |
| `-p 8080:80/udp`                | 将 Docker 主机的 8080 端口映射到容器的 UDP 80 端口。                                                                                   |
| `-p 8080:80/tcp -p 8080:80/udp` | 将 Docker 主机的 TCP 8080 端口映射到容器的 TCP 80 端口，并将 Docker 主机的 UDP 8080 端口映射到容器的 UDP 80 端口。 |

> [!IMPORTANT]
>
> 默认情况下，发布容器端口是不安全的。这意味着，当你发布容器端口时，它不仅对 Docker 主机可用，也对主机外部网络可用。
>
> 如果在发布标志中包含本地回环 IP 地址（`127.0.0.1` 或 `::1`），则只有 Docker 主机可以访问发布的容器端口。
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```
>
> > [!WARNING]
> >
> > 在 28.0.0 之前的版本中，同一 L2 网段（例如，连接到同一网络交换机的主机）中的主机可以访问发布到本地回环的端口。更多信息请参阅
> > [moby/moby#45610](https://github.com/moby/moby/issues/45610)

如果端口映射中未指定主机 IP，桥接网络仅支持 IPv4，且 `--userland-proxy=true`（默认值），则主机 IPv6 地址上的端口将映射到容器的 IPv4 地址。

## 直接路由

端口映射确保发布的端口在主机的网络地址上可访问，这些地址对外部客户端来说通常是可路由的。主机网络通常不会为容器地址设置路由，因为这些地址存在于主机内部。

但是，特别是对于 IPv6，你可能更倾向于避免使用 NAT，而是安排外部路由直接访问容器地址（“直接路由”）。

要从 Docker 主机外部访问桥接网络中的容器，你必须首先设置从外部到桥接网络的路由，通过 Docker 守护进程主机上的地址。这可以通过静态路由、边界网关协议（BGP）或任何适合你网络的其他方式实现。例如，在本地二层网络中，远程主机可以设置静态路由，通过 Docker 守护进程主机在本地网络上的地址访问容器网络。

### 桥接网络中容器的直接路由

默认情况下，远程主机无法直接访问 Docker Linux 桥接网络中的容器 IP 地址。它们只能访问发布到主机 IP 地址的端口。

要允许从任何位置直接访问任何 Linux 桥接网络中任何已发布端口，使用守护进程选项 `"allow-direct-routing": true`，在 `/etc/docker/daemon.json` 中配置，或使用等效的 `--allow-direct-routing`。

要允许从特定主机接口直接路由到特定桥接网络，参阅 [网关模式](#gateway-modes)。

或者，要允许通过特定主机接口直接路由到特定桥接网络，在创建网络时使用以下选项：
- `com.docker.network.bridge.trusted_host_interfaces`

#### 示例

创建一个网络，其中容器 IP 地址上的已发布端口可直接从接口 `vxlan.1` 和 `eth3` 访问：

```console
$ docker network create --subnet 192.0.2.0/24 --ip-range 192.0.2.0/29 -o com.docker.network.bridge.trusted_host_interfaces="vxlan.1:eth3" mynet
```

在该网络中运行一个容器，将其 80 端口发布到主机回环接口的 8080 端口：

```console
$ docker run -d --ip 192.0.2.100 -p 127.0.0.1:8080:80 nginx
```

现在，Docker 主机上运行在容器 80 端口的 Web 服务器可通过 `http://127.0.0.1:8080` 访问，也可直接通过 `http://192.0.2.100:80` 访问。如果通过 `vxlan.1` 和 `eth3` 连接到 Docker 主机的远程主机在 Docker 主机内部有到 `192.0.2.0/24` 网络的路由，它们也可以通过 `http://192.0.2.100:80` 访问该 Web 服务器。

## 网关模式

桥接网络驱动程序具有以下选项：
- `com.docker.network.bridge.gateway_mode_ipv6`
- `com.docker.network.bridge.gateway_mode_ipv4`

每个选项可设置为以下网关模式之一：
- `nat`
- `nat-unprotected`
- `routed`
- `isolated`

默认值为 `nat`，为每个已发布的容器端口设置 NAT 和伪装规则。离开主机的数据包将使用主机地址。

在 `routed` 模式下，不设置 NAT 或伪装规则，但仍设置防火墙规则，仅允许访问已发布的容器端口。来自容器的出站数据包将使用容器地址，而非主机地址。

要访问 `routed` 网络中的已发布端口，远程主机必须通过 Docker 主机上的外部地址路由到容器网络（“直接路由”）。本地二层网络上的主机无需额外网络配置即可设置直接路由。只有当网络路由器配置为启用直接路由时，本地网络外的主机才能使用直接路由访问容器。

在 `nat` 模式网络中，将端口发布到回环接口地址意味着远程主机无法访问它。`routed` 和 `nat` 网络中的其他已发布容器端口始终可通过直接路由从远程主机访问，除非 Docker 主机的防火墙有额外限制。

> [!NOTE]
>
> 在 `nat` 模式下，当端口发布到特定主机地址且 Docker 主机启用了 IP 转发时，发布的端口可通过其他主机接口使用直接路由访问，通过主机地址路由。
>
> 例如，启用了 IP 转发的 Docker 主机有两个网卡，地址分别为 `192.168.100.10/24` 和 `10.0.0.10/24`。当端口发布到 `192.168.100.10` 时，`10.0.0.0/24` 子网中的主机可通过 `10.0.0.10` 路由到 `192.168.100.10` 来访问该端口。

在 `nat-unprotected` 模式下，未发布的容器端口也可通过直接路由访问，不设置端口过滤规则。此模式用于兼容遗留的默认行为。

网关模式也影响同一主机上连接到不同 Docker 网络的容器之间的通信。
- 在 `nat` 和 `nat-unprotected` 模式下，其他桥接网络中的容器只能通过发布的端口地址访问，不能从其他网络直接路由。
- 在 `routed` 模式下，其他网络中的容器可使用直接路由访问端口，无需通过主机地址。

在 `routed` 模式下，`-p` 或 `--publish` 端口映射中的主机端口不被使用，主机地址仅用于决定是否将映射应用于 IPv4 或 IPv6。因此，当映射仅适用于 `routed` 模式时，应仅使用地址 `0.0.0.0` 或 `::`，且不应指定主机端口。如果指定了特定地址或端口，它对已发布端口无效，且会记录警告消息。

模式 `isolated` 仅在使用 CLI 标志 `--internal` 或等效选项创建网络时可用。通常会在 `internal` 网络中为桥接设备分配地址。因此，Docker 主机上的进程可以访问该网络，网络中的容器也可以访问主机上监听该桥接地址的服务（包括监听“任意”主机地址 `0.0.0.0` 或 `::` 的服务）。当网络使用网关模式 `isolated` 创建时，不会为桥接设备分配地址。

### 示例

创建一个适用于 IPv6 直接路由的网络，同时为 IPv4 启用 NAT：
```console
$ docker network create --ipv6 --subnet 2001:db8::/64 -o com.docker.network.bridge.gateway_mode_ipv6=routed mynet
```

创建一个带有已发布端口的容器：
```console
$ docker run --network=mynet -p 8080:80 myimage
```

然后：
- 仅容器的 80 端口将打开，适用于 IPv4 和 IPv6。
- 对于 IPv6，使用 `routed` 模式，容器 IP 地址上的 80 端口将打开。主机 IP 地址上的 8080 端口不会打开，出站数据包将使用容器 IP 地址。
- 对于 IPv4，使用默认的 `nat` 模式，容器的 80 端口将通过主机 IP 地址上的 8080 端口访问，也可直接从 Docker 主机内部访问。但容器的 80 端口无法直接从主机外部访问。来自容器的连接将进行伪装，使用主机 IP 地址。

在 `docker inspect` 中，此端口映射将显示如下。注意 IPv6 没有 `HostPort`，因为它使用 `routed` 模式：
```console
$ docker container inspect <id> --format "{{json .NetworkSettings.Ports}}"
{"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"8080"},{"HostIp":"::","HostPort":""}]}
```

或者，要使映射仅适用于 IPv6，禁用 IPv4 访问容器的 80 端口，使用未指定的 IPv6 地址 `[::]` 且不包含主机端口号：
```console
$ docker run --network mynet -p '[::]::80'
```

## 设置容器的默认绑定地址

默认情况下，当容器端口映射未指定特定主机地址时，Docker 守护进程将端口发布到所有主机地址（`0.0.0.0` 和 `[::]`）。

例如，以下命令将 8080 端口发布到主机上的所有网络接口，包括 IPv4 和 IPv6 地址，可能使其对网络外部可用。

```console
docker run -p 8080:80 nginx
```

你可以更改已发布容器端口的默认绑定地址，使其默认仅对 Docker 主机可用。为此，你可以将守护进程配置为使用回环地址（`127.0.0.1`）。

> [!WARNING]
>
> 在 28.0.0 之前的版本中，同一 L2 网段（例如，连接到同一网络交换机的主机）中的主机可以访问发布到本地回环的端口。更多信息请参阅
> [moby/moby#45610](https://github.com/moby/moby/issues/45610)

要为用户自定义桥接网络配置此设置，使用 `com.docker.network.bridge.host_binding_ipv4`
[驱动选项](./drivers/bridge.md#default-host-binding-address) 创建网络。尽管选项名称如此，但可以指定 IPv6 地址。

```console
$ docker network create mybridge \
  -o "com.docker.network.bridge.host_binding_ipv4=127.0.0.1"
```

或者，要为所有用户自定义桥接网络中的容器设置默认绑定地址，使用守护进程配置选项 `default-network-opts`。例如：

```json
{
  "default-network-opts": {
    "bridge": {
      "com.docker.network.bridge.host_binding_ipv4": "127.0.0.1"
    }
  }
}
```

> [!NOTE]
>
> 将默认绑定地址设置为 `::` 意味着未指定主机地址的端口绑定将在主机上的任何 IPv6 地址上工作。但 `0.0.0.0` 意味着任何 IPv4 或 IPv6 地址。
>
> 更改默认绑定地址对 Swarm 服务没有影响。Swarm 服务始终在 `0.0.0.0` 网络接口上暴露。

### 出站数据包的伪装或 SNAT

默认情况下，桥接网络启用 NAT，意味着来自容器的出站数据包会被伪装。离开 Docker 主机的数据包的源地址将更改为数据包发送接口上的主机地址。

可以通过在创建网络时使用 `com.docker.network.bridge.enable_ip_masquerade` 驱动选项，为用户自定义桥接网络禁用伪装。例如：
```console
$ docker network create mybridge \
  -o com.docker.network.bridge.enable_ip_masquerade=false ...
```

要为用户自定义网络使用特定的出站数据包源地址，而不是让伪装选择地址，使用选项 `com.docker.network.host_ipv4` 和 `com.docker.network.host_ipv6` 指定要使用的源网络地址转换（SNAT）地址。`com.docker.network.bridge.enable_ip_masquerade` 选项必须为 `true`（默认值），这些选项才能生效。

### 默认桥接网络

要为默认桥接网络设置默认绑定，配置 `daemon.json` 配置文件中的 `"ip"` 键：

```json
{
  "ip": "127.0.0.1"
}
```

这将默认桥接网络上已发布容器端口的默认绑定地址更改为 `127.0.0.1`。
重启守护进程以使此更改生效。
或者，你可以在启动守护进程时使用 `dockerd --ip` 标志。