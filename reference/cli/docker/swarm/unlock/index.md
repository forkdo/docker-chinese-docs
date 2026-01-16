---
title: docker swarm unlock
url: /reference/cli/docker/swarm/unlock/
parent:
  title: docker swarm
  url: /reference/cli/docker/swarm/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker swarm
    url: /reference/cli/docker/swarm/
  - title: docker swarm unlock
    url: /reference/cli/docker/swarm/unlock/
next:
  title: docker swarm leave
  url: /reference/cli/docker/swarm/leave/
prev:
  title: docker swarm unlock-key
  url: /reference/cli/docker/swarm/unlock-key/
---

**Description:** Unlock swarm

**Usage:** `docker swarm unlock`



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Unlocks a locked manager using a user-supplied unlock key. This command must be
used to reactivate a manager after its Docker daemon restarts if the autolock
setting is turned on. The unlock key is printed at the time when autolock is
enabled, and is also available from the `docker swarm unlock-key` command.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

```console
$ docker swarm unlock
Enter unlock key:
```



