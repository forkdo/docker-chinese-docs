---
description: 向 Swarm 添加节点
keywords: 教程, 集群管理, swarm, 入门
title: 向 Swarm 添加节点
weight: 20
notoc: true
---

在你[创建了一个包含管理节点的 Swarm](create-swarm.md) 之后，就可以添加工作节点了。

1.  打开终端，通过 SSH 连接到你想要运行工作节点的机器。
    本教程使用 `worker1` 作为机器名称。

2.  运行上一步[创建 Swarm](create-swarm.md) 教程中 `docker swarm init` 输出的命令，创建一个加入到现有 Swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

    如果你没有保存该命令，可以在管理节点上运行以下命令来获取工作节点的加入命令：

    ```console
    $ docker swarm join-token worker

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377
    ```

3.  打开终端，通过 SSH 连接到你想要运行第二个工作节点的机器。
    本教程使用 `worker2` 作为机器名称。

4.  运行上一步[创建 Swarm](create-swarm.md) 教程中 `docker swarm init` 输出的命令，创建第二个加入到现有 Swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

5.  打开终端，通过 SSH 连接到运行管理节点的机器，运行 `docker node ls` 命令查看工作节点：

    ```console
    $ docker node ls
    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
    9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
    ```

    `MANAGER` 列标识 Swarm 中的管理节点。`worker1` 和 `worker2` 在该列中为空，表示它们是工作节点。

    Swarm 管理命令（如 `docker node ls`）只能在管理节点上运行。

## 下一步是什么？

现在你的 Swarm 包含一个管理节点和两个工作节点。接下来，你将部署一个服务。

{{< button text="部署服务" url="deploy-service.md" >}}