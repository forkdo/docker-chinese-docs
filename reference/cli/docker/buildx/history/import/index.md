---
title: docker buildx history import
url: /reference/cli/docker/buildx/history/import/
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
  - title: docker buildx history import
    url: /reference/cli/docker/buildx/history/import/
next:
  title: docker buildx history export
  url: /reference/cli/docker/buildx/history/export/
prev:
  title: docker buildx history logs
  url: /reference/cli/docker/buildx/history/logs/
---

**Description:** Import build records into Docker Desktop

**Usage:** `docker buildx history import [OPTIONS] -`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/buildx
-->








## Description

Import a build record from a `.dockerbuild` archive into Docker Desktop. This
lets you view, inspect, and analyze builds created in other environments or CI
pipelines.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--file` |  |  Import from a file path |



## Examples

### Import a `.dockerbuild` archive from standard input

```console
docker buildx history import < mybuild.dockerbuild
```

### Import a build archive from a file (--file) {#file}

```console
docker buildx history import --file ./artifacts/backend-build.dockerbuild
```

### Open a build manually

By default, the `import` command automatically opens the imported build in Docker
Desktop. You don't need to run `open` unless you're opening a specific build
or re-opening it later.

If you've imported multiple builds, you can open one manually:

```console
docker buildx history open ci-build
```



