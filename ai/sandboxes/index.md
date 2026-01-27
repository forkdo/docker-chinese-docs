# Docker 沙箱




Docker 沙箱让您可以在机器上的隔离环境中运行 AI 编程代理。如果您正在使用像 Claude Code 这样的代理进行开发，沙箱提供了一种安全的方式，既能赋予代理自主权，又不会危及您的系统安全。

## 为何使用 Docker 沙箱

AI 代理需要执行命令、安装软件包和测试代码。如果直接在主机上运行它们，意味着它们可以完全访问您的文件、进程和网络。Docker 沙箱将代理隔离在微虚拟机（microVM）中，每个微虚拟机都有自己的 Docker 守护进程。代理可以在其中启动测试容器并修改其环境，而不会影响您的主机。

您将获得：

- 代理自主权，同时避免主机系统风险
- 专用的 Docker 守护进程，用于运行测试容器
- 主机与沙箱之间的文件共享
- 网络访问控制

有关 Docker 沙箱与其他隔离编程代理方法的比较，请参阅[与其他方案的比较](./architecture.md#comparison-to-alternatives)。

> [!NOTE]
> 基于微虚拟机的沙箱需要 macOS 或 Windows（实验性支持）。Linux 用户可以使用基于传统容器的沙箱，需配合 [Docker Desktop 4.57](/desktop/release-notes/#4570) 使用。

## 如何使用沙箱

要创建并运行一个沙箱：

```console
$ docker sandbox run claude ~/my-project
```

此命令会为您的项目空间（`~/my-project`）创建一个沙箱，并在其中启动 Claude Code 代理。现在，代理可以在隔离的沙箱环境中处理您的代码、安装工具并运行容器。

## 工作原理

沙箱运行在带有专用 Docker 守护进程的轻量级微虚拟机中。每个沙箱都是完全隔离的——代理在虚拟机内运行，无法访问您的主机 Docker 守护进程、容器或项目空间之外的文件。

您的项目目录会在主机和沙箱之间以相同的绝对路径同步，因此错误消息中的文件路径在两个环境中保持一致。

沙箱不会出现在您主机上的 `docker ps` 命令输出中，因为它们是虚拟机，而不是容器。请使用 `docker sandbox ls` 命令查看它们。

有关架构、隔离模型和网络的技术细节，请参阅[架构](architecture.md)。

### 多个沙箱

为不同的项目创建独立的沙箱：

```console
$ docker sandbox run claude ~/project-a
$ docker sandbox run claude ~/project-b
```

每个沙箱都与其他沙箱完全隔离。沙箱会持续存在，直到您手动删除它们，因此已安装的软件包和配置会为该工作空间保留。

## 支持的代理

Docker 沙箱支持多种 AI 编程代理：

- **Claude Code** - Anthropic 的编程代理
- **Codex** - OpenAI 的 Codex 代理（部分支持；开发中）
- **Gemini** - Google 的 Gemini 代理（部分支持；开发中）
- **cagent** - Docker 的 [cagent](/ai/cagent/)（部分支持；开发中）
- **Kiro** - AWS 开发（部分支持；开发中）

## 开始使用

请前往[入门指南](get-started.md)运行您的第一个沙箱代理。

## 故障排除

有关常见配置错误，请参阅[故障排除](./troubleshooting)，或在 [Docker Desktop 问题追踪器](https://github.com/docker/desktop-feedback) 上报告问题。
