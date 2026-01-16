---
title: docker scout 证明列表
url: /reference/cli/docker/scout/attestation/list/
parent:
  title: docker scout attestation
  url: /reference/cli/docker/scout/attestation/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker scout
    url: /reference/cli/docker/scout/
  - title: docker scout attestation
    url: /reference/cli/docker/scout/attestation/
  - title: docker scout 证明列表
    url: /reference/cli/docker/scout/attestation/list/
next:
  title: docker scout attestation get
  url: /reference/cli/docker/scout/attestation/get/
---

**Description:** List attestations for image

**Usage:** `docker scout attestation list OPTIONS IMAGE`

**Aliases:** `docker scout attestation list`, `docker scout attest list`

<!--
此页面由 Docker 的源代码自动生成。如果您建议修改此处显示的文本，请在 GitHub 上的源代码仓库中创建一个 issue：

https://github.com/docker/scout-cli
-->



> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

The docker scout attestation list command lists attestations for images.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `list` |  Output format:<br>- list: list of attestations of the image<br>- json: json representation of the attestation list (default "json") |
| `--org` |  |  Namespace of the Docker organization |
| `-o`, `--output` |  |  Write the report to a file |
| `--platform` |  |  Platform of image to analyze |
| `--predicate-type` |  |  Predicate-type for attestations |
| `--ref` |  |  Reference to use if the provided tarball contains multiple references.<br>Can only be used with archive |






