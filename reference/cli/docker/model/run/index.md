---
title: docker model run
url: /reference/cli/docker/model/run/
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
  - title: docker model run
    url: /reference/cli/docker/model/run/
next:
  title: docker model rm
  url: /reference/cli/docker/model/rm/
prev:
  title: docker model start-runner
  url: /reference/cli/docker/model/start-runner/
---

**Description:** Run a model and interact with it using a submitted prompt or chat mode

**Usage:** `docker model run MODEL [PROMPT]`



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/model-cli
-->








## Description

When you run a model, Docker calls an inference server API endpoint hosted by the Model Runner through Docker Desktop. The model stays in memory until another model is requested, or until a pre-defined inactivity timeout is reached (currently 5 minutes).

You do not have to use Docker model run before interacting with a specific model from a host process or from within a container. Model Runner transparently loads the requested model on-demand, assuming it has been pulled and is locally available.

You can also use chat mode in the Docker Desktop Dashboard when you select the model in the **Models** tab.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--color` | `no` |  Use colored output (auto|yes|no) |
| `--debug` |  |  Enable debug logging |
| `-d`, `--detach` |  |  Load the model in the background without interaction |
| `--ignore-runtime-memory-check` |  |  Do not block pull if estimated runtime memory for model exceeds system resources.<br> |



## Examples

### One-time prompt

```console
docker model run ai/smollm2 "Hi"
```

Output:

```console
Hello! How can I assist you today?
```

### Interactive chat

```console
docker model run ai/smollm2
```

Output:

```console
> Hi
Hi there! It's SmolLM, AI assistant. How can I help you today?
> /bye
```

### Pre-load a model

```console
docker model run --detach ai/smollm2
```

This loads the model into memory without interaction, ensuring maximum performance for subsequent requests.



