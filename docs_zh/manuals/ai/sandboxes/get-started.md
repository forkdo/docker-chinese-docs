---
title: 开始使用 Docker Sandboxes
linkTitle: 入门指南
description: 在隔离的沙箱中运行 Claude Code。包含先决条件和基本命令的快速设置指南。
weight: 20
---

{{< summary-bar feature_name="Docker Sandboxes" >}}

本指南将帮助您在隔离的沙箱中首次运行 Claude Code。

> [!NOTE]
> 正在从早期版本的 Docker Desktop 升级？请参阅
> [迁移指南](migration.md) 了解新的微虚拟机架构相关信息。

## 先决条件

开始前，请确保您已具备：

- Docker Desktop 4.58 或更高版本
- macOS，或 Windows {{< badge color=violet text=实验性 >}}
- Claude API 密钥

## 运行您的第一个沙箱

按照以下步骤运行 Claude Code：

1. 将 Anthropic API 密钥设置为环境变量。

   将 API 密钥添加到您的 shell 配置文件：

   ```plaintext {title="~/.bashrc 或 ~/.zshrc"}
   export ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
   ```

   Docker Sandboxes 使用独立于当前 shell 会话的守护进程。这意味着内联设置环境变量或在当前会话中设置将不起作用。您必须在 shell 配置文件中全局设置它，以确保守护进程可以访问该变量。

   然后应用更改：
   1. 加载您的 shell 配置文件。
   2. 重启 Docker Desktop，以便守护进程获取新的环境变量。

2. 为您的项目工作区创建并运行一个 Claude Code 沙箱：

   ```console
   $ docker sandbox run claude ~/my-project
   ```

   这将创建一个微虚拟机沙箱。Docker 会自动为其分配名称。

3. Claude Code 启动后，您就可以开始工作了。首次运行需要更长时间，因为 Docker 需要初始化微虚拟机并拉取模板镜像。

## 刚才发生了什么？

当您运行 `docker sandbox run` 时：

- Docker 创建了一个带有私有 Docker 守护进程的轻量级微虚拟机
- 沙箱根据工作区路径被分配了名称
- 您的工作区同步到虚拟机中
- Docker 在沙箱虚拟机内将 Claude Code 代理作为容器启动

沙箱会一直存在，直到您手动删除它。已安装的软件包和配置将保持可用。再次运行 `docker sandbox run <sandbox-name>` 即可重新连接。

> [!NOTE]
> 代理可以修改您工作区中的文件。在执行代码或执行自动运行脚本的操作前，请仔细审查更改。详情请参阅
> [安全注意事项](workflows.md#security-considerations)。

## 基本命令

以下是管理沙箱的基本命令：

### 列出沙箱

```console
$ docker sandbox ls
```

显示所有沙箱及其 ID、名称、状态和创建时间。

> [!NOTE]
> 沙箱不会出现在 `docker ps` 中，因为它们是微虚拟机而非容器。请使用 `docker sandbox ls` 查看它们。

### 访问运行中的沙箱

```console
$ docker sandbox exec -it <sandbox-name> bash
```

在沙箱内的容器中执行命令。使用 `-it` 打开交互式 shell 进行调试或安装额外工具。

### 删除沙箱

```console
$ docker sandbox rm <sandbox-name>
```

删除沙箱虚拟机及其内部所有已安装的软件包。您可以通过指定多个名称来一次删除多个沙箱：

```console
$ docker sandbox rm <sandbox-1> <sandbox-2>
```

### 重新创建沙箱

要使用干净的环境重新开始，请删除并重新创建沙箱：

```console
$ docker sandbox rm <sandbox-name>
$ docker sandbox run claude ~/project
```

自定义模板和工作区路径等配置在创建沙箱时设置。要更改这些设置，请删除并重新创建沙箱。

完整的命令和选项列表，请参阅
[CLI 参考文档](/reference/cli/docker/sandbox/)。

## 后续步骤

现在您已经在沙箱中成功运行了 Claude，可以进一步了解：

- [Claude Code 配置](claude-code.md)
- [支持的代理](agents.md)
- [高效使用沙箱](workflows.md)
- [自定义模板](templates.md)
- [网络策略](network-policies.md)
- [故障排除](troubleshooting.md)