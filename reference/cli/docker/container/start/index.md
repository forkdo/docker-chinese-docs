---
title: docker container start
url: /reference/cli/docker/container/start/
parent:
  title: docker container
  url: /reference/cli/docker/container/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker container
    url: /reference/cli/docker/container/
  - title: docker container start
    url: /reference/cli/docker/container/start/
next:
  title: docker container run
  url: /reference/cli/docker/container/run/
prev:
  title: docker container stats
  url: /reference/cli/docker/container/stats/
---

**Description:** Start one or more stopped containers

**Usage:** `docker container start [OPTIONS] CONTAINER [CONTAINER...]`

**Aliases:** `docker start`

<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Start one or more stopped containers


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-a`, `--attach` |  |  Attach STDOUT/STDERR and forward signals |
| `--checkpoint` |  |  **experimental (daemon)** Restore from this checkpoint |
| `--checkpoint-dir` |  |  **experimental (daemon)** Use a custom checkpoint storage directory |
| `--detach-keys` |  |  Override the key sequence for detaching a container |
| `-i`, `--interactive` |  |  Attach container's STDIN |



## Examples

```console
$ docker start my_container
```



