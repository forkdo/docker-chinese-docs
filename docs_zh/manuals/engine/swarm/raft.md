---
description: Swarm 模式中的 Raft 共识算法
keywords: docker, container, cluster, swarm, raft
title: Swarm 模式中的 Raft 共识
---

当 Docker 引擎在 Swarm 模式下运行时，管理器节点会实现 [Raft 共识算法](http://thesecretlivesofdata.com/raft/) 来管理全局集群状态。

Swarm 模式使用共识算法的原因是为了确保所有负责管理和调度集群任务的管理器节点都存储着相同的一致状态。

在整个集群中拥有相同的一致状态意味着在发生故障时，任何管理器节点都可以接管任务并将服务恢复到稳定状态。例如，如果负责在集群中调度任务的 Leader 管理器意外死亡，任何其他管理器都可以接管调度任务，并重新平衡任务以匹配期望的状态。

在分布式系统中使用共识算法来复制日志的系统需要特别注意。它们通过要求大多数节点对数值达成一致，来确保在出现故障时集群状态保持一致。

Raft 可以容忍最多 `(N-1)/2` 个故障，并且需要 `(N/2)+1` 个成员的多数或法定人数来对提交到集群的值达成一致。这意味着在运行 Raft 的 5 个管理器集群中，如果有 3 个节点不可用，系统将无法处理任何调度额外任务的请求。现有任务会继续运行，但如果管理器集不健康，调度器无法重新平衡任务以应对故障。

Swarm 模式中共识算法的实现意味着它具有分布式系统固有的特性：

- 在容错系统中对值达成一致。（参考 [FLP 不可能性定理](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/) 和 [Raft 共识算法论文](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)）
- 通过 Leader 选举过程实现互斥
- 集群成员管理
- 全局一致的对象排序和 CAS（比较并交换）原语