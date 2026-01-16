---
title: docker mcp catalog add
url: /reference/cli/docker/mcp/catalog/catalog_add/
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
  - title: docker mcp catalog add
    url: /reference/cli/docker/mcp/catalog/catalog_add/
next:
  title: 
  url: /reference/cli/docker/mcp/catalog/catalog_bootstrap/
prev:
  title: docker mcp catalog create
  url: /reference/cli/docker/mcp/catalog/catalog_create/
---

**Description:** Add a server to a catalog

**Usage:** `docker mcp catalog add <catalog> <server-name> <catalog-file>`



<!--
此页面根据 Docker 源代码自动生成。如果您想
建议修改此处显示的文本，请在 GitHub 的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Add an MCP server definition to an existing catalog by copying it from another catalog file.
The server definition includes all configuration, tools, and metadata.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--force` |  |  Overwrite existing server in the catalog |



## Examples

  # Add a server from another catalog file
  docker mcp catalog add my-catalog github-server ./github-catalog.yaml
  
  # Add with force to overwrite existing server
  docker mcp catalog add my-catalog slack-bot ./team-catalog.yaml --force



