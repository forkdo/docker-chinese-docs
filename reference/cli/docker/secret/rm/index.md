---
title: docker secret rm
url: /reference/cli/docker/secret/rm/
parent:
  title: docker secret
  url: /reference/cli/docker/secret/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker secret
    url: /reference/cli/docker/secret/
  - title: docker secret rm
    url: /reference/cli/docker/secret/rm/
next:
  title: docker secret ls
  url: /reference/cli/docker/secret/ls/
---

**Description:** Remove one or more secrets

**Usage:** `docker secret rm SECRET [SECRET...]`

**Aliases:** `docker secret remove`

<!--
此页面由 Docker 的源代码自动生成。如果你想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Removes the specified secrets from the swarm.

For detailed information about using secrets, refer to [manage sensitive data with Docker secrets](/engine/swarm/secrets/).

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.




## Examples

This example removes a secret:

```console
$ docker secret rm secret.json
sapth4csdo5b6wz2p5uimh5xg
```

> [!WARNING]
> Unlike `docker rm`, this command does not ask for confirmation before removing
> a secret.
{ .warning }



