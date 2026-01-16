---
title: docker mcp catalog show
url: /reference/cli/docker/mcp/catalog/catalog_show/
parent:
  title: docker mcp catalog
  url: /reference/cli/docker/mcp/catalog/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker mcp
    url: /reference/cli/docker/mcp/
  - title: docker mcp catalog
    url: /reference/cli/docker/mcp/catalog/
  - title: docker mcp catalog show
    url: /reference/cli/docker/mcp/catalog/catalog_show/
next:
  title: docker mcp catalog rm
  url: /reference/cli/docker/mcp/catalog/catalog_rm/
prev:
  title: docker mcp catalog update
  url: /reference/cli/docker/mcp/catalog/catalog_update/
---

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



