---
title: docker mcp catalog rm
url: /reference/cli/docker/mcp/catalog/catalog_rm/
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
  - title: docker mcp catalog rm
    url: /reference/cli/docker/mcp/catalog/catalog_rm/
next:
  title: docker mcp catalog reset
  url: /reference/cli/docker/mcp/catalog/catalog_reset/
prev:
  title: docker mcp catalog show
  url: /reference/cli/docker/mcp/catalog/catalog_show/
---

**Description:** Remove a catalog

**Usage:** `docker mcp catalog rm <name>`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/mcp-gateway
-->








## Description

Remove a locally configured catalog. This will delete the catalog and all its server definitions.
The Docker official catalog cannot be removed.




## Examples

  # Remove a catalog
  docker mcp catalog rm old-servers



