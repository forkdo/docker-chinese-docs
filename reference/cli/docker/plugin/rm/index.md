---
title: docker plugin rm
url: /reference/cli/docker/plugin/rm/
parent:
  title: docker plugin
  url: /reference/cli/docker/plugin/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker plugin
    url: /reference/cli/docker/plugin/
  - title: docker plugin rm
    url: /reference/cli/docker/plugin/rm/
next:
  title: docker plugin push
  url: /reference/cli/docker/plugin/push/
prev:
  title: docker plugin set
  url: /reference/cli/docker/plugin/set/
---

**Description:** Remove one or more plugins

**Usage:** `docker plugin rm [OPTIONS] PLUGIN [PLUGIN...]`

**Aliases:** `docker plugin remove`

<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Removes a plugin. You cannot remove a plugin if it is enabled, you must disable
a plugin using the [`docker plugin disable`](/reference/cli/docker/plugin/disable/) before removing
it, or use `--force`. Use of `--force` is not recommended, since it can affect
functioning of running containers using the plugin.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Force the removal of an active plugin |



## Examples

The following example disables and removes the `sample-volume-plugin:latest`
plugin:

```console
$ docker plugin disable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin rm tiborvass/sample-volume-plugin:latest

tiborvass/sample-volume-plugin
```



