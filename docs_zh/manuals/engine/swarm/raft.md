---
description: Swarm 模式中的 Raft 共识算法
keywords: docker, container, cluster, swarm, raft
title: Swarm 模式中的 Raft 共识
---

当 Docker Engine 以 Swarm 模式运行时，管理节点会实现
[Raft 共识算法](http://thesecretlivesofdata.com/raft/) 来管理全局集群状态。

Swarm 模式使用共识算法的原因是确保所有负责在集群中管理与调度任务的管理节点
都存储着相同的一致性状态。

跨集群保持相同的一致性状态意味着在发生故障时，任何管理节点都可以接管任务
并将服务恢复到稳定状态。例如，如果负责在集群中调度任务的主管理节点
意外宕机，任何其他管理节点都可以接管调度任务并重新平衡任务以匹配期望状态。

使用共识算法在分布式系统中复制日志的系统需要特别注意。它们通过要求
大多数节点就提议给集群的值达成一致，来确保在存在故障的情况下集群状态保持一致。

Raft 最多容忍 `(N-1)/2` 个故障，并且需要 `(N/2)+1` 个成员的多数或法定人数
来就提议给集群的值达成一致。这意味着在由 5 个管理节点运行 Raft 的集群中，
如果有 3 个节点不可用，系统将无法再处理任何调度额外任务的请求。现有的任务会继续运行，
但如果管理节点集合不健康，调度器就无法重新平衡任务来应对故障。

Swarm 模式中共识算法的实现意味着它具备分布式系统的固有特性：

- 在容错系统中就值达成一致。（参考 [FLP 不可能性定理](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/)
 和 [Raft 共识算法论文](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf)）
- 通过领导者选举过程实现互斥
- 集群成员管理
- 全局一致的对象排序和 CAS（比较并交换）原语