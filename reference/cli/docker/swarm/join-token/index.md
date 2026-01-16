---
title: docker swarm join-token
url: /reference/cli/docker/swarm/join-token/
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
  - title: docker swarm join-token
    url: /reference/cli/docker/swarm/join-token/
next:
  title: docker swarm join
  url: /reference/cli/docker/swarm/join/
prev:
  title: docker swarm leave
  url: /reference/cli/docker/swarm/leave/
---

**Description:** Manage join tokens

**Usage:** `docker swarm join-token [OPTIONS] (worker|manager)`



<!--
此页面由 Docker 源代码自动生成。如果您想修改此处显示的文本，
请在 GitHub 的源代码仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Join tokens are secrets that allow a node to join the swarm. There are two
different join tokens available, one for the worker role and one for the manager
role. You pass the token using the `--token` flag when you run
[swarm join](/reference/cli/docker/swarm/join/). Nodes use the join token only when they join the
swarm.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-q`, `--quiet` |  |  Only display token |
| `--rotate` |  |  Rotate join token |



## Examples

You can view or rotate the join tokens using `swarm join-token`.

As a convenience, you can pass `worker` or `manager` as an argument to
`join-token` to print the full `docker swarm join` command to join a new node to
the swarm:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx \
    172.17.0.2:2377

$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2 \
    172.17.0.2:2377
```

Use the `--rotate` flag to generate a new join token for the specified role:

```console
$ docker swarm join-token --rotate worker

Successfully rotated worker join token.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-b30ljddcqhef9b9v4rs7mel7t \
    172.17.0.2:2377
```

After using `--rotate`, only the new token will be valid for joining with the specified role.

The `-q` (or `--quiet`) flag only prints the token:

```console
$ docker swarm join-token -q worker

SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-b30ljddcqhef9b9v4rs7mel7t
```

### `--rotate` {#rotate}

Because tokens allow new nodes to join the swarm, you should keep them secret.
Be particularly careful with manager tokens since they allow new manager nodes
to join the swarm. A rogue manager has the potential to disrupt the operation of
your swarm.

Rotate your swarm's join token if a token gets checked-in to version control,
stolen, or a node is compromised. You may also want to periodically rotate the
token to ensure any unknown token leaks do not allow a rogue node to join
the swarm.

To rotate the join token and print the newly generated token, run
`docker swarm join-token --rotate` and pass the role: `manager` or `worker`.

Rotating a join-token means that no new nodes will be able to join the swarm
using the old token. Rotation does not affect existing nodes in the swarm
because the join token is only used for authorizing new nodes joining the swarm.

### `--quiet` {#quiet}

Only print the token. Do not print a complete command for joining.



