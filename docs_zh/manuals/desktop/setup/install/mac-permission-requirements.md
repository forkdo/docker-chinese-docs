---
description: 了解 Docker Desktop for Mac 的权限要求以及不同版本之间的差异
keywords: Docker Desktop, mac, 安全, 安装, 权限
title: 了解 Mac 上 Docker Desktop 的权限要求
linkTitle: Mac 权限要求
aliases:
- /docker-for-mac/privileged-helper/
- /desktop/mac/privileged-helper/
- /desktop/mac/permission-requirements/
- /desktop/install/mac-permission-requirements/
weight: 20
---

本文档包含在 Mac 上运行和安装 Docker Desktop 的权限要求信息。

同时，也澄清了以 `root` 身份运行容器与在主机上拥有 `root` 访问权限的区别。

Mac 上的 Docker Desktop 以安全为设计核心。仅在绝对必要时才需要管理员权限。

## 权限要求

Mac 上的 Docker Desktop 以非特权用户身份运行。但是，Docker Desktop 需要某些功能来执行有限的特权配置，例如：
 - [安装符号链接](#installing-symlinks) 到 `/usr/local/bin`。
 - [绑定特权端口](#binding-privileged-ports)，即小于 1024 的端口。尽管特权端口（1024 以下的端口）通常不作为安全边界使用，但操作系统仍然阻止非特权进程绑定到这些端口，这会导致诸如 `docker run -p 127.0.0.1:80:80 docker/getting-started` 等命令失败。
 - [确保 `localhost` 和 `kubernetes.docker.internal` 在 `/etc/hosts` 中定义](#ensuring-localhost-and-kubernetesdockerinternal-are-defined)。某些旧的 macOS 安装在 `/etc/hosts` 中没有 `localhost`，这会导致 Docker 失败。定义 DNS 名称 `kubernetes.docker.internal` 可以让 Docker 与容器共享 Kubernetes 上下文。
 - 安全地缓存注册表访问管理策略，该策略对开发者是只读的。

特权访问在安装期间授予。

Mac 上的 Docker Desktop 首次启动时，会显示一个安装窗口，您可以选择使用默认设置（适用于大多数开发者，需要授予特权访问权限），或使用高级设置。

如果您在安全要求更高的环境中工作，例如禁止本地管理员访问的环境，那么您可以使用高级设置来移除对特权访问的需求。您可以配置：
- Docker CLI 工具的位置（系统目录或用户目录）
- 默认 Docker 套接字
- 特权端口映射

根据您配置的高级设置，您可能需要输入密码以确认。

您可以在安装后从 **设置** 中的 **高级** 页面更改这些配置。

### 安装符号链接

Docker 二进制文件默认安装在 `/Applications/Docker.app/Contents/Resources/bin` 中。Docker Desktop 在 `/usr/local/bin` 中创建这些二进制文件的符号链接，这意味着它们会自动包含在大多数系统的 `PATH` 中。

您可以在安装 Docker Desktop 期间选择将符号链接安装在 `/usr/local/bin` 或 `$HOME/.docker/bin` 中。

如果选择 `/usr/local/bin`，且此位置无法由非特权用户写入，Docker Desktop 需要授权以确认此选择，然后才会在 `/usr/local/bin` 中创建 Docker 二进制文件的符号链接。如果选择 `$HOME/.docker/bin`，则不需要授权，但您必须[手动将 `$HOME/.docker/bin` 添加到 PATH](/manuals/desktop/settings-and-maintenance/settings.md#advanced)。

您还可以选择是否启用安装 `/var/run/docker.sock` 符号链接的选项。创建此符号链接可确保依赖默认 Docker 套接字路径的各种 Docker 客户端无需额外更改即可工作。

由于 `/var/run` 被挂载为 tmpfs，其内容在重启时会被删除，包括 Docker 套接字的符号链接。为了确保重启后 Docker 套接字仍然存在，Docker Desktop 设置了一个 `launchd` 启动任务，通过运行 `ln -s -f /Users/<user>/.docker/run/docker.sock /var/run/docker.sock` 来创建符号链接。这确保您不会在每次启动时被提示创建符号链接。如果您在安装时未启用此选项，则不会创建符号链接和启动任务，您可能需要在使用的客户端中显式设置 `DOCKER_HOST` 环境变量为 `/Users/<user>/.docker/run/docker.sock`。Docker CLI 依赖于当前上下文来检索套接字路径，当前上下文在 Docker Desktop 启动时被设置为 `desktop-linux`。

### 绑定特权端口

您可以在安装期间或安装后从 **设置** 中的 **高级** 页面选择启用特权端口映射。Docker Desktop 需要授权以确认此选择。

### 确保 `localhost` 和 `kubernetes.docker.internal` 已定义

您有责任确保 `localhost` 解析为 `127.0.0.1`，如果使用 Kubernetes，则确保 `kubernetes.docker.internal` 解析为 `127.0.0.1`。

## 从命令行安装

特权配置通过在 [安装命令](/manuals/desktop/setup/install/mac-install.md#install-from-the-command-line) 上使用 `--user` 标志在安装期间应用。在这种情况下，Docker Desktop 首次运行时不会提示授予 root 权限。具体来说，`--user` 标志会：
- 卸载之前的 `com.docker.vmnetd`（如果存在）
- 设置符号链接
- 确保 `localhost` 解析为 `127.0.0.1`

此方法的限制是 Docker Desktop 只能由每台机器上的一个用户账户运行，即在 `-–user` 标志中指定的那个。

## 特权辅助进程

在有限的情况下，当需要特权辅助进程时，例如绑定特权端口或缓存注册表访问管理策略，特权辅助进程由 `launchd` 启动并在后台运行，除非如前所述在运行时被禁用。Docker Desktop 后端通过 UNIX 域套接字 `/var/run/com.docker.vmnetd.sock` 与特权辅助进程通信。它执行的功能包括：
- 绑定特权端口（小于 1024）
- 安全地缓存注册表访问管理策略（对开发者只读）
- 卸载特权辅助进程

移除特权辅助进程的方式与移除 `launchd` 进程相同。

```console
$ ps aux | grep vmnetd
root             28739   0.0  0.0 34859128    228   ??  Ss    6:03PM   0:00.06 /Library/PrivilegedHelperTools/com.docker.vmnetd
user             32222   0.0  0.0 34122828    808 s000  R+   12:55PM   0:00.00 grep vmnetd

$ sudo launchctl unload -w /Library/LaunchDaemons/com.docker.vmnetd.plist
Password:

$ ps aux | grep vmnetd
user             32242   0.0  0.0 34122828    716 s000  R+   12:55PM   0:00.00 grep vmnetd

$ rm /Library/LaunchDaemons/com.docker.vmnetd.plist

$ rm /Library/PrivilegedHelperTools/com.docker.vmnetd
```

## Linux VM 中以 root 身份运行的容器

使用 Docker Desktop，Docker 守护进程和容器在 Docker 管理的轻量级 Linux 虚拟机中运行。这意味着尽管容器默认以 `root` 身份运行，但这并不会授予对 Mac 主机的 `root` 访问权限。Linux 虚拟机充当安全边界，限制了可从主机访问的资源。从主机绑定挂载到 Docker 容器的任何目录仍然保留其原始权限。

## 增强容器隔离

此外，Docker Desktop 支持 [增强容器隔离模式](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)（ECI），仅限 Business 客户使用，该模式进一步加强了容器安全性，同时不影响开发者工作流。

ECI 自动在 Linux 用户命名空间内运行所有容器，使得容器内的 root 映射到 Docker Desktop VM 内的非特权用户。ECI 使用此技术以及其他高级技术，进一步隔离 Docker Desktop Linux VM 内的容器，使其与 Docker 守护进程和 VM 内运行的其他服务进一步隔离。