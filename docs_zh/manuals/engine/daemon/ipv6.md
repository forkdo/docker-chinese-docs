---
title: 使用 IPv6 网络
weight: 20
description: 如何在 Docker 守护进程中启用 IPv6 支持
keywords: daemon, network, networking, ipv6
aliases:
- /engine/userguide/networking/default_network/ipv6/
- /config/daemon/ipv6/
---

IPv6 仅支持运行在 Linux 主机上的 Docker 守护进程。

## 创建 IPv6 网络

- 使用 `docker network create`：

  ```console
  $ docker network create --ipv6 ip6net
  ```

- 使用 `docker network create`，并指定 IPv6 子网：

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

现在，您可以运行连接到 `ip6net` 网络的容器。

```console
$ docker run --rm --network ip6net -p 80:80 traefik/whoami
```

这将在 IPv6 和 IPv4 上同时发布端口 80。
您可以通过运行 curl 来验证 IPv6 连接，
连接到 IPv6 回环地址的端口 80：

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

## 为默认桥接网络使用 IPv6

以下步骤向您展示如何在默认桥接网络上使用 IPv6。

1. 编辑位于 `/etc/docker/daemon.json` 的 Docker 守护进程配置文件。配置以下参数：

   ```json
   {
     "ipv6": true,
     "fixed-cidr-v6": "2001:db8:1::/64"
   }
   ```

   - `ipv6` 在默认网络上启用 IPv6 网络。
   - `fixed-cidr-v6` 为默认桥接网络分配一个子网，
     启用动态 IPv6 地址分配。
   - `ip6tables` 启用额外的 IPv6 数据包过滤规则，提供网络
     隔离和端口映射。默认情况下启用，但可以禁用。

2. 保存配置文件。
3. 重启 Docker 守护进程以使更改生效。

   ```console
   $ sudo systemctl restart docker
   ```

现在，您可以在默认桥接网络上运行容器。

```console
$ docker run --rm -p 80:80 traefik/whoami
```

这将在 IPv6 和 IPv4 上同时发布端口 80。
您可以通过向 IPv6 回环地址的端口 80 发出请求来验证 IPv6 连接：

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

如果您没有使用 `docker network create --subnet=<your-subnet>` 为用户定义的网络显式配置子网，
这些网络将使用守护进程的默认地址池作为后备。
这也适用于从 Docker Compose 文件创建的网络，
其中 `enable_ipv6` 设置为 `true`。

如果 Docker Engine 的 `default-address-pools` 中未包含 IPv6 池，
且未提供 `--subnet` 选项，则在启用 IPv6 时将使用[唯一本地地址 (ULAs)][wikipedia-ipv6-ula]。
这些 `/64` 子网包含一个基于 Docker Engine 随机生成 ID 的 40 位
全局 ID，以提供高度的唯一性。

内置的默认地址池配置在[子网分配](../network/_index.md#subnet-allocation)中显示。
它不包含任何 IPv6 池。

要为动态地址分配使用不同的 IPv6 子网池，
您必须手动配置守护进程的地址池以包括：

- 默认 IPv4 地址池
- 您自己的一个或多个 IPv6 池

以下示例显示了一个包含 IPv4 和 IPv6 池的有效配置，
两个池都提供 256 个子网。前缀长度为 `/24` 的 IPv4 子网将从 `/16` 池中分配。
前缀长度为 `/64` 的 IPv6 子网将从 `/56` 池中分配。

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
> 此示例中的地址 `2001:db8::` 是
> [保留用于文档][wikipedia-ipv6-reserved]的地址。
> 请将其替换为有效的 IPv6 网络。
>
> 默认 IPv4 池来自私有地址范围，
> 类似于默认 IPv6 [ULA][wikipedia-ipv6-ula] 网络。

有关 `default-address-pools` 的更多信息，请参见[子网分配](../network/_index.md#subnet-allocation)。

[wikipedia-ipv6-reserved]: https://en.wikipedia.org/wiki/Reserved_IP_addresses#IPv6
[wikipedia-ipv6-ula]: https://en.wikipedia.org/wiki/Unique_local_address

## Docker 中的 Docker

在使用 `xtables`（传统 `iptables`）而不是 `nftables` 的主机上，
在创建 IPv6 Docker 网络之前必须加载内核模块 `ip6_tables`，
通常在 Docker 启动时会自动加载。

但是，如果您运行的 Docker 中的 Docker 不是基于
[官方 `docker` 镜像](https://hub.docker.com/_/docker)的最新版本，
您可能需要在主机上运行 `modprobe ip6_tables`。或者，使用守护进程
选项 `--ip6tables=false` 为容器化的 Docker Engine 禁用 `ip6tables`。

## 下一步

- [网络概述](/manuals/engine/network/_index.md)