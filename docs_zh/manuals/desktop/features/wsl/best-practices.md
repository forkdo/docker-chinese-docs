---
title: 最佳实践
description: 使用 Docker Desktop 和 WSL 2 的最佳实践
keywords: wsl, docker desktop, 最佳实践
tags: [最佳实践]
aliases:
- /desktop/wsl/best-practices/
---

- 始终使用最新版本的 WSL。最低要求使用 WSL 版本 2.1.5，否则 Docker Desktop 可能无法正常工作。测试、开发和文档都是基于最新的内核版本。较旧版本的 WSL 可能导致：
    - Docker Desktop 周期性挂起或在升级时挂起
    - 通过 SCCM 的部署失败
    - `vmmem.exe` 消耗所有内存
    - 网络过滤策略被全局应用，而不是应用到特定对象
    - 容器的 GPU 故障

- 为了在绑定挂载文件时获得最佳的文件系统性能，建议将源代码和其他需要绑定挂载到 Linux 容器的数据存储在 Linux 文件系统中。例如，在 Linux 文件系统中使用 `docker run -v <host-path>:<container-path>`，而不是在 Windows 文件系统中。您也可以参考 [Microsoft 的建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - Linux 容器只有在原始文件存储在 Linux 文件系统中时才能接收到文件变更事件（“inotify 事件”）。例如，某些 Web 开发工作流依赖 inotify 事件来在文件变更时自动重新加载。
    - 当文件从 Linux 文件系统绑定挂载时，性能远高于从 Windows 主机远程挂载。因此避免使用 `docker run -v /mnt/c/users:/users`，其中 `/mnt/c` 是从 Windows 挂载的。
    - 相反，从 Linux shell 使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 由 Linux shell 扩展为 `$HOME`。

- 如果您担心 `docker-desktop-data` 分发版的大小，请查看 [Windows 中内置的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。
    - Docker Desktop 4.30 及更高版本的安装不再依赖 `docker-desktop-data` 分发版；相反，Docker Desktop 创建并管理自己的虚拟硬盘（VHDX）用于存储。（但请注意，如果 `docker-desktop-data` 分发版已由较早版本的软件创建，Docker Desktop 会继续使用它。）
    - 从 4.34 版本开始，Docker Desktop 自动管理托管 VHDX 的大小，并将未使用的空间返回给操作系统。

- 如果您担心 CPU 或内存使用情况，可以配置分配给 [WSL 2 实用工具 VM](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 的内存、CPU 和交换空间大小的限制。