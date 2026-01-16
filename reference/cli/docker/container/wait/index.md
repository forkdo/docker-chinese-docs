---
title: docker container wait
url: /reference/cli/docker/container/wait/
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
  - title: docker container wait
    url: /reference/cli/docker/container/wait/
next:
  title: docker container update
  url: /reference/cli/docker/container/update/
---

**Description:** Block until one or more containers stop, then print their exit codes

**Usage:** `docker container wait CONTAINER [CONTAINER...]`

**Aliases:** `docker wait`

<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
打开工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Block until one or more containers stop, then print their exit codes




## Examples

Start a container in the background.

```console
$ docker run -dit --name=my_container ubuntu bash
```

Run `docker wait`, which should block until the container exits.

```console
$ docker wait my_container
```

In another terminal, stop the first container. The `docker wait` command above
returns the exit code.

```console
$ docker stop my_container
```

This is the same `docker wait` command from above, but it now exits, returning
`0`.

```console
$ docker wait my_container

0
```



