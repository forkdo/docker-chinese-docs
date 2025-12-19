---
title: 最佳实践
description: 在 WSL 2 环境下使用 Docker Desktop 的最佳实践
keywords: wsl, docker desktop, best practices
tags: [最佳实践]
aliases:
- /desktop/wsl/best-practices/
---

- 始终使用最新版本的 WSL。最低要求使用 WSL 2.1.5 版本，否则 Docker Desktop 可能无法正常工作。测试、开发和文档均基于最新的内核版本。旧版本的 WSL 可能导致：
    - Docker Desktop 定期卡死或在升级时卡死
    - 通过 SCCM 部署失败
    - `vmmem.exe` 进程耗尽所有内存
    - 网络过滤策略全局应用，而非针对特定对象
    - 容器中的 GPU 故障

- 为了在绑定挂载文件时获得最佳文件系统性能，建议将源代码和其他需要绑定挂载到 Linux 容器的数据存储在 Linux 文件系统中。例如，使用 `docker run -v <host-path>:<container-path>` 时，应将路径指定为 Linux 文件系统而非 Windows 文件系统。您也可以参考 Microsoft 的[建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - 只有当原始文件存储在 Linux 文件系统中时，Linux 容器才会接收到文件变更事件（即“inotify 事件”）。例如，某些 Web 开发工作流依赖 inotify 事件在文件变更时自动重载。
    - 当文件从 Linux 文件系统绑定挂载时，性能远高于从 Windows 主机远程挂载。因此应避免使用 `docker run -v /mnt/c/users:/users`，其中 `/mnt/c` 是从 Windows 挂载的。
    - 相反，在 Linux 终端中应使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 由 Linux 终端扩展为 `$HOME`。

- 如果您担心 `docker-desktop-data` 分发版的大小，请查看 [Windows 内置的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。
    - Docker Desktop 4.30 及以上版本的安装不再依赖 `docker-desktop-data` 分发版；而是创建并管理自己的虚拟硬盘（VHDX）用于存储。（但请注意，如果旧版本已创建了 `docker-desktop-data` 分发版，Docker Desktop 仍会继续使用它）。
    - 从 4.34 及以上版本开始，Docker Desktop 会自动管理托管 VHDX 的大小，并将未使用的空间返还给操作系统。

- 如果您担心 CPU 或内存占用，可以配置 [WSL 2 工具虚拟机](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 的内存、CPU 和交换空间大小限制。