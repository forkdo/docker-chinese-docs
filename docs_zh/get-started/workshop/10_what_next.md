---
title: Docker 研讨会之后该做什么
weight: 100
linkTitle: "第9部分：下一步"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop
description: 确保你对应用程序接下来可以做什么有更多想法
aliases:
 - /get-started/11_what_next/
 - /guides/workshop/10_what_next/
---

虽然你已经完成了研讨会，但关于容器仍有许多内容需要学习。

以下是接下来可以关注的几个方向。

## 容器编排

在生产环境中运行容器非常复杂。你不会只想登录到某台机器上简单地运行
`docker run` 或 `docker compose up`。为什么不行？因为如果容器崩溃了怎么办？如何在多台机器上进行扩展？容器编排正是为了解决这些问题。Kubernetes、Swarm、Nomad 和 ECS 等工具都以各自不同的方式帮助解决这个问题。

基本思路是，由管理者接收期望的状态。例如这个状态可能是：
"我想运行两个我的 Web 应用实例，并暴露 80 端口"。管理者会查看集群中的所有机器，并将工作委派给工作节点。管理者会监控变化（例如容器退出），然后努力让实际状态反映期望状态。

## 云原生计算基金会（CNCF）项目

CNCF 是各种开源项目的厂商中立之家，包括 Kubernetes、Prometheus、
Envoy、Linkerd、NATS 等。你可以在[此处查看毕业和孵化项目](https://www.cncf.io/projects/)
以及完整的[CNCF 全景图](https://landscape.cncf.io/)。有许多项目可以帮助解决监控、日志、安全、镜像仓库、消息传递等方面的问题。

## 入门视频研讨会

Docker 推荐观看 DockerCon 2022 的视频研讨会。你可以观看整个视频，或使用以下链接跳转到特定章节。

* [Docker 概述和安装](https://youtu.be/gAGEar5HQoU)
* [拉取、运行和探索容器](https://youtu.be/gAGEar5HQoU?t=1400)
* [构建容器镜像](https://youtu.be/gAGEar5HQoU?t=3185)
* [将应用容器化](https://youtu.be/gAGEar5HQoU?t=4683)
* [连接数据库并设置绑定挂载](https://youtu.be/gAGEar5HQoU?t=6305)
* [将容器部署到云端](https://youtu.be/gAGEar5HQoU?t=8280)

<iframe src="https://www.youtube-nocookie.com/embed/gAGEar5HQoU" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 从零开始创建容器

如果你想了解容器是如何从零开始构建的，Aqua Security 的 Liz Rice 有一个精彩的演讲，她用 Go 语言从零开始创建了一个容器。虽然该演讲没有深入探讨网络、使用镜像作为文件系统以及其他高级主题，但它深入剖析了容器内部的工作原理。

<iframe src="https://www.youtube-nocookie.com/embed/8fi7uSYlOdc" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>