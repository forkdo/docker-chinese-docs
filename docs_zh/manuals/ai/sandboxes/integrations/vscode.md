---
title: 将 VS Code 连接到沙箱
linkTitle: VS Code
weight: 10
description: 使用 VS Code Remote - SSH 在 Docker Sandbox 内进行开发。
keywords: docker sandboxes, vs code, remote ssh, remote development, sbx
---

{{< summary-bar feature_name="Docker Sandboxes SSH" >}}

使用 Remote - SSH 扩展打开一个在沙箱内运行的 VS Code 窗口。你的编辑器留在主机上，而文件、终端和扩展在隔离的沙箱中运行。

## Prerequisites（前提条件）

- 已设置好 SSH 访问。参见 [编辑器与应用集成](_index.md#enable-ssh-access)。
- 已在 VS Code 中安装 [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) 扩展（`ms-vscode-remote.remote-ssh`）。

## Connect（连接）

确认你可以从终端连接到该沙箱：

```console
$ ssh demo.sbx
```

在 VS Code 中，打开命令面板并运行 **Remote-SSH: Connect to Host...**。手动输入沙箱主机名，例如 `demo.sbx`。VS Code 连接成功后，使用远程文件夹选择器 [选择已挂载的工作区](_index.md#select-the-workspace-folder)。

有关更多连接选项，参见 VS Code 的 [连接到远程主机](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) 说明。

## Notes（注意事项）

- 首次连接会在沙箱内安装 VS Code 服务器，因此可能需要片刻。后续连接会更快。

### Reconnect loop on macOS（macOS 上的重连循环）

受影响版本的 VS Code 在 macOS 上可能进入无限重连循环。如果发生这种情况，请在你的 VS Code 用户设置中将 `remote.SSH.useLocalServer` 设为 `false`：

```json
{
  "remote.SSH.useLocalServer": false
}
```

详情参见 [microsoft/vscode-remote-release#11672](https://github.com/microsoft/vscode-remote-release/issues/11672)。

### SSH host key verification fails（SSH 主机密钥验证失败）

在你添加 SSH 主机后，VS Code 可能在你的 SSH 配置中留下重复或格式错误的 `Host *.sbx` 块。如果 VS Code 连接报告 `KnownHostsCommand` 错误或 `Host key verification failed`，请删除每一个标记为 `docker sandboxes (managed)` 的 SSH 配置块，包括标记注释：

```diff
-# >>> docker sandboxes (managed) >>>
-Host *.sbx
-    User _default_user_
-    ProxyCommand "sbx" ssh proxy %n
-    ...
-    UserKnownHostsFile "~/.ssh/sbx_known_hosts"
-    KnownHostsCommand "sbx" ssh known-hosts %H
-    StrictHostKeyChecking yes
-# <<< docker sandboxes (managed) <<<
```

然后重新生成受管块：

```console
$ sbx setup ssh
```

从 VS Code 重新连接到沙箱。

## Related（相关）

- [编辑器与应用集成](_index.md) — SSH 访问如何工作以及如何设置
