---
title: docker buildx history logs
url: /reference/cli/docker/buildx/history/logs/
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
  - title: docker buildx history logs
    url: /reference/cli/docker/buildx/history/logs/
next:
  title: docker buildx history import
  url: /reference/cli/docker/buildx/history/import/
prev:
  title: docker buildx history ls
  url: /reference/cli/docker/buildx/history/ls/
---

**Description:** Print the logs of a build record

**Usage:** `docker buildx history logs [OPTIONS] [REF]`



<!--
此页面由 Docker 源代码自动生成。如果您希望修改此处显示的文本，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/buildx
-->








## Description

Print the logs for a completed build. The output appears in the same format as
`--progress=plain`, showing the full logs for each step.

By default, this shows logs for the most recent build on the current builder.

You can also specify an earlier build using an offset. For example:

- `^1` shows logs for the build before the most recent
- `^2` shows logs for the build two steps back


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--progress` | `plain` |  Set type of progress output (plain, rawjson, tty) |



## Examples

### Print logs for the most recent build

```console
$ docker buildx history logs
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 31B done
#1 DONE 0.0s
#2 [internal] load .dockerignore
#2 transferring context: 2B done
#2 DONE 0.0s
...
```

By default, this shows logs for the most recent build on the current builder.

### Print logs for a specific build

To print logs for a specific build, use a build ID or offset:

```console
# Using a build ID
docker buildx history logs qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history logs ^1
```

### Set type of progress output (--progress) {#progress}

```console
$ docker buildx history logs ^1 --progress rawjson
{"id":"buildx_step_1","status":"START","timestamp":"2024-05-01T12:34:56.789Z","detail":"[internal] load build definition from Dockerfile"}
{"id":"buildx_step_1","status":"COMPLETE","timestamp":"2024-05-01T12:34:57.001Z","duration":212000000}
...
```



