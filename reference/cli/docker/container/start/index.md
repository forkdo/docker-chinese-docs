# docker container start

**Description:** Start one or more stopped containers

**Usage:** `docker container start [OPTIONS] CONTAINER [CONTAINER...]`

**Aliases:** `docker start`

<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/cli
-->








## Description

Start one or more stopped containers


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-a`, `--attach` |  |  Attach STDOUT/STDERR and forward signals |
| `--checkpoint` |  |  **experimental (daemon)** Restore from this checkpoint |
| `--checkpoint-dir` |  |  **experimental (daemon)** Use a custom checkpoint storage directory |
| `--detach-keys` |  |  Override the key sequence for detaching a container |
| `-i`, `--interactive` |  |  Attach container's STDIN |



## Examples

```console
$ docker start my_container
```



