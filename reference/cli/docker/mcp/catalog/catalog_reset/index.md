---
title: docker mcp catalog reset
url: /reference/cli/docker/mcp/catalog/catalog_reset/
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
  - title: docker mcp catalog reset
    url: /reference/cli/docker/mcp/catalog/catalog_reset/
next:
  title: docker mcp catalog ls
  url: /reference/cli/docker/mcp/catalog/catalog_ls/
prev:
  title: docker mcp catalog rm
  url: /reference/cli/docker/mcp/catalog/catalog_rm/
---

**Description:** Reset the catalog system

**Usage:** `docker mcp catalog reset`

**Aliases:** `docker mcp catalog empty`

<!--
本页面由 Docker 源代码自动生成。如果您希望
建议修改此处显示的文本，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

Reset the local catalog management system by removing all user-managed catalogs and configuration. This does not affect Docker's official catalog.





## Examples

  # Reset all user catalogs
  docker mcp catalog reset



