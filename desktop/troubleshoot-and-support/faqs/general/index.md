# Docker Desktop 通用常见问题解答


### 我可以在离线状态下使用 Docker Desktop 吗？

可以，您可以在离线状态下使用 Docker Desktop。但是，您将无法访问需要互联网连接的功能。此外，任何需要登录的功能在离线或使用隔离网络环境时都无法使用。

### 如何连接到远程 Docker Engine API？

要连接到远程 Engine API，您可能需要为 Docker 客户端和开发工具提供 Engine API 的位置。

Mac 和 Windows WSL 2 用户可以通过 Unix 套接字连接到 Docker Engine：`unix:///var/run/docker.sock`。Docker Desktop for Linux 使用位于 `~/.docker/desktop/docker.sock` 的[按用户套接字](linuxfaqs.md#how-do-i-use-docker-sdks-with-docker-desktop-for-linux)，而不是系统级的 `/var/run/docker.sock`。

如果您使用的是 [Apache Maven](https://maven.apache.org/) 等应用程序，这些程序需要设置 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量，请指定这些变量以通过 Unix 套接字连接到 Docker 实例。

例如：

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows 用户可以通过**命名管道**连接到 Docker Engine：`npipe:////./pipe/docker_engine`，或通过此 URL 的 **TCP 套接字**：`tcp://localhost:2375`。

详细信息请参阅 [Docker Engine API](/reference/api/engine/_index.md)。

### 如何从容器连接到主机上的服务？

主机的 IP 地址是变化的，或者如果您没有网络访问权限，则可能没有 IP 地址。建议连接到特殊的 DNS 名称 `host.docker.internal`，该名称解析为主机使用的内部 IP 地址。

更多信息和示例，请参阅[如何从容器连接到主机上的服务](/manuals/desktop/features/networking.md#connect-a-container-to-a-service-on-the-host)。

### 我能否将 USB 设备直接传递给容器？

Docker Desktop 不支持直接传递 USB 设备。但是，您可以使用 USB over IP 将常用 USB 设备连接到 Docker Desktop 虚拟机，然后转发到容器。更多详情，请参阅[在 Docker Desktop 中使用 USB/IP](/manuals/desktop/features/usbip.md)。

### 如何验证 Docker Desktop 是否正在使用代理服务器？

要验证，请查看 `httpproxy.log` 中记录的最新事件。该文件位于 macOS 的 `~/Library/Containers/com.docker.docker/Data/log/host` 或 Windows 的 `%LOCALAPPDATA%/Docker/log/host/` 目录中。

以下是您可以看到的一些示例：

- Docker Desktop 使用应用级设置（代理模式：手动）作为代理：

   ```console
   host will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   Linux will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   ```

- Docker Desktop 使用系统级设置（代理模式：系统）作为代理：

   ```console
   host will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   Linux will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   ```

- Docker Desktop 未配置为使用代理服务器：

   ```console
   host will use proxy: disabled
   Linux will use proxy: disabled
   ```

- Docker Desktop 配置为使用应用级设置（代理模式：手动）并使用 PAC 文件：

   ```console
   using a proxy PAC file: http://127.0.0.1:8081/proxy.pac
   host will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   Linux will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   ```

- 使用配置的代理服务器进行连接请求：

   ```console
   CONNECT desktop.docker.com:443: host connecting via static system HTTPS proxy http://172.211.16.3:3128
   ```

### 我能否在不具备管理员权限的情况下运行 Docker Desktop？

Docker Desktop 仅在安装时需要管理员权限。安装完成后，运行它不需要管理员权限。但是，要让非管理员用户运行 Docker Desktop，必须使用特定的安装程序标志进行安装，并满足某些先决条件，这些条件因平台而异。

**Mac**



要在 Mac 上无需管理员权限运行 Docker Desktop，请通过命令行安装并传递 `—user=<userid>` 安装程序标志：

```console
$ /Applications/Docker.app/Contents/MacOS/install --user=<userid>
```

然后，您可以使用指定的用户 ID 登录到您的计算机并启动 Docker Desktop。

> [!NOTE]
> 
> 在启动 Docker Desktop 之前，如果 `~/Library/Group Containers/group.com.docker/` 目录中已存在 `settings-store.json` 文件，当您选择**完成**时，会出现一个**完成 Docker Desktop 设置**窗口，提示需要管理员权限。为避免这种情况，请确保在启动应用程序之前删除之前安装遗留下来的 `settings-store.json` 文件。

**Windows**



> [!NOTE]
>
> 如果您使用的是 WSL 2 后端，请首先确保您满足 WSL 2 的[最低版本要求](/manuals/desktop/features/wsl/best-practices.md)。否则，请先更新 WSL 2。

要在 Windows 上无需管理员权限运行 Docker Desktop，请通过命令行安装并传递 `—always-run-service` 安装程序标志。

```console
$ "Docker Desktop Installer.exe" install —always-run-service
```



