---
title: '管理 Docker Hardened Images 和 charts <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linktitle: 管理 images 和 charts
description: 了解如何在组织中管理镜像的和自定义的 Docker Hardened Images。
keywords: 管理 docker hardened images, 自定义 hardened images
weight: 35
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

在 Docker Hub 的 **Manage** 页面上，您可以管理组织中的镜像 DHI 仓库、镜像 DHI chart 仓库以及自定义内容。

## 管理镜像的 Docker Hardened Image 仓库

要管理镜像的 DHI 仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Mirrored Images**。
6. 选择您要管理的仓库所在行最右侧列的菜单图标。

   在这里，您可以：

   - **Customize**：基于源仓库创建自定义镜像。
   - **Stop mirroring**：停止镜像该 DHI 仓库。

## 管理自定义的 Docker Hardened Image 仓库

要管理自定义的 DHI 仓库：

1. 访问 [Docker Hub](https://hub.docker.com) 并登录。
2. 选择 **My Hub**。
3. 在命名空间下拉菜单中，选择您的组织。
4. 选择 **Hardened Images** > **Manage**。
5. 选择 **Customizations**。

   在此页面上，您可以查看自定义的 DHI 仓库。

6. 选择您要管理的仓库所在行最右侧列的菜单图标。

   在这里，您可以：

   - **Edit**：编辑自定义镜像。
   - **Create new**：基于源仓库创建新的自定义镜像。
   - **Delete**：删除自定义镜像。