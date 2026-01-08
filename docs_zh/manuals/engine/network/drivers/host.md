---
title: Host 网络驱动
description: 关于在 Docker 主机网络上暴露容器的全部内容
keywords: network, host, standalone, host mode networking
aliases:
- /network/host/
- /network/drivers/host/
- /engine/network/tutorials/host/
---

如果你为容器使用 `host` 网络模式，该容器的网络栈不会与 Docker 主机隔离（容器共享主机的网络命名空间），并且容器不会获得自己分配的 IP 地址。例如，如果你运行一个绑定到端口 80 的容器，并使用 `host` 网络，那么容器的应用程序在主机 IP 地址的端口 80 上可用。

> [!NOTE]
>
> 由于使用 `host` 模式网络时容器没有自己的 IP 地址，[端口映射](overlay.md#publish-ports) 不会生效，`-p`、`--publish`、`-P` 和 `--publish-all` 选项会被忽略，并产生警告：
>
> ```console
> WARNING: Published ports are discarded when using host network mode
> ```

Host 模式网络在以下用例中可能很有用：

- 为了优化性能
- 在容器需要处理大量端口的情况下

这是因为不需要网络地址转换（NAT），并且不会为每个端口创建“用户空间代理”。

## 平台支持

Host 网络驱动支持以下平台：

- Linux 上的 Docker Engine
- Docker Desktop 4.34 及更高版本（需要在设置中启用该功能）

> [!NOTE]
> 对于 Docker Desktop 用户，请参阅下面的 [Docker Desktop 部分](#docker-desktop) 了解设置说明。

你也可以为 Swarm 服务使用 `host` 网络，方法是向 `docker service create` 命令传递 `--network host`。在这种情况下，控制流量（与管理 Swarm 和服务相关的流量）仍然通过覆盖网络发送，但各个 Swarm 服务容器使用 Docker 守护进程的主机网络和端口发送数据。这会创建一些额外的限制。例如，如果服务容器绑定到端口 80，则在给定的 Swarm 节点上只能运行一个服务容器。

## Docker Desktop

Host 网络支持在 Docker Desktop 4.34 及更高版本中。要启用此功能：

1. 在 Docker Desktop 中登录你的 Docker 账户。
2. 导航到 **Settings**。
3. 在 **Resources** 选项卡下，选择 **Network**。
4. 勾选 **Enable host networking** 选项。
5. 选择 **Apply and restart**。

此功能在两个方向上都有效。这意味着你可以从主机访问在容器中运行的服务器，也可以从任何启用 host 网络启动的容器中访问在主机上运行的服务器。TCP 和 UDP 都支持作为通信协议。

### 示例

以下命令在容器中启动 netcat，监听端口 `8000`：

```console
$ docker run --rm -it --net=host nicolaka/netshoot nc -lkv 0.0.0.0 8000
```

然后端口 `8000` 将在主机上可用，你可以从另一个终端使用以下命令连接：

```console
$ nc localhost 8000
```

你在这里键入的内容将出现在运行容器的终端上。

要从容器访问主机上运行的服务，你可以使用以下命令启动一个启用 host 网络的容器：

```console
$ docker run --rm -it --net=host nicolaka/netshoot
```

然后，如果你想从容器访问主机上运行的服务（在此示例中，端口 `80` 上运行的 Web 服务器），可以这样做：

```console
$ nc localhost 80
```

### 限制

- 容器内的进程无法绑定到主机的 IP 地址，因为容器无法直接访问主机的接口。
- Docker Desktop 的主机网络功能在第 4 层工作。这意味着与 Linux 上的 Docker 不同，低于 TCP 或 UDP 的网络协议不受支持。
- 此功能在启用增强容器隔离时不起作用，因为将容器与主机隔离并允许它们访问主机网络是矛盾的。
- 仅支持 Linux 容器。Host 网络不适用于 Windows 容器。

## 使用示例

此示例展示如何启动一个直接绑定到 Docker 主机端口 80 的 Nginx 容器。从网络角度来看，这提供了与 Nginx 直接在主机上运行相同的隔离级别，但容器在所有其他方面保持隔离（存储、进程命名空间、用户命名空间）。

### 前提条件

- Docker 主机上的端口 80 必须可用。要让 Nginx 监听不同端口，请参阅 [Nginx 镜像文档](https://hub.docker.com/_/nginx/)。
- 主机网络驱动仅在 Linux 主机上工作，以及作为 Docker Desktop 4.34 及更高版本中的选择加入功能。

### 步骤

1. 创建并启动容器作为分离进程。`--rm` 选项在容器退出时移除容器。`-d` 标志在后台启动它：

   ```console
   $ docker run --rm -d --network host --name my_nginx nginx
   ```

2. 通过浏览到 [http://localhost:80/](http://localhost:80/) 访问 Nginx。

3. 检查你的网络栈：

   检查所有网络接口并验证没有创建新接口：

   ```console
   $ ip addr show
   ```

   使用 `netstat` 验证哪个进程绑定到端口 80。你需要 `sudo`，因为进程由 Docker 守护进程用户拥有：

   ```console
   $ sudo netstat -tulpn | grep :80
   ```

4. 停止容器。由于 `--rm` 选项，它会自动移除：

   ```console
   $ docker container stop my_nginx
   ```

## 下一步

- 了解 [从容器角度的网络](../_index.md)
- 了解 [桥接网络](./bridge.md)
- 了解 [覆盖网络](./overlay.md)
- 了解 [Macvlan 网络](./macvlan.md)