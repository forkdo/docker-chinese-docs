# Windows 上的 Docker Desktop WSL 2 后端


Windows Subsystem for Linux (WSL) 2 是由 Microsoft 构建的一个完整的 Linux 内核，它允许 Linux 发行版在无需管理虚拟机的情况下运行。在 WSL 2 上运行 Docker Desktop 时，用户可以利用 Linux 工作空间，并避免同时维护 Linux 和 Windows 构建脚本。此外，WSL 2 在文件系统共享、更快的冷启动时间以及动态资源分配方面都有所改进。

由于 WSL 2 使用动态内存分配，Docker Desktop 仅请求其实际需要的 CPU 和内存——从而为系统的其余部分释放资源，同时仍让多阶段镜像构建等内存密集型任务以全速运行。

## 先决条件

在开启 Docker Desktop WSL 2 功能之前，请确保你已：

*   最低要求为 WSL 版本 2.1.5，但理想情况下，为了[避免 Docker Desktop 无法按预期工作](best-practices.md)，请使用最新版本的 WSL。
*   满足 Docker Desktop for Windows 的[系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)。
*   已在 Windows 上安装 WSL 2 功能。有关详细说明，请参阅 [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。

> [!TIP]
>
> 考虑启用自 WSL 1.3.10 起可用的（实验性）WSL
> [autoMemoryReclaim](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#experimental-settings)
> 设置。
> 此设置允许 Windows 回收 WSL 虚拟机中未使用的内存，防止 Linux 内核的页缓存在容器镜像构建完成后仍持有大量 RAM。其结果是为主机上的其他应用程序提供更好的内存可用性。

## 开启 Docker Desktop WSL 2

在安装 Docker Desktop 之前，请卸载任何直接安装在 WSL Linux 发行版内部的 Docker Engine 或 Docker CLI 版本。同时运行两者可能会导致冲突。

1.  下载并安装最新版本的 [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-windows)。
2.  按照常规的安装说明安装 Docker Desktop。根据你使用的 Windows 版本，Docker Desktop 可能会在安装过程中提示你开启 WSL 2。请阅读屏幕上显示的信息，并开启 WSL 2 功能以继续。
3.  从 **Windows 开始**菜单启动 Docker Desktop。
4.  导航到 **设置**。
5.  在 **常规** 选项卡中，选择 **基于 WSL 2 的引擎**。

    如果你在支持 WSL 2 的系统上安装了 Docker Desktop，则此选项默认开启，且该设置不可见。
6.  选择 **应用**。

`docker` 命令现在可以在任何 Windows 终端中使用 WSL 2 引擎运行。

> [!TIP]
>
> 默认情况下，Docker Desktop 将 WSL 2 引擎的数据存储在 `C:\Users\[USERNAME]\AppData\Local\Docker\wsl`。
> 如果你想更改位置，请转到 Docker 仪表盘中的 `设置 -> 资源 -> 高级` 页面。
> 在[更改设置](/manuals/desktop/settings-and-maintenance/settings.md)中了解更多关于此设置及其他 Windows 设置的信息。

## 在 WSL 2 发行版中启用 Docker

WSL 2 允许多个 Linux 发行版在单个共享内核上并排运行。Docker Desktop 不需要安装特定的发行版，并且 `docker` 命令可以在没有发行版的情况下从 Windows 正常工作。但是，为发行版启用 WSL 集成可以让你从该发行版的终端直接访问 `docker` 命令——这对于 Linux 原生开发工作流非常有用。

1.  确保发行版在 WSL 2 模式下运行。WSL 可以在 v1 或 v2 模式下运行发行版。

    要检查 WSL 模式，请运行：

    ```console
    $ wsl.exe -l -v
    ```

    要将 Linux 发行版升级到 v2，请运行：

    ```console
    $ wsl.exe --set-version (distribution name) 2
    ```

    要将 v2 设置为未来安装的默认版本，请运行：

    ```console
    $ wsl.exe --set-default-version 2
    ```

2.  当 Docker Desktop 启动时，转到 **设置** > **资源** > **WSL 集成**。

    Docker-WSL 集成在默认的 WSL 发行版（即 [Ubuntu](https://learn.microsoft.com/en-us/windows/wsl/install)）上启用。要更改你的默认 WSL 发行版，请运行：
     ```console
    $ wsl.exe --set-default <distribution name>
    ```
   如果 **WSL 集成** 在 **资源** 下不可用，Docker 可能处于 Windows 容器模式。在你的任务栏中，选择 Docker 菜单，然后选择 **切换到 Linux 容器**。

3.  选择 **应用**。

## Docker Desktop 中的 WSL 2 安全性

Docker Desktop 的 WSL 2 集成在 WSL 的现有安全模型内运行，除了标准的 WSL 行为外，不会引入安全风险。

Docker Desktop 在其自己的 `docker-desktop` WSL 发行版内运行，其隔离属性与任何其他两个 WSL 发行版之间相互隔离的方式相同。只有当你为这些发行版显式启用 WSL 集成时，Docker Desktop 才会与其他发行版发生交互。此功能允许从集成的发行版轻松访问 Docker CLI。

WSL 旨在促进 Windows 和 Linux 环境之间的互操作性。其文件系统可以从 Windows 主机上的 `\\wsl$` 访问，这意味着 Windows 进程可以读取和修改 WSL 内的文件。此行为并非 Docker Desktop 特有，而是 WSL 本身的一个核心方面。

对于需要更严格隔离的环境：

- 改为在 Hyper-V 模式下运行 Docker Desktop，以完全避开共享内核模型。
- 启用[增强型容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)，以在任何后端的情况下都为容器工作负载增加一层额外的保护。

## 其他资源

*   [探索最佳实践](best-practices.md)
*   [了解如何使用 Docker 和 WSL 2 进行开发](use-wsl.md)
*   [了解 WSL 2 的 GPU 支持](/manuals/desktop/features/gpu.md)
*   [WSL 上的自定义内核](custom-kernels.md)

