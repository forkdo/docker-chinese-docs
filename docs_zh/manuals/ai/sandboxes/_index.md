---
title: Docker 沙盒
description: 在隔离环境中运行 AI 代理
weight: 20
params:
  sidebar:
    group: AI
    badge:
      color: violet
      text: 实验性功能
---

{{< summary-bar feature_name="Docker 沙盒" >}}

Docker 沙盒简化了在本地机器上安全运行 AI 代理的过程。它专为使用 Claude Code 等编码代理进行开发的开发者设计，通过沙盒将代理与本地机器隔离，同时保持熟悉的开发体验。使用 Docker 沙盒，代理可以在容器化工作空间内执行命令、安装包和修改文件，该工作空间与您的本地目录保持一致。这在保证安全的前提下，赋予了代理完全的自主性。

## 工作原理

当您运行 `docker sandbox run <agent>` 时：

1. Docker 从模板镜像创建一个容器，并将您的当前工作目录挂载到容器中的相同路径。

2. Docker 会发现您的 Git `user.name` 和 `user.email` 配置，并将其注入容器中，这样代理提交的代码将归属到您名下。

3. 首次运行时，系统会提示您进行身份验证。凭据将存储在 Docker 卷中，并在未来的沙盒代理中重复使用。

4. 代理在容器内启动，并启用绕过权限。

### 工作空间挂载

您的工作空间目录被挂载到容器中的相同绝对路径（在 macOS 和 Linux 上）。例如，主机上的 `/Users/alice/projects/myapp` 在容器中也是 `/Users/alice/projects/myapp`。这意味着：

- 错误消息中的文件路径与主机匹配
- 包含硬编码路径的脚本可以按预期工作
- 工作空间文件的更改在主机和容器上都能立即可见

### 每个工作空间一个沙盒

Docker 强制执行每个工作空间一个沙盒。当您在同一目录中运行 `docker sandbox run <agent>` 时，Docker 会重用现有的容器。这意味着状态（已安装的包、临时文件等）会在该工作空间的代理会话之间持续存在。

> [!NOTE]
> 要更改沙盒的配置（环境变量、挂载的卷等），您需要删除并重新创建它。详情请参阅 [管理沙盒](advanced-config.md#managing-sandboxes)。

## 发布状态

Docker 沙盒是一个实验性功能。功能和设置可能会发生变化。

在 GitHub 上报告问题：
- [Docker Desktop for Mac](https://github.com/docker/for-mac)
- [Docker Desktop for Windows](https://github.com/docker/for-win)
- [Docker Desktop for Linux](https://github.com/docker/desktop-linux)

## 开始使用

请前往 [入门指南](get-started.md) 运行您的第一个沙盒代理。