# docker model stop-runner

**Description:** Stop Docker Model Runner (Docker Engine only)

**Usage:** `docker model stop-runner`



<!--
此页面由 Docker 的源代码自动生成。如果您建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交 issue 或 pull request：

https://github.com/docker/model-cli
-->








## Description

This command stops the Docker Model Runner by removing the running containers, but preserves the container images on disk. Use this command when you want to temporarily stop the runner but plan to start it again later.

To completely remove the runner including images, use `docker model uninstall-runner --images` instead.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--models` |  |  Remove model storage volume |






