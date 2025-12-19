---
description: 检查应用程序
keywords: 教程, 集群管理, swarm 模式, 入门
title: 在 swarm 上检查服务
weight: 40
notoc: true
---

当您[部署服务](deploy-service.md)到 swarm 后，可以使用 Docker CLI 查看 swarm 中运行服务的详细信息。

1.  如果尚未操作，请打开终端并 SSH 登录到运行管理器节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service inspect --pretty <SERVICE-ID>` 以易于阅读的格式显示服务的详细信息。

    查看 `helloworld` 服务的详细信息：

    ```console
    [manager1]$ docker service inspect --pretty helloworld

    ID:		9uk4639qpg7npwf3fn2aasksr
    Name:		helloworld
    Service Mode:	REPLICATED
     Replicas:		1
    Placement:
    UpdateConfig:
     Parallelism:	1
    ContainerSpec:
     Image:		alpine
     Args:	ping docker.com
    Resources:
    Endpoint Mode:  vip
    ```

    > [!TIP]
    >
    > 要以 json 格式返回服务详细信息，请运行相同的命令但不带 `--pretty` 标志。

    ```console
    [manager1]$ docker service inspect helloworld
    [
    {
        "ID": "9uk4639qpg7npwf3fn2aasksr",
        "Version": {
            "Index": 418
        },
        "CreatedAt": "2016-06-16T21:57:11.622222327Z",
        "UpdatedAt": "2016-06-16T21:57:11.622222327Z",
        "Spec": {
            "Name": "helloworld",
            "TaskTemplate": {
                "ContainerSpec": {
                    "Image": "alpine",
                    "Args": [
                        "ping",
                        "docker.com"
                    ]
                },
                "Resources": {
                    "Limits": {},
                    "Reservations": {}
                },
                "RestartPolicy": {
                    "Condition": "any",
                    "MaxAttempts": 0
                },
                "Placement": {}
            },
            "Mode": {
                "Replicated": {
                    "Replicas": 1
                }
            },
            "UpdateConfig": {
                "Parallelism": 1
            },
            "EndpointSpec": {
                "Mode": "vip"
            }
        },
        "Endpoint": {
            "Spec": {}
        }
    }
    ]
    ```

3.  运行 `docker service ps <SERVICE-ID>` 查看哪些节点正在运行该服务：

    ```console
    [manager1]$ docker service ps helloworld

    NAME                                    IMAGE   NODE     DESIRED STATE  CURRENT STATE           ERROR               PORTS
    helloworld.1.8p1vev3fq5zm0mi8g0as41w35  alpine  worker2  Running        Running 3 minutes
    ```

    在本例中，`helloworld` 服务的一个实例正在 `worker2` 节点上运行。您可能会看到服务在管理器节点上运行。默认情况下，swarm 中的管理器节点可以像工作节点一样执行任务。

    Swarm 还显示服务任务的 `DESIRED STATE`（期望状态）和 `CURRENT STATE`（当前状态），以便您查看任务是否根据服务定义运行。

4.  在任务运行的节点上运行 `docker ps` 以查看任务容器的详细信息。

    > [!TIP]
    >
    > 如果 `helloworld` 在您的管理器节点以外的节点上运行，您必须 SSH 登录到该节点。

    ```console
    [worker2]$ docker ps

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    e609dde94e47        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.1.8p1vev3fq5zm0mi8g0as41w35
    ```

## 下一步

接下来，您将更改 swarm 中运行服务的规模。

{{< button text="更改规模" url="scale-service.md" >}}