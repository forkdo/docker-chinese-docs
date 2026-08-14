---
title: 通过 CLI 使用 Gordon
linkTitle: CLI
description: 通过 docker ai 命令访问和使用 Gordon
weight: 20
---

{{< summary-bar feature_name="Gordon" >}}

`docker ai` 命令为 Gordon 提供了一个终端用户界面（TUI），将 AI 辅助能力直接集成到你的终端中。

## 基本用法

启动交互式 TUI：

```console
$ docker ai
```

这会打开 Gordon 的终端界面，你可以在其中输入提示词、批准操作，并在完整上下文中继续对话。

<script src="https://asciinema.org/a/9kvZFH9LO9ZVDpwS.js" id="asciicast-9kvZFH9LO9ZVDpwS" async="true"></script>

也可以直接将提示词作为参数传入：

```console
$ docker ai "list my running containers"
```

使用 `/exit` 或 <kbd>Ctrl+C</kbd> 退出 TUI。

## Working directory（工作目录）

工作目录为 Gordon 的文件操作设定默认上下文。

Gordon 使用你当前的 shell 目录作为工作目录：

```console
$ cd ~/my-project
$ docker ai
```

使用 `-C` 或 `--working-dir` 覆盖：

```console
$ docker ai -C ~/different-project
```

## 禁用 Gordon

Gordon CLI 是 Docker Desktop 的一部分。要禁用它，请在 Docker Desktop 设置中禁用 Gordon：

1. 打开 Docker Desktop 设置。
2. 导航到 **AI** 部分。
3. 取消勾选 **Enable Gordon** 选项。
4. 选择 **Apply**。

## 命令

`docker ai` 命令包含若干子命令：

交互模式（默认）：

```console
$ docker ai
```

打开 TUI 以进行对话式交互。

版本：

```console
$ docker ai version
```

显示 Gordon 的版本。

反馈：

```console
$ docker ai feedback
```

在浏览器中打开反馈表单。
