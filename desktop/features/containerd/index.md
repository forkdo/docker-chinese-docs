# containerd 镜像存储


Docker Desktop 默认使用 containerd 作为其镜像存储。镜像存储是负责在文件系统上推送、拉取和存储镜像的组件。containerd 镜像存储支持多平台镜像、镜像证明以及替代快照器等特性。

## 什么是 `containerd`？

`containerd` 是一个容器运行时，为容器生命周期和镜像管理提供轻量级、一致的接口。Docker Engine 在底层使用它来创建、启动和停止容器。

## 什么是 `containerd` 镜像存储？

镜像存储是负责推送、拉取和在文件系统上存储镜像的组件。

containerd 镜像存储扩展了 Docker Engine 可以原生交互的镜像类型范围。虽然这是一个低级别的架构更改，但它是解锁一系列新用例的先决条件，包括：

- [构建多平台镜像](#build-multi-platform-images) 和带有证明的镜像
- 支持使用具有独特特性的 containerd 快照器，例如 [stargz][1] 用于在容器启动时延迟拉取镜像，或 [nydus][2] 和 [dragonfly][3] 用于点对点镜像分发。
- 运行 [Wasm](wasm.md) 容器的能力

[1]: https://github.com/containerd/stargz-snapshotter
[2]: https://github.com/containerd/nydus-snapshotter
[3]: https://github.com/dragonflyoss/image-service

## 经典镜像存储

经典镜像存储是 Docker 的旧版存储后端，已被 containerd 镜像存储取代。它不支持镜像索引或清单列表，因此你无法在本地加载多平台镜像，也无法构建带有证明的镜像。

大多数用户没有理由使用经典镜像存储。它适用于你需要匹配旧行为或存在兼容性要求的情况。

## 切换镜像存储

containerd 镜像存储在 Docker Desktop 4.34 版本及更高版本中默认启用。要在镜像存储之间切换：

1. 导航到 Docker Desktop 中的 **Settings**。
2. 在 **General** 选项卡中，勾选或清除 **Use containerd for pulling and storing images** 选项。
3. 选择 **Apply**。

> [!NOTE]
>
> Docker Desktop 为经典镜像存储和 containerd 镜像存储维护独立的镜像存储。
> 在两者之间切换时，非活动存储中的镜像和容器仍保留在磁盘上，但会被隐藏，直到您切换回来。

## 构建多平台镜像

containerd 镜像存储让你可以构建多平台镜像并将它们加载到本地镜像存储中：

<script async id="asciicast-ZSUI4Mi2foChLjbevl2dxt5GD" src="https://asciinema.org/a/ZSUI4Mi2foChLjbevl2dxt5GD.js"></script>

使用经典镜像存储不支持构建多平台镜像：

```console
$ docker build --platform=linux/amd64,linux/arm64 .
[+] Building 0.0s (0/0)
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
Learn more at https://docs.docker.com/go/build-multi-platform/
```

