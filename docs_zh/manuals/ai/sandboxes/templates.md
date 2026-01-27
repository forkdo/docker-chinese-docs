---
title: 自定义模板
description: 创建自定义沙箱模板，以标准化预装工具和配置的开发环境。
weight: 45
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

自定义模板允许您创建可重用的沙箱环境，其中包含预装的工具和配置。无需每次都要求代理安装包，而是构建一个包含所有内容的模板。

## 何时使用自定义模板

在以下情况下使用自定义模板：

- 多个团队成员需要相同的环境
- 您正在创建具有相同工具的许多沙箱
- 设置涉及复杂步骤，重复操作很繁琐
- 您需要特定版本的工具或库

对于一次性工作或简单设置，请使用默认模板并要求代理安装所需内容。

## 构建模板

从 Docker 的官方沙箱模板开始：

```dockerfile
FROM docker/sandbox-templates:claude-code

USER root

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install development tools
RUN pip3 install --no-cache-dir \
    pytest \
    black \
    pylint

USER agent
```

官方模板包含代理二进制文件、Ubuntu 基础、开发工具（Git、Docker CLI、Node.js、Python、Go）以及具有 sudo 访问权限的非 root `agent` 用户。

### USER 模式

在系统级安装时切换到 `root`，然后在最后切换回 `agent`。基础模板默认为 `USER agent`，因此您需要明确切换到 root 以进行包安装。在 Dockerfile 结束前始终切换回 `agent`，以便代理以正确的权限运行。

### 使用模板

构建您的模板：

```console
$ docker build -t my-template:v1 .
```

然后选择如何使用它：

选项 1：从本地镜像加载（快速，用于个人使用）

```console
$ docker sandbox create --template my-template:v1 \
    --load-local-template \
    claude ~/project
$ docker sandbox run <sandbox-name>
```

`--load-local-template` 标志从您的本地 Docker 守护进程中将镜像加载到沙箱 VM 中。这适用于快速迭代和个人模板。

选项 2：推送到注册表（用于共享和持久化）

```console
$ docker tag my-template:v1 myorg/my-template:v1
$ docker push myorg/my-template:v1
$ docker sandbox create --template myorg/my-template:v1 claude ~/project
$ docker sandbox run <sandbox-name>
```

推送到注册表使模板可供您的团队使用，并使其超越您的本地机器而持久存在。

## 示例：Node.js 模板

```dockerfile
FROM docker/sandbox-templates:claude-code

USER root

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install common tools
RUN npm install -g \
    typescript@5.1.6 \
    eslint@8.46.0 \
    prettier@3.0.0

USER agent
```

固定版本以实现可重现的构建。

## 使用标准镜像

您可以使用标准 Docker 镜像（如 `python:3.11` 或 `node:20`）作为基础，但它们不包含代理二进制文件或沙箱配置。

直接使用标准镜像创建沙箱但在运行时失败：

```console
$ docker sandbox create --template python:3-slim claude ~/project
✓ Created sandbox claude-sandbox-2026-01-16-170525 in VM claude-project

$ docker sandbox run claude-project
agent binary "claude" not found in sandbox: verify this is the correct sandbox type
```

要使用标准镜像，您需要安装代理二进制文件、添加沙箱依赖项、配置 shell 并设置 `agent` 用户。从 `docker/sandbox-templates:claude-code` 构建更简单。

## 与团队共享

将模板推送到注册表并进行版本控制：

```console
$ docker build -t myorg/sandbox-templates:python-v1.0 .
$ docker push myorg/sandbox-templates:python-v1.0
```

团队成员然后可以使用该模板：

```console
$ docker sandbox create --template myorg/sandbox-templates:python-v1.0 claude ~/project
```

使用版本标签（`:v1.0`、`:v2.0`）而不是 `:latest` 可确保团队中的稳定性。

## 下一步

- [有效使用沙箱](workflows.md)
- [架构](architecture.md)
- [网络策略](network-policies.md)
```