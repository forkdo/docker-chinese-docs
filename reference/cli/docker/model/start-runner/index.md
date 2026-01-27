# docker model start-runner

**Description:** Start Docker Model Runner (Docker Engine only)

**Usage:** `docker model start-runner`



<!--
本页内容由 Docker 源代码自动生成。如果您希望
建议对此处显示的文本进行修改，请在 GitHub 上的源仓库中
提交工单或拉取请求：

https://github.com/docker/model-cli
-->








## Description

This command starts the Docker Model Runner without pulling container images. Use this command to start the runner when you already have the required images locally.

For the first-time setup or to ensure you have the latest images, use `docker model install-runner` instead.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--backend` |  |  Specify backend (llama.cpp|vllm). Default: llama.cpp |
| `--debug` |  |  Enable debug logging |
| `--do-not-track` |  |  Do not track models usage in Docker Model Runner |
| `--gpu` | `auto` |  Specify GPU support (none|auto|cuda|rocm|musa|cann) |
| `--port` |  |  Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode)<br> |






