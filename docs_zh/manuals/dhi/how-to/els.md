---
title: 使用 Docker Hardened Images 的扩展生命周期支持 <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>
linktitle: 使用扩展生命周期支持
description: 了解如何将扩展生命周期支持与 Docker Hardened Images 结合使用。
weight: 39
keywords: extended lifecycle support, docker hardened images, container security, image lifecycle, vulnerability management
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

通过 Docker Hardened Images 订阅附加组件，您可以将扩展生命周期支持 (ELS) 用于 Docker Hardened Images。ELS 为生命周期结束 (EOL) 的镜像版本提供安全补丁，让您在按照自己的时间表规划升级的同时，保持安全、合规的运营。您可以像使用任何其他 Docker Hardened Image 一样使用 ELS 镜像，但您必须为要使用 ELS 的每个仓库启用 ELS。

## 发现支持 ELS 的仓库

要查找支持 ELS 的镜像：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 在 **Filter by** 中，选择 **Extended Lifecycle Support**。

## 为仓库启用 ELS

要为仓库启用 ELS，组织所有者必须将仓库[镜像](./mirror.md)到您的组织。

要在镜像时启用 ELS：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Catalog**。
5. 选择一个 DHI 仓库以查看其详细信息。
6. 选择 **Use this image** > **Mirror repository**。
7. 选择 **Enable support for end-of-life versions**，然后按照屏幕上的说明操作。

## 为仓库禁用 ELS

要为仓库禁用 ELS，您必须在镜像仓库的 **Settings** 选项卡中取消选中 ELS 选项，或者停止镜像该仓库。要停止镜像，请参阅[停止镜像仓库](./mirror.md#stop-mirroring-a-repository)。

要更新设置：

1. 前往 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Repositories**，然后选择镜像的仓库。
5. 选择 **Settings** 选项卡。
6. 取消选中 **Mirror end-of-life images** 选项。

## 管理 ELS 仓库

您可以像管理任何其他镜像的 DHI 仓库一样，查看和管理带有 ELS 的镜像仓库。更多详情，请参阅[管理镜像](./manage.md)。