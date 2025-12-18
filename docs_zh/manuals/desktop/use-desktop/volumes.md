---
description: 了解如何在 Docker Dashboard 的卷视图中进行操作
keywords: Docker Desktop Dashboard, 管理, 容器, GUI, 仪表板, 卷, 用户手册
title: 探索 Docker Desktop 中的卷视图
linkTitle: 卷
weight: 30
---

Docker Desktop 的 **Volumes（卷）** 视图允许你创建、检查、删除、克隆、清空、导出和导入 [Docker 卷](/manuals/engine/storage/volumes.md)。你还可以浏览卷中的文件和文件夹，并查看哪些容器正在使用它们。

## 查看你的卷

你可以查看以下卷信息：

- 名称：卷的名称。
- 状态：卷是否被容器使用。
- 创建时间：卷创建的时间。
- 大小：卷的大小。
- 定时导出：是否启用了定时导出。

默认情况下，**Volumes（卷）** 视图会显示所有卷的列表。

你可以通过以下方式过滤和排序卷，以及自定义显示的列：

- 按名称过滤卷：使用 **Search（搜索）** 字段。
- 按状态过滤卷：在搜索栏右侧，按 **In use（正在使用）** 或 **Unused（未使用）** 过滤卷。
- 排序卷：点击列名对卷进行排序。
- 自定义列：在搜索栏右侧，选择要显示的卷信息。

## 创建卷

你可以按以下步骤创建一个空卷。或者，如果你 [启动一个使用卷的容器](/manuals/engine/storage/volumes.md#start-a-container-with-a-volume)，而该卷尚不存在，Docker 会自动为你创建该卷。

要创建卷：

1. 在 **Volumes（卷）** 视图中，点击 **Create（创建）** 按钮。
2. 在 **New Volume（新卷）** 对话框中，指定卷名，然后点击 **Create（创建）**。

要将卷与容器一起使用，请参阅 [使用卷](/manuals/engine/storage/volumes.md#start-a-container-with-a-volume)。

## 检查卷

要查看特定卷的详细信息，从列表中选择一个卷。这将打开详细视图。

**Container in-use（正在使用的容器）** 选项卡显示使用该卷的容器名称、镜像名称、容器使用的端口号和目标。目标是容器内的路径，用于访问卷中的文件。

**Stored data（存储的数据）** 选项卡显示卷中的文件和文件夹以及文件大小。要保存文件或文件夹，右键点击文件或文件夹显示选项菜单，选择 **Save as...（另存为...）**，然后指定位置下载文件。

要从卷中删除文件或文件夹，右键点击文件或文件夹显示选项菜单，选择 **Delete（删除）**，然后再次选择 **Delete（删除）** 确认。

**Exports（导出）** 选项卡允许你 [导出卷](#export-a-volume)。

## 克隆卷

克隆卷会创建一个新卷，其中包含从克隆卷复制的所有数据。当克隆一个被一个或多个运行中容器使用的卷时，Docker 会临时停止容器，克隆数据，然后在克隆过程完成后重新启动容器。

要克隆卷：

1. 登录 Docker Desktop。你必须登录才能克隆卷。
2. 在 **Volumes（卷）** 视图中，点击要克隆的卷的 **Actions（操作）** 列中的 **Clone（克隆）** 图标。
3. 在 **Clone a volume（克隆卷）** 对话框中，指定 **Volume name（卷名）**，然后点击 **Clone（克隆）**。

## 删除一个或多个卷

删除卷会删除卷及其所有数据。当容器正在使用卷时，即使容器已停止，也无法删除卷。你必须先停止并删除使用该卷的任何容器，然后才能删除卷。

要删除卷：

1. 在 **Volumes（卷）** 视图中，点击要删除的卷的 **Actions（操作）** 列中的 **Delete（删除）** 图标。
2. 在 **Delete volume?（删除卷？）** 对话框中，点击 **Delete forever（永久删除）**。

要删除多个卷：

1. 在 **Volumes（卷）** 视图中，选择要删除的所有卷旁边的复选框。
2. 点击 **Delete（删除）**。
3. 在 **Delete volumes?（删除卷？）** 对话框中，点击 **Delete forever（永久删除）**。

## 清空卷

清空卷会删除卷的所有数据，但不会删除卷本身。当清空一个被一个或多个运行中容器使用的卷时，Docker 会临时停止容器，清空数据，然后在清空过程完成后重新启动容器。

要清空卷：

1. 登录 Docker Desktop。你必须登录才能清空卷。
2. 在 **Volumes（卷）** 视图中，选择要清空的卷。
3. 在 **Import（导入）** 旁边，点击 **More volume actions（更多卷操作）** 图标，然后选择 **Empty volume（清空卷）**。
4. 在 **Empty a volume?（清空卷？）** 对话框中，点击 **Empty（清空）**。

## 导出卷

你可以将卷的内容导出到本地文件、本地镜像，或 Docker Hub 中的镜像，或支持的云提供商。当从被一个或多个运行中容器使用的卷导出内容时，Docker 会临时停止容器，导出内容，然后在导出过程完成后重新启动容器。

你可以 [立即导出卷](#export-a-volume-now) 或 [安排定期导出](#schedule-a-volume-export)。

### 立即导出卷

1. 登录 Docker Desktop。你必须登录才能导出卷。
2. 在 **Volumes（卷）** 视图中，选择要导出的卷。
3. 选择 **Exports（导出）** 选项卡。
4. 选择 **Quick export（快速导出）**。
5. 选择是否将卷导出到 **Local or Hub storage（本地或 Hub 存储）** 或 **External cloud storage（外部云存储）**，然后根据你的选择指定以下附加详细信息。

   {{< tabs >}}
   {{< tab name="Local or Hub storage" >}}
   
   - **Local file（本地文件）**：指定文件名并选择文件夹。
   - **Local image（本地镜像）**：选择要导出内容的本地镜像。镜像中的任何现有数据将被导出的内容替换。
   - **New image（新镜像）**：为新镜像指定名称。
   - **Registry（注册表）**：指定 Docker Hub 仓库。

   {{< /tab >}}
   {{< tab name="External cloud storage" >}}

   你必须有 [Docker Business 订阅](../../subscription/details.md) 才能导出到外部云提供商。

   选择你的云提供商，然后指定上传到存储的 URL。参考以下云提供商的文档了解如何获取 URL。

   - Amazon Web Services：[使用 AWS SDK 创建 Amazon S3 的预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   - Microsoft Azure：[生成 SAS 令牌和 URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   - Google Cloud：[创建签名 URL 上传对象](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

   {{< /tab >}}
   {{< /tabs >}}

6. 点击 **Save（保存）**。

### 安排卷导出

1. 登录 Docker Desktop。你必须登录并拥有付费的 [Docker 订阅](../../subscription/details.md) 才能安排卷导出。
2. 在 **Volumes（卷）** 视图中，选择要导出的卷。
3. 选择 **Exports（导出）** 选项卡。
4. 选择 **Schedule export（安排导出）**。
5. 在 **Recurrence（重复）** 中，选择导出发生的频率，然后根据你的选择指定以下附加详细信息。

   - **Daily（每日）**：指定每天导出的时间。
   - **Weekly（每周）**：指定一周中的一天或多天，以及每周导出的时间。
   - **Monthly（每月）**：指定每月的日期和每月导出的时间。

6. 选择是否将卷导出到 **Local or Hub storage（本地或 Hub 存储）** 或 **External cloud storage（外部云存储）**，然后根据你的选择指定以下附加详细信息。
   
   {{< tabs >}}
   {{< tab name="Local or Hub storage" >}}
   
   - **Local file（本地文件）**：指定文件名并选择文件夹。
   - **Local image（本地镜像）**：选择要导出内容的本地镜像。镜像中的任何现有数据将被导出的内容替换。
   - **New image（新镜像）**：为新镜像指定名称。
   - **Registry（注册表）**：指定 Docker Hub 仓库。

   {{< /tab >}}
   {{< tab name="External cloud storage" >}}

   你必须有 [Docker Business 订阅](../../subscription/details.md) 才能导出到外部云提供商。

   选择你的云提供商，然后指定上传到存储的 URL。参考以下云提供商的文档了解如何获取 URL。

   - Amazon Web Services：[使用 AWS SDK 创建 Amazon S3 的预签名 URL](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   - Microsoft Azure：[生成 SAS 令牌和 URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   - Google Cloud：[创建签名 URL 上传对象](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

   {{< /tab >}}
   {{< /tabs >}}

7. 点击 **Save（保存）**。

## 附加资源

- [持久化容器数据](/get-started/docker-concepts/running-containers/persisting-container-data.md)
- [使用卷](/manuals/engine/storage/volumes.md)