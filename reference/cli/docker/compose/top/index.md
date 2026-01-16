---
title: docker compose top
url: /reference/cli/docker/compose/top/
parent:
  title: docker compose
  url: /reference/cli/docker/compose/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker compose
    url: /reference/cli/docker/compose/
  - title: docker compose top
    url: /reference/cli/docker/compose/top/
next:
  title: docker compose stop
  url: /reference/cli/docker/compose/stop/
prev:
  title: docker compose unpause
  url: /reference/cli/docker/compose/unpause/
---

**Description:** Display the running processes

**Usage:** `docker compose top [SERVICES...]`



<!--
抱歉，此页面内容是自动从 Docker 源代码生成的。
如果您想修改此处显示的文本，需要在以下仓库中搜索相关字符串：
https://github.com/docker/compose
-->








## Description

Displays the running processes




## Examples

```console
$ docker compose top
example_foo_1
UID    PID      PPID     C    STIME   TTY   TIME       CMD
root   142353   142331   2    15:33   ?     00:00:00   ping localhost -c 5
```



