---
title: docker mcp catalog fork
url: /reference/cli/docker/mcp/catalog/catalog_fork/
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
  - title: docker mcp catalog fork
    url: /reference/cli/docker/mcp/catalog/catalog_fork/
next:
  title: docker mcp catalog export
  url: /reference/cli/docker/mcp/catalog/catalog_export/
prev:
  title: docker mcp catalog import
  url: /reference/cli/docker/mcp/catalog/catalog_import/
---

**Description:** Create a copy of an existing catalog

**Usage:** `docker mcp catalog fork <src-catalog> <new-name>`



<!--
此页面由 Docker 源代码自动生成。如果您想对本文内容提出修改建议，请在 GitHub 上的源仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Create a new catalog by copying all servers from an existing catalog. Useful for creating variations of existing catalogs.





## Examples

  # Fork the Docker catalog to customize it
  docker mcp catalog fork docker-mcp my-custom-docker
  
  # Fork a team catalog for personal use
  docker mcp catalog fork team-servers my-servers



