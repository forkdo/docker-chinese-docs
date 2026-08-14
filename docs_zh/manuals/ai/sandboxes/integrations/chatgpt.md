---
title: 将 ChatGPT 连接到沙箱
linkTitle: ChatGPT
weight: 40
description: 通过 SSH 在 ChatGPT 桌面应用中针对 Docker Sandbox 运行 Codex。
keywords: docker sandboxes, chatgpt, codex, openai, remote ssh, sbx
---

{{< summary-bar feature_name="Docker Sandboxes SSH" >}}

通过 SSH 将 ChatGPT 桌面应用连接到沙箱，让 Codex 在隔离的环境中工作，而不是在你的主机上。

> [!NOTE]
> 本页介绍在 ChatGPT 桌面应用中通过 SSH 连接到沙箱运行 Codex。要直接在沙箱内运行 Codex CLI，参见 [Codex](../agents/codex.md)。

## Prerequisites（前提条件）

- 已设置好 SSH 访问。参见 [编辑器与应用集成](_index.md#enable-ssh-access)。
- 已安装 ChatGPT 桌面应用。

ChatGPT 的远程服务器需要沙箱中有 `codex` 命令。下一节使用的 Codex 沙箱模板包含此命令。

## Connect（连接）

如果你还没有，为当前目录创建一个具名 Codex 沙箱：

```console
$ sbx create --name demo codex .
```

确认你可以从终端连接到该沙箱：

```console
$ ssh demo.sbx
```

在 ChatGPT 桌面应用中，打开 **Settings > Connections** 并手动添加一个 SSH 连接。输入沙箱主机名（如 `demo.sbx`）作为主机，然后使用远程文件夹选择器 [选择已挂载的工作区](_index.md#select-the-workspace-folder) 作为远程项目。

有关更多连接选项，参见 OpenAI 的 [连接到 SSH 主机](https://learn.chatgpt.com/docs/remote-connections#connect-to-an-ssh-host) 说明。

## Related（相关）

- [编辑器与应用集成](_index.md) — SSH 访问如何工作以及如何设置
- [Codex](../agents/codex.md) — 在沙箱内运行 Codex CLI
