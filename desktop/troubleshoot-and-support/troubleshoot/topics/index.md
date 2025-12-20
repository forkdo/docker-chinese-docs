# Docker Desktop 故障排除主题
> [!TIP]
>
> 如果在故障排除中未找到解决方案，请浏览 GitHub 仓库或创建新的 issue：
>
> - [docker/for-mac](https://github.com/docker/for-mac/issues)
> - [docker/for-win](https://github.com/docker/for-win/issues)
> - [docker/for-linux](https://github.com/docker/for-linux/issues)

## 适用于所有平台的主题

### 证书未正确设置 

#### 错误信息 

当尝试使用 `docker run` 从一个 registry 拉取镜像时，你可能会遇到以下错误：

```console
Error response from daemon: Get http://192.168.203.139:5858/v2/: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

此外，registry 的日志可能显示：

```console
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52882: tls: client didn't provide a certificate
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52883: tls: first record does not look like a TLS handshake
```

#### 可能的原因 

- Docker Desktop 会忽略在 insecure registries 下列出的证书。
- 客户端证书不会发送到 insecure registries，从而导致握手失败。

#### 解决方案 

- 确保你的 registry 已使用有效的 SSL 证书正确配置。
- 如果你的 registry 是自签名的，请通过将证书添加到 Docker 的证书目录（Linux 上为 /etc/docker/certs.d/）来配置 Docker 信任该证书。
- 如果问题仍然存在，请检查你的 Docker 守护进程配置并启用 TLS 身份验证。

### Docker Desktop 的 UI 显示为绿色、扭曲或出现视觉瑕疵

#### 原因

Docker Desktop 默认使用硬件加速图形，这可能会在某些 GPU 上引发问题。

#### 解决方案

禁用硬件加速：

1. 编辑 Docker Desktop 的 `settings-store.json` 文件（对于 Docker Desktop 4.34 及更早版本，则为 `settings.json`）。你可以在以下位置找到此文件：

   - Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
   - Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
   - Linux: `~/.docker/desktop/settings-store.json.`

2. 添加以下条目：

   ```JSON
   $ "disableHardwareAcceleration": true
   ```

3. 保存文件并重启 Docker Desktop。

### 使用挂载卷时出现运行时错误，提示找不到应用程序文件、对卷挂载的访问被拒绝或服务无法启动

#### 原因

如果你的项目目录位于主目录（`/home/<user>`）之外，Docker Desktop 需要文件共享权限才能访问它。

#### 解决方案

在适用于 Mac 和 Linux 的 Docker Desktop 中启用文件共享：

1. 导航到 **Settings**，选择 **Resources**，然后选择 **File sharing**。
2. 添加包含 Dockerfile 和卷挂载路径的驱动器或文件夹。

在适用于 Windows 的 Docker Desktop 中启用文件共享：

1. 在 **Settings** 中，选择 **Shared Folders**。 
2. 共享包含 Dockerfile 和卷挂载路径的文件夹。

### `port already allocated` 错误

#### 错误信息

启动容器时，你可能会看到类似以下的错误：

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

或者

```text
listen tcp:0.0.0.0:8080: bind: address is already in use
```

#### 原因

- 你系统上的另一个应用程序正在使用指定的端口。
- 之前运行的容器未正确停止，并且仍然绑定到该端口。

#### 解决方案

要发现该软件的身份，可以：
- 使用 `resmon.exe` GUI，选择 **Network**，然后选择 **Listening Ports**
- 在 PowerShell 中，使用 `netstat -aon | find /i "listening "` 来发现当前正在使用该端口的进程的 PID（PID 是最右侧列中的数字）。

然后，决定是关闭另一个进程，还是在你的 Docker 应用中使用不同的端口。

## 适用于 Linux 和 Mac 的主题

### Docker Desktop 在 Mac 或 Linux 平台上无法启动

#### 错误信息 

由于 Unix 域套接字路径长度限制，Docker 无法启动：

```console
[vpnkit-bridge][F] listen unix <HOME>/Library/Containers/com.docker.docker/Data/http-proxy-control.sock: bind: invalid argument
```

```console
[com.docker.backend][E] listen(vsock:4099) failed: listen unix <HOME>/Library/Containers/com.docker.docker/Data/vms/0/00000002.00001003: bind: invalid argument
```

#### 原因

在 Mac 和 Linux 上，Docker Desktop 创建用于进程间通信的 Unix 域套接字。这些套接字是在用户的主目录下创建的。

Unix 域套接字有最大路径长度限制：
 - Mac 上为 104 个字符
 - Linux 上为 108 个字符

如果你的主目录路径过长，Docker Desktop 将无法创建必要的套接字。

#### 解决方案

确保你的用户名足够短，以使路径保持在允许的限制内：
 - Mac：用户名应 ≤ 33 个字符
 - Linux：用户名应 ≤ 55 个字符

## 适用于 Mac 的主题

### 升级需要管理员权限

#### 原因 

在 macOS 上，没有管理员权限的用户无法从 Docker Desktop 仪表板执行应用内升级。

#### 解决方案

> [!IMPORTANT]
>
> 升级前请勿卸载当前版本。这样做会删除所有本地的 Docker 容器、镜像和卷。

要升级 Docker Desktop：

- 请管理员在现有版本上安装较新的版本。
- 如果你的设置适合，可以使用 []`--user` 安装标志](/manuals/desktop/setup/install/mac-install.md#security-and-access)。

### 持续收到通知，提示某个应用程序更改了我的 Desktop 配置

#### 原因 

你收到此通知是因为配置完整性检查功能检测到第三方应用程序已更改你的 Docker Desktop 配置。这通常是由于符号链接不正确或缺失造成的。该通知确保你了解这些更改，以便你可以审查并修复任何潜在问题，以保持系统可靠性。

打开通知会弹出一个窗口，其中提供了有关检测到的完整性问题的详细信息。

#### 解决方案

如果你选择忽略通知，它只会在下次启动 Docker Desktop 时再次显示。如果你选择修复配置，你将不会再次收到提示。

如果你想关闭配置完整性检查通知，请导航到 Docker Desktop 的设置，在 **General** 选项卡中，清除 **Automatically check configuration** 设置。 

### `com.docker.vmnetd` 在我退出应用程序后仍在运行

特权辅助进程 `com.docker.vmnetd` 由 `launchd` 启动并在后台运行。除非 `Docker.app` 连接到它，否则该进程不会消耗任何资源，因此可以安全忽略。

### 检测到不兼容的 CPU

#### 原因

Docker Desktop 需要支持虚拟化的处理器 (CPU)，更具体地说，需要支持 [Apple Hypervisor
framework](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)。

#### 解决方案

检查以下内容：

 - 你已为你的架构安装了正确的 Docker Desktop
 - 你的 Mac 支持 Apple 的 Hypervisor 框架。要检查你的 Mac 是否支持 Hypervisor 框架，请在终端窗口中运行以下命令。

   ```console
   $ sysctl kern.hv_support
   ```

   如果你的 Mac 支持 Hypervisor 框架，该命令将打印 `kern.hv_support: 1`。

   如果不支持，该命令将打印 `kern.hv_support: 0`。

另请参阅 Apple 文档中的 [Hypervisor Framework
Reference](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/)
以及 Docker Desktop 的 [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#system-requirements)。

### VPNKit 持续中断

#### 原因

在 Docker Desktop 4.19 版本中，gVisor 取代了 VPNKit，以在 macOS 13 及更高版本上使用 Virtualization 框架时增强 VM 网络的性能。

#### 解决方案

要继续使用 VPNKit：

1. 打开位于 `~/Library/Group Containers/group.com.docker/settings-store.json` 的 `settings-store.json` 文件
2. 添加：

   ```JSON
   $ "networkType":"vpnkit"
   ```
3. 保存文件并重启 Docker Desktop。

## 适用于 Windows 的主题

### 安装防病毒软件时 Docker Desktop 无法启动

#### 原因

某些防病毒软件可能与 Hyper-V 和 Microsoft
Windows 10 版本不兼容。这种冲突通常发生在 Windows 更新之后，表现为来自 Docker 守护进程的错误响应和 Docker Desktop 启动失败。

#### 解决方案

作为临时解决方案，请卸载防病毒软件，或将 Docker 添加到你的防病毒软件的排除项/例外中。

### 共享卷的数据目录出现权限错误

#### 原因 

从 Windows 共享文件时，Docker Desktop 将[共享卷](/manuals/desktop/settings-and-maintenance/settings.md#file-sharing)
的权限设置为默认值 [0777](https://chmodcommand.com/chmod-0777/)
（为 `user` 和 `group` 设置 `read`、`write`、`execute` 权限）。

共享卷上的默认权限是不可配置的。 

#### 解决方案

如果你正在使用需要不同权限的应用程序，可以：
 - 使用非主机挂载卷  
 - 找到一种方法使应用程序使用默认文件权限工作

### 意外的语法错误，请对容器中的文件使用 Unix 风格的行结束符

#### 原因 

Docker 容器期望 Unix 风格的 `\n` 行结束符，而不是 Windows 风格的 `\r\n`。这包括在构建时在命令行引用的文件以及 Dockerfile 中的 RUN 命令。

在使用 Windows 工具（例如 shell 脚本）编写文件时请记住这一点，在这些工具中默认很可能是 Windows 风格的行结束符。这些命令最终会传递给基于 Unix 的容器内的 Unix 命令（例如，传递给 `/bin/sh` 的 shell 脚本）。如果使用 Windows 风格的行结束符，`docker run` 将因语法错误而失败。

#### 解决方案 

 - 使用以下命令将文件转换为 Unix 风格的行结束符：
   
   ```console
   $ dos2unix script.sh
   ```
- 在 VS Code 中，将行结束符设置为 `LF` (Unix) 而不是 `CRLF` (Windows)。

### Windows 上的路径转换错误

#### 原因

与 Linux 不同，Windows 需要对卷挂载进行显式路径转换。


在 Linux 上，系统负责将一个路径挂载到另一个路径。例如，当你在 Linux 上运行以下命令时：

```console
$ docker run --rm -ti -v /home/user/work:/work alpine
```

它会向目标容器添加一个 `/work` 目录来镜像指定的路径。

#### 解决方案

更新源路径。例如，如果你使用
旧版 Windows shell (`cmd.exe`)，可以使用以下命令：

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
```

这将启动容器并确保卷变得可用。这是可能的，因为 Docker Desktop 检测到
Windows 风格的路径并提供适当的转换来挂载目录。

Docker Desktop 还允许你使用 Unix 风格的路径进行适当的格式化。例如：

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

Git Bash（或 MSYS）在 Windows 上提供了一个类 Unix 环境。这些工具在命令行上应用它们自己的
预处理。

这会影响 `$(pwd)`、冒号分隔的路径和波浪号 (`~`)

此外，`\` 字符在 Git Bash 中有特殊含义。 

#### 解决方案

 - 临时禁用 Git Bash 路径转换。例如，使用禁用 MSYS 路径转换的方式运行命令：
    ```console
    $ MSYS_NO_PATHCONV=1 docker run --rm -ti -v $(pwd):/work alpine
    ```
 - 使用正确的路径格式：
    - 使用双正向和反向斜杠（`\\` `//`）代替单斜杠（`\` `/`）。
    - 如果引用 `$(pwd)`，请额外添加一个 `/`：

脚本的可移植性不受影响，因为 Linux 将多个 `/` 视为单个条目。

### 由于虚拟化无法工作，Docker Desktop 启动失败

#### 错误信息

一个典型的错误信息是 "Docker Desktop - Unexpected WSL error"，其中提到错误代码
`Wsl/Service/RegisterDistro/CreateVm/HCS/HCS_E_HYPERV_NOT_INSTALLED`。手动执行 `wsl` 命令
也会因相同的错误代码而失败。

#### 原因

- BIOS 中的虚拟化设置已禁用。
- Windows Hyper-V 或 WSL 2 组件缺失。

请注意，某些第三方软件（如 Android 模拟器）会在安装时禁用 Hyper-V。

#### 解决方案

你的计算机必须具备以下功能才能使 Docker Desktop 正常运行：

##### WSL 2 and Windows Home

1. 虚拟机平台
2. [适用于 Linux 的 Windows 子系统](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
   请注意，许多 Windows 设备已启用虚拟化，因此这可能不适用。
4. 在 Windows 启动时启用 Hypervisor

![WSL 2 enabled](../../images/wsl2-enabled.png)

必须能够无错误地运行 WSL 2 命令，例如：

```console
PS C:\users\> wsl -l -v
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Stopped         2
PS C:\users\> wsl -d docker-desktop echo WSL 2 is working
WSL 2 is working
```

如果功能已启用但命令无法正常工作，请首先检查[虚拟化是否已开启](#virtualization-must-be-turned-on)
然后，如果需要，[在 Windows 启动时启用 Hypervisor](#hypervisor-enabled-at-windows-startup)。如果在虚拟机中运行 Docker
Desktop，请确保 [hypervisor 已启用嵌套虚拟化](#turn-on-nested-virtualization)。

##### Hyper-V

在 Windows 10 Pro 或 Enterprise 上，你也可以使用 Hyper-V，并启用以下功能：

1. [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview)
   已安装并正常工作
2. [在 BIOS 中启用虚拟化](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1)
   请注意，许多 Windows 设备已启用虚拟化，因此这可能不适用。
3. 在 Windows 启动时启用 Hypervisor

![Hyper-V on Windows features](../../images/hyperv-enabled.png)

Docker Desktop 需要安装并启用 Hyper-V 以及适用于 Windows
PowerShell 的 Hyper-V 模块。Docker Desktop 安装程序会为你启用它。

Docker Desktop 还需要两个 CPU 硬件功能来使用 Hyper-V：虚拟化和二级地址转换 (SLAT)，后者也称为快速虚拟化索引 (RVI)。在某些系统上，必须在 BIOS 中启用虚拟化。所需步骤因供应商而异，但通常 BIOS 选项称为 `Virtualization Technology (VTx)` 或类似名称。运行命令 `systeminfo` 以检查所有必需的 Hyper-V 功能。有关更多详细信息，请参阅 [Windows 10 上的 Hyper-V 先决条件](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements)。

要手动安装 Hyper-V，请参阅 [在 Windows 10 上安装 Hyper-V](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/quick_start/walkthrough_install)。安装后*必须*重启。如果安装 Hyper-V 后未重启，Docker Desktop 将无法正常工作。

从开始菜单，键入 **启用或关闭 Windows 功能** 并按回车键。
在后续屏幕中，验证 Hyper-V 是否已启用。

##### 必须开启虚拟化

除了 [Hyper-V](#hyper-v) 或 [WSL 2](/manuals/desktop/features/wsl/_index.md)，还必须开启虚拟化。检查任务管理器中的性能选项卡。或者，你可以在终端中键入 `systeminfo`。如果你看到 `Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed`，则表示虚拟化已启用。

![Task Manager](../../images/virtualization-enabled.png)

如果你手动卸载了 Hyper-V、WSL 2 或关闭了虚拟化，
Docker Desktop 将无法启动。 

要开启嵌套虚拟化，请参阅 [在 VM 或 VDI 环境中运行 Docker Desktop for Windows](/manuals/desktop/setup/vm-vdi.md#turn-on-nested-virtualization)。

##### 在 Windows 启动时启用 Hypervisor

如果你已完成前面的步骤但仍然遇到
Docker Desktop 启动问题，这可能是因为 Hypervisor 已安装，
但在 Windows 启动期间未启动。某些工具（如旧版 Virtual Box）
和视频游戏安装程序会在启动时关闭 hypervisor。要重新打开它：

1. 以管理员身份打开控制台提示符。
2. 运行 `bcdedit /set hypervisorlaunchtype auto`。
3. 重启 Windows。

你也可以参考关于控制流防护 (CFG) 设置的 [Microsoft TechNet 文章](https://social.technet.microsoft.com/Forums/en-US/ee5b1d6b-09e2-49f3-a52c-820aafc316f9/hyperv-doesnt-work-after-upgrade-to-windows-10-1809?forum=win10itprovirt)。

##### 开启嵌套虚拟化

如果你使用 Hyper-V，并且在 VDI 环境中运行
