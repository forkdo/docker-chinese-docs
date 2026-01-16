---
title: docker node demote
url: /reference/cli/docker/node/demote/
parent:
  title: docker node
  url: /reference/cli/docker/node/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker node
    url: /reference/cli/docker/node/
  - title: docker node demote
    url: /reference/cli/docker/node/demote/
prev:
  title: docker node inspect
  url: /reference/cli/docker/node/inspect/
---

**Description:** Demote one or more nodes from manager in the swarm

**Usage:** `docker node demote NODE [NODE...]`



<!--
此页面由 Docker 的源代码自动生成。如果你想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Demotes an existing manager so that it is no longer a manager.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the [Swarm mode
> section](/engine/swarm/) in the documentation.




## Examples

```console
$ docker node demote <node name>
```



