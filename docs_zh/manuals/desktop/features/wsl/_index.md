---
description: 开启 Docker WSL 2 后端，并在本详尽指南中使用最佳实践、GPU 支持等功能开始工作。
keywords: wsl, wsl2, 安装 wsl2, wsl 安装, docker wsl2, wsl docker, wsl2 技术预览, wsl 安装 docker, 安装 docker wsl, 如何在 wsl 中安装 docker
title: Windows 上的 Docker Desktop WSL 2 后端
linkTitle: WSL
weight: 120
aliases:
- /docker-for-windows/wsl/
- /docker-for-windows/wsl-tech-preview/
- /desktop/windows/wsl/
- /desktop/wsl/
---

Windows Subsystem for Linux (WSL) 2 是由 Microsoft 构建的完整 Linux 内核，它让 Linux 发行版无需管理虚拟机即可运行。通过在 WSL 2 上运行 Docker Desktop，用户可以利用 Linux 工作区，避免同时维护 Linux 和 Windows 构建脚本。此外，WSL 2 在文件系统共享和启动时间方面进行了改进。

Docker Desktop 使用 WSL 2 中的动态内存分配功能来改善资源消耗。这意味着 Docker Desktop 仅使用所需的 CPU 和内存量，同时允许 CPU 和内存密集型任务（例如构建容器）运行得更快。

此外，使用 WSL 2，冷启动后启动 Docker 守护进程所需的时间显著缩短。

## 先决条件

在开启 Docker Desktop WSL 2 功能之前，请确保您已满足以下条件：

- 至少拥有 WSL 2.1.5 版本，但最好是 WSL 的最新版本，以[避免 Docker Desktop 无法按预期工作](best-practices.md)。
- 满足 Docker Desktop for Windows 的[系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)。
- 在 Windows 上安装了 WSL 2 功能。有关详细说明，请参阅 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。

> [!TIP]
>
> 为了在 WSL 上获得更好的体验，建议启用 WSL
> [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings)
> 设置（自 WSL 1.3.10 起可用，实验性）。
>
> 此功能增强了 Windows 主机回收 WSL 虚拟机内未使用内存的能力，确保为其他主机应用程序提供更好的内存可用性。此功能对 Docker Desktop 特别有益，因为它可以防止 WSL VM 在 Docker 容器镜像构建期间在 Linux 内核的页面缓存中保留大量内存（以 GB 为单位），并在 VM 内不再需要时将其释放回主机。

## 开启 Docker Desktop WSL 2

> [!IMPORTANT]
>
> 为避免在 Docker Desktop 上使用 WSL 2 时出现任何潜在冲突，您必须在安装 Docker Desktop 之前卸载通过 Linux 发行版直接安装的任何旧版 Docker Engine 和 CLI。

1. 下载并安装最新版本的 [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows)。
2. 按照常规安装说明安装 Docker Desktop。根据您使用的 Windows 版本，Docker Desktop 可能会在安装期间提示您开启 WSL 2。阅读屏幕上显示的信息并开启 WSL 2 功能以继续。
3. 从 **Windows 开始** 菜单启动 Docker Desktop。
4. 导航至 **设置 (Settings)**。
5. 在 **通用 (General)** 选项卡中，选择 **使用 WSL 2 引擎 (Use WSL 2 based engine)**。

    如果您在支持 WSL 2 的系统上安装了 Docker Desktop，此选项默认开启。
6. 选择 **应用 (Apply)**。

现在，使用新的 WSL 2 引擎，`docker` 命令可以在 Windows 中正常工作。

> [!TIP]
>
> 默认情况下，Docker Desktop 将 WSL 2 引擎的数据存储在 `C:\Users\[用户名]\AppData\Local\Docker\wsl`。
> 如果您想更改位置，例如更改为其他驱动器，可以通过 Docker 仪表板的 `设置 -> 资源 -> 高级 (Settings -> Resources -> Advanced)` 页面进行操作。
> 有关此设置及其他 Windows 设置的更多信息，请阅读[更改设置](/manuals/desktop/settings-and-maintenance/settings.md)。

## 在 WSL 2 发行版中启用 Docker 支持

WSL 2 为 Windows 添加了对 "Linux 发行版" 的支持，其中每个发行版的行为类似于虚拟机，但它们都运行在共享的 Linux 内核之上。

Docker Desktop 不需要安装任何特定的 Linux 发行版。`docker` CLI 和 UI 都可以在 Windows 上正常工作，无需任何额外的 Linux 发行版。但是，为了获得最佳的开发者体验，我们建议至少安装一个额外的发行版并启用 Docker 支持：

1. 确保发行版在 WSL 2 模式下运行。WSL 可以在 v1 或 v2 模式下运行发行版。

    要检查 WSL 模式，请运行：

     ```console
     $ wsl.exe -l -v
     ```

    要将 Linux 发行版升级到 v2，请运行：

    ```console
    $ wsl.exe --set-version (发行版名称) 2
    ```

    要将 v2 设置为未来安装的默认版本，请运行：

    ```console
    $ wsl.exe --set-default-version 2
    ```

2. 当 Docker Desktop 启动时，转到 **设置 (Settings)** > **资源 (Resources)** > **WSL 集成 (WSL Integration)**。

    Docker-WSL 集成在默认 WSL 发行版上启用，即 [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install)。要更改您的默认 WSL 发行版，请运行：
     ```console
    $ wsl.exe --set-default <发行版名称>
    ```
   如果 **WSL 集成 (WSL integrations)** 在 **资源 (Resources)** 下不可用，Docker 可能处于 Windows 容器模式。在任务栏中，选择 Docker 菜单，然后选择 **切换到 Linux 容器 (Switch to Linux containers)**。

3. 选择 **应用 (Apply)**。

> [!NOTE]
>
> 在 Docker Desktop 4.30 及更早版本中，Docker Desktop 会安装两个特殊用途的内部 Linux 发行版 `docker-desktop` 和 `docker-desktop-data`。`docker-desktop` 用于运行 Docker 引擎 `dockerd`，而 `docker-desktop-data` 用于存储容器和镜像。两者都不能用于常规开发。
>
> 对于 Docker Desktop 4.30 及更高版本的全新安装，不再创建 `docker-desktop-data`。相反，Docker Desktop 会创建并管理自己的虚拟硬盘进行存储。`docker-desktop` 发行版仍然会被创建并用于运行 Docker 引擎。
>
> 请注意，如果 `docker-desktop-data` 发行版是由旧版 Docker Desktop 创建的，并且未进行全新安装或恢复出厂设置，则 Docker Desktop 4.30 及更高版本会继续使用该发行版。

## Docker Desktop 中的 WSL 2 安全性

Docker Desktop 的 WSL 2 集成在 WSL 的现有安全模型内运行，不会引入超出标准 WSL 行为的额外安全风险。

Docker Desktop 在其自己专用的 WSL 发行版 `docker-desktop` 中运行，该发行版遵循与其他任何 WSL 发行版相同的隔离属性。Docker Desktop 与其他已安装的 WSL 发行版之间的唯一交互发生在设置中启用了 Docker Desktop **WSL 集成** 功能时。此功能允许从集成的发行版轻松访问 Docker CLI。

WSL 旨在促进 Windows 和 Linux 环境之间的互操作性。其文件系统可从 Windows 主机 `\\wsl$` 访问，这意味着 Windows 进程可以读取和修改 WSL 内的文件。此行为并非 Docker Desktop 特有，而是 WSL 本身的核心方面。

对于担心 WSL 相关安全风险并希望更严格隔离和安全控制的组织，请改用 Hyper-V 模式运行 Docker Desktop，而不是 WSL 2。或者，使用[增强型容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)运行您的容器工作负载。

## 其他资源

- [探索最佳实践](best-practices.md)
- [了解如何使用 Docker 和 WSL 2 进行开发](use-wsl.md)
- [了解 WSL 2 的 GPU 支持](/desktop/features/gpu.md)
- [WSL 上的自定义内核](custom-kernels.md)