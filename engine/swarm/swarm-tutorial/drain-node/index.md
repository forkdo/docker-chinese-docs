# 将 swarm 中的节点设置为排空状态

在本教程的前面步骤中，所有节点都处于 `Active` 可用状态。Swarm 管理器可以将任务分配给任何 `Active` 节点，因此到目前为止，所有节点都可以接收任务。

在某些情况下，例如计划维护期间，您需要将某个节点设置为 `Drain` 可用状态。`Drain` 可用状态会阻止该节点从 swarm 管理器接收新任务。这也意味着管理器会停止该节点上运行的任务，并在处于 `Active` 可用状态的节点上启动副本任务。

> [!IMPORTANT]: 
>
> 将节点设置为 `Drain` 状态并不会从该节点移除独立容器，例如那些通过 `docker run`、`docker compose up` 或 Docker Engine API 创建的容器。节点的状态（包括 `Drain`）仅影响该节点调度 swarm 服务工作负载的能力。

1.  如果尚未操作，请打开终端并通过 ssh 登录到您运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  验证所有节点是否都处于活跃可用状态。

    ```console
    $ docker node ls

    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    1bcef6utixb0l0ca7gxuivsj0    worker2   Ready   Active
    38ciaotwjuritcdtn9npbnkuz    worker1   Ready   Active
    e216jshn25ckzbvmwlnh5jr3g *  manager1  Ready   Active        Leader
    ```

3.  如果您尚未运行 [滚动更新](rolling-update.md) 教程中的 `redis` 服务，请立即启动它：

    ```console
    $ docker service create --replicas 3 --name redis --update-delay 10s redis:7.4.0

    c5uo6kdmzpon37mgj9mwglcfw
    ```

4.  运行 `docker service ps redis` 查看 swarm 管理器如何将任务分配给不同节点：

    ```console
    $ docker service ps redis

    NAME                               IMAGE        NODE     DESIRED STATE  CURRENT STATE
    redis.1.7q92v0nr1hcgts2amcjyqg3pq  redis:7.4.0  manager1 Running        Running 26 seconds
    redis.2.7h2l8h3q3wqy5f66hlv9ddmi6  redis:7.4.0  worker1  Running        Running 26 seconds
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd  redis:7.4.0  worker2  Running        Running 26 seconds
    ```

    在这种情况下，swarm 管理器将一个任务分配给每个节点。您可能会在您的环境中看到任务在不同节点上的分布情况不同。

5.  运行 `docker node update --availability drain <NODE-ID>` 将一个已分配任务的节点设置为排空状态：

    ```console
    $ docker node update --availability drain worker1

    worker1
    ```

6.  检查该节点以查看其可用状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Drain
    ...snip...
    ```

    被排空的节点显示 `Availability` 为 `Drain`。

7.  运行 `docker service ps redis` 查看 swarm 管理器如何更新 `redis` 服务的任务分配：

    ```console
    $ docker service ps redis

    NAME                                    IMAGE        NODE      DESIRED STATE  CURRENT STATE           ERROR
    redis.1.7q92v0nr1hcgts2amcjyqg3pq       redis:7.4.0  manager1  Running        Running 4 minutes
    redis.2.b4hovzed7id8irg1to42egue8       redis:7.4.0  worker2   Running        Running About a minute
     \_ redis.2.7h2l8h3q3wqy5f66hlv9ddmi6   redis:7.4.0  worker1   Shutdown       Shutdown 2 minutes ago
    redis.3.9bg7cezvedmkgg6c8yzvbhwsd       redis:7.4.0  worker2   Running        Running 4 minutes
    ```

    Swarm 管理器通过结束处于 `Drain` 可用状态的节点上的任务，并在处于 `Active` 可用状态的节点上创建新任务，来维持期望的状态。

8.  运行 `docker node update --availability active <NODE-ID>` 将被排空的节点恢复为活跃状态：

    ```console
    $ docker node update --availability active worker1

    worker1
    ```

9.  检查该节点以查看更新后的状态：

    ```console
    $ docker node inspect --pretty worker1

    ID:			38ciaotwjuritcdtn9npbnkuz
    Hostname:		worker1
    Status:
     State:			Ready
     Availability:		Active
    ...snip...
    ```

    当您将节点重新设置为 `Active` 可用状态时，它可以接收新任务：

    * 在服务更新以扩展时
    * 在滚动更新期间
    * 当您设置另一个节点为 `Drain` 可用状态时
    * 当任务在另一个活跃节点上失败时

## 下一步

接下来，您将学习如何使用 Swarm 模式路由网格


<a class="button not-prose" href="https://docs.docker.com/engine/swarm/ingress/">使用 Swarm 模式路由网格</a>

