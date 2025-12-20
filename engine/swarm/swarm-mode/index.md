# 在 Swarm 模式下运行 Docker Engine

首次安装并开始使用 Docker Engine 时，默认情况下 Swarm 模式是禁用的。启用 Swarm 模式后，您将使用通过 `docker service` 命令管理的服务概念。

有两种方式可以在 Swarm 模式下运行引擎：

* 创建一个新的 swarm（本文介绍）。
* [加入现有的 swarm](join-nodes.md)。

当您在本地机器上以 Swarm 模式运行引擎时，可以基于您创建的镜像或其他可用镜像来创建和测试服务。在生产环境中，Swarm 模式提供了一个具有集群管理功能的容错平台，以确保您的服务持续运行并保持可用。

这些说明假设您已经在一台机器上安装了 Docker Engine，该机器将作为 swarm 中的管理器节点。

如果您还没有这样做，请通读 [Swarm 模式关键概念](key-concepts.md) 并尝试 [Swarm 模式教程](swarm-tutorial/_index.md)。

## 创建 swarm

当您运行创建 swarm 的命令时，Docker Engine 会开始以 Swarm 模式运行。

运行 [`docker swarm init`](/reference/cli/docker/swarm/init.md) 在当前节点上创建单节点 swarm。引擎按如下方式设置 swarm：

* 将当前节点切换到 Swarm 模式。
* 创建一个名为 `default` 的 swarm。
* 指定当前节点作为 swarm 的领导者管理器节点。
* 使用机器主机名命名该节点。
* 配置管理器在端口 `2377` 上的活动网络接口进行监听。
* 将当前节点的可用性设置为 `Active`，这意味着它可以接收来自调度器的任务。
* 为参与 swarm 的引擎启动一个内部的分布式数据存储，以维护对 swarm 及其上运行的所有服务的一致视图。
* 默认情况下，为 swarm 生成自签名的根 CA。
* 默认情况下，为工作节点和管理器节点生成加入 swarm 的令牌。
* 创建一个名为 `ingress` 的覆盖网络，用于发布 swarm 外部的服务端口。
* 为您的网络创建覆盖默认 IP 地址和子网掩码。

`docker swarm init` 的输出提供了将新工作节点加入 swarm 时要使用的连接命令：

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

默认情况下，Swarm 模式使用默认地址池 `10.0.0.0/8` 用于全局范围（覆盖）网络。每个未指定子网的网络都将从该池中顺序分配一个子网。在某些情况下，可能需要为网络使用不同的默认 IP 地址池。

例如，如果默认的 `10.0.0.0/8` 范围与您网络中已分配的地址空间冲突，那么最好确保网络使用不同的范围，而无需 swarm 用户使用 `--subnet` 命令指定每个子网。

要配置自定义默认地址池，必须在 swarm 初始化时使用 `--default-addr-pool` 命令行选项定义池。此命令行选项使用 CIDR 表示法来定义子网掩码。要为 Swarm 创建自定义地址池，必须至少定义一个默认地址池，以及一个可选的默认地址池子网掩码。例如，对于 `10.0.0.0/27`，使用值 `27`。

Docker 从 `--default-addr-pool` 选项指定的地址范围分配子网地址。例如，命令行选项 `--default-addr-pool 10.10.0.0/16` 表示 Docker 将从该 `/16` 地址范围分配子网。如果 `--default-addr-pool-mask-len` 未指定或显式设置为 24，这将导致 256 个形式为 `10.10.X.0/24` 的 `/24` 网络。

子网范围来自 `--default-addr-pool`（例如 `10.10.0.0/16`）。其中的大小 16 表示可以在该 `default-addr-pool` 范围内创建的网络数量。`--default-addr-pool` 选项可以多次出现，每个选项为 docker 提供用于覆盖子网的额外地址。

命令格式如下：

```console
$ docker swarm init --default-addr-pool <IP range in CIDR> [--default-addr-pool <IP range in CIDR> --default-addr-pool-mask-length <CIDR value>]
```

为 `10.20.0.0` 网络创建具有 /16（B 类）的默认 IP 地址池的命令如下所示：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16
```

为 `10.20.0.0` 和 `10.30.0.0` 网络创建具有 `/16`（B 类）的默认 IP 地址池，并为每个网络创建 `/26` 子网掩码的命令如下所示：

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool 10.30.0.0/16 --default-addr-pool-mask-length 26
```

在此示例中，`docker network create -d overlay net1` 将导致 `10.20.0.0/26` 作为 `net1` 的分配子网，而 `docker network create -d overlay net2` 将导致 `10.20.0.64/26` 作为 `net2` 的分配子网。这种情况会一直持续，直到所有子网耗尽。

有关更多信息，请参考以下页面：
- [Swarm 网络](./networking.md) 了解更多关于默认地址池使用的信息
- `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md) 了解更多关于 `--default-addr-pool` 标志的详细信息。

### 配置通告地址

管理器节点使用通告地址允许 swarm 中的其他节点访问 Swarmkit API 和覆盖网络。Swarm 上的其他节点必须能够通过其通告地址访问管理器节点。

如果未指定通告地址，Docker 会检查系统是否只有一个 IP 地址。如果是，Docker 默认使用该 IP 地址和监听端口 `2377`。如果系统有多个 IP 地址，您必须指定正确的 `--advertise-addr` 以启用管理器间通信和覆盖网络：

```console
$ docker swarm init --advertise-addr <MANAGER-IP>
```

如果其他节点到达第一个管理器节点的地址与管理器看到的自身地址不同，也必须指定 `--advertise-addr`。例如，在跨越不同区域的云设置中，主机既有用于区域内访问的内部地址，也有用于从该区域外部访问的外部地址。在这种情况下，请使用 `--advertise-addr` 指定外部地址，以便该节点可以将该信息传播给随后连接到它的其他节点。

有关通告地址的更多详细信息，请参阅 `docker swarm init` [CLI 参考](/reference/cli/docker/swarm/init.md)。

### 查看加入命令或更新 swarm 加入令牌

节点需要一个秘密令牌才能加入 swarm。工作节点的令牌与管理器节点的令牌不同。节点仅在加入 swarm 时使用加入令牌。在节点已经加入 swarm 后轮换加入令牌不会影响该节点的 swarm 成员资格。轮换令牌可确保旧令牌不能被任何试图加入 swarm 的新节点使用。

要检索包含工作节点加入令牌的加入命令，请运行：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377

This node joined a swarm as a worker.
```

要查看管理器节点的加入命令和令牌，请运行：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-59egwe8qangbzbqb3ryawxzk3jn97ifahlsrw01yar60pmkr90-bdjfnkcflhooyafetgjod97sz \
    192.168.99.100:2377
```

传递 `--quiet` 标志以仅打印令牌：

```console
$ docker swarm join-token --quiet worker

SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c
```

请小心处理加入令牌，因为它们是加入 swarm 所必需的秘密。特别是，将秘密检入版本控制系统是一种糟糕的做法，因为它将允许任何有权访问应用程序源代码的人向 swarm 添加新节点。管理器令牌尤其敏感，因为它们允许新的管理器节点加入并获得对整个 swarm 的控制权。

我们建议在以下情况下轮换加入令牌：

* 如果令牌意外检入版本控制系统、群组聊天或意外打印到日志中。
* 如果您怀疑某个节点已遭到入侵。
* 如果您希望保证没有新节点可以加入 swarm。

此外，对包括 swarm 加入令牌在内的任何秘密实施定期轮换计划是一种最佳实践。我们建议您至少每 6 个月轮换一次令牌。

运行 `swarm join-token --rotate` 以使旧令牌失效并生成新令牌。指定您是要轮换 `worker` 还是 `manager` 节点的令牌：

```console
$ docker swarm join-token  --rotate worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-2kscvs0zuymrsc9t0ocyy1rdns9dhaodvpl639j2bqx55uptag-ebmn5u927reawo27s3azntd44 \
    192.168.99.100:2377
```

## 了解更多

* [将节点加入 swarm](join-nodes.md)
* `swarm init` [命令行参考](/reference/cli/docker/swarm/init.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)
