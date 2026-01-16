---
title: docker stack ls
url: /reference/cli/docker/stack/ls/
parent:
  title: docker stack
  url: /reference/cli/docker/stack/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker stack
    url: /reference/cli/docker/stack/
  - title: docker stack ls
    url: /reference/cli/docker/stack/ls/
next:
  title: docker stack deploy
  url: /reference/cli/docker/stack/deploy/
prev:
  title: docker stack ps
  url: /reference/cli/docker/stack/ps/
---

**Description:** List stacks

**Usage:** `docker stack ls [OPTIONS]`

**Aliases:** `docker stack list`

<!--
此页面由 Docker 源代码自动生成。如果你想修改此处显示的文本内容，请在 GitHub 上的源代码仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->






**Orchestrator:** Swarm

## Description

Lists the stacks.

> [!NOTE]
> This is a cluster management command, and must be executed on a swarm
> manager node. To learn about managers and workers, refer to the
> [Swarm mode section](/engine/swarm/) in the
> documentation.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` |  |  Format output using a custom template:<br>'table':            Print output in table format with column headers (default)<br>'table TEMPLATE':   Print output in table format using the given Go template<br>'json':             Print in JSON format<br>'TEMPLATE':         Print output using the given Go template.<br>Refer to https://docs.docker.com/go/formatting/ for more information about formatting output with templates |



## Examples

The following command shows all stacks and some additional information:

```console
$ docker stack ls

ID                 SERVICES            ORCHESTRATOR
myapp              2                   Kubernetes
vossibility-stack  6                   Swarm
```

### Format the output (--format) {#format}

The formatting option (`--format`) pretty-prints stacks using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder     | Description        |
|-----------------|--------------------|
| `.Name`         | Stack name         |
| `.Services`     | Number of services |
| `.Orchestrator` | Orchestrator name  |
| `.Namespace`    | Namespace          |

When using the `--format` option, the `stack ls` command either outputs
the data exactly as the template declares or, when using the
`table` directive, includes column headers as well.

The following example uses a template without headers and outputs the
`Name` and `Services` entries separated by a colon (`:`) for all stacks:

```console
$ docker stack ls --format "{{.Name}}: {{.Services}}"
web-server: 1
web-cache: 4
```

To list all stacks in JSON format, use the `json` directive:

```console
$ docker stack ls --format json
{"Name":"myapp","Namespace":"","Orchestrator":"Swarm","Services":"3"}
```



