# 将 Claude Desktop 连接到沙箱




Claude Desktop 可以通过 SSH 在远程机器上运行 Claude Code。将它指向一个沙箱，让代理在隔离的环境中工作，而不是在你的主机上。

> [!NOTE]
> 本页介绍 Claude Desktop 通过 SSH 连接到沙箱。要直接在沙箱内运行 Claude Code CLI，参见 [Claude Code](../agents/claude-code.md)。

## Prerequisites（前提条件）

- 已设置好 SSH 访问。参见 [编辑器与应用集成](_index.md#enable-ssh-access)。
- 已安装 Claude Desktop。

请使用以 Claude 代理类型创建的沙箱。Claude 沙箱模板会为远程 Claude Code 会话配置 Anthropic 凭据和网络访问。

## Connect（连接）

> [!WARNING]
> 通过 SSH 将 Claude Desktop 连接到沙箱，会将 Anthropic 凭据传输到沙箱内的 Claude Code 进程中，从而降低隔离保障。

如果你还没有，为当前目录创建一个具名 Claude 沙箱：

```console
$ sbx create --name demo claude .
```

确认你可以从终端连接到该沙箱：

```console
$ ssh demo.sbx
```

在 Claude Desktop 中，启动会话前打开环境下拉菜单并选择 **+ Add SSH connection**。为连接输入一个名称，并在 **SSH Host** 中输入沙箱主机名（如 `demo.sbx`）。将 **SSH Port** 和 **Identity File** 留空，因为受管 SSH 配置已提供它们。

从环境下拉菜单中选择该连接，然后使用远程文件夹选择器 [选择已挂载的工作区](_index.md#select-the-workspace-folder)。选择器最初可能在 `/home/agent` 处打开。

有关更多连接选项，参见 Claude Desktop 关于 [SSH 会话](https://code.claude.com/docs/en/desktop#ssh-sessions) 的说明。

## Troubleshoot a broken SSH connection after token refresh（排查令牌刷新后 SSH 连接中断的问题）

当 Anthropic 令牌过期并需要刷新时，SSH 连接会断开。要规避此问题，请从你的主机手动运行沙箱：

```console
$ sbx run --name <sandbox-name>
```

## Troubleshoot SSH connection timeouts on Windows（排查 Windows 上的 SSH 连接超时问题）

Claude Desktop 在 Windows 上需要 Git。如果 SSH 连接超时且 Claude Desktop 日志中包含 `ProxyCommand error: spawn sh ENOENT`，请安装 [Git for Windows](https://git-scm.com/download/win)。

如果已经安装了 Git，请确认 `sh.exe` 在你的 `PATH` 上可用：

```powershell
PS> where.exe sh
```

如果该命令找不到 `sh.exe`，请将 Git 的 `bin` 目录添加到你的用户 `Path` 中。默认目录为 `C:\Program Files\Git\bin`。更新 `Path` 后请退出并重启 Claude Desktop。

## Related（相关）

- [编辑器与应用集成](_index.md) — SSH 访问如何工作以及如何设置
- [Claude Code](../agents/claude-code.md) — 在沙箱内运行 Claude Code CLI

