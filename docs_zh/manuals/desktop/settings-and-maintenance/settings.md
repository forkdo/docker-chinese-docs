---
description: 了解并更改 Docker Desktop 的设置
keywords: settings, preferences, proxy, file sharing, resources, kubernetes, Docker
  Desktop, Linux, Mac, Windows
title: 更改 Docker Desktop 设置
linkTitle: 更改设置
aliases:
 - /desktop/settings/mac/
 - /desktop/settings/windows/
 - /desktop/settings/linux/
 - /desktop/settings/
weight: 10
---

要导航到 **Settings**，有两种方式：

- 选择 Docker 菜单 {{< inline-image src="../images/whale-x.svg" alt="whale menu" >}}，然后选择 **Settings**
- 从 Docker Desktop 仪表板中选择 **Settings** 图标。

您也可以找到 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`）：
 - Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
 - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
 - Linux: `~/.docker/desktop/settings-store.json`

有关 Docker Desktop Dashboard 和管理员通过 Admin Console 可设置的更多设置信息，请参阅 [Settings reference](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md)。

## General

在 **General** 选项卡中，您可以配置 Docker 启动时间和其他设置：

- **Start Docker Desktop when you sign in to your computer**。选择此项可在您登录计算机时自动启动 Docker Desktop。

- **Open Docker Dashboard when Docker Desktop starts**。选择此项可在启动 Docker Desktop 时自动打开仪表板。

- **Choose theme for Docker Desktop**。选择要为 Docker Desktop 应用 **Light** 或 **Dark** 主题，或者设置为 **Use system settings**。

- **Configure shell completions**。自动编辑您的 shell 配置，在终端中按 `<Tab>` 键时为命令、标志和 Docker 对象（如容器和卷名）提供自动补全功能。更多信息请参阅 [Completion](/manuals/engine/cli/completion.md)。

- **Choose container terminal**。确定从容器中打开终端时启动哪个终端。
如果您选择集成终端，可以直接从 Docker Desktop Dashboard 在运行中的容器中执行命令。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md)。

- **Enable Docker terminal**。直接从 Docker Desktop 与主机交互并执行命令。

- **Enable Docker Debug by default**。选中此项后，在访问集成终端时默认使用 Docker Debug。更多信息请参阅 [Explore containers](/manuals/desktop/use-desktop/container.md#integrated-terminal)。

- {{< badge color=blue text="Mac only" >}}**Include VM in Time Machine backups**。选择此项可备份 Docker Desktop 虚拟机。默认情况下此选项关闭。

- **Use containerd for pulling and storing images**。启用 containerd 镜像存储。这带来了新功能，如通过延迟拉取镜像提高容器启动性能，以及使用 Docker 运行 Wasm 应用的能力。更多信息请参阅 [containerd image store](/manuals/desktop/features/containerd.md)。

- {{< badge color=blue text="Windows only" >}}**Expose daemon on tcp://localhost:2375 without TLS**。选中此项可启用旧版客户端连接 Docker 守护进程。必须谨慎使用此选项，因为不使用 TLS 暴露守护进程可能导致远程代码执行攻击。

- {{< badge color=blue text="Windows only" >}}**Use the WSL 2 based engine**。WSL 2 提供比 Hyper-V 后端更好的性能。更多信息请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。

- {{< badge color=blue text="Windows only" >}}**Add the `*.docker.internal` names to the host's `/etc/hosts` file (Password required)**。允许您从主机和容器中解析 `*.docker.internal` DNS 名称。

- {{< badge color=blue text="Mac only" >}} **Choose Virtual Machine Manager (VMM)**。选择用于创建和管理 Docker Desktop Linux VM 的虚拟机管理器。
  - 选择 **Docker VMM** 以获得最新且性能最佳的 Hypervisor/虚拟机管理器。此选项仅在运行 macOS 12.5 或更高版本的 Apple Silicon Mac 上可用，目前处于 Beta 阶段。
    > [!TIP]
    >
    > 开启此设置可使 Docker Desktop 运行更快。
  - 或者，您可以选择 **Apple Virtualization framework**、**QEMU**（Docker Desktop 4.43 及更早版本的 Apple Silicon）或 **HyperKit**（Intel Mac）。对于 macOS 12.5 及更高版本，Apple Virtualization framework 是默认设置。

   更多信息请参阅 [Virtual Machine Manager](/manuals/desktop/features/vmm.md)。

- {{< badge color=blue text="Mac only" >}}**Choose file sharing implementation for your containers**。选择是否要使用 **VirtioFS**、**gRPC FUSE** 或 **osxfs (Legacy)** 来共享文件。VirtioFS 仅在 macOS 12.5 及更高版本上可用，默认启用。
    > [!TIP]
    >
    > 使用 VirtioFS 实现快速文件共享。VirtioFS 将文件系统操作完成时间减少了 [多达 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206)。它是 Docker VMM 支持的唯一文件共享实现。

- {{< badge color=blue text="Mac only" >}}**Use Rosetta for x86_64/amd64 emulation on Apple Silicon**。在 Apple Silicon 上启用 Rosetta 以加速 x86/AMD64 二进制仿真。只有当您选择 **Apple Virtualization framework** 作为虚拟机管理器且运行 macOS 13 或更高版本时，此选项才可用。

- **Send usage statistics**。选择此项可让 Docker Desktop 发送诊断信息、崩溃报告和使用数据。这些信息有助于 Docker 改进和排查应用程序问题。清除复选框可选择退出。Docker 可能会定期提示您提供更多信息。

- **Use Enhanced Container Isolation**。选择此项可通过防止容器突破 Linux VM 来增强安全性。更多信息请参阅 [Enhanced Container Isolation](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)。
    > [!NOTE]
    >
    > 只有登录 Docker Desktop 并拥有 Docker Business 订阅时，此设置才可用。

- **Show CLI hints**。在 CLI 中运行 Docker 命令时显示 CLI 提示和技巧。默认启用。要从 CLI 开启或关闭 CLI 提示，分别将 `DOCKER_CLI_HINTS` 设置为 `true` 或 `false`。

- **Enable Scout image analysis**。启用此选项后，在 Docker Desktop 中检查镜像时会显示 **Start analysis** 按钮，选择后会使用 Docker Scout 分析镜像。

- **Enable background SBOM indexing**。启用此选项后，Docker Scout 会自动分析您构建或拉取的镜像。

- {{< badge color=blue text="Mac only" >}}**Automatically check configuration**。定期检查您的配置以确保其他应用程序未对其进行意外更改。

  Docker Desktop 会检查安装期间配置的设置是否被外部应用程序（如 Orbstack）更改。Docker Desktop 检查：
    - Docker 二进制文件到 `/usr/local/bin` 的符号链接。
    - 默认 Docker 套接字的符号链接。
  此外，Docker Desktop 确保在启动时上下文切换到 `desktop-linux`。
  
  如果发现更改，您会收到通知，并可以直接从通知中恢复配置。更多信息请参阅 [FAQs](/manuals/desktop/troubleshoot-and-support/faqs/macfaqs.md#why-do-i-keep-getting-a-notification-telling-me-an-application-has-changed-my-desktop-configurations)。

## Resources

**Resources** 选项卡允许您配置 CPU、内存、磁盘、代理、网络和其他资源。

### Advanced

> [!NOTE]
>
> 在 Windows 上，**Advanced** 选项卡中的 **Resource allocation** 选项仅在 Hyper-V 模式下可用，因为 Windows 在 WSL 2 模式和 Windows 容器模式下管理资源。在 WSL 2 模式下，您可以在 [WSL 2 utility VM](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig) 中配置分配给 WSL 2 实用程序 VM 的内存、CPU 和交换大小限制。

在 **Advanced** 选项卡中，您可以限制 Docker Linux VM 可用的资源。

高级设置包括：

- **CPU limit**。指定 Docker Desktop 可使用的最大 CPU 数。默认情况下，Docker Desktop 设置为使用主机上所有可用的处理器。

- **Memory limit**。默认情况下，Docker Desktop 设置为使用主机最多 50% 的内存。要增加 RAM，请将此值设置为更高的数字；要减少它，请降低该数字。

- **Swap**。根据需要配置交换文件大小。默认值为 1 GB。

- **Disk usage limit**。指定引擎可使用的最大磁盘空间量。

- **Disk image location**。指定存储容器和镜像的 Linux 卷的位置。

  您还可以将磁盘映像移动到不同位置。如果您尝试将磁盘映像移动到已有映像的位置，系统会询问您是否要使用现有映像或替换它。

>[!TIP]
>
> 如果您感觉 Docker Desktop 开始变慢或运行多容器工作负载，请增加内存和磁盘映像空间分配。

- **Resource Saver**。启用或禁用 [Resource Saver mode](/manuals/desktop/use-desktop/resource-saver.md)，通过在 Docker Desktop 空闲时（即没有容器运行时）自动关闭 Linux VM 来显著减少主机的 CPU 和内存使用。

  您还可以配置 Resource Saver 超时，指示 Docker Desktop 空闲多长时间后 Resource Saver 模式启动。默认为 5 分钟。

  > [!NOTE]
  >
  > 退出 Resource Saver 模式会在容器运行时自动发生。退出可能需要几秒钟（约 3 到 10 秒），因为 Docker Desktop 会重新启动 Linux VM。

### File sharing

> [!NOTE]
>
> 在 Windows 上，**File sharing** 选项卡仅在 Hyper-V 模式下可用，因为文件在 WSL 2 模式和 Windows 容器模式下会自动共享。

使用文件共享允许您机器上的本地目录与 Linux 容器共享。这对于在主机上的 IDE 中编辑源代码同时在容器中运行和测试代码特别有用。

#### Synchronized file shares 

同步文件共享是一种替代的文件共享机制，通过使用同步的文件系统缓存提供快速灵活的主机到 VM 文件共享，增强绑定挂载性能。Pro、Team 和 Business 订阅提供。

要了解更多信息，请参阅 [Synchronized file share](/manuals/desktop/features/synchronized-file-sharing.md)。

#### Virtual file shares

默认情况下，`/Users`、`/Volumes`、`/private`、`/tmp` 和 `/var/folders` 目录被共享。
如果您的项目在此目录之外，则必须将其添加到列表中，否则您可能在运行时遇到 `Mounts denied` 或 `cannot start service` 错误。

文件共享设置包括：

- **Add a Directory**。选择 `+` 并导航到要添加的目录。

- **Remove a Directory**。选择要删除的目录旁边的 `-`。

- **Apply** 使用 Docker 的绑定挂载 (`-v`) 功能使目录对容器可用。

> [!TIP]
>
> * 只共享您需要与容器共享的目录。文件共享会引入开销，因为主机上文件的任何更改都需要通知 Linux VM。共享过多文件会导致高 CPU 负载和文件系统性能变慢。
> * 共享文件夹设计用于允许应用程序代码在主机上编辑，同时在容器中执行。对于缓存目录或数据库等非代码项，如果它们存储在 Linux VM 中，使用 [data volume](/manuals/engine/storage/volumes.md)（命名卷）或 [data container](/manuals/engine/storage/volumes.md) 性能会好得多。
> * 如果您将整个主目录共享到容器中，macOS 可能会提示您授予 Docker 访问主目录中个人区域（如提醒事项或下载）的权限。
> * 默认情况下，Mac 文件系统不区分大小写，而 Linux 区分大小写。在 Linux 上，可以创建两个独立的文件：`test` 和 `Test`，而在 Mac 上这些文件名实际上指的是同一个基础文件。这可能导致应用程序在开发人员机器上工作正常（文件内容被共享），但在 Linux 生产环境中运行时失败（文件内容不同）。为避免这种情况，Docker Desktop 坚持所有共享文件必须以其原始大小写访问。因此，如果创建了一个名为 `test` 的文件，它必须以 `test` 打开。尝试打开 `Test` 将失败，错误为 "No such file or directory"。同样，一旦创建了名为 `test` 的文件，尝试创建名为 `Test` 的第二个文件将失败。
>
> 有关更多信息，请参阅 [Volume mounting requires file sharing for any project directories outside of `/Users`](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md)

#### Shared folders on demand

在 Windows 上，您可以在容器首次使用特定文件夹时按需共享该文件夹。

如果您从带有卷挂载的 shell 运行 Docker 命令（如下例所示）或启动包含卷挂载的 Compose 文件，您会收到一个弹窗，询问您是否要共享指定的文件夹。

您可以选择 **Share it**，在这种情况下它会被添加到您的 Docker Desktop 共享文件夹列表中并可供容器使用。或者，您可以通过选择 **Cancel** 选择不共享它。

![Shared folder on demand](../images/shared-folder-on-demand.png)

### Proxies

Docker Desktop 支持使用 HTTP/HTTPS 和 SOCKS5 代理（需要商业订阅）。

HTTP/HTTPS 和 SOCKS5 代理可用于：

- 登录 Docker
- 拉取或推送镜像
- 镜像构建期间获取工件
- 容器与外部网络交互
- 扫描镜像

有关工作原理的更多详细信息，请参阅 [Using Docker Desktop with a proxy](/manuals/desktop/features/networking/index.md#useing-docker-desktop-with-a-proxy)。

如果主机使用 HTTP/HTTPS 代理配置（静态或通过代理自动配置 (PAC)），Docker Desktop 会读取此配置并自动使用这些设置进行登录 Docker、拉取和推送镜像，以及容器的 Internet 访问。如果代理需要授权，Docker Desktop 会动态询问开发人员用户名和密码。所有密码都安全存储在操作系统凭据存储中。请注意，仅支持 `Basic` 代理身份验证方法，因此我们建议对 HTTP/HTTPS 代理使用 `https://` URL 以在传输过程中保护密码。Docker Desktop 在与代理通信时支持 TLS 1.3。

要为 Docker Desktop 设置不同的代理，请打开 **Manual proxy configuration** 并输入单个上游代理 URL，格式为 `http://proxy:port` 或 `https://proxy:port`。

要防止开发人员意外更改代理设置，请参阅 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md#what-features-can-i-configure-with-settings-management)。

用于扫描镜像的 HTTPS 代理设置使用 `HTTPS_PROXY` 环境变量设置。

> [!NOTE]
>
> 如果您使用托管在 Web 服务器上的 PAC 文件，请确保在服务器或网站上为 `.pac` 文件扩展名添加 MIME 类型 `application/x-ns-proxy-autoconfig`。没有此配置，PAC 文件可能无法正确解析。有关 PAC 文件和 Docker Desktop 的更多详细信息，请参阅 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/air-gapped-containers.md#proxy-auto-configuration-files)

> [!IMPORTANT]
> 您不能使用 Docker 守护进程配置文件 (`daemon.json`) 配置代理设置，我们建议您不要通过 Docker CLI 配置文件 (`config.json`) 配置代理设置。
>
> 要管理 Docker Desktop 的代理配置，请在 Docker Desktop 应用中配置设置或使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。

#### Proxy authentication

##### Basic authentication

如果您的代理使用基本身份验证，Docker Desktop 会提示开发人员输入用户名和密码并缓存凭据。所有密码都安全存储在操作系统凭据存储中。如果缓存被删除，它会请求重新身份验证。

建议您对 HTTP/HTTPS 代理使用 `https://` URL 以在传输过程中保护密码。Docker Desktop 还支持与代理通信时的 TLS 1.3。

##### Kerberos and NTLM authentication

> [!NOTE]
>
> 适用于 Docker Business 订阅用户，Docker Desktop for Windows 版本 4.30 及更高版本。

开发人员不再会被代理凭据提示中断，因为身份验证是集中的。这也减少了由于错误登录尝试导致账户锁定的风险。

如果您的代理在 407（需要代理身份验证）响应中提供多种身份验证方案，Docker Desktop 默认选择基本身份验证方案。

对于 Docker Desktop 版本 4.30 到 4.31：

要启用 Kerberos 或 NTLM 代理身份验证，除了指定代理 IP 地址和端口外，不需要额外的配置。

对于 Docker Desktop 版本 4.32 及更高版本：

要启用 Kerberos 或 NTLM 代理身份验证，您必须在通过命令行安装期间传递 `--proxy-enable-kerberosntlm` 安装程序标志，并确保您的代理服务器正确配置了 Kerberos 或 NTLM 身份验证。

### Network

> [!NOTE]
>
> 在 Windows 上，**Network** 选项卡在 Windows 容器模式下不可用，因为 Windows 管理网络。

Docker Desktop 使用私有 IPv4 网络用于内部服务，如 DNS 服务器和 HTTP 代理。如果 Docker Desktop 的子网选择与您环境中的 IP 冲突，您可以使用 **Network** 设置指定自定义子网。

在 Windows 和 Mac 上，您还可以设置默认网络模式和 DNS 解析行为。更多信息请参阅 [Networking](/manuals/desktop/features/networking.md#networking-mode-and-dns-behaviour-for-mac-and-windows)。

在 Mac 上，您还可以选择 **Use kernel networking for UDP** 设置。这允许您对 UDP 使用更高效的内核网络路径。这可能与您的 VPN 软件不兼容。

您还可以定义端口绑定的行为。默认情况下，Docker Desktop 将容器上的所有端口绑定到主机上的 `0.0.0.0`，尽管这可以通过提供特定 IP 来覆盖。您可以通过更改 **Port binding behavior** 设置来更改此默认行为，允许您默认绑定到 `localhost` (`127.0.0.1`)，或者在任何情况下只允许容器绑定到 `localhost`，即使请求其他方式也是如此。

### WSL Integration

在 Windows 的 WSL 2 模式下，您可以配置哪些 WSL 2 发行版将具有 Docker WSL 集成功能。

默认情况下，集成在您的默认 WSL 发行版上启用。
要更改您的默认 WSL 发行版，请运行 `wsl --set-default <distribution name>`。（例如，要将 Ubuntu 设置为您的默认 WSL 发行版，请运行 `wsl --set-default ubuntu`）。

您还可以选择要启用 WSL 2 集成的任何其他发行版。

有关配置 Docker Desktop 使用 WSL 2 的更多详细信息，请参阅 [Docker Desktop WSL 2 backend](/manuals/desktop/features/wsl/_index.md)。

## Docker Engine

**Docker Engine** 选项卡允许您配置用于运行容器的 Docker 守护进程。

您使用 JSON 配置文件配置守护进程。配置文件可能如下所示：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false
}
```

您可以在 `$HOME/.docker/daemon.json` 找到此文件。要更改配置，可以直接从 Docker Desktop 仪表板编辑 JSON 配置，或使用您最喜欢的文本编辑器打开并编辑该文件。

要查看可能的配置选项的完整列表，请参阅 [dockerd 命令参考](/reference/cli/dockerd/)。

选择 **Apply** 保存您的设置。

## Builders

如果您已启用 [Docker Desktop Builds 视图](/manuals/desktop/use-desktop/builds.md)，可以使用 **Builders** 选项卡在 Docker Desktop 设置中检查和管理构建器。

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

## Kubernetes

> [!NOTE]
>
> 在 Windows 上，**Kubernetes** 选项卡在 Windows 容器模式下不可用。

Docker Desktop 包含一个独立的 Kubernetes 服务器，因此您可以测试在 Kubernetes 上部署 Docker 工作负载。要启用 Kubernetes 支持并安装作为 Docker 容器运行的独立 Kubernetes 实例，请选择 **Enable Kubernetes**。这也可以从 **Kubernetes** 视图中完成。

您可以选择集群配置方法：
 - **Kubeadm** 创建单节点集群，版本由 Docker Desktop 设置。
 - **kind** 创建多节点集群，您可以设置版本和节点数。

选择 **Show system containers (advanced)** 在使用 Docker 命令时查看内部容器。

选择 **Reset Kubernetes cluster** 删除所有堆栈和 Kubernetes 资源。

有关将 Kubernetes 集成与 Docker Desktop 一起使用的更多信息，请参阅 [Explore the Kubernetes view](/manuals/desktop/use-desktop/kubernetes.md)。

## Software updates

**Software updates** 选项卡允许您管理 Docker Desktop 更新。
当有新更新时，您可以选择立即下载更新，或选择 **Release Notes** 选项了解更新版本包含的内容。

**Automatically check for updates** 设置会在 Docker 菜单和 Docker Desktop Dashboard 页脚中通知您 Docker Desktop 的任何可用更新。默认情况下此设置已开启。

要允许 Docker Desktop 在后台自动下载新更新，请选择 **Always download updates**。这会在有更新可用时下载 Docker Desktop 的较新版本。下载更新后，选择 **Apply and restart** 安装更新。您可以通过 Docker 菜单或 Docker Desktop Dashboard 的 **Updates** 部分执行此操作。

**Automatically update components** 设置检查 Docker Desktop 的组件（如 Docker Compose、Docker Scout 和 Docker CLI）是否可以独立更新，而无需完全重启。默认情况下此设置已开启。

## Extensions

使用 **Extensions** 选项卡可以：

- **Enable Docker Extensions**
- **Allow only extensions distributed through the Docker Marketplace**
- **Show Docker Extensions system containers**

有关 Docker 扩展的更多信息，请参阅 [Extensions](/manuals/extensions/_index.md)。

## Beta features

Beta 功能提供对未来产品功能的访问。
这些功能仅用于测试和反馈，因为它们可能在版本之间更改或完全移除。Beta 功能不得在生产环境中使用。Docker 不为 beta 功能提供支持。

您还可以从 **Beta features** 选项卡注册 [Developer Preview program](https://www.docker.com/community/get-involved/developer-preview/)。

有关 Docker CLI 当前实验功能的列表，请参阅 [Docker CLI Experimental features](https://github.com/docker/cli/blob/master/experimental/README.md)。

> [!IMPORTANT]
>
> 对于 Docker Desktop 4.41 及更早版本，**Features in development** 页面下还有一个 **Experimental features** 选项卡。
>
> 与 beta 功能一样，实验功能不得在生产环境中使用。Docker 不为实验功能提供支持。

## Notifications

使用 **Notifications** 选项卡打开或关闭以下事件的通知：

- **Status updates on tasks and processes**
- **Recommendations from Docker**
- **Docker announcements**
- **Docker surveys**

默认情况下，所有常规通知都已打开。您将始终收到错误通知和有关新 Docker Desktop 发布和更新的通知。

您还可以 [配置 Docker Scout 相关问题的通知设置](/manuals/scout/explore/dashboard.md#notification-settings)。

通知会短暂显示在 Docker Desktop Dashboard 的右下角，然后移动到可从 Docker Desktop Dashboard 右上角访问的 **Notifications** 抽屉中。

## Advanced

在 Mac 上，您可以在 **Advanced** 选项卡上重新配置初始安装设置：

- **Choose how to configure the installation of Docker's CLI tools**。
  - **System**: Docker CLI 工具安装在 `/usr/local/bin` 下的系统目录中
  - **User**: Docker CLI 工具安装在 `$HOME/.docker/bin` 下的用户目录中。然后您必须将 `$HOME/.docker/bin` 添加到您的 PATH 中。要将 `$HOME/.docker/bin` 添加到您的路径中：
      1. 打开您的 shell 配置文件。如果您使用的是 bash shell，则为 `~/.bashrc`，如果您使用的是 zsh shell，则为 `~/.zshrc`。
      2. 复制并粘贴以下内容：
            ```console
            $ export PATH=$PATH:~/.docker/bin
            ```
     3. 保存并关闭文件。重启您的 shell 以应用 PATH 变量的更改。

- **Allow the default Docker socket to be used (Requires password)**。创建 `/var/run/docker.sock`，某些第三方客户端可能使用它与 Docker Desktop 通信。更多信息请参阅 [macOS 的权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#installing-symlinks)。

- **Allow privileged port mapping (Requires password)**。启动特权辅助进程，绑定 1 到 1024 之间的端口。更多信息请参阅 [macOS 的权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#binding-privileged-ports)。

有关每个配置和用例的更多信息，请参阅 [Permission requirements](/manuals/desktop/setup/install/mac-permission-requirements.md)。

## Docker Offload

使用具有 [Docker Offload](../../offload/_index.md) 访问权限的 Docker 账户登录时，您可以从 **Docker Offload** 选项卡管理您的 Offload 设置。

使用 **Docker Offload** 选项卡可以：

- 切换 **Enable Docker Offload**。启用后，您可以启动 Offload 会话。
- 选择 **Idle timeout**。这是 Docker Offload 进入空闲模式之前无活动的时间段。有关空闲超时的详细信息，请参阅 [Active and idle states](../../offload/configuration.md#understand-active-and-idle-states)
- 检查 **Enable GPU support**。启用后，工作负载可以使用云 GPU（如果可用）。