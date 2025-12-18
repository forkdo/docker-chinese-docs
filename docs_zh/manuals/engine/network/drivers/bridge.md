---
title: Bridge 网络驱动
description: 关于使用用户自定义桥接网络和默认桥接网络的全部内容
keywords: 网络、桥接、用户自定义、独立
aliases:
  - /config/containers/bridges/
  - /engine/userguide/networking/default_network/build-bridges/
  - /engine/userguide/networking/default_network/custom-docker0/
  - /engine/userguide/networking/work-with-networks/
  - /network/bridge/
  - /network/drivers/bridge/
  - /engine/network/tutorials/standalone/
---

Docker 桥接网络具有 IPv4 子网，以及可选的 IPv6 子网。连接到桥接网络的每个容器都有一个网络接口，其地址位于网络的子网中。默认情况下，它：

- 允许主机和同一桥接网络上的其他容器不受限制地访问网络中的容器。
- 阻止来自其他网络的容器和 Docker 主机外部的访问。
- 使用伪装（masquerading）为容器提供外部网络访问。外部网络上的设备只能看到 Docker 主机的 IP 地址。
- 支持端口发布（port publishing），网络流量在容器端口和主机 IP 地址上的端口之间转发。发布的端口可以从 Docker 主机外部通过其 IP 地址访问。

从 Docker 的角度来看，桥接网络使用软件桥接，允许连接到同一桥接网络的容器相互通信，同时与未连接到该桥接网络的容器隔离。默认情况下，Docker 桥接驱动会自动在主机上安装规则，使得连接到不同桥接网络的容器只能通过发布的端口相互通信。

桥接网络适用于在同一 Docker 守护进程主机上运行的容器。对于在不同 Docker 守护进程主机上运行的容器之间的通信，您可以手动管理路由，或者使用 [覆盖网络](overlay.md)。

启动 Docker 时，会自动创建一个 [默认桥接网络](#use-the-default-bridge-network)（也称为 `bridge`），新启动的容器除非另有指定，否则会连接到它。您也可以创建用户自定义的桥接网络。**用户自定义的桥接网络优于默认的 `bridge` 网络。**

## 用户自定义桥接网络与默认桥接网络的区别

- **用户自定义桥接网络提供容器间的自动 DNS 解析**。

  默认桥接网络上的容器只能通过 IP 地址相互访问，除非您使用 [`--link` 选项](../links.md)，但该选项已被视为过时。在用户自定义桥接网络上，容器可以通过名称或别名相互解析。

  想象一个具有 Web 前端和数据库后端的应用。如果您将容器命名为 `web` 和 `db`，那么 Web 容器可以在任何 Docker 主机上通过 `db` 连接到 db 容器。

  如果您在默认桥接网络上运行相同的应用栈，您需要手动创建容器之间的链接（使用过时的 `--link` 标志）。这些链接需要双向创建，因此当超过两个需要通信的容器时，这会变得复杂。或者，您可以操作容器内的 `/etc/hosts` 文件，但这会产生难以调试的问题。

- **用户自定义桥接网络提供更好的隔离性**。

  所有没有指定 `--network` 的容器都会附加到默认桥接网络。这可能有风险，因为不相关的栈/服务/容器可以相互通信。

  使用用户自定义网络提供了一个作用域网络，只有附加到该网络的容器才能相互通信。

- **容器可以在运行时动态连接和断开用户自定义网络**。

  在容器的生命周期中，您可以动态地将其连接或断开用户自定义网络。要将容器从默认桥接网络中移除，您需要停止容器并使用不同的网络选项重新创建它。

- **每个用户自定义网络创建一个可配置的桥接**。

  如果您的容器使用默认桥接网络，您可以配置它，但所有容器都使用相同的设置，例如 MTU 和 `iptables` 规则。此外，默认桥接网络的配置在 Docker 之外进行，需要重启 Docker。

  用户自定义桥接网络使用 `docker network create` 创建和配置。如果不同的应用组有不同的网络需求，您可以在创建时分别为每个用户自定义桥接网络进行配置。

- **默认桥接网络上的链接容器共享环境变量**。

  最初，容器间共享环境变量的唯一方法是使用 [`--link` 标志](../links.md) 将它们链接起来。这种变量共享在用户自定义网络中是不可能的。但是，有更优越的方法来共享环境变量。一些想法：
  - 多个容器可以挂载包含共享信息的文件或目录，使用 Docker 卷。

  - 可以使用 `docker-compose` 启动多个容器，compose 文件可以定义共享变量。

  - 您可以使用 Swarm 服务而不是独立容器，并利用共享 [密钥](/manuals/engine/swarm/secrets.md) 和 [配置](/manuals/engine/swarm/configs.md)。

连接到同一用户自定义桥接网络的容器实际上会向彼此暴露所有端口。要使端口对不同网络上的容器或非 Docker 主机可访问，必须使用 `-p` 或 `--publish` 标志 _发布_ 该端口。

## 选项

下表描述了使用 `bridge` 驱动创建自定义网络时，可以传递给 `--opt` 的驱动特定选项。

| 选项                                                                                          | 默认                     | 描述                                                                                         |
| ----------------------------------------------------------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------- |
| `com.docker.network.bridge.name`                                                                |                             | 创建 Linux 桥接时使用的接口名称。                                               |
| `com.docker.network.bridge.enable_ip_masquerade`                                                | `true`                      | 启用 IP 伪装。                                                                             |
| `com.docker.network.host_ipv4`<br/>`com.docker.network.host_ipv6`                               |                             | 用于源 NAT 的地址。请参阅 [数据包过滤和防火墙](packet-filtering-firewalls.md)。 |
| `com.docker.network.bridge.gateway_mode_ipv4`<br/>`com.docker.network.bridge.gateway_mode_ipv6` | `nat`                       | 控制外部连接性。请参阅 [数据包过滤和防火墙](packet-filtering-firewalls.md)。 |
| `com.docker.network.bridge.enable_icc`                                                          | `true`                      | 启用或禁用容器间连接。                                                     |
| `com.docker.network.bridge.host_binding_ipv4`                                                   | 所有 IPv4 和 IPv6 地址 | 绑定容器端口时的默认 IP。                                                            |
| `com.docker.network.driver.mtu`                                                                 | `0`（无限制）              | 设置容器网络的最大传输单元（MTU）。                                         |
| `com.docker.network.container_iface_prefix`                                                     | `eth`                       | 设置容器接口的自定义前缀。                                                       |
| `com.docker.network.bridge.inhibit_ipv4`                                                        | `false`                     | 防止 Docker [为桥接分配 IP 地址](#skip-bridge-ip-address-configuration)。 |

其中一些选项也可以作为 `dockerd` CLI 的标志使用，您可以在启动 Docker 守护进程时使用它们配置默认的 `docker0` 桥接。下表显示了哪些选项在 `dockerd` CLI 中有等效的标志。

| 选项                                           | 标志        |
| ------------------------------------------------ | ----------- |
| `com.docker.network.bridge.name`                 | -           |
| `com.docker.network.bridge.enable_ip_masquerade` | `--ip-masq` |
| `com.docker.network.bridge.enable_icc`           | `--icc`     |
| `com.docker.network.bridge.host_binding_ipv4`    | `--ip`      |
| `com.docker.network.driver.mtu`                  | `--mtu`     |
| `com.docker.network.container_iface_prefix`      | -           |

Docker 守护进程支持 `--bridge` 标志，您可以使用它来定义自己的 `docker0` 桥接。如果您想在同一主机上运行多个守护进程实例，请使用此选项。详细信息请参阅 [运行多个守护进程](/reference/cli/dockerd.md#run-multiple-daemons)。

### 默认主机绑定地址

当端口发布选项（如 `-p 80` 或 `-p 8080:80`）中未指定主机地址时，默认情况下容器的端口 80 将在所有主机地址（IPv4 和 IPv6）上可用。

桥接网络驱动选项 `com.docker.network.bridge.host_binding_ipv4` 可用于修改已发布端口的默认地址。

尽管选项名称如此，但可以指定 IPv6 地址。

当默认绑定地址是分配给特定接口的地址时，容器的端口只能通过该地址访问。

将默认绑定地址设置为 `::` 意味着已发布的端口只能在主机的 IPv6 地址上使用。但是，将其设置为 `0.0.0.0` 意味着它将在主机的 IPv4 和 IPv6 地址上使用。

要将已发布的端口限制为仅 IPv4，地址必须包含在容器的发布选项中。例如，`-p 0.0.0.0:8080:80`。

## 管理用户自定义桥接网络

使用 `docker network create` 命令创建用户自定义桥接网络。

```console
$ docker network create my-net
```

您可以指定子网、IP 地址范围、网关和其他选项。请参阅 [docker network create](/reference/cli/docker/network/create.md#specify-advanced-options) 参考或 `docker network create --help` 的输出以获取详细信息。

使用 `docker network rm` 命令删除用户自定义桥接网络。如果容器当前连接到网络，请先 [断开它们](#disconnect-a-container-from-a-user-defined-bridge)。

```console
$ docker network rm my-net
```

> **实际发生了什么？**
>
> 当您创建或删除用户自定义桥接网络，或将容器连接或断开用户自定义桥接网络时，Docker 使用特定于操作系统的工具来管理底层网络基础设施（例如在 Linux 上添加或删除桥接设备或配置 `iptables` 规则）。这些细节应被视为实现细节。让 Docker 为您管理用户自定义网络。

## 将容器连接到用户自定义桥接网络

创建新容器时，您可以指定一个或多个 `--network` 标志。此示例将 Nginx 容器连接到 `my-net` 网络。它还将容器中的端口 80 发布到 Docker 主机的端口 8080，以便外部客户端可以访问该端口。连接到 `my-net` 网络的任何其他容器都可以访问 `my-nginx` 容器上的所有端口，反之亦然。

```console
$ docker create --name my-nginx \
  --network my-net \
  --publish 8080:80 \
  nginx:latest
```

要将正在运行的容器连接到现有的用户自定义桥接网络，请使用 `docker network connect` 命令。以下命令将已运行的 `my-nginx` 容器连接到已存在的 `my-net` 网络：

```console
$ docker network connect my-net my-nginx
```

## 从用户自定义桥接网络断开容器连接

要将正在运行的容器从用户自定义桥接网络断开连接，请使用 `docker network disconnect` 命令。以下命令将 `my-nginx` 容器从 `my-net` 网络断开连接。

```console
$ docker network disconnect my-net my-nginx
```

## 在用户自定义桥接网络中使用 IPv6

创建网络时，您可以指定 `--ipv6` 标志以启用 IPv6。

```console
$ docker network create --ipv6 --subnet 2001:db8:1234::/64 my-net
```

如果您不提供 `--subnet` 选项，将自动选择一个唯一本地地址（ULA）前缀。

## 仅 IPv6 桥接网络

要在桥接及其容器中跳过 IPv4 地址配置，请使用选项 `--ipv4=false` 创建网络，并使用 `--ipv6` 启用 IPv6。

```console
$ docker network create --ipv6 --ipv4=false v6net
```

无法在默认桥接网络中禁用 IPv4 地址配置。

## 使用默认桥接网络

默认的 `bridge` 网络被认为是 Docker 的遗留细节，不建议在生产环境中使用。配置它是手动操作，且存在 [技术缺陷](#differences-between-user-defined-bridges-and-the-default-bridge)。

### 将容器连接到默认桥接网络

如果您未使用 `--network` 标志指定网络，且未指定网络驱动，您的容器默认连接到默认的 `bridge` 网络。连接到默认 `bridge` 网络的容器可以相互通信，但只能通过 IP 地址，除非它们使用过时的 [`--link` 标志](../links.md) 链接。

### 配置默认桥接网络

要配置默认的 `bridge` 网络，请在 `daemon.json` 中指定选项。以下是一个指定多个选项的 `daemon.json` 示例。仅指定您需要自定义的设置。

```json
{
  "bip": "192.168.1.1/24",
  "fixed-cidr": "192.168.1.0/25",
  "mtu": 1500,
  "default-gateway": "192.168.1.254",
  "dns": ["10.20.1.2", "10.20.1.3"]
}
```

在此示例中：

- 桥接的地址是 "192.168.1.1/24"（来自 `bip`）。
- 桥接网络的子网是 "192.168.1.0/24"（来自 `bip`）。
- 容器地址将从 "192.168.1.0/25"（来自 `fixed-cidr`）分配。

### 在默认桥接网络中使用 IPv6

可以使用 `daemon.json` 中的以下选项或其命令行等效项为默认桥接启用 IPv6。

这三个选项仅影响默认桥接，用户自定义网络不使用它们。下面的地址来自 IPv6 文档范围的示例。

- 选项 `ipv6` 是必需的。
- 选项 `bip6` 是可选的，它指定默认桥接的地址，容器将使用它作为默认网关。它还指定桥接网络的子网。
- 选项 `fixed-cidr-v6` 是可选的，它指定 Docker 可能自动分配给容器的地址范围。
  - 前缀通常应为 `/64` 或更短。
  - 为了在本地网络上进行实验，使用唯一本地地址（ULA）前缀（匹配 `fd00::/8`）比使用链路本地前缀（匹配 `fe80::/10`）更好。
- 选项 `default-gateway-v6` 是可选的。如果未指定，默认值是 `fixed-cidr-v6` 子网中的第一个地址。

```json
{
  "ipv6": true,
  "bip6": "2001:db8::1111/64",
  "fixed-cidr-v6": "2001:db8::/64",
  "default-gateway-v6": "2001:db8:abcd::89"
}
```

如果未指定 `bip6`，`fixed-cidr-v6` 定义桥接网络的子网。如果未指定 `bip6` 或 `fixed-cidr-v6`，将选择一个 ULA 前缀。

重启 Docker 以使更改生效。

## 桥接网络的连接限制

由于 Linux 内核的限制，当 1000 个或更多容器连接到单个网络时，桥接网络会变得不稳定，容器间通信可能中断。

有关此限制的更多信息，请参阅 [moby/moby#44973](https://github.com/moby/moby/issues/44973#issuecomment-1543747718)。

## 跳过桥接 IP 地址配置

桥接通常被分配网络的 `--gateway` 地址，该地址用作从桥接网络到其他网络的默认路由。

选项 `com.docker.network.bridge.inhibit_ipv4` 允许您创建一个不为桥接分配 IPv4 网关地址的网络。如果您想手动配置桥接的网关 IP 地址，这很有用。例如，如果您将物理接口添加到桥接中，并且需要它具有网关地址。

在此配置下，除非您已手动在桥接或连接到它的设备上配置网关地址，否则南北向流量（到和来自桥接网络）将无法工作。

此选项只能与用户自定义桥接网络一起使用。

## 使用示例

本节提供了使用桥接网络的实际示例。

### 使用默认桥接网络

此示例显示默认的 `bridge` 网络如何工作。您在默认桥接上启动两个 `alpine` 容器并测试它们如何通信。

> [!NOTE]
> 默认的 `bridge` 网络不推荐用于生产环境。请改用用户自定义桥接网络。

1. 列出现有网络：

   ```console
   $ docker network ls

   NETWORK ID          NAME                DRIVER              SCOPE
   17e324f45964        bridge              bridge              local
   6ed54d316334        host                host                local
   7092879f2cc8        none                null                local
   ```

   默认的 `bridge` 网络已列出，以及 `host` 和 `none`。

2. 启动两个运行 `ash` 的 `alpine` 容器。`-dit` 标志表示分离、交互和 TTY。由于您未指定 `--network` 标志，容器连接到默认的 `bridge` 网络。

   ```console
   $