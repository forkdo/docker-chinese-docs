---
description: 为 Docker Hub 镜像设置本地镜像
keywords: registry, on-prem, images, tags, repository, distribution, mirror, Hub,
  recipe, advanced
title: 镜像 Docker Hub 官方仓库
linkTitle: 镜像
weight: 80
aliases:
- /engine/admin/registry_mirror/
- /registry/recipes/mirror/
- /docker-hub/mirror/
---

## 使用场景

如果你的环境中运行着多个 Docker 实例，比如多台物理机或虚拟机都在运行 Docker，每个守护进程都会连接到互联网，从 Docker 仓库拉取本地没有的镜像。你可以运行一个本地注册表镜像，并将所有守护进程指向那里，以避免额外的网络流量。

> [!NOTE]
>
> Docker 官方镜像是 Docker 的知识产权。

### 替代方案

另外，如果你使用的镜像集合范围明确，你可以手动拉取它们并推送到一个简单的本地私有注册表。

此外，如果你的所有镜像都是内部构建的，完全不使用 Hub，而完全依赖于本地注册表，这是最简单的场景。

### 注意事项

目前无法镜像另一个私有注册表。只能镜像中央 Hub。

> [!NOTE]
>
> Docker Hub 的镜像仍然受 Docker [公平使用政策](/manuals/docker-hub/usage/_index.md#fair-use) 的约束。

### 解决方案

注册表可以配置为拉取缓存。在这种模式下，注册表响应所有正常的 docker pull 请求，但将所有内容存储在本地。

### 在注册表镜像中使用注册表访问管理 (RAM)

如果通过你的注册表访问管理 (RAM) 配置限制了 Docker Hub 的访问，即使镜像在你的注册表镜像中可用，你也无法拉取来自 Docker Hub 的镜像。

你会遇到以下错误：
```console
Error response from daemon: Access to docker.io has been restricted by your administrators.
```

如果你无法允许访问 Docker Hub，你可以手动从注册表镜像拉取并可选择重新标记镜像。例如：
```console
docker pull <your-registry-mirror>[:<port>]/library/busybox
docker tag <your-registry-mirror>[:<port>]/library/busybox:latest busybox:latest
```

## 它是如何工作的？

当你第一次从本地注册表镜像请求镜像时，它会从公共 Docker 注册表拉取镜像并存储在本地，然后再返回给你。在后续请求中，本地注册表镜像能够从其自己的存储中提供镜像。

### 如果 Hub 上的内容发生变化怎么办？

当使用标签尝试拉取时，注册表会检查远程端点，确保它是否拥有请求内容的最新版本。否则，它会获取并重新缓存最新内容。

### 磁盘空间怎么办？

在高变化率的环境中，缓存中可能会积累陈旧数据。当作为拉取缓存运行时，注册表会定期删除旧内容以节省磁盘空间。对已删除内容的后续请求会导致远程获取和本地重新缓存。

为了确保最佳性能并保证正确性，注册表缓存应配置为对存储使用 `filesystem` 驱动。

## 将注册表作为拉取缓存运行

将注册表作为拉取缓存运行的最简单方法是运行官方的 [Registry](https://hub.docker.com/_/registry) 镜像。至少，你需要在 `/etc/docker/registry/config.yml` 中指定 `proxy.remoteurl`，如以下小节所述。

多个注册表缓存可以部署在相同的后端上。单个注册表缓存确保并发请求不会拉取重复数据，但注册表缓存集群不保证此属性。

### 配置缓存

要将注册表配置为作为拉取缓存运行，需要在配置文件中添加 `proxy` 部分。

要访问 Docker Hub 上的私有镜像，可以提供用户名和密码。

```yaml
proxy:
  remoteurl: https://registry-1.docker.io
  username: [username]
  password: [password]
```

> [!WARNING]
>
> 如果你指定了用户名和密码，非常重要的一点是理解该用户在 Docker Hub 上可以访问的私有资源将在此镜像上可用。如果你期望这些资源保持私有，必须通过实现身份验证来保护你的镜像！

> [!WARNING]
>
> 为了使调度器能够清理旧条目，必须在注册表配置中启用 `delete`。

### 配置 Docker 守护进程

手动启动 `dockerd` 时，可以传递 `--registry-mirror` 选项，或者编辑 [`/etc/docker/daemon.json`](/reference/cli/dockerd.md#daemon-configuration-file) 并添加 `registry-mirrors` 键和值，使更改持久化。

```json
{
  "registry-mirrors": ["https://<my-docker-mirror-host>"]
}
```

保存文件并重新加载 Docker 使更改生效。

> [!NOTE]
>
> 某些看似错误的日志消息实际上是信息性消息。
>
> 请检查 `level` 字段以确定消息是警告你出现错误还是在提供信息。例如，此日志消息是信息性的：
>
> ```text
> time="2017-06-02T15:47:37Z" level=info msg="error statting local store, serving from upstream: unknown blob" go.version=go1.7.4
> ```
>
> 它告诉你文件尚未在本地缓存中存在，正从上游拉取。