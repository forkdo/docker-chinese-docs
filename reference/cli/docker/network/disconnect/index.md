---
title: docker network disconnect
url: /reference/cli/docker/network/disconnect/
parent:
  title: docker network
  url: /reference/cli/docker/network/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker network
    url: /reference/cli/docker/network/
  - title: docker network disconnect
    url: /reference/cli/docker/network/disconnect/
next:
  title: docker network create
  url: /reference/cli/docker/network/create/
prev:
  title: docker network inspect
  url: /reference/cli/docker/network/inspect/
---

**Description:** Disconnect a container from a network

**Usage:** `docker network disconnect [OPTIONS] NETWORK CONTAINER`



<!--
本页内容由 Docker 源代码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Disconnects a container from a network. The container must be running to
disconnect it from the network.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Force the container to disconnect from a network |



## Examples

```console
$ docker network disconnect multi-host-network container1
```



