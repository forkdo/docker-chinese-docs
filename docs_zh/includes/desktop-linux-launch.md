要启动 Linux 版 Docker Desktop：

1. 在你的 Gnome/KDE 桌面中导航到 Docker Desktop 应用程序。

2. 选择 **Docker Desktop** 以启动 Docker。

   此时将显示 Docker 订阅服务协议。

3. 选择 **Accept（接受）** 以继续。接受条款后，Docker Desktop 将启动。

   注意：如果你不同意条款，Docker Desktop 将无法运行。你可以稍后通过打开 Docker Desktop 来选择接受条款。

   更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议你也阅读 [常见问题解答](https://www.docker.com/pricing/faq)。

或者，打开终端并运行：

```console
$ systemctl --user start docker-desktop
```

Docker Desktop 启动时，会创建一个专用的 [上下文](/engine/context/working-with-contexts)，Docker CLI 可以将其作为目标使用，并将其设置为当前使用的上下文。这是为了避免与可能在 Linux 主机上运行并使用默认上下文的本地 Docker Engine 发生冲突。关闭时，Docker Desktop 会将当前上下文重置为之前的上下文。

Docker Desktop 安装程序会更新主机上的 Docker Compose 和 Docker CLI 二进制文件。
它安装 Docker Compose V2，并允许用户在设置面板中选择将其链接为 docker-compose。Docker Desktop 在 `/usr/local/bin/com.docker.cli` 中安装新的 Docker CLI 二进制文件，该文件包含云集成功能，并在 `/usr/local/bin` 中创建到经典 Docker CLI 的符号链接。

成功安装 Docker Desktop 后，你可以通过运行以下命令检查这些二进制文件的版本：

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

要启用 Docker Desktop 在登录时自动启动，请从 Docker 菜单中选择
**Settings（设置）** > **General（常规）** > **Start Docker Desktop when you sign in to your computer（在登录计算机时启动 Docker Desktop）**。

或者，打开终端并运行：

```console
$ systemctl --user enable docker-desktop
```

要停止 Docker Desktop，请选择 Docker 菜单图标以打开 Docker 菜单，然后选择 **Quit Docker Desktop（退出 Docker Desktop）**。

或者，打开终端并运行：

```console
$ systemctl --user stop docker-desktop
```