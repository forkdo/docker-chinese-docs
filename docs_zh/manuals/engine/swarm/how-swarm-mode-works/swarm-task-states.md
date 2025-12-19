---
title: Swarm 任务状态
description: 了解在 Swarm 上调度的任务。
keywords: swarm, task, service
aliases:
- /datacenter/ucp/2.2/guides/admin/monitor-and-troubleshoot/troubleshoot-task-state/
---

Docker 允许您创建服务，而服务可以启动任务。服务是对期望状态的描述，而任务则执行具体的工作。在 Swarm 中，工作按以下顺序进行调度：

1.  使用 `docker service create` 创建服务。
2.  请求发送到 Docker 管理节点。
3.  Docker 管理节点将服务调度到特定的节点上运行。
4.  每个服务可以启动多个任务。
5.  每个任务都有生命周期，包含 `NEW`、`PENDING` 和 `COMPLETE` 等状态。

任务是执行单元，运行一次即完成。当任务停止后，它不会再次执行，但可能会有新任务取代它的位置。

任务会经历一系列状态，直到完成或失败。任务初始化时处于 `NEW` 状态。任务会向前推进经过多个状态，其状态不会倒退。例如，任务永远不会从 `COMPLETE` 变为 `RUNNING`。

任务按以下顺序经历各个状态：

| 任务状态 (Task state) | 描述 (Description)                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `NEW`                 | 任务已初始化。                                                                                                    |
| `PENDING`             | 任务的资源已分配。                                                                                                |
| `ASSIGNED`            | Docker 已将任务分配给节点。                                                                                        |
| `ACCEPTED`            | 任务已被工作节点接受。如果工作节点拒绝任务，状态将变为 `REJECTED`。                                                |
| `READY`               | 工作节点已准备好启动任务。                                                                                          |
| `PREPARING`           | Docker 正在准备任务。                                                                                             |
| `STARTING`            | Docker 正在启动任务。                                                                                             |
| `RUNNING`             | 任务正在执行中。                                                                                                  |
| `COMPLETE`            | 任务退出且没有错误代码。                                                                                          |
| `FAILED`              | 任务退出并带有错误代码。                                                                                          |
| `SHUTDOWN`            | Docker 已请求任务关闭。                                                                                           |
| `REJECTED`            | 工作节点拒绝了任务。                                                                                              |
| `ORPHANED`            | 节点宕机时间过长。                                                                                                |
| `REMOVE`              | 任务尚未终止，但关联的服务已被移除或缩减。                                                                        |

## 查看任务状态

运行 `docker service ps <service-name>` 可以获取任务的状态。`CURRENT STATE` 字段显示任务的状态以及处于该状态的时间。

```console
$ docker service ps webserver
ID             NAME              IMAGE    NODE        DESIRED STATE  CURRENT STATE            ERROR                              PORTS
owsz0yp6z375   webserver.1       nginx    UbuntuVM    Running        Running 44 seconds ago
j91iahr8s74p    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 50 seconds ago    "No such container: webserver.…"
7dyaszg13mw2    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 5 hours ago       "No such container: webserver.…"
```

## 下一步

- [了解 Swarm 任务](https://github.com/docker/swarmkit/blob/master/design/task_model.md)