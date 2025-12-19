---
title: 配置 Docker Offload
linktitle: 配置
weight: 20
description: 了解如何为 Docker Offload 配置构建设置。
keywords: cloud, configuration, settings, offload
---

{{< summary-bar feature_name="Docker Offload" >}}

您可以根据您的角色在不同级别配置 Docker Offload 设置。组织所有者可以管理其组织中所有用户的设置，而个人开发者可以在组织允许的情况下配置自己的 Docker Desktop 设置。

## 管理组织的设置

对于组织所有者，您可以管理组织中所有用户的 Docker Offload 设置。有关更多详细信息，请参阅[管理 Docker 产品](../admin/organization/manage-products.md)。要查看使用情况并为 Docker Offload 配置账单，请参阅[Docker Offload 使用情况和账单](/offload/usage/)。

## 在 Docker Desktop 中配置设置

对于开发者，您可以在 Docker Desktop 中管理 Docker Offload 设置。要管理设置：

1. 打开 Docker Desktop 仪表板并登录。
2. 在 Docker Desktop 仪表板标题中选择设置图标。
3. 在**设置**中，选择**Docker Offload**。

   在这里您可以：

   - 切换**启用 Docker Offload**。启用后，您可以启动 Offload 会话。
   - 选择**空闲超时**。这是指在没有活动后，Docker Offload 进入空闲模式之前的时间段。有关空闲超时的详细信息，请参阅[了解活动和空闲状态](#了解活动和空闲状态)。

### 了解活动和空闲状态

Docker Offload 会自动在活动和空闲状态之间转换，以帮助您在保持无缝开发体验的同时控制成本。

#### 当您的会话处于活动状态时

当您正在构建镜像、运行容器或与它们积极交互（例如查看日志或保持网络连接打开）时，您的 Docker Offload 环境处于活动状态。在活动状态下：

- 使用情况会计费
- 远程 Docker 引擎连接到您的本地机器
- 所有容器操作都在云环境中执行

#### 当您的会话处于空闲状态时

当没有活动时，Docker Offload 会转换到空闲状态。在空闲状态下：

- 您无需支付使用费用
- 远程连接被挂起
- 云中没有运行任何容器

空闲转换延迟可以在 Docker Desktop 设置中配置，范围从 10 秒到 1 小时。此设置决定了 Docker Offload 在检测到不活动后，等待多长时间才转换到空闲状态。

#### 如何保留您的会话

如果您的会话空闲时间少于 5 分钟，并且您恢复活动，您之前的容器和镜像将被保留并保持可用。这允许您从上次中断的地方继续。

但是，如果空闲时间超过 5 分钟，将启动一个具有干净环境的新会话，之前会话中的任何容器、镜像或卷都将被删除。

> [!NOTE]
>
> 在 5 分钟内从活动状态转换到空闲状态，然后再转换回活动状态，将被视为连续使用而计费。