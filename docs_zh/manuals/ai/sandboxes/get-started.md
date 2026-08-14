---
title: 开始使用 Docker Sandboxes
linkTitle: 入门指南
weight: 10
description: 安装 sbx CLI、配置凭据，并完成你的第一个沙箱会话。
keywords: sandbox, sbx, get started, install, credentials, clone mode, network policy
---

Docker Sandboxes 在隔离的 microVM 沙箱中运行 AI 编程 agent。每个沙箱都有自己的 Docker 守护
进程、文件系统和网络——agent 可以构建容器、安装包、修改文件，而无需触及你的宿主系统。

本页讲解你的第一个会话：安装 CLI、在沙箱中运行 agent、了解沙箱如何隔离它、控制它能在网络上
到达什么，并进行清理。

## 先决条件

{{< tabs group="os" >}}
{{< tab name="macOS" >}}

- macOS Sonoma（版本 14）或更高
- Apple 芯片
- 你要使用的 agent 的 API 密钥或认证方式。多数 agent 需要其模型提供方（Anthropic、OpenAI、
  Google 等）的 API 密钥。有关提供方特定的说明，请参阅 [agent 页面](agents/)。

{{< /tab >}}
{{< tab name="Windows" >}}

- 64 位 Intel 或 AMD（x86_64）
- Windows 11
- 已启用 Windows Hypervisor Platform。打开提升权限的 PowerShell 提示符（以管理员身份运行）并运行：
  ```powershell
  Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform -All
  ```
- 你要使用的 agent 的 API 密钥或认证方式。多数 agent 需要其模型提供方（Anthropic、OpenAI、
  Google 等）的 API 密钥。有关提供方特定的说明，请参阅 [agent 页面](agents/)。

{{< /tab >}}
{{< tab name="Linux (Ubuntu)" >}}

- Ubuntu 24.04 或更高
- 64 位 Intel 或 AMD（x86_64）或 64 位 Arm（aarch64）
- CPU 支持并启用 KVM 硬件虚拟化。如果你在 VM 内运行，必须开启嵌套虚拟化。验证 KVM 是否可用：
  ```console
  $ lsmod | grep kvm
  ```
  正常设置会在输出中显示 `kvm_intel`、`kvm_amd`、`kvm_arm64` 或 `kvm`。如果输出为空，运行
  `kvm-ok` 进行诊断。如果 KVM 不可用，`sbx` 将无法启动。
- 你的用户在 `kvm` 组中：
  ```console
  $ sudo usermod -aG kvm $USER
  ```
  注销并重新登录（或运行 `newgrp kvm`）以使组更改生效。
- 你要使用的 agent 的 API 密钥或认证方式。多数 agent 需要其模型提供方（Anthropic、OpenAI、
  Google 等）的 API 密钥。有关提供方特定的说明，请参阅 [agent 页面](agents/)。

{{< /tab >}}
{{< /tabs >}}

如果你在虚拟桌面基础设施（VDI）环境中运行 `sbx`，该环境必须支持嵌套虚拟化。

使用 `sbx` 不需要 Docker Desktop。

## 安装并登录

{{< tabs group="os" >}}
{{< tab name="macOS" >}}

```console
$ brew trust docker/tap
$ brew install docker/tap/sbx
$ sbx login
```

{{< /tab >}}
{{< tab name="Windows" >}}

```powershell
> winget install -h Docker.sbx
> sbx login
```

{{< /tab >}}
{{< tab name="Linux (Ubuntu)" >}}

```console
$ curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
$ sudo apt-get install docker-sbx
$ sbx login
```

第一条命令将 Docker 的 `apt` 仓库添加到你的系统。

{{< /tab >}}
{{< /tabs >}}

如果你需要手动安装 `sbx`，直接从
[sbx-releases](https://github.com/docker/sbx-releases/releases) 仓库下载二进制文件。

`sbx login` 打开浏览器进行 Docker OAuth。

> [!NOTE]
> 有关为何需要登录以及你的数据会发生什么，请参阅 [FAQ](faq.md)。

## 为你的 agent 认证

对于使用 Claude 订阅（Max、Team 或 Enterprise）的 Claude Code，无需前期设置——在沙箱内使用
`/login` 命令通过 OAuth 登录。会话 token 保留在你的宿主机上，从不存储在沙箱内。

如果你倾向于用 API 密钥认证，请参阅 [凭据](security/credentials.md) 了解如何用 `sbx secret set`
存储一个。

要给 agent 访问 GitHub 以创建 pull request 或与仓库交互：

```console
$ sbx secret set github -t "$(gh auth token)"
```

## 运行你的第一个沙箱

选择一个项目目录，用 [`sbx run`](/reference/cli/sbx/run/) 启动一个 agent：

```console
$ cd ~/my-project
$ sbx run --name my-sandbox claude
```

首次运行沙箱时，CLI 会提示你选择默认网络预设：

```plaintext
Initialize the global network policy for your sandboxes:

  Applies to all sandboxes, current and future — change it later with
  "sbx policy allow/deny/rm". Kits, including built-in agent kits, may
  also add per-sandbox rules.

     1. Open         — All network traffic allowed, no restrictions.
  ❯  2. Balanced     — Default deny, with common dev sites allowed.
     3. Locked Down  — All network traffic blocked unless you allow it.

  Use ↑/↓ or 1–3 to navigate, Enter to confirm, Esc to cancel.
```

**Balanced** 是一个不错的起点——它允许到常见开发服务的流量，同时阻止其他一切。你也可以稍后
调整个别规则。每个选项的完整说明请参阅 [本地策略](governance/access-controls/local.md)。

将 `claude` 替换为你想使用的 agent——完整列表请参阅 [Agents](agents/)。

首次运行需要稍长时间，因为要拉取 agent 镜像。后续运行复用缓存的镜像，几秒内即可启动。

这会让你连接到运行在沙箱内的 agent。给它一个真实任务——让它添加功能、安装依赖，或构建并运行
你的项目。agent 拥有完整的 Linux 环境及其自己的 Docker 守护进程，因此它可以在工作时自行安装
包、构建镜像、启动容器。

## 查看 agent 能触及什么

从另一个终端，列出你的沙箱：

```console
$ sbx ls
SANDBOX       AGENT    STATUS    PORTS   WORKSPACE
my-sandbox    claude   running           ~/my-project
```

每一行显示一个沙箱的名称、其中运行的 agent、其状态、任何
[已发布端口](usage.md#publish-ports)，以及它的 workspace——共享进沙箱的宿主目录。那个 workspace
是 agent 能看到的你机器上的唯一部分。

默认情况下，workspace 以读写方式共享，因此 agent 和你的宿主机看到相同的文件。agent 对你的
项目所做的编辑会在写入时出现在你的工作树中，你在提交前作为普通的 Git diff 审查它们。

其他一切都在 microVM 内运行，与你的宿主隔离：

- agent 有自己的文件系统、Docker 守护进程和网络。
- 它安装的包、拉取的镜像、启动的容器都留在沙箱内。你的宿主系统不受影响，移除沙箱会丢弃它们。

如果你宁愿 agent 根本不触及你的工作树——例如在一个仓库上运行多个 agent 时——请使用
[clone 模式](usage.md#clone-mode)，它给 agent 一个私有克隆。

## 控制 agent 能到达什么

隔离不仅是关于文件系统。你还控制沙箱能在网络上到达什么。你在沙箱启动前选择了默认策略，并且
可以随时检查或调整它。

检查哪些规则生效：

```console
$ sbx policy ls
```

要允许特定主机：

```console
$ sbx policy allow network registry.npmjs.org
```

使用 **Locked Down** 时，即使你的模型提供方 API 也会被阻止，除非你显式允许。使用 **Balanced**
时，常见开发服务默认被允许。完整的规则集及如何自定义请参阅
[本地策略](governance/access-controls/local.md)。

## 清理

沙箱在 agent 退出后仍然存在，因此你可以停止一个，稍后从你离开的地方继续：

```console
$ sbx stop my-sandbox
```

已安装的包、Docker 镜像和配置更改在重启期间保留。当你用完一个沙箱后，移除它以回收磁盘空间：

```console
$ sbx rm my-sandbox
```

移除沙箱会删除其中的一切——已安装的包、Docker 镜像，以及如果你使用了 clone 模式的沙箱内
Git 克隆。你宿主工作树中的文件不受影响。

## 下一步

你已运行了一个 agent，了解了沙箱如何隔离它，并控制了它的网络访问。从这里有几个方向。

不带参数运行 `sbx` 打开交互式仪表板：每个沙箱的实时视图，你可以在一个地方连接 agent、打开
shell 并管理网络规则。

![交互式仪表板显示沙箱状态、资源使用情况和网络治理控制。](images/sbx-dashboard.png)

然后探索：

- [使用指南](usage.md) — 基本命令、重新连接、工作区和端口发布。
- [工作流模式](workflows.md) — Git 策略、本地服务、CI 和认证工具。
- [用 kits 定制](customize/) — 将一个 agent、它的工具和它的网络规则打包成一个可复用的定义，
  用单个标志启动。
- [Agents](agents/) — 受支持 agent 的完整列表，以及如何配置每个。
- [治理](governance/) — 在团队中集中管理网络、文件系统和 MCP 策略。
