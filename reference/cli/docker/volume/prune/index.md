---
title: docker volume prune
url: /reference/cli/docker/volume/prune/
parent:
  title: docker volume
  url: /reference/cli/docker/volume/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker volume
    url: /reference/cli/docker/volume/
  - title: docker volume prune
    url: /reference/cli/docker/volume/prune/
next:
  title: docker volume ls
  url: /reference/cli/docker/volume/ls/
prev:
  title: docker volume rm
  url: /reference/cli/docker/volume/rm/
---

**Description:** Remove unused local volumes

**Usage:** `docker volume prune [OPTIONS]`



<!--
此页面由 Docker 源代码自动生成。如果您想对本文内容提出修改建议，请在 GitHub 上的源仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Remove all unused local volumes. Unused local volumes are those which are not
referenced by any containers. By default, it only removes anonymous volumes.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-a`, `--all` |  | API 1.42+ Remove all unused volumes, not just anonymous ones |
| `--filter` |  |  Provide filter values (e.g. `label=<label>`) |
| `-f`, `--force` |  |  Do not prompt for confirmation |



## Examples

```console
$ docker volume prune

WARNING! This will remove anonymous local volumes not used by at least one container.
Are you sure you want to continue? [y/N] y
Deleted Volumes:
07c7bdf3e34ab76d921894c2b834f073721fccfbbcba792aa7648e3a7a664c2e
my-named-vol

Total reclaimed space: 36 B
```

### Filtering (--all, -a) {#all}

Use the `--all` flag to prune both unused anonymous and named volumes.

### Filtering (--filter) {#filter}

The filtering flag (`--filter`) format is of "key=value". If there is more
than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

* label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove volumes with (or without, in case `label!=...` is used) the specified labels.

The `label` filter accepts two formats. One is the `label=...` (`label=<key>` or `label=<key>=<value>`),
which removes volumes with the specified labels. The other
format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes
volumes without the specified labels.



