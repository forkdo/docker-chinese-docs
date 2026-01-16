---
title: docker compose down
url: /reference/cli/docker/compose/down/
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
  - title: docker compose down
    url: /reference/cli/docker/compose/down/
next:
  title: docker compose create
  url: /reference/cli/docker/compose/create/
prev:
  title: docker compose events
  url: /reference/cli/docker/compose/events/
---

**Description:** Stop and remove containers, networks

**Usage:** `docker compose down [OPTIONS] [SERVICES]`



<!--
抱歉，此页面内容是自动生成的，来源于 Docker 的源代码。
如果您希望修改此处显示的文本，需要在以下仓库中搜索相关字符串：
https://github.com/docker/compose
-->








## Description

Stops containers and removes containers, networks, volumes, and images created by `up`.

By default, the only things removed are:

- Containers for services defined in the Compose file.
- Networks defined in the networks section of the Compose file.
- The default network, if one is used.

Networks and volumes defined as external are never removed.

Anonymous volumes are not removed by default. However, as they don’t have a stable name, they are not automatically
mounted by a subsequent `up`. For data that needs to persist between updates, use explicit paths as bind mounts or
named volumes.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--remove-orphans` |  |  Remove containers for services not defined in the Compose file |
| `--rmi` |  |  Remove images used by services. "local" remove only images that don't have a custom tag ("local"|"all")<br> |
| `-t`, `--timeout` |  |  Specify a shutdown timeout in seconds |
| `-v`, `--volumes` |  |  Remove named volumes declared in the "volumes" section of the Compose file and anonymous volumes attached to containers<br> |






