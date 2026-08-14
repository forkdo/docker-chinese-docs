# 将 Cursor 连接到沙箱




Cursor 构建于 VS Code 之上，因此它以相同的方式连接到沙箱，使用 Remote - SSH。你的编辑器留在主机上，而文件、终端和扩展在隔离的沙箱中运行。

> [!NOTE]
> 本页介绍 Cursor 编辑器通过 SSH 连接到沙箱。要改为在沙箱内运行 Cursor agent CLI，参见 [Cursor agent](../agents/cursor.md)。

## Prerequisites（前提条件）

- 已设置好 SSH 访问。参见 [编辑器与应用集成](_index.md#enable-ssh-access)。
- 已安装 Cursor 的 Remote - SSH 支持。

## Connect（连接）

确认你可以从终端连接到该沙箱：

```console
$ ssh demo.sbx
```

1. 打开命令面板并运行 **Remote-SSH: Connect to Host**。
2. 手动将沙箱主机输入为 `<name>.sbx`。
3. Cursor 会打开一个已连接到沙箱的新窗口。使用远程文件夹选择器 [选择已挂载的工作区](_index.md#select-the-workspace-folder)。

## Notes（注意事项）

- 首次连接会在沙箱内安装编辑器服务器，因此可能需要片刻。后续连接会更快。

## Related（相关）

- [编辑器与应用集成](_index.md) — SSH 访问如何工作以及如何设置
- [Cursor agent](../agents/cursor.md) — 在沙箱内运行 Cursor CLI

