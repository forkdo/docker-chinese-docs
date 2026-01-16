---
title: docker desktop enable model-runner
url: /reference/cli/docker/desktop/enable/model-runner/
parent:
  title: docker desktop enable
  url: /reference/cli/docker/desktop/enable/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker desktop (Beta)
    url: /reference/cli/docker/desktop/
  - title: docker desktop enable
    url: /reference/cli/docker/desktop/enable/
  - title: docker desktop enable model-runner
    url: /reference/cli/docker/desktop/enable/model-runner/
---

**Description:** Manage Docker Model Runner settings

**Usage:** `docker desktop enable model-runner [OPTIONS]`












## Description

Enable and manage Docker Model Runner settings used by 'docker model'


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--no-tcp` |  |  Disable TCP connection. Cannot be used with --tcp. |
| `--tcp` | `12434` |  Enable or change TCP port for connection (1-65535). Cannot be used with --no-tcp.<br> |
| `--cors` | `all` |  CORS configuration. Can be `all`, `none`, or comma-separated list of allowed origins. |






