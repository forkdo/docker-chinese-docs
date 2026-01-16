---
title: docker buildx use
url: /reference/cli/docker/buildx/use/
parent:
  title: docker buildx
  url: /reference/cli/docker/buildx/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker buildx
    url: /reference/cli/docker/buildx/
  - title: docker buildx use
    url: /reference/cli/docker/buildx/use/
next:
  title: docker buildx stop
  url: /reference/cli/docker/buildx/stop/
prev:
  title: docker buildx version
  url: /reference/cli/docker/buildx/version/
---

**Description:** Set the current builder instance

**Usage:** `docker buildx use [OPTIONS] NAME`



<!--
此页面由 Docker 源代码自动生成。如果您希望修改此处显示的文本内容，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/buildx
-->








## Description

Switches the current builder instance. Build commands invoked after this command
will run on a specified builder. Alternatively, a context name can be used to
switch to the default builder of that context.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--default` |  |  Set builder as default for current context |
| `--global` |  |  Builder persists context changes |



## Examples

### Override the configured builder instance (--builder) {#builder}

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).



