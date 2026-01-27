---
title: 从旧版沙箱迁移
description: 从基于容器的沙箱迁移到基于 microVM 的沙箱
weight: 100
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

Docker Desktop 4.58 引入了基于 microVM 的沙箱，取代了之前的基于容器的实现。本指南帮助您从旧版沙箱迁移到新架构。

## 变更内容

Docker 沙箱现在运行在轻量级 microVM 中，而非容器内。每个沙箱都拥有独立的 Docker 守护进程、更好的隔离性和网络过滤策略。

> [!NOTE]
> 如果您需要使用旧版基于容器的沙箱，请安装
> [Docker Desktop 4.57](/desktop/release-notes/#4570)。

升级到 Docker Desktop 4.58 后：

- 旧版沙箱不会出现在 `docker sandbox ls` 中
- 它们仍然作为常规的 Docker 容器和卷存在
- 您可以使用 `docker ps -a` 和 `docker volume ls` 查看它们
- 旧版沙箱无法使用新的 CLI 命令
- 运行 `docker sandbox run` 会创建一个新的基于 microVM 的沙箱

## 迁移选项

选择适合您情况的方案：

### 选项 1：重新开始（推荐）

这是针对实验性功能的最简单方法。您将使用新架构重新创建沙箱。

1. 记录旧版沙箱中任何重要的配置或已安装的软件包。
2. 移除旧版沙箱容器：

   ```console
   $ docker rm -f $(docker ps -q -a --filter="label=docker/sandbox=true")
   ```

3. 移除凭证卷：

   ```console
   $ docker volume rm docker-claude-sandbox-data
   ```

4. 创建新的 microVM 沙箱：

   ```console
   $ docker sandbox create claude ~/project
   $ docker sandbox run <sandbox-name>
   ```

5. 重新安装依赖项。让代理安装所需的工具：

   ```plaintext
   You: "Install all the tools needed to build and test this project"
   Claude: [Installs tools]
   ```

您将失去：

- API 密钥（首次运行时重新认证，或设置 `ANTHROPIC_API_KEY`）
- 已安装的软件包（通过代理重新安装）
- 自定义配置（根据需要重新配置）

您将获得：

- 更好的隔离性（microVM 对比容器）
- 用于测试容器的独立 Docker 守护进程
- 网络过滤策略
- 增强的安全性

### 选项 2：迁移配置

如果您有大量自定义设置，可以通过创建自定义模板来保留您的配置。

1. 检查旧版沙箱以查看已安装的内容：

   ```console
   $ docker exec <old-sandbox-container> dpkg -l
   ```

2. 使用您的工具创建自定义模板：

   ```dockerfile
   FROM docker/sandbox-templates:claude-code
   USER root
   # Install your tools
   RUN apt-get update && apt-get install -y \
       build-essential \
       nodejs \
       npm
   # Install language-specific packages
   RUN npm install -g typescript eslint
   # Add any custom configuration
   ENV EDITOR=vim
   USER agent
   ```

3. 构建您的模板：

   ```console
   $ docker build -t my-sandbox-template:v1 .
   ```

4. 使用您的模板创建新沙箱：

   ```console
   $ docker sandbox create --template my-sandbox-template:v1 \
       --load-local-template \
       claude ~/project
   ```

5. 运行沙箱：

   ```console
   $ docker sandbox run <sandbox-name>
   ```

如果您想与团队共享此模板，请将其推送到镜像仓库。详情请参见[自定义模板](templates.md)。

## 清理旧资源

迁移完成后，清理旧版容器和卷：

移除特定沙箱：

```console
$ docker rm -f <old-sandbox-container>
$ docker volume rm docker-claude-sandbox-data
```

移除所有已停止的容器和未使用的卷：

```console
$ docker container prune
$ docker volume prune
```

> [!WARNING]
> `docker volume prune` 会移除所有未使用的卷，而不仅仅是沙箱卷。
> 在运行此命令之前，请确保您没有其他重要的未使用卷。

## 了解差异

### 架构

旧版（基于容器）：

- 沙箱是 Docker 容器
- 出现在 `docker ps` 中
- 挂载主机 Docker 套接字以访问容器
- 将凭证存储在 Docker 卷中

新版（基于 microVM）：

- 沙箱是轻量级 microVM
- 使用 `docker sandbox ls` 查看它们
- VM 内部拥有独立的 Docker 守护进程
- 通过 `ANTHROPIC_API_KEY` 环境变量或交互式认证获取凭证

### CLI 变更

旧版命令结构：

```console
$ docker sandbox run ~/project
```

新版命令结构：

```console
$ docker sandbox run claude ~/project
```

代理名称（`claude`、`codex`、`gemini`、`cagent`、`kiro`）现在是在创建沙箱时的必需参数，您需要通过名称来运行沙箱。