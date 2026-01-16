---
title: docker plugin disable
url: /reference/cli/docker/plugin/disable/
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
  - title: docker plugin disable
    url: /reference/cli/docker/plugin/disable/
next:
  title: docker plugin create
  url: /reference/cli/docker/plugin/create/
prev:
  title: docker plugin enable
  url: /reference/cli/docker/plugin/enable/
---

**Description:** Disable a plugin

**Usage:** `docker plugin disable [OPTIONS] PLUGIN`



<!--
此页面由 Docker 的源代码自动生成。如果您想对此处显示的文本提出修改建议，请在 GitHub 上的源代码仓库中提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Disables a plugin. The plugin must be installed before it can be disabled,
see [`docker plugin install`](/reference/cli/docker/plugin/install/). Without the `-f` option,
a plugin that has references (e.g., volumes, networks) cannot be disabled.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Force the disable of an active plugin |



## Examples

The following example shows that the `sample-volume-plugin` plugin is installed
and enabled:

```console
$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   true
```

To disable the plugin, use the following command:

```console
$ docker plugin disable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   false
```



