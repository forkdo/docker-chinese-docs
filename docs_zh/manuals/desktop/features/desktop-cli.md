---
title: 使用 Docker Desktop CLI
linkTitle: Docker Desktop CLI
weight: 100
description: 如何使用 Docker Desktop CLI
keywords: cli, docker desktop, macos, windows, linux
---

{{< summary-bar feature_name="Docker Desktop CLI" >}}

Docker Desktop CLI 允许你直接从命令行执行启动、停止、重启和更新 Docker Desktop 等关键操作。

Docker Desktop CLI 提供以下功能：

- 简化本地开发自动化：在脚本和测试中更高效地执行 Docker Desktop 操作。
- 改进的开发者体验：从命令行重启、退出或重置 Docker Desktop，减少对 Docker Desktop 仪表板的依赖，提升灵活性和效率。

## 用法

```console
docker desktop COMMAND [OPTIONS]
```

## 命令

| 命令                 | 描述                                     |
|:---------------------|:-----------------------------------------|
| `start`              | 启动 Docker Desktop                      |
| `stop`               | 停止 Docker Desktop                      |
| `restart`            | 重启 Docker Desktop                      |
| `status`             | 显示 Docker Desktop 的运行或停止状态     |
| `engine ls`          | 列出可用的引擎（仅限 Windows）           |
| `engine use`         | 在 Linux 和 Windows 容器之间切换（仅限 Windows） |
| `update`             | 管理 Docker Desktop 更新。仅在 Mac 上 Docker Desktop 4.38 版本，或所有操作系统上的 4.39 及更高版本中可用。 |
| `logs`               | 打印日志条目                             |
| `disable`            | 禁用功能                                 |
| `enable`             | 启用功能                                 |
| `version`            | 显示 Docker Desktop CLI 插件版本信息     |
| `kubernetes`         | 列出 Docker Desktop 使用的 Kubernetes 镜像或重启集群。在 Docker Desktop 4.44 及更高版本中可用。 |

有关每个命令的详细信息，请参阅 [Docker Desktop CLI 参考文档](/reference/cli/docker/desktop/_index.md)。