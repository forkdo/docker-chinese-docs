---
title: docker compose bridge convert
url: /reference/cli/docker/compose/bridge/convert/
parent:
  title: docker compose bridge
  url: /reference/cli/docker/compose/bridge/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker compose
    url: /reference/cli/docker/compose/
  - title: docker compose bridge
    url: /reference/cli/docker/compose/bridge/
  - title: docker compose bridge convert
    url: /reference/cli/docker/compose/bridge/convert/
---

**Description:** Convert compose files to Kubernetes manifests, Helm charts, or another model


**Usage:** `docker compose bridge convert`



<!--
抱歉，此页面的内容是从 Docker 的源代码自动生成的。
如果您想建议修改此处显示的文本，您需要通过搜索此代码库来找到相应的字符串：
https://github.com/docker/compose
-->








## Description

Convert compose files to Kubernetes manifests, Helm charts, or another model



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` | `out` |  The output directory for the Kubernetes resources |
| `--templates` |  |  Directory containing transformation templates |
| `-t`, `--transformation` |  |  Transformation to apply to compose model (default: docker/compose-bridge-kubernetes)<br> |






