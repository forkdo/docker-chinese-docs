# 了解 Windows 的权限要求

本页包含有关在 Windows 上运行和安装 Docker Desktop 的权限要求、特权辅助进程 `com.docker.service` 的功能以及采用此方法的原因等信息。

本文还阐明了以 `root` 身份运行容器与在主机上拥有 `Administrator` 访问权限的区别，以及 Windows Docker 引擎和 Windows 容器的权限。

Windows 上的 Docker Desktop 在设计时考虑了安全性。仅在绝对必要时才需要管理权限。

## 权限要求

虽然 Windows 上的 Docker Desktop 可以在没有 `Administrator` 权限的情况下运行，但在安装过程中需要这些权限。安装时，会收到 UAC 提示，允许安装特权辅助服务。之后，Docker Desktop 就可以在没有管理员权限的情况下运行。

在没有特权辅助的情况下运行 Windows 上的 Docker Desktop 并不要求用户必须是 `docker-users` 组的成员。但是，某些需要特权操作的功能会有此要求。

如果您执行了安装，您会自动添加到该组中，但其他用户必须手动添加。这允许管理员控制谁有权访问需要更高权限的功能，例如创建和管理 Hyper-V VM，或使用 Windows 容器。

当 Docker Desktop 启动时，会创建所有非特权命名管道，以便只有以下用户可以访问它们：
- 启动 Docker Desktop 的用户。
- 本地 `Administrators` 组的成员。
- `LOCALSYSTEM` 帐户。

## 特权辅助

Docker Desktop 需要执行一组有限的特权操作，这些操作由特权辅助进程 `com.docker.service` 执行。这种方法遵循最小权限原则，使得 `Administrator` 访问权限仅用于绝对必要的操作，同时仍能以非特权用户身份使用 Docker Desktop。

特权辅助 `com.docker.service` 是一个 Windows 服务，在后台以 `SYSTEM` 特权运行。它监听命名管道 `//./pipe/dockerBackendV2`。开发者运行 Docker Desktop 应用程序，该程序连接到命名管道并向服务发送命令。此命名管道受到保护，只有 `docker-users` 组的用户才能访问它。

该服务执行以下功能：
- 确保在 Win32 hosts 文件中定义了 `kubernetes.docker.internal`。定义 DNS 名称 `kubernetes.docker.internal` 允许 Docker 与容器共享 Kubernetes 上下文。
- 确保在 Win32 hosts 文件中定义了 `host.docker.internal` 和 `gateway.docker.internal`。它们指向主机本地 IP 地址，并允许应用程序使用相同的名称从主机本身或容器解析主机 IP。
- 安全缓存注册表访问管理策略，该策略对开发者是只读的。
- 创建 Hyper-V VM `"DockerDesktopVM"` 并管理其生命周期 - 启动、停止和销毁。VM 名称在服务代码中是硬编码的，因此该服务不能用于创建或操作任何其他 VM。
- 移动 VHDX 文件或文件夹。
- 启动和停止 Windows Docker 引擎，并查询其是否正在运行。
- 删除所有 Windows 容器数据文件。
- 检查 Hyper-V 是否已启用。
- 检查引导加载程序是否激活了 Hyper-V。
- 检查所需的 Windows 功能是否已安装并启用。
- 执行运行状况检查并检索服务本身的版本。

服务启动模式取决于所选的容器引擎，对于 WSL，还取决于是否需要在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal`。这由设置页面中 `基于 WSL 2 的引擎` 下的设置控制。设置此选项后，WSL 引擎的行为与 Hyper-V 相同。因此：
- 对于 Windows 容器或 Hyper-v Linux 容器，服务在系统启动时启动并一直运行，即使 Docker Desktop 未运行。这是必需的，以便您可以在没有管理员权限的情况下启动 Docker Desktop。
- 对于 WSL2 Linux 容器，服务不是必需的，因此不会在系统启动时自动运行。当您切换到 Windows 容器或 Hyper-V Linux 容器，或选择在 Win32 hosts 文件中维护 `host.docker.internal` 和 `gateway.docker.internal` 时，会出现 UAC 提示，要求您接受特权操作以启动服务。如果接受，服务将启动并设置为在下次 Windows 启动时自动启动。

## 在 Linux VM 内部以 root 身份运行的容器

Linux Docker 守护进程和容器运行在一个由 Docker 管理的最小、专用的 Linux VM 中。它是不可变的，因此您无法扩展它或更改已安装的软件。这意味着，尽管容器默认以 `root` 身份运行，但这不允许更改 VM，也不会授予对 Windows 主机的 `Administrator` 访问权限。Linux VM 充当安全边界，并限制了可以访问的主机资源。文件共享使用用户空间精心制作的文件服务器，并且从主机绑定挂载到 Docker 容器中的任何目录仍保留其原始权限。容器无法访问任何超出显式共享范围的主机文件。

## 增强型容器隔离

此外，Docker Desktop 支持 [增强型容器隔离模式](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md) (ECI)，仅对商业客户可用，它可以在不影响开发者工作流的情况下进一步保护容器。

ECI 自动在 Linux 用户命名空间内运行所有容器，使得容器内的 root 映射到 Docker Desktop VM 内的一个非特权用户。ECI 利用这一点和其他先进技术进一步保护 Docker Desktop Linux VM 内的容器，使它们与 VM 内运行的 Docker 守护进程和其他服务进一步隔离。

## Windows 容器

> [!WARNING]
>
> 启用 Windows 容器具有重要的安全影响。

与在 VM 中运行的 Linux Docker 引擎和容器不同，Windows 容器使用操作系统功能实现，并直接在 Windows 主机上运行。如果您在安装过程中启用 Windows 容器，用于容器内管理的 `ContainerAdministrator` 用户是主机上的本地管理员。在安装过程中启用 Windows 容器使得 `docker-users` 组的成员能够提升为主机上的管理员。对于不希望其开发者运行 Windows 容器的组织，可以使用安装程序标志 `–-no-windows-containers` 来禁用它们的使用。

## 网络

对于网络连接，Docker Desktop 使用一个用户空间进程 (`vpnkit`)，该进程继承了启动它的用户的约束，如防火墙规则、VPN、HTTP 代理属性等。
