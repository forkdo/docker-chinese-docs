# docker mcp catalog show

**Description:** Display catalog contents

**Usage:** `docker mcp catalog show [name]`



<!--
此页面由 Docker 源代码自动生成。如果您想建议对此处显示的文本进行更改，请在 GitHub 上的源仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Display the contents of a catalog including all server definitions and metadata.
If no name is provided, shows the Docker official catalog.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` |  |  Supported: "json", "yaml". |



## Examples

  # Show Docker's official catalog
  docker mcp catalog show

  # Show a specific catalog in JSON format
  docker mcp catalog show my-catalog --format=json



