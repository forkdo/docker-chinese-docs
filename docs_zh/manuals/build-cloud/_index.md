---
title: Docker Build Cloud
weight: 20
description: 查找 Docker Build Cloud 文档，帮助您更快地构建容器镜像，无论是在本地还是 CI 环境中
keywords: build, cloud, cloud build, remote builder
params:
  sidebar:
    group: Products
aliases:
  - /build/cloud/faq/
  - /build/cloud/
---

{{< summary-bar feature_name="Docker Build Cloud" >}}

Docker Build Cloud 是一项服务，可让您在本地和 CI 环境中更快地构建容器镜像。
构建在针对您的工作负载优化配置的云基础设施上运行，无需任何配置。
该服务使用远程构建缓存，确保所有团队成员在任何地方都能快速构建。

## Docker Build Cloud 的工作原理

使用 Docker Build Cloud 与运行常规构建没有区别。您使用 `docker buildx build` 命令调用构建，
与平常方式相同。不同之处在于构建的执行位置和方式。

默认情况下，当您调用构建命令时，构建在本地运行的 BuildKit 实例上执行，该实例与 Docker 守护进程捆绑在一起。
使用 Docker Build Cloud 时，您将构建请求发送到远程云环境中的 BuildKit 实例。
所有数据在传输过程中均被加密。

远程构建器执行构建步骤，并将生成的构建输出发送到您指定的目标。例如，发送回您的本地 Docker Engine 镜像存储，或发送到镜像仓库。

Docker Build Cloud 相比本地构建提供了多项优势：

- 提升构建速度
- 共享构建缓存
- 原生多平台构建

最棒的部分是：您无需担心管理构建器或基础设施。只需连接到您的构建器，然后开始构建。
分配给组织的每个云构建器完全隔离在单个 Amazon EC2 实例上，具有专用的 EBS 卷用于构建缓存，以及传输加密。
这意味着云构建器之间没有共享的进程或数据。

> [!NOTE]
>
> Docker Build Cloud 目前仅在美东地区提供。欧洲和亚洲的用户可能会比北美用户遇到更高的延迟。
>
> 多地区构建器支持已在路线图中。

## 获取 Docker Build Cloud

要开始使用 Docker Build Cloud，
[创建一个 Docker 账户](/accounts/create-account/)。有两种方式可以获取 Docker Build Cloud：

- 使用免费个人账户的用户可以选择参加 7 天免费试用，试用结束后可选择订阅继续使用。要开始免费试用，请登录 [Docker Build Cloud 仪表板](https://app.docker.com/build/)，并按照屏幕上的说明操作。
- 所有付费 Docker 订阅用户都可以使用 Docker Build Cloud，它包含在 Docker 产品套件中。更多信息请参阅 [Docker 订阅和功能](/manuals/subscription/details.md)。

注册并创建构建器后，继续在您的本地环境中[设置构建器](./setup.md)。

有关 Docker Build Cloud 的角色和权限信息，请参阅
[角色和权限](/manuals/enterprise/security/roles-and-permissions.md#docker-build-cloud-permissions)。