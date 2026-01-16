---
title: docker service scale
url: /reference/cli/docker/service/scale/
parent:
  title: docker service
  url: /reference/cli/docker/service/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker service
    url: /reference/cli/docker/service/
  - title: docker service scale
    url: /reference/cli/docker/service/scale/
next:
  title: docker service rollback
  url: /reference/cli/docker/service/rollback/
prev:
  title: docker service update
  url: /reference/cli/docker/service/update/
---

**Description:** Scale one or multiple replicated services

**Usage:** `docker service scale SERVICE=REPLICAS [SERVICE=REPLICAS...]`



<!--
此页面由 Docker 源代码自动生成。如果你想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

The scale command enables you to scale one or more replicated services either up
or down to the desired number of replicas. This command cannot be applied on
services which are global mode. The command will return immediately, but the
actual scaling of the service may take some time. To stop all replicas of a
service while keeping the service active in the swarm you can set the scale to 0.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  | API 1.29+ Exit immediately instead of waiting for the service to converge |



## Examples

### Scale a single service

The following command scales the "frontend" service to 50 tasks.

```console
$ docker service scale frontend=50

frontend scaled to 50
```

The following command tries to scale a global service to 10 tasks and returns an error.

```console
$ docker service create --mode global --name backend backend:latest

b4g08uwuairexjub6ome6usqh

$ docker service scale backend=10

backend: scale can only be used with replicated or replicated-job mode
```

Directly afterwards, run `docker service ls`, to see the actual number of
replicas.

```console
$ docker service ls --filter name=frontend

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  15/50     nginx:alpine
```

You can also scale a service using the [`docker service update`](/reference/cli/docker/service/update/)
command. The following commands are equivalent:

```console
$ docker service scale frontend=50
$ docker service update --replicas=50 frontend
```

### Scale multiple services

The `docker service scale` command allows you to set the desired number of
tasks for multiple services at once. The following example scales both the
backend and frontend services:

```console
$ docker service scale backend=3 frontend=5

backend scaled to 3
frontend scaled to 5

$ docker service ls

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  5/5       nginx:alpine
74nzcxxjv6fq  backend   replicated  3/3       redis:7.4.1
```



