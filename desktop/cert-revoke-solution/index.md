# 修复 Mac 上的 Docker Desktop 启动问题

本指南提供了解决近期影响部分 macOS 用户使用 Docker Desktop 问题的步骤。该问题可能导致 Docker Desktop 无法启动，在某些情况下还可能触发不准确的恶意软件警告。有关该事件的更多详细信息，请参阅[博客文章](https://www.docker.com/blog/incident-update-docker-desktop-for-mac/)。

> [!NOTE]
>
> Docker Desktop 版本 4.28 及更早版本不受此问题影响。

## 可用解决方案

根据您的情况，有以下几种可选方案：

### 升级到 Docker Desktop 版本 4.37.2（推荐）

推荐的方法是升级到最新的 Docker Desktop 版本，即版本 4.37.2。

如果可能，请直接通过应用程序更新。如果无法更新，且仍然看到恶意软件弹窗，请按以下步骤操作：

1. 终止无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep -i docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```
    
2. 确保恶意软件弹窗已永久关闭。

3. [下载并安装版本 4.37.2](/manuals/desktop/release-notes.md#4372)。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权弹窗消息。

5. 输入您的密码。

现在您应该能看到 Docker Desktop 仪表板。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹窗仍然存在，且 Docker 在废纸篓中，请尝试清空废纸篓并重新运行这些步骤。

### 如果您使用版本 4.32 - 4.36，请安装补丁

如果您无法升级到最新版本，且看到恶意软件弹窗，请按以下步骤操作：

1. 终止无法正常启动的 Docker 进程：
   ```console
   $ sudo launchctl bootout system/com.docker.vmnetd 2>/dev/null || true
   $ sudo launchctl bootout system/com.docker.socket 2>/dev/null || true
    
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.vmnetd || true
   $ sudo rm /Library/PrivilegedHelperTools/com.docker.socket || true
 
   $ ps aux | grep docker | awk '{print $2}' | sudo xargs kill -9 2>/dev/null
   ```

2. 确保恶意软件弹窗已永久关闭。

3. [下载并安装与您当前基础版本匹配的补丁安装程序](/manuals/desktop/release-notes.md)。例如，如果您使用版本 4.36.0，请安装 4.36.1。

4. 启动 Docker Desktop。5 到 10 秒后会显示一个特权弹窗消息。

5. 输入您的密码。

现在您应该能看到 Docker Desktop 仪表板。

> [!TIP]
>
> 如果完成这些步骤后恶意软件弹窗仍然存在，且 Docker 在废纸篓中，请尝试清空废纸篓并重新运行这些步骤。

## MDM 脚本

如果您是 IT 管理员，且您的开发人员看到恶意软件弹窗：

1. 确保您的开发人员拥有重新签名的 Docker Desktop 版本 4.32 或更高版本。
2. 运行以下脚本：

   ```console
   #!/bin/bash

   # Stop the docker services
   echo "Stopping Docker..."
   sudo pkill -i docker

   # Stop the vmnetd service
   echo "Stopping com.docker.vmnetd service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.vmnetd.plist

   # Stop the socket service
   echo "Stopping com.docker.socket service..."
   sudo launchctl bootout system /Library/LaunchDaemons/com.docker.socket.plist

   # Remove vmnetd binary
   echo "Removing com.docker.vmnetd binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.vmnetd

   # Remove socket binary
   echo "Removing com.docker.socket binary..."
   sudo rm -f /Library/PrivilegedHelperTools/com.docker.socket

   # Install new binaries
   echo "Install new binaries..."
   sudo cp /Applications/Docker.app/Contents/Library/LaunchServices/com.docker.vmnetd /Library/PrivilegedHelperTools/
   sudo cp /Applications/Docker.app/Contents/MacOS/com.docker.socket /Library/PrivilegedHelperTools/
   ```

## Homebrew casks

如果您使用 Homebrew casks 安装了 Docker Desktop，推荐的解决方案是完全重新安装以解决问题。

要重新安装 Docker Desktop，请在终端中运行以下命令：

```console
$ brew update
$ brew reinstall --cask docker
```

这些命令将更新 Homebrew 并完全重新安装 Docker Desktop，确保您拥有已应用修复的最新版本。
