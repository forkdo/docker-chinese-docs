---
title: Docker Compose v5 发布说明
linkTitle: 发布说明
weight: 10
description: 了解最新 Docker Compose 版本的新功能、错误修复和破坏性变更
keywords: 发布说明, compose
tags: [发布说明]
toc_max: 2
aliases:
- /release-notes/docker-compose/
- /compose/release-notes/
---

<!-- vale off -->

更详细的信息，请参见 [Compose 仓库中的发布说明](https://github.com/docker/compose/releases/)。

## 5.0.0

{{< release-date date="2025-12-02" >}}

本版本的主要变更：

- Compose v5 引入了一个新的官方 Go SDK。该 SDK 提供了一个全面的 API，允许您直接将 Compose 功能集成到应用程序中，从而无需依赖 Compose CLI 即可加载、验证和管理多容器环境。更多信息请参见 [Compose SDK 文档](/manuals/compose/compose-sdk.md)。

> [!NOTE]
>
> 为了避免与标记为“v2”和“v3”的旧版 Compose 文件格式混淆，版本号直接推进到 v5。

### 错误修复和增强

- 移除了对内部 buildkit 构建器的支持。
- 引入了使用函数式参数的 Compose SDK。
- 引入了抽象层以支持在不依赖 Docker CLI 的情况下使用 SDK。
- 将进度写入器（progress Writer）设为可配置的 CLI 组件。
- 将 progress 包移至 cmd 作为 CLI 组件。
- 在 SDK 中添加了加载项目（load project）函数。
- 引入了 SDK 文档。
- 记录了对 OCI 和 Git 远程资源的支持。
- 添加了对重启时运行钩子（run hooks）的支持。
- 修复了 run 命令中检查现有镜像的逻辑，仅选择目标服务。
- 引入了 `--insecure-registry` 标志，仅用于测试目的。
- 添加了对 `build.no_cache_filter` 的支持。
- 为 `docker compose start` 命令添加了 `--wait` 选项。
- 修复了 OCI Compose 覆盖支持。
- 修复了 `exec --no-tty` 选项的帮助输出。
- 修复了错误消息中的一个拼写错误。
- 当使用 `--print` 运行构建时禁用进度 UI。
- 恢复了对分离键（detach keys）的支持。
- 修复了 images 命令以显示镜像创建时间。
- 修复了对端口范围的支持。
- 修复了 publish 命令中对 includes 的支持。
- 在模型配置中忽略运行时标志。

### 更新

- 依赖项升级：将 compose go 升级至 v2.10.0
- 依赖项升级：将 docker 升级至 28.5.2
- 依赖项升级：将 containerd 升级至 2.2.0
- 依赖项升级：将 docker/cli 升级至 28.5.2
- 依赖项升级：将 buildx 升级至 v0.30.0，buildkit 升级至 v0.26.0，otel 升级至 v1.38.0，otel/contrib 升级至 v0.63.0
- 依赖项升级：将 golang.org/x/sys 升级至 0.38.0
- 依赖项升级：将 golang.org/x/sync 升级至 0.18.0
- 依赖项升级：将 github.com/hashicorp/go-version 升级至 1.8.0
- 依赖项升级：将 golang.org/x/crypto 升级至 v0.45.0
- Dockerfile：将 golangci-lint 更新至 v2.6.2