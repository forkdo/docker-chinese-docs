---
title: docker volume rm
url: /reference/cli/docker/volume/rm/
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
  - title: docker volume rm
    url: /reference/cli/docker/volume/rm/
next:
  title: docker volume prune
  url: /reference/cli/docker/volume/prune/
prev:
  title: docker volume update
  url: /reference/cli/docker/volume/update/
---

**Description:** Remove one or more volumes

**Usage:** `docker volume rm [OPTIONS] VOLUME [VOLUME...]`

**Aliases:** `docker volume remove`

<!--
此页面是自动生成的，来源于 Docker 的源代码。如果您想
修改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Remove one or more volumes. You can't remove a volume that's in use by a container.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  | API 1.25+ Force the removal of one or more volumes |



## Examples

```console
$ docker volume rm hello

hello
```



