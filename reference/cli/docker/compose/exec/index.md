---
title: docker compose exec
url: /reference/cli/docker/compose/exec/
parent:
  title: docker compose
  url: /reference/cli/docker/compose/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker compose
    url: /reference/cli/docker/compose/
  - title: docker compose exec
    url: /reference/cli/docker/compose/exec/
next:
  title: docker compose events
  url: /reference/cli/docker/compose/events/
prev:
  title: docker compose images
  url: /reference/cli/docker/compose/images/
---

**Description:** Execute a command in a running container

**Usage:** `docker compose exec [OPTIONS] SERVICE COMMAND [ARGS...]`



<!--
抱歉，本页面的内容是自动从 Docker 源代码生成的。如果您想修改此处显示的文本，
需要在以下代码仓库中搜索相关字符串并提出修改建议：
https://github.com/docker/compose
-->








## Description

This is the equivalent of `docker exec` targeting a Compose service.

With this subcommand, you can run arbitrary commands in your services. Commands allocate a TTY by default, so
you can use a command such as `docker compose exec web sh` to get an interactive prompt.

By default, Compose will enter container in interactive mode and allocate a TTY, while the equivalent `docker exec`
command requires passing `--interactive --tty` flags to get the same behavior. Compose also support those two flags
to offer a smooth migration between commands, whenever they are no-op by default. Still, `interactive` can be used to
force disabling interactive mode (`--interactive=false`), typically when `docker compose exec` command is used inside
a script.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  |  Detached mode: Run command in the background |
| `-e`, `--env` |  |  Set environment variables |
| `--index` |  |  Index of the container if service has multiple replicas |
| `-T`, `--no-tty` | `true` |  Disable pseudo-TTY allocation. By default 'docker compose exec' allocates a TTY.<br> |
| `--privileged` |  |  Give extended privileges to the process |
| `-u`, `--user` |  |  Run the command as this user |
| `-w`, `--workdir` |  |  Path to workdir directory for this command |






