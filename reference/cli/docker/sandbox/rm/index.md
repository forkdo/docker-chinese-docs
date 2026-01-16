---
title: docker sandbox 删除
url: /reference/cli/docker/sandbox/rm/
parent:
  title: Docker 沙箱
  url: /reference/cli/docker/sandbox/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: Docker 沙箱
    url: /reference/cli/docker/sandbox/
  - title: docker sandbox 删除
    url: /reference/cli/docker/sandbox/rm/
next:
  title: docker sandbox run
  url: /reference/cli/docker/sandbox/run/
---

**Description:** Remove one or more sandboxes

**Usage:** `docker sandbox rm [OPTIONS] SANDBOX [SANDBOX...]`












## Description

Remove one or more sandboxes by their IDs or names.

This command removes the specified sandboxes. Each sandbox is identified by its unique ID or name.




## Examples

### Remove a sandbox

```console
$ docker sandbox rm abc123def
abc123def
```

### Remove multiple sandboxes

```console
$ docker sandbox rm abc123def def456ghi
abc123def
def456ghi
```

### Remove all sandboxes

```console
$ docker sandbox rm $(docker sandbox ls -q)
```



