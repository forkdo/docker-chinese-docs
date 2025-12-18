---
description: 了解如何在 Docker Desktop 中使用 Docker Desktop 仪表板，包括快速搜索、Docker 菜单等
keywords: Docker Desktop Dashboard, 管理, 容器, 图形界面, 仪表板, 镜像, 用户手册,
  鲸鱼菜单
title: 探索 Docker Desktop
weight: 30
aliases:
- /desktop/dashboard/
---

打开 Docker Desktop 时，会显示 Docker Desktop 仪表板。

![Docker Desktop Dashboard on Containers view](../images/dashboard.webp) 

它提供了一个集中式界面，用于管理您的 [容器](container.md)、[镜像](images.md)、[卷](volumes.md)、[构建](builds.md) 和 [Kubernetes 资源](kubernetes.md)。

此外，Docker Desktop 仪表板还允许您：

- 使用 [Ask Gordon](/manuals/ai/gordon/_index.md)，这是嵌入在 Docker Desktop 和 Docker CLI 中的个人 AI 助手。它旨在简化您的工作流程，并帮助您充分利用 Docker 生态系统。
- 导航到 **Settings** 菜单以配置 Docker Desktop 设置。在仪表板标题中选择 **Settings** 图标。
- 访问 **Troubleshoot** 菜单以进行调试和执行重启操作。在仪表板标题中选择 **Troubleshoot** 图标。
- 在 **Notifications center** 中接收新版本、安装进度更新等通知。在 Docker Desktop 仪表板右下角选择铃铛图标以访问通知中心。
- 从仪表板标题访问 **Learning center**。它通过快速的应用内演练和其他学习资源帮助您入门 Docker。
  
  有关更详细的入门指南，请参阅 [Get started](/get-started/introduction/_index.md)。
- 访问 [Docker Hub](/manuals/docker-hub/_index.md) 以搜索、浏览、拉取、运行或查看镜像详情。
- 进入 [Docker Scout](../../scout/_index.md) 仪表板。
- 导航到 [Docker Extensions](/manuals/extensions/_index.md)。

## Docker 终端

从 Docker 仪表板底部，您可以在 Docker Desktop 中直接使用集成终端。

集成终端：

- 如果您导航到 Docker Desktop 仪表板的其他部分然后返回，会保留您的会话。
- 支持复制、粘贴、搜索和清除会话。

#### 打开集成终端

要打开集成终端，可以：

- 将鼠标悬停在正在运行的容器上，在 **Actions** 列中，选择 **Show container actions** 菜单。从下拉菜单中选择 **Open in terminal**。
- 或者，选择位于右下角、版本号旁边的 **Terminal** 图标。

要使用外部终端，请导航到 **Settings** 中的 **General** 选项卡，并在 **Choose your terminal** 下选择 **System default** 选项。

## 快速搜索

使用位于 Docker 仪表板标题中的快速搜索功能来搜索：

- 您本地系统上的任何容器或 Compose 应用。您可以查看关联环境变量的概览，或执行快速操作，如启动、停止或删除。

- 公共 Docker Hub 镜像、本地镜像以及来自远程仓库的镜像（Hub 中您所属组织的私有仓库）。根据您选择的镜像类型，您可以按标签拉取镜像、查看文档、转到 Docker Hub 获取更多详细信息，或使用该镜像运行新容器。

- 扩展。在这里，您可以了解有关扩展的更多信息，并通过单击安装。或者，如果您已安装扩展，可以直接从搜索结果中打开它。

- 任何卷。在这里您可以查看关联的容器。

- 文档。直接从 Docker Desktop 查找 Docker 官方文档的帮助。

## Docker 菜单

Docker Desktop 还包含一个托盘图标，称为 Docker 菜单 {{< inline-image src="../../assets/images/whale-x.svg" alt="whale menu" >}}，用于快速访问。

选择任务栏中的 {{< inline-image src="../../assets/images/whale-x.svg" alt="whale menu" >}} 图标以打开以下选项：

- **Dashboard**。这会带您进入 Docker Desktop 仪表板。
- **Sign in/Sign up**
- **Settings**
- **Check for updates**
- **Troubleshoot**
- **Give feedback**
- **Switch to Windows containers**（如果您使用 Windows）
- **About Docker Desktop**。包含您正在运行的版本信息，以及订阅服务协议等链接。
- **Docker Hub**
- **Documentation**
- **Extensions**
- **Kubernetes**
- **Restart**
- **Quit Docker Desktop**