---
description: 了解如何在 Docker Hub 上归档或取消归档仓库
keywords: Docker Hub, Hub, 仓库, 归档, 取消归档
title: 归档或取消归档仓库
linkTitle: 归档
toc_max: 3
weight: 35
---

您可以在 Docker Hub 上归档仓库，将其标记为只读状态，并表明它不再被积极维护。这有助于防止在工作流中使用过时或不受支持的镜像。如有需要，已归档的仓库也可以被取消归档。

Docker Hub 会通过在 [**仓库**页面](https://hub.docker.com/repositories/) 上显示一个图标（{{< inline-image src="./images/outdated-icon.webp" alt="outdated icon" >}}）来突出显示那些超过一年未更新的仓库。建议您检查这些被突出显示的仓库，如有必要，请将其归档。

当仓库被归档时，会发生以下情况：

- 仓库信息无法被修改。
- 无法向仓库推送新镜像。
- 在公共仓库页面上会显示一个 **已归档** 标签。
- 用户仍然可以拉取镜像。

您可以取消归档已归档的仓库，以移除归档状态。当取消归档时，会发生以下情况：

- 仓库信息可以被修改。
- 可以向仓库推送新镜像。
- 在公共仓库页面上会移除 **已归档** 标签。

## 归档仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   该仓库的 **General** 页面会出现。

4. 选择 **Settings** 选项卡。
5. 选择 **Archive repository**。
6. 输入您的仓库名称以确认。
7. 选择 **Archive**。

## 取消归档仓库

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表会出现。

3. 选择一个仓库。

   该仓库的 **General** 页面会出现。

4. 选择 **Settings** 选项卡。
5. 选择 **Unarchive repository**。