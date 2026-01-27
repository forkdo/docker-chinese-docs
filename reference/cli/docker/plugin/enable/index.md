# docker plugin enable

**Description:** Enable a plugin

**Usage:** `docker plugin enable [OPTIONS] PLUGIN`



<!--
本页内容由 Docker 源代码自动生成。如果您希望
建议修改此处显示的文本，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Enables a plugin. The plugin must be installed before it can be enabled,
see [`docker plugin install`](/reference/cli/docker/plugin/install/).


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--timeout` | `30` |  HTTP client timeout (in seconds) |



## Examples

The following example shows that the `sample-volume-plugin` plugin is installed,
but disabled:

```console
$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   false
```

To enable the plugin, use the following command:

```console
$ docker plugin enable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin ls

ID            NAME                                    DESCRIPTION                ENABLED
69553ca1d123  tiborvass/sample-volume-plugin:latest   A test plugin for Docker   true
```



