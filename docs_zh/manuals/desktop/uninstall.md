---
description: 如何卸载 Docker Desktop
keywords: Windows, 卸载, Mac, Linux, Docker Desktop
title: 卸载 Docker Desktop
linkTitle: 卸载
weight: 210
---

> [!WARNING]
>
> 卸载 Docker Desktop 会删除机器上本地的 Docker 容器、镜像、卷和其他 Docker 相关数据，并移除应用程序生成的文件。如需了解如何在卸载前保留重要数据，请参考 [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 章节。

{{< tabs >}}
{{< tab name="Windows" >}}

#### 通过图形界面卸载

1. 从 Windows **开始** 菜单中，选择 **设置** > **应用** > **应用和功能**。
2. 在 **应用和功能** 列表中选择 **Docker Desktop**，然后选择 **卸载**。
3. 点击 **卸载** 确认操作。

#### 通过命令行卸载

1. 定位安装程序：
   ```console
   $ C:\Program Files\Docker\Docker\Docker Desktop Installer.exe
   ```
2. 卸载 Docker Desktop。
   - 在 PowerShell 中运行：
    ```console
    $ Start-Process 'Docker Desktop Installer.exe' -Wait uninstall
    ```
   - 在命令提示符中运行：
    ```console
    $ start /w "" "Docker Desktop Installer.exe" uninstall
    ```

卸载 Docker Desktop 后，可能仍会残留一些文件，你可以手动删除。这些文件包括：

```console
C:\ProgramData\Docker
C:\ProgramData\DockerDesktop
C:\Program Files\Docker
C:\Users\<你的用户名>\AppData\Local\Docker
C:\Users\<你的用户名>\AppData\Roaming\Docker
C:\Users\<你的用户名>\AppData\Roaming\Docker Desktop
C:\Users\<你的用户名>\.docker
```

{{< /tab >}}
{{< tab name="Mac" >}}

#### 通过图形界面卸载

1. 打开 Docker Desktop。
2. 在 Docker Desktop 仪表板的右上角，点击 **Troubleshoot**（故障排除）图标。
3. 选择 **Uninstall**（卸载）。
4. 系统提示时，再次点击 **Uninstall**（卸载）确认。

然后你可以将 Docker 应用程序移至废纸篓。

#### 通过命令行卸载

运行：

```console
$ /Applications/Docker.app/Contents/MacOS/uninstall
```

然后你可以将 Docker 应用程序移至废纸篓。

> [!NOTE]
> 使用卸载命令卸载 Docker Desktop 时，你可能会遇到以下错误：
>
> ```console
> $ /Applications/Docker.app/Contents/MacOS/uninstall
> Password:
> Uninstalling Docker Desktop...
> Error: unlinkat /Users/<USER_HOME>/Library/Containers/com.docker.docker/.com.apple.containermanagerd.metadata.plist: > operation not permitted
> ```
>
> “operation not permitted” 错误可能出现在文件 `.com.apple.containermanagerd.metadata.plist` 或其父目录 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/` 上。此错误可以忽略，因为你已成功卸载 Docker Desktop。
> 你可以稍后通过允许终端应用使用 **完全磁盘访问权限**（**系统设置** > **隐私与安全性** > **完全磁盘访问权限**）来删除目录 `/Users/<USER_HOME>/Library/Containers/com.docker.docker/`。

卸载 Docker Desktop 后，可能仍会残留一些文件，你可以手动删除：

```console
$ rm -rf ~/Library/Group\ Containers/group.com.docker
$ rm -rf ~/.docker
```

对于 Docker Desktop 4.36 及更早版本，文件系统上可能还会残留以下文件，你可以使用管理员权限删除：

```console
/Library/PrivilegedHelperTools/com.docker.vmnetd
/Library/PrivilegedHelperTools/com.docker.socket
```

{{< /tab >}}
{{< tab name="Ubuntu" >}}

卸载 Ubuntu 上的 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这将移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这将移除 `$HOME/.docker/desktop` 中的配置和数据文件、`/usr/local/bin/com.docker.cli` 中的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后仍然保留，它们可能会与未来的 Docker 设置发生冲突。

{{< /tab >}}
{{< tab name="Debian" >}}

卸载 Debian 上的 Docker Desktop：

1. 移除 Docker Desktop 应用程序：

   ```console
   $ sudo apt remove docker-desktop
   ```

   这将移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo apt purge docker-desktop
   ```

   这将移除 `$HOME/.docker/desktop` 中的配置和数据文件、`/usr/local/bin/com.docker.cli` 中的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后仍然保留，它们可能会与未来的 Docker 设置发生冲突。

{{< /tab >}}
{{< tab name="Fedora" >}}

卸载 Fedora 上的 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo dnf remove docker-desktop
   ```

   这将移除 Docker Desktop 软件包本身，但不会删除其所有文件或设置。

2. 手动删除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   $ sudo rm /usr/local/bin/com.docker.cli
   $ sudo dnf remove docker-desktop
   ```

   这将移除 `$HOME/.docker/desktop` 中的配置和数据文件、`/usr/local/bin/com.docker.cli` 中的符号链接，并清除剩余的 systemd 服务文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后仍然保留，它们可能会与未来的 Docker 设置发生冲突。

{{< /tab >}}
{{< tab name="Arch" >}}

卸载 Arch 上的 Docker Desktop：

1. 移除 Docker Desktop 应用程序。运行：

   ```console
   $ sudo pacman -Rns docker-desktop
   ```

   这将移除 Docker Desktop 软件包及其配置文件和不再被其他软件包需要的依赖项。

2. 手动删除残留文件。

   ```console
   $ rm -r $HOME/.docker/desktop
   ```

   这将移除 `$HOME/.docker/desktop` 中的配置和数据文件。

3. 清理 Docker 配置设置。在 `$HOME/.docker/config.json` 中，删除 `credsStore` 和 `currentContext` 属性。

   这些条目告诉 Docker 在哪里存储凭据以及哪个上下文处于活动状态。如果在卸载 Docker Desktop 后仍然保留，它们可能会与未来的 Docker 设置发生冲突。

{{< /tab >}}
{{< /tabs >}}