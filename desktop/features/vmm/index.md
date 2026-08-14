# 虚拟机管理器


Docker Desktop 支持多种虚拟机管理器 (VMM) 来为运行容器的 Linux 虚拟机提供动力。可用的选项取决于您的平台。

## Docker VMM



Docker VMM 是一种为容器优化的虚拟机管理程序。从 Docker Desktop 4.86 开始，Docker VMM 使用 Docker 自有虚拟机管理程序，取代了 4.35 - 4.85 版本中 Mac 用户使用的 `libkrun`。Docker VMM 专为容器工作负载构建，它可以：

- 在容器不活跃时将空闲内存返还给主机，这样 Docker Desktop 就不会占用它并未使用的内存
- 改善容器与主机之间的文件 I/O，减少编辑-编译-测试循环中的延迟
- 缩短引擎和容器的启动时间

由于 Docker 掌控虚拟化层，因此可以以前置后端无法做到的方式进行监控和管控。在 Windows 上，Docker VMM 提供了一个稳定的 WSL 2 替代方案，在容器环境和主机之间建立了真正的虚拟机边界。

### 切换到 Docker VMM

Docker VMM 要求至少为 Docker Linux 虚拟机分配 4 GB 内存。在切换之前，请在 **设置** > **资源** 中增加内存。

**Mac (Apple Silicon)**



1. 转到 **设置** > **常规** > **虚拟机管理器**。
2. 选择 **Docker VMM**。
3. 选择 **应用并重启**。

如果您之前已选择 Docker VMM，运行的引擎取决于您的版本：

- Docker Desktop 4.35 及更早版本由 `libkrun` 提供支持
- Docker Desktop 4.86 及更高版本由 Docker 自有虚拟机管理程序提供支持

如果您从 4.35 及更高版本升级，您的设置会被保留，并且 Docker Desktop 会在重启时自动切换到新的 Docker VMM。

**Windows**



1. 转到 **设置** > **常规** > **虚拟机管理器**。
2. 选择 **Docker VMM**。
3. 选择 **应用并重启**。



### 已知问题

- 切换到 Docker VMM 后，可能需要重启 Docker Desktop。
- Docker VMM 不支持绑定挂载自动共享。如果您看到 `file is not shared from the host` 错误，请转到 **设置** > **资源** > **文件共享**，并添加您想要共享的目录。

#### 仅限 Mac

- Docker VMM 目前不支持 Rosetta，因此 amd64 架构的模拟速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库（如 MongoDB 和 Cassandra）在使用 Docker VMM 的 virtiofs 时可能会失败。预计此问题将在未来的版本中解决。

## Mac 的替代 VMM

### Apple Virtualization 框架

Apple Virtualization 框架是 Mac 上管理虚拟机的稳定且成熟的选项。多年来，它一直是许多 Mac 用户的可靠选择。

### 适用于基于 Intel 的 Mac 的 HyperKit（传统）

> [!NOTE]
>
> HyperKit 已被弃用。Docker 建议切换到 Apple Virtualization 框架。

HyperKit 是基于 Intel 的 Mac 的传统虚拟化选项。Docker 建议切换到现代替代方案以获得更好的性能，并使您的设置面向未来。

## Windows 的替代 VMM

### WSL 2

WSL 2（Windows Subsystem for Linux 2）是 Docker Desktop 的默认 Windows 后端。它在轻量级虚拟机中运行完整的 Linux 内核，并与 Windows 主机文件系统和网络紧密集成。WSL 2 在单用户和所有用户安装模式下均可用，并且不需要管理员权限。

有关更多信息，请参阅 [Docker Desktop WSL 2 后端](/manuals/desktop/features/wsl/_index.md)。

### Hyper-V

Hyper-V 是 Windows 的原生虚拟机管理程序。它在完全隔离的虚拟机中运行 Docker Linux 虚拟机，在容器环境和 Windows 主机之间提供强大的边界。Hyper-V 仅在所有用户安装模式下可用，并且需要管理员权限。

