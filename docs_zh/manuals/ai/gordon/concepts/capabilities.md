---
title: Gordon 的能力
linkTitle: 能力
description: 了解 Gordon 能做什么以及它可以访问的工具
weight: 10
---

{{< summary-bar feature_name="Gordon" >}}

Gordon 结合了多种能力来处理 Docker 工作流。本页介绍 Gordon 能做什么以及它使用的工具。

## 核心能力

Gordon 使用五种能力来代表你采取行动：

- 用于特定 Docker 任务的专用子智能体
- 用于运行命令的 Shell 访问
- 用于读写文件的文件系统访问
- Docker 文档与最佳实践知识库
- 用于获取外部资源的网络访问

## 内部架构

Gordon 使用一个处理大多数任务的主智能体，以及一个用于特定工作流的专用子智能体：

- **主智能体**：处理所有 Docker 操作、软件开发、容器化以及通用开发任务
- **DHI 迁移子智能体**：用于将 Dockerfile 迁移到 Docker Hardened Images 的专用处理程序

主智能体负责：

- 创建 Docker 资产（Dockerfile、compose.yaml、.dockerignore）
- 优化 Dockerfile 以减小镜像大小并提升构建性能
- 运行 Docker 命令（ps、logs、exec、build、compose）
- 调试容器问题并分析配置
- 编写和审查多种编程语言的代码
- 通用的开发问题和任务

当你请求 DHI 迁移时，Gordon 会自动委派给 DHI 迁移子智能体。

## Shell 访问

Gordon 在你批准后会在你的环境中执行 shell 命令。这包括 Docker CLI 命令、系统实用程序以及特定于应用的工具。

Gordon 可能运行的示例命令：

```console
$ docker ps
$ docker logs container-name
$ docker exec -it container-name bash
$ grep "error" app.log
```

命令以你的用户权限运行。除非你明确授予，否则 Gordon 无法访问 `sudo`。

## 文件系统访问

Gordon 读取和写入你系统上的文件。它可以分析 Dockerfile、读取配置文件、扫描目录并解析日志，且无需批准。写入文件需要你的批准。

工作目录为文件操作设置了默认上下文，但 Gordon 在需要时可以访问此目录之外的文件。

## 知识库

Gordon 使用检索增强生成来访问 Docker 文档、最佳实践、故障排除步骤和安全建议。这让 Gordon 能够准确回答问题、解释错误，并提出遵循 Docker 指南的解决方案。

## 网络访问

Gordon 获取外部网络资源来查找错误消息、包版本和框架文档。这有助于调试需要 Docker 自身文档之外上下文的问题。

Gordon 无法访问需要身份验证的私有资源，且外部请求受到速率限制。

## 与其他工具协作

Gordon 专注于 Docker 工作流，是对通用 AI 编码助手的补充。使用 Cursor 或 GitHub Copilot 等工具处理应用代码和重构，使用 Gordon 处理容器化、部署配置和 Docker 操作。它们配合良好。
