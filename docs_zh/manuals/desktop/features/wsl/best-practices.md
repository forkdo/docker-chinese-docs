---
linkTitle: 最佳实践
title: 在 Windows 上使用 WSL 2 的 Docker Desktop 最佳实践
description: 在 WSL 2 中使用 Docker Desktop 的最佳实践
keywords: wsl 2, docker desktop, best practices, Windows Subsystem for Linux, Docker Desktop Windows performance
tags:
- Best practices
aliases:
- /desktop/wsl/best-practices/
---

本页涵盖了在 Windows 上使用 WSL 2 运行 Docker Desktop 的建议，包括版本要求和文件系统性能。

## 保持 WSL 为最新版本

始终使用最新版本的 WSL。

至少必须使用 WSL 2.1.5 版本，否则 Docker Desktop 可能无法按预期工作。此外，如果您打算使用增强型容器隔离（Enhanced Container Isolation），请确保您使用的是 WSL 2.6 或更高版本。这是必需的，因为 ECI 依赖于至少 6.3.0 的 Linux 内核版本，而 WSL 2.6+ 捆绑了 Linux 内核版本 6.6。测试、开发和文档均基于最新的内核版本。较旧版本的 WSL 可能导致：
- Docker Desktop 定期挂起或在升级时挂起
- 通过 SCCM 部署失败
- `vmmem.exe` 消耗所有内存
- 网络筛选器策略被全局应用，而不是应用到特定对象
- 容器出现 GPU 故障

## 使用绑定挂载优化文件系统性能

为了在绑定挂载文件时获得最佳文件系统性能，请将源代码和其他需要绑定挂载到 Linux 容器的数据存储在 Linux 文件系统中。例如，在 Linux 文件系统中使用 `docker run -v <host-path>:<container-path>`，而不是在 Windows 文件系统中使用。您也可以参考 [Microsoft 的建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。

仅当原始文件存储在 Linux 文件系统中时，Linux 容器才会收到文件更改事件（“inotify 事件”）。例如，某些 Web 开发工作流依赖 inotify 事件在文件更改时自动重新加载。

当文件从 Linux 文件系统绑定挂载时，性能远高于从 Windows 主机文件系统访问。因此，请避免使用 `docker run -v /mnt/c/users:/users`，其中 `/mnt/c` 是从 Windows 挂载的。

相反，应从 Linux shell 使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 会被 Linux shell 展开为 `$HOME`。

## 限制 CPU 和内存使用情况

如果您担心 CPU 或内存使用情况，可以配置分配给 [WSL 2 实用程序 VM](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 的内存、CPU 和交换空间大小的限制。
