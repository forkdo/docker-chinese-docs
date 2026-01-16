---
title: docker buildx history rm
url: /reference/cli/docker/buildx/history/rm/
parent:
  title: docker buildx history
  url: /reference/cli/docker/buildx/history/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker buildx
    url: /reference/cli/docker/buildx/
  - title: docker buildx history
    url: /reference/cli/docker/buildx/history/
  - title: docker buildx history rm
    url: /reference/cli/docker/buildx/history/rm/
next:
  title: docker buildx history open
  url: /reference/cli/docker/buildx/history/open/
prev:
  title: docker buildx history trace
  url: /reference/cli/docker/buildx/history/trace/
---

**Description:** Remove build records

**Usage:** `docker buildx history rm [OPTIONS] [REF...]`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
打开工单或拉取请求：

https://github.com/docker/buildx
-->








## Description

Remove one or more build records from the current builder’s history. You can
remove specific builds by ID or offset, or delete all records at once using
the `--all` flag.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--all` |  |  Remove all build records |



## Examples

### Remove a specific build

```console
# Using a build ID
docker buildx history rm qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history rm ^1
```

### Remove multiple builds

```console
# Using build IDs
docker buildx history rm qu2gsuo8ejqrwdfii23xkkckt qsiifiuf1ad9pa9qvppc0z1l3

# Or using relative offsets
docker buildx history rm ^1 ^2
```

### Remove all build records from the current builder (--all) {#all}

```console
docker buildx history rm --all
```



