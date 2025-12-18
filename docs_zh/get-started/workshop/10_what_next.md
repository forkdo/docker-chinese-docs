---
title: Docker 工作坊之后还能学什么
weight: 100
linkTitle: "第 9 部分：下一步"
keywords: 快速开始, 环境配置, 概念介绍, 快速上手, 容器概念,
  docker desktop
description: 为你提供更多关于应用后续发展的思路
aliases:
 - /get-started/11_what_next/
 - /guides/workshop/10_what_next/
---

虽然工作坊已经结束，但关于容器技术还有更多值得深入学习的内容。

以下是一些你可以继续探索的方向。

## 容器编排

在生产环境中运行容器并不容易。你不会想每次都在机器上手动执行 `docker run` 或 `docker compose up`。为什么呢？如果容器意外退出了怎么办？如何在多台机器之间进行扩展？容器编排技术正是为了解决这些问题。Kubernetes、Swarm、Nomad 和 ECS 等工具都以不同的方式帮助你解决这些问题。

基本思路是：你有一个管理节点（manager），它接收你期望达到的状态。这个状态可能是“我需要运行两个 Web 应用实例，并暴露 80 端口”。然后管理节点会查看集群中的所有机器，将任务分发给工作节点（worker）。管理节点会持续监控变化（比如某个容器退出），并努力让实际状态与期望状态保持一致。

## 云原生计算基金会（CNCF）项目

CNCF 是一个厂商中立的组织，维护着众多开源项目，包括 Kubernetes、Prometheus、Envoy、Linkerd、NATS 等。你可以在 [这里查看毕业和孵化阶段的项目](https://www.cncf.io/projects/)，也可以浏览完整的 [CNCF 项目全景图](https://landscape.cncf.io/)。这些项目涵盖了监控、日志、安全、镜像仓库、消息传递等各个领域，能帮你解决很多实际问题。

## 快速上手视频工作坊

Docker 推荐观看 2022 年 DockerCon 的视频工作坊。你可以观看完整视频，也可以通过以下链接直接跳转到特定章节：

* [Docker 概述和安装](https://youtu.be/gAGEar5HQoU)
* [拉取、运行和探索容器](https://youtu.be/gAGEar5HQoU?t=1400)
* [构建容器镜像](https://youtu.be/gAGEar5HQoU?t=3185)
* [将应用容器化](https://youtu.be/gAGEar5HQoU?t=4683)
* [连接数据库并配置挂载卷](https://youtu.be/gAGEar5HQoU?t=6305)
* [将容器部署到云端](https://youtu.be/gAGEar5HQoU?t=8280)

<iframe src="https://www.youtube-nocookie.com/embed/gAGEar5HQoU" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 从零创建一个容器

如果你想深入了解容器是如何从零构建的，Aqua Security 的 Liz Rice 有一个非常棒的演讲，她在其中用 Go 语言从头实现了一个容器。虽然这个演讲没有深入网络、文件系统镜像等高级主题，但它深入剖析了容器的工作原理。

<iframe src="https://www.youtube-nocookie.com/embed/8fi7uSYlOdc" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>