---
title: docker compose restart
url: /reference/cli/docker/compose/restart/
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
  - title: docker compose restart
    url: /reference/cli/docker/compose/restart/
next:
  title: docker compose push
  url: /reference/cli/docker/compose/push/
prev:
  title: docker compose rm
  url: /reference/cli/docker/compose/rm/
---

**Description:** Restart service containers

**Usage:** `docker compose restart [OPTIONS] [SERVICE...]`



<!--
抱歉，此页面的内容由 Docker 的源代码自动生成。如果您想修改此处显示的文本，
需要在此仓库中查找对应的字符串：
https://github.com/docker/compose
-->








## Description

Restarts all stopped and running services, or the specified services only.

If you make changes to your `compose.yml` configuration, these changes are not reflected
after running this command. For example, changes to environment variables (which are added
after a container is built, but before the container's command is executed) are not updated
after restarting.

If you are looking to configure a service's restart policy, refer to
[restart](https://github.com/compose-spec/compose-spec/blob/main/spec.md#restart)
or [restart_policy](https://github.com/compose-spec/compose-spec/blob/main/deploy.md#restart_policy).


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--no-deps` |  |  Don't restart dependent services |
| `-t`, `--timeout` |  |  Specify a shutdown timeout in seconds |






