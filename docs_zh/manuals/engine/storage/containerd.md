---
title: Docker Engine 中的 containerd 镜像存储
linkTitle: containerd 镜像存储
weight: 50
keywords: containerd, 快照器, 镜像存储, docker engine
description: 了解 containerd 镜像存储
aliases:
  - /storage/containerd/
---

containerd 镜像存储是 Docker Engine 29.0 及更高版本在全新安装时的默认存储后端。如果您从早期版本升级，您的守护进程将继续使用传统的图形驱动（overlay2），直到您启用 containerd 镜像存储。

containerd 是行业标准的容器运行时，它使用快照器（snapshotters）而非经典的存储驱动来管理镜像和容器数据在文件系统上的存储和访问方式。

> [!NOTE]
> 使用用户命名空间重映射（`userns-remap`）时，containerd 镜像存储不可用。详情请参见
> [moby#47377](https://github.com/moby/moby/issues/47377)。

## 为什么使用 containerd 镜像存储

containerd 镜像存储使用快照器来管理镜像层在文件系统上的存储和访问方式。这与 overlay2 等经典图形驱动不同。

containerd 镜像存储支持：

- 在本地构建和存储多平台镜像。使用经典存储驱动时，您需要外部构建器来处理多平台镜像。
- 处理包含证明（provenance、SBOM）的镜像。这些镜像使用经典存储不支持的镜像索引。
- 运行 Wasm 容器。containerd 镜像存储支持 WebAssembly 工作负载。
- 使用高级快照器。containerd 支持可插拔的快照器，提供诸如镜像延迟拉取（stargz）或点对点镜像分发（nydus、dragonfly）等功能。

对于大多数用户，切换到 containerd 镜像存储是透明的。存储后端发生变化，但您的工作流程保持不变。

## 磁盘空间使用

对于相同的镜像，containerd 镜像存储比传统存储驱动使用更多的磁盘空间。这是因为 containerd 同时存储压缩和未压缩格式的镜像，而传统驱动仅存储未压缩层。

拉取镜像时，containerd 会保留压缩层（从镜像仓库接收）并将其解压到磁盘。这种双重存储意味着每层占用更多空间。压缩格式可实现更快的拉取和推送，但需要额外的磁盘容量。

当多个镜像共享相同的基础层时，这种差异尤为明显。使用传统存储驱动时，共享的基础层在本地仅存储一份，并被依赖它们的镜像复用。而使用 containerd 时，即使未压缩层仍通过快照器去重，每个镜像都会存储其共享层的独立压缩版本。压缩存储增加了与使用这些层的镜像数量成比例的开销。

如果磁盘空间受限，请考虑以下建议：

- 定期使用 `docker image prune` 清理未使用的镜像
- 使用 `docker system df` 监控磁盘使用情况
- [配置数据目录位置](../daemon/_index.md#configure-the-data-directory-location)
  以使用有足够空间的分区

## 在 Docker Engine 上启用 containerd 镜像存储

如果您从早期 Docker Engine 版本升级，需要手动启用 containerd 镜像存储。

> [!IMPORTANT]
> 切换存储后端会暂时隐藏使用另一后端创建的镜像和容器。您的数据仍保留在磁盘上。要再次访问旧镜像，请切换回之前的存储配置。

在 `/etc/docker/daemon.json` 文件中添加以下配置：

```json
{
  "features": {
    "containerd-snapshotter": true
  }
}
```

保存文件并重启守护进程：

```console
$ sudo systemctl restart docker
```

重启守护进程后，验证您是否正在使用 containerd 镜像存储：

```console
$ docker info -f '{{ .DriverStatus }}'
[[driver-type io.containerd.snapshotter.v1]]
```

Docker Engine 默认使用 `overlayfs` containerd 快照器。

> [!NOTE]
> 启用 containerd 镜像存储后，overlay2 驱动的现有镜像和容器仍保留在磁盘上但被隐藏。如果您切换回 overlay2，它们会重新出现。要将现有镜像与 containerd 镜像存储一起使用，请先将它们推送到镜像仓库，或使用 `docker save` 导出它们。

## 实验性自动迁移

Docker Engine 包含一个实验性功能，可在特定条件下自动切换到 containerd 镜像存储。**此功能处于实验阶段**。它面向希望测试的用户，但[从头开始](#enable-containerd-image-store-on-docker-engine)是推荐的方法。

> [!CAUTION]
> 自动迁移功能处于实验阶段，在所有场景中可能无法可靠工作。使用前请创建备份。

要启用自动迁移，请在 `/etc/docker/daemon.json` 中添加 `containerd-migration` 功能：

```json
{
  "features": {
    "containerd-migration": true
  }
}
```

您还可以设置 `DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD` 环境变量，使守护进程在没有容器且镜像数量小于或等于阈值时自动切换。对于 systemd：

```console
$ sudo systemctl edit docker.service
```

添加：

```ini
[Service]
Environment="DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD=5"
```

如果您没有运行中或已停止的容器，且镜像数量小于或等于 5 个，守护进程将在重启时切换到 containerd 镜像存储。您的 overlay2 数据仍保留在磁盘上但被隐藏。

## 额外资源

要深入了解 Docker Desktop 中 containerd 镜像存储及其功能，请参见
[Docker Desktop 中的 containerd 镜像存储](/manuals/desktop/features/containerd.md)。