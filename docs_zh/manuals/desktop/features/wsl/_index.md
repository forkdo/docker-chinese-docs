---
description: 开启 Docker WSL 2 后端，使用最佳实践、GPU 支持等功能，高效开展工作。
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

Windows 子系统 for Linux (WSL) 2 是由 Microsoft 构建的完整 Linux 内核，它让用户无需管理虚拟机即可运行 Linux 发行版。使用 WSL 2 运行 Docker Desktop，用户可以利用 Linux 工作空间，避免维护 Linux 和 Windows 两套构建脚本。此外，WSL 2 还改进了文件系统共享和启动时间。

Docker Desktop 利用 WSL 2 的动态内存分配功能来改善资源消耗。这意味着 Docker Desktop 仅使用所需的 CPU 和内存资源，同时允许 CPU 和内存密集型任务（如构建容器）运行得更快。

此外，使用 WSL 2 后，Docker 守护进程在冷启动后的启动时间显著加快。

## 前置条件

在启用 Docker Desktop WSL 2 功能之前，请确保您已满足以下条件：

- WSL 版本至少为 2.1.5，但理想情况下使用最新版本的 WSL，以[避免 Docker Desktop 无法正常工作](best-practices.md)。
- 满足 Docker Desktop for Windows 的[系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)。
- 已在 Windows 上安装 WSL 2 功能。详细说明请参考 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。

> [!TIP]
>
> 为了在 WSL 上获得更好的体验，建议启用 WSL 的 [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings) 设置（自 WSL 1.3.10 起支持，实验性功能）。
>
> 此功能增强了 Windows 主机从 WSL 虚拟机中回收未使用内存的能力，确保为其他主机应用程序提供更好的内存可用性。这对于 Docker Desktop 尤其有益，因为它可以防止 WSL VM 在 Docker 容器镜像构建期间将大量内存（以 GB 计）保留在 Linux 内核的页面缓存中，且在 VM 内不再需要时无法释放回主机。

## 启用 Docker Desktop WSL 2

> [!IMPORTANT]
>
> 为避免与 Docker Desktop 使用 WSL 2 时可能产生冲突，您必须在安装 Docker Desktop 之前卸载通过 Linux 发行版直接安装的任何旧版本 Docker Engine 和 CLI。

1. 下载并安装最新版本的 [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows)。
2. 按照常规安装说明安装 Docker Desktop。根据您使用的 Windows 版本，Docker Desktop 可能在安装过程中提示您启用 WSL 2。阅读屏幕上显示的信息并启用 WSL 2 功能以继续安装。
3. 从 **Windows 开始** 菜单启动 Docker Desktop。
4. 导航到 **Settings**（设置）。
5. 在 **General**（常规）选项卡中，选择 **Use WSL 2 based engine**（使用基于 WSL 2 的引擎）。

    如果您在支持 WSL 2 的系统上安装了 Docker Desktop，此选项默认已启用。
6. 选择 **Apply**（应用）。

现在，您可以直接从 Windows 使用新的 WSL 2 引擎运行 `docker` 命令。

> [!TIP]
>
> 默认情况下，Docker Desktop 将 WSL 2 引擎的数据存储在 `C:\Users\[用户名]\AppData\Local\Docker\wsl`。如果您想更改位置（例如，更改为另一个驱动器），可以通过 Docker 仪表板的 **Settings -> Resources -> Advanced**（设置 -> 资源 -> 高级）页面进行设置。
> 有关 Windows 设置的更多信息，请参阅 [更改设置](/manuals/desktop/settings-and-maintenance/settings.md)。

## 在 WSL 2 发行版中启用 Docker 支持

WSL 2 为 Windows 添加了对“Linux 发行版”的支持，每个发行版的行为都像一个虚拟机，但它们都在一个共享的 Linux 内核之上运行。

Docker Desktop 不要求安装任何特定的 Linux 发行版。`docker` CLI 和 UI 均可在 Windows 上正常工作，无需额外的 Linux 发行版。但为了获得最佳开发体验，我们建议至少安装一个额外的发行版并启用 Docker 支持：

1. 确保发行版运行在 WSL 2 模式下。WSL 可以在 v1 或 v2 模式下运行发行版。

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

2. 当 Docker Desktop 启动后，转到 **Settings**（设置）> **Resources**（资源）> **WSL Integration**（WSL 集成）。

    Docker-WSL 集成默认在 [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install) 上启用，这是默认的 WSL 发行版。要更改默认 WSL 发行版，请运行：
     ```console
    $ wsl.exe --set-default <发行版名称>
    ```
   如果 **Resources**（资源）下没有 **WSL integrations**（WSL 集成），Docker 可能处于 Windows 容器模式。在任务栏中选择 Docker 菜单，然后选择 **Switch to Linux containers**（切换到 Linux 容器）。

3. 选择 **Apply**（应用）。

> [!NOTE]
>
> 在 Docker Desktop 4.30 及更早版本中，Docker Desktop 安装了两个特殊用途的内部 Linux 发行版 `docker-desktop` 和 `docker-desktop-data`。`docker-desktop` 用于运行 Docker 引擎 `dockerd`，而 `docker-desktop-data` 用于存储容器和镜像。两者都不能用于常规开发。
>
> 对于 Docker Desktop 4.30 及更高版本的新安装，不再创建 `docker-desktop-data`。相反，Docker Desktop 创建并管理自己的虚拟硬盘用于存储。`docker-desktop` 发行版仍然被创建并用于运行 Docker 引擎。
>
> 请注意，Docker Desktop 4.30 及更高版本如果检测到 `docker-desktop-data` 发行版已由早期版本的 Docker Desktop 创建且未进行全新安装或出厂重置，将继续使用该发行版。

## Docker Desktop 中的 WSL 2 安全性

Docker Desktop 的 WSL 2 集成在 WSL 的现有安全模型内运行，不会引入超出标准 WSL 行为的额外安全风险。

Docker Desktop 在其专用的 WSL 发行版 `docker-desktop` 中运行，遵循与其他 WSL 发行版相同的隔离属性。Docker Desktop 与其他已安装 WSL 发行版之间的唯一交互发生在启用 Docker Desktop **WSL 集成**功能时（在设置中）。此功能允许从集成的发行版轻松访问 Docker CLI。

WSL 旨在促进 Windows 和 Linux 环境之间的互操作性。其文件系统可从 Windows 主机 `\\wsl$` 访问，这意味着 Windows 进程可以读取和修改 WSL 内的文件。这种行为并非 Docker Desktop 特有，而是 WSL 本身的核心特性。

对于关注 WSL 安全风险并希望更严格隔离和安全控制的组织，可以在 Hyper-V 模式下运行 Docker Desktop，而不是 WSL 2。或者，在启用[增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)的情况下运行容器工作负载。

## 附加资源

- [探索最佳实践](best-practices.md)
- [了解如何使用 Docker 和 WSL 2 进行开发](use-wsl.md)
- [了解 WSL 2 的 GPU 支持](/manuals/desktop/features/gpu.md)
- [WSL 上的自定义内核](custom-kernels.md)