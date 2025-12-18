---
title: 无网络驱动
description: 如何使用 none 驱动隔离容器的网络栈
keywords: network, none, standalone
aliases:
  - /network/none/
  - /network/drivers/none/
---

如果您想完全隔离容器的网络栈，可以在启动容器时使用 `--network none` 标志。
在容器内部，仅创建回环设备。

以下示例展示了使用 `none` 网络驱动的 `alpine` 容器中 `ip link show` 的输出。

```console
$ docker run --rm --network none alpine:latest ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

使用 `none` 驱动的容器不会配置 IPv6 回环地址。

```console
$ docker run --rm --network none --name no-net-alpine alpine:latest ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
```

## 下一步

- 了解 [从容器视角看网络](../_index.md)
- 了解 [主机网络](host.md)
- 了解 [桥接网络](bridge.md)
- 了解 [覆盖网络](overlay.md)
- 了解 [Macvlan 网络](macvlan.md)
