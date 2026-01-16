---
title: docker scout cache prune
url: /reference/cli/docker/scout/cache/prune/
parent:
  title: docker scout cache
  url: /reference/cli/docker/scout/cache/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker scout
    url: /reference/cli/docker/scout/
  - title: docker scout cache
    url: /reference/cli/docker/scout/cache/
  - title: docker scout cache prune
    url: /reference/cli/docker/scout/cache/prune/
next:
  title: docker scout cache df
  url: /reference/cli/docker/scout/cache/df/
---

**Description:** Remove temporary or cached data

**Usage:** `docker scout cache prune`



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单：

https://github.com/docker/scout-cli
-->








## Description

The `docker scout cache prune` command removes temporary data and SBOM cache.

By default, `docker scout cache prune` only deletes temporary data.
To delete temporary data and clear the SBOM cache, use the `--sboms` flag.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Do not prompt for confirmation |
| `--sboms` |  |  Prune cached SBOMs |



## Examples

### Delete temporary data

```console
$ docker scout cache prune
? Are you sure to delete all temporary data? Yes
    ✓ temporary data deleted
```

### Delete temporary and cache data

```console
$ docker scout cache prune --sboms
? Are you sure to delete all temporary data and all cached SBOMs? Yes
    ✓ temporary data deleted
    ✓ cached SBOMs deleted
```



