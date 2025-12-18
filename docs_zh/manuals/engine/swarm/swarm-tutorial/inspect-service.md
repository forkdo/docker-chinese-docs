---
description: 查看应用程序
keywords: 教程, 集群管理, swarm 模式, 入门
title: 查看 Swarm 中的服务
weight: 40
notoc: true
---

在将服务部署到 Swarm 后，你可以使用 Docker CLI 查看 Swarm 中运行的服务的详细信息。

1.  如果尚未打开终端，请通过 SSH 连接到运行管理节点的机器。例如，本教程使用名为 `manager1` 的机器。

2.  运行 `docker service inspect --pretty <SERVICE-ID>` 以易读的格式显示服务的详细信息。

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
    > 要以 JSON 格式返回服务详细信息，请运行不带 `--pretty` 标志的相同命令。

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

    在本例中，`helloworld` 服务的唯一实例正在 `worker2` 节点上运行。你可能会看到服务在管理节点上运行。默认情况下，Swarm 中的管理节点可以像工作节点一样执行任务。

    Swarm 还会显示服务任务的 `DESIRED STATE` 和 `CURRENT STATE`，以便你可以查看任务是否按照服务定义运行。

4.  在运行任务的节点上运行 `docker ps` 以查看任务容器的详细信息。

    > [!TIP]
    >
    > 如果 `helloworld` 在除管理节点之外的节点上运行，你必须通过 SSH 连接到该节点。

    ```console
    [worker2]$ docker ps

    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    e609dde94e47        alpine:latest       "ping docker.com"   3 minutes ago       Up 3 minutes                            helloworld.1.8p1vev3fq5zm0mi8g0as41w35
    ```

## 下一步

接下来，你将更改 Swarm 中运行的服务的规模。

{{< button text="更改规模" url="scale-service.md" >}}