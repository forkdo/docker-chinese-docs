---
title: docker network rm
url: /reference/cli/docker/network/rm/
parent:
  title: docker network
  url: /reference/cli/docker/network/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker network
    url: /reference/cli/docker/network/
  - title: docker network rm
    url: /reference/cli/docker/network/rm/
next:
  title: docker network prune
  url: /reference/cli/docker/network/prune/
---

**Description:** Remove one or more networks

**Usage:** `docker network rm NETWORK [NETWORK...]`

**Aliases:** `docker network remove`

<!--
此页面由 Docker 的源代码自动生成。如果您希望建议修改此处的文本，请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/cli
-->








## Description

Removes one or more networks by name or identifier. To remove a network,
you must first disconnect any containers connected to it.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Do not error if the network does not exist |



## Examples

### Remove a network

To remove the network named 'my-network':

```console
$ docker network rm my-network
```

### Remove multiple networks

To delete multiple networks in a single `docker network rm` command, provide
multiple network names or ids. The following example deletes a network with id
`3695c422697f` and a network named `my-network`:

```console
$ docker network rm 3695c422697f my-network
```

When you specify multiple networks, the command attempts to delete each in turn.
If the deletion of one network fails, the command continues to the next on the
list and tries to delete that. The command reports success or failure for each
deletion.



