---
title: docker container pause
url: /reference/cli/docker/container/pause/
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
  - title: docker container pause
    url: /reference/cli/docker/container/pause/
next:
  title: docker container ls
  url: /reference/cli/docker/container/ls/
prev:
  title: docker container port
  url: /reference/cli/docker/container/port/
---

**Description:** Pause all processes within one or more containers

**Usage:** `docker container pause CONTAINER [CONTAINER...]`

**Aliases:** `docker pause`

<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

The `docker pause` command suspends all processes in the specified containers.
On Linux, this uses the freezer cgroup. Traditionally, when suspending a process
the `SIGSTOP` signal is used, which is observable by the process being suspended.
With the freezer cgroup the process is unaware, and unable to capture,
that it is being suspended, and subsequently resumed. On Windows, only Hyper-V
containers can be paused.

See the
[freezer cgroup documentation](https://www.kernel.org/doc/Documentation/cgroup-v1/freezer-subsystem.txt)
for further details.




## Examples

```console
$ docker pause my_container
```



