---
title: docker stack rm
url: /reference/cli/docker/stack/rm/
parent:
  title: docker stack
  url: /reference/cli/docker/stack/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker stack
    url: /reference/cli/docker/stack/
  - title: docker stack rm
    url: /reference/cli/docker/stack/rm/
next:
  title: docker stack ps
  url: /reference/cli/docker/stack/ps/
prev:
  title: docker stack services
  url: /reference/cli/docker/stack/services/
---

**Description:** Remove one or more stacks

**Usage:** `docker stack rm [OPTIONS] STACK [STACK...]`

**Aliases:** `docker stack remove`, `docker stack down`

<!--
此页面由 Docker 的源代码自动生成。如果您想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Remove the stack from the swarm.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` | `true` |  Do not wait for stack removal |



## Examples

### Remove a stack

This will remove the stack with the name `myapp`. Services, networks, and secrets
associated with the stack will be removed.

```console
$ docker stack rm myapp

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
```

### Remove multiple stacks

This will remove all the specified stacks, `myapp` and `vossibility`. Services,
networks, and secrets associated with all the specified stacks will be removed.

```console
$ docker stack rm myapp vossibility

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
Removing service vossibility_nsqd
Removing service vossibility_logstash
Removing service vossibility_elasticsearch
Removing service vossibility_kibana
Removing service vossibility_ghollector
Removing service vossibility_lookupd
Removing network vossibility_default
Removing network vossibility_vossibility
```



