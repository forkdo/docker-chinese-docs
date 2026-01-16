---
title: docker compose kill
url: /reference/cli/docker/compose/kill/
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
  - title: docker compose kill
    url: /reference/cli/docker/compose/kill/
next:
  title: docker compose images
  url: /reference/cli/docker/compose/images/
prev:
  title: docker compose logs
  url: /reference/cli/docker/compose/logs/
---

**Description:** Force stop service containers

**Usage:** `docker compose kill [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面的内容是自动从 Docker 的源代码生成的。如果您想修改此处显示的文本内容，
需要在以下仓库中搜索相关字符串并提出修改建议：
https://github.com/docker/compose
-->








## Description

Forces running containers to stop by sending a `SIGKILL` signal. Optionally the signal can be passed, for example:

```console
$ docker compose kill -s SIGINT
```


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--remove-orphans` |  |  Remove containers for services not defined in the Compose file |
| `-s`, `--signal` | `SIGKILL` |  SIGNAL to send to the container |






