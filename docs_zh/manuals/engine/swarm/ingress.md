---
description: 使用路由网格将服务发布到集群外部
keywords: 指南, 集群模式, swarm, 网络, ingress, 路由网格
title: 使用集群模式路由网格
---

Docker Engine 集群模式可以轻松地为服务发布端口，使其对集群外部的资源可用。所有节点都参与 ingress 路由网格。路由网格使集群中的每个节点都能接受发布端口上的连接，即使该节点上没有运行任何任务。路由网格会将所有进入发布端口的请求路由到可用节点上的活动容器。

要在集群中使用 ingress 网络，需要在启用集群模式之前，在集群节点之间开放以下端口：

* 端口 `7946` TCP/UDP，用于容器网络发现。
* 端口 `4789` UDP（可配置），用于容器 ingress 网络。

在 Swarm 中设置网络时应格外小心。请查阅[教程](swarm-tutorial/_index.md#open-protocols-and-ports-between-the-hosts)以获取概述。

您还必须在集群节点和任何需要访问该端口的外部资源（例如外部负载均衡器）之间开放已发布的端口。

您也可以为特定服务[绕过路由网格](#bypass-the-routing-mesh)。

## 为服务发布端口

在创建服务时，使用 `--publish` 标志来发布端口。`target` 用于指定容器内部的端口，`published` 用于指定在路由网格上绑定的端口。如果省略 `published` 端口，则会为每个服务任务绑定一个随机的高位端口。您需要检查任务以确定端口。

```console
$ docker service create \
  --name <服务名称> \
  --publish published=<已发布端口>,target=<容器端口> \
  <镜像>
```

> [!NOTE]
>
> 此语法的旧形式是冒号分隔的字符串，其中已发布端口在前，目标端口在后，例如 `-p 8080:80`。首选新语法，因为它更易于阅读且允许更大的灵活性。

`<已发布端口>` 是集群使服务可用的端口。如果省略，则绑定一个随机的高位端口。
`<容器端口>` 是容器侦听的端口。此参数是必需的。

例如，以下命令将 nginx 容器中的端口 80 发布到集群中任何节点的端口 8080：

```console
$ docker service create \
  --name my-web \
  --publish published=8080,target=80 \
  --replicas 2 \
  nginx
```

当您访问任何节点上的端口 8080 时，Docker 会将您的请求路由到一个活动容器。在集群节点本身上，端口 8080 可能并未实际绑定，但路由网格知道如何路由流量并防止任何端口冲突发生。

路由网格侦听分配给节点的任何 IP 地址上的已发布端口。对于外部可路由的 IP 地址，该端口可从主机外部访问。对于所有其他 IP 地址，访问仅在主机内部可用。

![服务 ingress 图像](images/ingress-routing-mesh.webp)

您可以使用以下命令为现有服务发布端口：

```console
$ docker service update \
  --publish-add published=<已发布端口>,target=<容器端口> \
  <服务>
```

您可以使用 `docker service inspect` 查看服务的已发布端口。例如：

```console
$ docker service inspect --format="{{json .Endpoint.Spec.Ports}}" my-web

[{"Protocol":"tcp","TargetPort":80,"PublishedPort":8080}]
```

输出显示容器的 `<容器端口>`（标记为 `TargetPort`）以及节点侦听服务请求的 `<已发布端口>`（标记为 `PublishedPort`）。

### 仅发布 TCP 或 UDP 端口

默认情况下，发布端口时，它是 TCP 端口。您可以专门发布 UDP 端口来代替 TCP 端口或与 TCP 端口一起发布。当您同时发布 TCP 和 UDP 端口时，如果省略协议说明符，则该端口将作为 TCP 端口发布。如果使用较长的语法（推荐），请将 `protocol` 键设置为 `tcp` 或 `udp`。

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

默认情况下，发布端口的集群服务使用路由网格。当您连接到任何集群节点上已发布的端口（无论该节点是否正在运行给定服务）时，您都会被透明地重定向到正在运行该服务的工作人员。实际上，Docker 充当了集群服务的负载均衡器。

您可以绕过路由网格，这样当您访问给定节点上绑定的端口时，您始终访问的是该节点上运行的服务实例。这被称为 `host` 模式。有几件事需要记住。

- 如果您访问的节点没有运行服务任务，则该服务不会侦听该端口。可能没有任何东西在侦听，或者一个完全不同的应用程序在侦听。

- 如果您期望在每个节点上运行多个服务任务（例如，当您有 5 个节点但运行 10 个副本时），您不能指定静态目标端口。要么允许 Docker 分配一个随机的高位端口（通过省略 `published`），要么确保在给定节点上只运行一个服务实例，方法是使用全局服务而不是复制服务，或者使用放置约束。

要绕过路由网格，必须使用长格式的 `--publish` 服务并将 `mode` 设置为 `host`。如果省略 `mode` 键或将其设置为 `ingress`，则使用路由网格。以下命令创建一个使用 `host` 模式并绕过路由网格的全局服务。

```console
$ docker service create --name dns-cache \
  --publish published=53,target=53,protocol=udp,mode=host \
  --mode global \
  dns-cache
```

## 配置外部负载均衡器

您可以为集群服务配置外部负载均衡器，可以与路由网格结合使用，也可以完全不使用路由网格。

### 使用路由网格

您可以配置外部负载均衡器将请求路由到集群服务。例如，您可以配置 [HAProxy](https://www.haproxy.org) 来平衡对发布到端口 8080 的 nginx 服务的请求。

![带有外部负载均衡器的 Ingress 图像](images/ingress-lb.webp)

在这种情况下，负载均衡器和集群节点之间必须开放端口 8080。集群节点可以驻留在代理服务器可访问的私有网络上，但该网络不能公开访问。

您可以配置负载均衡器在集群中的每个节点之间平衡请求，即使该节点上没有安排任何任务。例如，您可以在 `/etc/haproxy/haproxy.cfg` 中进行以下 HAProxy 配置：

```bash
global
        log /dev/log    local0
        log /dev/log    local1 notice
...snip...

# 配置 HAProxy 在端口 80 上侦听
frontend http_front
   bind *:80
   stats uri /haproxy?stats
   default_backend http_back

# 配置 HAProxy 将请求路由到端口 8080 上的集群节点
backend http_back
   balance roundrobin
   server node1 192.168.99.100:8080 check
   server node2 192.168.99.101:8080 check
   server node3 192.168.99.102:8080 check
```

当您访问端口 80 上的 HAProxy 负载均衡器时，它会将请求转发到集群中的节点。集群路由网格将请求路由到活动任务。如果由于某种原因集群调度器将任务分派到不同的节点，您不需要重新配置负载均衡器。

您可以配置任何类型的负载均衡器将请求路由到集群节点。要了解有关 HAProxy 的更多信息，请参阅 [HAProxy 文档](https://cbonte.github.io/haproxy-dconv/)。

### 不使用路由网格

要在不使用路由网格的情况下使用外部负载均衡器，请将 `--endpoint-mode` 设置为 `dnsrr`，而不是默认值 `vip`。在这种情况下，没有单一的虚拟 IP。相反，Docker 会为服务设置 DNS 条目，使得对服务名称的 DNS 查询返回 IP 地址列表，客户端直接连接到其中之一。

您不能将 `--endpoint-mode dnsrr` 与 `--publish mode=ingress` 一起使用。您必须在服务前面运行自己的负载均衡器。在 Docker 主机上对服务名称的 DNS 查询会返回运行该服务的节点的 IP 地址列表。配置您的负载均衡器以使用此列表并在节点之间平衡流量。
请参阅[配置服务发现](networking.md#configure-service-discovery)。

## 了解更多

* [将服务部署到集群](services.md)