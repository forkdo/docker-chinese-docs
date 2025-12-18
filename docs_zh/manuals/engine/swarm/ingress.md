---
description: 使用路由网格将 Swarm 服务对外发布
keywords: guide, swarm mode, swarm, network, ingress, routing mesh
title: 使用 Swarm 模式路由网格
---

Docker Engine 的 Swarm 模式使得发布服务端口变得简单，让服务可以被 Swarm 外部的资源访问。所有节点都参与一个入口路由网格（ingress routing mesh）。路由网格允许 Swarm 中的每个节点在接受到任何运行在 Swarm 中的服务的已发布端口上的连接请求时进行处理，即使该节点上没有运行任务。路由网格将所有发往已发布端口的入站请求路由到可用的容器上。

要在 Swarm 中使用入口网络，您需要在启用 Swarm 模式之前，在 Swarm 节点之间开放以下端口：

* 端口 `7946` TCP/UDP，用于容器网络发现。
* 端口 `4789` UDP（可配置），用于容器入口网络。

在 Swarm 中设置网络时，需要特别注意。请参考 [教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts) 了解概述。

您还必须在 Swarm 节点与任何外部资源（如外部负载均衡器）之间开放已发布的端口，这些资源需要访问该端口。

您也可以为特定服务[绕过路由网格](#bypass-the-routing-mesh)。

## 为服务发布端口

创建服务时使用 `--publish` 标志来发布端口。使用 `target` 指定容器内的端口，使用 `published` 指定要在路由网格上绑定的端口。如果您省略 `published` 端口，每个服务任务会绑定一个随机的高位端口。您需要检查任务以确定端口。

```console
$ docker service create \
  --name <SERVICE-NAME> \
  --publish published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  <IMAGE>
```

> [!NOTE]
>
> 此语法的旧形式是冒号分隔的字符串，其中发布的端口在前，目标端口在后，例如 `-p 8080:80`。新语法更受推荐，因为它更易读且提供了更多灵活性。

`<PUBLISHED-PORT>` 是 Swarm 使服务可用的端口。如果您省略它，会绑定一个随机的高位端口。`<CONTAINER-PORT>` 是容器监听的端口。此参数是必需的。

例如，以下命令将 nginx 容器中的端口 80 发布到 Swarm 中任意节点的端口 8080：

```console
$ docker service create \
  --name my-web \
  --publish published=8080,target=80 \
  --replicas 2 \
  nginx
```

当您访问 Swarm 中任意节点的端口 8080 时，Docker 会将您的请求路由到活跃的容器。在 Swarm 节点本身上，端口 8080 可能实际上并未绑定，但路由网格知道如何路由流量并防止任何端口冲突。

路由网格监听节点上分配的任意 IP 地址的已发布端口。对于可外部路由的 IP 地址，该端口可从主机外部访问。对于所有其他 IP 地址，访问仅限于主机内部。

![Service ingress image](images/ingress-routing-mesh.webp)

您可以使用以下命令为现有服务发布端口：

```console
$ docker service update \
  --publish-add published=<PUBLISHED-PORT>,target=<CONTAINER-PORT> \
  <SERVICE>
```

您可以使用 `docker service inspect` 查看服务的已发布端口。例如：

```console
$ docker service inspect --format="{{json .Endpoint.Spec.Ports}}" my-web

[{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080}]
```

输出显示了来自容器的 `<CONTAINER-PORT>`（标记为 `TargetPort`）和节点监听请求的服务的 `<PUBLISHED-PORT>`（标记为 `PublishedPort`）。

### 仅为 TCP 或仅为 UDP 发布端口

默认情况下，当您发布端口时，它是 TCP 端口。您可以专门发布 UDP 端口，而不是或除了 TCP 端口之外。当您同时发布 TCP 和 UDP 端口时，如果您省略协议说明符，端口将作为 TCP 端口发布。如果您使用更长的语法（推荐），将 `protocol` 键设置为 `tcp` 或 `udp`。

#### 仅 TCP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  dns-cache
```

#### TCP 和 UDP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53 \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53 \
  -p 53:53/udp \
  dns-cache
```

#### 仅 UDP

长语法：

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp \
  dns-cache
```

短语法：

```console
$ docker service create --name dns-cache \
  -p 53:53/udp \
  dns-cache
```

## 绕过路由网格

默认情况下，发布端口的 Swarm 服务使用路由网格。当您连接到任意 Swarm 节点的已发布端口时（无论它是否运行给定服务），您都会被重定向到运行该服务的工作节点，这是透明的。实际上，Docker 充当了您 Swarm 服务的负载均衡器。

您可以绕过路由网格，这样当您访问特定节点的绑定端口时，您总是访问运行在该节点上的服务实例。这被称为 `host` 模式。有几点需要注意。

- 如果您访问的节点未运行服务任务，该服务不会监听该端口。可能没有任何内容在监听，或者完全不同的应用程序在监听。

- 如果您期望在每个节点上运行多个服务任务（例如，当您有 5 个节点但运行 10 个副本时），您不能指定静态目标端口。要么允许 Docker 分配一个随机的高位端口（通过省略 `published`），要么通过使用全局服务而不是复制服务，或使用位置约束，确保给定节点上只运行服务的单个实例。

要绕过路由网格，您必须使用长 `--publish` 服务并将 `mode` 设置为 `host`。如果您省略 `mode` 键或将其设置为 `ingress`，则使用路由网格。以下命令创建一个使用 `host` 模式并绕过路由网格的全局服务。

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp,mode=host \
  --mode global \
  dns-cache
```

## 配置外部负载均衡器

您可以为 Swarm 服务配置外部负载均衡器，可以与路由网格结合使用，也可以完全不使用路由网格。

### 使用路由网格

您可以配置外部负载均衡器将请求路由到 Swarm 服务。例如，您可以配置 [HAProxy](https://www.haproxy.org) 来平衡发布到端口 8080 的 nginx 服务的请求。

![Ingress with external load balancer image](images/ingress-lb.webp)

在这种情况下，负载均衡器和 Swarm 节点之间必须开放端口 8080。Swarm 节点可以位于对代理服务器可访问但不可公开访问的私有网络上。

您可以配置负载均衡器在每个 Swarm 节点之间平衡请求，即使节点上没有调度任务。例如，您可以在 `/etc/haproxy/haproxy.cfg` 中配置如下 HAProxy：

```bash
global
        log /dev/log    local0
        log /dev/log    local1 notice
...snip...

# 配置 HAProxy 在端口 80 上监听
frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

# 配置 HAProxy 将请求路由到端口 8080 上的 Swarm 节点
backend http_back
   balance roundrobin
   server node1 192.168.99.100:8080 check
   server node2 192.168.99.101:8080 check
   server node3 192.168.99.102:8080 check
```

当您在端口 80 上访问 HAProxy 负载均衡器时，它会将请求转发到 Swarm 节点。Swarm 路由网格将请求路由到活跃任务。如果由于任何原因 Swarm 调度器将任务调度到不同的节点，您无需重新配置负载均衡器。

您可以配置任意类型的负载均衡器将请求路由到 Swarm 节点。要了解更多关于 HAProxy 的信息，请参阅 [HAProxy 文档](https://cbonte.github.io/haproxy-dconv/)。

### 不使用路由网格

要在不使用路由网格的情况下使用外部负载均衡器，请将 `--endpoint-mode` 设置为 `dnsrr`，而不是默认值 `vip`。在这种情况下，没有单一的虚拟 IP。相反，Docker 为服务设置 DNS 条目，使得对服务名称的 DNS 查询返回 IP 地址列表，客户端直接连接到其中一个。

您不能将 `--endpoint-mode dnsrr` 与 `--publish mode=ingress` 一起使用。您必须在服务前面运行自己的负载均衡器。在 Docker 主机上对服务名称的 DNS 查询返回运行服务的节点的 IP 地址列表。配置您的负载均衡器以使用此列表并在节点之间平衡流量。
参见 [配置服务发现](networking.md#configure-service-discovery)。

## 了解更多

* [将服务部署到 Swarm](services.md)