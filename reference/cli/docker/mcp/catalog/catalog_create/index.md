---
title: docker mcp catalog create
url: /reference/cli/docker/mcp/catalog/catalog_create/
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
  - title: docker mcp catalog create
    url: /reference/cli/docker/mcp/catalog/catalog_create/
next:
  title: docker mcp catalog add
  url: /reference/cli/docker/mcp/catalog/catalog_add/
prev:
  title: docker mcp catalog export
  url: /reference/cli/docker/mcp/catalog/catalog_export/
---

**Description:** Create a new empty catalog

**Usage:** `docker mcp catalog create <name>`



<!--
此页面内容自动从 Docker 的源代码生成。如果您希望
修改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Create a new empty catalog for organizing custom MCP servers. The catalog will be stored locally and can be populated using 'docker mcp catalog add'.





## Examples

  # Create a new catalog for development servers
  docker mcp catalog create dev-servers
  
  # Create a catalog for production monitoring tools  
  docker mcp catalog create prod-monitoring



