---
datafolder: scout-cli
datafile: docker_scout_integration_configure
aliases:
- /engine/reference/commandline/scout_integration_configure
title: docker scout integration configure
layout: cli
---

<!--
此页面由 Docker 源代码自动生成。如果您想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单：

https://github.com/docker/scout-cli
-->

{{% include "scout-early-access.md" %}}

## 概述

配置集成

## 用法

```bash
docker scout integration configure [OPTIONS]
```

## 描述

`docker scout integration configure` 命令配置集成。

## 选项

| 选项 | 描述 |
| --- | --- |
| `--description` | 集成的可选描述 |
| `--help` | 显示使用信息 |
| `--name` | 集成的名称 |
| `--org` | 要在其中配置集成的组织 |
| `--provider` | 集成的提供者 |
| `--repo` | 集成的仓库（格式：owner/name） |
| `--token` | 用于配置集成的令牌 |
| `--url` | 集成的 URL |

## 父命令

| 命令 | 描述 |
| --- | --- |
| [docker scout integration](docker_scout_integration.md) | 管理集成 |

## 相关资源

- [Docker Scout 文档](https://docs.docker.com/scout/)
- [Docker Scout CLI 参考](https://docs.docker.com/scout/cli-reference/)