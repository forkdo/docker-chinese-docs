# docker scout push

**Description:** Push an image or image index to Docker Scout

**Usage:** `docker scout push IMAGE`



<!--
此页面是自动从 Docker 的源代码生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单：

https://github.com/docker/scout-cli
-->








## Description

The `docker scout push` command lets you push an image or analysis result to Docker Scout.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--author` |  |  Name of the author of the image |
| `--dry-run` |  |  Do not push the image but process it |
| `--org` |  |  Namespace of the Docker organization to which image will be pushed |
| `-o`, `--output` |  |  Write the report to a file |
| `--platform` |  |  Platform of image to be pushed |
| `--sbom` |  |  Create and upload SBOMs |
| `--secrets` |  |  Scan for secrets in the image |
| `--timestamp` |  |  Timestamp of image or tag creation |



## Examples

### Push an image to Docker Scout

```console
$ docker scout push --org my-org registry.example.com/repo:tag
```



