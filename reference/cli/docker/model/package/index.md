---
title: docker model package
url: /reference/cli/docker/model/package/
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
  - title: docker model package
    url: /reference/cli/docker/model/package/
next:
  title: docker model logs
  url: /reference/cli/docker/model/logs/
prev:
  title: docker model pull
  url: /reference/cli/docker/model/pull/
---

**Description:** Package a GGUF file, Safetensors directory, or existing model into a Docker model OCI artifact.


**Usage:** `docker model package (--gguf <path> | --safetensors-dir <path> | --from <model>) [--license <path>...] [--context-size <tokens>] [--push] MODEL`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/model-cli
-->








## Description

Package a GGUF file, Safetensors directory, or existing model into a Docker model OCI artifact, with optional licenses. The package is sent to the model-runner, unless --push is specified.
When packaging a sharded GGUF model, --gguf should point to the first shard. All shard files should be siblings and should include the index in the file name (e.g. model-00001-of-00015.gguf).
When packaging a Safetensors model, --safetensors-dir should point to a directory containing .safetensors files and config files (*.json, merges.txt). All files will be auto-discovered and config files will be packaged into a tar archive.
When packaging from an existing model using --from, you can modify properties like context size to create a variant of the original model.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--chat-template` |  |  absolute path to chat template file (must be Jinja format) |
| `--context-size` |  |  context size in tokens |
| `--dir-tar` |  |  relative path to directory to package as tar (can be specified multiple times)<br> |
| `--from` |  |  reference to an existing model to repackage |
| `--gguf` |  |  absolute path to gguf file |
| `-l`, `--license` |  |  absolute path to a license file |
| `--push` |  |  push to registry (if not set, the model is loaded into the Model Runner content store)<br> |
| `--safetensors-dir` |  |  absolute path to directory containing safetensors files and config |






