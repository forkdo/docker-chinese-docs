---
description: 了解如何删除镜像标签。
keywords: Docker Hub, Hub, tags, delete
title: 镜像管理
linktitle: 镜像管理
weight: 12
---

{{< summary-bar feature_name="Image management" >}}

镜像（Images）和镜像索引（Image indexes）是仓库中容器镜像的基础。下图展示了镜像和镜像索引之间的关系。

  ![a pretty wide image](./images/image-index.svg)

这种结构通过单一引用实现了多架构支持。需要注意的是，镜像并不总是由镜像索引引用。图中展示了以下对象：

- **镜像索引 (Image index)**：指向多个特定架构镜像（如 AMD 和 ARM）的镜像，使得单一引用可以在不同平台上工作。
- **镜像 (Image)**：包含特定架构和操作系统实际配置及层的独立容器镜像。

## 管理仓库镜像和镜像索引

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 在列表中，选择一个仓库。
4. 选择 **Image Management**。
5. 搜索、筛选或排序项目。
   - **搜索 (Search)**：在列表上方的搜索框中指定搜索内容。
   - **筛选 (Filter)**：在 **Filter by** 下拉菜单中，选择 **Tagged**、**Image index** 或 **Image**。
   - **排序 (Sort)**：选择 **Size**、**Last pushed** 或 **Last pulled** 的列标题。

   > [!NOTE]
   >
   > 超过 6 个月未被拉取的镜像会在 **Status** 列中标记为 **Stale**。

6. **可选**。删除一个或多个项目。
   1. 选中列表中项目旁边的复选框。选择任何顶级索引也会删除任何未在其他地方引用的基础镜像。
   2. 选择 **Preview and delete**。
   3. 在出现的窗口中，确认将要删除的项目以及将要回收的存储空间量。
   4. 选择 **Delete forever**。

   > [!NOTE]
   >
   > 如果您想批量删除，可以使用[删除 API 端点](/reference/api/registry/latest/#tag/delete)。