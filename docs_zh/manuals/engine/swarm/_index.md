---
description: Docker Engine Swarm 模式概述
keywords: docker, container, cluster, swarm, docker engine
title: Swarm 模式
weight: 80
aliases:
- /api/swarm-api/
- /engine/userguide/networking/overlay-standalone-swarm/
- /network/overlay-standalone.swarm/
- /release-notes/docker-swarm/
- /swarm/
- /swarm/api/
- /swarm/configure-tls/
- /swarm/discovery/
- /swarm/get-swarm/
- /swarm/install-manual/
- /swarm/install-w-machine/
- /swarm/multi-host-networking/
- /swarm/multi-manager-setup/
- /swarm/networking/
- /swarm/overview/
- /swarm/plan-for-production/
- /swarm/provision-with-machine/
- /swarm/reference/
- /swarm/reference/create/
- /swarm/reference/help/
- /swarm/reference/join/
- /swarm/reference/list/
- /swarm/reference/manage/
- /swarm/reference/swarm/
- /swarm/release-notes/
- /swarm/scheduler/
- /swarm/scheduler/filter/
- /swarm/scheduler/rescheduling/
- /swarm/scheduler/strategy/
- /swarm/secure-swarm-tls/
- /swarm/status-code-comparison-to-docker/
- /swarm/swarm-api/
- /swarm/swarm_at_scale/
- /swarm/swarm_at_scale/02-deploy-infra/
- /swarm/swarm_at_scale/03-create-cluster/
- /swarm/swarm_at_scale/04-deploy-app/
- /swarm/swarm_at_scale/about/
- /swarm/swarm_at_scale/deploy-app/
- /swarm/swarm_at_scale/deploy-infra/
- /swarm/swarm_at_scale/troubleshoot/
---

{{% include "swarm-mode.md" %}}

当前版本的 Docker 包含 Swarm 模式，用于原生管理一组 Docker Engine 集群，称为 swarm。使用 Docker CLI 可以创建 swarm、部署应用程序服务到 swarm，并管理 swarm 的行为。

Docker Swarm 模式内置于 Docker Engine 中。请不要将其与 [Docker Classic Swarm](https://github.com/docker/classicswarm) 混淆，后者已不再积极开发。

## 功能亮点

### 与 Docker Engine 集成的集群管理

使用 Docker Engine CLI 创建 Docker Engine 的 swarm 集群，您可以在其中部署应用程序服务。您不需要额外的编排软件来创建或管理 swarm。

### 去中心化设计

Docker Engine 在运行时处理节点角色之间的差异化，而不是在部署时。您可以使用 Docker Engine 部署两种类型的节点：管理器（managers）和工作节点（workers）。这意味着您可以从单个磁盘镜像构建整个 swarm。

### 声明式服务模型

Docker Engine 采用声明式方法，让您定义应用程序堆栈中各种服务的期望状态。例如，您可能描述一个由 Web 前端服务、消息队列服务和数据库后端组成的应用程序。

### 扩展性

对于每个服务，您可以声明要运行的任务数量。当您扩展或缩减时，swarm 管理器会自动通过添加或删除任务来适应，以维持期望的状态。

### 期望状态协调

swarm 管理器节点持续监控集群状态，并协调实际状态与您声明的期望状态之间的任何差异。例如，如果您设置一个服务运行 10 个容器副本，而托管其中两个副本的工作节点崩溃，管理器会创建两个新副本以替换崩溃的副本。swarm 管理器将新副本分配给正在运行且可用的工作节点。

### 多主机网络

您可以为服务指定覆盖网络（overlay network）。当初始化或更新应用程序时，swarm 管理器会自动为覆盖网络上的容器分配地址。

### 服务发现

swarm 管理器节点为 swarm 中的每个服务分配一个唯一的 DNS 名称，并对运行的容器进行负载均衡。您可以通过 swarm 中嵌入的 DNS 服务器查询 swarm 中运行的每个容器。

### 负载均衡

您可以将服务的端口暴露给外部负载均衡器。在内部，swarm 允许您指定如何在节点之间分发服务容器。

### 默认安全

swarm 中的每个节点都强制执行 TLS 双向身份验证和加密，以确保自身与所有其他节点之间通信的安全。您可以选择使用自签名根证书或自定义根 CA 的证书。

### 滚动更新

在发布时，您可以增量地将服务更新应用到节点。swarm 管理器允许您控制服务部署到不同节点组之间的延迟。如果出现问题，您可以回滚到服务的先前版本。

## 接下来做什么？

* 学习 Swarm 模式的 [关键概念](key-concepts.md)。
* 从 [Swarm 模式教程](swarm-tutorial/_index.md) 开始。
* 探索 Swarm 模式 CLI 命令
  * [swarm init](/reference/cli/docker/swarm/init.md)
  * [swarm join](/reference/cli/docker/swarm/join.md)
  * [service create](/reference/cli/docker/service/create.md)
  * [service inspect](/reference/cli/docker/service/inspect.md)
  * [service ls](/reference/cli/docker/service/ls.md)
  * [service rm](/reference/cli/docker/service/rm.md)
  * [service scale](/reference/cli/docker/service/scale.md)
  * [service ps](/reference/cli/docker/service/ps.md)
  * [service update](/reference/cli/docker/service/update.md)