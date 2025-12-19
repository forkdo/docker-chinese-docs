---
description: 了解如何在 Docker Desktop 中连接容器到主机、跨容器连接，或通过代理和 VPN 进行连接。
keywords: docker desktop, networking, vpn, proxy, port mapping, dns
title: 探索 Docker Desktop 上的网络操作指南
linkTitle: 操作指南
aliases:
- /desktop/linux/networking/
- /docker-for-mac/networking/
- /mackit/networking/
- /desktop/mac/networking/
- /docker-for-win/networking/
- /docker-for-windows/networking/
- /desktop/windows/networking/
- /desktop/networking/
---

本页介绍如何配置和使用网络功能、将容器连接到主机服务、在代理或 VPN 后工作以及排查常见问题。

有关 Docker Desktop 如何在容器、虚拟机和主机之间路由网络流量和文件 I/O 的详细信息，请参阅 [网络概述](/manuals/desktop/features/networking/index.md#overview)。

## 核心网络操作指南

### 将容器连接到主机上的服务

主机具有变化的 IP 地址，或者如果您没有网络访问权限则没有 IP 地址。要连接到主机上运行的服务，请使用特殊的 DNS 名称：

| 名称                      | 描述                                       |
| ------------------------- | ------------------------------------------ |
| `host.docker.internal`    | 解析为主机的内部 IP 地址                   |
| `gateway.docker.internal` | 解析为 Docker 虚拟机的网关 IP              |

#### 示例

在端口 `8000` 上运行一个简单的 HTTP 服务器：

```console
$ python -m http.server 8000
```

然后运行一个容器，安装 `curl`，并尝试使用以下命令连接到主机：

```console
$ docker run --rm -it alpine sh
# apk add curl
# curl http://host.docker.internal:8000
# exit
```

### 从主机连接到容器

要从主机或本地网络访问容器化服务，请使用 `-p` 或 `--publish` 标志发布端口。例如：

```console
$ docker run -d -p 80:80 --name webserver nginx
```

Docker Desktop 使容器中端口 `80` 上运行的任何内容（在本例中为 `nginx`）在 `localhost` 的端口 `80` 上可用。

> [!TIP]
>
> `-p` 的语法是 `HOST_PORT:CLIENT_PORT`。

要发布所有端口，请使用 `-P` 标志。例如，以下命令启动一个容器（在分离模式下），`-P` 标志将容器的所有暴露端口发布到主机上的随机端口。

```console
$ docker run -d -P --name webserver nginx
```

或者，您也可以使用 [主机网络](/manuals/engine/network/drivers/host.md#docker-desktop) 让容器直接访问主机的网络堆栈。

有关与 `docker run` 一起使用的发布选项的更多详细信息，请参阅 [run 命令](/reference/cli/docker/container/run.md)。

所有入站连接都通过 Docker Desktop 后端进程（Mac 上的 `com.docker.backend`，Windows 上的 `com.docker.backend`，或 Linux 上的 `qemu`），该进程处理到虚拟机的端口转发。有关更多详细信息，请参阅 [暴露端口的工作原理](/manuals/desktop/features/networking/index.md#how-exposed-ports-work)。

### 使用 VPN

Docker Desktop 网络在连接到 VPN 时可以工作。

为此，Docker Desktop 会拦截来自容器的流量，并将其注入到主机中，就像它源自 Docker 应用程序一样。

有关此流量如何出现在主机防火墙和端点检测系统中的详细信息，请参阅 [防火墙和端点可见性](/manuals/desktop/features/networking/index.md#firewalls-and-endpoint-visibility.md)。

### 使用代理

Docker Desktop 可以使用系统代理或手动配置。
要配置代理：

1. 导航到 **设置** 中的 **资源** 选项卡。
2. 从下拉菜单中选择 **代理**。
3. 打开 **手动代理配置** 切换开关。
4. 输入您的 HTTP、HTTPS 或 SOCKS5 代理 URL。

有关代理和代理配置的更多详细信息，请参阅 [代理设置文档](/manuals/desktop/settings-and-maintenance/settings.md#proxies)。

## Mac 和 Windows 的网络操作指南

使用 Docker Desktop 4.42 及更高版本，您可以控制 Docker 如何处理容器网络和 DNS 解析，以更好地支持各种环境——从仅 IPv4 到双栈和仅 IPv6 系统。这些设置有助于防止因不兼容或配置错误的主机网络导致的超时和连接问题。

您可以在 Docker Desktop 仪表板设置的 **网络** 选项卡上设置以下设置，或者如果您是管理员，可以通过 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#networking) 或 [管理控制台](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 使用设置管理。

> [!NOTE]
>
> 这些设置可以使用 CLI 标志或 Compose 文件选项针对每个网络进行覆盖。

### 默认网络模式

选择 Docker 创建新网络时使用的默认 IP 协议。这允许您使 Docker 与主机的网络功能或组织要求（例如强制执行仅 IPv6 访问）保持一致。

| 模式                           | 描述                                       |
| ------------------------------ | ------------------------------------------ |
| **双 IPv4/IPv6（默认）**       | 同时支持 IPv4 和 IPv6。最灵活。            |
| **仅 IPv4**                    | 仅使用 IPv4 寻址。                         |
| **仅 IPv6**                    | 仅使用 IPv6 寻址。                         |

### DNS 解析行为

控制 Docker 如何过滤返回给容器的 DNS 记录，提高仅支持 IPv4 或 IPv6 的环境中的可靠性。此设置对于防止应用程序尝试使用实际上不可用的 IP 族进行连接特别有用，这可能导致可避免的延迟或失败。

| 选项                           | 描述                                                             |
| ------------------------------ | ---------------------------------------------------------------- |
| **自动（推荐）**               | 自动过滤不受支持的记录类型。（IPv4 为 A，IPv6 为 AAAA）          |
| **过滤 IPv4（A 记录）**        | 阻止 IPv4 查找。仅在双栈模式下可用。                             |
| **过滤 IPv6（AAAA 记录）**     | 阻止 IPv6 查找。仅在双栈模式下可用。                             |
| **不过滤**                     | 返回 A 和 AAAA 记录。                                            |

> [!IMPORTANT]
>
> 切换默认网络模式会将 DNS 过滤器重置为自动。

## Mac 和 Linux 的网络操作指南

### SSH 代理转发

Docker Desktop for Mac 和 Linux 允许您在容器内使用主机的 SSH 代理。为此：

1. 通过将以下参数添加到您的 `docker run` 命令中来绑定挂载 SSH 代理套接字：

   ```console
   $--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock
   ```

2. 在容器中添加 `SSH_AUTH_SOCK` 环境变量：

    ```console
    $ -e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock"
    ```

要在 Docker Compose 中启用 SSH 代理，请将以下标志添加到您的服务中：

 ```yaml
services:
  web:
    image: nginx:alpine
    volumes:
      - type: bind
        source: /run/host-services/ssh-auth.sock
        target: /run/host-services/ssh-auth.sock
    environment:
      - SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock
 ```

## 已知限制

### 更改内部 IP 地址

Docker 使用的内部 IP 地址可以从 **设置** 中更改。更改 IP 后，您需要重置 Kubernetes 集群并离开任何活动的 Swarm。

### 主机上没有 `docker0` 网桥

由于 Docker Desktop 中网络的实现方式，您无法在主机上看到 `docker0` 接口。此接口实际上位于虚拟机内部。

### 我无法 ping 我的容器

Docker Desktop 无法将流量路由到 Linux 容器。但是，如果您是 Windows 用户，则可以 ping Windows 容器。

### 无法为每个容器分配 IP 地址

这是因为 Docker `bridge` 网络无法从主机访问。但是，如果您是 Windows 用户，则对于 Windows 容器，可以为每个容器分配 IP 地址。