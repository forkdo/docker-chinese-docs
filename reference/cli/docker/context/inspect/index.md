---
title: docker context inspect
url: /reference/cli/docker/context/inspect/
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
  - title: docker context inspect
    url: /reference/cli/docker/context/inspect/
next:
  title: docker context import
  url: /reference/cli/docker/context/import/
prev:
  title: docker context ls
  url: /reference/cli/docker/context/ls/
---

**Description:** Display detailed information on one or more contexts

**Usage:** `docker context inspect [OPTIONS] [CONTEXT] [CONTEXT...]`



<!--
此页面是自动生成的，源自 Docker 的源代码。如果您想
修改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Inspects one or more contexts.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--format` |  |  Format output using a custom template:<br>'json':             Print in JSON format<br>'TEMPLATE':         Print output using the given Go template.<br>Refer to https://docs.docker.com/go/formatting/ for more information about formatting output with templates |



## Examples

### Inspect a context by name

```console
$ docker context inspect "local+aks"

[
  {
    "Name": "local+aks",
    "Metadata": {
      "Description": "Local Docker Engine",
      "StackOrchestrator": "swarm"
    },
    "Endpoints": {
      "docker": {
        "Host": "npipe:////./pipe/docker_engine",
        "SkipTLSVerify": false
      }
    },
    "TLSMaterial": {},
    "Storage": {
      "MetadataPath": "C:\\Users\\simon\\.docker\\contexts\\meta\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee",
      "TLSPath": "C:\\Users\\simon\\.docker\\contexts\\tls\\cb6d08c0a1bfa5fe6f012e61a442788c00bed93f509141daff05f620fc54ddee"
    }
  }
]
```



