---
title: 构建器设置
description: 设置与私有仓库、磁盘分配相关的构建器配置。
keywords: build, cloud build, optimize, remote, local, cloud, registry, package repository, vpn
---

Docker Build Cloud 中的 **构建器设置** 页面允许您为组织中的云构建器配置磁盘分配、私有资源访问和防火墙设置。这些配置有助于优化存储、启用私有仓库访问并保护出站网络流量。

## 存储和缓存管理

### 磁盘分配

**磁盘分配** 设置允许您控制有多少可用存储空间用于构建缓存。较低的分配会增加可用于活动构建的存储空间。

要修改磁盘分配，请导航到 Docker Build Cloud 中的 **构建器设置**，然后调整 **磁盘分配** 滑块以指定用于构建缓存的存储百分比。

任何更改将立即生效。

### 构建缓存空间

您的订阅包含以下构建缓存空间：

| 订阅类型 | 构建缓存空间 |
|----------|--------------|
| 个人版   | 不适用       |
| Pro      | 50GB         |
| Team     | 100GB        |
| Business | 200GB        |

### 多架构存储分配

Docker Build Cloud 自动为 amd64 和 arm64 架构提供构建器。您的总构建缓存空间在这两个构建器之间平均分配：

- Pro（总计 50GB）：amd64 构建器 25GB + arm64 构建器 25GB
- Team（总计 100GB）：amd64 构建器 50GB + arm64 构建器 50GB
- Business（总计 200GB）：amd64 构建器 100GB + arm64 构建器 100GB

> [!IMPORTANT]
>
> 如果您只为一种架构构建，请注意您的有效缓存空间是订阅总分配量的一半。

### 获取更多构建缓存空间

要获取更多构建缓存空间，请[升级您的订阅](/manuals/subscription/scale.md)。

> [!TIP]
>
> 如果您构建大型镜像，考虑减少用于缓存的存储分配，为活动构建预留更多空间。

## 私有资源访问

私有资源访问允许云构建器从私有资源拉取镜像和包。当构建依赖于自托管的制品仓库或私有 OCI 仓库时，此功能非常有用。

例如，如果您的组织在私有网络上托管私有 [PyPI](https://pypi.org/) 仓库，默认情况下 Docker Build Cloud 无法访问它，因为云构建器未连接到您的私有网络。

要让您的云构建器能够访问私有资源，请输入私有资源的主机名和端口，然后选择 **添加**。

### 身份验证

如果您的内部制品需要身份验证，请确保在构建之前或构建期间对仓库进行身份验证。对于 npm 或 PyPI 的内部包仓库，使用 [构建密钥](/manuals/build/building/secrets.md) 在构建期间进行身份验证。对于内部 OCI 仓库，使用 `docker login` 在构建之前进行身份验证。

请注意，如果使用需要身份验证的私有仓库，您需要在构建之前进行两次 `docker login`。这是因为云构建器需要先使用 Docker 进行身份验证以使用云构建器，然后再对私有仓库进行身份验证。

```console
$ echo $DOCKER_PAT | docker login docker.io -u <username> --password-stdin
$ echo $REGISTRY_PASSWORD | docker login registry.example.com -u <username> --password-stdin
$ docker build --builder <cloud-builder> --tag registry.example.com/<image> --push .
```

## 防火墙

防火墙设置允许您将云构建器的出站流量限制到特定 IP 地址。这有助于通过限制构建器的外部网络出站流量来增强安全性。

1. 选中 **启用防火墙：将云构建器出站流量限制到特定公共 IP 地址** 复选框。
2. 输入您要允许的 IP 地址。
3. 选择 **添加** 以应用限制。