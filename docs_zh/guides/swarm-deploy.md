---
title: 部署到 Swarm
keywords: swarm, swarm services, stacks
description: 学习如何在 Docker Swarm 上描述和部署一个简单的应用。
aliases:
- /get-started/part4/
- /get-started/swarm-deploy/
- /guides/deployment-orchestration/swarm-deploy/
summary: '&desc 发现如何使用 Docker Swarm 部署和管理 Docker 容器。

  '
tags:
- deploy
params:
  time: 10 minutes
---

{{% include "swarm-mode.md" %}}

## 前提条件

- 按照 [获取 Docker](/get-started/get-docker.md) 中的描述下载并安装 Docker Desktop。
- 完成 [Docker 研讨会第 2 部分](/get-started/workshop/02_our_app.md) 中将应用容器化的步骤。
- 通过输入 `docker system info` 并查找 `Swarm: active` 消息（可能需要向上滚动一点），确保 Docker Desktop 上启用了 Swarm。

  如果 Swarm 未运行，只需在 shell 提示符下输入 `docker swarm init` 进行设置。

## 简介

既然您已经证明了应用的各个组件可以作为独立容器运行，并展示了如何使用 Kubernetes 进行部署，现在可以看看如何安排它们由 Docker Swarm 管理。Swarm 提供了许多工具来扩展、联网、保护和维护您的容器化应用，这些功能超出了容器本身的能力。

为了验证您的容器化应用在 Swarm 上运行良好，您将使用 Docker Desktop 内置的 Swarm 环境直接在开发机器上部署您的应用，然后再将其移交给生产环境中的完整 Swarm 集群运行。Docker Desktop 创建的 Swarm 环境功能齐全，这意味着它具有您的应用在真实集群上将享有的所有 Swarm 功能，并且可以从您的开发机器方便地访问。

## 使用 Stack 文件描述应用

Swarm 不会像本教程上一步那样创建单个容器。相反，所有 Swarm 工作负载都被调度为服务（services），这是具有自动维护的附加网络功能的可扩展容器组。此外，所有 Swarm 对象都可以并且应该在称为 stack 文件的清单中描述。这些 YAML 文件描述了 Swarm 应用的所有组件和配置，并可用于在任何 Swarm 环境中创建和销毁您的应用。

现在您可以编写一个简单的 stack 文件来运行和管理您的 Todo 应用，即教程 [第 2 部分](02_our_app.md) 中创建的 `getting-started` 容器镜像。将以下内容放入名为 `bb-stack.yaml` 的文件中：

{{% include "swarm-compose-compat.md" %}}

```yaml
version: "3.7"

services:
  bb-app:
    image: getting-started
    ports:
      - "8000:3000"
```

在这个 Swarm YAML 文件中，有一个对象，即 `service`，描述了一个可扩展的相同容器组。在这种情况下，您将只获得一个容器（默认值），该容器将基于您在教程 [第 2 部分](02_our_app.md) 中创建的 `getting-started` 镜像。此外，您还要求 Swarm 将到达开发机器端口 8000 的所有流量转发到 getting-started 容器内部的端口 3000。

> **Kubernetes 服务和 Swarm 服务截然不同**
>
> 尽管名称相似，但这两个编排器对“服务”一词的含义大相径庭。在 Swarm 中，服务同时提供调度和网络功能，创建容器并提供将流量路由到它们的工具。在 Kubernetes 中，调度和网络是分开处理的，部署（或其他控制器）处理作为 Pod 调度容器，而服务仅负责为这些 Pod 添加网络功能。

## 部署并检查您的应用

1. 将您的应用部署到 Swarm：

   ```console
   $ docker stack deploy -c bb-stack.yaml demo
   ```

   如果一切顺利，Swarm 将报告创建了所有 stack 对象，没有任何报错：

   ```shell
   Creating network demo_default
   Creating service demo_bb-app
   ```

   请注意，除了您的服务之外，Swarm 默认还会创建一个 Docker 网络，以隔离作为 stack 一部分部署的容器。

2. 通过列出您的服务来确保一切正常：

   ```console
   $ docker service ls
   ```

   如果一切顺利，您的服务将报告其副本数为 1/1：

   ```shell
   ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
   il7elwunymbs        demo_bb-app         replicated          1/1                 getting-started:latest   *:8000->3000/tcp
   ```

   这表明您要求作为服务一部分的 1/1 个容器已启动并正在运行。此外，您看到开发机器上的端口 8000 被转发到 getting-started 容器中的端口 3000。

3. 打开浏览器并访问您的 Todo 应用 `localhost:8000`；您应该会看到您的 Todo 应用程序，与您在教程 [第 2 部分](02_our_app.md) 中将其作为独立容器运行时相同。

4. 满意后，拆除您的应用：

   ```console
   $ docker stack rm demo
   ```

## 结论

此时，您已成功使用 Docker Desktop 将您的应用部署到开发机器上的功能齐全的 Swarm 环境中。您现在可以向您的应用添加其他组件，并利用 Swarm 的所有功能和强大功能，直接在您自己的机器上操作。

除了部署到 Swarm 之外，您还将您的应用描述为 stack 文件。这个简单的文本文件包含了在运行状态下创建应用所需的一切；您可以将其检入版本控制并与同事共享，让您可以将应用分发到其他集群（例如在开发环境之后可能出现的测试和生产集群）。

## Swarm 和 CLI 参考

本文中使用的所有新 Swarm 对象和 CLI 命令的进一步文档可在此处获取：

- [Swarm 模式](/manuals/engine/swarm/_index.md)
- [Swarm 模式服务](/manuals/engine/swarm/how-swarm-mode-works/services.md)
- [Swarm Stacks](/manuals/engine/swarm/stack-deploy.md)
- [`docker stack *`](/reference/cli/docker/stack/)
- [`docker service *`](/reference/cli/docker/service/)