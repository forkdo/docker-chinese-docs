---
description: Docker Engine Swarm 模式入门教程
keywords: 教程, 集群管理, Swarm 模式, Docker Engine, 入门
title: Docker Engine Swarm 模式入门
toc_max: 4
---

本教程向您介绍 Docker Engine Swarm 模式的功能。在开始之前，您可能需要先熟悉一下 [核心概念](../key-concepts.md)。

本教程将引导您完成以下操作：

* 初始化 Docker Engine 集群（Swarm 模式）
* 向 Swarm 添加节点
* 向 Swarm 部署应用服务
* 管理已运行的 Swarm

本教程使用在终端窗口命令行中输入的 Docker Engine CLI 命令。

如果您是 Docker 新手，请参阅 [Docker Engine 简介](../../_index.md)。

## 准备工作

运行本教程，您需要：

* [三台可通过网络通信并已安装 Docker 的 Linux 主机](#三台可通过网络通信的-linux-主机)
* [管理节点的 IP 地址](#管理节点的-ip-地址)
* [主机之间开放的协议和端口](#主机之间开放的协议和端口)

### 三台可通过网络通信的 Linux 主机

本教程需要三台已安装 Docker 并可通过网络通信的 Linux 主机。这些可以是物理机、虚拟机、Amazon EC2 实例，或以其他方式托管。请查看 [部署到 Swarm](/guides/swarm-deploy.md#先决条件) 了解主机设置的可能方案。

这些主机中，一台是管理节点（称为 `manager1`），两台是工作节点（`worker1` 和 `worker2`）。

> [!NOTE]
>
> 您也可以按照许多教程步骤测试单节点 Swarm，此时您只需要一台主机。多节点命令无法工作，但您仍然可以初始化 Swarm、创建服务并进行扩展。

#### 在 Linux 主机上安装 Docker Engine

如果您使用基于 Linux 的物理计算机或云提供的计算机作为主机，只需按照您平台的 [Linux 安装说明](../../install/_index.md) 操作即可。启动三台机器，您就准备好了。您可以在 Linux 机器上测试单节点和多节点 Swarm 场景。

### 管理节点的 IP 地址

IP 地址必须分配给主机操作系统可用的网络接口。Swarm 中的所有节点都需要通过该 IP 地址连接到管理节点。

由于其他节点通过 IP 地址联系管理节点，您应使用固定的 IP 地址。

您可以在 Linux 或 macOS 上运行 `ifconfig` 查看可用网络接口列表。

本教程使用 `manager1` : `192.168.99.100`。

### 主机之间开放的协议和端口

以下端口必须可用。在某些系统上，这些端口默认是开放的。

* 端口 `2377` TCP 用于管理节点之间的通信
* 端口 `7946` TCP/UDP 用于覆盖网络节点发现
* 端口 `4789` UDP（可配置）用于覆盖网络流量

如果您计划创建带加密的覆盖网络（`--opt encrypted`），还需要确保允许 IP 协议 50（IPSec ESP）流量。

端口 `4789` 是 Swarm 数据路径端口的默认值，也称为 VXLAN 端口。防止不受信任的流量到达此端口非常重要，因为 VXLAN 不提供身份验证。此端口应仅对受信任的网络开放，永远不应在边界防火墙上开放。

如果 Swarm 流量穿过的网络不是完全受信任的，强烈建议使用加密覆盖网络。如果仅使用加密覆盖网络，建议进行一些额外的加固：

* [自定义默认入口网络](../networking.md) 以使用加密
* 仅接受数据路径端口上的加密数据包：

```bash
# 示例 iptables 规则（顺序和其他工具可能需要自定义）
iptables -I INPUT -m udp --dport 4789 -m policy --dir in --pol none -j DROP
```

## 后续步骤

接下来，您将创建一个 Swarm。

{{< button text="创建 Swarm" url="create-swarm.md" >}}
