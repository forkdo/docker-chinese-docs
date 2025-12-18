---
title: '使用 Docker Hardened Images 的扩展生命周期支持 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linktitle: 使用扩展生命周期支持
description: 了解如何在 Docker Hardened Images 中使用扩展生命周期支持 (ELS)。
weight: 39
keywords: 扩展生命周期支持, docker 硬化镜像, 容器安全, 镜像生命周期, 漏洞管理
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

通过 Docker Hardened Images 订阅附加组件，您可以使用 Docker Hardened Images 的扩展生命周期支持 (ELS)。ELS 为已终止生命周期 (EOL) 的镜像版本提供安全补丁，让您在按自己的时间表规划升级的同时，保持安全、合规的运行。您可以像使用其他 Docker Hardened Image 一样使用 ELS 镜像，但必须为要使用 ELS 的每个仓库启用 ELS。

## 发现支持 ELS 的仓库

要查找支持 ELS 的镜像：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 在 **Filter by** 中，选择 **Extended Lifecycle Support**。

## 为仓库启用 ELS

要为仓库启用 ELS，组织所有者必须将该仓库[镜像](./mirror.md)到您的组织中。

镜像时启用 ELS 的步骤：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库以查看其详细信息。
6. 选择 **Use this image** > **Mirror repository**。
7. 勾选 **Enable support for end-of-life versions**，然后按照屏幕上的说明操作。

## 为仓库禁用 ELS

要为仓库禁用 ELS，您必须在镜像仓库的 **Settings** 选项卡中取消勾选 ELS 选项，或停止镜像该仓库。要停止镜像，请参阅[停止镜像仓库](./mirror.md#stop-mirroring-a-repository)。

更新设置的步骤：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Repositories**，然后选择镜像的仓库。
5. 选择 **Settings** 选项卡。
6. 取消勾选 **Mirror end-of-life images** 选项。

## 管理 ELS 仓库

您可以像管理其他镜像 DHI 仓库一样查看和管理您的 ELS 镜像仓库。更多详细信息，请参阅 [管理镜像](./manage.md)。