---
title: Builder settings
description: Set your builder settings relating to private registries, disk allocation .
keywords: build, cloud build, optimize, remote, local, cloud, registry, package repository, vpn
---

Docker Build Cloud 中的 **Builder 设置** 页面允许你为组织中的云构建器配置磁盘分配、私有资源访问和防火墙设置。这些配置有助于优化存储、启用对私有注册表的访问，并保护出站网络流量。

## 存储和缓存管理

### 磁盘分配

**磁盘分配** 设置允许你控制有多少可用存储空间用于构建缓存。较低的分配会增加可用于活跃构建的存储空间。

要修改磁盘分配，请在 Docker Build Cloud 中导航到 **Builder 设置** 页面，然后调整 **磁盘分配** 滑块，指定用于构建缓存的存储空间百分比。

任何更改将立即生效。

### 构建缓存空间

你的订阅包含以下构建缓存空间：

| 订阅类型 | 构建缓存空间 |
|--------------|-------------------|
| Personal     | N/A               |
| Pro          | 50GB              |
| Team         | 100GB             |
| Business     | 200GB             |

### 多架构存储分配

Docker Build Cloud 会自动为 amd64 和 arm64 两种架构配置构建器。你的总构建缓存空间会在这两个构建器之间平均分配：

- Pro（总计 50GB）：amd64 构建器 25GB + arm64 构建器 25GB
- Team（总计 100GB）：amd64 构建器 50GB + arm64 构建器 50GB
- Business（总计 200GB）：amd64 构建器 100GB + arm64 构建器 100GB

> [!IMPORTANT]
>
> 如果你只针对一种架构构建，请注意你的有效缓存空间是你订阅总分配量的一半。

### 获取更多构建缓存空间

要获取更多构建缓存空间，请[升级你的订阅](/manuals/subscription/scale.md)。

> [!TIP]
>
> 如果你构建大型镜像，考虑减少用于缓存的存储分配，为活跃构建留出更多空间。

## 私有资源访问

私有资源访问功能允许云构建器从私有资源拉取镜像和包。当构建依赖于自托管的工件仓库或私有 OCI 注册表时，此功能非常有用。

例如，如果你的组织在私有网络上托管私有 [PyPI](https://pypi.org/) 仓库，Docker Build Cloud 默认情况下无法访问它，因为云构建器未连接到你的私有网络。

要让你的云构建器能够访问私有资源，请输入私有资源的主机名和端口，然后选择 **Add**。

### 身份验证

如果你的内部工件需要身份验证，请确保在构建之前或构建期间对仓库进行身份验证。对于 npm 或 PyPI 的内部包仓库，使用 [构建密钥](/manuals/build/building/secrets.md) 在构建期间进行身份验证。对于内部 OCI 注册表，使用 `docker login` 在构建之前进行身份验证。

请注意，如果你使用需要身份验证的私有注册表，你需要在构建之前进行两次 `docker login`。这是因为云构建器需要先向 Docker 进行身份验证以使用云构建器，然后再向私有注册表进行身份验证。

```console
$ echo $DOCKER_PAT | docker login docker.io -u <username> --password-stdin
$ echo $REGISTRY_PASSWORD | docker login registry.example.com -u <username> --password-stdin
$ docker build --builder <cloud-builder> --tag registry.example.com/<image> --push .
```

## 防火墙

防火墙设置允许你将云构建器的出站流量限制到特定的 IP 地址。这有助于通过限制构建器的外部网络出站流量来增强安全性。

1. 选中 **Enable firewall: Restrict cloud builder egress to specific public IP address** 复选框。
2. 输入你想要允许的 IP 地址。
3. 选择 **Add** 以应用限制。