---
description: 将工作节点和管理节点添加到 Swarm
keywords: 指南, Swarm 模式, 节点
title: 将节点加入 Swarm
---

当你首次创建 Swarm 时，会将单个 Docker Engine 置于 Swarm 模式。为了充分利用 Swarm 模式，你可以向 Swarm 添加节点：

* 添加工作节点可增加容量。当你向 Swarm 部署服务时，引擎会在可用节点（无论是工作节点还是管理节点）上调度任务。当你向 Swarm 添加工作节点时，你扩展了 Swarm 的规模以处理任务，而不会影响管理节点的 Raft 共识。
* 管理节点提高容错能力。管理节点执行 Swarm 的编排和集群管理功能。在管理节点之间，单个领导者节点负责编排任务。如果领导者节点宕机，其余管理节点会选举出新的领导者并恢复编排和 Swarm 状态维护。默认情况下，管理节点也运行任务。

Docker Engine 根据你提供给 `docker swarm join` 命令的 **加入令牌** 来加入 Swarm。节点仅在加入时使用令牌。如果后续轮换令牌，不会影响现有的 Swarm 节点。请参考 [以 Swarm 模式运行 Docker Engine](swarm-mode.md#view-the-join-command-or-update-a-swarm-join-token)。

## 作为工作节点加入

要检索工作节点的加入命令（包括加入令牌），在管理节点上运行以下命令：

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

在工作节点上运行输出中的命令以加入 Swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

This node joined a swarm as a worker.
```

`docker swarm join` 命令执行以下操作：

* 将当前节点上的 Docker Engine 切换到 Swarm 模式。
* 向管理节点请求 TLS 证书。
* 使用机器主机名命名节点。
* 根据 Swarm 令牌将当前节点加入到管理节点监听地址的 Swarm。
* 将当前节点设置为 `Active` 可用性状态，表示它可以接收调度器的任务。
* 将 `ingress` 覆盖网络扩展到当前节点。

## 作为管理节点加入

当你运行 `docker swarm join` 并传递管理令牌时，Docker Engine 会像工作节点一样切换到 Swarm 模式。管理节点也参与 Raft 共识。新节点应该是 `Reachable` 状态，但现有的管理节点仍然是 Swarm 的 `Leader`。

Docker 建议每个集群配置三个或五个管理节点以实现高可用性。由于 Swarm 模式的管理节点使用 Raft 共享数据，因此管理节点数量必须是奇数。只要超过一半的管理节点保持可用，Swarm 就能继续运行。

有关 Swarm 管理员和管理 Swarm 的更多详细信息，请参阅
[管理和维护 Docker Engine Swarm](admin_guide.md)。

要检索管理节点的加入命令（包括加入令牌），在管理节点上运行以下命令：

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
    192.168.99.100:2377
```

在新管理节点上运行输出中的命令以将其加入 Swarm：

```console
$ docker swarm join \
  --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
  192.168.99.100:2377

This node joined a swarm as a manager.
```

## 进一步了解

* `swarm join` [命令行参考](/reference/cli/docker/swarm/join.md)
* [Swarm 模式教程](swarm-tutorial/_index.md)