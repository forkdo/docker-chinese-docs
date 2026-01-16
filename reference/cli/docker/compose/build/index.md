---
title: docker compose build
url: /reference/cli/docker/compose/build/
parent:
  title: docker compose
  url: /reference/cli/docker/compose/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker compose
    url: /reference/cli/docker/compose/
  - title: docker compose build
    url: /reference/cli/docker/compose/build/
next:
  title: docker compose attach
  url: /reference/cli/docker/compose/attach/
prev:
  title: docker compose config
  url: /reference/cli/docker/compose/config/
---

**Description:** Build or rebuild services

**Usage:** `docker compose build [OPTIONS] [SERVICE...]`



<!--
抱歉，本页面的内容是自动从 Docker 的源代码生成的。如果您想修改此处显示的文本，
需要在以下仓库中搜索相关字符串并提出修改建议：
https://github.com/docker/compose
-->








## Description

Services are built once and then tagged, by default as `project-service`.

If the Compose file specifies an
[image](https://github.com/compose-spec/compose-spec/blob/main/spec.md#image) name,
the image is tagged with that name, substituting any variables beforehand. See
[variable interpolation](https://github.com/compose-spec/compose-spec/blob/main/spec.md#interpolation).

If you change a service's `Dockerfile` or the contents of its build directory,
run `docker compose build` to rebuild it.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--build-arg` |  |  Set build-time variables for services |
| `--builder` |  |  Set builder to use |
| `--check` |  |  Check build configuration |
| `-m`, `--memory` |  |  Set memory limit for the build container. Not supported by BuildKit.<br> |
| `--no-cache` |  |  Do not use cache when building the image |
| `--print` |  |  Print equivalent bake file |
| `--provenance` |  |  Add a provenance attestation |
| `--pull` |  |  Always attempt to pull a newer version of the image |
| `--push` |  |  Push service images |
| `-q`, `--quiet` |  |  Suppress the build output |
| `--sbom` |  |  Add a SBOM attestation |
| `--ssh` |  |  Set SSH authentications used when building service images. (use 'default' for using your default SSH Agent)<br> |
| `--with-dependencies` |  |  Also build dependencies (transitively) |






