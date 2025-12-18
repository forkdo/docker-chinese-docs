---
title: 部署到 Swarm
keywords: swarm, swarm services, stacks
description: 了解如何在 Docker Swarm 上描述和部署一个简单的应用程序。
aliases:
  - /get-started/part4/
  - /get-started/swarm-deploy/
  - /guides/deployment-orchestration/swarm-deploy/
summary: |
  了解如何使用 Docker Swarm 部署和管理 Docker 容器。
tags: [deploy]
params:
  time: 10 分钟
---

{{% include "swarm-mode.md" %}}

## 前置条件

- 按照 [获取 Docker](/get-started/get-docker.md) 中的说明下载并安装 Docker Desktop。
- 完成 [Docker 工作坊第 2 部分](/get-started/workshop/02_our_app.md) 中的应用容器化实践。
- 通过运行 `docker system info` 并查找 `Swarm: active` 消息（可能需要稍微向上滚动），确保 Docker Desktop 上已启用 Swarm。

  如果 Swarm 未运行，只需在命令行中输入 `docker swarm init` 即可设置。

## 介绍

现在你已经证明了应用程序的各个组件可以作为独立容器运行，并展示了如何使用 Kubernetes 部署它。接下来，你可以了解如何使用 Docker Swarm 来安排和管理它们。Swarm 提供了许多工具来扩展、网络化、保护和维护你的容器化应用程序，这些功能远超容器本身的能力。

为了验证你的容器化应用程序在 Swarm 上运行良好，你将使用 Docker Desktop 内置的 Swarm 环境，在你的开发机器上部署应用程序，然后再将其部署到生产环境中的完整 Swarm 集群上。Docker Desktop 创建的 Swarm 环境功能完整，意味着它具备你的应用程序在真实集群上运行所需的所有 Swarm 功能，你可以直接从开发机器上方便地访问这些功能。

## 使用堆栈文件描述应用程序

Swarm 从不创建像你在本教程上一步骤中那样单独的容器。相反，所有 Swarm 工作负载都作为服务进行调度，服务是可扩展的、具有自动网络功能的容器组，由 Swarm 自动维护。此外，所有 Swarm 对象都应（也必须）在称为堆栈文件的清单中描述。这些 YAML 文件描述了你的 Swarm 应用程序的所有组件和配置，可用于在任何 Swarm 环境中创建和销毁你的应用程序。

现在你可以编写一个简单的堆栈文件来运行和管理你的 Todo 应用，即在教程第 2 部分中创建的 `getting-started` 镜像。在名为 `bb-stack.yaml` 的文件中放置以下内容：

{{% include "swarm-compose-compat.md" %}}

```yaml
version: "3.7"

services:
  bb-app:
    image: getting-started
    ports:
      - "8000:3000"
```

在这个 Swarm YAML 文件中，有一个对象，即 `service`，描述了一组可扩展的、相同的容器，具有 Swarm 自动提供的网络功能。在这种情况下，你将得到一个容器（默认值），该容器将基于你在教程第 2 部分中创建的 `getting-started` 镜像。此外，你还要求 Swarm 将到达你开发机器上 8000 端口的所有流量转发到 getting-started 容器内的 3000 端口。

> **Kubernetes 服务与 Swarm 服务有很大不同**
>
> 尽管名称相似，但两种编排器对“服务”一词的含义有很大不同。在 Swarm 中，服务同时提供调度和网络功能，创建容器并提供将流量路由到容器的工具。在 Kubernetes 中，调度和网络是分开处理的，部署（或其他控制器）负责将容器作为 Pod 进行调度，而服务仅负责为这些 Pod 添加网络功能。

## 部署并检查你的应用程序

1. 将你的应用程序部署到 Swarm：

   ```console
   $ docker stack deploy -c bb-stack.yaml demo
   ```

   如果一切顺利，Swarm 将报告创建了所有堆栈对象，没有任何错误：

   ```shell
   Creating network demo_default
   Creating service demo_bb-app
   ```

   请注意，除了你的服务外，Swarm 还默认创建了一个 Docker 网络，以隔离作为你的堆栈一部分部署的容器。

2. 通过列出你的服务来确保一切正常：

   ```console
   $ docker service ls
   ```

   如果一切顺利，你的服务将报告其副本已创建 1/1：

   ```shell
   ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
   il7elwunymbs        demo_bb-app         replicated          1/1                 getting-started:latest   *:8000->3000/tcp
   ```

   这表示你作为服务一部分请求的 1/1 容器已启动并运行。同时，你看到开发机器上的 8000 端口正在转发到 getting-started 容器中的 3000 端口。

3. 打开浏览器，访问 `localhost:8000` 上的 Todo 应用；你应该看到你的 Todo 应用，与你在教程第 2 部分中作为独立容器运行它时相同。

4. 确认无误后，拆除你的应用程序：

   ```console
   $ docker stack rm demo
   ```

## 结论

至此，你已成功使用 Docker Desktop 将你的应用程序部署到开发机器上的完整 Swarm 环境。现在你可以向你的应用添加其他组件，并利用 Swarm 的所有功能和强大能力，就在你自己的机器上。

除了部署到 Swarm 外，你还使用堆栈文件描述了你的应用程序。这个简单的文本文件包含了创建你的应用程序运行状态所需的一切；你可以将其检入版本控制并与同事共享，让你能够将应用程序分发到其他集群（比如开发环境之后的测试和生产集群）。

## Swarm 和 CLI 参考

本文中使用的所有新 Swarm 对象和 CLI 命令的进一步文档可在此处找到：

- [Swarm 模式](/manuals/engine/swarm/_index.md)
- [Swarm 模式服务](/manuals/engine/swarm/how-swarm-mode-works/services.md)
- [Swarm 堆栈](/manuals/engine/swarm/stack-deploy.md)
- [`docker stack *`](/reference/cli/docker/stack/)
- [`docker service *`](/reference/cli/docker/service/)