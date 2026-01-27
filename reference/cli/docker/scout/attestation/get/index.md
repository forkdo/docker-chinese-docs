# docker scout attestation get

**Description:** Get attestation for image

**Usage:** `docker scout attestation get OPTIONS IMAGE [DIGEST]`

**Aliases:** `docker scout attest get`

<!--
此页面内容自动从 Docker 的源代码生成。如果您想修改此处显示的文本，
请在 GitHub 的源代码仓库中提交工单：

https://github.com/docker/scout-cli
-->



> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

The docker scout attestation get command gets attestations for images.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--key` | `https://registry.scout.docker.com/keyring/dhi/latest.pub` |  Signature key to use for verification |
| `--org` |  |  Namespace of the Docker organization |
| `-o`, `--output` |  |  Write the report to a file |
| `--platform` |  |  Platform of image to analyze |
| `--predicate` |  |  Get in-toto predicate only dropping the subject |
| `--predicate-type` |  |  Predicate-type for attestation |
| `--ref` |  |  Reference to use if the provided tarball contains multiple references.<br>Can only be used with archive |
| `--skip-tlog` |  |  Skip signature verification against public transaction log |
| `--verify` |  |  Verify the signature on the attestation |






