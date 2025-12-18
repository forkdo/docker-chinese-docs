---
title: Docker 术语
description: Docker 特定的术语和定义
keywords: 术语, 风格指南, 贡献
---

#### `compose.yaml`

Compose 文件的当前命名，因为它是一个文件，所以格式化为代码。

#### Compose 插件

作为 Docker CLI 的可启用/禁用的附加组件的 compose 插件。

#### Digest（摘要）

每次推送镜像时自动生成的长字符串。你可以通过 Digest 或 Tag 拉取镜像。

#### Docker Compose

当我们谈论应用程序或与该应用程序相关的所有功能时使用。

#### `docker compose`

在文本和命令使用示例/代码样本中，使用代码格式引用命令。

#### Docker Compose CLI

当引用 Docker CLI 提供的 Compose 命令系列时使用。

#### K8s

请勿使用。改用 `Kubernetes`。

#### 多平台（Multi-platform）

（广义）Mac vs Linux vs Microsoft，也指平台架构对，例如 Linux/amd64 和 Linux/arm64；（狭义）Windows/Linux/macOS。

#### 多架构 / 多架构（Multi-architecture / multi-arch）

当特指 CPU 架构或基于硬件架构的内容时使用。避免将其用作与多平台相同的意思。

#### 成员（Member）

Docker Hub 上属于某个组织的用户。

#### 命名空间（Namespace）

组织或用户名。每个镜像都需要一个命名空间来归属。

#### 节点（Node）

在 Swarm 模式下运行 Docker Engine 实例的物理或虚拟机。
管理节点（Manager nodes）执行 Swarm 管理和编排任务。默认情况下，管理节点也是工作节点。
工作节点（Worker nodes）执行任务。

#### 注册表（Registry）

Docker 镜像的在线存储。

#### 仓库（Repository）

允许用户与团队、客户或 Docker 社区共享容器镜像。