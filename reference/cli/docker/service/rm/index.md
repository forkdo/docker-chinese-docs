---
title: docker service rm
url: /reference/cli/docker/service/rm/
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
  - title: docker service rm
    url: /reference/cli/docker/service/rm/
next:
  title: docker service ps
  url: /reference/cli/docker/service/ps/
prev:
  title: docker service rollback
  url: /reference/cli/docker/service/rollback/
---

**Description:** Remove one or more services

**Usage:** `docker service rm SERVICE [SERVICE...]`

**Aliases:** `docker service remove`

<!--
此页面由 Docker 的源代码自动生成。如果你想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Removes the specified services from the swarm.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

Remove the `redis` service:

```console
$ docker service rm redis

redis

$ docker service ls

ID  NAME  MODE  REPLICAS  IMAGE
```

> [!WARNING]
> Unlike `docker rm`, this command does not ask for confirmation before removing
> a running service.



