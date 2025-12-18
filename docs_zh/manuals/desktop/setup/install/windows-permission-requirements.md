---
description: 了解 Windows 上 Docker Desktop 的权限要求
keywords: Docker Desktop, Windows, 安全, 安装
title: 了解 Windows 的权限要求
linkTitle: Windows 权限要求
aliases:
- /desktop/windows/privileged-helper/
- /desktop/windows/permission-requirements/
- /desktop/install/windows-permission-requirements/
weight: 40
---

本文档包含有关在 Windows 上运行和安装 Docker Desktop 的权限要求、特权辅助进程 `com.docker.service` 的功能以及采用此方法的原因等信息。

同时，本文档也阐明了在容器中以 `root` 身份运行与在主机上拥有 `Administrator` 访问权限的区别，以及 Windows Docker 引擎和 Windows 容器的权限。

Windows 上的 Docker Desktop 在设计时就考虑了安全性。仅在绝对必要时才需要管理员权限。

## 权限要求

虽然 Docker Desktop 可以在没有 `Administrator` 权限的情况下运行，但在安装过程中确实需要这些权限。安装时，您会收到 UAC 提示，允许安装特权辅助服务。之后，Docker Desktop 可以在没有管理员权限的情况下运行。

在 Windows 上运行没有特权辅助的 Docker Desktop 不需要用户加入 `docker-users` 组。但是，某些需要特权操作的功能将有此要求。

如果您执行了安装，您会自动被添加到此组，但其他用户必须手动添加。这允许管理员控制谁可以访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机，或使用 Windows 容器。

当 Docker Desktop 启动时，所有非特权命名管道都会被创建，以便只有以下用户可以访问它们：
- 启动 Docker Desktop 的用户。
- 本地 `Administrators` 组的成员。
- `LOCALSYSTEM` 账户。

## 特权辅助

Docker Desktop 需要执行一组有限的特权操作，这些操作由特权辅助进程 `com.docker.service` 执行。这种方法允许遵循最小权限原则，仅在绝对必要时才使用 `Administrator` 访问权限，同时仍然能够以非特权用户身份使用 Docker Desktop。

特权辅助 `com.docker.service` 是一个在后台运行的 Windows 服务，具有 `SYSTEM` 权限。它监听命名管道 `//./pipe/dockerBackendV2`。开发者运行 Docker Desktop 应用程序，该应用程序连接到命名管道并向服务发送命令。此命名管道受到保护，只有 `docker-users` 组的成员才能访问。

该服务执行以下功能：
- 确保在 Win32 hosts 文件中定义了 `kubernetes.docker.internal`。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
- 确保在 Win32 hosts 文件中定义了 `host.docker.internal` 和 `gateway.docker.internal`。它们指向主机的本地 IP 地址，允许应用程序使用相同的名称从主机本身或容器中解析主机 IP。
- 安全地缓存只读的 Registry Access Management 策略。
- 创建 Hyper-V 虚拟机 `"DockerDesktopVM"` 并管理其生命周期 - 启动、停止和销毁。虚拟机名称在服务代码中是硬编码的，因此该服务不能用于创建或操作任何其他虚拟机。
- 移动 VHDX 文件或文件夹。
- 启动和停止 Windows Docker 引擎并查询其是否正在运行。
- 删除所有 Windows 容器数据文件。
- 检查 Hyper-V 是否已启用。
- 检查引导加载程序是否激活了 Hyper-V。
- 检查是否安装并启用了所需的 Windows 功能。
- 执行健康检查并检索服务本身的版本。

服务的启动模式取决于选择的容器引擎，对于 WSL，还取决于是否需要在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal`。这由设置页面中 `Use the WSL 2 based engine` 下的设置控制。当设置此选项时，WSL 引擎的行为与 Hyper-V 相同。因此：
- 使用 Windows 容器或 Hyper-V Linux 容器时，服务在系统启动时启动并持续运行，即使 Docker Desktop 未运行也是如此。这是必需的，以便您可以在没有管理员权限的情况下启动 Docker Desktop。
- 使用 WSL2 Linux 容器时，不需要服务，因此在系统启动时不会自动运行。当您切换到 Windows 容器或 Hyper-V Linux 容器，或选择在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal` 时，会出现 UAC 提示，要求您接受特权操作以启动服务。如果接受，服务将启动并设置为在下次 Windows 启动时自动启动。

## Linux 虚拟机中以 root 身份运行的容器

Linux Docker 守护进程和容器运行在由 Docker 管理的最小、专用的 Linux 虚拟机中。它是不可变的，因此您无法扩展它或更改已安装的软件。这意味着尽管容器默认以 `root` 身份运行，但这不允许修改虚拟机，也不会授予对 Windows 主机的 `Administrator` 访问权限。Linux 虚拟机充当安全边界，限制了可以访问的主机资源。文件共享使用用户空间构建的文件服务器，从主机绑定挂载到 Docker 容器中的任何目录仍然保留其原始权限。容器无法访问主机上的任何文件，除非这些文件被明确共享。

## 增强容器隔离

此外，Docker Desktop 支持 [增强容器隔离模式](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)（ECI），仅对企业客户可用，它进一步加强了容器安全性，同时不影响开发人员工作流程。

ECI 自动在 Linux 用户命名空间内运行所有容器，使得容器内的 root 映射到 Docker Desktop 虚拟机内的非特权用户。ECI 使用此技术及其他高级技术，进一步加强 Docker Desktop Linux 虚拟机内容器的安全性，使它们与 Docker 守护进程和虚拟机内运行的其他服务进一步隔离。

## Windows 容器

> [!WARNING]
>
> 启用 Windows 容器具有重要的安全影响。

与在虚拟机中运行的 Linux Docker 引擎和容器不同，Windows 容器使用操作系统功能实现，并直接在 Windows 主机上运行。如果您在安装期间启用 Windows 容器，容器内用于管理的 `ContainerAdministrator` 用户是主机上的本地管理员。在安装期间启用 Windows 容器意味着 `docker-users` 组的成员能够提升为主机上的管理员。对于不希望其开发人员运行 Windows 容器的组织，安装程序提供了 `-–no-windows-containers` 标志以禁用其使用。

## 网络

对于网络连接，Docker Desktop 使用用户空间进程（`vpnkit`），它继承了启动它的用户的约束，如防火墙规则、VPN、HTTP 代理属性等。