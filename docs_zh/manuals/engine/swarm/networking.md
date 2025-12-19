---
description: 使用 swarm 模式的覆盖网络功能
keywords: swarm, networking, ingress, overlay, service discovery
title: 管理 swarm 服务网络
toc_max: 3
---

本页面介绍 swarm 服务的网络。

## Swarm 和流量类型

Docker swarm 会产生两种不同的流量：

- 控制和管理平面流量：这包括 swarm 管理消息，例如加入或离开 swarm 的请求。此流量始终经过加密。

- 应用数据平面流量：这包括容器流量以及与外部客户端之间的流量。

## 关键网络概念

以下三个网络概念对 swarm 服务非常重要：

- **覆盖网络（Overlay networks）** 管理参与 swarm 的 Docker 守护进程之间的通信。你可以创建覆盖网络，方式与为独立容器创建用户定义网络相同。你也可以将服务附加到一个或多个现有的覆盖网络，以实现服务间通信。覆盖网络是使用 `overlay` 网络驱动程序的 Docker 网络。

- **入口网络（Ingress network）** 是一种特殊的覆盖网络，用于在服务的节点之间实现负载均衡。当任何 swarm 节点在发布的端口上接收到请求时，它会将该请求移交给一个名为 `IPVS` 的模块。`IPVS` 会跟踪参与该服务的所有 IP 地址，选择其中一个，并通过 `ingress` 网络将请求路由到该地址。

  当你初始化或加入 swarm 时，`ingress` 网络会自动创建。大多数用户不需要自定义其配置，但 Docker 允许你这样做。

- **docker_gwbridge** 是一个桥接网络，用于将覆盖网络（包括 `ingress` 网络）连接到单个 Docker 守护进程的物理网络。默认情况下，服务运行的每个容器都连接到其本地 Docker 守护进程主机的 `docker_gwbridge` 网络。

  当你初始化或加入 swarm 时，`docker_gwbridge` 网络会自动创建。大多数用户不需要自定义其配置，但 Docker 允许你这样做。

> [!TIP]
>
> 另请参阅[网络概述](/manuals/engine/network/_index.md)以获取有关 Swarm 网络的更多详细信息。

## 防火墙注意事项

参与 swarm 的 Docker 守护进程需要能够通过以下端口相互通信：

* 端口 `7946` TCP/UDP 用于容器网络发现。
* 端口 `4789` UDP（可配置）用于覆盖网络（包括入口）的数据路径。

在 Swarm 中设置网络时，应特别小心。请查阅[教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts)以获取概述。

## 覆盖网络

当你初始化 swarm 或将 Docker 主机加入现有 swarm 时，会在该 Docker 主机上创建两个新网络：

- 一个名为 `ingress` 的覆盖网络，用于处理与 swarm 服务相关的控制和数据流量。当你创建 swarm 服务且未将其连接到用户定义的覆盖网络时，它默认会连接到 `ingress` 网络。
- 一个名为 `docker_gwbridge` 的桥接网络，用于将单个 Docker 守护进程连接到参与 swarm 的其他守护进程。

### 创建覆盖网络

要创建覆盖网络，请在使用 `docker network create` 命令时指定 `overlay` 驱动程序：

```console
$ docker network create \
  --driver overlay \
  my-network
```

上述命令未指定任何自定义选项，因此 Docker 会分配一个子网并使用默认选项。你可以使用 `docker network inspect` 查看有关网络的信息。

当没有容器连接到覆盖网络时，其配置并不十分令人兴奋：

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "0001-01-01T00:00:00Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": null,
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": null
    }
]
```

在上面的输出中，请注意驱动程序是 `overlay`，范围是 `swarm`，而不是你在其他类型的 Docker 网络中可能看到的 `local`、`host` 或 `global` 范围。此范围表示只有参与 swarm 的主机才能访问此网络。

网络的子网和网关在服务首次连接到网络时动态配置。以下示例显示了与上面相同的网络，但连接了 `redis` 服务的三个容器。

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "2017-05-31T18:35:58.877628262Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.0.0.0/24",
                    "Gateway": "10.0.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": {
            "0e08442918814c2275c31321f877a47569ba3447498db10e25d234e47773756d": {
                "Name": "my-redis.1.ka6oo5cfmxbe6mq8qat2djgyj",
                "EndpointID": "950ce63a3ace13fe7ef40724afbdb297a50642b6d47f83a5ca8636d44039e1dd",
                "MacAddress": "02:42:0a:00:00:03",
                "IPv4Address": "10.0.0.3/24",
                "IPv6Address": ""
            },
            "88d55505c2a02632c1e0e42930bcde7e2fa6e3cce074507908dc4b827016b833": {
                "Name": "my-redis.2.s7vlybipal9xlmjfqnt6qwz5e",
                "EndpointID": "dd822cb68bcd4ae172e29c321ced70b731b9994eee5a4ad1d807d9ae80ecc365",
                "MacAddress": "02:42:0a:00:00:05",
                "IPv4Address": "10.0.0.5/24",
                "IPv6Address": ""
            },
            "9ed165407384f1276e5cfb0e065e7914adbf2658794fd861cfb9b991eddca754": {
                "Name": "my-redis.3.hbz3uk3hi5gb61xhxol27hl7d",
                "EndpointID": "f62c686a34c9f4d70a47b869576c37dffe5200732e1dd6609b488581634cf5d2",
                "MacAddress": "02:42:0a:00:00:04",
                "IPv4Address": "10.0.0.4/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "moby-e57c567e25e2",
                "IP": "192.168.65.2"
            }
        ]
    }
]
```

### 自定义覆盖网络

在某些情况下，你可能不想使用覆盖网络的默认配置。有关可配置选项的完整列表，请运行命令 `docker network create --help`。以下是一些最常见的可更改选项。

#### 配置子网和网关

默认情况下，网络的子网和网关在首次将服务连接到网络时自动配置。你可以在创建网络时使用 `--subnet` 和 `--gateway` 标志进行配置。以下示例通过配置子网和网关扩展了前面的示例。

```console
$ docker network create \
  --driver overlay \
  --subnet 10.0.9.0/24 \
  --gateway 10.0.9.99 \
  my-network
```

##### 使用自定义默认地址池

要自定义 Swarm 网络的子网分配，你可以在 `swarm init` 期间[可选地配置它们](swarm-mode.md)。

例如，以下命令在初始化 Swarm 时使用：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 26
```

每当用户创建网络但未使用 `--subnet` 命令行选项时，该网络的子网将从池中下一个可用的子网顺序分配。如果指定的网络已被分配，则该网络将不会用于 Swarm。

如果需要不连续的地址空间，可以配置多个池。但是，不支持从特定池进行分配。网络子网将从 IP 池空间中顺序分配，并且子网在从已删除的网络中释放后将被重用。

可以配置默认掩码长度，并且对所有网络都相同。默认设置为 `/24`。要更改默认子网掩码长度，请使用 `--default-addr-pool-mask-length` 命令行选项。

> [!NOTE]
>
> 默认地址池只能在 `swarm init` 上配置，集群创建后无法更改。

##### 覆盖网络大小限制

Docker 建议使用 `/24` 块创建覆盖网络。`/24` 覆盖网络块将网络限制为 256 个 IP 地址。

此建议解决了[swarm 模式的限制](https://github.com/moby/moby/issues/30820)。
如果你需要超过 256 个 IP 地址，请不要增加 IP 块大小。你可以使用带有外部负载均衡器的 `dnsrr` 端点模式，或者使用多个较小的覆盖网络。有关不同端点模式的更多信息，请参阅[配置服务发现](#configure-service-discovery)。

#### 配置应用数据加密 {#encryption}

与 swarm 相关的管理和控制平面数据始终经过加密。有关加密机制的更多详细信息，请参阅 [Docker swarm 模式覆盖网络安全模型](/manuals/engine/network/drivers/overlay.md)。

Swarm 节点之间的应用数据默认不加密。要在给定的覆盖网络上加密此流量，请在 `docker network create` 上使用 `--opt encrypted` 标志。这会在 vxlan 级别启用 IPSEC 加密。这种加密会带来不可忽视的性能损失，因此在生产中使用此选项之前应进行测试。

> [!NOTE]
>
> 你必须[自定义自动创建的入口](#customize-ingress)以启用加密。默认情况下，所有入口流量都是未加密的，因为加密是网络级别的选项。

## 将服务附加到覆盖网络

要将服务附加到现有的覆盖网络，请将 `--network` 标志传递给 `docker service create`，或将 `--network-add` 标志传递给 `docker service update`。

```console
$ docker service create \
  --replicas 3 \
  --name my-web \
  --network my-network \
  nginx
```

连接到覆盖网络的服务容器可以通过该网络相互通信。

要查看服务连接到哪些网络，请使用 `docker service ls` 找到服务的名称，然后使用 `docker service ps <service-name>` 列出网络。或者，要查看哪些服务的容器连接到某个网络，请使用 `docker network inspect <network-name>`。你可以从任何加入 swarm 且处于 `running` 状态的 swarm 节点运行这些命令。

### 配置服务发现

服务发现是 Docker 用来将请求从服务的外部客户端路由到单个 swarm 节点的机制，客户端无需知道有多少节点参与服务或其 IP 地址和端口。对于同一网络上的服务之间使用的端口，你不需要发布。例如，如果你有一个[将其数据存储在 MySQL 服务中的 WordPress 服务](https://training.play-with-docker.com/swarm-service-discovery/)，并且它们连接到同一个覆盖网络，则你不需要将 MySQL 端口发布给客户端，只需发布 WordPress HTTP 端口。

服务发现可以以两种不同的方式工作：使用嵌入式 DNS 和虚拟 IP (VIP) 在第 3 层和第 4 层进行基于连接的内部负载均衡，或者使用 DNS 轮询 (DNSRR) 在第 7 层进行外部和定制的基于请求的负载均衡。你可以按服务配置此设置。

- 默认情况下，当你将服务附加到网络并且该服务发布一个或多个端口时，Docker 会为该服务分配一个虚拟 IP (VIP)，这是客户端访问服务的“前端”。Docker 保留服务中所有工作节点的列表，并在客户端和其中一个节点之间路由请求。来自客户端的每个请求可能会路由到不同的节点。

- 如果你将服务配置为使用 DNS 轮询 (DNSRR) 服务发现，则没有单一的虚拟 IP。相反，Docker 会为该服务设置 DNS 条目，使得对服务名称的 DNS 查询返回一个 IP 地址列表，客户端直接连接到其中一个地址。

  DNS 轮询在你想要使用自己的负载均衡器（例如 HAProxy）的情况下非常有用。要配置服务使用 DNSRR，请在创建新服务或更新现有服务时使用标志 `--endpoint-mode dnsrr`。

## 自定义入口网络 {#customize-ingress}

大多数用户永远不需要配置 `ingress` 网络，但 Docker 允许你这样做。如果自动选择的子网与网络上已有的子网冲突，或者你需要自定义其他低级网络设置（如 MTU），或者你想[启用加密](#encryption)，这可能很有用。

自定义 `ingress` 网络涉及删除并重新创建它。这通常在 swarm 中创建任何服务之前完成。如果你有发布端口的现有服务，则需要先删除这些服务，然后才能删除 `ingress` 网络。

在没有 `ingress` 网络期间，不发布端口的现有服务会继续运行，但不会进行负载均衡。这会影响发布端口的服务，例如发布端口 80 的 WordPress 服务。

1.  使用 `docker network inspect ingress` 检查 `ingress` 网络，并删除其容器连接到它的任何服务。这些是发布端口的服务，例如发布端口 80 的 WordPress 服务。如果未停止所有此类服务，下一步将失败。

2.  删除现有的 `ingress` 网络：

    ```console
    $ docker network rm ingress

    WARNING! Before removing the routing-mesh network, make sure all the nodes
    in your swarm run the same docker engine version. Otherwise, removal may not
    be effective and functionality of newly created ingress networks will be
    impaired.
    Are you sure you want to continue? [y/N]
    ```

3.  使用 `--ingress` 标志以及你想要设置的自定义选项创建一个新的覆盖网络。此示例将 MTU 设置为 1200，将子网设置为 `10.11.0.0/16`，并将网关设置为 `10.11.0.2`。

    ```console
    $ docker network create \
      --driver overlay \
      --ingress \
      --subnet=10.11.0.0/16 \
      --gateway=10.11.0.2 \
      --opt com.docker.network.driver.mtu=1200 \
      my-ingress
    ```

    > [!NOTE]
    >
    > 你可以将你的 `ingress` 网络命名为 `ingress` 以外的名称，但你只能有一个。尝试创建第二个会失败。

4.  重新启动你在第一步中停止的服务。

## 自定义 docker_gwbridge

`docker_gwbridge` 是一个虚拟网桥，用于将覆盖网络（包括 `ingress` 网络）连接到单个 Docker 守护进程的物理网络。当你初始化 swarm 或将 Docker 主机加入 swarm 时，Docker 会自动创建它，但它不是 Docker 设备。它存在于 Docker 主机的内核中。如果你需要自定义其设置，必须在将 Docker 主机加入 swarm 之前或暂时将主机从 swarm 中移除后进行。

你需要在操作系统上安装 `brctl` 应用程序才能删除现有的网桥。软件包名称为 `bridge-utils`。

1.  停止 Docker。

2.  使用 `brctl show docker_gwbridge` 命令检查是否存在名为 `docker_gwbridge` 的网桥设备。如果存在，请使用 `brctl delbr docker_gwbridge` 将其删除。

3.  启动 Docker。不要加入或初始化 swarm。

4.  使用你的自定义设置创建或重新创建 `docker_gwbridge` 网桥。此示例使用子网 `10.11.0.0/16`。有关可自定义选项的完整列表，请参阅[网桥驱动程序选项](/reference/cli/docker/network/create.md#bridge-driver-options)。

    ```console
    $ docker network create \
    --subnet 10.11.0.0/16 \
    --opt com.docker.network.bridge.name=docker_gwbridge \
    --opt com.docker.network.bridge.enable_icc=false \
    --opt com.docker.network.bridge.enable_ip_masquerade=true \
    docker_gwbridge
    ```

5.  初始化或加入 swarm。

## 为控制和数据流量使用单独的接口

默认情况下，所有 swarm 流量都通过同一接口发送，包括用于维护 swarm 本身的控制和管理流量，以及服务容器的进出数据流量。

你可以在初始化或加入 swarm 时传递 `--data-path-addr` 标志来分离此流量。如果有多个接口，则必须显式指定 `--advertise-addr`，如果未指定，`--data-path-addr` 默认为 `--advertise-addr`。有关加入、离开和管理 swarm 的流量通过 `--advertise-addr` 接口发送，服务容器之间的流量通过 `--data-path-addr` 接口发送。这些标志可以采用 IP 地址或网络设备名称，例如 `eth0`。

此示例使用单独的 `--data-path-addr` 初始化 swarm。它假设你的 Docker 主机有两个不同的网络接口：10.0.0.1 应用于控制和管理流量，192.168.0.1 应用于与服务相关的流量。

```console
$ docker swarm init --advertise-addr 10.0.0.1 --data-path-addr 192.168.0.1
```

此示例加入由主机 `192.168.99.100:2377` 管理的 swarm，并将 `--advertise-addr` 标志设置为 `eth0`，将 `--data-path-addr` 标志设置为 `eth1`。

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2d7c \
  --advertise-addr eth0 \
  --data-path-addr eth1 \
  192.168.99.100:2377
```

## 在覆盖网络上发布端口

连接到同一覆盖网络的 Swarm 服务有效地向彼此公开所有端口。要使端口在服务外部可访问，必须使用 `docker service create` 或 `docker service update` 上的 `-p` 或 `--publish` 标志发布该端口。支持旧的冒号分隔语法和新的逗号分隔值语法。首选较长的语法，因为它具有一定的自描述性。

<table>
<thead>
<tr>
<th>标志值</th>
<th>描述</th>
</tr>
</thead>
<tr>
<td><tt>-p 8080:80</tt> 或<br /><tt>-p published=8080,target=80</tt></td>
<td>将服务上的 TCP 端口 80 映射到路由网格上的端口 8080。</td>
</tr>
<tr>
<td><tt>-p 8080:80/udp</tt> 或<br /><tt>-p published=8080,target=80,protocol=udp</tt></td>
<td>将服务上的 UDP 端口 80 映射到路由网格上的端口 8080。</td>
</tr>
<tr>
<td><tt>-p 8080:80/tcp -p 8080:80/udp</tt> 或 <br /><tt>-p published=8080,target=80,protocol=tcp -p published=8080,target=80,protocol=udp</tt></td>
<td>将服务上的 TCP 端口 80 映射到路由网格上的 TCP 端口 8080，并将服务上的 UDP 端口 80 映射到路由网格上的 UDP 端口 8080。</td>
</tr>
</table>

## 了解更多

* [将服务部署到 swarm](services.md)
* [Swarm 管理指南](admin_guide.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)
* [网络概述](/manuals/engine/network/_index.md)
* [Docker CLI 参考](/reference/cli/docker/)