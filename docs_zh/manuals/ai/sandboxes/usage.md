<!-- FILE: manuals/ai/sandboxes/usage.md -->

---
title: 用法
weight: 20
description: 用于创建、管理和连接 Docker Sandboxes 的基本 sbx 命令。
keywords: docker sandboxes, sbx, usage, run, create, stop, remove, ports, workspaces
---

将本页作为面向日常 `sbx` 操作的以命令为导向的指南。有关基于场景的建议，请参阅 [工作流模式](workflows.md)。

## 登录

在终端中登录：

```console
$ sbx login
```

对于没有浏览器的脚本或 CI 运行器，请参阅 [CI 与无头使用](workflows.md#ci-and-headless-use)。

## 启动、停止和移除

基本工作流是：[`run`](/reference/cli/sbx/run/) 启动、[`ls`](/reference/cli/sbx/ls/) 查看状态、[`stop`](/reference/cli/sbx/stop/) 暂停、[`rm`](/reference/cli/sbx/rm/) 清理：

```console
$ sbx run claude                    # 启动一个 agent
$ sbx ls                            # 查看正在运行的内容
$ sbx stop my-sandbox               # 暂停它
$ sbx rm my-sandbox                 # 彻底删除它
```

如果沙盒有一个活动会话——一个打开的 attach、SSH 连接或正在进行的 SFTP 传输——`sbx rm` 会拒绝，除非你传递 `--force`：

```console
$ sbx rm --force my-sandbox
```

如果你需要一个干净的状态，移除沙盒并再次运行它：

```console
$ sbx stop my-sandbox
$ sbx rm my-sandbox
$ sbx run claude
```

## 重新连接和为沙盒命名

agent 退出后，沙盒仍然保留。再次运行相同的工作区路径会重新连接到现有沙盒，而不是创建另一个沙盒：

```console
$ sbx run claude ~/my-project  # 创建沙盒
$ sbx run claude ~/my-project  # 重新连接到同一个沙盒
```

使用 `--name` 给沙盒一个显式的标识：

```console
$ sbx run claude --name my-project
```

一旦命名沙盒存在，使用 `--name` 可以从任意工作目录重新附加到它，无论是否带 agent 位置参数：

```console
$ sbx run --name my-project        # 从任何地方重新附加
$ sbx run claude --name my-project # 同上，并确认 agent
```

要对同一工作区运行多个沙盒，给每个一个不同的名称：

```console
$ sbx run claude --name feature ~/my-project
$ sbx run claude --name spike ~/my-project
```

## 创建而不附加

[`sbx run`](/reference/cli/sbx/run/) 会创建沙盒并将你附加到 agent。要在后台创建沙盒而不附加：

```console
$ sbx create --name my-project claude .
```

与 `run` 不同，`create` 需要一个显式的工作区路径。之后用 `sbx run --name` 附加：

```console
$ sbx run --name my-project
```

## 在沙盒内运行命令

要进入运行中的沙盒内部的 shell，使用 [`sbx exec`](/reference/cli/sbx/exec/)：

```console
$ sbx exec -it <sandbox-name> bash
```

## 交互模式

不带任何子命令运行 `sbx` 会打开一个交互式终端仪表板：

```console
$ sbx
```

仪表板将所有沙盒以卡片形式展示，带有实时状态、CPU 和内存使用情况。从这里你可以：

- **创建**一个沙盒（`c`）。
- **启动或停止**一个沙盒（`s`）。
- **附加**到一个 agent 会话（`Enter`），与 `sbx run` 相同。
- **打开**沙盒内部的 shell（`x`），与 `sbx exec` 相同。
- **移除**一个沙盒（`r`）。

仪表板还包含一个网络管控面板，你可以在其中监控沙盒发出的出站连接并管理网络规则。使用 `tab` 在沙盒面板和网络面板之间切换。

从网络面板你可以浏览连接日志、允许或阻止特定主机，以及添加自定义网络规则。按 `?` 查看所有键盘快捷键。

## Git 工作区模式

当你的主工作区是一个 Git 仓库时，选择在创建沙盒时接收它的方式：

- 直接模式是默认模式。agent 对你的工作树拥有读写访问权，更改会立即出现在你的宿主上。
- [克隆模式](#clone-mode) 使用 `--clone`。agent 在沙盒内部编辑一个独立的 Git 克隆。它的更改会留在那里，直到你获取它们或 agent 推送它们。你的宿主仓库在 `/run/sandbox/source` 也可用，但只有读访问。

有关分支策略、从沙盒获取工作以及并行 agent 工作流的指导，请参阅 [Git 工作流](workflows.md#git-workflows)。每种模式背后的安全模型，请参阅 [工作区隔离](security/isolation.md#workspace-isolation)。

### 克隆模式

要创建克隆模式沙盒，在运行或创建时传递 `--clone`：

```console
$ sbx run --clone claude
```

你也可以在后台创建沙盒并稍后附加：

```console
$ sbx create --clone --name my-sandbox claude .
$ sbx run --name my-sandbox
```

克隆模式有一些创建时的约束：

- 克隆模式在创建时即固定。要将现有沙盒切换到克隆模式，请使用 `sbx create --clone` 移除并重建它。
- 克隆跟随你的宿主仓库在创建时检出的任何引用（ref）。不会自动创建分支。
- 主工作区必须是一个 Git 仓库。对于非 Git 工作区省略 `--clone`。
- 克隆模式会在主仓库检出之外的 Git worktree 中被拒绝。只读绑定挂载无法解析 worktree 的 `.git` 指针文件。请从主仓库检出运行 `sbx create --clone`。
- 移除克隆模式沙盒会丢弃沙盒内的克隆。在移除之前，获取或推送你想保留的任何提交。

## 多个工作区

你可以将额外的目录与主工作区一起挂载进沙盒。第一个路径是主工作区——agent 从这里启动，如果你使用 `--clone`，沙盒内的 Git 克隆会从该目录填充。额外的工作区始终直接挂载。

所有工作区出现在沙盒内部时位于它们的绝对宿主路径下。追加 `:ro` 以只读方式挂载一个额外工作区——适用于 agent 不应修改的参考资料或共享库：

```console
$ sbx run claude ~/project-a ~/shared-libs:ro ~/docs:ro
```

你也可以并排运行独立的项目。完成后移除未使用的沙盒以回收磁盘空间：

```console
$ sbx run claude ~/project-a
$ sbx run claude ~/project-b
$ sbx rm <sandbox-name>       # 完成时
```

## 在宿主和沙盒之间复制文件

使用 [`sbx cp`](/reference/cli/sbx/cp/) 在宿主和沙盒之间复制文件或目录。这对于不属于已挂载工作区的一次性文件很有用，例如生成的输出、日志或设置文件。

```console
$ sbx cp ./config.json my-sandbox:/home/user/
$ sbx cp my-sandbox:/home/user/output.log ./
$ sbx cp ./src/ my-sandbox:/home/user/src
```

复制的一侧必须使用 `SANDBOX:PATH`。不支持在两个沙盒之间直接复制。

## 发布端口

沙盒是[网络隔离](security/isolation.md)的——默认情况下，你的浏览器或本地工具无法到达在其中运行的服务器。端口映射 `8080:3000` 将沙盒端口 3000 发布到宿主端口 8080。

如果你知道需要哪些端口，在创建沙盒时发布它们：

```console
$ sbx run --publish 8080:3000 --name my-sandbox claude
```

对于现有沙盒，使用 [`sbx ports`](/reference/cli/sbx/ports/) 从宿主转发流量：

```console
$ sbx ports my-sandbox --publish 8080:3000
$ open http://localhost:8080
```

要让操作系统选择一个空闲的宿主端口，而不是自己指定，只指定沙盒端口。然后使用 `sbx ports` 检查分配了哪个宿主端口：

```console
$ sbx ports my-sandbox --publish 3000
$ sbx ports my-sandbox
```

`sbx ls` 在每个沙盒旁边显示活动的端口映射。`sbx ports` 详细列出它们。

```console
$ sbx ls
SANDBOX         AGENT   STATUS   PORTS                    WORKSPACE
my-sandbox      claude  running  127.0.0.1:8080->3000/tcp /home/user/proj
```

要停止转发一个端口：

```console
$ sbx ports my-sandbox --unpublish 8080:3000
```

当 `sbx run` 重新附加到现有沙盒时，它会忽略 `--publish`。使用 `sbx ports` 在该沙盒上发布端口。有关开发服务器和宿主服务的方法，请参阅 [本地服务](workflows.md#local-services)。

## 持久化的内容

只要沙盒存在，已安装的包、Docker 镜像、配置更改和命令历史都会跨停止和重启持续存在。当你移除沙盒时，内部的一切都会被删除。你的工作区文件和[共享 agent 技能存储](workflows.md#share-agent-skills)保留在你的宿主上。要保留一个配置好的环境，请创建一个 [自定义模板](customize/templates.md) 或使用一个 [kit](customize/kits.md)。
