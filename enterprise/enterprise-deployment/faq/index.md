# 企业部署常见问题

## MSI

有关使用 MSI 安装程序安装 Docker Desktop 的常见问题。

### 如果用户已有旧版 Docker Desktop 安装（即 `.exe` 版本），用户数据会怎样？

用户必须先[卸载](/manuals/desktop/uninstall.md)旧的 `.exe` 安装，才能使用新的 MSI 版本。这将删除机器上所有 Docker 容器、镜像、卷以及其他与 Docker 相关的本地数据，并移除 Docker Desktop 生成的文件。

要在卸载前保留现有数据，用户应[备份](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)其容器和卷。

对于 Docker Desktop 4.30 及更高版本，`.exe` 安装程序包含一个 `-keep-data` 标志，可在移除 Docker Desktop 的同时保留底层资源（例如容器 VM）：

```powershell
& 'C:\Program Files\Docker\Docker\Docker Desktop Installer.exe' uninstall -keep-data
```

### 如果用户的机器上有旧的 `.exe` 安装，会发生什么？

MSI 安装程序会检测旧的 `.exe` 安装，并阻止安装，直到卸载先前版本。它会提示用户先卸载当前/旧版本，然后再重试安装 MSI 版本。

### 我的安装失败了，如何查明原因？

MSI 安装可能会静默失败，几乎不提供诊断反馈。

要调试失败的安装，请在启用详细日志记录的情况下再次运行安装：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

安装失败后，打开日志文件并搜索 `value 3` 的出现位置。这是 Windows Installer 在失败时输出的退出代码。在该行上方，您将找到失败的原因。

### 为什么安装程序在每次全新安装结束时都提示重新启动？

安装程序提示重新启动，是因为它假定系统已进行更改，需要重新启动才能完成其配置。

例如，如果您选择了 WSL 引擎，安装程序会添加所需的 Windows 功能。安装这些功能后，系统会重新启动以完成配置，从而使 WSL 引擎能够正常工作。

您可以使用 `/norestart` 选项从命令行启动安装程序来禁止重新启动：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /norestart
```

### 为什么使用 Intune 或其他 MDM 解决方案安装 MSI 时，`docker-users` 组未填充用户账户？

MDM 解决方案通常在系统账户的上下文中安装应用程序。这意味着 `docker-users` 组不会填充用户账户，因为系统账户无权访问用户上下文。

例如，您可以通过在提升的命令提示符下使用 `psexec` 运行安装程序来重现此问题：

```powershell
psexec -i -s msiexec /i "DockerDesktop.msi"
```
安装应成功完成，但 `docker-users` 组不会被填充。

作为解决方法，您可以创建一个在用户账户上下文中运行的脚本。

该脚本将负责创建 `docker-users` 组并使用正确的用户填充它。

这是一个创建 `docker-users` 组并将当前用户添加到其中的示例脚本（要求可能因环境而异）：

```powershell
$Group = "docker-users"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# 创建组
New-LocalGroup -Name $Group

# 将用户添加到组中
Add-LocalGroupMember -Group $Group -Member $CurrentUser
```

> [!NOTE]
>
> 将新用户添加到 `docker-users` 组后，用户必须先注销然后再重新登录，更改才能生效。

## MDM

有关使用移动设备管理（MDM）工具（如 Jamf、Intune 或 Workspace ONE）部署 Docker Desktop 的常见问题。

### 为什么我的 MDM 工具无法一次性应用所有 Docker Desktop 配置设置？

某些 MDM 工具（例如 Workspace ONE）可能不支持在单个 XML 文件中应用多个配置设置。在这些情况下，您可能需要在单独的 XML 文件中部署每个设置。

请参阅您的 MDM 提供商的文档，了解具体的部署要求或限制。
