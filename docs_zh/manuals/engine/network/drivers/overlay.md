---
title: 覆盖网络驱动
description: 关于使用覆盖网络的全部内容
keywords: 网络, 覆盖, 用户自定义, swarm, 服务
aliases:
  - /config/containers/overlay/
  - /engine/userguide/networking/overlay-security-model/
  - /network/overlay/
  - /network/drivers/overlay/
  - /engine/network/tutorials/overlay/
  - /engine/userguide/networking/get-started-overlay/
---

`overlay` 网络驱动在多个 Docker 守护进程主机之间创建分布式网络。此网络位于（覆盖于）主机特定网络之上，允许连接到它的容器在启用加密时安全通信。Docker 会透明地处理每个数据包到正确 Docker 守护进程主机和正确目标容器的路由。

您可以使用 `docker network create` 创建用户自定义 `overlay` 网络，就像创建用户自定义 `bridge` 网络一样。服务或容器可以同时连接到多个网络。服务或容器只能在它们都连接的网络之间通信。

覆盖网络通常用于在 Swarm 服务之间创建连接，但您也可以使用它来连接运行在不同主机上的独立容器。使用独立容器时，仍然需要使用 Swarm 模式在主机之间建立连接。

本页描述了覆盖网络的一般用法，以及与独立容器一起使用时的情况。有关 Swarm 服务覆盖的信息，请参阅 [管理 Swarm 服务网络](/manuals/engine/swarm/networking.md)。

## 要求

Docker 主机必须是 Swarm 的一部分才能使用覆盖网络，即使在连接独立容器时也是如此。以下端口必须在参与的主机之间打开：

- `2377/tcp`：Swarm 控制平面（可配置）
- `4789/udp`：覆盖流量（可配置）
- `7946/tcp` 和 `7946/udp`：节点通信（不可配置）

## 创建覆盖网络

下表列出了参与覆盖网络的每个主机需要打开的端口：

| 端口                   | 描述                                                                                                                                                     |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `2377/tcp`             | 默认 Swarm 控制平面端口，可通过 [`docker swarm join --listen-addr`](/reference/cli/docker/swarm/join.md#--listen-addr-value) 配置                       |
| `4789/udp`             | 默认覆盖流量端口，可通过 [`docker swarm init --data-path-addr`](/reference/cli/docker/swarm/init.md#data-path-port) 配置                                 |
| `7946/tcp`, `7946/udp` | 用于节点间通信，不可配置                                                                                                                                  |

要创建独立容器可以连接的覆盖网络，请运行以下命令：

```console
$ docker network create -d overlay --attachable my-attachable-overlay
```

`--attachable` 选项允许独立容器和 Swarm 服务都连接到覆盖网络。没有 `--attachable` 时，只有 Swarm 服务可以连接到网络。

您可以指定 IP 地址范围、子网、网关和其他选项。详情请参阅 `docker network create --help`。

## 加密覆盖网络上的流量

使用 `--opt encrypted` 标志加密通过覆盖网络传输的应用数据：

```console
$ docker network create \
  --opt encrypted \
  --driver overlay \
  --attachable \
  my-attachable-multi-host-network
```

这在虚拟可扩展局域网 (VXLAN) 级别启用 IPsec 加密。此加密会带来不可忽视的性能开销，因此在生产环境中使用此选项之前应先进行测试。

> [!WARNING]
>
> 不要将 Windows 容器连接到加密的覆盖网络。
>
> Windows 不支持覆盖网络加密。当 Windows 主机尝试连接到加密覆盖网络时，Swarm 不会报告错误，
> 但网络对 Windows 容器的影响如下：
>
> - Windows 容器无法与网络上的 Linux 容器通信
> - 网络上 Windows 容器之间的数据流量未加密

## 将容器连接到覆盖网络

将容器添加到覆盖网络使它们能够与其他容器通信，而无需在各个 Docker 守护进程主机上设置路由。前提是主机已加入同一个 Swarm。

要将名为 `multi-host-network` 的覆盖网络与 `busybox` 容器连接：

```console
$ docker run --network multi-host-network busybox sh
```

> [!NOTE]
>
> 这仅在覆盖网络是可连接的（使用 `--attachable` 标志创建）时才有效。

## 容器发现

在覆盖网络上发布容器端口会向网络上的其他容器打开这些端口。可以通过使用容器名称进行 DNS 查找来发现容器。

| 标志值                      | 描述                                                                                                                                                 |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | 将容器中的 TCP 端口 80 映射到覆盖网络上的端口 `8080`。                                                                                             |
| `-p 8080:80/udp`                | 将容器中的 UDP 端口 80 映射到覆盖网络上的端口 `8080`。                                                                                             |
| `-p 8080:80/sctp`               | 将容器中的 SCTP 端口 80 映射到覆盖网络上的端口 `8080`。                                                                                            |
| `-p 8080:80/tcp -p 8080:80/udp` | 将容器中的 TCP 端口 80 映射到覆盖网络上的 TCP 端口 `8080`，并将容器中的 UDP 端口 80 映射到覆盖网络上的 UDP 端口 `8080`。 |

## 覆盖网络的连接限制

由于 Linux 内核的限制，当 1000 个容器共存于同一主机时，覆盖网络会变得不稳定，容器间通信可能中断。

有关此限制的更多信息，请参阅
[moby/moby#44973](https://github.com/moby/moby/issues/44973#issuecomment-1543747718)。

## 使用示例

本节提供使用覆盖网络的实际示例。这些示例涵盖多 Docker 主机上的 Swarm 服务和独立容器。

### 前提条件

所有示例至少需要一个单节点 Swarm。通过在主机上运行 `docker swarm init` 来初始化一个。您也可以在多节点 Swarm 上运行这些示例。

### 使用默认覆盖网络

此示例展示默认覆盖网络如何与 Swarm 服务一起工作。您将创建一个 `nginx` 服务并从服务容器的角度检查网络。

#### 多节点设置的先决条件

此演练需要三台 Docker 主机，它们可以通过同一网络相互通信，且主机间无防火墙阻止流量：

- `manager`：同时作为管理器和工作节点
- `worker-1`：仅作为工作节点
- `worker-2`：仅作为工作节点

如果您没有三台主机，可以在云提供商上设置三台安装了 Docker 的虚拟机。

#### 创建 Swarm

1. 在 `manager` 上初始化 Swarm。如果主机只有一个网络接口，`--advertise-addr` 标志是可选的：

   ```console
   $ docker swarm init --advertise-addr=<MANAGER-IP-ADDRESS>
   ```

   保存显示的加入令牌以供工作节点使用。

2. 在 `worker-1` 上加入 Swarm：

   ```console
   $ docker swarm join --token <TOKEN> \
     --advertise-addr <WORKER-1-IP-ADDRESS> \
     <MANAGER-IP-ADDRESS>:2377
   ```

3. 在 `worker-2` 上加入 Swarm：

   ```console
   $ docker swarm join --token <TOKEN> \
     --advertise-addr <WORKER-2-IP-ADDRESS> \
     <MANAGER-IP-ADDRESS>:2377
   ```

4. 在 `manager` 上列出所有节点：

   ```console
   $ docker node ls

   ID                            HOSTNAME            STATUS              AVAILABILITY        MANAGER STATUS
   d68ace5iraw6whp7llvgjpu48 *   ip-172-31-34-146    Ready               Active              Leader
   nvp5rwavvb8lhdggo8fcf7plg     ip-172-31-35-151    Ready               Active
   ouvx2l7qfcxisoyms8mtkgahw     ip-172-31-36-89     Ready               Active
   ```

   如有必要，按角色过滤：

   ```console
   $ docker node ls --filter role=manager
   $ docker node ls --filter role=worker
   ```

5. 在所有主机上列出 Docker 网络。每台主机现在都有一个名为 `ingress` 的覆盖网络和一个名为 `docker_gwbridge` 的桥接网络：

   ```console
   $ docker network ls

   NETWORK ID          NAME                DRIVER              SCOPE
   495c570066be        bridge              bridge              local
   961c6cae9945        docker_gwbridge     bridge              local
   ff35ceda3643        host                host                local
   trtnl4tqnc3n        ingress             overlay             swarm
   c8357deec9cb        none                null                local
   ```

`docker_gwbridge` 将 `ingress` 网络连接到 Docker 主机的网络接口。如果您创建服务时未指定网络，它们会连接到 `ingress`。建议为每个应用程序或相关应用程序组使用单独的覆盖网络。

#### 创建服务

1. 在 `manager` 上创建一个新的覆盖网络：

   ```console
   $ docker network create -d overlay nginx-net
   ```

   当工作节点运行需要该网络的服务任务时，覆盖网络会自动在工作节点上创建。

2. 在 `manager` 上创建一个 5 副本的 Nginx 服务，连接到 `nginx-net`：

   > [!NOTE]
   > 服务只能在管理器上创建。

   ```console
   $ docker service create \
     --name my-nginx \
     --publish target=80,published=80 \
     --replicas=5 \
     --network nginx-net \
     nginx
   ```

   默认 `ingress` 发布模式意味着您可以浏览到任何节点的 80 端口并连接到 5 个服务任务之一，即使该节点上没有运行任务。

3. 监控服务创建进度：

   ```console
   $ docker service ls
   ```

4. 在所有主机上检查 `nginx-net` 网络。`Containers` 部分列出了从该主机连接到覆盖网络的所有服务任务。

5. 从 `manager` 检查服务：

   ```console
   $ docker service inspect my-nginx
   ```

   注意有关端口和端点的信息。

6. 创建第二个网络并更新服务以使用它：

   ```console
   $ docker network create -d overlay nginx-net-2
   $ docker service update \
     --network-add nginx-net-2 \
     --network-rm nginx-net \
     my-nginx
   ```

7. 验证更新完成：

   ```console
   $ docker service ls
   ```

   检查两个网络以验证容器从 `nginx-net` 移动到 `nginx-net-2`。

   > [!NOTE]
   > 覆盖网络在 Swarm 工作节点上根据需要自动创建，
   > 但不会自动删除。

8. 清理：

   ```console
   $ docker service rm my-nginx
   $ docker network rm nginx-net nginx-net-2
   ```

### 使用用户自定义覆盖网络

此示例展示了在生产服务中使用自定义覆盖网络的推荐方法。

#### 前提条件

这假设 Swarm 已经设置好，您正在管理器节点上。

#### 步骤

1. 创建用户自定义覆盖网络：

   ```console
   $ docker network create -d overlay my-overlay
   ```

2. 启动使用覆盖网络的服务，将端口 80 发布到端口 8080：

   ```console
   $ docker service create \
     --name my-nginx \
     --network my-overlay \
     --replicas 1 \
     --publish published=8080,target=80 \
     nginx:latest
   ```

3. 验证服务任务连接到网络：

   ```console
   $ docker network inspect my-overlay
   ```

   在 `Containers` 部分查找 `my-nginx` 服务任务。

4. 清理：

   ```console
   $ docker service rm my-nginx
   $ docker network rm my-overlay
   ```

### 对独立容器使用覆盖网络

此示例演示了在不同 Docker 主机上使用覆盖网络的独立容器之间的 DNS 容器发现。

#### 前提条件

您需要两台 Docker 主机，它们可以通过以下端口相互通信：

- TCP 端口 2377
- TCP 和 UDP 端口 7946
- UDP 端口 4789

本示例将主机称作 `host1` 和 `host2`。

#### 步骤

1. 设置 Swarm：

   在 `host1` 上初始化 Swarm：

   ```console
   $ docker swarm init
   Swarm initialized: current node (vz1mm9am11qcmo979tlrlox42) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-5g90q48weqrtqryq4kj6ow0e8xm9wmv9o6vgqc5j320ymybd5c-8ex8j0bc40s6hgvy5ui5gl4gy 172.31.47.252:2377
   ```

   在 `host2` 上使用上一步输出的令牌加入 Swarm：

   ```console
   $ docker swarm join --token <your_token> <your_ip_address>:2377
   This node joined a swarm as a worker.
   ```

   如果加入失败，在 `host2` 上运行 `docker swarm leave --force`，验证网络和防火墙设置，然后重试。

2. 在 `host1` 上创建一个可连接的覆盖网络：

   ```console
   $ docker network create --driver=overlay --attachable test-net
   uqsof8phj3ak0rq9k86zta6ht
   ```

   注意返回的网络 ID。

3. 在 `host1` 上启动一个交互式容器，连接到 `test-net`：

   ```console
   $ docker run -it --name alpine1 --network test-net alpine
   / #
   ```

4. 在 `host2` 上列出可用网络。注意 `test-net` 尚未存在：

   ```console
   $ docker network ls
   NETWORK ID          NAME                DRIVER              SCOPE
   ec299350b504        bridge              bridge              local
   66e77d0d0e9a        docker_gwbridge     bridge              local
   9f6ae26ccb82        host                host                local
   omvdxqrda80z        ingress             overlay             swarm
   b65c952a4b2b        none                null                local
   ```

5. 在 `host2` 上启动一个分离的交互式容器，连接到 `test-net`：

   ```console
   $ docker run -dit --name alpine2 --network test-net alpine
   fb635f5ece59563e7b8b99556f816d24e6949a5f6a5b1fbd92ca244db17a4342
   ```

   > [!NOTE]
   > 自动 DNS 容器发现仅适用于唯一容器名称。

6. 在 `host2` 上验证 `test-net` 已以与 `host1` 相同的网络 ID 创建：

   ```console
   $ docker network ls
   NETWORK ID          NAME                DRIVER              SCOPE
   ...
   uqsof8phj3ak        test-net            overlay             swarm
   ```

7. 在 `host1` 上从 `alpine1` ping `alpine2`：

   ```console
   / # ping -c 2 alpine2
   PING alpine2 (10.0.0.5): 56 data bytes
   64 bytes from 10.0.0.5: seq=0 ttl=64 time=0.600 ms
   64 bytes from 10.0.0.5: seq=1 ttl=64 time=0.555 ms

   --- alpine2 ping statistics ---
   2 packets transmitted, 2 packets received, 0% packet loss
   round-trip min/avg/max = 0.555/0.577/0.600 ms
   ```

   两个容器通过连接两台主机的覆盖网络通信。您也可以在 `host2` 上运行另一个容器并 ping `alpine1`：

   ```console
   $ docker run -it --rm --name alpine3 --network test-net alpine
   / # ping -c 2 alpine1
   / # exit
   ```

8. 在 `host1` 上关闭 `alpine1` 会话（这会停止容器）：

   ```console
   / # exit
   ```

9. 清理。您必须在每个主机上独立停止和删除容器：

   在 `host2` 上：

   ```console
   $ docker container stop alpine2
   $ docker network ls
   $ docker container rm alpine2
   ```

   当您停止 `alpine2` 时，`test-net` 会从 `host2` 上消失。

   在 `host1` 上：

