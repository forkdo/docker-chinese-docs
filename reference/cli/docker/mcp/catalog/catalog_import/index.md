---
title: docker mcp catalog import
url: /reference/cli/docker/mcp/catalog/catalog_import/
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
  - title: docker mcp catalog import
    url: /reference/cli/docker/mcp/catalog/catalog_import/
next:
  title: docker mcp catalog fork
  url: /reference/cli/docker/mcp/catalog/catalog_fork/
prev:
  title: docker mcp catalog init
  url: /reference/cli/docker/mcp/catalog/catalog_init/
---

**Description:** Import a catalog from URL or file

**Usage:** `docker mcp catalog import <alias|url|file>`



<!--
此页面由 Docker 源代码自动生成。如果您希望修改此处显示的文本内容，请在 GitHub 上的源代码仓库中提交问题或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Import an MCP server catalog from a URL or local file. The catalog will be downloaded 
and stored locally for use with the MCP gateway.

When --mcp-registry flag is used, the argument must be an existing catalog name, and the
command will import servers from the MCP registry URL into that catalog.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dry-run` |  |  Show Imported Data but do not update the Catalog |
| `--mcp-registry` |  |  Import server from MCP registry URL into existing catalog |



## Examples

  # Import from URL
  docker mcp catalog import https://example.com/my-catalog.yaml
  
  # Import from local file
  docker mcp catalog import ./shared-catalog.yaml
  
  # Import from MCP registry URL into existing catalog
  docker mcp catalog import my-catalog --mcp-registry https://registry.example.com/server



