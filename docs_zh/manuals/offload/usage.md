---
title: Docker Offload 使用量与计费
linktitle: 使用量与计费
weight: 30
description: 了解 Docker Offload 使用量以及如何监控您的云资源。
keywords: cloud, usage, cloud minutes, shared cache, top repositories, cloud builder, Docker Offload
---

{{< summary-bar feature_name="Docker Offload" >}}

> [!NOTE]
>
> Docker Offload Beta 版的所有免费试用使用量自授予之日起 90 天后过期。要在使用量过期后继续使用 Docker Offload Beta 版，您可以在 [Docker Home 计费](https://app.docker.com/billing) 中启用按需使用量。

## 了解使用量与计费模式

Docker Offload 提供两种使用模式，以满足不同团队的需求和使用模式：

- 承诺使用量：为您的组织提供一定量的云计算时间承诺。
- 按需使用量：提供即用即付的灵活性。您可以在 [计费](#manage-billing) 中启用或禁用按需使用量。

## 管理计费

对于 Docker Offload，您可以在 [Docker Home 计费](https://app.docker.com/billing) 的 **Docker Offload** 页面查看和配置计费。在此页面上，您可以：

- 查看您的承诺使用量
- 查看云资源费率
- 管理按需计费，包括设置月度限额
- 跟踪您组织的 Docker Offload 使用量
- 添加或更改支付方式

您必须是组织所有者才能管理计费。有关计费的一般信息，请参阅 [计费](../billing/_index.md)。

## 监控您的使用量

Docker Home 中的 **Offload 概览** 页面提供了关于您如何使用云资源构建和运行容器的可见性。

要监控您的使用量：

1. 登录到 [Docker Home](https://app.docker.com/)。
2. 选择您要监控使用量的账户。
3. 选择 **Offload** > **Offload 概览**。

以下小部件可用：

- 我最近的会话：此小部件显示您的总会话时间以及最近会话持续时间的细分。
- 我的前 10 个镜像：此小部件显示在 Docker Offload 运行会话中使用的前 10 个镜像。它提供了对最常使用镜像的洞察，帮助您了解容器使用模式。
- 我的活动会话：此小部件显示任何当前活跃的 Docker Offload 会话。

### 查看最近活动

Docker Home 中的 **最近活动** 页面提供了关于您最近 Docker Offload 会话的详细信息。这包括会话 ID、开始日期和时间、持续时间以及容器数量。

要查看 **最近活动** 页面：

1. 登录到 [Docker Home](https://app.docker.com/)。
2. 选择您要管理 Docker Offload 的账户。
3. 选择 **Offload** > **Recent activity**。