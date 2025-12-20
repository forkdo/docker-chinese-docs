# 使用 containerd 镜像存储的 Docker Engine

containerd 镜像存储是 Docker Engine 29.0 及更高版本在全新安装时的默认存储后端。如果您是从早期版本升级而来，守护进程将继续使用传统的 graph 驱动程序（overlay2），直到您启用 containerd 镜像存储为止。

作为行业标准容器运行时的 containerd 使用 snapshotters 而非传统的存储驱动程序来存储镜像和容器数据。

> [!NOTE]
> 使用用户命名空间重映射（`userns-remap`）时，containerd 镜像存储不可用。详情请参见 [moby#47377](https://github.com/moby/moby/issues/47377)。

## 为何使用 containerd 镜像存储

containerd 镜像存储使用 snapshotters 来管理镜像层在文件系统中的存储和访问方式。这与传统的 graph 驱动程序（如 overlay2）不同。

containerd 镜像存储支持以下功能：

- 本地构建和存储多平台镜像。使用传统存储驱动程序时，您需要外部构建器来创建多平台镜像。
- 处理包含证明（来源、SBOM）的镜像。这些镜像使用传统存储不支持的镜像索引。
- 运行 Wasm 容器。containerd 镜像存储支持 WebAssembly 工作负载。
- 使用高级 snapshotters。containerd 支持可插拔的 snapshotters，提供诸如镜像延迟拉取（stargz）或对等镜像分发（nydus、dragonfly）等功能。

对大多数用户而言，切换到 containerd 镜像存储是透明的。虽然存储后端发生了变化，但您的工作流程保持不变。

## 磁盘空间使用

对于相同的镜像，containerd 镜像存储比传统存储驱动程序占用更多磁盘空间。这是因为 containerd 以压缩和非压缩两种格式存储镜像，而传统驱动程序仅存储非压缩层。

当您拉取镜像时，containerd 会保留压缩层（从注册表中接收到的格式），同时也会将其解压到磁盘上。这种双重存储意味着每一层都会占用更多空间。压缩格式可以实现更快的拉取和推送操作，但需要额外的磁盘容量。

当多个镜像共享相同的基础层时，这种差异尤为明显。使用传统存储驱动程序时，共享的基础层在本地仅存储一次，依赖它们的镜像可以重复使用。而使用 containerd 时，即使非压缩层仍通过 snapshotters 进行去重，每个镜像也会存储其共享层的压缩版本。压缩存储会增加与这些层使用镜像数量成比例的开销。

如果磁盘空间受限，请考虑以下建议：

- 定期使用 `docker image prune` 清理未使用的镜像
- 使用 `docker system df` 监控磁盘使用情况
- [配置数据目录](../daemon/_index.md#configure-the-data-directory-location) 以使用具有足够空间的分区

## 在 Docker Engine 上启用 containerd 镜像存储

如果您是从早期 Docker Engine 版本升级而来，需要手动启用 containerd 镜像存储。

> [!IMPORTANT]
> 切换存储后端会暂时隐藏使用其他后端创建的镜像和容器。您的数据仍保留在磁盘上。要再次访问旧镜像，请切换回之前的存储配置。

将以下配置添加到您的 `/etc/docker/daemon.json` 文件中：

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

守护进程重启后，验证您是否正在使用 containerd 镜像存储：

```console
$ docker info -f '{{ .DriverStatus }}'
[[driver-type io.containerd.snapshotter.v1]]
```

Docker Engine 默认使用 `overlayfs` containerd snapshotter。

> [!NOTE]
> 启用 containerd 镜像存储后，来自 overlay2 驱动程序的现有镜像和容器仍保留在磁盘上，但会被隐藏。如果您切换回 overlay2，它们会重新出现。要使现有镜像与 containerd 镜像存储配合使用，请先将它们推送到注册表，或使用 `docker save` 导出它们。

## 实验性自动迁移

Docker Engine 包含一项实验性功能，可在特定条件下自动切换到 containerd 镜像存储。**此功能为实验性质**。它专为希望测试该功能的用户提供，但[全新安装](#enable-containerd-image-store-on-docker-engine)仍是推荐方法。

> [!CAUTION]
> 自动迁移功能为实验性质，可能无法在所有场景中可靠工作。尝试使用前请先创建备份。

要启用自动迁移，请将 `containerd-migration` 功能添加到您的 `/etc/docker/daemon.json` 中：

```json
{
  "features": {
    "containerd-migration": true
  }
}
```

您还可以设置 `DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD` 环境变量，使守护进程在没有任何容器且镜像数量等于或低于阈值时自动切换。对于 systemd：

```console
$ sudo systemctl edit docker.service
```

添加：

```ini
[Service]
Environment="DOCKER_MIGRATE_SNAPSHOTTER_THRESHOLD=5"
```

如果您没有正在运行或已停止的容器，且镜像数量不超过 5 个，守护进程将在重启时切换到 containerd 镜像存储。您的 overlay2 数据仍保留在磁盘上，但会被隐藏。

## 其他资源

要了解有关 containerd 镜像存储及其在 Docker Desktop 中功能的更多信息，请参阅 [Docker Desktop 上的 containerd 镜像存储](/manuals/desktop/features/containerd.md)。
