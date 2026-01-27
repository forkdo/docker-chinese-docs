# docker image inspect

**Description:** Display detailed information on one or more images

**Usage:** `docker image inspect [OPTIONS] IMAGE [IMAGE...]`



<!--
此页面由 Docker 的源代码自动生成。如果您想建议修改此处显示的文本，
请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/cli
-->








## Description

Display detailed information on one or more images


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--format` |  |  Format output using a custom template:<br>'json':             Print in JSON format<br>'TEMPLATE':         Print output using the given Go template.<br>Refer to https://docs.docker.com/go/formatting/ for more information about formatting output with templates |
| `--platform` |  | API 1.49+ Inspect a specific platform of the multi-platform image.<br>If the image or the server is not multi-platform capable, the command will error out if the platform does not match.<br>'os[/arch[/variant]]': Explicit platform (eg. linux/amd64) |






