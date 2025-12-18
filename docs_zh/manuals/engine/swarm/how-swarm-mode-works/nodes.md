---
description: Swarm 节点的工作原理
keywords: docker, container, cluster, swarm mode, node
title: 节点工作原理
weight: 10
aliases:
- /engine/swarm/how-swarm-mode-works/
---

Swarm 模式允许您创建一个或多个 Docker 引擎的集群，称为 swarm。一个 swarm 由一个或多个节点组成：运行 Docker 引擎的物理或虚拟机。

有两种类型的节点：[管理器](#manager-nodes) 和 [工作节点](#worker-nodes)。

![Swarm 模式集群](/engine/swarm/images/swarm-diagram.webp)

如果您还没有阅读过，请先阅读 [Swarm 模式概述](../_index.md) 和 [关键概念](../key-concepts.md)。

## 管理器节点

管理器节点负责集群管理任务：

* 维护集群状态
* 调度服务
* 提供 Swarm 模式的 [HTTP API 端点](/reference/api/engine/_index.md)

通过 [Raft](https://raft.github.io/raft.pdf) 实现，管理器维护整个 swarm 及其上运行的所有服务的一致内部状态。出于测试目的，运行单管理器的 swarm 是可以的。如果单管理器 swarm 中的管理器失败，您的服务将继续运行，但您需要创建一个新集群来恢复。

为了利用 Swarm 模式的容错功能，我们建议您根据组织的高可用性要求实现奇数个节点。当您有多个管理器时，可以在管理器节点发生故障时恢复而不会造成停机。

* 三管理器 swarm 最多可容忍一个管理器的丢失。
* 五管理器 swarm 最多可容忍同时丢失两个管理器节点。
* 集群中的奇数 `N` 个管理器节点最多可容忍丢失 `(N-1)/2` 个管理器。
Docker 建议 swarm 中最多七个管理器节点。

    > [!IMPORTANT]
    >
    > 添加更多管理器并不意味着可扩展性或更高性能的提升。通常，情况恰恰相反。

## 工作节点

工作节点也是 Docker 引擎的实例，其唯一目的是执行容器。工作节点不参与 Raft 分布式状态、不做调度决策，也不提供 swarm 模式的 HTTP API。

您可以创建只有一个管理器的 swarm，但不能在没有至少一个管理器节点的情况下拥有工作节点。默认情况下，所有管理器也是工作节点。在单管理器节点集群中，您可以运行 `docker service create` 等命令，调度器将所有任务放在本地引擎上。

为了防止调度器在多节点 swarm 中将任务放在管理器节点上，将管理器节点的可用性设置为 `Drain`。调度器会优雅地停止处于 `Drain` 模式的节点上的任务，并将任务调度到 `Active` 节点上。调度器不会为具有 `Drain` 可用性的节点分配新任务。

请参阅 [`docker node update`](/reference/cli/docker/node/update.md) 命令行参考，了解如何更改节点可用性。

## 更改角色

您可以通过运行 `docker node promote` 将工作节点提升为管理器。例如，当您将管理器节点离线进行维护时，可能需要提升工作节点。请参阅 [node promote](/reference/cli/docker/node/promote.md)。

您也可以将管理器节点降级为工作节点。请参阅 [node demote](/reference/cli/docker/node/demote.md)。

## 了解更多

* 阅读 Swarm 模式中 [服务](services.md) 的工作原理。
* 了解 Swarm 模式中的 [PKI](pki.md) 工作原理。