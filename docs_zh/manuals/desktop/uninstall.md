---
description: 如何卸载 Docker Desktop
keywords: Windows, uninstall, Mac, Linux, Docker Desktop
title: 卸载 Docker Desktop
linkTitle: 卸载
weight: 210
---

> [!WARNING]
>
> 卸载 Docker Desktop 会销毁机器本地的 Docker 容器、镜像、卷和其他与 Docker 相关的数据，并删除应用程序生成的文件。要了解如何在卸载前保留重要数据，请参阅[备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md)部分。

{{< tabs >}}
{{< tab name="Windows" >}}

#### 通过图形界面 (GUI)

1. 在 Windows **开始**菜单中，选择 **设置** > **应用** > **应用和功能**。
2. 从**应用和功能**列表中选择 **Docker Desktop**，然后选择**卸载**。
3. 选择**卸载**以确认您的选择。

#### 通过命令行界面 (CLI)

1. 找到安装程序：
   ```console
   $ C:\Program Files\Docker\Docker\Docker Desktop Installer.exe
   ```
2. 卸载 Docker Desktop。
 - 在 PowerShell 中，运行：
    ```console
    $ Start-Process 'Docker Desktop Installer.exe' -Wait uninstall
    ```
 - 在命令提示符中，运行：
    ```console
    $ start /w "" "Docker Desktop Installer.exe" uninstall
    ```

卸载 Docker Desktop 后，可能会残留一些文件，您可以手动删除。这些文件包括：

```console
C:\ProgramData\Docker
C:\ProgramData\DockerDesktop
C:\Program Files\Docker
C:\Users\<您的用户名>\AppData\Local\Docker
C:\Users\<您的用户名>\AppData\Roaming\Docker
C:\Users\<您的用户名>\AppData\Roaming\Docker Desktop
C:\Users\<您的用户名>\.docker
```
 
{{< /tab >}}
{{< tab name="Mac" >}}

#### 通过图形界面 (GUI)

1. 打开 Docker Desktop。
2. 在 Docker Desktop 仪表板的右上角，选择**故障排除**图标。
3. 选择**卸载**。
4. 出现提示时，再次选择**卸载**进行确认。

然后，您可以将 Docker 应用程序移到废纸篓。

#### 通过命令行界面 (CLI)

运行：

```console
$ /Applications/Docker.app/Contents/MacOS/uninstall
```

然后，您可以将 Docker 应用程序移到废纸篓。

> [!NOTE]
> 使用卸载命令卸载 Docker Desktop 时，您可能会遇到以下错误。
>
> ```console
> $ /Applications/Docker.app/Contents/MacOS/uninstall
> Password:
> Uninstalling Docker Desktop...
> Error: unlinkat /Users/<USER_HOME>/Library/Containers/com.docker.docker/.com.apple.containermanagerd.metadata.plist: > operation not permitted
> ```
>
> “operation not permitted”（操作不被允许）错误报告在文件 `.com.apple.containermanagerd.metadata.plist` 或其父目录 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/` 上。您可以忽略此错误，因为您已成功卸载 Docker Desktop。
> 稍后，您可以为正在使用的终端应用程序授予**完全磁盘访问权限**（**系统设置** > **隐私与安全性** > **完全磁盘访问权限**），然后删除目录 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/`。

卸载 Docker Desktop 后，可能会残留一些文件，您可以删除：

```console
$ rm -rf ~/Library/Group\ Containers/group.com.docker
$ rm -rf ~/.docker
```

对于 Docker Desktop 4.36 及更早版本，文件系统上可能还会留下以下文件。您可以使用管理员权限删除这些文件：

```console
/Library/PrivilegedHelperTools/com.docker.vmnetd
/Library/PrivilegedHelperTools/com.docker.socket
```

{{< /tab >}}
{{< tab name="Ubuntu" >}}

要卸载 Ubuntu 的 Docker Desktop：

1. 删除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这将删除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除剩余文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这将删除 `$HOME/.docker/desktop` 的配置和数据文件、`/usr/local/bin/com.docker.cli` 的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 存储凭据的位置以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后它们仍然存在，可能会与未来的 Docker 设置冲突。

{{< /tab >}}
{{< tab name="Debian" >}}

要卸载 Debian 的 Docker Desktop，请运行：

1. 删除 Docker Desktop 应用程序：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这将删除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除剩余文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这将删除 `$HOME/.docker/desktop` 的配置和数据文件、`/usr/local/bin/com.docker.cli` 的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 存储凭据的位置以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后它们仍然存在，可能会与未来的 Docker 设置冲突。

{{< /tab >}}
{{< tab name="Fedora" >}}

要卸载 Fedora 的 Docker Desktop：

1. 删除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo dnf remove docker-desktop
   ```

   这将删除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除剩余文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo dnf remove docker-desktop
   ```

   这将删除 `$HOME/.docker/desktop` 的配置和数据文件、`/usr/local/bin/com.docker.cli` 的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 存储凭据的位置以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后它们仍然存在，可能会与未来的 Docker 设置冲突。

{{< /tab >}}
{{< tab name="Arch" >}}

要卸载 Arch 的 Docker Desktop：

1. 删除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo pacman -Rns docker-desktop
   ```

   这将删除 Docker Desktop 软件包及其配置文件和不被其他软件包所需的依赖项。

2. 手动删除剩余文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   ```

   这将删除 `$HOME/.docker/desktop` 的配置和数据文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 存储凭据的位置以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后它们仍然存在，可能会与未来的 Docker 设置冲突。

{{< /tab >}}
{{< /tabs >}}