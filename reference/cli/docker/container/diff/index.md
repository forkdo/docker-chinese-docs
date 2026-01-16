---
title: docker container diff
url: /reference/cli/docker/container/diff/
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
  - title: docker container diff
    url: /reference/cli/docker/container/diff/
next:
  title: docker container create
  url: /reference/cli/docker/container/create/
prev:
  title: docker container exec
  url: /reference/cli/docker/container/exec/
---

**Description:** Inspect changes to files or directories on a container's filesystem

**Usage:** `docker container diff CONTAINER`

**Aliases:** `docker diff`

<!--
此页面由 Docker 源代码自动生成。如果您想修改此处显示的文本，
请在 GitHub 的源代码仓库中提出工单或拉取请求：

https://github.com/docker/cli
-->








## Description

List the changed files and directories in a container᾿s filesystem since the
container was created. Three different types of change are tracked:

| Symbol | Description                     |
|--------|---------------------------------|
| `A`    | A file or directory was added   |
| `D`    | A file or directory was deleted |
| `C`    | A file or directory was changed |

You can use the full or shortened container ID or the container name set using
`docker run --name` option.




## Examples

Inspect the changes to an `nginx` container:

```console
$ docker diff 1fdfd1f54c1b

C /dev
C /dev/console
C /dev/core
C /dev/stdout
C /dev/fd
C /dev/ptmx
C /dev/stderr
C /dev/stdin
C /run
A /run/nginx.pid
C /var/lib/nginx/tmp
A /var/lib/nginx/tmp/client_body
A /var/lib/nginx/tmp/fastcgi
A /var/lib/nginx/tmp/proxy
A /var/lib/nginx/tmp/scgi
A /var/lib/nginx/tmp/uwsgi
C /var/log/nginx
A /var/log/nginx/access.log
A /var/log/nginx/error.log
```



