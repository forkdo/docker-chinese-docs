# 删除在 swarm 上运行的服务

教程的剩余步骤不再使用 `helloworld` 服务，因此现在您可以将该服务从 swarm 中删除。

1.  如果尚未打开终端，请打开终端并 SSH 登录到运行管理器节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service rm helloworld` 命令以删除 `helloworld` 服务。

    ```console
    $ docker service rm helloworld

    helloworld
    ```

3.  运行 `docker service inspect <SERVICE-ID>` 命令以验证 swarm 管理器是否已删除该服务。CLI 会返回一条消息，提示未找到该服务：

    ```console
    $ docker service inspect helloworld
    []
    Status: Error: no such service: helloworld, Code: 1
    ```

4.  尽管服务已不存在，任务容器仍需要几秒钟才能清理完毕。您可以在节点上使用 `docker ps` 命令来验证任务何时被移除。

    ```console
    $ docker ps

    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
    db1651f50347        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.5.9lkmos2beppihw95vdwxy1j3w
    43bf6e532a92        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.3.a71i8rp6fua79ad43ycocl4t2
    5a0fb65d8fa7        alpine:latest       "ping docker.com"        44 minutes ago      Up 45 seconds                 helloworld.2.2jpgensh7d935qdc857pxulfr
    afb0ba67076f        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.4.1c47o7tluz7drve4vkm2m5olx
    688172d3bfaa        alpine:latest       "ping docker.com"        45 minutes ago      Up About a minute             helloworld.1.74nbhb3fhud8jfrhigd7s29we

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES

    ```

## 下一步

接下来，您将设置一个新服务并应用滚动更新。


<a class="button not-prose" href="https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/">应用滚动更新</a>

