---
title: 编辑器与应用集成
linkTitle: 集成
weight: 37
description: 通过 SSH 将编辑器和桌面应用连接到 Docker Sandbox。
keywords: docker sandboxes, ssh, integrations, vs code, cursor, remote development, sbx
---

{{< summary-bar feature_name="Docker Sandboxes SSH" >}}

你可以通过 SSH 将外部编辑器或桌面应用连接到正在运行的沙箱。这让你能够使用已经熟悉的工具——VS Code、Cursor、Claude Desktop 等——同时你的代码在隔离的沙箱内运行、构建和执行，而不是在你的主机上。

每个沙箱都可通过 `<name>.sbx` 访问，其中 `<name>` 是沙箱名称。设置好 SSH 后，`<name>.sbx` 就像任何其他 SSH 主机一样工作，因此任何支持通过 SSH 进行远程开发的工具都可以连接到它。

## Prerequisites（前提条件）

- 已安装并登录 `sbx` CLI。参见 [Get started](../get-started.md)。
- 一个 SSH 客户端。macOS 和大多数 Linux 发行版都自带 OpenSSH。在 Windows 上，请安装 OpenSSH 客户端。
- 你想连接的编辑器或应用，并已安装其通过 SSH 的远程开发支持。

## Enable SSH access（启用 SSH 访问）

运行一次 SSH 设置命令：

```console
$ sbx setup ssh
```

该命令会在需要时启动 Docker Sandboxes 守护进程并配置你的 SSH 客户端。你可以随时重新运行它。

## Create or identify a sandbox（创建或识别沙箱）

SSH 连接需要一个已存在的沙箱。为当前目录创建一个具名 shell 沙箱：

```console
$ sbx create --name demo shell .
```

要识别现有沙箱，列出你的沙箱：

```console
$ sbx ls
```

## Connect to a sandbox over SSH（通过 SSH 连接到沙箱）

使用带 `.sbx` 后缀的沙箱名称。例如，连接到名为 `demo` 的沙箱：

```console
$ ssh demo.sbx
```

## Select the workspace folder（选择工作区文件夹）

将应用连接到沙箱会选中远程环境，但它可能不会自动打开已挂载的工作区。在配置连接或启动会话时，使用应用的远程文件夹选择器来选择工作区。

文件夹选择器可能会在沙箱用户的主目录处打开，通常是 `/home/agent`。工作区在沙箱内保留其绝对主机路径。例如，如果你挂载了 `/Users/bob/src/my-project`，请在远程文件夹选择器中选择 `/Users/bob/src/my-project`。

## Connect a specific tool（连接特定工具）

- [VS Code](vscode.md)
- [Cursor](cursor.md)
- [Claude Desktop](claude-desktop.md)
- [ChatGPT](chatgpt.md)

## How SSH connections work（SSH 连接的工作原理）

### Managed SSH configuration（受管 SSH 配置）

`sbx setup ssh` 会向你的 SSH 配置写入一个受管块：在 macOS 和 Linux 上是 `~/.ssh/config`，在 Windows 上是 `%USERPROFILE%\.ssh\config`。该块类似如下：

```text
# >>> docker sandboxes (managed) >>>
Host *.sbx
    User _default_user_
    ProxyCommand "sbx" ssh proxy %n
    IdentityAgent none
    IdentityFile /dev/null
    IdentitiesOnly yes
    ControlMaster no
    ControlPath none
    UserKnownHostsFile "~/.ssh/sbx_known_hosts"
    KnownHostsCommand "sbx" ssh known-hosts %H
    StrictHostKeyChecking yes
# <<< docker sandboxes (managed) <<<
```

你无需手动编辑此块。其关键条目的作用如下：

- `Host *.sbx` 将沙箱主机名映射到沙箱守护进程。应用的主机选择器无法从此通配符中发现具体的沙箱名称，因此在配置集成时请手动输入主机名，例如 `demo.sbx`。
- `User _default_user_` 告诉守护进程使用沙箱镜像的默认用户，因此你的主机用户名绝不会被发送。

### Connection and authentication（连接与认证）

连接不使用网络端口或 SSH 密钥：

- `ProxyCommand` 通过守护进程的本地套接字（在 macOS 和 Linux 上是 Unix 域套接字，在 Windows 上是命名管道）转达 SSH 流。
- 守护进程仅在你拥有活跃的 Docker 登录时才接受连接。认证与你的登录绑定，而非与存储的密钥绑定。
- 每次连接都会验证主机密钥，因此轮换的守护进程密钥绝不会触发主机密钥不匹配。

由于 SSH 终止于守护进程，沙箱内部不运行 SSH 服务器。沙箱必须已经创建。如果它已停止，连接到 `<name>.sbx` 会自动启动它。

### Environment variables（环境变量）

SSH 连接不会将客户端环境变量转发到沙箱中。守护进程会为兼容性而确认 SSH 环境请求，但忽略其名称和取值。

### Port forwarding（端口转发）

SSH 客户端可以使用本地端口转发，将监听沙箱回环接口的服务在主机上提供访问。例如，远程开发客户端可以将沙箱中的 `127.0.0.1:4321` 映射到主机上的 `127.0.0.1:55565`，并自动选择一个可用的主机端口。流量通过 SSH 连接传递，而非通过发布的 Docker 端口。

沙箱守护进程仅接受转发到沙箱内回环地址的连接，包括 `localhost`、`127.0.0.0/8` 和 `::1`。SSH 客户端为主机上的监听器选择绑定地址。绑定到 `127.0.0.1` 或 `::1` 的监听器仅可从主机访问。配置为绑定到非回环地址的客户端可以使转发的服务从其他机器访问，具体取决于主机的网络和防火墙配置。
