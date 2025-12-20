# 节点的工作原理

Swarm 模式允许你创建一个或多个 Docker 引擎的集群，称为 swarm。swarm 由一个或多个节点组成：运行 Docker 引擎的物理或虚拟机。

有两种类型的节点：[管理器](#manager-nodes) 和 [工作节点](#worker-nodes)。

![Swarm 模式集群](/engine/swarm/images/swarm-diagram.webp)

如果你还没有阅读过，请先查看 [Swarm 模式概述](../_index.md) 和 [关键概念](../key-concepts.md)。

## 管理器节点

管理器节点负责集群管理任务：

* 维护集群状态
* 调度服务
* 提供 Swarm 模式 [HTTP API 端点](/reference/api/engine/_index.md)

通过 [Raft](https://raft.github.io/raft.pdf) 实现，管理器维护整个 swarm 及其上运行的所有服务的一致内部状态。出于测试目的，运行单个管理器的 swarm 是可以的。如果单管理器 swarm 中的管理器失败，你的服务将继续运行，但你需要创建一个新集群来恢复。

为了利用 Swarm 模式容错功能，我们建议你根据组织的高可用性要求实现奇数个节点。当你有多个管理器时，可以从管理器节点故障中恢复而不会造成停机。

* 三个管理器的 swarm 最多可以容忍一个管理器的丢失。
* 五个管理器的 swarm 最多可以同时容忍两个管理器节点的丢失。
* 集群中奇数个 `N` 管理器节点最多可以容忍 `(N-1)/2` 个管理器的丢失。
Docker 建议 swarm 中最多有七个管理器节点。

    > [!IMPORTANT]
    >
    > 添加更多管理器并不意味着可扩展性或更高性能的提升。通常，情况恰恰相反。

## 工作节点

工作节点也是 Docker 引擎的实例，其唯一目的是执行容器。工作节点不参与 Raft 分布式状态、不做调度决策，也不提供 swarm 模式 HTTP API。

你可以创建只有一个管理器节点的 swarm，但不能在没有至少一个管理器节点的情况下拥有工作节点。默认情况下，所有管理器也是工作节点。在单管理器节点集群中，你可以运行 `docker service create` 等命令，调度器将所有任务放置在本地引擎上。

为了防止调度器在多节点 swarm 中将任务放置在管理器节点上，将管理器节点的可用性设置为 `Drain`。调度器会优雅地停止 `Drain` 模式节点上的任务，并将任务调度到 `Active` 节点上。调度器不会将新任务分配给具有 `Drain` 可用性的节点。

请参阅 [`docker node update`](/reference/cli/docker/node/update.md) 命令行参考，了解如何更改节点可用性。

## 更改角色

你可以通过运行 `docker node promote` 将工作节点提升为管理器。例如，当你将管理器节点离线进行维护时，可能需要提升工作节点。请参阅 [node promote](/reference/cli/docker/node/promote.md)。

你也可以将管理器节点降级为工作节点。请参阅 [node demote](/reference/cli/docker/node/demote.md)。

## 了解更多

* 阅读 Swarm 模式 [服务](services.md) 的工作原理。
* 了解 Swarm 模式中 [PKI](pki.md) 的工作原理。
