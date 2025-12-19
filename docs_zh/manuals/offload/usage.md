---
title: Docker Offload 使用与计费
linktitle: 使用与计费
weight: 30
description: 了解 Docker Offload 的使用情况以及如何监控您的云资源。
keywords: cloud, usage, cloud minutes, shared cache, top repositories, cloud builder, Docker Offload, 云, 使用情况, 云分钟数, 共享缓存, 热门镜像, 云构建器
---

{{< summary-bar feature_name="Docker Offload" >}}

> [!NOTE]
>
> 为 Docker Offload Beta 授予的所有免费试用额度自授予之日起 90 天后过期。若要在试用额度到期后继续使用 Docker Offload Beta，您可以在 [Docker Home 计费](https://app.docker.com/billing) 页面上启用按需使用功能。

## 了解使用和计费模式

Docker Offload 提供两种使用模式，以满足不同团队的需求和使用模式：

- **承诺使用量 (Committed usage)**：为您的组织提供承诺的云端计算时间。
- **按需使用量 (On-demand usage)**：提供随用随付的灵活性。您可以在[计费](#manage-billing)页面中启用或禁用按需使用。

## 管理计费

对于 Docker Offload，您可以在 [Docker Home 计费](https://app.docker.com/billing) 的 **Docker Offload** 页面上查看和配置计费。在此页面上，您可以：

- 查看您的承诺使用量
- 查看云资源的费率
- 管理按需计费，包括设置每月限额
- 跟踪您组织的 Docker Offload 使用情况
- 添加或更改付款方式

您必须是组织所有者才能管理计费。有关计费的更多信息，请参阅[计费](../billing/_index.md)。

## 监控您的使用情况

Docker Home 中的 **Offload 概览 (Offload overview)** 页面提供了对您如何使用云资源来构建和运行容器的可见性。

要监控您的使用情况：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 选择您要监控使用情况的账户。
3. 选择 **Offload** > **Offload 概览 (Offload overview)**。

提供以下小组件：

- **我的近期会话 (My recent sessions)**：此小组件显示您的总会话时长，以及最近会话时长的细分。
- **我的前 10 个镜像 (My top 10 images)**：此小组件显示在运行会话中 Docker Offload 使用的前 10 个镜像。它提供了对最常使用镜像的洞察，帮助您了解容器使用模式。
- **我的活动会话 (My active sessions)**：此小组件显示当前任何活动的 Docker Offload 会话。

### 查看近期活动

Docker Home 中的 **近期活动 (Recent activity)** 页面提供了有关您近期 Docker Offload 会话的详细信息。这包括会话 ID、开始日期和时间、持续时间以及容器数量。

要查看**近期活动 (Recent activity)** 页面：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 选择您要管理 Docker Offload 的账户。
3. 选择 **Offload** > **近期活动 (Recent activity)**。