---
title: containerd 镜像存储
weight: 80
description: 如何在 Docker Desktop 中激活 containerd 集成功能
keywords: Docker, containerd, engine, image store, lazy-pull
toc_max: 3
aliases:
- /desktop/containerd/
---

Docker Desktop 正在向使用 containerd 进行镜像和文件系统管理过渡。本文档概述了 containerd 镜像存储的优势、设置过程以及启用的新功能。

> [!NOTE]
> 
> Docker Desktop 为经典镜像存储和 containerd 镜像存储维护独立的镜像存储。
> 在两者之间切换时，非活动存储中的镜像和容器仍保留在磁盘上，但会被隐藏，直到您切换回来。

## 什么是 `containerd`？

`containerd` 是一个容器运行时，为容器生命周期管理提供轻量级、一致的接口。Docker Engine 在底层已经使用它来创建、启动和停止容器。

Docker Desktop 对 containerd 的持续集成现在扩展到了镜像存储，提供了更多的灵活性和对现代镜像的支持。

## 什么是 `containerd` 镜像存储？

镜像存储是负责推送、拉取和在文件系统上存储镜像的组件。

经典的 Docker 镜像存储在支持的镜像类型方面存在限制。例如，它不支持包含清单列表的镜像索引。当您创建多平台镜像时，镜像索引会解析镜像的所有特定平台变体。构建带有证明的镜像时也需要镜像索引。

containerd 镜像存储扩展了 Docker Engine 可以原生交互的镜像类型范围。虽然这是一个低级别的架构更改，但它是解锁一系列新用例的先决条件，包括：

- [构建多平台镜像](#build-multi-platform-images) 和带有证明的镜像
- 支持使用具有独特特性的 containerd 快照器，例如 [stargz][1] 用于在容器启动时延迟拉取镜像，或 [nydus][2] 和 [dragonfly][3] 用于点对点镜像分发。
- 运行 [Wasm](wasm.md) 容器的能力

[1]: https://github.com/containerd/stargz-snapshotter
[2]: https://github.com/containerd/nydus-snapshotter
[3]: https://github.com/dragonflyoss/image-service

## 启用 containerd 镜像存储

containerd 镜像存储在 Docker Desktop 4.34 版本及更高版本中默认启用，但仅适用于全新安装或执行工厂重置的情况。如果您从早期版本的 Docker Desktop 升级，或者使用较旧版本的 Docker Desktop，则必须手动切换到 containerd 镜像存储。

要在 Docker Desktop 中手动启用此功能：

1. 导航到 Docker Desktop 中的 **Settings**。
2. 在 **General** 选项卡中，勾选 **Use containerd for pulling and storing images**。
3. 选择 **Apply**。

要禁用 containerd 镜像存储，请取消勾选 **Use containerd for pulling and storing images** 复选框。

## 构建多平台镜像

多平台镜像这个术语指的是针对多个不同架构的镜像包。开箱即用，默认的 Docker Desktop 构建器不支持构建多平台镜像。

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

启用 containerd 镜像存储后，您可以构建多平台镜像并将它们加载到本地镜像存储中：

<script async id="asciicast-ZSUI4Mi2foChLjbevl2dxt5GD" src="https://asciinema.org/a/ZSUI4Mi2foChLjbevl2dxt5GD.js"></script>