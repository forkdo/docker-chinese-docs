---
description: 使用 Swarm 模式的覆盖网络功能
keywords: swarm, networking, ingress, overlay, service discovery
title: 管理 Swarm 服务网络
toc_max: 3
---

本文档描述了 Swarm 服务的网络功能。

## Swarm 和流量类型

Docker Swarm 生成两种不同类型的流量：

- 控制和管理平面流量：包括 Swarm 管理消息，例如加入或离开 Swarm 的请求。此流量始终被加密。

- 应用数据平面流量：包括容器流量以及与外部客户端之间的流量。

## 关键网络概念

以下三个网络概念对 Swarm 服务很重要：

- 覆盖网络（Overlay networks）管理参与 Swarm 的 Docker 守护进程之间的通信。您可以像创建独立容器的用户自定义网络一样创建覆盖网络。您也可以将服务连接到一个或多个现有的覆盖网络，以实现服务间通信。覆盖网络是使用 `overlay` 网络驱动的 Docker 网络。

- `ingress` 网络是一个特殊的覆盖网络，用于在服务的节点之间实现负载均衡。当任何 Swarm 节点在已发布的端口上接收到请求时，它将该请求传递给一个名为 `IPVS` 的模块。`IPVS` 跟踪参与该服务的所有 IP 地址，选择其中一个，并通过 `ingress` 网络将请求路由到该地址。

  `ingress` 网络在初始化或加入 Swarm 时自动创建。大多数用户不需要自定义其配置，但 Docker 允许您这样做。

- `docker_gwbridge` 是一个桥接网络，将覆盖网络（包括 `ingress` 网络）连接到单个 Docker 守护进程的物理网络。默认情况下，服务运行的每个容器都连接到其本地 Docker 守护进程主机的 `docker_gwbridge` 网络。

  `docker_gwbridge` 网络在初始化或加入 Swarm 时自动创建。大多数用户不需要自定义其配置，但 Docker 允许您这样做。

> [!TIP]
>
> 有关 Swarm 网络的更多详细信息，请参阅 [网络概述](/manuals/engine/network/_index.md)。

## 防火墙注意事项

参与 Swarm 的 Docker 守护进程需要能够通过以下端口相互通信：

* 端口 `7946` TCP/UDP 用于容器网络发现。
* 端口 `4789` UDP（可配置）用于覆盖网络（包括 ingress）数据路径。

设置 Swarm 网络时应特别小心。请参阅 [教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts) 了解概述。

## 覆盖网络

当您初始化 Swarm 或将 Docker 主机加入现有 Swarm 时，会在该 Docker 主机上创建两个新网络：

- 一个名为 `ingress` 的覆盖网络，用于处理与 Swarm 服务相关的控制和数据流量。当您创建 Swarm 服务且未将其连接到用户自定义覆盖网络时，它默认连接到 `ingress` 网络。
- 一个名为 `docker_gwbridge` 的桥接网络，将各个 Docker 守护进程连接到参与 Swarm 的其他守护进程。

### 创建覆盖网络

要创建覆盖网络，在使用 `docker network create` 命令时指定 `overlay` 驱动：

```console
$ docker network create \
  --driver overlay \
  my-network
```

上述命令未指定任何自定义选项，因此 Docker 分配子网并使用默认选项。您可以使用 `docker network inspect` 查看网络信息。

当没有容器连接到覆盖网络时，其配置并不令人兴奋：

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

在上述输出中，请注意驱动是 `overlay`，作用域是 `swarm`，而不是您可能在其他类型 Docker 网络中看到的 `local`、`host` 或 `global` 作用域。此作用域表示只有参与 Swarm 的主机才能访问此网络。

当服务首次连接到网络时，网络的子网和网关会动态配置。以下示例显示了与上述相同的网络，但有三个 `redis` 服务的容器连接到它。

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

在某些情况下，您可能不想使用覆盖网络的默认配置。有关可配置选项的完整列表，请运行命令 `docker network create --help`。以下是其中一些最常更改的选项。

#### 配置子网和网关

默认情况下，当第一个服务连接到网络时，网络的子网和网关会自动配置。您可以在创建网络时使用 `--subnet` 和 `--gateway` 标志配置这些。以下示例扩展了前面的示例，通过配置子网和网关。

```console
$ docker network create \
  --driver overlay \
  --subnet 10.0.9.0/24 \
  --gateway 10.0.9.99 \
  my-network
```

##### 使用自定义默认地址池

要自定义 Swarm 网络的子网分配，您可以在 `swarm init` 期间[选择性配置它们](swarm-mode.md)。

例如，初始化 Swarm 时使用以下命令：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 26
```

每当用户创建网络但未使用 `--subnet` 命令行选项时，该网络的子网将从池中的下一个可用子网顺序分配。如果指定的网络已被分配，该网络将不会用于 Swarm。

如果需要不连续的地址空间，可以配置多个池。但是，不支持从特定池分配。网络子网将从 IP 池空间顺序分配，当从删除的网络中解除分配时，子网将被重用。

可以配置默认掩码长度，它对所有网络都相同。默认设置为 `/24`。要更改默认子网掩码长度，请使用 `--default-addr-pool-mask-length` 命令行选项。

> [!NOTE]
>
> 默认地址池只能在 `swarm init` 时配置，集群创建后无法更改。

##### 覆盖网络大小限制

Docker 建议使用 `/24` 块创建覆盖网络。`/24` 覆盖网络块将网络限制为 256 个 IP 地址。

此建议解决了 [Swarm 模式的限制](https://github.com/moby/moby/issues/30820)。如果您需要超过 256 个 IP 地址，不要增加 IP 块大小。您可以对具有外部负载均衡器的服务使用 `dnsrr` 端点模式，或使用多个较小的覆盖网络。有关不同端点模式的更多信息，请参阅 [配置服务发现](#configure-service-discovery)。

#### 配置应用数据加密 {#encryption}

与 Swarm 相关的管理和控制平面数据始终被加密。有关加密机制的更多详细信息，请参阅 [Docker Swarm 模式覆盖网络安全模型](/manuals/engine/network/drivers/overlay.md)。

Swarm 节点之间的应用数据默认不加密。要在给定覆盖网络上加密此流量，请在 `docker network create` 上使用 `--opt encrypted` 标志。这在 vxlan 级别启用 IPSEC 加密。此加密会带来显著的性能损失，因此在生产环境中使用此选项之前应先进行测试。

> [!NOTE]
>
> 您必须 [自定义自动创建的 ingress](#customize-ingress) 以启用加密。默认情况下，所有 ingress 流量都是未加密的，因为加密是网络级选项。

## 将服务附加到覆盖网络

要将服务附加到现有覆盖网络，请在 `docker service create` 上传递 `--network` 标志，或在 `docker service update` 上传递 `--network-add` 标志。

```console
$ docker service create \
  --replicas 3 \
  --name my-web \
  --network my-network \
  nginx
```

连接到覆盖网络的服务容器可以通过它相互通信。

要查看服务连接到哪些网络，请使用 `docker service ls` 找到服务名称，然后使用 `docker service ps <service-name>` 列出网络。或者，要查看哪些服务的容器连接到网络，请使用 `docker network inspect <network-name>`。您可以从加入 Swarm 且处于 `running` 状态的任何 Swarm 节点运行这些命令。

### 配置服务发现

服务发现是 Docker 用于将服务外部客户端的请求路由到单个 Swarm 节点的机制，而客户端不需要知道有多少节点参与服务或它们的 IP 地址或端口。您不需要发布在同一网络上的服务之间使用的端口。例如，如果您有一个 [将数据存储在 MySQL 服务中的 WordPress 服务](https://training.play-with-docker.com/swarm-service-discovery/)，并且它们连接到同一覆盖网络，您不需要向客户端发布 MySQL 端口，只需发布 WordPress HTTP 端口。

服务发现可以通过两种不同的方式工作：使用嵌入式 DNS 和虚拟 IP (VIP) 在第 3 层和第 4 层进行内部基于连接的负载均衡，或使用 DNS 轮询 (DNSRR) 在第 7 层进行外部和自定义基于请求的负载均衡。您可以按服务配置此设置。

- 默认情况下，当您将服务连接到网络且该服务发布一个或多个端口时，Docker 会为该服务分配一个虚拟 IP (VIP)，这是客户端访问服务的“前端”。Docker 维护服务中所有工作节点的列表，并在客户端和其中一个节点之间路由请求。来自客户端的每个请求可能被路由到不同的节点。

- 如果您配置服务使用 DNS 轮询 (DNSRR) 服务发现，则没有单个虚拟 IP。相反，Docker 为服务设置 DNS 条目，使得对服务名称的 DNS 查询返回 IP 地址列表，客户端直接连接到其中一个。

  DNS 轮询在您想要使用自己的负载均衡器（如 HAProxy）的情况下很有用。要配置服务使用 DNSRR，请在创建新服务或更新现有服务时使用 `--endpoint-mode dnsrr` 标志。

## 自定义 ingress 网络 {#customize-ingress}

大多数用户永远不需要配置 `ingress` 网络，但 Docker 允许您这样做。如果自动选择的子网与您网络上已存在的子网冲突，或者您需要自定义其他低级网络设置（如 MTU），或者您想要 [启用加密](#encryption)，这可能很有用。

自定义 `ingress` 网络涉及删除并重新创建它。这通常在您在 Swarm 中创建任何服务之前完成。如果您有发布端口的现有服务，这些服务需要在删除 `ingress` 网络之前被删除。

在没有 `ingress` 网络存在的时间内，未发布端口的现有服务继续运行但不进行负载均衡。这会影响发布端口的服务，例如发布端口 80 的 WordPress 服务。

1.  使用 `docker network inspect ingress` 检查 `ingress` 网络，并删除连接到它的任何服务。这些是发布端口的服务，例如发布端口 80 的 WordPress 服务。如果所有此类服务未停止，下一步将失败。

2.  删除现有的 `ingress` 网络：

    ```console
    $ docker network rm ingress

    WARNING! Before removing the routing-mesh network, make sure all the nodes
    in your swarm run the same docker engine version. Otherwise, removal may not
    be effective and functionality of newly created ingress networks will be
    impaired.
    Are you sure you want to continue? [y/N]
    ```

3.  使用 `--ingress` 标志以及您要设置的自定义选项创建新的覆盖网络。此示例将 MTU 设置为 1200，将子网设置为 `10.11.0.0/16`，并将网关设置为 `10.11.0.2`。

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
    > 您可以将 `ingress` 网络命名为除 `ingress` 之外的其他名称，但您只能有一个。尝试创建第二个将失败。

4.  重新启动您在第一步中停止的服务。

## 自定义 docker_gwbridge

`docker_gwbridge` 是一个虚拟桥接，将覆盖网络（包括 `ingress` 网络）连接到单个 Docker 守护进程的物理网络。Docker 在您初始化 Swarm 或将 Docker 主机加入 Swarm 时自动创建它，但它不是 Docker 设备。它存在于 Docker 主机的内核中。如果您需要自定义其设置，必须在将 Docker 主机加入 Swarm 之前或暂时将其从 Swarm 中移除之后进行。

您需要在操作系统上安装 `brctl` 应用程序才能删除现有桥接。包名是 `bridge-utils`。

1.  停止 Docker。

2.  使用 `brctl show docker_gwbridge` 命令检查是否存在名为 `docker_gwbridge` 的桥接设备。如果存在，请使用 `brctl delbr docker_gwbridge` 删除它。

3.  启动 Docker。不要加入或初始化 Swarm。

4.  使用您的自定义设置创建或重新创建 `docker_gwbridge` 