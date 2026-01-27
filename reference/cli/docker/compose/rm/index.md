# docker compose rm

**Description:** Removes stopped service containers

**Usage:** `docker compose rm [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面的内容由 Docker 源代码自动生成。
如果您想建议对此处显示的文本进行更改，请通过搜索此仓库查找相关字符串：
https://github.com/docker/compose
-->








## Description

Removes stopped service containers.

By default, anonymous volumes attached to containers are not removed. You can override this with `-v`. To list all
volumes, use `docker volume ls`.

Any data which is not in a volume is lost.

Running the command with no options also removes one-off containers created by `docker compose run`:

```console
$ docker compose rm
Going to remove djangoquickstart_web_run_1
Are you sure? [yN] y
Removing djangoquickstart_web_run_1 ... done
```


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Don't ask to confirm removal |
| `-s`, `--stop` |  |  Stop the containers, if required, before removing |
| `-v`, `--volumes` |  |  Remove any anonymous volumes attached to containers |






