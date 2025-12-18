---
title: 配置 Docker Offload
linktitle: 配置
weight: 20
description: 了解如何为 Docker Offload 配置构建设置。
keywords: cloud, configuration, settings, offload
---

{{< summary-bar feature_name="Docker Offload" >}}

您可以根据您的角色在不同层级配置 Docker Offload 设置。组织所有者可以管理其组织中所有用户的设置，而个人开发者（在组织允许的情况下）可以配置自己的 Docker Desktop 设置。

## 管理组织的设置

对于组织所有者，您可以管理组织中所有用户的 Docker Offload 设置。更多详细信息，请参阅 [管理 Docker 产品](../admin/organization/manage-products.md)。要查看使用情况并配置 Docker Offload 的计费，请参阅 [Docker Offload 使用情况和计费](/offload/usage/)。

## 在 Docker Desktop 中配置设置

对于开发者，您可以在 Docker Desktop 中管理 Docker Offload 设置。要管理设置：

1. 打开 Docker Desktop 仪表板并登录。
2. 选择 Docker Desktop 仪表板标题中的设置图标。
3. 在 **Settings** 中，选择 **Docker Offload**。

   在这里您可以：

   - 切换 **Enable Docker Offload**。启用后，您可以启动 Offload 会话。
   - 选择 **Idle timeout**。这是在没有活动后，Docker Offload 进入空闲模式之前的持续时间。
     有关空闲超时的详细信息，请参阅 [了解活跃和空闲状态](#understand-active-and-idle-states)。

### 了解活跃和空闲状态

Docker Offload 会在活跃和空闲状态之间自动切换，以帮助您在保持无缝开发体验的同时控制成本。

#### 会话处于活跃状态时

当您正在构建镜像、运行容器或积极与它们交互（例如查看日志或保持开放的网络连接）时，您的 Docker Offload 环境处于活跃状态。在活跃状态下：

- 会收取使用费用
- 远程 Docker 引擎连接到您的本地机器
- 所有容器操作在云端环境中执行

#### 会话处于空闲状态时

当没有活动时，Docker Offload 会过渡到空闲状态。在空闲状态下：

- 不会收取使用费用
- 远程连接被暂停
- 云端没有运行的容器

空闲过渡延迟可以在 Docker Desktop 设置中配置，范围从 10 秒到 1 小时。此设置决定了 Docker Offload 在检测到无活动后，等待多长时间才过渡到空闲状态。

#### 会话如何被保留

如果您的会话空闲时间少于 5 分钟且您恢复活动，您的先前容器和镜像将被保留并保持可用。这允许您从中断处无缝继续。

但是，如果空闲时间超过 5 分钟，将启动一个新的会话并使用干净的环境，之前会话中的任何容器、镜像或卷都将被删除。

> [!NOTE]
>
> 在 5 分钟内从活跃状态过渡到空闲状态再回到活跃状态将被视为连续使用并计费。