# 在 Windows 上安装 Docker Desktop


> **Docker Desktop 使用条款**
>
> 在大型企业（员工超过 250 人 **或** 年收入超过 1,000 万美元）中商业使用 Docker Desktop 需要 [付费订阅](https://www.docker.com/pricing?ref=Docs&refAction=DocsDesktopWindowsInstall)。

本页面提供 Docker Desktop for Windows 的下载链接、系统要求和逐步安装说明。

[Docker Desktop for Windows - x86_64](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64)

[Docker Desktop for Windows - x86_64 on the Microsoft Store](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB)

[Docker Desktop for Windows - Arm (Early Access)](https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-arm64)


_如需校验和，请参阅[发布说明](/manuals/desktop/release-notes.md)_

## 安装模式

Docker Desktop 支持两种安装模式。按用户安装是大多数用户的推荐选择，并且是安装程序默认选择的模式。它不需要管理员权限即可安装或更新，其使用的 WSL 2 后端可满足绝大多数 Docker Desktop 用户的需求。

| | 按用户（推荐） | 所有用户 |
|---|---|---|
| 安装位置 | `%LOCALAPPDATA%\Programs\DockerDesktop` | `C:\Program Files\Docker\Docker` |
| 注册表项 | 当前用户 (HKCU) | 本地计算机 (HKLM) |
| 安装所需管理员权限 | 不需要 | 需要 |
| 更新所需管理员权限 | 不需要 | 需要 |
| Linux 容器后端 | WSL 2 或 Docker VMM | WSL 2、Hyper-V 或 Docker VMM |
| Windows 容器 | 不支持 | 支持 |
| 安全性 | 攻击面更小；不安装特权系统服务 | 需要特权系统服务；对主机资源的访问范围更广 |

有关更多信息，请参阅 [了解 Windows 的权限要求](windows-install.md)。

## 系统要求

> [!TIP]
>
> **我应该使用哪种后端？**
>
> Docker Desktop for Windows 支持三种后端：WSL 2、Hyper-V 和 Docker VMM（Beta）。WSL 2 是默认后端，可在大多数用户无需管理员权限的情况下工作。Hyper-V 仅在所有用户安装模式下可用。Docker VMM 是一个针对容器优化的虚拟机监控程序，可回收空闲内存并改善文件 I/O。有关更多信息，请参阅 [虚拟机管理器](/manuals/desktop/features/vmm.md)。

**WSL 2 后端，x86_64**



- WSL 版本 2.1.5 或更高版本。要检查您的版本，请参阅[WSL：验证和设置](#wsl-verification-and-setup)
- 如果您打算使用增强容器隔离（ECI），请确保您使用的是 WSL 版本 2.6 或更高版本。这是必需的，因为 ECI 依赖于至少 6.3.0 的 Linux 内核版本，而 WSL 2.6+ 捆绑了 Linux 内核版本 6.6。
- Windows 10 64 位：Enterprise、Pro 或 Education 版本 22H2（构建 19045）。
- Windows 11 64 位：Enterprise、Pro 或 Education 版本 23H2（构建 22631）或更高版本。
- Windows Server 服务（LanmanServer）必须已启用，且其启动模式设置为 **自动**。
- 在 Windows 上启用 WSL 2 功能。有关详细说明，请参阅
  [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 要在 Windows 10 或 Windows 11 上成功运行 WSL 2，需要以下硬件前提条件：
  - 支持[第二层地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 8GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅
    [虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

有关如何在 Docker Desktop 中设置 WSL 2 的更多信息，请参阅 [WSL](/manuals/desktop/features/wsl/_index.md)。

> [!NOTE]
>
> Docker 仅支持在仍处于 [Microsoft 支持时间表](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet) 内的 Windows 版本上运行 Docker Desktop。Docker Desktop 不支持 Windows 的服务器版本，例如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 [Windows 容器](#windows-containers)，您需要 Windows 10 或 Windows 11 Professional 或 Enterprise 版本。
> Windows Home 或 Education 版本只能运行 Linux 容器。

**Hyper-V 后端，x86_64**



- Windows 10 64 位：Enterprise、Pro 或 Education 版本 22H2（构建 19045）。
- Windows 11 64 位：Enterprise、Pro 或 Education 版本 23H2（构建 22631）或更高版本。
- Windows Server 服务（LanmanServer）必须已启用，且其启动模式设置为 **自动**。
- 启用 Hyper-V 和 Containers Windows 功能。
- 要在 Windows 10 上成功运行 Client Hyper-V，需要以下硬件前提条件：

  - 支持[第二层地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 8GB 系统内存
  - 在 BIOS/UEFI 设置中启用 BIOS/UEFI 级硬件虚拟化支持。有关更多信息，请参阅
    [虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!NOTE]
>
> Docker 仅支持在仍处于 [Microsoft 支持时间表](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet) 内的 Windows 版本上运行 Docker Desktop。Docker Desktop 不支持 Windows 的服务器版本，例如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 [Windows 容器](#windows-containers)，您需要 Windows 10 或 Windows 11 Professional 或 Enterprise 版本。
> Windows Home 或 Education 版本只能运行 Linux 容器。

**WSL 2 后端，Arm（早期访问）**



- WSL 版本 2.1.5 或更高版本。要检查您的版本，请参阅[WSL：验证和设置](#wsl-verification-and-setup)
- Windows 10 64 位：Enterprise、Pro 或 Education 版本 22H2（构建 19045）。
- Windows 11 64 位：Enterprise、Pro 或 Education 版本 23H2（构建 22631）或更高版本。
- Windows Server 服务（LanmanServer）必须已启用，且其启动模式设置为 **自动**。
- 在 Windows 上启用 WSL 2 功能。有关详细说明，请参阅
  [Microsoft 文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 要在 Windows 10 或 Windows 11 上成功运行 WSL 2，需要以下硬件前提条件：
  - 支持[第二层地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 8GB 系统内存
  - 在 BIOS/UEFI 中启用硬件虚拟化。有关更多信息，请参阅
    [虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!IMPORTANT]
>
> 不支持 Windows 容器。



在安装了 Docker Desktop 的机器上，使用 Docker Desktop 创建的容器和镜像会在所有用户账户之间共享。这是因为所有 Windows 账户都使用相同的虚拟机来构建和运行容器。请注意，当使用 Docker Desktop WSL 2 后端时，无法在用户账户之间共享容器和镜像。

在 VMware ESXi 或 Azure 虚拟机中运行 Docker Desktop 仅适用于 Docker Business 客户。  
它需要首先在超管理器上启用嵌套虚拟化。  
有关更多信息，请参阅 [在 VM 或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)。

## 在 Windows 上安装 Docker Desktop

### 交互式安装

1. 使用页面顶部的下载按钮或从[发布说明](/manuals/desktop/release-notes.md)下载安装程序。

2. 双击 `Docker Desktop Installer.exe` 运行安装程序。安装程序会询问您偏好的安装模式。选择按用户安装会安装到 `%LOCALAPPDATA%\Programs\DockerDesktop`，且不需要管理员权限。选择所有用户安装会提示提升权限。

   > [!NOTE]
   >
   > 如果您日后想要切换安装模式，需要先卸载再重新安装 Docker Desktop。

3. 根据提示，在“配置”页面上选择您的后端：WSL 2 选择 **使用 WSL 2 而非 Hyper-V**，Hyper-V 则保持不选中。安装后您可以从 **设置** > **常规** 切换到 Docker VMM。

    在仅支持一种后端的系统上，Docker Desktop 会自动选择可用的选项。

4. 按照安装向导中的说明授权安装程序并继续安装。

5. 安装成功后，选择“关闭”以完成安装过程。

6. [启动 Docker Desktop](#start-docker-desktop)。

### 从命令行安装

下载 `Docker Desktop Installer.exe` 后，在终端中运行以下命令，将 Docker Desktop 安装到 `%LOCALAPPDATA%\Programs\DockerDesktop`。

对于按用户安装，运行：

```console
$ "Docker Desktop Installer.exe" install --user
```

要安装在机器上的所有用户（需要管理员权限）：

```console
$ "Docker Desktop Installer.exe" install
```

如果您使用 PowerShell，请运行：

```powershell
# 按用户安装（无需管理员）
Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--user'

# 所有用户安装（以管理员身份运行）
Start-Process 'Docker Desktop Installer.exe' -Wait install
```

如果您使用 Windows 命令提示符：

```sh
# 按用户安装（无需管理员）
start /w "" "Docker Desktop Installer.exe" install --user

# 所有用户安装（以管理员身份运行）
start /w "" "Docker Desktop Installer.exe" install
```

如果使用所有用户安装，且您的管理员账户与用户账户不同，您必须将用户添加到 **docker-users** 组中，以访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机，或使用 Windows 容器：

```console
$ net localgroup docker-users <user> /add
```

> [!WARNING]
>
> `docker-users` 组的成员身份授予对 Docker 守护进程套接字的访问权限，这等同于在主机上授予管理权限。只添加需要访问 Windows 容器或 Hyper-V VM 管理的用户。对于使用 WSL 2 后端的 Linux 容器，不需要该组成员身份。有关更多信息，请参阅 [保护 Docker 守护进程套接字](/manuals/engine/security/protect-access.md)。

如果您通过 MDM（例如 Intune）部署，且 `docker-users` 组未被自动填充，请参阅[为什么通过 Intune 或其他 MDM 解决方案安装 MSI 时未填充 `docker-users` 组？](/manuals/enterprise/enterprise-deployment/faq.md#why-isnt-the-docker-users-group-populated-when-the-msi-is-installed-with-intune-or-another-mdm-solution)。

请参阅[安装程序标志](#installer-flags)部分，了解 `install` 命令接受哪些标志。

> [!NOTE]
>
> 如果您日后想要切换安装模式，需要先卸载再重新安装 Docker Desktop。

## 启动 Docker Desktop

安装后，Docker Desktop 不会自动启动。要启动 Docker Desktop：

1. 搜索 Docker，然后在搜索结果中选择 **Docker Desktop**。

2. Docker 菜单 (


![whale menu](images/whale-x.svg)) 显示 Docker 订阅服务协议。

   
   
   
   
   以下是关键点的总结：
   
   - Docker Desktop 对小企业（员工少于 250 人 AND 年收入低于 1000 万美元）、个人使用、教育用途以及非商业开源项目是免费的。
   - 否则，专业使用需要付费订阅。
   - 政府机构也需要付费订阅。
   - Docker Pro、Team 和 Business 订阅包含 Docker Desktop 的商业使用权限。


3. 选择 **接受** 以继续。接受条款后，Docker Desktop 将启动。

   注意，如果您不同意条款，Docker Desktop 将无法运行。您也可以通过打开 Docker Desktop 在以后接受条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement/)。建议您阅读[常见问题](https://www.docker.com/pricing/faq)。

> [!TIP]
>
> 作为 IT 管理员，您可以使用端点管理（MDM）软件来识别您环境中 Docker Desktop 的实例数和版本。这可以提供准确的许可证报告，帮助确保您的设备使用最新版本的 Docker Desktop，并使您能够[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 高级系统配置和安装选项

### WSL：验证和设置

如果您选择使用 WSL，请首先运行以下命令在终端中验证您的已安装版本是否满足系统要求：

```console
wsl --version
```

如果未显示版本信息，您可能使用的是内置版本的 WSL。此版本不支持现代功能，必须更新。

您可以使用以下任一方法更新或安装 WSL：

#### 选项 1：通过终端安装或更新 WSL

1. 以管理员身份打开 PowerShell 或 Windows 命令提示符。
2. 运行安装或更新命令。系统可能会提示您重新启动计算机。有关更多信息，请参阅[安装 WSL](https://learn.microsoft.com/en-us/windows/wsl/install)。
```console
wsl --install

wsl --update
```

#### 选项 2：通过 MSI 包安装 WSL

如果由于安全策略阻止了 Microsoft Store 访问：
1. 前往官方 [WSL GitHub 发布页面](https://github.com/microsoft/WSL/releases)。
2. 下载最新稳定版本的 `.msi` 安装程序（在“Assets”下拉列表中）。
3. 运行下载的安装程序并按照设置说明操作。

### 安装程序标志

> [!NOTE]
>
> 如果您使用 PowerShell，需要在任何标志前使用 `ArgumentList` 参数。
> 例如：
> ```powershell
> Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'
> ```

#### 安装行为

- `--user`：以按用户模式安装 Docker Desktop，安装到 `%LOCALAPPDATA%\Programs\DockerDesktop`。不需要管理员权限。这是大多数用户的推荐模式。请参阅[安装模式](#installation-modes)。
- `--quiet`: 运行安装程序时抑制信息输出
- `--accept-license`: 立即接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而无需在首次运行应用程序时要求接受
- `--installation-dir=<path>`: 更改默认安装位置（`C:\Program Files\Docker\Docker`）
- `--backend=<backend name>`: 为 Docker Desktop 选择默认后端，`hyper-v`、`windows` 或 `wsl-2`（默认）
- `--always-run-service`: 安装完成后启动 `com.docker.service` 并将服务启动类型设置为自动。这绕过了启动 `com.docker.service` 时通常需要的管理员权限。`com.docker.service` 由 Windows 容器和 Hyper-V 后端所需。

#### 安全和访问控制

- `--allowed-org=<org name>`: 要求用户登录并属于指定的 Docker Hub 组织才能运行应用程序
- `--admin-settings`: 自动创建一个 `admin-settings.json` 文件，用于管理员控制其组织内客户端机器上的某些 Docker Desktop 设置。有关更多信息，请参阅[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。
  - 必须与 `--allowed-org=<org name>` 标志一起使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`
- `--no-windows-containers`: 禁用 Windows 容器集成。这可以提高安全性。有关更多信息，请参阅[Windows 容器](/manuals/desktop/setup/install/windows-permission-requirements.md#windows-containers)。

#### 代理配置

- `--proxy-http-mode=<mode>`: 设置 HTTP 代理模式，`system`（默认）或 `manual`
- `--override-proxy-http=<URL>`: 设置用于出站 HTTP 请求的 HTTP 代理 URL，要求 `--proxy-http-mode` 为 `manual`
- `--override-proxy-https=<URL>`: 设置用于出站 HTTPS 请求的 HTTP 代理 URL，要求 `--proxy-http-mode` 为 `manual`
- `--override-proxy-exclude=<hosts/domains>`: 为指定主机和域名绕过代理设置。使用逗号分隔的列表。
- `--proxy-enable-kerberosntlm`: 启用 Kerberos 和 NTLM 代理身份验证。启用此功能时，请确保您的代理服务器已正确配置 Kerberos/NTLM 身份验证。适用于 Docker Desktop 4.32 及更高版本。
- `--override-proxy-pac=<PAC file URL>`: 设置 PAC 文件 URL。此设置仅在使用 `manual` 代理模式时生效。
- `--override-proxy-embedded-pac=<PAC script>`: 指定嵌入式 PAC（代理自动配置）脚本。此设置仅在使用 `manual` 代理模式时生效，并优先于 `--override-proxy-pac` 标志。

##### 指定 PAC 文件的示例

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

##### 指定 PAC 脚本的示例

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

#### 数据根目录和磁盘位置

- `--hyper-v-default-data-root=<path>`: 指定 Hyper-V 虚拟机磁盘的默认位置。
- `--windows-containers-default-data-root=<path>`: 指定 Windows 容器的默认位置。
- `--wsl-default-data-root=<path>`: 指定 WSL 发行版磁盘的默认位置。

### 管理员权限

在按用户模式下，可以在不需要管理员权限的情况下安装和更新 Docker Desktop。某些设置在设置 UI 中标记为 **需要密码** 并仍需要提升权限。首次启用 WSL 2 也需要管理员权限，但这是一次性的、按计算机的操作。

在所有用户模式下，安装 Docker Desktop 需要管理员权限。但安装后，可以在无需管理员访问权限的情况下使用它。不过，某些操作仍需要提升权限。有关详细信息，请参阅[了解 Windows 的权限要求](./windows-permission-requirements.md)。

请参阅[常见问题](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-i-run-docker-desktop-without-administrator-privileges)，了解如何在不需要管理员权限的情况下安装和运行 Docker Desktop。

如果您是 IT 管理员，用户没有管理员权限，但计划执行需要提升权限的操作，请确保使用 `--always-run-service` 安装程序标志安装 Docker Desktop。这确保在不提示用户账户控制（UAC）提升的情况下仍可执行这些操作。请参阅[安装程序标志](#installer-flags)了解更详细信息。

### Windows 容器

> [!NOTE]
>
> Windows 容器仅在所有用户安装模式下受支持。在按用户安装 Docker Desktop 时不可用。

在 Docker Desktop 菜单中，您可以切换 Docker CLI 与之通信的守护进程（Linux 或 Windows）。选择 **切换到 Windows 容器** 以使用 Windows 容器，或选择 **切换到 Linux 容器** 以使用 Linux 容器（默认）。

有关 Windows 容器的更多信息，请参阅以下文档：

- Microsoft 关于[Windows 容器](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index)的文档。

- [构建并运行您的第一个 Windows Server 容器（博客文章）](https://www.docker.com/blog/build-your-first-docker-windows-server-container/)
  演示了如何在 Windows 10 和 Windows Server 2016 评估版本上构建和运行原生 Docker Windows 容器。

- [Windows 容器入门（实验）](https://github.com/docker/labs/blob/master/windows/windows-containers/README.md)
  展示了如何使用 [MusicStore](https://github.com/aspnet/MusicStore/)
  应用程序与 Windows 容器。MusicStore 是一个标准的 .NET 应用程序，经过 [此处的分支以使用容器](https://github.com/friism/MusicStore)，是多容器应用程序的一个良好示例。

- 要了解如何从本地主机连接到 Windows 容器，请参阅
  [我想从 Windows 连接到容器](/manuals/desktop/features/networking.md#i-want-to-connect-to-a-container-from-the-host)

> [!NOTE]
>
> 切换到 Windows 容器时，**设置**仅显示对您的 Windows 容器活跃且适用的选项卡。

如果您在 Windows 容器模式下设置了代理或守护进程配置，这些设置仅适用于 Windows 容器。如果您切换回 Linux 容器，代理和守护进程配置将恢复为您为 Linux 容器设置的配置。您的 Windows 容器设置将被保留，并在您切换回来时再次可用。

## 接下来该做什么

- 探索 [Docker 订阅](https://www.docker.com/pricing?ref=Docs&refAction=DocsDesktopWindowsInstall)，了解 Docker 为您提供什么。
- [开始使用 Docker](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、变通方案以及如何获得支持。
- [常见问题](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供常见问题的答案。
- [发布说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 发布相关的组件更新、新增功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供关于 Docker 相关数据备份和恢复的说明。

