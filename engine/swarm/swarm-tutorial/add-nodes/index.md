# 向 swarm 添加节点

在[创建了一个 swarm](create-swarm.md) 并拥有管理节点后，您就可以添加工作节点了。

1.  打开终端，并通过 ssh 登录到您希望运行工作节点的机器。本教程使用的机器名为 `worker1`。

2.  运行在[创建 swarm](create-swarm.md) 教程步骤中 `docker swarm init` 命令输出的命令，以创建一个加入现有 swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token  SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

    如果您没有该命令，可以在管理节点上运行以下命令来获取用于工作节点的加入命令：

    ```console
    $ docker swarm join-token worker

    To add a worker to this swarm, run the following command:

        docker swarm join \
        --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
        192.168.99.100:2377
    ```

3.  打开终端，并通过 ssh 登录到您希望运行第二个工作节点的机器。本教程使用的机器名为 `worker2`。

4.  运行在[创建 swarm](create-swarm.md) 教程步骤中 `docker swarm init` 命令输出的命令，以创建第二个加入现有 swarm 的工作节点：

    ```console
    $ docker swarm join \
      --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
      192.168.99.100:2377

    This node joined a swarm as a worker.
    ```

5.  打开终端，并通过 ssh 登录到管理节点所在的机器，运行 `docker node ls` 命令以查看工作节点：

    ```console
    $ docker node ls
    ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
    03g1y59jwfg7cf99w4lt0f662    worker2   Ready   Active
    9j68exjopxe7wfl6yuxml7a7j    worker1   Ready   Active
    dxn1zf6l61qsb1josjja83ngz *  manager1  Ready   Active        Leader
    ```

    `MANAGER` 列标识了 swarm 中的管理节点。`worker1` 和 `worker2` 在此列中的空状态表示它们是工作节点。

    像 `docker node ls` 这样的 swarm 管理命令只能在管理节点上运行。

## 下一步？

现在您的 swarm 包含了一个管理节点和两个工作节点。接下来，您将部署一个服务。


<a class="button not-prose" href="/engine/swarm/swarm-tutorial/deploy-service/">部署服务</a>

