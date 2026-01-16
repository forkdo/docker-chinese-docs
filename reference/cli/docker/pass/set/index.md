---
title: docker pass set
url: /reference/cli/docker/pass/set/
parent:
  title: Docker Pass
  url: /reference/cli/docker/pass/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: Docker Pass
    url: /reference/cli/docker/pass/
  - title: docker pass set
    url: /reference/cli/docker/pass/set/
next:
  title: docker pass rm
  url: /reference/cli/docker/pass/rm/
---

**Description:** Set a secret

**Usage:** `docker pass set NAME=VALUE`








> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

Secrets can also be created from STDIN:

```console
<some command> | docker pass set <name>
```







