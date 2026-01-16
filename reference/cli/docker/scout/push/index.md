---
title: docker scout push
url: /reference/cli/docker/scout/push/
parent:
  title: docker scout
  url: /reference/cli/docker/scout/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker scout
    url: /reference/cli/docker/scout/
  - title: docker scout push
    url: /reference/cli/docker/scout/push/
next:
  title: docker scout policy
  url: /reference/cli/docker/scout/policy/
prev:
  title: docker scout quickview
  url: /reference/cli/docker/scout/quickview/
---

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



