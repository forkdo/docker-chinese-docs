---
title: docker node promote
url: /reference/cli/docker/node/promote/
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
  - title: docker node promote
    url: /reference/cli/docker/node/promote/
next:
  title: docker node ls
  url: /reference/cli/docker/node/ls/
prev:
  title: docker node ps
  url: /reference/cli/docker/node/ps/
---

**Description:** Promote one or more nodes to manager in the swarm

**Usage:** `docker node promote NODE [NODE...]`



<!--
本页内容由 Docker 源码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 的源码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Promotes a node to manager. This command can only be executed on a manager node.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

```console
$ docker node promote <node name>
```



