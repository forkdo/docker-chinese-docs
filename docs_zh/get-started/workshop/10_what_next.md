---
title: Docker 工作坊之后该做什么
weight: 100
linkTitle: "第 9 部分：下一步"
keywords: get started, setup, orientation, quickstart, intro, concepts, containers,
  docker desktop
description: 确保您对自己的应用程序接下来可以做什么有更多想法
aliases:
 - /get-started/11_what_next/
 - /guides/workshop/10_what_next/
---

虽然您已经完成了工作坊，但关于容器仍有许多内容需要学习。

以下是接下来可以了解的一些其他领域。

## 容器编排

在生产环境中运行容器非常困难。您不会想要登录到一台机器上简单地运行 `docker run` 或 `docker compose up`。为什么？因为如果容器崩溃了怎么办？如何在多台机器上进行扩展？容器编排可以解决这个问题。Kubernetes、Swarm、Nomad 和 ECS 等工具都可以解决这个问题，只是方式略有不同。

其基本思想是您有一些管理器，它们接收预期的状态。这种状态可能是“我想运行我的 Web 应用程序的两个实例并暴露端口 80”。然后，管理器会查看集群中的所有机器，并将工作委派给工作节点。管理器会监视更改（例如容器退出），然后努力使实际状态反映预期状态。

## 云原生计算基金会项目

CNCF 是各种开源项目的厂商中立之家，包括 Kubernetes、Prometheus、Envoy、Linkerd、NATS 等。您可以在此处查看[已毕业和孵化的项目](https://www.cncf.io/projects/)，以及整个[CNCF 全景图](https://landscape.cncf.io/)。有很多项目可以帮助解决监控、日志记录、安全、镜像注册表、消息传递等方面的问题。

## 入门视频工作坊

Docker 建议观看 DockerCon 2022 的视频工作坊。您可以观看整个视频，或使用以下链接在特定部分打开视频。

* [Docker 概述和安装](https://youtu.be/gAGEar5HQoU)
* [拉取、运行和探索容器](https://youtu.be/gAGEar5HQoU?t=1400)
* [构建容器镜像](https://youtu.be/gAGEar5HQoU?t=3185)
* [将应用程序容器化](https://youtu.be/gAGEar5HQoU?t=4683)
* [连接数据库并设置绑定挂载](https://youtu.be/gAGEar5HQoU?t=6305)
* [将容器部署到云端](https://youtu.be/gAGEar5HQoU?t=8280)

<iframe src="https://www.youtube-nocookie.com/embed/gAGEar5HQoU" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 从零开始创建容器

如果您想了解容器是如何从零开始构建的，Aqua Security 的 Liz Rice 有一个精彩的演讲，她在演讲中使用 Go 从零开始创建了一个容器。虽然该演讲没有深入探讨网络、使用镜像作为文件系统以及其他高级主题，但它深入探讨了事物是如何工作的。

<iframe src="https://www.youtube-nocookie.com/embed/8fi7uSYlOdc" style="max-width: 100%; aspect-ratio: 16 / 9;" width="560" height="auto" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>