---
description: 为 Docker Hub 镜像设置本地镜像仓库
keywords: registry, on-prem, images, tags, repository, distribution, mirror, Hub, recipe, advanced
title: 镜像 Docker Hub 官方镜像库
linkTitle: 镜像
weight: 80
aliases:
- /engine/admin/registry_mirror/
- /registry/recipes/mirror/
- /docker-hub/mirror/
---

## 使用场景

如果您的环境中运行着多个 Docker 实例，例如多台物理机或虚拟机都在运行 Docker，那么每个守护进程都会访问互联网，从 Docker 仓库获取本地不存在的镜像。您可以运行一个本地仓库镜像，并将所有守护进程指向它，以避免这种额外的互联网流量。

> [!NOTE]
>
> Docker 官方镜像是 Docker 的知识产权。

### 替代方案

或者，如果您使用的镜像集合范围明确，您可以手动拉取它们并推送到一个简单的本地私有仓库。

此外，如果您的镜像都是内部构建的，完全不使用 Hub，而完全依赖本地仓库，则是最简单的场景。

### 注意事项

目前无法镜像另一个私有仓库。只能镜像中心 Hub。

> [!NOTE]
>
> Docker Hub 的镜像仍需遵守 Docker 的[公平使用政策](/manuals/docker-hub/usage/_index.md#fair-use)。

### 解决方案

仓库可以配置为直通缓存（pull through cache）。在此模式下，仓库会响应所有正常的 docker pull 请求，但会将所有内容存储在本地。

### 将仓库镜像与仓库访问管理 (RAM) 结合使用

如果通过您的仓库访问管理 (RAM) 配置限制了对 Docker Hub 的访问，即使镜像在您的仓库镜像中可用，您也将无法拉取源自 Docker Hub 的镜像。

您会遇到以下错误：
```console
Error response from daemon: Access to docker.io has been restricted by your administrators.
```

如果您无法允许访问 Docker Hub，可以手动从您的仓库镜像拉取，并可选择重新标记镜像。例如：
```console
docker pull <your-registry-mirror>[:<port>]/library/busybox
docker tag <your-registry-mirror>[:<port>]/library/busybox:latest busybox:latest
```

## 工作原理

当您第一次从本地仓库镜像请求镜像时，它会从公共 Docker 仓库拉取该镜像，将其存储在本地，然后将其返回给您。在后续请求中，本地仓库镜像能够从其自身存储中提供镜像。

### 如果 Hub 上的内容发生变化怎么办？

当尝试使用标签拉取时，仓库会检查远程仓库以确保其是否拥有请求内容的最新版本。否则，它会获取并缓存最新内容。

### 磁盘空间问题怎么办？

在变更率高的环境中，缓存中可能会堆积陈旧数据。当作为直通缓存运行时，仓库会定期删除旧内容以节省磁盘空间。对已删除内容的后续请求会导致远程获取和本地重新缓存。

为确保最佳性能并保证正确性，仓库缓存应配置为使用 `filesystem` 驱动进行存储。

## 运行仓库作为直通缓存

将仓库作为直通缓存运行的最简单方法是运行官方的 [Registry](https://hub.docker.com/_/registry) 镜像。
至少，您需要在 `/etc/docker/registry/config.yml` 中指定 `proxy.remoteurl`，如下小节所述。

多个仓库缓存可以部署在同一个后端之上。单个仓库缓存可以确保并发请求不会拉取重复数据，但此特性在仓库缓存集群中不成立。

### 配置缓存

要将仓库配置为作为直通缓存运行，需要在配置文件中添加一个 `proxy` 部分。

要访问 Docker Hub 上的私有镜像，可以提供用户名和密码。

```yaml
proxy:
  remoteurl: https://registry-1.docker.io
  username: [username]
  password: [password]
```

> [!WARNING]
>
> 如果指定了用户名和密码，必须非常重要的理解：该用户有权访问的 Docker Hub 私有资源将在您的镜像上可用。如果您希望这些资源保持私有，必须通过实施身份验证来保护您的镜像！

> [!WARNING]
>
> 为了让调度程序清理旧条目，必须在仓库配置中启用 `delete`。

### 配置 Docker 守护进程

在手动启动 `dockerd` 时传递 `--registry-mirror` 选项，或者编辑 [`/etc/docker/daemon.json`](/reference/cli/dockerd.md#daemon-configuration-file) 并添加 `registry-mirrors` 键和值，以使更改持久化。

```json
{
  "registry-mirrors": ["https://<my-docker-mirror-host>"]
}
```

保存文件并重新加载 Docker 以使更改生效。

> [!NOTE]
>
> 一些看似错误的日志消息实际上是信息性消息。
>
> 检查 `level` 字段以确定消息是警告您错误还是提供信息。例如，此日志消息是信息性的：
>
> ```text
> time="2017-06-02T15:47:37Z" level=info msg="error statting local store, serving from upstream: unknown blob" go.version=go1.7.4
> ```
>
> 它告诉您该文件在本地缓存中尚不存在，正在从上游拉取。