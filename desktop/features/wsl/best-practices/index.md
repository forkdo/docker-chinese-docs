# 最佳实践

- 始终使用最新版本的 WSL。至少必须使用 WSL 2.1.5 版本，否则 Docker Desktop 可能无法按预期工作。测试、开发和文档均基于最新的内核版本。较旧版本的 WSL 可能导致：
    - Docker Desktop 定期挂起或在升级时挂起
    - 通过 SCCM 部署失败
    - `vmmem.exe` 消耗所有内存
    - 网络筛选器策略被全局应用，而不是应用到特定对象
    - 容器出现 GPU 故障

- 为了在绑定挂载文件时获得最佳文件系统性能，建议将源代码和其他需要绑定挂载到 Linux 容器的数据存储在 Linux 文件系统中。例如，在 Linux 文件系统中使用 `docker run -v <host-path>:<container-path>`，而不是在 Windows 文件系统中使用。您也可以参考 Microsoft 的[建议](https://learn.microsoft.com/en-us/windows/wsl/compare-versions)。
    - 仅当原始文件存储在 Linux 文件系统中时，Linux 容器才会收到文件更改事件（“inotify 事件”）。例如，某些 Web 开发工作流依赖 inotify 事件在文件更改时自动重新加载。
    - 当文件从 Linux 文件系统绑定挂载时，性能远高于从 Windows 主机远程挂载。因此，请避免使用 `docker run -v /mnt/c/users:/users`，其中 `/mnt/c` 是从 Windows 挂载的。
    - 相反，应从 Linux shell 使用类似 `docker run -v ~/my-project:/sources <my-image>` 的命令，其中 `~` 会被 Linux shell 展开为 `$HOME`。

- 如果您担心 `docker-desktop-data` 发行版的大小，请查看 [Windows 内置的 WSL 工具](https://learn.microsoft.com/en-us/windows/wsl/disk-space)。
    - Docker Desktop 4.30 及更高版本的安装不再依赖 `docker-desktop-data` 发行版；相反，Docker Desktop 会创建并管理自己的虚拟硬盘 (VHDX) 进行存储。（但请注意，如果 `docker-desktop-data` 发行版已由早期版本的软件创建，Docker Desktop 会继续使用它）。
    - 从 4.34 版本开始，Docker Desktop 会自动管理受管 VHDX 的大小，并将未使用的空间返还给操作系统。

- 如果您担心 CPU 或内存使用情况，可以配置分配给 [WSL 2 实用程序 VM](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig) 的内存、CPU 和交换空间大小的限制。
