---
title: Compose v2 版本发布说明
linkTitle: 早期版本
weight: 20
description: 了解 Docker Compose v2 的功能、错误修复和破坏性变更
keywords: 旧版本发布说明, compose
toc_max: 2
---

<!-- vale off -->

更多详细信息，请参阅 [Compose 仓库中的发布说明](https://github.com/docker/compose/releases/)。

## 2.40.3

{{< release-date date="2025-10-30" >}}

### 错误修复和增强

- 生命周期钩子现在适用于 `restart` 命令
- 改进了发布 OCI 工件时的覆盖支持
- 修复了一个问题，确保 `run` 命令只为特定服务检查镜像是否存在
- 添加了默认的 Prompt 实现


## 2.40.2

{{< release-date date="2025-10-22" >}}

### 错误修复和增强

- 添加检查，如果最低要求的 Buildx 版本未安装，则构建失败
- 移除未使用的代码，仅依赖 api.Service
- 通过检查摘要/规范引用（而不仅仅是标签）来改进镜像检测
- 引入 `WithPrompt`，添加可插拔的用户交互 UI
- 恢复对 `uid:gid` 的 secret/config 设置的修复，以匹配容器的 `USER` 定义

## 2.40.1

{{< release-date date="2025-10-17" >}}

### 错误修复和增强

- 修复了使用 bake 构建时的几个问题
- 添加了 `publish` 命令对 profiles 和 extends 的支持
- 添加了对 `CTRL+Z` 的支持，可在后台运行 Compose
- 修复了 secret/config 的 `uid:gid` 设置，以匹配容器的 `USER` 定义

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.5.1
- 依赖项升级：将 buildx 升级到 v0.29.1
- 依赖项升级：将 golang 升级到 v1.24.9

## 2.40.0

{{< release-date date="2025-10-03" >}}

### 错误修复和增强

- 添加了将 Compose 应用发布为带有镜像的 `compose.yaml` 的选项
- 修复了使用 bake 构建时对基于环境变量的 secret 的支持
- 修复了使用 bake 构建时对转义的 '$' 字符的支持

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.5.0

## 2.39.4

{{< release-date date="2025-09-19" >}}

### 错误修复和增强

- 在 Compose Develop 规范定义中添加了 `initial_sync` 属性，用于在启动 watch 会话后同步文件
- 修复了使用 bake 构建时的 TLS 问题
- 在 `run` 命令作为管道命令运行时禁用 Tty

### 更新

- 依赖项升级：将 compose-go 升级到 v2.9.0

## 2.39.3

{{< release-date date="2025-09-09" >}}

### 错误修复和增强

- 为 `--progress` 标志添加了补全
- 修复了使用 `bake` 构建时的轻微问题
- 修复了使用 bind mounts 和 `-y` 标志发布 Compose 栈时的问题

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.4.0
- 依赖项升级：将 compose-go 升级到 v2.8.2
- 依赖项升级：将 buildx 升级到 v0.28.0
- 依赖项升级：将 buildkit 升级到 v0.24.0
- 依赖项升级：将 golang 升级到 v1.24.7
- 依赖项升级：将 containerd 升级到 2.1.4

## 2.39.2

{{< release-date date="2025-08-04" >}}

### 错误修复和增强

- 修复了构建输出的多个渲染问题
- 修复了 `pull` 和 `no_cache` 属性在使用 `bake` 时未生效的问题
- 在 `up` 命令中移除了对显式未附加服务的日志显示

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.3.3
- 依赖项升级：将 golang 升级到 v1.23.12
- 依赖项升级：将 containerd 升级到 2.1.4

## 2.39.1

{{< release-date date="2025-07-24" >}}

### 错误修复和增强

- 添加了用于监控 `models` 使用情况的指标

### 更新

- 依赖项升级：将 compose-go 升级到 v2.8.1

## 2.39.0

{{< release-date date="2025-07-24" >}}

### 错误修复和增强

- 为 `config` 命令添加了 `--models` 标志以列出模型
- 为 `events` 添加了 `--since` 和 `--until` 标志
- 在 `build` 部分引入了 `provenance` 和 `sbom` 属性
- 修复了 Windows 上 `bridge convert` 的问题
- 修复了 `bake` 构建的多个问题

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.3.2
- 依赖项升级：将 buildx 升级到 v0.26.1
- 依赖项升级：将 compose-go 升级到 v2.8.0

## 2.38.2

{{< release-date date="2025-07-08" >}}

### 错误修复和增强

- 为 `config` 命令添加了 `--networks` 标志以列出网络
- 修复了 Docker Model Runner 用作提供者服务时 `down` 命令的问题
- 修复了 Docker Model Runner 进度显示问题
- 修复了有 profile 但缺少 secret 的服务的问题

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.3.1
- 依赖项升级：将 buildkit 升级到 v0.23.2
- 依赖项升级：将 golang 升级到 v1.23.10

## 2.38.1

{{< release-date date="2025-06-30" >}}

### 错误修复和增强

- 添加了对服务 `models` 配置的 `model_variable` 的支持

### 更新

- 依赖项升级：将 compose-go 升级到 v2.7.1

## 2.38.0

{{< release-date date="2025-06-30" >}}

### 错误修复和增强

- 引入了对 LLM 配置的 `models` 的支持
- 添加了 `volumes` 命令
- 移除了 bind mounts 上 `publish` 的限制
- 修复了将 docker socket 挂载到不需要它的容器的问题
- 修复了 bake 输出挂起的问题

### 更新

- 依赖项升级：将 compose-go 升级到 v2.7.0
- 依赖项升级：将 docker engine 和 cli 升级到 v28.3.0

## 2.37.3

{{< release-date date="2025-06-24" >}}

### 错误修复和增强

- 添加了对 Bake 的 `cache_to` 支持
- 修复了 Bake 集成问题
- 修复了影响 `run` 命令的多个问题

### 更新

- 依赖项升级：将 buildkit 升级到 v0.23.1

## 2.37.2

{{< release-date date="2025-06-20" >}}

### 错误修复和增强

- 引入了 `use_api_socket`
- 修复了 `compose images` JSON 输出格式
- 修复了在没有 watch 支持的项目上使用 `w` 快捷键时的 panic
- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误

### 更新

- 依赖项升级：将 compose-go 升级到 v2.6.5
- 依赖项升级：将 buildx 升级到 v0.25.0
- 依赖项升级：将 buildkit 升级到 v0.23.0

## 2.37.1

{{< release-date date="2025-06-12" >}}

### 错误修复和增强

- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误
- 将 `compose images` JSON 输出恢复为数组格式

## 2.37.0

{{< release-date date="2025-06-05" >}}

### 错误修复和增强

- 修复了随机端口分配的问题
- 修复了在内部循环期间不必要地重新创建容器的问题
- 修复了 `watch` 重建镜像时依赖服务重启的问题
- 修复了 `up --build` 与 `additional_context` 时的问题

### 更新

- 依赖项升级：将 compose-go 升级到 v2.6.4
- 依赖项升级：将 buildx 升级到 v0.24.0
- 依赖项升级：将 buildkit 升级到 v0.22.0

## 2.36.2

{{< release-date date="2025-05-23" >}}

### 错误修复和增强

- Compose Bridge 功能现在是 Compose 的一部分
- 改进了 `docker compose images` 命令的显示
- 将 `bake` 提升为 Compose 的默认构建工具
- 修复了构建流程的问题
- 修复了 `watch` 重建镜像后依赖服务的重启问题

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.2.2

## 2.36.1

{{< release-date date="2025-05-19" >}}

### 错误修复和增强

- 为 `provider` 服务的 `options` 属性引入了对数组的支持
- 在扩展协议中添加了 `debug` 消息
- 修复了尝试发布带有 `provider` 服务的 Compose 应用时的问题
- 修复了使用 `service.provider` 的 Compose 应用的构建问题
- 为 `config` 命令引入了 `--lock-image-digests` 标志

### 更新

- 依赖项升级：将 compose-go 升级到 v2.6.3
- 依赖项升级：将 containerd 升级到 2.1.0

## 2.36.0

{{< release-date date="2025-05-07" >}}

### 错误修复和增强

- 引入了 `networks.interface_name`
- 添加了对 `COMPOSE_PROGRESS` 环境变量的支持
- 为外部二进制文件添加了 `service.provider`
- 引入了构建 `--check` 标志
- 修复了在解析 Compose 文件时的多个 panic 问题

### 更新

- 依赖项升级：将 compose-go 升级到 v2.6.2
- 依赖项升级：将 docker engine 和 cli 升级到 v28.1.0
- 依赖项升级：将 containerd 升级到 2.0.5
- 依赖项升级：将 buildkit 升级到 v0.21.1

## 2.35.1

{{< release-date date="2025-04-17" >}}

### 错误修复和增强

- 修复了 bind mounts 的问题

### 更新

- 依赖项升级：将 compose-go 升级到 v2.6.0
- 依赖项升级：将 docker engine 和 cli 升级到 v28.0.4
- 依赖项升级：将 buildx 升级到 v0.22.0

## 2.35.0

{{< release-date date="2025-04-10" >}}

### 错误修复和增强

- 添加了对 [Docker Model Runner](/manuals/ai/model-runner.md) 的支持，以便轻松将 AI 模型集成到 Compose 应用中
- 添加了 `build --print` 命令，通过显示等效的 bake 文件来帮助调试复杂的构建配置
- 添加了 `volume.type=image` 以提供更灵活的容器镜像卷管理
- 为 `run` 命令添加了 `--quiet` 选项，以便在运行容器时获得更干净的输出
- 为 `config` 命令添加了 `--no-env-resolution` 选项，以查看未经环境变量替换的原始配置
- 修复了 `depends_on` 的行为，防止依赖项更改时不必要的容器重新创建
- 修复了使用 `include` 时对由环境变量定义的 secret 的支持
- 修复了卷挂载处理，确保 bind mounts 在所有场景中都能正常工作

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.1.0
- 依赖项升级：将 buildx 升级到 v0.23.0
- 依赖项升级：将 buildkit 升级到 v0.21.0

## 2.34.0

{{< release-date date="2025-03-14" >}}

### 错误修复和增强

- 添加了对 refresh `pull_policy` 值 `daily`、`weekly` 和 `every_<duration>` 的支持
- 在 `watch` 定义中引入了 `include` 属性以匹配文件模式
- 为 `docker compose run` 命令引入了 `--env-from-file` 标志
- 将 `publish` 提升为 Compose 的常规命令
- 修复了在选择服务后加载 `env_file` 的问题

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.0.1
- 依赖项升级：将 buildkit 升级到 v0.17.1
- 依赖项升级：将 compose-go 升级到 v2.4.9
- 依赖项升级：将 buildx 升级到 v0.21.2

## 2.33.1

{{< release-date date="2025-02-21" >}}

### 错误修复和增强

- 添加了对 `gw_priority`、`enable_ipv4`（需要 Docker v28.0）的支持
- 修复了导航菜单的问题
- 改进了对只读服务使用非文件 secret/config 的错误消息

### 更新

- 依赖项升级：将 docker engine 和 cli 升级到 v28.0.0

## 2.33.0

{{< release-date date="2025-02-13" >}}

### 错误修复和增强

- 引入了对 Bake 的使用提示
- 引入了对引用另一个服务的 `additional_context` 属性的支持
- 添加了对 `BUILDKIT_PROGRESS` 的支持
- Compose 现在会在发布的 Compose 应用包含环境变量时发出警告
- 添加了 `--with-env` 标志以发布带有环境变量的 Compose 应用
- 更新了 `ls --quiet` 的帮助描述
- 修复了委托构建给 Bake 的多个问题
- 更新了 `stats` 命令的帮助
- 修复了对 "builtin" seccomp 配置文件的支持
- 修复了 `watch` 与多个服务的兼容性
- 移除了旧版指标系统使用的每种错误类型的退出代码
- 修复了 `compatibility` 的测试覆盖率
- 移除了发送到 OpenTelemetry 的原始 os.Args
- 启用了 copyloopvar linter
- 为二进制文件生成 provenance 并生成 SBOM
- 文档上游验证的主分支现在使用
- 添加了代码所有者文件
- 将 Docker Engine v28.x 添加到测试矩阵中

### 更新

- 依赖项升级：将 compose-go 升级到 v2.4.8
- 依赖项升级：将 buildx 升级到 v0.20.1
- 依赖项升级：将 docker 升级到 v27.5.1
- 依赖项升级：将 golangci-lint 升级到 v1.63.4
- 依赖项升级：将 golang.org/x/sys 从 0.28.0 升级到 0.30.0
- 依赖项升级：将 github.com/moby/term 升级到 v0.5.2
- 依赖项升级：将 github.com/otiai10/copy 从 1.14.0 升级到 1.14.1
- 依赖项升级：将 github.com/jonboulle/clockwork 从 0.4.0 升