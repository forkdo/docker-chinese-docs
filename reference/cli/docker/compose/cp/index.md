---
title: docker compose cp
url: /reference/cli/docker/compose/cp/
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
  - title: docker compose cp
    url: /reference/cli/docker/compose/cp/
next:
  title: docker compose config
  url: /reference/cli/docker/compose/config/
prev:
  title: docker compose create
  url: /reference/cli/docker/compose/create/
---

**Description:** Copy files/folders between a service container and the local filesystem

**Usage:** `docker compose cp [OPTIONS] SERVICE:SRC_PATH DEST_PATH|-
	docker compose cp [OPTIONS] SRC_PATH|- SERVICE:DEST_PATH`



<!--
抱歉，此页面内容是自动从 Docker 源代码生成的。
如果您想建议修改此处显示的文本，您需要在以下仓库中搜索相关字符串：
https://github.com/docker/compose
-->








## Description

Copy files/folders between a service container and the local filesystem


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--all` |  |  Include containers created by the run command |
| `-a`, `--archive` |  |  Archive mode (copy all uid/gid information) |
| `-L`, `--follow-link` |  |  Always follow symbol link in SRC_PATH |
| `--index` |  |  Index of the container if service has multiple replicas |






