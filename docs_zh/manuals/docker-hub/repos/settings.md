---
description: 了解 Docker Hub 中的个人仓库设置
keywords: Docker Hub, Hub, 仓库, 设置
title: 仓库个人设置
linkTitle: 个人设置
toc_max: 3
weight: 50
---

对于您的账户，您可以为仓库设置个人偏好，包括默认仓库隐私设置和自动构建通知。

## 默认仓库隐私设置

在 Docker Hub 中创建新仓库时，您可以指定仓库的可见性。您也可以随时在 Docker Hub 中更改可见性设置。

如果您使用 `docker push` 命令推送到尚不存在的仓库，默认设置会非常有用。在这种情况下，Docker Hub 会自动使用您的默认仓库隐私设置创建该仓库。

### 配置默认仓库隐私设置

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Settings** > **Default privacy**。
3. 为任何新创建的仓库选择 **Default privacy**。

   - **Public**：所有新仓库都会出现在 Docker Hub 搜索结果中，并且可以被所有人拉取。
   - **Private**：所有新仓库不会出现在 Docker Hub 搜索结果中，只有您和协作者可以访问。此外，如果仓库是在组织的命名空间中创建的，那么具有相应角色或权限的人员也可以访问该仓库。

4. 选择 **Save**。

## 自动构建通知

您可以为所有使用自动构建功能的仓库配置电子邮件通知。

### 配置自动构建通知

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories** > **Settings** > **Notifications**。
3. 选择要通过电子邮件接收的通知类型。

   - **Off**：不发送通知。
   - **Only failures**：仅发送构建失败的通知。
   - **Everything**：发送构建成功和失败的通知。

4. 选择 **Save**。