---
description: 扩展 Swarm 中运行的服务
keywords: 教程, 集群管理, Swarm 模式, 扩展, 入门
title: 扩展 Swarm 中的服务
weight: 50
notoc: true
---

在 Swarm 中 [部署服务](deploy-service.md) 后，您可以使用 Docker CLI 来扩展服务中的容器数量。在服务中运行的容器称为任务。

1.  如果您还没有打开终端，请通过 SSH 连接到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行以下命令来更改 Swarm 中运行服务的期望状态：

    ```console
    $ docker service scale <SERVICE-ID>=<NUMBER-OF-TASKS>
    ```

    例如：

    ```console
    $ docker service scale helloworld=5

    helloworld scaled to 5
    ```

3.  运行 `docker service ps <SERVICE-ID>` 查看更新的任务列表：

    ```console
    $ docker service ps helloworld

    NAME                                    IMAGE   NODE      DESIRED STATE  CURRENT STATE
    helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2   Running        Running 7 minutes
    helloworld.2.c7a7tcdq5s0uk3qr88mf8xco6  alpine  worker1   Running        Running 24 seconds
    helloworld.3.6crl09vdcalvtfehfh69ogfb1  alpine  worker1   Running        Running 24 seconds
    helloworld.4.auky6trawmdlcne8ad8phb0f1  alpine  manager1  Running        Running 24 seconds
    helloworld.5.ba19kca06l18zujfwxyc5lkyn  alpine  worker2   Running        Running 24 seconds
    ```

    您可以看到 Swarm 创建了 4 个新任务，将服务扩展到总共 5 个正在运行的 Alpine Linux 实例。这些任务分布在 Swarm 的三个节点之间。其中一个在 `manager1` 上运行。

4.  运行 `docker ps` 查看连接节点上运行的容器。以下示例显示在 `manager1` 上运行的任务：

    ```console
    $ docker ps

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    528d68040f95        alpine:latest       "ping docker.com"   About a minute ago   Up About a minute                       helloworld.4.auky6trawmdlcne8ad8phb0f1
    ```

    如果您想查看其他节点上运行的容器，请通过 SSH 连接到这些节点并运行 `docker ps` 命令。

## 下一步

在本教程的这一点上，您已完成 `helloworld` 服务的操作。接下来，您将删除该服务。

{{< button text="删除服务" url="delete-service.md" >}}
