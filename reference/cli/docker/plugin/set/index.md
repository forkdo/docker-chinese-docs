---
title: docker plugin set
url: /reference/cli/docker/plugin/set/
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
  - title: docker plugin set
    url: /reference/cli/docker/plugin/set/
next:
  title: docker plugin rm
  url: /reference/cli/docker/plugin/rm/
prev:
  title: docker plugin upgrade
  url: /reference/cli/docker/plugin/upgrade/
---

**Description:** Change settings for a plugin

**Usage:** `docker plugin set PLUGIN KEY=VALUE [KEY=VALUE...]`



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Change settings for a plugin. The plugin must be disabled.

The settings currently supported are:
 * env variables
 * source of mounts
 * path of devices
 * args




## Examples

### Change an environment variable

The following example change the env variable `DEBUG` on the
`sample-volume-plugin` plugin.

```console
$ docker plugin inspect -f {{.Settings.Env}} tiborvass/sample-volume-plugin
[DEBUG=0]

$ docker plugin set tiborvass/sample-volume-plugin DEBUG=1

$ docker plugin inspect -f {{.Settings.Env}} tiborvass/sample-volume-plugin
[DEBUG=1]
```

### Change the source of a mount

The following example change the source of the `mymount` mount on
the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{with $mount := index .Settings.Mounts 0}}{{$mount.Source}}{{end}}' myplugin
/foo

$ docker plugins set myplugin mymount.source=/bar

$ docker plugin inspect -f '{{with $mount := index .Settings.Mounts 0}}{{$mount.Source}}{{end}}' myplugin
/bar
```

> [!NOTE]
> Since only `source` is settable in `mymount`,
> `docker plugins set mymount=/bar myplugin` would work too.

### Change a device path

The following example change the path of the `mydevice` device on
the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{with $device := index .Settings.Devices 0}}{{$device.Path}}{{end}}' myplugin

/dev/foo

$ docker plugins set myplugin mydevice.path=/dev/bar

$ docker plugin inspect -f '{{with $device := index .Settings.Devices 0}}{{$device.Path}}{{end}}' myplugin

/dev/bar
```

> [!NOTE]
> Since only `path` is settable in `mydevice`,
> `docker plugins set mydevice=/dev/bar myplugin` would work too.

### Change the source of the arguments

The following example change the value of the args on the `myplugin` plugin.

```console
$ docker plugin inspect -f '{{.Settings.Args}}' myplugin

["foo", "bar"]

$ docker plugins set myplugin myargs="foo bar baz"

$ docker plugin inspect -f '{{.Settings.Args}}' myplugin

["foo", "bar", "baz"]
```



