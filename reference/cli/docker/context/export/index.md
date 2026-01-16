---
title: docker context export
url: /reference/cli/docker/context/export/
parent:
  title: docker context
  url: /reference/cli/docker/context/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker context
    url: /reference/cli/docker/context/
  - title: docker context export
    url: /reference/cli/docker/context/export/
next:
  title: docker context create
  url: /reference/cli/docker/context/create/
prev:
  title: docker context import
  url: /reference/cli/docker/context/import/
---

**Description:** Export a context to a tar archive FILE or a tar stream on STDOUT.

**Usage:** `docker context export [OPTIONS] CONTEXT [FILE|-]`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/cli
-->








## Description

Exports a context to a file that can then be used with `docker context import`.

The default output filename is `<CONTEXT>.dockercontext`. To export to `STDOUT`,
use `-` as filename, for example:

```console
$ docker context export my-context -
```







