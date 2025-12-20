# 将服务部署到 swarm

在[创建 swarm](create-swarm.md) 后，您可以将服务部署到 swarm。在本教程中，您还[添加了工作节点](add-nodes.md)，但这并非部署服务的必要条件。

1.  打开终端并 SSH 登录到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行以下命令：

    ```console
    $ docker service create --replicas 1 --name helloworld alpine ping docker.com

    9uk4639qpg7npwf3fn2aasksr
    ```

    * `docker service create` 命令用于创建服务。
    * `--name` 标志将服务命名为 `helloworld`。
    * `--replicas` 标志指定了期望运行 1 个实例的状态。
    * 参数 `alpine ping docker.com` 将服务定义为一个执行 `ping docker.com` 命令的 Alpine Linux 容器。

3.  运行 `docker service ls` 查看正在运行的服务列表：

    ```console
    $ docker service ls

    ID            NAME        SCALE  IMAGE   COMMAND
    9uk4639qpg7n  helloworld  1/1    alpine  ping docker.com
    ```

## 下一步

现在您已准备好检查服务。


<a class="button not-prose" href="/engine/swarm/swarm-tutorial/inspect-service/">检查服务</a>

