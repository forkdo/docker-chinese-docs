---
description: 了解 Docker for Windows 的使用入门。本文档涵盖系统要求、下载位置，以及安装和更新的详细说明。
keywords: docker for windows, docker windows, docker desktop for windows, docker on
  windows, install docker windows, install docker on windows, docker windows 10, docker
  run on windows, installing docker for windows, windows containers, wsl, hyper-v
title: 在 Windows 上安装 Docker Desktop
linkTitle: Windows
weight: 30
aliases:
- /desktop/windows/install/
- /docker-ee-for-windows/install/
- /docker-for-windows/install-windows-home/
- /docker-for-windows/install/
- /ee/docker-ee/windows/docker-ee/
- /engine/installation/windows/
- /engine/installation/windows/docker-ee/
- /install/windows/docker-ee/
- /install/windows/ee-preview/
- /installation/windows/
- /desktop/win/configuring-wsl/
- /desktop/install/windows-install/
---

> **Docker Desktop 使用条款**
>
> 大型企业（超过 250 名员工或年收入超过 1000 万美元）在商业用途中使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页面提供 Docker Desktop for Windows 的下载链接、系统要求以及详细的安装步骤说明。

{{< button text="Docker Desktop for Windows - x86_64" url="https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-amd64" >}}
{{< button text="Docker Desktop for Windows - x86_64 (Microsoft Store)" url="https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=en-GB&gl=GB" >}}
{{< button text="Docker Desktop for Windows - Arm (早期访问版)" url="https://desktop.docker.com/win/main/arm64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-win-arm64" >}}

_关于校验和，请参阅 [发布说明](/manuals/desktop/release-notes.md)_

## 系统要求

> [!TIP]
>
> **我应该使用 Hyper-V 还是 WSL？**
>
> Docker Desktop 在 WSL 和 Hyper-V 上的功能保持一致，对两种架构没有偏好。Hyper-V 和 WSL 各有优势和劣势，具体取决于您的特定设置和使用场景。

{{< tabs >}}
{{< tab name="WSL 2 后端，x86_64" >}}

- WSL 版本 2.1.5 或更高版本。
- Windows 10 64 位：企业版、专业版或教育版，版本 22H2（构建号 19045）。
- Windows 11 64 位：企业版、专业版或教育版，版本 23H2（构建号 22631）或更高版本。
- 在 Windows 上启用 WSL 2 功能。详细说明请参考[微软文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 以下硬件要求是成功在 Windows 10 或 Windows 11 上运行 WSL 2 所必需的：
  - 支持[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统 RAM
  - 在 BIOS/UEFI 中启用硬件虚拟化。更多信息请参见[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#docker-desktop-fails-due-to-virtualization-not-working)。

有关在 Docker Desktop 中设置 WSL 2 的更多信息，请参阅 [WSL](/manuals/desktop/features/wsl/_index.md)。

> [!NOTE]
>
> Docker 仅支持在仍处于 [Microsoft 服务生命周期](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet) 内的 Windows 版本上运行 Docker Desktop。Docker Desktop 不支持 Windows Server 版本，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 专业版或企业版。
> Windows Home 或 Education 版本仅允许您运行 Linux 容器。

{{< /tab >}}
{{< tab name="Hyper-V 后端，x86_64" >}}

- Windows 10 64 位：企业版、专业版或教育版，版本 22H2（构建号 19045）。
- Windows 11 64 位：企业版、专业版或教育版，版本 23H2（构建号 22631）或更高版本。
- 启用 Hyper-V 和 Containers Windows 功能。
- 以下硬件要求是成功在 Windows 10 上运行 Client Hyper-V 所必需的：
  - 支持[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统 RAM
  - 在 BIOS/UEFI 设置中启用 BIOS/UEFI 级硬件虚拟化支持。更多信息请参见[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!NOTE]
>
> Docker 仅支持在仍处于 [Microsoft 服务生命周期](https://support.microsoft.com/en-us/help/13853/windows-lifecycle-fact-sheet) 内的 Windows 版本上运行 Docker Desktop。Docker Desktop 不支持 Windows Server 版本，如 Windows Server 2019 或 Windows Server 2022。有关如何在 Windows Server 上运行容器的更多信息，请参阅 [Microsoft 官方文档](https://learn.microsoft.com/virtualization/windowscontainers/quick-start/set-up-environment)。

> [!IMPORTANT]
>
> 要运行 Windows 容器，您需要 Windows 10 或 Windows 11 专业版或企业版。
> Windows Home 或 Education 版本仅允许您运行 Linux 容器。

{{< /tab >}}
{{< tab name="WSL 2 后端，Arm（早期访问版）" >}}

- WSL 版本 2.1.5 或更高版本。
- Windows 10 64 位：企业版、专业版或教育版，版本 22H2（构建号 19045）。
- Windows 11 64 位：企业版、专业版或教育版，版本 23H2（构建号 22631）或更高版本。
- 在 Windows 上启用 WSL 2 功能。详细说明请参考[微软文档](https://docs.microsoft.com/en-us/windows/wsl/install-win10)。
- 以下硬件要求是成功在 Windows 10 或 Windows 11 上运行 WSL 2 所必需的：
  - 支持[二级地址转换（SLAT）](https://en.wikipedia.org/wiki/Second_Level_Address_Translation)的 64 位处理器
  - 4GB 系统 RAM
  - 在 BIOS/UEFI 中启用硬件虚拟化。更多信息请参见[虚拟化](/manuals/desktop/troubleshoot-and-support/troubleshoot/topics.md#virtualization)。

> [!IMPORTANT]
>
> Windows 容器不受支持。

{{< /tab >}}
{{< /tabs >}}

Docker Desktop 创建的容器和镜像在安装它的机器上所有用户账户之间共享。这是因为所有 Windows 账户使用同一个虚拟机来构建和运行容器。请注意，当使用 Docker Desktop WSL 2 后端时，无法在用户账户之间共享容器和镜像。

对于 Docker Business 客户，支持在 VMware ESXi 或 Azure 虚拟机内运行 Docker Desktop。这需要首先在虚拟机管理程序上启用嵌套虚拟化。更多信息请参阅 [在虚拟机或 VDI 环境中运行 Docker Desktop](/manuals/desktop/setup/vm-vdi.md)。

{{< accordion title="如何在 Windows 和 Linux 容器之间切换？" >}}

从 Docker Desktop 菜单中，您可以切换 Docker CLI 与哪个守护进程（Linux 或 Windows）通信。选择 **Switch to Windows containers** 使用 Windows 容器，或选择 **Switch to Linux containers** 使用 Linux 容器（默认）。

有关 Windows 容器的更多信息，请参考以下文档：

- Microsoft 关于 [Windows 容器](https://docs.microsoft.com/en-us/virtualization/windowscontainers/about/index) 的文档。

- [构建并运行您的第一个 Windows Server 容器（博客文章）](https://www.docker.com/blog/build-your-first-docker-windows-server-container/)
  快速浏览如何在 Windows 10 和 Windows Server 2016 评估版本上构建和运行原生 Docker Windows 容器。

- [Windows 容器入门（实验）](https://github.com/docker/labs/blob/master/windows/windows-containers/README.md)
  向您展示如何使用 [MusicStore](https://github.com/aspnet/MusicStore/)
  应用程序与 Windows 容器。MusicStore 是一个标准的 .NET 应用程序，[此处分叉以使用容器](https://github.com/friism/MusicStore)，是一个很好的多容器应用程序示例。

- 要了解如何从本地主机连接到 Windows 容器，请参见
  [我想从主机连接到容器](/manuals/desktop/features/networking.md#i-want-to-connect-to-a-container-from-the-host)

> [!NOTE]
>
> 当您切换到 Windows 容器时，**Settings** 仅显示那些活跃且适用于您的 Windows 容器的选项卡。

如果您在 Windows 容器模式下设置了代理或守护进程配置，这些设置仅在 Windows 容器中生效。如果您切换回 Linux 容器，代理和守护进程配置将恢复为您之前为 Linux 容器设置的内容。您的 Windows 容器设置将被保留，并在您再次切换回来时可用。

{{< /accordion >}}

## 管理员权限和安装要求

安装 Docker Desktop 需要管理员权限。但是，安装后，可以无需管理员访问权限使用它。尽管如此，某些操作仍然需要提升的权限。详情请参阅 [了解 Windows 的权限要求](./windows-permission-requirements.md)。

如果您的用户没有管理员权限，并且计划执行需要提升权限的操作，请确保使用 `--always-run-service` 安装程序标志安装 Docker Desktop。这确保这些操作仍然可以执行，而无需提示用户账户控制（UAC）提升。详情请参阅 [安装程序标志](#installer-flags)。

## WSL：验证和设置

如果您选择使用 WSL，首先通过在终端中运行以下命令验证您安装的版本是否满足系统要求：

```console
wsl --version
```

如果未显示版本详细信息，您可能正在使用内置版本的 WSL。此版本不支持现代功能，必须更新。

您可以使用以下方法之一更新或安装 WSL：

### 选项 1：通过终端安装或更新 WSL

1. 以管理员身份打开 PowerShell 或 Windows 命令提示符。
2. 运行安装或更新命令。您可能需要重启计算机。更多信息请参阅 [安装 WSL](https://learn.microsoft.com/en-us/windows/wsl/install)。
```console
wsl --install

wsl --update
```

### 选项 2：通过 MSI 包安装 WSL

如果由于安全策略阻止了 Microsoft Store 访问：
1. 前往官方 [WSL GitHub 发布页面](https://github.com/microsoft/WSL/releases)。
2. 从最新稳定版本（在 Assets 下拉菜单中）下载 `.msi` 安装程序。
3. 运行下载的安装程序并按照设置说明操作。

## 在 Windows 上安装 Docker Desktop

> [!TIP]
>
> 有关如何安装和运行 Docker Desktop 而无需管理员权限的说明，请参阅 [常见问题](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-i-run-docker-desktop-without-administrator-privileges)。

### 交互式安装

1. 使用页面顶部的下载按钮或从 [发布说明](/manuals/desktop/release-notes.md) 下载安装程序。

2. 双击 `Docker Desktop Installer.exe` 运行安装程序。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。

3. 出现提示时，根据您选择的后端，在配置页面上选择或取消选择 **Use WSL 2 instead of Hyper-V** 选项。

    在仅支持一种后端的系统上，Docker Desktop 会自动选择可用的选项。

4. 按照安装向导中的说明授权安装程序并继续安装。

5. 安装成功后，选择 **Close** 完成安装过程。

6. [启动 Docker Desktop](#start-docker-desktop)。

如果您的管理员账户与您的用户账户不同，您必须将用户添加到 **docker-users** 组以访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器：

1. 以 **管理员** 身份运行 **Computer Management**。
2. 导航到 **Local Users and Groups** > **Groups** > **docker-users**。
3. 右键单击将用户添加到该组。
4. 注销并重新登录以使更改生效。

### 从命令行安装

下载 `Docker Desktop Installer.exe` 后，在终端中运行以下命令安装 Docker Desktop：

```console
$ "Docker Desktop Installer.exe" install
```

如果您使用 PowerShell，应将其作为以下方式运行：

```powershell
Start-Process 'Docker Desktop Installer.exe' -Wait install
```

如果使用 Windows 命令提示符：

```sh
start /w "" "Docker Desktop Installer.exe" install
```

默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。

#### 安装程序标志

> [!NOTE]
>
> 如果您使用 PowerShell，需要在任何标志之前使用 `ArgumentList` 参数。
> 例如：
> ```powershell
> Start-Process 'Docker Desktop Installer.exe' -Wait -ArgumentList 'install', '--accept-license'
> ```

如果您的管理员账户与您的用户账户不同，您必须将用户添加到 **docker-users** 组以访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器。

```console
$ net localgroup docker-users <user> /add
```

`install` 命令接受以下标志：

##### 安装行为

- `--quiet`：运行安装程序时抑制信息输出
- `--accept-license`：现在接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不是在首次运行应用程序时要求接受
- `--installation-dir=<path>`：更改默认安装位置（`C:\Program Files\Docker\Docker`）
- `--backend=<backend name>`：选择 Docker Desktop 使用的默认后端，`hyper-v`、`windows` 或 `wsl-2`（默认）
- `--always-run-service`：安装完成后，启动 `com.docker.service` 并将服务启动类型设置为自动。这绕过了对管理员权限的需求，否则启动 `com.docker.service` 是必需的。Windows 容器和 Hyper-V 后端需要 `com.docker.service`。

##### 安全和访问控制

- `--allowed-org=<org name>`：要求用户在运行应用程序时登录并成为指定 Docker Hub 组织的成员
- `--admin-settings`：自动创建 `admin-settings.json` 文件，管理员使用该文件控制其组织内客户端机器上的某些 Docker Desktop 设置。更多信息请参阅 [设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。
  - 必须与 `--allowed-org=<org name>` 标志一起使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"` 
- `--no-windows-containers`：禁用 Windows 容器集成。这可以提高安全性。更多信息请参阅 [Windows 容器](/manuals/desktop/setup/install/windows-permission-requirements.md#windows-containers)。

##### 代理配置

- `--proxy-http-mode=<mode>`：设置 HTTP 代理模式，`system`（默认）或 `manual`
- `--override-proxy-http=<URL>`：设置出站 HTTP 请求必须使用的 HTTP 代理 URL，需要 `--proxy-http-mode` 为 `manual`
- `--override-proxy-https=<URL>`：设置出站 HTTPS 请求必须使用的 HTTP 代理 URL，需要 `--proxy-http-mode` 为 `manual`
- `--override-proxy-exclude=<hosts/domains>`：对主机和域绕过代理设置。使用逗号分隔列表。
- `--proxy-enable-kerberosntlm`：启用 Kerberos 和 NTLM 代理身份验证。如果启用此功能，请确保您的代理服务器正确配置了 Kerberos/NTLM 身份验证。Docker Desktop 4.32 及以后版本提供。
- `--override-proxy-pac=<PAC file URL>`：设置 PAC 文件 URL。仅在使用 `manual` 代理模式时生效。
- `--override-proxy-embedded-pac=<PAC script>`：指定嵌入式 PAC（代理自动配置）脚本。仅在使用 `manual` 代理模式时生效，且优先于 `--override-proxy-pac` 标志。

###### 指定 PAC 文件的示例

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

###### 指定 PAC 脚本的示例

```console
"Docker Desktop Installer.exe" install --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

##### 数据根目录和磁盘