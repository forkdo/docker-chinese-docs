---
title: docker scout config
url: /reference/cli/docker/scout/config/
parent:
  title: docker scout
  url: /reference/cli/docker/scout/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker scout
    url: /reference/cli/docker/scout/
  - title: docker scout config
    url: /reference/cli/docker/scout/config/
next:
  title: docker scout compare
  url: /reference/cli/docker/scout/compare/
prev:
  title: docker scout cves
  url: /reference/cli/docker/scout/cves/
---

**Description:** Manage Docker Scout configuration

**Usage:** `docker scout config [KEY] [VALUE]`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单：

https://github.com/docker/scout-cli
-->








## Description

`docker scout config` allows you to list, get and set Docker Scout configuration.

Available configuration key:

- `organization`: Namespace of the Docker organization to be used by default.




## Examples

### List existing configuration

```console
$ docker scout config
organization=my-org-namespace
```

### Print configuration value

```console
$ docker scout config organization
my-org-namespace
```

### Set configuration value

```console
$ docker scout config organization my-org-namespace
    ✓ Successfully set organization to my-org-namespace
```



