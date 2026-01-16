---
title: docker model install-runner
url: /reference/cli/docker/model/install-runner/
parent:
  title: docker model
  url: /reference/cli/docker/model/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker model
    url: /reference/cli/docker/model/
  - title: docker model install-runner
    url: /reference/cli/docker/model/install-runner/
next:
  title: docker model inspect
  url: /reference/cli/docker/model/inspect/
prev:
  title: docker model list
  url: /reference/cli/docker/model/list/
---

**Description:** Install Docker Model Runner (Docker Engine only)

**Usage:** `docker model install-runner`



<!--
此页面由 Docker 的源代码自动生成。如果您希望建议更改此处显示的文本，请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/model-cli
-->








## Description

This command runs implicitly when a docker model command is executed. You can run this command explicitly to add a new configuration.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--backend` |  |  Specify backend (llama.cpp|vllm). Default: llama.cpp |
| `--debug` |  |  Enable debug logging |
| `--do-not-track` |  |  Do not track models usage in Docker Model Runner |
| `--gpu` | `auto` |  Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| `--host` | `127.0.0.1` |  Host address to bind Docker Model Runner |
| `--port` |  |  Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode)<br> |






