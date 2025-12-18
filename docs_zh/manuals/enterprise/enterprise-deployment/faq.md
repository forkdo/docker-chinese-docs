---
title: 企业部署常见问题
linkTitle: 常见问题
description: 大规模部署 Docker Desktop 的常见问题
keywords: msi, 部署, docker desktop, 常见问题, pkg, mdm, jamf, intune, windows, mac, 企业, 管理员
tags: [FAQ, admin]
weight: 70
aliases:
 - /desktop/install/msi/faq/
 - /desktop/setup/install/msi/faq/
 - /desktop/setup/install/enterprise-deployment/faq/
---

## MSI

关于使用 MSI 安装程序安装 Docker Desktop 的常见问题。

### 如果用户机器上已有旧版 Docker Desktop 安装（即 `.exe`），用户数据会发生什么？

用户必须先[卸载](/manuals/desktop/uninstall.md)旧版 `.exe` 安装，然后才能使用新的 MSI 版本。这会删除机器上本地的所有 Docker 容器、镜像、卷和其他 Docker 相关数据，并移除 Docker Desktop 生成的文件。

要在卸载前保留现有数据，用户应先[备份](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)其容器和卷。

对于 Docker Desktop 4.30 及更高版本，`.exe` 安装程序包含 `-keep-data` 标志，可在保留底层资源（如容器虚拟机）的同时移除 Docker Desktop：

```powershell
& 'C:\Program Files\Docker\Docker\Docker Desktop Installer.exe' uninstall -keep-data
```

### 如果用户的机器上已有旧版 `.exe` 安装，会发生什么？

MSI 安装程序会检测旧版 `.exe` 安装，并在安装新版本前阻止安装，直到旧版本被卸载。它会提示用户先卸载当前/旧版本，然后再尝试安装 MSI 版本。

### 我的安装失败了，如何找出原因？

MSI 安装可能静默失败，提供的诊断反馈很少。

要调试失败的安装，请启用详细日志记录并重新运行安装：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

安装失败后，打开日志文件并搜索 `value 3`。这是 Windows Installer 在失败时输出的退出代码。在该行上方，您会找到失败的原因。

### 为什么每次全新安装结束时，安装程序都会提示重启？

安装程序提示重启，是因为它假设系统已发生需要重启才能完成配置的更改。

例如，如果您选择了 WSL 引擎，安装程序会添加所需的 Windows 功能。安装这些功能后，系统会重启以完成配置，使 WSL 引擎能够正常工作。

您可以在命令行启动安装程序时使用 `/norestart` 选项来抑制重启：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /norestart
```

### 为什么使用 Intune 或其他 MDM 解决方案安装 MSI 时，`docker-users` 组未被填充？

MDM 解决方案通常在系统账户的上下文中安装应用程序。这意味着 `docker-users` 组不会填充用户账户，因为系统账户无法访问用户上下文。

例如，您可以通过在提升的命令提示符中使用 `psexec` 运行安装程序来重现此问题：

```powershell
psexec -i -s msiexec /i "DockerDesktop.msi"
```
安装应能成功完成，但 `docker-users` 组不会被填充。

作为变通方法，您可以创建一个在用户账户上下文中运行的脚本。

该脚本负责创建 `docker-users` 组并用正确的用户填充它。

以下是一个创建 `docker-users` 组并将当前用户添加到该组的示例脚本（具体要求可能因环境而异）：

```powershell
$Group = "docker-users"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

# 创建组
New-LocalGroup -Name $Group

# 将用户添加到组
Add-LocalGroupMember -Group $Group -Member $CurrentUser
```

> [!NOTE]
>
> 将新用户添加到 `docker-users` 组后，用户必须先注销，然后重新登录，更改才会生效。

## MDM

关于使用移动设备管理 (MDM) 工具（如 Jamf、Intune 或 Workspace ONE）部署 Docker Desktop 的常见问题。

### 为什么我的 MDM 工具不能一次性应用所有 Docker Desktop 配置设置？

某些 MDM 工具（如 Workspace ONE）可能不支持在单个 XML 文件中应用多个配置设置。在这种情况下，您可能需要在单独的 XML 文件中部署每个设置。

请参考您的 MDM 提供商文档，了解特定的部署要求或限制。