---
title: 使用 IPv6 网络
weight: 20
description: 如何在 Docker 守护进程中启用 IPv6 支持
keywords: 守护进程, 网络, 网络配置, ipv6
aliases:
- /engine/userguide/networking/default_network/ipv6/
- /config/daemon/ipv6/
---

IPv6 仅在 Linux 主机上运行的 Docker 守护进程中受支持。

## 创建 IPv6 网络

- 使用 `docker network create`：

  ```console
  $ docker network create --ipv6 ip6net
  ```

- 使用 `docker network create`，指定 IPv6 子网：

  ```console
  $ docker network create --ipv6 --subnet 2001:db8::/64 ip6net
  ```

- 使用 Docker Compose 文件：

  ```yaml
   networks:
     ip6net:
       enable_ipv6: true
       ipam:
         config:
           - subnet: 2001:db8::/64
  ```

现在你可以运行连接到 `ip6net` 网络的容器。

```console
$ docker run --rm --network ip6net -p 80:80 traefik/whoami
```

这会在 IPv6 和 IPv4 上都发布端口 80。你可以通过 curl 连接到 IPv6 环回地址的端口 80 来验证 IPv6 连接：

```console
$ curl http://[::1]:80
Hostname: ea1cfde18196
IP: 127.0.0.1
IP: ::1
IP: 172.17.0.2
IP: 2001:db8::2
IP: fe80::42:acff:fe11:2
RemoteAddr: [2001:db8::1]:37574
GET / HTTP/1.1
Host: [::1]
User-Agent: curl/8.1.2
Accept: */*
```

## 在默认桥接网络上使用 IPv6

以下步骤展示如何在默认桥接网络上使用 IPv6。

1. 编辑 Docker 守护进程配置文件，位于 `/etc/docker/daemon.json`。配置以下参数：

   ```json
   {
     "ipv6": true,
     "fixed-cidr-v6": "2001:db8:1::/64"
   }
   ```

   - `ipv6` 在默认网络上启用 IPv6 网络。
   - `fixed-cidr-v6` 为默认桥接网络分配子网，启用动态 IPv6 地址分配。
   - `ip6tables` 启用额外的 IPv6 数据包过滤规则，提供网络隔离和端口映射。默认启用，但可以禁用。

2. 保存配置文件。
3. 重启 Docker 守护进程使更改生效。

   ```console
   $ sudo systemctl restart docker
   ```

现在你可以在默认桥接网络上运行容器。

```console
$ docker run --rm -p 80:80 traefik/whoami
```

这会在 IPv6 和 IPv4 上都发布端口 80。你可以通过向 IPv6 环回地址的端口 80 发起请求来验证 IPv6 连接：

```console
$ curl http://[::1]:80
Hostname: ea1cfde18196
IP: 127.0.0.1
IP: ::1
IP: 172.17.0.2
IP: 2001:db8:1::242:ac12:2
IP: fe80::42:acff:fe12:2
RemoteAddr: [2001:db8:1::1]:35558
GET / HTTP/1.1
Host: [::1]
User-Agent: curl/8.1.2
Accept: */*
```

## 动态 IPv6 子网分配

如果你没有显式配置用户定义网络的子网（使用 `docker network create --subnet=<your-subnet>`），这些网络将使用守护进程的默认地址池作为后备。这也适用于在 Docker Compose 文件中创建的网络，其中 `enable_ipv6` 设置为 `true`。

如果 Docker Engine 的 `default-address-pools` 中不包含任何 IPv6 地址池，且没有提供 `--subnet` 选项，启用 IPv6 时将使用 [唯一本地地址 (ULA)][wikipedia-ipv6-ula]。这些 `/64` 子网包含一个基于 Docker Engine 随机生成 ID 的 40 位全局 ID，以提供高度的唯一性概率。

内置的默认地址池配置在 [子网分配](../network/_index.md#subnet-allocation) 中显示。它不包含任何 IPv6 地址池。

要使用不同的 IPv6 子网池进行动态地址分配，你必须手动配置守护进程的地址池，包括：

- 默认的 IPv4 地址池
- 一个或多个你自己的 IPv6 地址池

以下示例显示了一个包含 IPv4 和 IPv6 地址池的有效配置，两个池都提供 256 个子网。IPv4 子网的前缀长度为 `/24`，从 `/16` 池中分配。IPv6 子网的前缀长度为 `/64`，从 `/56` 池中分配。

```json
{
  "default-address-pools": [
    { "base": "172.17.0.0/16", "size": 24 },
    { "base": "2001:db8::/56", "size": 64 }
  ]
}
```

> [!NOTE]
>
> 此示例中的地址 `2001:db8::` 在 [文档保留地址][wikipedia-ipv6-reserved] 中。请将其替换为有效的 IPv6 网络。
>
> 默认的 IPv4 地址池来自私有地址范围，类似于默认的 IPv6 [ULA][wikipedia-ipv6-ula] 网络。

有关 `default-address-pools` 的更多信息，请参阅 [子网分配](../network/_index.md#subnet-allocation)。

[wikipedia-ipv6-reserved]: https://en.wikipedia.org/wiki/Reserved_IP_addresses#IPv6
[wikipedia-ipv6-ula]: https://en.wikipedia.org/wiki/Unique_local_address

## Docker in Docker

在使用 `xtables`（旧版 `iptables`）而非 `nftables` 的主机上，必须在创建 IPv6 Docker 网络之前加载内核模块 `ip6_tables`。它通常在 Docker 启动时自动加载。

但是，如果你在 Docker in Docker 中运行，且不是基于最新版本的 [官方 `docker` 镜像](https://hub.docker.com/_/docker)，你可能需要在主机上运行 `modprobe ip6_tables`。或者，使用守护进程选项 `--ip6tables=false` 禁用容器化 Docker 引擎的 `ip6tables`。

## 下一步

- [网络概述](/manuals/engine/network/_index.md)
