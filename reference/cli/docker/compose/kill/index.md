# docker compose kill

**Description:** Force stop service containers

**Usage:** `docker compose kill [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面的内容是自动从 Docker 的源代码生成的。如果您想修改此处显示的文本内容，
需要在以下仓库中搜索相关字符串并提出修改建议：
https://github.com/docker/compose
-->








## Description

Forces running containers to stop by sending a `SIGKILL` signal. Optionally the signal can be passed, for example:

```console
$ docker compose kill -s SIGINT
```


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--remove-orphans` |  |  Remove containers for services not defined in the Compose file |
| `-s`, `--signal` | `SIGKILL` |  SIGNAL to send to the container |






