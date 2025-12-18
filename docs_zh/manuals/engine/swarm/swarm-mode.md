---
description: 在 Swarm 模式下运行 Docker 引擎
keywords: 指南, Swarm 模式, 节点, Docker 引擎
title: 在 Swarm 模式下运行 Docker 引擎
---

当你首次安装并开始使用 Docker 引擎时，Swarm 模式默认是禁用的。当你启用 Swarm 模式后，就可以通过 `docker service` 命令来管理工作负载的概念。

有两种方式可以在 Swarm 模式下运行引擎：

* 创建一个新 Swarm，本文将介绍此方法。
* [加入现有 Swarm](join-nodes.md)。

当你在本地机器上以 Swarm 模式运行引擎时，你可以基于自己创建的镜像或其他可用镜像来创建和测试服务。在生产环境中，Swarm 模式提供了一个具备集群管理功能的容错平台，以保持你的服务持续运行并可用。

这些说明假设你已经在一台机器上安装了 Docker 引擎，该机器将作为你 Swarm 的管理节点。

如果你尚未阅读，请先了解 [Swarm 模式关键概念](key-concepts.md)，并尝试 [Swarm 模式教程](swarm-tutorial/_index.md)。

## 创建一个 Swarm

运行创建 Swarm 的命令时，Docker 引擎将开始以 Swarm 模式运行。

运行 [`docker swarm init`](/reference/cli/docker/swarm/init.md) 在当前节点上创建一个单节点 Swarm。引擎按以下方式设置 Swarm：

* 将当前节点切换到 Swarm 模式。
* 创建一个名为 `default` 的 Swarm。
* 指定当前节点为 Swarm 的领导者管理节点。
* 使用机器主机名命名节点。
* 配置管理节点在活跃网络接口的 `2377` 端口上监听。
* 将当前节点设置为 `Active` 可用性状态，表示它可以接收调度器分配的任务。
* 启动一个内部分布式数据存储，供参与 Swarm 的引擎维护 Swarm 及其上所有服务的一致视图。
* 默认情况下，为 Swarm 生成自签名根 CA。
* 默认情况下，生成工作节点和管理节点加入 Swarm 的令牌。
* 创建一个名为 `ingress` 的覆盖网络，用于发布 Swarm 外部的服务端口。
* 为你的网络创建覆盖网络的默认 IP 地址和子网掩码。

`docker swarm init` 的输出提供了将新工作节点加入 Swarm 时使用的连接命令：

```console
$ docker swarm init
Swarm initialized: current node (dxn1zf6l61qsb1josjja83ngz) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

### 配置默认地址池

默认情况下，Swarm 模式使用默认地址池 `10.0.0.0/8` 作为全局作用域（覆盖）网络。每个未指定子网的网络将从该地址池中顺序分配一个子网。在某些情况下，可能需要为网络使用不同的默认 IP 地址池。

例如，如果默认的 `10.0.0.0/8` 范围与你网络中已分配的地址空间冲突，那么最好确保网络使用不同的范围，而无需 Swarm 用户通过 `--subnet` 命令显式指定每个子网。

要配置自定义默认地址池，必须在 Swarm 初始化时使用 `--default-addr-pool` 命令行选项定义池。此命令行选项使用 CIDR 表示法定义子网掩码。要为 Swarm 创建自定义地址池，你必须至少定义一个默认地址池，以及一个可选的默认地址池子网掩码。例如，对于 `10.0.0.0/27`，使用值 `27`。

Docker 从 `--default-addr-pool` 选项指定的地址范围中分配子网地址。例如，命令行选项 `--default-addr-pool 10.10.0.0/16` 表示 Docker 将从该 `/16` 地址范围中为子网分配地址。如果 `--default-addr-pool-mask-len` 未指定或显式设置为 24，则会从该 `default-addr-pool` 范围内创建 256 个 `/24` 网络，形式为 `10.10.X.0/24`。

子网范围来自 `--default-addr-pool`（例如 `10.10.0.0/16`）。其中 16 表示可以在该 `default-addr-pool` 范围内创建的网络数量。`--default-addr-pool` 选项可以多次出现，每次选项提供 Docker 用于覆盖子网的额外地址。

命令格式为：

```console
$ docker swarm init --default-addr-pool <CIDR 格式的 IP 范围> [--default-addr-pool <CIDR 格式的 IP 范围> --default-addr-pool-mask-length <CIDR 值>]
```

创建默认 IP 地址池，使用 `/16`（B 类）作为 `10.20.0.0` 网络的命令如下：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16
```

创建默认 IP 地址池，使用 `/16`（B 类）作为 `10.20.0.0` 和 `10.30.0.0` 网络，并为每个网络创建 `/26` 子网掩码的命令如下：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool 10.30.0.0/16 --default-addr-pool-mask-length 26
```

在此示例中，`docker network create -d overlay net1` 将导致 `net1` 分配子网 `10.20.0.0/26`，而 `docker network create -d overlay net2` 将导致 `net2` 分配子网 `10.20.0.64/26`。此过程持续进行，直到所有子网耗尽。

更多信息请参考以下页面：
- [Swarm 网络](./networking.md) 了解默认地址池使用的更多详情
- `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md) 了解 `--default-addr-pool` 标志的更多细节。

### 配置通告地址

管理节点使用通告地址允许 Swarm 中的其他节点访问 Swarmkit API 和覆盖网络。Swarm 中的其他节点必须能够通过其通告地址访问管理节点。

如果你未指定通告地址，Docker 会检查系统是否具有单个 IP 地址。如果有，Docker 默认使用该 IP 地址和监听端口 `2377`。如果系统有多个 IP 地址，你必须指定正确的 `--advertise-addr` 以启用管理节点间通信和覆盖网络：

```console
$ docker swarm init --advertise-addr <MANAGER-IP>
```

如果你首次添加的管理节点可被其他节点访问的地址，与该管理节点自身看到的地址不同，你也必须指定 `--advertise-addr`。例如，在跨越不同区域的云环境中，主机既有区域内访问的内部地址，也有区域外访问的外部地址。在这种情况下，使用 `--advertise-addr` 指定外部地址，以便节点可以将该信息传播给后续连接的其他节点。

更多关于通告地址的详细信息，请参考 `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md)。

### 查看加入命令或更新 Swarm 加入令牌

节点需要一个密钥令牌才能加入 Swarm。工作节点的令牌与管理节点的令牌不同。节点仅在加入 Swarm 时使用加入令牌。在节点已加入 Swarm 后轮换加入令牌不会影响该节点的 Swarm 成员身份。令牌轮换确保旧令牌不能被任何尝试加入 Swarm 的新节点使用。

要检索包含工作节点加入令牌的加入命令，请运行：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

This node joined a swarm as a worker.
```

要查看管理节点的加入命令和令牌，请运行：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-59egwe8qangbzbqb3ryawxzk3jn97ifahlsrw01yar60pmkr90-bdjfnkcflhooyafetgjod97sz \
    192.168.99.100:2377
```

传递 `--quiet` 标志仅打印令牌：

```console
$ docker swarm join-token --quiet worker

SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c
```

请小心保管加入令牌，因为它们是加入 Swarm 所需的密钥。特别是，将密钥检入版本控制系统是不好的做法，因为它允许任何访问应用程序源代码的人向 Swarm 添加新节点。管理令牌尤其敏感，因为它们允许新的管理节点加入并控制整个 Swarm。

我们建议在以下情况下轮换加入令牌：

* 如果令牌意外检入版本控制系统、群聊或意外打印到日志中。
* 如果你怀疑某个节点已被攻破。
* 如果你希望确保没有新节点可以加入 Swarm。

此外，实施定期轮换计划（包括 Swarm 加入令牌在内的任何密钥）是最佳实践。我们建议至少每 6 个月轮换一次令牌。

运行 `swarm join-token --rotate` 以使旧令牌失效并生成新令牌。指定你要轮换的是 `worker` 还是 `manager` 节点的令牌：

```console
$ docker swarm join-token  --rotate worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-2kscvs0zuymrsc9t0ocyy1rdns9dhaodvpl639j2bqx55uptag-ebmn5u927reawo27s3azntd44 \
    192.168.99.100:2377
```

## 了解更多

* [将节点加入 Swarm](join-nodes.md)
* `swarm init` [命令行参考](/reference/cli/docker/swarm/init.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)