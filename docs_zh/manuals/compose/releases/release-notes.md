---
title: Docker Compose v5 发布说明
linkTitle: 发布说明
weight: 10
description: 了解最新 Docker Compose 版本的新功能、错误修复和破坏性变更
keywords: release notes, compose
tags: [release-notes]
toc_max: 2
aliases:
- /release-notes/docker-compose/
- /compose/release-notes/
---

<!-- vale off -->

更多详细信息，请参阅 [Compose 仓库中的发布说明](https://github.com/docker/compose/releases/)。

## 5.0.1

{{< release-date date="2025-12-18" >}}

### 错误修复和增强功能

- 恢复了对 `COMPOSE_COMPATIBILITY` 的支持。
- 修复了代码中的语法错误并提高了清晰度。
- 修复了损坏的 `run --quiet`。
- 修复了 SDK 示例。
- 在比较之前添加了检查 buildx 版本是否已设置。
- 修复了语法：将 'service' 复数化并删除了撇号。
- 修复了进度 UI 在操作后无法恢复终端的问题。
- 修复了进度 UI 中的状态对齐问题。
- 恢复了拉取时的镜像层下载进度详细信息。
- 在模型配置阶段结束时添加了 'configured' 事件。
- 引入了构建标签以选择观察器实现。
- 在 README 中删除了对 v2 的提及。
- 修复了 setEnvWithDotEnv 中缺少的错误处理。
- 采用 morikuni/aec 库代替原始 ANSI 序列。
- 防止错误的进度指标破坏 compose。
- 恢复了对 `BUILDKIT_PROGRESS` 的支持。
- 添加了检查模型插件是否成功加载。
- 在未选择要构建的服务时添加了警告。

### 更新

- 依赖项升级：golang 升级至 1.24.11
- 依赖项升级：osxcross 升级
- 依赖项升级：golang.org/x/sys 升级至 0.39.0
- 依赖项升级：github.com/docker/cli-docs-tool 升级至 0.11.0
- 依赖项升级：golang.org/x/sync 升级至 0.19.0
- 依赖项升级：tags.cncf.io/container-device-interface 升级至 1.1.0
- 依赖项升级：github.com/moby/buildkit 升级至 0.26.3

## 5.0.0

{{< release-date date="2025-12-02" >}}

此版本的主要变更：

- Compose v5 引入了新的官方 Go SDK。该 SDK 提供了一个全面的 API，可让您将 Compose 功能直接集成到应用程序中，从而允许您加载、验证和管理多容器环境，而无需依赖 Compose CLI。更多信息，请参阅 [Compose SDK 文档](/manuals/compose/compose-sdk.md)。

> [!NOTE]
>
> 为避免与标记为“v2”和“v3”的旧版 Compose 文件格式混淆，版本号直接提升至 v5。

### 错误修复和增强功能

- 放弃了对内部 buildkit 构建器的支持。
- 引入了使用功能参数的 Compose SDK。
- 引入了抽象以支持 SDK 使用，而无需 Docker CLI。
- 使进度 Writer 成为可配置的 CLI 组件。
- 将进度包移至 cmd 作为 CLI 组件。
- 向 SDK 添加了加载项目功能。
- 引入了 SDK 文档。
- 记录了对 OCI 和 Git 远程资源的支持。
- 添加了对重启时运行钩子的支持。
- 修复了现有镜像检查，以便在 run 命令中仅选择目标服务。
- 引入了 `--insecure-registry` 标志，保留用于测试目的。
- 添加了对 `build.no_cache_filter` 的支持。
- 向 `docker compose start` 命令添加了 `--wait` 选项。
- 修复了 OCI Compose 覆盖支持。
- 修复了 `exec --no-tty` 选项的帮助输出。
- 修复了错误消息中的拼写错误。
- 当使用 `--print` 运行构建时禁用了进度 UI。
- 恢复了对分离键的支持。
- 修复了 images 命令以显示镜像的创建时间。
- 修复了对端口范围的支持。
- 修复了 publish 命令中对 includes 的支持。
- 在模型配置中忽略运行时标志。

### 更新

- 依赖项升级：compose go 升级至 v2.10.0
- 依赖项升级：docker 升级至 28.5.2
- 依赖项升级：containerd 升级至 2.2.0
- 依赖项升级：docker/cli 升级至 28.5.2
- 依赖项升级：buildx 升级至 v0.30.0，buildkit 升级至 v0.26.0，otel 升级至 v1.38.0，otel/contrib 升级至 v0.63.0
- 依赖项升级：golang.org/x/sys 升级至 0.38.0
- 依赖项升级：golang.org/x/sync 升级至 0.18.0
- 依赖项升级：github.com/hashicorp/go-version 升级至 1.8.0
- 依赖项升级：golang.org/x/crypto 升级至 v0.45.0
- Dockerfile：golangci-lint 升级至 v2.6.2