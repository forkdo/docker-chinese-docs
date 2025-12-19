---
description: 探索 Docker Desktop 的常见故障排除主题
keywords: Linux, Mac, Windows, 故障排除, 主题, Docker Desktop
title: Docker Desktop 故障排除主题
linkTitle: 常见主题
toc_max: 3
tags: [ 故障排除 ]
weight: 10 
aliases:
 - /desktop/troubleshoot/topics/
 - /manuals/desktop/troubleshoot-and-support/troubleshoot/workarounds/
---

> [!TIP]
>
> 如果在故障排除中没有找到解决方案，请浏览 GitHub 仓库或创建新 Issue：
>
> - [docker/for-mac](https://github.com/docker/for-mac/issues)
> - [docker/for-win](https://github.com/docker/for-win/issues)
> - [docker/for-linux](https://github.com/docker/for-linux/issues)

## 所有平台通用主题

### 证书未正确设置

#### 错误信息

当尝试使用 `docker run` 从注册表拉取镜像时，可能会遇到以下错误：

```console
Error response from daemon: Get http://192.168.203.139:5858/v2/: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

此外，注册表的日志可能显示：

```console
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52882: tls: client didn't provide a certificate
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52883: tls: first record does not look like a TLS handshake
```

#### 可能的原因

- Docker Desktop 忽略了在不安全注册表下列出的证书。
- 客户端证书未发送到不安全的注册表，导致握手失败。

#### 解决方案

- 确保您的注册表已使用有效的 SSL 证书正确配置。
- 如果您的注册表是自签名的，请通过将其添加到 Docker 的证书目录（Linux 上为 `/etc/docker/certs.d/`）来配置 Docker 信任该证书。
- 如果问题仍然存在，请检查您的 Docker 守护进程配置并启用 TLS 身份验证。

### Docker Desktop 的界面显示为绿色、失真或有视觉伪影

#### 原因

Docker Desktop 默认使用硬件加速图形，这可能会导致某些 GPU 出现问题。

#### 解决方案

禁用硬件加速：

1. 编辑 Docker Desktop 的 `settings-store.json` 文件（对于 Docker Desktop 4.34 及更早版本，为 `settings.json`）。您可以在以下位置找到此文件：

   - Mac：`~/Library/Group Containers/group.com.docker/settings-store.json`
   - Windows：`C:\Users\[用户名]\AppData\Roaming\Docker\settings-store.json`
   - Linux：`~/.docker/desktop/settings-store.json`

2. 添加以下条目：

   ```JSON
   $ "disableHardwareAcceleration": true
   ```

3. 保存文件并重启 Docker Desktop。

### 使用挂载卷时出现运行时错误，提示找不到应用程序文件、访问卷挂载被拒绝或服务无法启动

#### 原因

如果您的项目目录位于主目录（`/home/<用户>`）之外，Docker Desktop 需要文件共享权限才能访问它。

#### 解决方案

在 Docker Desktop for Mac 和 Linux 中启用文件共享：

1. 导航到 **Settings**（设置），选择 **Resources**（资源），然后选择 **File sharing**（文件共享）。
2. 添加包含 Dockerfile 和卷挂载路径的驱动器或文件夹。

在 Docker Desktop for Windows 中启用文件共享：

1. 从 **Settings**（设置）中，选择 **Shared Folders**（共享文件夹）。
2. 共享包含 Dockerfile 和卷挂载路径的文件夹。

### `port already allocated`（端口已分配）错误

#### 错误信息

启动容器时，可能会看到类似以下的错误：

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

或

```text
listen tcp:0.0.0.0:8080: bind: address is already in use
```

#### 原因

- 系统上的另一个应用程序已在使用指定的端口。
- 之前运行的容器未正常停止，且仍绑定到该端口。

#### 解决方案

要确定此软件的身份，可以：
- 使用 `resmon.exe` GUI，选择 **Network**（网络），然后选择 **Listening Ports**（监听端口）
- 在 PowerShell 中，使用 `netstat -aon | find /i "listening "` 查找当前使用该端口的进程的 PID（PID 是最右侧列中的数字）。

然后，决定是关闭其他进程，还是在您的 Docker 应用程序中使用不同的端口。

## Linux 和 Mac 主题

### Docker Desktop 在 Mac 或 Linux 平台上无法启动

#### 错误信息

由于 Unix 域套接字路径长度限制，Docker 启动失败：

```console
[vpnkit-bridge][F] listen unix <HOME>/Library/Containers/com.docker.docker/Data/http-proxy-control.sock: bind: invalid argument
```

```console
[com.docker.backend][E] listen(vsock:4099) failed: listen unix <HOME>/Library/Containers/com.docker.docker/Data/vms/0/00000002.00001003: bind: invalid argument
```

#### 原因

在 Mac 和 Linux 上，Docker Desktop 创建用于进程间通信的 Unix 域套接字。这些套接字在用户的主目录下创建。

Unix 域套接字有最大路径长度：
 - Mac：104 个字符
 - Linux：108 个字符

如果您的主目录路径太长，Docker Desktop 将无法创建必要的套接字。

#### 解决方案

确保您的用户名足够短，以使路径保持在允许的限制内：
 - Mac：用户名应 ≤ 33 个字符
 - Linux：用户名应 ≤ 55 个字符

## Mac 主题

### 升级需要管理员权限

#### 原因

在 macOS 上，没有管理员权限的用户无法从 Docker Desktop 仪表板执行应用内升级。

#### 解决方案

> [!IMPORTANT]
>
> 升级前请不要卸载当前版本。这样做会删除所有本地 Docker 容器、镜像和卷。

要升级 Docker Desktop：

- 请管理员安装新版本以覆盖现有版本。
- 如果适合您的设置，请使用 [`--user` 安装标志](/manuals/desktop/setup/install/mac-install.md#security-and-access)。

### 持续弹出通知，提示有应用程序更改了我的桌面配置

#### 原因

您会收到此通知，是因为配置完整性检查功能检测到第三方应用程序更改了您的 Docker Desktop 配置。这通常是由于不正确或丢失的符号链接造成的。该通知可确保您知晓这些更改，以便您审查并修复任何潜在问题，从而保持系统可靠性。

打开通知会显示一个弹出窗口，提供有关检测到的完整性问题的详细信息。

#### 解决方案

如果您选择忽略该通知，则只会在下次 Docker Desktop 启动时再次显示。如果您选择修复配置，则不会再收到提示。

如果您想关闭配置完整性检查通知，请导航到 Docker Desktop 的设置，在 **General**（常规）选项卡中，取消选中 **Automatically check configuration**（自动检查配置）设置。

### 退出应用程序后 `com.docker.vmnetd` 仍在运行

特权辅助进程 `com.docker.vmnetd` 由 `launchd` 启动并在后台运行。除非 `Docker.app` 连接到它，否则该进程不会消耗任何资源，因此可以安全地忽略。

### 检测到不兼容的 CPU

#### 原因

Docker Desktop 需要支持虚拟化的处理器（CPU），更具体地说，需要支持 [Apple Hypervisor 框架](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)。

#### 解决方案

检查：
 - 您已为您的架构安装了正确的 Docker Desktop
 - 您的 Mac 支持 Apple 的 Hypervisor 框架。要检查您的 Mac 是否支持 Hypervisor 框架，请在终端窗口中运行以下命令。

   ```console
   $ sysctl kern.hv_support
   ```

   如果您的 Mac 支持 Hypervisor 框架，该命令将打印 `kern.hv_support: 1`。

   如果不支持，该命令将打印 `kern.hv_support: 0`。

另请参阅 Apple 文档中的 [Hypervisor Framework Reference](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)，以及 Docker Desktop 的 [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#system-requirements)。

### VPNKit 不断中断

#### 原因

在 Docker Desktop 4.19 版本中，gVisor 取代了 VPNKit，以在 macOS 13 及更高版本上使用虚拟化框架时增强 VM 网络性能。

#### 解决方案

要继续使用 VPNKit：

1. 打开位于 `~/Library/Group Containers/group.com.docker/settings-store.json` 的 `settings-store.json` 文件
2. 添加：

   ```JSON
   $ "networkType":"vpnkit"
   ```
3. 保存文件并重启 Docker Desktop。

## Windows 主题

### 安装了防病毒软件时 Docker Desktop 启动失败

#### 原因

某些防病毒软件可能与 Hyper-V 和 Microsoft Windows 10 构建版本不兼容。冲突通常在 Windows 更新后发生，并表现为 Docker 守护进程的错误响应以及 Docker Desktop 启动失败。

#### 解决方案

作为临时解决方法，请卸载防病毒软件，或者将 Docker 添加到防病毒软件的排除项/例外列表中。

### 共享卷的数据目录权限错误

#### 原因

从 Windows 共享文件时，Docker Desktop 会将[共享卷](/manuals/desktop/settings-and-maintenance/settings.md#file-sharing)的权限设置为默认值 [0777](https://chmodcommand.com/chmod-0777/)（`user` 和 `group` 的 `读取`、`写入`、`执行` 权限）。

共享卷上的默认权限不可配置。

#### 解决方案

如果您正在处理需要不同权限的应用程序，请：
 - 使用非主机挂载的卷
 - 找到一种方法使应用程序在默认文件权限下工作

### 意外的语法错误，请对容器中的文件使用 Unix 风格的行尾

#### 原因

Docker 容器期望 Unix 风格的行尾 `\n`，而不是 Windows 风格的 `\r\n`。这包括在命令行中为构建引用的文件以及 Docker 文件中的 RUN 命令。

在使用 Windows 工具创建文件（如 shell 脚本）时请记住这一点，因为默认情况下可能是 Windows 风格的行尾。这些命令最终会传递给基于 Unix 的容器内的 Unix 命令（例如，传递给 `/bin/sh` 的 shell 脚本）。如果使用 Windows 风格的行尾，`docker run` 会因语法错误而失败。

#### 解决方案

- 使用以下命令将文件转换为 Unix 风格的行尾：
  
  ```console
  $ dos2unix script.sh
  ```
- 在 VS Code 中，将行尾设置为 `LF`（Unix）而不是 `CRLF`（Windows）。

### Windows 上的路径转换错误

#### 原因

与 Linux 不同，Windows 需要显式路径转换才能挂载卷。

在 Linux 上，系统负责将一个路径挂载到另一个路径。例如，当您在 Linux 上运行以下命令时：

```console
$ docker run --rm -ti -v /home/user/work:/work alpine
```

它会将 `/work` 目录添加到目标容器中以镜像指定的路径。

#### 解决方案

更新源路径。例如，如果您使用的是旧版 Windows shell (`cmd.exe`)，可以使用以下命令：

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
```

这将启动容器并确保卷可用。这是可能的，因为 Docker Desktop 会检测 Windows 风格的路径并提供适当的转换来挂载目录。

Docker Desktop 还允许您使用 Unix 风格的路径转换为适当的格式。例如：

```console
$ docker run --rm -ti -v /c/Users/user/work:/work alpine ls /work
```

### Docker 命令在 Git Bash 中失败

#### 错误信息

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
docker: Error response from daemon: mkdir C:UsersUserwork: Access is denied.
```

```console
$ docker run --rm -ti -v $(pwd):/work alpine
docker: Error response from daemon: OCI runtime create failed: invalid mount {Destination:\Program Files\Git\work Type:bind Source:/run/desktop/mnt/host/c/Users/user/work;C Options:[rbind rprivate]}: mount destination \Program Files\Git\work not absolute: unknown.
```

#### 原因

Git Bash（或 MSYS）在 Windows 上提供类似 Unix 的环境。这些工具对命令行应用自己的预处理。

这会影响 `$(pwd)`、冒号分隔的路径和波浪号 (`~`)。

此外，`\` 字符在 Git Bash 中具有特殊含义。

#### 解决方案

- 临时禁用 Git Bash 路径转换。例如，使用禁用 MSYS 路径转换的方式运行命令：
  ```console
  $ MSYS_NO_PATHCONV=1 docker run --rm -ti -v $(pwd):/work alpine
  ```
- 使用正确的路径格式：
  - 使用双正斜杠和反斜杠 (`\\` `//`) 代替单斜杠 (`\` `/`)。
  - 如果引用 `$(pwd)`，请添加一个额外的 `/`：

脚本的可移植性不受影响，因为 Linux 将多个 `/` 视为单个条目。

### 由于虚拟化不工作而导致 Docker Desktop 失败

#### 错误信息

典型的错误消息是 "Docker Desktop - Unexpected WSL error"，其中提到错误代码 `Wsl/Service/RegisterDistro/CreateVm/HCS/HCS_E_HYPERV_NOT_INSTALLED`。手动执行 `wsl` 命令也会因相同的错误代码而失败。

#### 原因

- BIOS 中的虚拟化设置被禁用。
- Windows Hyper-V 或 WSL 2 组件缺失。

请注意，某些第三方软件（如 Android 模拟器）会在安装时禁用 Hyper-V。

#### 解决方案

您的计算机必须具备以下功能，Docker Desktop 才能正常运行：

##### WSL 2 和 Windows 家庭版

1. 虚拟机平台
2. [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
   请注意，许多 Windows 设备已启用虚拟化，因此这可能不适用。
4. 在 Windows 启动时启用 Hypervisor

![WSL 2 已启用](../../images/wsl2-enabled.png)

必须能够无错误地运行 WSL 2 命令，例如：

```console
PS C:\users\> wsl -l -v
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Stopped         2
PS C:\users\> wsl -d docker-desktop echo WSL 2 is working
WSL 2 is working
```

如果功能已启用但命令不起作用，请首先检查 [虚拟化已开启](#virtualization-must-be-turned-on)，然后如果需要，[在 Windows 启动时启用 Hypervisor](#hypervisor-enabled-at-windows-startup)。如果在虚拟机中运行 Docker Desktop，请确保 [虚拟机管理程序已启用嵌套虚拟化](#turn-on-nested-virtualization)。

##### Hyper-V

在 Windows 10 专业版或企业版上，您也可以使用 Hyper-V，但需要启用以下功能：

1. [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview) 已安装并正常工作
2. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
   请注意，许多 Windows 设备已启用虚拟化，因此这可能不适用。
3. 在 Windows 启动时启用 Hypervisor

![Windows 功能中的 Hyper-V](../../images/hyperv-enabled.png)

Docker Desktop 需要 Hyper-V 以及 Windows PowerShell 的 Hyper-V 模块已安装并启用。Docker Desktop 安装程序会为您启用它。

Docker Desktop 还需要两个 CPU 硬件功能才能使用 Hyper-V：虚拟化和二级地址转换 (SLAT)，也称为快速虚拟化索引 (RVI)。在某些系统上，必须在 BIOS 中启用虚拟化。所需的步骤因供应商而异，但通常 BIOS 选项称为 `Virtualization Technology (VTx)` 或类似名称。运行命令 `systeminfo` 以检查所有必需的 Hyper-V 功能。有关更多详细信息，请参阅 [Windows 10 上 Hyper-V 的先决条件](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)。

要手动安装 Hyper-V，请参阅 [在 Windows 10 上安装 Hyper-V](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/quick_start/walkthrough_install)。安装后*需要*重新启动。如果您安装 Hyper-V 而不重新启动，Docker Desktop 将无法正常工作。

从开始菜单，键入 **打开或关闭 Windows 功能** 并按 Enter。
在随后的屏幕中，验证 Hyper-V 是否已启用。

##### 虚拟化必须开启

除了 [Hyper-V](#hyper-v) 或 [WSL 2](/manuals/desktop/features/wsl/_index.md) 之外，还必须开启虚拟化。检查任务管理器的“性能”选项卡。或者，您可以在终端中键入 `systeminfo`。如果您看到 `Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed`，则表示虚拟化已启用。

![任务管理器](../../images/virtualization-enabled.png)

如果您手动卸载 Hyper-V、WSL 2 或关闭虚拟化，Docker Desktop 将无法启动。

要开启嵌套虚拟化，请参阅 [在 VM 或 VDI 环境中运行 Docker Desktop for Windows](/manuals/desktop/setup/vm-vdi.md#turn-on-nested-virtualization)。

##### 在 Windows 启动时启用 Hypervisor

如果您已完成前面的步骤，但仍然遇到 Docker Desktop 启动问题，这可能是因为 Hypervisor 已安装，但在 Windows 启动期间未启动。某些工具（如旧版本的 Virtual Box）和视频游戏安装程序会在启动时关闭 hypervisor。要重新打开它：

1. 打开管理控制台提示符。
2. 运行 `bcdedit /set hypervisorlaunchtype auto`。
3. 重新启动 Windows。

您也可以参考 Microsoft TechNet 关于代码流保护 (CFG) 设置的[文章](https://social.technet.microsoft.com/Forums/en-US/ee5b1d6b-09e2-49f3-a52c-820aafc316f9/hyperv-doesnt-work-after-upgrade-to-windows-10-1809?forum=win10itprovirt)。

##### 开启嵌套虚拟化

如果您正在使用 Hyper-V，并且在 VDI 环境中运行 Docker Desktop 时出现以下错误消息：

```console
The Virtual Machine Management Service failed to start the virtual machine 'DockerDesktopVM' because one of the Hyper-V components is not running
```

请尝试[启用嵌套虚拟化](/manuals/desktop/setup/vm-vdi.md#turn-on-nested-virtualization)。

### 使用 Windows 容器的 Docker Desktop 出现 "The media is write protected" 错误

#### 错误信息

`FSCTL_EXTEND_VOLUME \\?\Volume{GUID}: The media is write protected`

#### 原因

如果您在使用 Windows 容器运行 Docker Desktop 时遇到故障，可能是由于特定的 Windows 配置策略：FDVDenyWriteAccess。

此策略启用后，会导致 Windows 将所有未通过 BitLocker 加密的固定驱动器挂载为只读。这也会影响虚拟机卷，因此 Docker Desktop 可能无法启动或正确运行容器，因为它需要对这些卷具有读写访问权限。

FDVDenyWriteAccess 是一个 Windows 组策略设置，启用后会阻止对未受 BitLocker 保护的固定数据驱动器的写入访问。这通常用于安全意识强的环境中，但可能会干扰 Docker 等开发工具。在 Windows 注册表中，它位于 `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Policies\Microsoft\FVE\FDVDenyWriteAccess`。

#### 解决方案

Docker Desktop 不支持在 FDVDenyWriteAccess 已启用的系统上运行 Windows 容器。此设置会干扰 Docker 正确挂载卷的能力，而这对容器功能至关重要。

要将 Docker Desktop 与 Windows 容器一起使用，请确保 FDVDenyWriteAccess 已禁用。您可以通过注册表或组策略编辑器 (`gpedit.msc`) 检查和更改此设置，路径为：

**计算机配置** > **管理模板** > **Windows 组件** > **BitLocker 驱动器加密** > **固定数据驱动器** > **拒绝写入未受 BitLocker 保护的固定驱动器**

> [!NOTE]
>
> 修改组策略设置可能需要管理员权限，并且应遵守您组织的 IT 策略。如果设置在一段时间后重置，这通常意味着它被您 IT 部门的集中配置覆盖了。在进行任何更改之前，请与他们沟通。

### 启动 Docker Desktop 时出现 `Docker Desktop Access Denied` 错误消息

#### 错误信息

启动 Docker Desktop 时，出现以下错误：

```text
Docker Desktop - Access Denied
```

#### 原因

用户不属于 `docker-users` 组，这是权限所必需的。

#### 解决方案

如果您的管理员帐户与您的用户帐户不同，请将其添加：

1. 以管理员身份运行 **计算机管理**。
2. 导航到 **本地用户和组** > **组** > **docker-users**。
3. 右键单击以将用户添加到组中。
4. 注销并重新登录以使更改生效。