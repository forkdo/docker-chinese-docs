---
title: docker compose events
url: /reference/cli/docker/compose/events/
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
  - title: docker compose events
    url: /reference/cli/docker/compose/events/
next:
  title: docker compose down
  url: /reference/cli/docker/compose/down/
prev:
  title: docker compose exec
  url: /reference/cli/docker/compose/exec/
---

**Description:** Receive real time events from containers

**Usage:** `docker compose events [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面的内容是从 Docker 的源代码自动生成的。
如果您想建议修改此处显示的文本，您需要通过搜索此代码仓库来找到相应的字符串：
https://github.com/docker/compose
-->








## Description

Stream container events for every container in the project.

With the `--json` flag, a json object is printed one per line with the format:

```json
{
    "time": "2015-11-20T18:01:03.615550",
    "type": "container",
    "action": "create",
    "id": "213cf7...5fc39a",
    "service": "web",
    "attributes": {
      "name": "application_web_1",
      "image": "alpine:edge"
    }
}
```

The events that can be received using this can be seen [here](/reference/cli/docker/system/events/#object-types).


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--json` |  |  Output events as a stream of json objects |
| `--since` |  |  Show all events created since timestamp |
| `--until` |  |  Stream events until this timestamp |






