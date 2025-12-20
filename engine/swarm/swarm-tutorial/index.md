# Swarm 模式入门

本教程向您介绍 Docker Engine Swarm 模式的各项功能。在开始之前，您可能需要先熟悉[关键概念](../key-concepts.md)。

本教程将指导您完成以下操作：

* 在 swarm 模式下初始化 Docker Engine 集群
* 将节点添加到 swarm
* 将应用程序服务部署到 swarm
* 在一切运行后管理 swarm

本教程使用在终端窗口命令行中输入的 Docker Engine CLI 命令。

如果您是 Docker 的新手，请参阅[关于 Docker Engine](../../_index.md)。

## 设置

要运行本教程，您需要：

* [三台可以通过网络通信并安装了 Docker 的 Linux 主机](#三台联网主机)
* [管理节点的 IP 地址](#管理节点的-ip-地址)
* [主机之间的开放端口](#主机之间的开放协议和端口)

### 三台联网主机

本教程需要三台安装了 Docker 并且可以通过网络通信的 Linux 主机。这些可以是物理机、虚拟机、Amazon EC2 实例，或以其他方式托管的主机。请查看[部署到 Swarm](/guides/swarm-deploy.md#prerequisites) 了解一种可能的主机设置方案。

其中一台机器是管理节点（称为 `manager1`），另外两台是工作节点（`worker1` 和 `worker2`）。

> [!NOTE]
>
> 您也可以遵循本教程的许多步骤来测试单节点 swarm，在这种情况下，您只需要一台主机。多节点命令将不起作用，但您可以初始化 swarm、创建服务并对其进行扩展。

#### 在 Linux 机器上安装 Docker Engine

如果您使用基于 Linux 的物理计算机或云提供的计算机作为主机，只需按照您平台的 [Linux 安装说明](../../install/_index.md) 操作即可。启动这三台机器，您就准备就绪了。您可以在 Linux 机器上测试单节点和多节点 swarm 场景。

### 管理节点的 IP 地址

IP 地址必须分配给主机操作系统可用的网络接口。swarm 中的所有节点都需要通过该 IP 地址连接到管理节点。

因为其他节点通过其 IP 地址联系管理节点，所以您应该使用固定的 IP 地址。

您可以在 Linux 或 macOS 上运行 `ifconfig` 来查看可用网络接口的列表。

本教程使用 `manager1` : `192.168.99.100`。

### 主机之间的开放协议和端口

以下端口必须可用。在某些系统上，这些端口默认是开放的。

* 端口 `2377` TCP，用于管理节点之间以及与管理节点的通信
* 端口 `7946` TCP/UDP，用于覆盖网络节点发现
* 端口 `4789` UDP（可配置），用于覆盖网络流量

如果您计划创建带有加密的覆盖网络（`--opt encrypted`），您还需要确保允许 IP 协议 50 (IPSec ESP) 流量。

端口 `4789` 是 Swarm 数据路径端口的默认值，也称为 VXLAN 端口。防止任何不受信任的流量到达此端口非常重要，因为 VXLAN 不提供身份验证。此端口应只对受信任的网络开放，切勿在边界防火墙处开放。

如果 Swarm 流量经过的网络不完全受信任，强烈建议使用加密的覆盖网络。如果只使用加密覆盖网络，建议采取一些额外的加固措施：

* [自定义默认入口网络](../networking.md) 以使用加密
* 仅在数据路径端口上接受加密数据包：

```bash
# iptables 规则示例（顺序和其他工具可能需要自定义）
iptables -I INPUT -m udp --dport 4789 -m policy --dir in --pol none -j DROP
```

## 下一步

接下来，您将创建一个 swarm。


<a class="button not-prose" href="https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/">创建 swarm</a>


- [创建 swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/)

- [向 swarm 添加节点](https://docs.docker.com/engine/swarm/swarm-tutorial/add-nodes/)

- [将服务部署到 swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/deploy-service/)

- [在 swarm 上检查服务](https://docs.docker.com/engine/swarm/swarm-tutorial/inspect-service/)

- [扩展 Swarm 中的服务](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/)

- [删除在 swarm 上运行的服务](https://docs.docker.com/engine/swarm/swarm-tutorial/delete-service/)

- [对服务应用滚动更新](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/)

- [将 swarm 中的节点设置为排空状态](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/)

