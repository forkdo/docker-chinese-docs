# 更改 Docker Desktop 设置


使用 Docker Desktop 的设置来自定义其行为并优化性能和资源使用。

打开 **Settings** 有两种方式：

- 选择 Docker 菜单 


![whale menu](../images/whale-x.svg)，然后选择 **Settings**
- 从 Docker Desktop 仪表板中选择 **Settings** 图标。

您也可以找到 `settings-store.json` 文件：

 - Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
 - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
 - Linux: `~/.docker/desktop/settings-store.json`

有关在组织级别强制执行设置的信息，请参阅 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md)。

## General

配置 Docker Desktop 的启动行为、UI 外观、终端偏好和功能默认值。

| 设置 | 说明 | 默认值 | 平台 | 备注 |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------ | ------------ | ------------------------------------- |
| **Start Docker Desktop when you sign in to your computer** | 登录计算机时自动启动 Docker Desktop。 | 关闭 | 全部 | 推荐频繁使用的用户开启。 |
| **Open Docker Dashboard when Docker Desktop starts** | 启动 Docker Desktop 时自动打开仪表板。 | 关闭 | 全部 | |
| **Choose theme for Docker Desktop** | 为 Docker Desktop 应用 **Light** 或 **Dark** 主题。 | **Use system settings**。 | 全部 | |
| **Configure shell completions** | 编辑 shell 配置，在终端中按 `<Tab>` 时为命令、标志和 Docker 对象启用自动补全。更多信息请参阅 [Completion](/manuals/engine/cli/completion.md)。 | 关闭 | 全部 | |
| **Choose container terminal** | 设置选择容器终端时打开的终端。使用集成终端可从仪表板在运行中的容器中执行命令。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md)。 | 关闭 | 全部 | |
| **Enable Docker terminal**。 | 直接从 Docker Desktop 与主机交互并执行命令。 | 关闭 | 全部 | |
| **Enable Docker Debug by default** | 打开集成终端时默认使用 Docker Debug。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md#integrated-terminal)。 | 关闭 | 全部 | |
| **Include VM in Time Machine backups** | 备份 Docker Desktop 虚拟机。 | 关闭 | Mac | |
| **Use containerd for pulling and storing images** | 使用 containerd 镜像存储而非经典镜像存储。更多信息请参阅 [containerd image store](/manuals/desktop/features/containerd.md)。 | 开启 | 全部 | |
| **Expose daemon on tcp://localhost:2375 without TLS** | 允许旧版客户端连接 Docker 守护进程。请谨慎使用，因为不使用 TLS 暴露守护进程可能导致远程代码执行攻击。 | 关闭 | Windows（仅 Hyper-V 后端） | |
| **Use the WSL 2 based engine** | WSL 2 比 Hyper-V 后端性能更好。更多信息请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。 | 关闭 | Windows | |
| **Add \*.docker.internal to host file** | 添加内部 DNS 条目。 | 开启 | Windows | 有助于解析 Docker 内部域名 |
| **Choose Virtual Machine Manager (VMM)** | 选择用于创建和管理 Docker Desktop Linux VM 的 VMM。更多信息请参阅 [Virtual Machine Manager](/manuals/desktop/features/vmm.md)。 | | Mac、Windows | 选择 **Docker VMM** 以获得优化的容器性能。Docker VMM 处于 Beta 阶段。 |
| **Choose file sharing implementation for your containers** | 选择是否使用 **VirtioFS** 或 **gRPC FUSE** 来共享文件。 | **VirtioFS** | Mac | 使用 VirtioFS 实现快速文件共享。VirtioFS 将文件系统操作完成时间减少了 [多达 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206)。它是 Docker VMM 支持的唯一文件共享实现。 |
|**Use Rosetta for x86_64/amd64 emulation on Apple Silicon** | 在 Apple Silicon 上加速 x86/AMD64 二进制仿真。只有当您选择 **Apple Virtualization framework** 作为虚拟机管理器时，此选项才可用。 | 关闭 | Mac | |
| **Send usage statistics** | 向 Docker 发送诊断信息、崩溃报告和使用数据，以改进并排查应用程序问题。Docker 可能会定期提示您提供更多信息。 | 开启 | 全部 | |
| **Use Enhanced Container Isolation** | 防止容器突破 Linux VM。更多信息请参阅 [Enhanced Container Isolation](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)。 | 关闭 | 全部 | 必须已登录并拥有 Docker Business 订阅。 |
| **Show CLI hints** | 在终端中显示有用的 CLI 建议。 | 开启 | 全部 | 提高可发现性 |
| **Enable Docker Scout image analysis** | 检查镜像时显示 **Start analysis** 按钮，使用 Docker Scout 分析镜像。 | 开启 | 全部 | |
| **Enable background SBOM indexing** | 自动分析您构建或拉取的镜像。 | 关闭 | 全部 | |
| **Automatically check configuration** | 定期检查您的配置，确保其他应用程序未对其进行意外更改。如果发现更改会通知您，并可直接从通知中恢复配置。更多信息请参阅 [FAQs](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md#why-do-i-keep-getting-a-notification-telling-me-an-application-has-changed-my-desktop-configurations)。 | 开启 | Mac | Docker Desktop 会检查安装期间配置的设置是否被外部应用程序（如 Orbstack）更改。Docker Desktop 会检查 Docker 二进制文件到 `/usr/local/bin` 的符号链接以及默认 Docker 套接字的符号链接。此外，Docker Desktop 确保在启动时上下文切换到 `desktop-linux`。 |

## Resources

控制可供 Docker Desktop 使用的 CPU、内存、磁盘、文件共享、代理和网络资源。

### Advanced

| 设置 | 说明 | 平台 | 备注 |
| ------------------- | ----------------------------------------- | -------- | ------------------------------------- |
| **CPU limit** | 指定 Docker Desktop 可使用的最大 CPU 数。 | Mac、Linux、Windows Hyper-V | |
| **Memory limit** | 分配给 Docker VM 的 RAM。 | Mac、Linux、Windows Hyper-V | 默认为主机内存的 50%。 |
| **Swap** | 根据需要配置交换文件大小。 | Mac、Linux、Windows Hyper-V | 默认 1 GB。 |
| **Disk usage limit** | 指定引擎可使用的最大磁盘空间量。 | Mac、Linux、Windows Hyper-V | |
|  **Disk image location** | 指定存储容器和镜像的 Linux 卷位置。在 **Advanced** 选项卡中，您可以限制 Docker Linux VM 可用的资源。 | Mac、Linux、Windows Hyper-V | 您也可以将磁盘映像移动到不同位置。如果您尝试将磁盘映像移动到已有映像的位置，系统会询问您是要使用现有映像还是替换它。 |
| **Resource Saver** | 启用或禁用 [Resource Saver mode](/manuals/desktop/use-desktop/resource-saver.md)，通过在 Docker Desktop 空闲时自动关闭 Linux VM 来显著减少主机的 CPU 和内存使用。 | Mac、Linux、Windows Hyper-V | 容器运行时自动重启。重启可能需要 3–10 秒。 |

在 WSL 2 模式下，请在 [WSL 2 utility VM](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig) 上配置内存、CPU 和交换限制。

> [!TIP]
>
> 如果您感觉 Docker Desktop 开始变慢或运行多容器工作负载，请增加内存和磁盘映像空间分配。

### File sharing

使用文件共享允许您机器上的本地目录与 Linux 容器共享。这对于在主机上的 IDE 中编辑源代码同时在容器中运行和测试代码特别有用。

| 设置 | 说明 | 平台 | 备注 |
| ------------------- | ----------------------------------------- | -------- | ------------------------------------- |
| **Synchronized file shares** | 快速灵活的主机到 VM 文件共享，通过使用同步的文件系统缓存增强绑定挂载性能。要了解更多信息，请参阅 [Synchronized file share](/manuals/desktop/features/synchronized-file-sharing.md)。 | Mac、Linux、Windows Hyper-V | Pro、Team 和 Business 订阅提供。 |
| **Virtual file shares** | 与 Linux 容器共享本地目录。默认情况下，`/Users`、`/Volumes`、`/private`、`/tmp` 和 `/var/folders` 目录被共享。如果您的项目在此目录之外，则必须将其添加到列表中，否则您可能在运行时遇到 `Mounts denied` 或 `cannot start service` 错误。 | Mac、Linux、Windows Hyper-V | |


- 只共享您需要与容器共享的目录。文件共享会引入开销，因为主机上文件的任何更改都需要通知 Linux VM。共享过多文件会导致高 CPU 负载和文件系统性能变慢。
- 共享文件夹设计用于允许应用程序代码在主机上编辑，同时在容器中执行。对于缓存目录或数据库等非代码项，如果它们存储在 Linux VM 中，使用 [data volume](/manuals/engine/storage/volumes.md)（命名卷）或 [data container](/manuals/engine/storage/volumes.md) 性能会好得多。
- 如果您将整个主目录共享到容器中，Mac 可能会提示您授予 Docker 访问主目录中个人区域（如提醒事项或下载）的权限。
- 默认情况下，Mac 文件系统不区分大小写，而 Linux 区分大小写。在 Linux 上，可以创建两个独立的文件：`test` 和 `Test`，而在 Mac 上这些文件名实际上指的是同一个基础文件。这可能导致应用程序在开发人员机器上工作正常（文件内容被共享），但在 Linux 生产环境中运行时失败（文件内容不同）。为避免这种情况，Docker Desktop 坚持所有共享文件必须以其原始大小写访问。因此，如果创建了一个名为 `test` 的文件，它必须以 `test` 打开。尝试打开 `Test` 将失败，错误为 "No such file or directory"。同样，一旦创建了名为 `test` 的文件，尝试创建名为 `Test` 的第二个文件将失败。

有关更多信息，请参阅 [Volume mounting requires file sharing for any project directories outside of `/Users`](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)。

### Proxies

Docker Desktop 支持 HTTP/HTTPS 和 SOCKS5 代理。SOCKS5 需要 Business 订阅。

要防止开发人员意外更改代理设置，请参阅 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md#what-features-can-i-configure-with-settings-management)。

#### Docker Desktop proxy

用于 Docker Desktop 主机级别的流量：登录 Docker、Desktop 应用程序、CLI 和扩展。仅在未配置 [Containers proxy](#containers-proxy) 时，作为 `docker image pull` 的回退。

| 代理模式 | 说明 |
|------------|-------------|
| **System proxy** | 使用主机上配置的代理（静态或代理自动配置 (PAC)）。Docker Desktop 会自动读取。 |
| **No proxy** | 直接连接，不使用代理。 |
| **Manual configuration** | 手动输入 **Web Server (HTTP)** 和 **Secure Web Server (HTTPS)** URL。使用格式 `http://proxy:port` 或 `https://proxy:port`。您还可以指定应绕过代理的主机和域，例如：`registry-1.docker.com,*.docker.com,10.0.0.0/8`。 |

> [!NOTE]
>
> 如果您使用托管在 Web 服务器上的 PAC 文件，请为 `.pac` 扩展名添加 MIME 类型 `application/x-ns-proxy-autoconfig`。否则 PAC 文件可能无法正确解析。请参阅 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md#proxy-auto-configuration-files)。

#### Containers proxy

用于 `docker image pull`（始终强制执行——所有 `docker pull` 和 Compose 拉取操作都经过此代理）以及在配置了气隙容器强制时来自运行中的容器的出站流量。如果在此配置了 PAC 文件，请确保它为 Docker 注册表端点返回合适的代理服务器，否则镜像拉取将失败。

| 代理模式 | 说明 |
|------------|-------------|
| **Same as host proxy** | 使用与 Docker Desktop 代理相同的代理配置。 |
| **System proxy** | 使用主机上配置的代理。 |
| **No proxy** | 直接连接，不使用代理。 |
| **Manual configuration** | 手动输入 **Web Server (HTTP)** 和 **Secure Web Server (HTTPS)** URL。使用格式 `http://proxy:port` 或 `https://proxy:port`。您还可以指定应绕过代理的主机和域，例如：`registry-1.docker.com,*.docker.com,10.0.0.0/8`。 |

> [!NOTE]
>
> 用于镜像扫描的 HTTPS 代理使用 `HTTPS_PROXY` 环境变量配置。

#### Proxy authentication

| 方法 | 行为 | 备注 |
|--------|-----------| ----- |
| **Basic** | Docker Desktop 提示输入凭据并将其缓存在操作系统凭据存储中。 | 使用 `https://` 代理 URL 以在传输过程中保护密码。支持 TLS 1.3。 |
| **Kerberos / NTLM** | 集中身份验证——开发人员不会被提示输入凭据，降低了账户锁定的风险。如果代理在 407 响应中返回多种方案，Docker Desktop 默认选择 Basic。 | 需要 Business 订阅。要启用 Kerberos 或 NTLM 代理身份验证，您必须在通过命令行安装期间传递 `--proxy-enable-kerberosntlm` 安装程序标志，并确保您的代理服务器正确配置了 Kerberos 或 NTLM 身份验证。 |

### Network

> [!NOTE]
>
> 在 Windows 上，**Network** 选项卡在 Windows 容器模式下不可用，因为 Windows 管理网络。

| 设置 | 说明 | 平台 |
|---------|-------------|----------|
| **Docker subnet** | 设置自定义子网以避免与您环境中的 IP 冲突。Docker Desktop 使用私有 IPv4 网络用于内部服务，包括 DNS 服务器和 HTTP 代理。默认：`192.168.65.0/24`。 | 全部 |
| **Use kernel networking for UDP** | 为 UDP 流量使用更高效的内核网络路径。可能与 VPN 软件不兼容。 | Mac |
| **Enable host networking** | 允许使用 `--net=host` 启动的容器使用 `localhost` 连接到主机上的 TCP 和 UDP 服务。还允许主机软件使用 `localhost` 连接到容器中的 TCP 和 UDP 服务。 | Mac |

在 Windows 和 Mac 上，您还可以设置默认网络模式和 DNS 解析行为。更多信息请参阅 [Networking](/manuals/desktop/features/networking/networking-how-tos.md#network-how-tos-for-mac-and-windows)。

### WSL integration (Windows only)

| 设置 | 说明 | 备注 |
| ------------------- | ----------------------------------------- | ------------------------------------- |
| WSL distribution integration | 选择哪些 WSL 2 发行版启用 Docker WSL 集成。 | 默认在您的默认 WSL 发行版上启用集成。要更改默认发行版，请运行 `wsl --set-default <distribution name>`。 |

有关配置 Docker Desktop 使用 WSL 2 的更多详细信息，请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。

## Docker Engine

使用 JSON 配置文件配置 Docker 守护进程。

该文件位于 `$HOME/.docker/daemon.json`。可直接在 Docker Desktop 仪表板或文本编辑器中编辑它。

要查看可能的配置选项的完整列表，请参阅 [dockerd command reference](/reference/cli/dockerd/)。

## Builders

使用 **Builders** 选项卡在 Docker Desktop 设置中检查和管理构建器。

### Inspect

要检查构建器，找到您要检查的构建器并选择展开图标。您只能检查活动构建器。

检查活动构建器会显示：

- BuildKit 版本
- 状态
- 驱动类型
- 支持的功能和平台
- 磁盘使用情况
- 端点地址

### Select a different builder

**Selected builder** 部分显示所选的构建器。
要选择不同的构建器：

1. 在 **Available builders** 下找到您要使用的构建器
2. 打开构建器名称旁边的下拉菜单。
3. 选择 **Use** 切换到此构建器。

您的构建命令现在默认使用所选的构建器。

### Create a builder

要创建构建器，请使用 Docker CLI。请参阅 [Create a new builder](/build/builders/manage/#create-a-new-builder)

### Remove a builder

如果满足以下条件，您可以删除构建器：

- 构建器不是您的 [selected builder](/build/builders/#selected-builder)
- 构建器未 [与 Docker 上下文关联](/build/builders/#default-builder)。

  要删除与 Docker 上下文关联的构建器，请使用 `docker context rm` 命令删除上下文。

要删除构建器：

1. 在 **Available builders** 下找到您要删除的构建器
2. 打开下拉菜单。
3. 选择 **Remove** 删除此构建器。

如果构建器使用 `docker-container` 或 `kubernetes` 驱动，构建缓存和构建器也会被删除。

### Stop and start a builder

使用 [`docker-container` 驱动](/build/builders/drivers/docker-container/) 的构建器在容器中运行 BuildKit 守护进程。
您可以使用下拉菜单启动和停止 BuildKit 容器。

如果容器已停止，运行构建会自动启动容器。

您只能启动和停止使用 `docker-container` 驱动的构建器。

## AI

在 AI 选项卡中，您可以配置以下设置：

- [Gordon](/manuals/ai/gordon/_index.md)，可针对您的 Docker 工作流执行操作的 AI 驱动助手。
- [Docker Model Runner](/manuals/ai/model-runner/_index.md)，让您可以轻松使用 Docker 管理、运行和部署 AI 模型。

## Kubernetes

> [!NOTE]
>
> 在 Windows 上，**Kubernetes** 选项卡在 Windows 容器模式下不可用。

启用并配置内置的独立 Kubernetes 集群以测试容器部署。

| 设置 | 说明 |
| ------------------- | ----------------------------------------- |
| **Enable Kubernetes** | 安装并运行作为 Docker 容器运行的独立 Kubernetes 服务器，用于测试部署。 |
| **Cluster provisioning method** | 选择 **Kubeadm**（版本由 Docker Desktop 设置的单节点集群）或 **Kind**（可设置版本和节点数的多节点集群）。 |
| **Show system containers (advanced)** | 使用 Docker 命令时显示内部容器。 |
| **Reset Kubernetes cluster** | 删除所有堆栈和 Kubernetes 资源。 |

有关将 Kubernetes 集成与 Docker Desktop 一起使用的更多信息，请参阅 [Explore the Kubernetes view](/manuals/desktop/use-desktop/kubernetes.md)。

## Software updates

管理 Docker Desktop 检查和下载更新的方式和时间。

| 设置 | 说明 | 默认值 |
| ------------------- | ----------------------------------------- | ------------------------------------- |
| **Automatically check for updates** | 在 Docker 菜单和仪表板页脚中通知您可用的更新。 | 开启 |
| **Always download updates** | 在后台自动下载 Docker Desktop 的新版本。 | 关闭 |
| **Automatically update components** | 独立更新 Docker Desktop 的组件（如 Docker Compose、Docker Scout 和 Docker CLI），无需完全重启。 | 开启 |

## Extensions

启用 Docker 扩展并控制哪些扩展可供安装和运行。

| 设置 | 说明 |
| ------------------- | ----------------------------------------- |
| **Enable Docker Extensions** | 打开或关闭 Docker 扩展。默认关闭。 |
| **Allow only extensions distributed through the Docker Marketplace** | 仅限制为 Marketplace 批准的来源提供的扩展。 |
| **Show Docker Extensions system containers** | 显示 Docker 扩展使用的容器。 |

有关 Docker 扩展的更多信息，请参阅 [Docker Extensions](/manuals/extensions/_index.md)。

## Beta features

Beta 功能提供对未来产品功能的访问。
这些功能仅用于测试和反馈，因为它们可能在版本之间更改或完全移除。Beta 功能不得在生产环境中使用。Docker 不为 beta 功能提供支持。

您还可以从 **Beta features** 选项卡注册 [Developer Preview program](https://www.docker.com/community/get-involved/developer-preview/)。

有关 Docker CLI 当前实验功能的列表，请参阅 [Docker CLI Experimental features](https://github.com/docker/cli/blob/master/experimental/README.md)。

## Notifications

选择您想要接收的 Docker Desktop 通知类型。

| 通知类型 | 默认值 |
| ----------------- | ------ |
| Status updates on tasks and processes | 开启 |
| Recommendations from Docker | 开启 |
| Docker announcements | 开启 |
| Docker surveys | 开启 |
| Error notifications | 始终开启（不可更改） |
| New releases | 始终开启（不可更改） |

通知会短暂显示在 Docker Desktop 仪表板的右下角，然后移动到可从仪表板右上角访问的 **Notifications** 抽屉中。

## Advanced (Mac only)

重新配置初始安装期间设置的 CLI 工具安装路径和特权系统权限。

| 设置 | 说明 | 备注 |
| ------------------- | ----------------------------------------- | ------------------------------------- |
| CLI tools installation — **System** | 将 Docker CLI 工具安装到 `/usr/local/bin`。 | |
| CLI tools installation — **User** | 将 Docker CLI 工具安装到 `$HOME/.docker/bin` | 通过将 `export PATH=$PATH:~/.docker/bin` 追加到 `~/.bashrc` 或 `~/.zshrc`，然后将 `$HOME/.docker/bin` 添加到您的 PATH，再重启 shell。 |
| **Allow the default Docker socket to be used** | 创建 `/var/run/docker.sock`，某些第三方客户端可能使用它与 Docker Desktop 通信。更多信息请参阅 [permission requirements for macOS](/manuals/desktop/setup/install/mac-permission-requirements.md#installing-symlinks)。 | 需要密码 |
| **Allow privileged port mapping** | 启动特权辅助进程，绑定 1 到 1024 之间的端口。更多信息请参阅 [permission requirements for macOS](/manuals/desktop/setup/install/mac-permission-requirements.md#binding-privileged-ports)。 | 需要密码 |

## Docker Offload

启用 Docker Offload 并配置基于云的工作负载的空闲超时和 GPU 支持。

| 设置 | 说明 | 备注 |
| ------------------- | ----------------------------------------- | ------------------------------------- |
| **Enable Docker Offload** | 在云中运行您的容器。 | 需要登录和 Offload 订阅 |
| **Idle timeout** | 设置无活动到 Docker Offload 进入空闲模式之间的时长。有关空闲超时的详细信息，请参阅 [Session management and idle state](/manuals/offload/about.md#session-management-and-idle-state)。 | |
| **Enable GPU support** | 让工作负载在可用时使用云 GPU。 | |

