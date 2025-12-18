---
description: 使用我们的分步安装指南轻松在 Linux 上安装 Docker，涵盖系统要求、支持的平台以及后续操作指引。
keywords: linux, docker linux install, docker linux, linux docker installation, docker
  for linux, docker desktop for linux, installing docker on linux, docker download
  linux, how to install docker on linux, linux vs docker engine, switch docker contexts
title: 在 Linux 上安装 Docker Desktop
linkTitle: Linux
weight: 60
aliases:
- /desktop/linux/install/
- /desktop/install/linux-install/
- /desktop/install/linux/
---

> **Docker Desktop 使用条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要 [付费订阅](https://www.docker.com/pricing/)。

本页面包含有关一般系统要求、支持的平台，以及如何在 Linux 上安装 Docker Desktop 的信息。

> [!IMPORTANT]
>
> Linux 上的 Docker Desktop 运行一个虚拟机（VM），在启动时会创建并使用一个自定义的 docker 上下文 `desktop-linux`。
>
> 这意味着在安装 Docker Desktop 之前部署在 Linux Docker Engine 上的镜像和容器在 Docker Desktop for Linux 中不可用。
>
> {{< accordion title=" Docker Desktop 与 Docker Engine：有什么区别？" >}}

> [!IMPORTANT]
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用通过 Docker Desktop 获得的 Docker Engine 需要 [付费订阅](https://www.docker.com/pricing/)。

Linux 上的 Docker Desktop 提供了一个用户友好的图形界面，简化了容器和服务的管理。它包含 Docker Engine，因为这是支持 Docker 容器的核心技术。Linux 上的 Docker Desktop 还附带了其他功能，如 Docker Scout 和 Docker 扩展。

#### 安装 Docker Desktop 和 Docker Engine

Docker Desktop for Linux 和 Docker Engine 可以在同一台机器上并行安装。Linux 上的 Docker Desktop 将容器和镜像存储在 VM 内的隔离存储位置中，并提供控件来限制 [其资源](/manuals/desktop/settings-and-maintenance/settings.md#resources)。为 Docker Desktop 使用专用存储位置可以防止它与同一台机器上的 Docker Engine 安装相互干扰。

虽然可以同时运行 Docker Desktop 和 Docker Engine，但在某些情况下同时运行两者可能会导致问题。例如，当为容器映射网络端口（`-p` / `--publish`）时，Docker Desktop 和 Docker Engine 可能都会尝试保留机器上的同一个端口，从而导致冲突（“端口已在使用中”）。

我们通常建议在使用 Docker Desktop 时停止 Docker Engine，以防止 Docker Engine 消耗资源并避免上述冲突。

使用以下命令停止 Docker Engine 服务：

```console
$ sudo systemctl stop docker docker.socket containerd
```

根据您的安装情况，Docker Engine 可能被配置为在机器启动时自动作为系统服务启动。使用以下命令禁用 Docker Engine 服务，并防止其自动启动：

```console
$ sudo systemctl disable docker docker.socket containerd
```

### 在 Docker Desktop 和 Docker Engine 之间切换

Docker CLI 可用于与多个 Docker Engine 实例交互。例如，您可以使用相同的 Docker CLI 来控制本地 Docker Engine 和控制云中运行的远程 Docker Engine 实例。[Docker 上下文](/manuals/engine/manage-resources/contexts.md) 允许您在 Docker Engine 实例之间切换。

安装 Docker Desktop 时，会创建一个专用的 "desktop-linux" 上下文来与 Docker Desktop 交互。启动时，Docker Desktop 自动将其自身的上下文（`desktop-linux`）设置为当前上下文。这意味着后续的 Docker CLI 命令将针对 Docker Desktop。关闭时，Docker Desktop 会将当前上下文重置为 `default` 上下文。

使用 `docker context ls` 命令查看机器上可用的上下文。当前上下文用星号（`*`）标示。

```console
$ docker context ls
NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
desktop-linux                                             unix:///home/<user>/.docker/desktop/docker.sock  ...        
```

如果您的机器上同时安装了 Docker Desktop 和 Docker Engine，您可以运行 `docker context use` 命令在 Docker Desktop 和 Docker Engine 上下文之间切换。例如，使用 "default" 上下文与 Docker Engine 交互：

```console
$ docker context use default
default
Current context is now "default"
```
  
使用 `desktop-linux` 上下文与 Docker Desktop 交互：
 
```console
$ docker context use desktop-linux
desktop-linux
Current context is now "desktop-linux"
``` 
更多详细信息，请参考 [Docker 上下文文档](/manuals/engine/manage-resources/contexts.md)。
{{< /accordion >}}

## 支持的平台

Docker 为以下 Linux 发行版和架构提供 `.deb` 和 `.rpm` 软件包：

| 平台                | x86_64 / amd64          | 
|:------------------------|:-----------------------:|
| [Ubuntu](ubuntu.md)                         | ✅  |
| [Debian](debian.md)                         | ✅  |
| [Red Hat Enterprise Linux (RHEL)](rhel.md)  | ✅  |
| [Fedora](fedora.md)                         | ✅  |


为 [Arch](archlinux.md) 系发行版提供了一个实验性软件包。Docker 未测试或验证此安装。

Docker 在上述发行版的当前 LTS 版本和最新版本上支持 Docker Desktop。随着新版本的发布，Docker 会停止对最旧版本的支持，并支持最新版本。

## 一般系统要求

要成功安装 Docker Desktop，您的 Linux 主机必须满足以下一般要求：

- 64 位内核和 CPU 虚拟化支持。
- KVM 虚拟化支持。请按照 [KVM 虚拟化支持说明](#kvm-virtualization-support) 检查 KVM 内核模块是否已启用，以及如何访问 KVM 设备。
- QEMU 必须是 5.2 或更高版本。建议升级到最新版本。
- systemd 初始化系统。
- 支持 GNOME、KDE 或 MATE 桌面环境，但其他环境可能也可以工作。
  - 对于许多 Linux 发行版，GNOME 环境不支持系统托盘图标。要添加对托盘图标的支持，您需要安装 GNOME 扩展。例如，[AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 至少 4 GB RAM。
- 启用用户命名空间中的 ID 映射配置，参见 [文件共享](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#how-do-i-enable-file-sharing)。注意：对于 Docker Desktop 4.35 及更高版本，不再需要此步骤。
- 推荐：[初始化 `pass`](/manuals/desktop/setup/sign-in.md#credentials-management-for-linux-users) 用于凭据管理。

Linux 上的 Docker Desktop 运行一个虚拟机（VM）。更多原因，请参见 [为什么 Linux 上的 Docker Desktop 运行 VM](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#why-does-docker-desktop-for-linux-run-a-vm)。

> [!NOTE]
>
> Docker 不提供在嵌套虚拟化场景中运行 Linux 上的 Docker Desktop 的支持。我们建议您在支持的发行版上原生运行 Linux 上的 Docker Desktop。

### KVM 虚拟化支持


Docker Desktop 运行需要 [KVM 支持](https://www.linux-kvm.org) 的 VM。
如果主机具有虚拟化支持，`kvm` 模块应该自动加载。要手动加载模块，请运行：

```console
$ modprobe kvm
```

根据主机 CPU 的类型，必须加载相应的模块：

```console
$ modprobe kvm_intel  # Intel 处理器

$ modprobe kvm_amd    # AMD 处理器
```

如果上述命令失败，您可以通过运行以下命令查看诊断信息：

```console
$ kvm-ok
```

要检查 KVM 模块是否已启用，请运行：

```console
$ lsmod | grep kvm
kvm_amd               167936  0
ccp                   126976  1 kvm_amd
kvm                  1089536  1 kvm_amd
irqbypass              16384  1 kvm
```

#### 设置 KVM 设备用户权限


要检查 `/dev/kvm` 的所有者，请运行：

```console
$ ls -al /dev/kvm
```

将您的用户添加到 kvm 组以访问 kvm 设备：

```console
$ sudo usermod -aG kvm $USER
```

注销并重新登录，以便重新评估您的组成员身份。

## 后续操作

- 为您的特定 Linux 发行版安装 Linux 上的 Docker Desktop：
   - [在 Ubuntu 上安装](ubuntu.md)
   - [在 Debian 上安装](debian.md)
   - [在 Red Hat Enterprise Linux (RHEL) 上安装](rhel.md)
   - [在 Fedora 上安装](fedora.md)
   - [在 Arch 上安装](archlinux.md)


