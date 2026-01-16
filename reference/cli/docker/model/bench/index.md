---
title: docker model bench
url: /reference/cli/docker/model/bench/
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
  - title: docker model bench
    url: /reference/cli/docker/model/bench/
prev:
  title: docker model inspect
  url: /reference/cli/docker/model/inspect/
---

**Description:** Benchmark a model's performance at different concurrency levels

**Usage:** `docker model bench [MODEL]`



<!--
此页面是从 Docker 的源代码自动生成的。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提交工单或拉取请求：

https://github.com/docker/model-cli
-->








## Description

Benchmark a model's performance showing tokens per second at different concurrency levels.

This command runs a series of benchmarks with 1, 2, 4, and 8 concurrent requests by default,
measuring the tokens per second (TPS) that the model can generate.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--concurrency` | `[1,2,4,8]` |  Concurrency levels to test |
| `--duration` | `30s` |  Duration to run each concurrency test |
| `--json` |  |  Output results in JSON format |
| `--prompt` | `Write a comprehensive 100 word summary on whales and their impact on society.
` |  Prompt to use for benchmarking |
| `--timeout` | `5m0s` |  Timeout for each individual request |






