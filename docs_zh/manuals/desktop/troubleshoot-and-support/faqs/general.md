---
description: Docker Desktop 常见问题解答（适用于所有平台）
keywords: desktop, mac, windows, faqs
title: 通用 FAQ
linkTitle: 通用
tags: [FAQ]
aliases:
- /mackit/faqs/
- /docker-for-mac/faqs/
- /docker-for-windows/faqs/
- /desktop/faqs/
- /desktop/faqs/general/
weight: 10
---

### Docker Desktop 可以离线使用吗？

可以，Docker Desktop 支持离线使用。但是，您无法使用需要活跃互联网连接的功能。此外，任何需要登录的功能在离线或气隙环境中也无法工作。这包括：

- [学习中心](/manuals/desktop/use-desktop/_index.md) 中的资源
- 从 Docker Hub 拉取或推送镜像
- [镜像访问管理](/manuals/security/access-tokens.md)
- [静态漏洞扫描](/manuals/docker-hub/repos/manage/vulnerability-scanning.md)
- Docker 仪表盘中查看远程镜像
- 使用 [BuildKit](/manuals/build/buildkit/_index.md#getting-started) 时的 Docker Build。您可以通过禁用 BuildKit 来解决此问题。运行 `DOCKER_BUILDKIT=0 docker build .` 可禁用 BuildKit。
- [Kubernetes](/manuals/desktop/use-desktop/kubernetes.md)（首次启用 Kubernetes 时会下载镜像）
- 检查更新
- [应用内诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-app)（包括 [自诊断工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-app)）
- 发送使用统计信息
- 当 `networkMode` 设置为 `mirrored` 时

### 如何连接到远程 Docker Engine API？

要连接到远程 Engine API，您可能需要为 Docker 客户端和开发工具提供 Engine API 的位置。

Mac 和 Windows WSL 2 用户可以通过 Unix 套接字连接：`unix:///var/run/docker.sock`。

如果您使用 [Apache Maven](https://maven.apache.org/) 等需要设置 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量的应用，可以指定这些变量以通过 Unix 套接字连接到 Docker 实例。

例如：

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows 用户可以通过 **命名管道** 连接：`npipe:////./pipe/docker_engine`，或通过 **TCP 套接字** 在此 URL 连接：`tcp://localhost:2375`。

详细信息，请参阅 [Docker Engine API](/reference/api/engine/_index.md)。

### 如何从容器连接到主机上的服务？

主机具有变化的 IP 地址，或者在没有网络访问时没有 IP 地址。建议您连接到特殊的 DNS 名称 `host.docker.internal`，它解析为主机使用的内部 IP 地址。

有关详细信息和示例，请参阅 [如何从容器连接到主机上的服务](/manuals/desktop/features/networking.md#connect-a-container-to-a-service-on-the-host)。

### 我可以将 USB 设备透传到容器吗？

Docker Desktop 不支持直接 USB 设备透传。但是，您可以使用 USB/IP 将常见的 USB 设备连接到 Docker Desktop VM，然后转发到容器。详细信息，请参阅 [在 Docker Desktop 中使用 USB/IP](/manuals/desktop/features/usbip.md)。

### 如何验证 Docker Desktop 正在使用代理服务器？

要验证，请查看 `httpproxy.log` 中记录的最新事件。在 macOS 上位于 `~/Library/Containers/com.docker.docker/Data/log/host`，在 Windows 上位于 `%LOCALAPPDATA%/Docker/log/host/`。

以下是您可能看到的一些示例：

- Docker Desktop 使用应用级设置（手动代理模式）：

   ```console
   host will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   Linux will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   ```

- Docker Desktop 使用系统级设置（系统代理模式）：

   ```console
   host will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   Linux will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   ```

- Docker Desktop 未配置使用代理服务器：

   ```console
   host will use proxy: disabled
   Linux will use proxy: disabled
   ```

- Docker Desktop 配置为使用应用级设置（手动代理模式）并使用 PAC 文件：

   ```console
   using a proxy PAC file: http://127.0.0.1:8081/proxy.pac
   host will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   Linux will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   ```

- 使用配置的代理服务器连接请求：

   ```console
   CONNECT desktop.docker.com:443: host connecting via static system HTTPS proxy http://172.211.16.3:3128
   ```

### 如何在没有管理员权限的情况下运行 Docker Desktop？

Docker Desktop 仅在安装时需要管理员权限。安装后，运行它不需要管理员权限。但是，非管理员用户要运行 Docker Desktop，必须使用特定的安装程序标志安装，并满足特定平台的某些先决条件。

{{< tabs >}}
{{< tab name="Mac" >}}

要在 Mac 上无需管理员权限运行 Docker Desktop，需通过命令行安装并传递 `—user=<userid>` 安装程序标志：

```console
$ /Applications/Docker.app/Contents/MacOS/install --user=<userid>
```

然后使用指定的用户 ID 登录机器并启动 Docker Desktop。

> [!NOTE]
>
> 启动 Docker Desktop 之前，如果 `~/Library/Group Containers/group.com.docker/` 目录中已存在 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`），您会看到 **Finish setting up Docker Desktop** 窗口，选择 **Finish** 时会提示输入管理员权限。为避免此情况，请确保在启动应用前删除之前安装留下的 `settings-store.json` 文件（或 Docker Desktop 4.34 及更早版本的 `settings.json`）。

{{< /tab >}}
{{< tab name="Windows" >}}

> [!NOTE]
>
> 如果您使用 WSL 2 后端，请首先确保满足 WSL 2 的[最低版本要求](/manuals/desktop/features/wsl/best-practices.md)。否则，请先更新 WSL 2。

要在 Windows 上无需管理员权限运行 Docker Desktop，需通过命令行安装并传递 `—always-run-service` 安装程序标志。

```console
$ "Docker Desktop Installer.exe" install —always-run-service
```

{{< /tab >}}
{{< /tabs >}}


