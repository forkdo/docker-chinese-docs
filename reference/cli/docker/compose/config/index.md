---
title: docker compose config
url: /reference/cli/docker/compose/config/
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
  - title: docker compose config
    url: /reference/cli/docker/compose/config/
next:
  title: docker compose build
  url: /reference/cli/docker/compose/build/
prev:
  title: docker compose cp
  url: /reference/cli/docker/compose/cp/
---

**Description:** Parse, resolve and render compose file in canonical format

**Usage:** `docker compose config [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面内容由 Docker 源代码自动生成。
如果您想修改此处显示的文本，需要在此仓库中搜索对应字符串：
https://github.com/docker/compose
-->








## Description

`docker compose config` renders the actual data model to be applied on the Docker Engine.
It merges the Compose files set by `-f` flags, resolves variables in the Compose file, and expands short-notation into
the canonical format.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--environment` |  |  Print environment used for interpolation. |
| `--format` |  |  Format the output. Values: [yaml | json] |
| `--hash` |  |  Print the service config hash, one per line. |
| `--images` |  |  Print the image names, one per line. |
| `--lock-image-digests` |  |  Produces an override file with image digests |
| `--models` |  |  Print the model names, one per line. |
| `--networks` |  |  Print the network names, one per line. |
| `--no-consistency` |  |  Don't check model consistency - warning: may produce invalid Compose output<br> |
| `--no-env-resolution` |  |  Don't resolve service env files |
| `--no-interpolate` |  |  Don't interpolate environment variables |
| `--no-normalize` |  |  Don't normalize compose model |
| `--no-path-resolution` |  |  Don't resolve file paths |
| `-o`, `--output` |  |  Save to file (default to stdout) |
| `--profiles` |  |  Print the profile names, one per line. |
| `-q`, `--quiet` |  |  Only validate the configuration, don't print anything |
| `--resolve-image-digests` |  |  Pin image tags to digests |
| `--services` |  |  Print the service names, one per line. |
| `--variables` |  |  Print model variables and default values. |
| `--volumes` |  |  Print the volume names, one per line. |






