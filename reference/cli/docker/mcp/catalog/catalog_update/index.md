---
title: docker mcp catalog update
url: /reference/cli/docker/mcp/catalog/catalog_update/
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
  - title: docker mcp catalog update
    url: /reference/cli/docker/mcp/catalog/catalog_update/
next:
  title: docker mcp catalog show
  url: /reference/cli/docker/mcp/catalog/catalog_show/
---

**Description:** Update catalog(s) from remote sources

**Usage:** `docker mcp catalog update [name]`



<!--
此页面内容自动从 Docker 的源代码生成。如果您想修改此处显示的文本，
请在 GitHub 的源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Update one or more catalogs by re-downloading from their original sources.
If no name is provided, updates all catalogs that have remote sources.




## Examples

  # Update all catalogs
  docker mcp catalog update

  # Update specific catalog
  docker mcp catalog update team-servers



