---
description: 了解 Docker Hub 中的个人仓库设置
keywords: Docker Hub, Hub, 仓库, 设置
title: 仓库的个人设置
linkTitle: 个人设置
toc_max: 3
weight: 50
---

对于您的账户，您可以设置仓库的个人设置，包括默认仓库隐私和自动构建通知。

## 默认仓库隐私

在 Docker Hub 中创建新仓库时，您可以指定仓库的可见性。您也可以随时在 Docker Hub 中更改仓库的可见性。

当您使用 `docker push` 命令推送一个尚不存在的仓库时，此默认设置非常有用。在这种情况下，Docker Hub 会使用您的默认仓库隐私设置自动创建该仓库。

### 配置默认仓库隐私

1. 登录到 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Settings** > **Default privacy**。
3. 选择任何新创建仓库的 **Default privacy**。

   - **Public（公开）**：所有新仓库都会出现在 Docker Hub 搜索结果中，并且每个人都可以拉取。
   - **Private（私有）**：所有新仓库不会出现在 Docker Hub 搜索结果中，仅对您和协作者可见。此外，如果仓库创建在组织命名空间中，则只有具有相应角色或权限的用户才能访问。

4. 选择 **Save（保存）**。

## 自动构建通知

您可以使用自动构建功能，通过电子邮件接收所有仓库的通知。

### 配置自动构建通知

1. 登录到 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories** > **Settings** > **Notifications**。
3. 选择要通过电子邮件接收的通知类型。

   - **Off（关闭）**：不接收任何通知。
   - **Only failures（仅失败）**：仅接收构建失败的通知。
   - **Everything（全部）**：接收成功和失败构建的通知。

4. 选择 **Save（保存）**。