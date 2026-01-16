---
title: docker swarm unlock-key
url: /reference/cli/docker/swarm/unlock-key/
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
  - title: docker swarm unlock-key
    url: /reference/cli/docker/swarm/unlock-key/
next:
  title: docker swarm unlock
  url: /reference/cli/docker/swarm/unlock/
prev:
  title: docker swarm update
  url: /reference/cli/docker/swarm/update/
---

**Description:** Manage the unlock key

**Usage:** `docker swarm unlock-key [OPTIONS]`



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

An unlock key is a secret key needed to unlock a manager after its Docker daemon
restarts. These keys are only used when the autolock feature is enabled for the
swarm.

You can view or rotate the unlock key using `swarm unlock-key`. To view the key,
run the `docker swarm unlock-key` command without any arguments:

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-q`, `--quiet` |  |  Only display token |
| `--rotate` |  |  Rotate unlock key |



## Examples

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-fySn8TY4w5lKcWcJPIpKufejh9hxx5KYwx6XZigx3Q4

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

Use the `--rotate` flag to rotate the unlock key to a new, randomly-generated
key:

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

The `-q` (or `--quiet`) flag only prints the key:

```console
$ docker swarm unlock-key -q

SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8
```

### `--rotate` {#rotate}

This flag rotates the unlock key, replacing it with a new randomly-generated
key. The old unlock key will no longer be accepted.

### `--quiet` {#quiet}

Only print the unlock key, without instructions.



