---
title: docker buildx rm
url: /reference/cli/docker/buildx/rm/
parent:
  title: docker buildx
  url: /reference/cli/docker/buildx/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker buildx
    url: /reference/cli/docker/buildx/
  - title: docker buildx rm
    url: /reference/cli/docker/buildx/rm/
next:
  title: docker buildx prune
  url: /reference/cli/docker/buildx/prune/
prev:
  title: docker buildx stop
  url: /reference/cli/docker/buildx/stop/
---

**Description:** Remove one or more builder instances

**Usage:** `docker buildx rm [OPTIONS] [NAME...]`



<!--
此页面是自动生成的，源自 Docker 的源代码。如果您想建议修改此处显示的文本，
请在 GitHub 的源代码仓库中提交工单或拉取请求：

https://github.com/docker/buildx
-->








## Description

Removes the specified or current builder. It is a no-op attempting to remove the
default builder.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--all-inactive` |  |  Remove all inactive builders |
| `-f`, `--force` |  |  Do not prompt for confirmation |
| `--keep-daemon` |  |  Keep the BuildKit daemon running |
| `--keep-state` |  |  Keep BuildKit state |



## Examples

### Remove all inactive builders (--all-inactive) {#all-inactive}

Remove builders that are not in running state.

```console
$ docker buildx rm --all-inactive
WARNING! This will remove all builders that are not in running state. Are you sure you want to continue? [y/N] y
```

### Override the configured builder instance (--builder) {#builder}

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).

### Do not prompt for confirmation (--force) {#force}

Do not prompt for confirmation before removing inactive builders.

```console
$ docker buildx rm --all-inactive --force
```

### Keep the BuildKit daemon running (--keep-daemon) {#keep-daemon}

Keep the BuildKit daemon running after the buildx context is removed. This is
useful when you manage BuildKit daemons and buildx contexts independently.
Only supported by the
[`docker-container`](/build/drivers/docker-container/)
and [`kubernetes`](/build/drivers/kubernetes/) drivers.

### Keep BuildKit state (--keep-state) {#keep-state}

Keep BuildKit state, so it can be reused by a new builder with the same name.
Currently, only supported by the [`docker-container` driver](/build/drivers/docker-container/).



