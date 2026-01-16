---
title: docker model reinstall-runner
url: /reference/cli/docker/model/reinstall-runner/
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
  - title: docker model reinstall-runner
    url: /reference/cli/docker/model/reinstall-runner/
next:
  title: docker model push
  url: /reference/cli/docker/model/push/
prev:
  title: docker model restart-runner
  url: /reference/cli/docker/model/restart-runner/
---

**Description:** Reinstall Docker Model Runner (Docker Engine only)

**Usage:** `docker model reinstall-runner`



<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 上的
源代码仓库中提交工单或拉取请求：

https://github.com/docker/model-cli
-->








## Description

This command removes the existing Docker Model Runner container and reinstalls it with the specified configuration. Models and images are preserved during reinstallation.



## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--backend` |  |  Specify backend (llama.cpp|vllm). Default: llama.cpp |
| `--debug` |  |  Enable debug logging |
| `--do-not-track` |  |  Do not track models usage in Docker Model Runner |
| `--gpu` | `auto` |  Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| `--host` | `127.0.0.1` |  Host address to bind Docker Model Runner |
| `--port` |  |  Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode)<br> |






