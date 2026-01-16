---
title: docker mcp catalog ls
url: /reference/cli/docker/mcp/catalog/catalog_ls/
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
  - title: docker mcp catalog ls
    url: /reference/cli/docker/mcp/catalog/catalog_ls/
next:
  title: docker mcp catalog init
  url: /reference/cli/docker/mcp/catalog/catalog_init/
prev:
  title: docker mcp catalog reset
  url: /reference/cli/docker/mcp/catalog/catalog_reset/
---

**Description:** List all configured catalogs

**Usage:** `docker mcp catalog ls`



<!--
本页面由 Docker 源代码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->








## Description

List all configured catalogs including Docker's official catalog and any locally managed catalogs.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` |  |  Output format. Supported: "json", "yaml". |



## Examples

  # List all catalogs
  docker mcp catalog ls

  # List catalogs in JSON format
  docker mcp catalog ls --format=json



