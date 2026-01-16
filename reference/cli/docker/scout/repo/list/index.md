---
title: docker scout repo list
url: /reference/cli/docker/scout/repo/list/
parent:
  title: docker scout repo
  url: /reference/cli/docker/scout/repo/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker scout
    url: /reference/cli/docker/scout/
  - title: docker scout repo
    url: /reference/cli/docker/scout/repo/
  - title: docker scout repo list
    url: /reference/cli/docker/scout/repo/list/
next:
  title: docker scout repo enable
  url: /reference/cli/docker/scout/repo/enable/
---

**Description:** List Docker Scout repositories

**Usage:** `docker scout repo list`



<!--
此页面是从 Docker 的源代码自动生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码存储库中打开工单：

https://github.com/docker/scout-cli
-->








## Description

The docker scout repo list command shows all repositories in an organization.

If ORG is not provided the default configured organization will be used.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--filter` |  |  Regular expression to filter repositories by name |
| `--only-disabled` |  |  Filter to disabled repositories only |
| `--only-enabled` |  |  Filter to enabled repositories only |
| `--only-registry` |  |  Filter to a specific registry only:<br>- hub.docker.com<br>- ecr (AWS ECR) |
| `--org` |  |  Namespace of the Docker organization |






