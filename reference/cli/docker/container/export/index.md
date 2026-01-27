# docker container export

**Description:** Export a container's filesystem as a tar archive

**Usage:** `docker container export [OPTIONS] CONTAINER`

**Aliases:** `docker export`

<!--
本页内容由 Docker 源代码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

The `docker export` command doesn't export the contents of volumes associated
with the container. If a volume is mounted on top of an existing directory in
the container, `docker export` exports the contents of the underlying
directory, not the contents of the volume.

Refer to [Backup, restore, or migrate data volumes](/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes)
in the user guide for examples on exporting data in a volume.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` |  |  Write to a file, instead of STDOUT |



## Examples

The following commands produce the same result.

```console
$ docker export red_panda > latest.tar
```

```console
$ docker export --output="latest.tar" red_panda
```



