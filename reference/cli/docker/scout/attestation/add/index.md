# docker scout attestation add

**Description:** Add attestation to image

**Usage:** `docker scout attestation add OPTIONS IMAGE [IMAGE...]`

**Aliases:** `docker scout attest add`

<!--
本页面根据 Docker 源代码自动生成。如果您想对本文内容提出修改建议，请在 GitHub 上的源代码仓库中提交问题：

https://github.com/docker/scout-cli
-->



> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

The docker scout attestation add command adds attestations to images.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--file` |  |  File location of attestations to attach |
| `--org` |  |  Namespace of the Docker organization |
| `--predicate-type` |  |  Predicate-type for attestations |
| `--referrer` |  |  Use OCI referrer API for pushing attestation |
| `--referrer-repository` | `registry.scout.docker.com` |  Repository to push referrer to |






