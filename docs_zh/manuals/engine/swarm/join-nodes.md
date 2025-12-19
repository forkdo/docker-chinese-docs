---
description: 将 worker 和 manager 节点加入到一个 swarm 中
keywords: guide, swarm mode, node
title: 将节点加入到一个 swarm 中
---

当您初次创建一个 swarm 时，您会将单个 Docker Engine 置于 Swarm 模式。为了充分利用 Swarm 模式，您可以将节点添加到该 swarm 中：

* 添加 worker 节点可以增加容量。当您向一个 swarm 部署服务时，引擎会在可用节点（无论是 worker 节点还是 manager 节点）上调度任务。当您向您的 swarm 添加 worker 时，您就增加了处理任务的 swarm 规模，而不会影响 manager 的 raft 共识。
* Manager 节点可以提高容错性。Manager 节点为 swarm 执行编排和集群管理功能。在 manager 节点中，一个单一的 leader 节点负责执行编排任务。如果一个 leader 节点宕机，其余的 manager 节点将选举一个新的 leader 并恢复对 swarm 状态的编排和维护。默认情况下，manager 节点也运行任务。

Docker Engine 会根据您提供给 `docker swarm join` 命令的 **join-token** 来加入 swarm。节点仅在加入时使用该令牌。如果您后续轮换了该令牌，这不会影响现有的 swarm 节点。请参阅[在 Swarm 模式下运行 Docker Engine](swarm-mode.md#view-the-join-command-or-update-a-swarm-join-token)。

## 作为 worker 节点加入

要获取包含用于 worker 节点的 join token 的加入命令，请在 manager 节点上运行以下命令：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

在 worker 上运行输出中的命令以加入 swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

This node joined a swarm as a worker.
```

`docker swarm join` 命令会执行以下操作：

* 将当前节点上的 Docker Engine 切换到 Swarm 模式。
* 从 manager 请求一个 TLS 证书。
* 使用机器的主机名为节点命名。
* 基于 swarm token 将当前节点加入 manager 监听地址处的 swarm。
* 将当前节点设置为 `Active` 可用性，意味着它可以接收调度器分配的任务。
* 将 `ingress` 覆盖网络扩展到当前节点。

## 作为 manager 节点加入

当您运行 `docker swarm join` 并传入 manager token 时，Docker Engine 会像 worker 一样切换到 Swarm 模式。Manager 节点也参与 raft 共识。新节点应该是 `Reachable` 状态，但现有的 manager 仍然是该 swarm 的 `Leader`。

为实现高可用性，Docker 建议每个集群配置三个或五个 manager 节点。由于 Swarm 模式下的 manager 节点使用 Raft 共享数据，因此 manager 节点的数量必须是奇数。只要超过半数的 manager 节点可用（即达到法定人数），swarm 就可以继续运行。

有关 swarm manager 和 swarm 管理的更多详细信息，请参阅[管理和维护 Docker Engine 集群](admin_guide.md)。

要获取包含用于 manager 节点的 join token 的加入命令，请在 manager 节点上运行以下命令：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
    192.168.99.100:2377
```

在新的 manager 节点上运行输出中的命令以将其加入 swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
  192.168.99.100:2377

This node joined a swarm as a manager.
```

## 了解更多

* `swarm join` [命令行参考](/reference/cli/docker/swarm/join.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)