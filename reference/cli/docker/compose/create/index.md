---
title: docker compose create
url: /reference/cli/docker/compose/create/
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
  - title: docker compose create
    url: /reference/cli/docker/compose/create/
next:
  title: docker compose cp
  url: /reference/cli/docker/compose/cp/
prev:
  title: docker compose down
  url: /reference/cli/docker/compose/down/
---

**Description:** Creates containers for a service

**Usage:** `docker compose create [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面内容是自动从 Docker 源代码生成的。
如果您想修改此处显示的文本，需要在以下仓库中搜索相关字符串：
https://github.com/docker/compose
-->








## Description

Creates containers for a service


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--build` |  |  Build images before starting containers |
| `--force-recreate` |  |  Recreate containers even if their configuration and image haven't changed<br> |
| `--no-build` |  |  Don't build an image, even if it's policy |
| `--no-recreate` |  |  If containers already exist, don't recreate them. Incompatible with --force-recreate.<br> |
| `--pull` | `policy` |  Pull image before running ("always"|"missing"|"never"|"build") |
| `--quiet-pull` |  |  Pull without printing progress information |
| `--remove-orphans` |  |  Remove containers for services not defined in the Compose file |
| `--scale` |  |  Scale SERVICE to NUM instances. Overrides the `scale` setting in the Compose file if present.<br> |
| `-y`, `--yes` |  |  Assume "yes" as answer to all prompts and run non-interactively |






