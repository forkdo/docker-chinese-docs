---
description: 使用我们分步安装指南轻松在 Linux 上安装 Docker，涵盖系统要求、支持的平台以及后续步骤。
keywords: linux, docker linux install, docker linux, linux docker installation, docker for linux, docker desktop for linux, installing docker on linux, docker download linux, how to install docker on linux, linux vs docker engine, switch docker contexts
title: 在 Linux 上安装 Docker Desktop
linkTitle: Linux
weight: 60
aliases:
- /desktop/linux/install/
- /desktop/install/linux-install/
- /desktop/install/linux/
---

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关一般系统要求、支持的平台以及如何安装 Docker Desktop for Linux 的说明。

> [!IMPORTANT]
>
> Linux 上的 Docker Desktop 运行一个虚拟机 (VM)，该虚拟机在启动时创建并使用自定义的 Docker 上下文 `desktop-linux`。
>
> 这意味着在安装之前部署在 Linux Docker Engine 上的镜像和容器在 Docker Desktop for Linux 中不可用。
>
> {{< accordion title=" Docker Desktop 与 Docker Engine：有什么区别？" >}}

> [!IMPORTANT]
>
> 对于在大型企业（超过 250 名员工或年收入超过 1000 万美元）中通过 Docker Desktop 获取的 Docker Engine 进行商业使用，需要[付费订阅](https://www.docker.com/pricing/)。

Docker Desktop for Linux 提供了一个用户友好的图形界面，简化了容器和服务的管理。它包含 Docker Engine，因为这是驱动 Docker 容器的核心技术。Docker Desktop for Linux 还附带额外的功能，如 Docker Scout 和 Docker Extensions。

#### 安装 Docker Desktop 和 Docker Engine

Docker Desktop for Linux 和 Docker Engine 可以在同一台机器上并行安装。Docker Desktop for Linux 将容器和镜像存储在虚拟机内的隔离存储位置，并提供控制以限制[其资源](/manuals/desktop/settings-and-maintenance/settings.md#resources)。为 Docker Desktop 使用专用的存储位置可以防止它干扰同一台机器上的 Docker Engine 安装。

虽然可以同时运行 Docker Desktop 和 Docker Engine，但在某些情况下同时运行两者可能会导致问题。例如，在为容器映射网络端口（`-p` / `--publish`）时，Docker Desktop 和 Docker Engine 都可能尝试保留机器上的相同端口，从而导致冲突（“端口已被占用”）。

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

Docker CLI 可用于与多个 Docker Engine 交互。例如，您可以使用相同的 Docker CLI 来控制本地 Docker Engine 和控制在云中运行的远程 Docker Engine 实例。[Docker Contexts](/manuals/engine/manage-resources/contexts.md) 允许您在 Docker Engine 实例之间切换。

安装 Docker Desktop 时，会创建一个专用的 "desktop-linux" 上下文以与 Docker Desktop 交互。启动时，Docker Desktop 会自动将其自身的上下文 (`desktop-linux`) 设置为当前上下文。这意味着后续的 Docker CLI 命令都针对 Docker Desktop。关闭时，Docker Desktop 会将当前上下文重置为 `default` 上下文。

使用 `docker context ls` 命令查看机器上可用的上下文。当前上下文用星号 (`*`) 表示。

```console
$ docker context ls
NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
desktop-linux                                             unix:///home/<user>/.docker/desktop/docker.sock  ...        
```

如果您在同一台机器上同时安装了 Docker Desktop 和 Docker Engine，可以运行 `docker context use` 命令在 Docker Desktop 和 Docker Engine 上下文之间切换。例如，使用 "default" 上下文与 Docker Engine 交互：

```console
$ docker context use default
default
Current context is now "default"
```
  
并使用 `desktop-linux` 上下文与 Docker Desktop 交互：
 
```console
$ docker context use desktop-linux
desktop-linux
Current context is now "desktop-linux"
``` 
有关更多详细信息，请参阅 [Docker Context 文档](/manuals/engine/manage-resources/contexts.md)。
{{< /accordion >}}

## 支持的平台

Docker 为以下 Linux 发行版和架构提供 `.deb` 和 `.rpm` 软件包：

| 平台                | x86_64 / amd64          |
|:------------------------|:-----------------------:|
| [Ubuntu](ubuntu.md)                         | ✅  |
| [Debian](debian.md)                         | ✅  |
| [Red Hat Enterprise Linux (RHEL)](rhel.md)  | ✅  |
| [Fedora](fedora.md)                         | ✅  |


适用于基于 [Arch](archlinux.md) 的发行版的实验性软件包可用。Docker 尚未测试或验证该安装。

Docker 支持上述发行版的当前 LTS 版本和最新版本上的 Docker Desktop。随着新版本的发布，Docker 会停止支持最旧的版本并支持最新的版本。

## 一般系统要求

要成功安装 Docker Desktop，您的 Linux 主机必须满足以下一般要求：

- 64 位内核和 CPU 对虚拟化的支持。
- KVM 虚拟化支持。请遵循 [KVM 虚拟化支持说明](#kvm-virtualization-support) 以检查 KVM 内核模块是否已启用以及如何提供对 KVM 设备的访问。
- QEMU 版本必须为 5.2 或更高。我们建议升级到最新版本。
- systemd init 系统。
- 支持 GNOME、KDE 或 MATE 桌面环境，但其他环境也可能可用。
  - 对于许多 Linux 发行版，GNOME 环境不支持托盘图标。要添加对托盘图标的支持，您需要安装 GNOME 扩展。例如，[AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/)。
- 至少 4 GB RAM。
- 启用在用户命名空间中配置 ID 映射，请参阅[文件共享](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#how-do-i-enable-file-sharing)。请注意，对于 Docker Desktop 4.35 及更高版本，不再需要此操作。
- 推荐：[初始化 `pass`](/manuals/desktop/setup/sign-in.md#credentials-management-for-linux-users) 用于凭据管理。

Docker Desktop for Linux 运行一个虚拟机 (VM)。有关原因的更多信息，请参阅 [为什么 Docker Desktop for Linux 运行虚拟机](/manuals/desktop/troubleshoot-and-support/faqs/linuxfaqs.md#why-does-docker-desktop-for-linux-run-a-vm)。

> [!NOTE]
>
> Docker 不支持在嵌套虚拟化场景中运行 Docker Desktop for Linux。我们建议您在支持的发行版上原生运行 Docker Desktop for Linux。

### KVM 虚拟化支持

Docker Desktop 运行一个需要 [KVM 支持](https://www.linux-kvm.org) 的虚拟机。

如果主机支持虚拟化，`kvm` 模块应该会自动加载。要手动加载模块，请运行：

```console
$ modprobe kvm
```

根据主机的处理器，必须加载相应的模块：

```console
$ modprobe kvm_intel  # Intel 处理器

$ modprobe kvm_amd    # AMD 处理器
```

如果上述命令失败，可以通过运行以下命令查看诊断信息：

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

要检查 `/dev/kvm` 的所有权，请运行：

```console
$ ls -al /dev/kvm
```

将您的用户添加到 kvm 组以访问 kvm 设备：

```console
$ sudo usermod -aG kvm $USER
```

注销并重新登录，以便重新评估您的组成员身份。

## 下一步

- 为您的特定 Linux 发行版安装 Docker Desktop for Linux：
   - [在 Ubuntu 上安装](ubuntu.md)
   - [在 Debian 上安装](debian.md)
   - [在 Red Hat Enterprise Linux (RHEL) 上安装](rhel.md)
   - [在 Fedora 上安装](fedora.md)
   - [在 Arch 上安装](archlinux.md)