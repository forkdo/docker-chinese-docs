# docker volume rm

**Description:** Remove one or more volumes

**Usage:** `docker volume rm [OPTIONS] VOLUME [VOLUME...]`

**Aliases:** `docker volume remove`

<!--
此页面是自动生成的，来源于 Docker 的源代码。如果您想
修改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Remove one or more volumes. You can't remove a volume that's in use by a container.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  | API 1.25+ Force the removal of one or more volumes |



## Examples

```console
$ docker volume rm hello

hello
```



