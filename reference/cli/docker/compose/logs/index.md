# docker compose logs

**Description:** View output from containers

**Usage:** `docker compose logs [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面内容由 Docker 源代码自动生成。
如果您希望修改此处显示的文本，需要在以下仓库中搜索对应字符串：
https://github.com/docker/compose
-->








## Description

Displays log output from services


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--follow` |  |  Follow log output |
| `--index` |  |  index of the container if service has multiple replicas |
| `--no-color` |  |  Produce monochrome output |
| `--no-log-prefix` |  |  Don't print prefix in logs |
| `--since` |  |  Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)<br> |
| `-n`, `--tail` | `all` |  Number of lines to show from the end of the logs for each container<br> |
| `-t`, `--timestamps` |  |  Show timestamps |
| `--until` |  |  Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)<br> |






