---
description: Drain nodes on the swarm
keywords: tutorial, cluster management, swarm, service, drain, get started
title: Drain a node on the swarm
weight: 80
notoc: true
---

在本教程的前面步骤中，所有节点都以 `Active` 状态运行。Swarm 管理员可以将任务分配给任何 `Active` 节点，因此到目前为止，所有节点都可以接收任务。

有时，在计划维护期间，你需要将节点设置为 `Drain` 状态。`Drain` 状态会阻止节点从 Swarm 管理员接收新任务，同时意味着管理员会停止节点上运行的任务，并在具有 `Active` 状态的节点上启动副本任务。

> [!IMPORTANT]: 
>
> 将节点设置为 `Drain` 状态不会删除该节点上的独立容器（例如通过 `docker run`、`docker compose up` 或 Docker Engine API 创建的容器）。节点的状态（包括 `Drain`）仅影响节点调度 Swarm 服务工作负载的能力。

1.  如果尚未执行，请打开终端并 SSH 连接到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  验证所有节点是否都处于活跃可用状态。

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    1bcef6utixb0l0ca7gxuivsj0    worker2   Ready   Active
    38ciaotwjuritcdtn9npbnkuz    worker1   Ready   Active
    e216jshn25ckzbvmwlnh5jr3g *  manager1  Ready   Active        Leader
    ```

3.  如果你尚未运行 [滚动更新](rolling-update.md) 教程中的 `redis` 服务，请现在启动它：

    ```console
    $ docker service create --replicas 3 --name redis --update-delay 10s redis:7.4.0

    c5uo6kdmzpon37mgj9mwglcfw
    ```

4.  运行 `docker service ps redis` 查看 Swarm 管理员如何将任务分配给不同的节点：

    ```console
    $ docker service ps redis

    NAME                               IMAGE        NODE     DESIRED STATE  CURRENT STATE
    redis.1.7q92v0nr1hcgts2amcjyqg3pq  redis:7.4.0  manager1 Running        Running 26 seconds
    redis.2.7h2l8h3q3wqy5f66hlv9ddmi6  redis:7.4.0  worker1  Running        Running 26 seconds
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd  redis:7.4.0  worker2  Running        Running 26 seconds
    ```

    在这种情况下，Swarm 管理员将一个任务分配给每个节点。在你的环境中，任务的分配可能有所不同。

5.  运行 `docker node update --availability drain <NODE-ID>` 将已分配任务的节点设置为 Drain 状态：

    ```console
    $ docker node update --availability drain worker1

    worker1
    ```

6.  检查节点以确认其可用性状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Drain
    ...snip...
    ```

    被 Drain 的节点在 `Availability` 字段显示 `Drain`。

7.  运行 `docker service ps redis` 查看 Swarm 管理员如何更新 `redis` 服务的任务分配：

    ```console
    $ docker service ps redis

    NAME                                    IMAGE        NODE      DESIRED STATE  CURRENT STATE           ERROR
    redis.1.7q92v0nr1hcgts2amcjyqg3pq       redis:7.4.0  manager1  Running        Running 4 minutes
    redis.2.b4hovzed7id8irg1to42egue8       redis:7.4.0  worker2   Running        Running About a minute
     \_ redis.2.7h2l8h3q3wqy5f66hlv9ddmi6   redis:7.4.0  worker1   Shutdown       Shutdown 2 minutes ago
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd       redis:7.4.0  worker2   Running        Running 4 minutes
    ```

    Swarm 管理员通过结束 `Drain` 状态节点上的任务，并在 `Active` 状态节点上创建新任务来维持期望状态。

8.  运行 `docker node update --availability active <NODE-ID>` 将 Drain 的节点恢复为活跃状态：

    ```console
    $ docker node update --availability active worker1

    worker1
    ```

9.  检查节点以查看更新后的状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Active
    ...snip...
    ```

    当你将节点恢复为 `Active` 状态时，它可以接收新任务：

    * 在服务更新期间扩容
    * 在滚动更新期间
    * 当你将另一个节点设置为 `Drain` 状态时
    * 当活跃节点上的任务失败时

## 下一步

接下来，你将学习如何使用 Swarm 模式的路由网格

{{< button text="Use a Swarm mode routing mesh" url="../ingress.md" >}}