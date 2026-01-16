---
title: docker context ls
url: /reference/cli/docker/context/ls/
parent:
  title: docker context
  url: /reference/cli/docker/context/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker context
    url: /reference/cli/docker/context/
  - title: docker context ls
    url: /reference/cli/docker/context/ls/
next:
  title: docker context inspect
  url: /reference/cli/docker/context/inspect/
prev:
  title: docker context rm
  url: /reference/cli/docker/context/rm/
---

**Description:** List contexts

**Usage:** `docker context ls [OPTIONS]`

**Aliases:** `docker context list`

<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提出工单或拉取请求：

https://github.com/docker/cli
-->








## Description

List contexts


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` |  |  Format output using a custom template:<br>'table':            Print output in table format with column headers (default)<br>'table TEMPLATE':   Print output in table format using the given Go template<br>'json':             Print in JSON format<br>'TEMPLATE':         Print output using the given Go template.<br>Refer to https://docs.docker.com/go/formatting/ for more information about formatting output with templates |
| `-q`, `--quiet` |  |  Only show context names |



## Examples

Use `docker context ls` to print all contexts. The currently active context is
indicated with an `*`:

```console
$ docker context ls

NAME                DESCRIPTION                               DOCKER ENDPOINT                      ORCHESTRATOR
default *           Current DOCKER_HOST based configuration   unix:///var/run/docker.sock          swarm
production                                                    tcp:///prod.corp.example.com:2376
staging                                                       tcp:///stage.corp.example.com:2376
```



