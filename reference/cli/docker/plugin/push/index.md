# docker plugin push

**Description:** Push a plugin to a registry

**Usage:** `docker plugin push [OPTIONS] PLUGIN[:TAG]`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

After you have created a plugin using `docker plugin create` and the plugin is
ready for distribution, use `docker plugin push` to share your images to Docker
Hub or a self-hosted registry.

Registry credentials are managed by [docker login](/reference/cli/docker/login/).




## Examples

The following example shows how to push a sample `user/plugin`.

```console
$ docker plugin ls

ID             NAME                    DESCRIPTION                  ENABLED
69553ca1d456   user/plugin:latest      A sample plugin for Docker   false

$ docker plugin push user/plugin
```



